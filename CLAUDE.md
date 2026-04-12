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
uv sync                                    # Python deps
cd frontend && npm install && npm run build # Frontend (once)
uv run manage.py runserver 8765            # Serve everything
```

For frontend hot-reload during dev: run `npm run dev` in frontend/ alongside
the Django server.

## Testing

```sh
uv run pytest                    # backend (models, storage, repo, service, API, snapshot, importer)
cd frontend && npm test          # frontend (vitest + testing-library)
uv run ruff check .              # lint
```

All backend tests use `tmp_path` fixtures — no test touches real data.
Frontend tests use jsdom + mocked API.

## Key conventions

- **Status from path**: an item's status (inbox/next/waiting/...) is the name
  of its parent directory. It is NOT stored in YAML frontmatter. On load,
  `storage.load_item(path, bucket)` receives the bucket as an argument.

- **Filename = ID**: `YYYY-MM-DDTHHMM-slug.md`. Immutable after creation.
  Title can change freely in frontmatter; filename never does.

- **Contexts are strict**: validated against `data/<env>/config.yml` on every
  write. Unknown contexts raise `ValueError`.

- **Energy ceiling**: filtering by energy=low returns only low items.
  energy=high returns low+medium+high. It's "max energy I can spend", not
  "exactly this level".

- **Soft delete**: `service.delete()` moves to trash. `service.purge()` is
  the irreversible hard delete. API DELETE returns the trashed item.

- **Natural-language dates**: `due` and `defer_until` accept strings like
  "next friday", "2w", "end of month", or ISO dates. The service layer
  parses them via `gtd_core/dates.py` (dateparser + preprocessor).

- **Recurring templates**: files in `data/<env>/templates/` with a
  `recurrence:` field (daily/weekly/monthly/etc). Every snapshot (Sync
  button or `manage.py snapshot`) spawns inbox items for due templates
  before committing.

- **Data commits**: `data/` is tracked in the same git repo as code. Use
  `uv run manage.py snapshot` (or the Sync button in the UI) to commit
  data changes separately from code. Never mix code and data in one commit.

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
- `/gtd-check` — lint + test + build pipeline
