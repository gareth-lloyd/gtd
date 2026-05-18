# GTD

Local Getting Things Done system backed by markdown + YAML frontmatter files.
Two interfaces on top of a shared service layer: a React web UI and direct
file access from Claude Code CLI sessions.

## Architecture

```
gtd_core/       Standalone Python library — all domain logic
  ↑ only dependency direction
gtd_api/        Thin DRF layer — HTTP ↔ service translation
frontend/       Vite + React + TypeScript SPA
gtd_site/       Django project glue (settings, root URLs, SPA serving)
data/           The actual GTD data (tracked in git)
```

`gtd_core` knows nothing about HTTP or Django. You can import it from scripts,
notebooks, or CLI sessions. The API only ever calls `GtdService` methods.

## Running

```sh
./scripts/setup-dev.sh                     # First clone: deps + pre-commit hook
uv run manage.py runserver 8765            # Serve everything
```

For frontend hot-reload during dev: run `npm run dev` in frontend/ alongside
the Django server.

## Testing

```sh
uv run pytest                    # backend (models, storage, repo, service, API, snapshot, importer)
cd frontend && npm test          # frontend (vitest + testing-library)
./scripts/lint.sh                # ruff + eslint + prettier + tsc (also auto-runs pre-commit)
./scripts/coverage.sh            # backend + frontend coverage summary
./scripts/e2e.sh                 # Playwright e2e against a throwaway env
```

## Linting

A single `pre-commit` umbrella covers both languages. One-time setup is
`./scripts/setup-dev.sh` (or `uv run pre-commit install`); thereafter
hooks fire on every `git commit`.

```sh
./scripts/lint.sh                # full battery, fail-fast (mirrors pre-commit)
uv run ruff check . --fix        # Python lint, auto-fix
uv run ruff format .             # Python format
uv run pyright                   # Python type-check (basic mode)
cd frontend && npm run lint:fix  # ESLint, auto-fix
cd frontend && npm run format    # Prettier, auto-fix
cd frontend && npm run typecheck # tsc --noEmit
```

Pyright runs in `basic` mode in both `scripts/lint.sh` and pre-commit
(whole-project, ~1.3s warm). Set `SKIP_TYPECHECK=1` to skip pyright +
tsc in `lint.sh` when iterating fast.

All backend tests use `tmp_path` fixtures — no test touches real data.
Frontend tests use jsdom + mocked API.

## E2E testing

Playwright drives a real browser against a Django server with
`GTD_DATA_ROOT` pointed at `frontend/e2e/.tmp/data/` (created fresh per
run, bucket dirs wiped per test). The AI capture endpoint is short-
circuited via the `GTD_AI_STUB_RESPONSE` env var — set in the Playwright
`webServer` config, it causes `gtd_core/ai.py:ai_capture()` to return the
value verbatim instead of shelling out to the `claude` CLI. Production
behaviour is unchanged when the var is unset.

Specs live in `frontend/e2e/*.spec.ts`. Run `./scripts/e2e.sh` (builds
then tests) or `cd frontend && npm run e2e:ui` for interactive mode.

## Key conventions

- **Status from path**: an item's status (inbox/next/waiting/...) is the name
  of its parent directory. It is NOT stored in YAML frontmatter. On load,
  `storage.load_item(path, bucket)` receives the bucket as an argument.
  Bucket dirs are `inbox`, `next`, `waiting`, `someday`, `reference`,
  `archive`, `trash`. `projects/` and `templates/` are sibling top-level
  dirs under `data/<env>/`, not buckets — projects/templates have their
  own dataclasses and storage helpers.

- **Filename = ID**: `YYYY-MM-DDTHHMM-slug.md`. Immutable after creation.
  Title can change freely in frontmatter; filename never does.

- **Contexts are strict**: validated against `data/<env>/config.yml` on every
  write. Unknown contexts raise `ValueError`.

- **Energy ceiling**: filtering by energy=low returns only low items.
  energy=high returns low+medium+high. It's "max energy I can spend", not
  "exactly this level".

- **Soft delete**: `service.delete()` moves to trash. `service.purge()` is
  the irreversible hard delete. API DELETE returns the trashed item.

- **Natural-language dates**: `due` accepts strings like "next friday", "2w",
  "end of month", or ISO dates (`parse_human_date` → `date`). `defer_until`
  additionally supports hour-level precision ("in 2 hours", "3h", "tomorrow
  9am", ISO datetime) via `parse_human_datetime` → `datetime`. Date-only
  inputs promote to midnight local time.

- **Project priority + due**: projects carry a `priority` (1-5, where 1 is
  most urgent) and an optional `due` date. The frontend sorts by priority
  then due. Priority has no automated effect — it's a sorting/visibility aid.

- **Next-actions cap per project**: projects carry `max_next_items: int | None`.
  `None` (default) means no cap — every ordered action is visible. `1`
  surfaces only the lowest-`order` incomplete item (classic "sequential"
  behaviour); completing it reveals the next. Higher values cap the next
  list to N items per project. Items have `order: int | None` used when a
  cap is set. `GET /items/?status=next` applies the cap by default;
  `?show_all=true` bypasses it (for reviews).

- **Recurring templates**: files in `data/<env>/templates/` with a
  `recurrence:` field (daily/weekly/monthly/etc). Every snapshot (Sync
  button or `manage.py snapshot`) spawns inbox items for due templates
  before committing.

- **Data commits**: `data/` is tracked in the same git repo as code. Use
  `uv run manage.py snapshot` (or the Sync button in the UI) to commit
  data changes separately from code. Never mix code and data in one commit.

- **AI capture**: a second capture mode that takes unstructured text and
  runs it through the `claude` CLI to extract a structured Item. The
  backend shells out to `claude -p "<prompt>"` (uses the user's Max plan,
  no API credits). Fuzzy project matching resolves freeform project names.
  If a project matches, the item auto-moves to `next`.
  Endpoint: `POST /api/envs/<env>/items/capture-ai/`.

- **Inline editing**: items use a dual-purpose `ItemCard` — collapsed
  shows chips, expanded shows live editors. All edits auto-save via
  debounced PATCH (500ms text, immediate discrete). No Save button.

- **Working-on pin**: items carry `working_on: bool` (default false). When
  set, the item pins to the very top of the next-actions list and bypasses
  its project's `max_next_items` cap. Auto-cleared on completion, on any
  move out of the next bucket, and when `defer_until` is set to a future
  datetime. Edits to title/body/contexts/etc leave it alone.

- **Agent launch**: the `🤖 agent` button on an item (next-actions card or
  detail pane) opens an interactive iTerm session running `claude
  --permission-mode auto` with a generated prompt. macOS-only — spawns
  iTerm via `osascript`. Endpoint: `POST /api/envs/<env>/items/<id>/
  launch-agent/` → `service.launch_agent_session()` →
  `agent_launch.build_prompt()` + `launch_claude_session()`. Launching
  sets the item's `working_on: true`. The prompt embeds the item
  title/body, project context (incl. `working_dir`), any prior `output:`,
  and strict guardrails: the agent does NOT decide when the task is done
  and must not make external/outbound writes without explicit in-session
  approval. Exit protocol the agent follows: append findings to `output:`
  (a new `## Agent run <ISO>` section if prior runs exist), set
  `working_on: false`, bump `updated:`, then stop — it never moves/
  archives/completes the item. The user reads the output and decides next
  steps. cwd precedence: project `working_dir` → `settings.GTD_AGENT_CWD`
  → `$HOME`. Errors surface as 503 (no `claude` CLI), 502 (osascript
  failed), 404 (item gone).

- **Project working dir**: projects carry `working_dir: str | None`. When
  an agent is launched (`🤖 agent`) for an item linked to a project that
  has `working_dir` set, the iTerm session `cd`s into that directory
  (`~` expanded) instead of the default agent cwd. Items not linked to
  such a project use the default. Editable in the project editor / new-
  project form.

- **Keyboard shortcuts** (when not focused in an input):
  - `C` — open capture bar (Regular mode)
  - `Shift+C` — open capture bar (Regular ↑ mode: float new item to top of inbox)
  - `A` — open capture bar (AI mode)
  - `/` — focus search
  - `F` — toggle working_on on the selected item
  - `Cmd/Ctrl+Enter` — save and close (in expanded item or capture bar)

## Working rules for Claude

- **Red/green TDD**: write a failing test first, then make it pass. This is
  the standard workflow for all code changes in this project.
- Run `uv run pytest` before committing code changes.
- Rebuild frontend after UI changes: `cd frontend && npm run build`.
- Don't modify `data/` files in code PRs — use `tmp_path` fixtures in tests.
- When reading GTD data in a CLI session, read the files under `data/`
  directly. No need to start the server or hit the API.
- See subdirectory CLAUDE.md files for layer-specific guidance.

## CLI skills

GTD workflow commands available from Claude Code sessions:

- `/gtd-review` — guided weekly review (inbox zero → projects → waiting → someday)
- `/gtd-capture <title>` — rapid-fire inbox capture
- `/gtd-dashboard` — text summary with counts and flags
- `/gtd-inbox` — interactive inbox processing
- `/gtd-coach` — LLM-powered triage that flags stale / vague / mis-bucketed items
  and walks through fixes one by one
- `/gtd-check` — lint + test + build pipeline
