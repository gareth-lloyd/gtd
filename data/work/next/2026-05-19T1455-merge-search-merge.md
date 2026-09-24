---
area: null
completed_at: null
contexts: []
created: 2026-05-19 14:55:35.588068
defer_until: null
due: null
energy: low
id: 2026-05-19T1455-merge-search-merge
order: 2
output: "## Agent run 2026-09-24T10:12:37\n\nImplemented the merge feature end to
  end, mirroring the AI-capture pipeline. Committed to `main` as 97c5b7b4 (code only;
  `data/` left out of the commit). Local service restarted via `make restart-service`
  and answering on :8765.\n\n### Backend\n- `gtd_core/ai.py`: `AiMergeResult`, `_MERGE_JSON_SCHEMA`,
  `ai_merge(target, source, today, config_dir, model)`, `_build_merge_prompt`. Factored
  the subprocess call into `_run_claude()` and the fence-strip/JSON parse into `_parse_json_object()`,
  both now shared with `ai_capture`. Same `GTD_AI_STUB_RESPONSE` seam and `AiCapture*`
  exception hierarchy.\n- `gtd_core/service.py`: `merge_items(env, target_id, source_id,
  model=\"\")`. Rejects self-merge (ValueError), missing either side (KeyError). Patch
  = AI title/body + order-preserving union of contexts (filtered against config) and
  tags + source value for any *falsy* target scalar (energy, time_minutes, due, defer_until,
  waiting_on). Applied via `update()`, then `delete()` trashes the source. Ordering
  means an AI failure leaves both items untouched. Passes the env's `claude_config_dir`
  so `home` merges use the personal account.\n- `gtd_api`: `ItemMergeSerializer`,
  `item_merge` view (404 missing / 400 self-or-blank / 422 bad JSON / 502 CLI / 503
  no CLI), route `items/<id>/merge/`. Added `merge_items` to the method table in `gtd_core/CLAUDE.md`.\n\n###
  Frontend\n- `api.mergeItem(env, id, sourceId)`.\n- New `MergeButton.tsx`: \"⇄ merge
  other\" button → overlay (reuses `.capture-overlay`/`.capture`) with autofocused
  search input backed by `useSearchIndex` (corpus only fetched once opened). Results
  keep `kind===\"item\"`, exclude the current item, cap at 20, show status + project
  chips. Click → `confirm()` naming both items and warning the source will be trashed
  → mutation → invalidates queries for both ids → success toast → close. Escape /
  backdrop click closes. Button shows busy while pending.\n- Mounted in `WorkflowActions`
  normal branch after the two agent buttons. Trash/archive branches unchanged.\n\n###
  Tests (red/green)\n- `gtd_core/tests/test_merge.py` (14): stub seam, missing title
  → 422-class error, null body → \"\", no CLI → NotConfigured, prompt embeds both
  items; service: identity/project/status preserved, source in trash, contexts+tags
  union in order, unknown source context dropped, empty scalars filled, non-empty
  untouched, self-merge ValueError, missing target/source KeyError with no side effects,
  AI failure leaves both untouched.\n- `gtd_api/tests/test_api.py::TestItemMerge`
  (6): 200 happy path + source in trash, 404 missing source/target, 400 blank source_id,
  400 self-merge, 422 garbage AI output.\n- `frontend/src/MergeButton.test.tsx` (5):
  corpus not fetched until opened, picker filters + excludes current item + shows
  status chip, select → confirm → `api.mergeItem` → toast + invalidations + close,
  declined confirm leaves picker open, Escape closes.\n- Note: the frontend test file
  and component were written in the same step, so I did not observe the frontend red
  phase separately. Backend red was observed.\n\n### Verification\n- `uv run pytest`:
  649 passed (full suite, before the 2 test-only line-wrap edits; merge subsets re-run
  green after).\n- `cd frontend && npm test`: 163 passed. `npm run build`: ok.\n-
  `./scripts/lint.sh`: all clear (ruff, pyright, eslint, prettier, tsc). Pre-commit
  hooks passed on commit.\n- HTTP smoke on a throwaway `GTD_DATA_ROOT` with `GTD_AI_STUB_RESPONSE`:
  POST merge → 200 with merged title/body, contexts `[calls, office]`, energy filled
  from source, status unchanged, source file in `trash/`; self-merge → 400; missing
  source → 404.\n\n### Not done / for you\n- Manual UI check against real data with
  the real `claude` CLI (spec step 3). I did not run this because it would move a
  real item to trash. Open any next-action → \"⇄ merge other\" → search → pick → confirm.\n-
  No e2e Playwright spec added (spec marked it optional). Easy follow-up: the stub
  env var is already in the Playwright webServer config.\n- Prompt quality with the
  real model is untested; if it over-trims, the \"err STRONGLY toward including ALL
  information\" rule in `_build_merge_prompt` is the knob.\n\n## Agent run 2026-09-24T10:27:07\n\nUser
  feedback after trying the first cut: `{\"error\":\"Claude CLI timed out after 30s\"}`.
  Direction: don't merge inside the web request; open an agent session like the \U0001F916
  agent button. Redesigned accordingly, committed to `main` as c723150f, service restarted.\n\n###
  New flow\n1. \"⇄ merge other\" → search picker → pick → confirm → `POST /items/<id>/merge/`
  `{source_id, target?}`.\n2. `service.launch_merge_session()` validates both ids,
  pins the current item (`working_on: true`), builds a prompt with `agent_launch.build_merge_prompt()`,
  and opens iTerm (default) or the desktop app in the gtd repo root. Returns 204 immediately.
  Nothing is merged in the request.\n3. The agent reads both files, composes one merged
  title + body (same rules as before: de-dup but err strongly toward keeping everything,
  prefer the current title, verb-first, no invention), writes the body to a temp file
  and runs\n   `uv run manage.py merge_items <env> <target_id> <source_id> --title
  '…' --body-file …`.\n4. That command → `service.merge_items(title=, body=)`, now
  a deterministic apply step with no AI: sets title/body, unions contexts (filtered
  vs config) and tags, fills empty scalars from the source, keeps project + bucket,
  moves the source to trash.\n5. The agent appends a `## Agent run` section to the
  target's `output:` (what was folded in + the source id for recovery from trash),
  restores `working_on`, bumps `updated:`, stops. The prompt forbids `mv`/hand-editing
  fields — the command is the only sanctioned write.\n\n### Removed\n`ai_merge` /
  `_build_merge_prompt` / `AiMergeResult` and the `claude -p` merge path are gone
  from `gtd_core/ai.py`. The `_run_claude` + `_parse_json_object` refactor stays (still
  used by AI capture).\n\n### Tests\n- `gtd_core/tests/test_merge.py` (27): apply
  semantics as before plus blank-title rejection; `manage.py merge_items` via `call_command`
  (body file, inline body, missing item → CommandError); prompt content (both items
  + paths, exact apply command, rules, no-mv/no-edit, exit protocol, external-write
  ban); launcher (cwd = repo root, pins target only, prior pin preserved, desktop
  target, env `claude_config_dir`, self/missing rejected before pin or launch).\n-
  `gtd_api/tests/test_api.py::TestItemMerge` (9): 204 + target pinned + source untouched,
  desktop target, bad target 400, missing 404s, blank/self 400, 503/502 launch errors.\n-
  Frontend `MergeButton.test.tsx` updated for void return + \"Agent launched\" toast.\n\n###
  Verification\n- `uv run pytest`: 664 passed. `npm test`: 163 passed. `npm run build`:
  ok. `./scripts/lint.sh`: all clear.\n- Smoke on a throwaway `GTD_DATA_ROOT`: ran
  the exact `manage.py merge_items … --body-file` command → title/body set, contexts
  `[calls, office]`, energy filled, source in `trash/`.\n\n### For you\n- Try the
  real flow again: pick an item → \"⇄ merge other\" → pick → confirm → an iTerm tab
  should open in `~/projects/gtd`. The agent needs `uv` on PATH there (it will).\n-
  Only iTerm is wired from the button; the API accepts `target: \"desktop\"` if you
  want a desktop variant later.\n- Docs: new \"Merge items\" bullet in the root `CLAUDE.md`;
  `merge_items` + `launch_merge_session` in the `gtd_core/CLAUDE.md` method table.\n"
project: 2026-04-27-gtd
source_id: null
tags: []
time_minutes: 5
title: merge -> search -> merge
updated: 2026-09-24 10:27:07
waiting_on: null
waiting_since: null
working_on: false
---

# Merge Item Feature

## Context

When two GTD items describe the same work (a duplicate capture, an item that
belongs with an existing one), there's no way to fold one into the other — you
delete one and retype its notes into the other.

This adds a **merge** flow: while viewing an item ("current/target"), click
**"merge other"**, search for a second item ("source"), and the AI merges the
source's content into the current item. The current item's **project and bucket
(status) are preserved unconditionally**. The merge de-duplicates but errs
toward keeping everything from both. The source item is moved to **trash**
(reversible) once merged.

Mirrors the existing AI-capture pipeline end-to-end (prompt build → `claude`
CLI subprocess with a test stub seam → JSON parse → service method → DRF
endpoint → typed frontend client + button).

## Decisions

- **Source disposal:** move to trash via `service.delete()` (reversible).
- **Merge scope:** AI merges only prose (`title` + `body`). Code unions
  `contexts` & `tags` and fills any *empty* target scalar (`energy`,
  `time_minutes`, `due`, `defer_until`, `waiting_on`) from the source.
  `project` and `status` always stay the target's.
- **Button placement:** in `WorkflowActions` (detail-pane row + card hover).

## Backend

### 1. `gtd_core/ai.py` — new `ai_merge()` (mirror `ai_capture`)

- `AiMergeResult(title: str, body: str)` dataclass + `_MERGE_JSON_SCHEMA`.
- `ai_merge(*, target: Item, source: Item, today: date, model="") -> AiMergeResult`:
  reuse the `GTD_AI_STUB_RESPONSE` stub seam, `shutil.which("claude")` check,
  `subprocess.run([... -p prompt ...])` 30s timeout, existing exception
  hierarchy, and fence-stripping/`json.loads` parse (factor the shared parse).
- `_build_merge_prompt(*, target, source, today)`: show both items' title+body
  labelled; rules — one merged title + body; **de-dup but err strongly toward
  including ALL info from both**; prefer target's title unless source's clearly
  better (stay verb-first); merge bodies to clean markdown preserving every
  distinct note/link/checklist; don't invent. Returns only title+body.

### 2. `gtd_core/service.py` — `merge_items(env, target_id, source_id, model="")`

- Reject `target_id == source_id` (ValueError); `repo.get()` both (KeyError if missing).
- Lazy `from gtd_core.ai import ai_merge` (matches `capture_ai`).
- Call `ai_merge(...)`; build patch: title/body from AI; `contexts` =
  order-preserving union filtered vs `cfg.contexts`; `tags` = union; for
  energy/time_minutes/due/defer_until/waiting_on set from source only if target
  falsy. Apply via existing `self.update()` (reuses validation/date coercion/
  `updated` bump). Then `self.delete(env, source_id)` → trash. Return target.
- Add to method table in `gtd_core/CLAUDE.md`.

### 3. `gtd_api/` — endpoint

- `serializers.py`: `ItemMergeSerializer { source_id: CharField }`.
- `views.py`: `item_merge(request, env, item_id)` `@api_view(["POST"])` mirroring
  `items_capture_ai` exception→status mapping (503/422/502/500, KeyError→404,
  ValueError→400); success → `ItemSerializer(...).data` 200.
- `urls.py`: `items/<str:item_id>/merge/` next to `launch-agent/` + `move/`.

## Frontend

### 4. `frontend/src/api.ts`

```
mergeItem: (env, id, sourceId) =>
  request<Item>(`/envs/${env}/items/${id}/merge/`,
    { method: "POST", body: JSON.stringify({ source_id: sourceId }) })
```

### 5. `frontend/src/MergeButton.tsx` (new)

- `MergeButton({ env, item })` renders a **"merge other"** `<Button>`.
- Click opens a lightweight overlay (reuse `capture-overlay`/modal CSS):
  autofocus search `<input>` → results from existing
  `useSearchIndex(env, { enabled: open })` (`search.ts`), `index.search(query, 20)`,
  keep `kind==="item"`, **exclude current item id**, show title + status/project chip.
- Select → confirm (source will be trashed) → mutation:
  `invalidateItemQueries` for target + source, close, success toast. Use
  `<Button busy={mut.isPending}>`; global MutationCache handles error toasts.

### 6. `frontend/src/WorkflowActions.tsx`

Mount `<MergeButton env={env} item={item} />` in the normal branch next to
🤖 agent. Trash/archive branches unchanged.

## Tests (red/green TDD)

- `gtd_core/tests/test_merge.py`: stub `GTD_AI_STUB_RESPONSE` → target keeps
  project/status/id/created; title/body from stub; contexts/tags unioned;
  empty target scalars filled, non-empty untouched; source in trash. Plus
  `target==source`→ValueError, missing→KeyError, unknown source context dropped.
- `gtd_api/tests/test_api.py`: POST merge happy path → 200; missing source→404;
  empty source_id→400.
- Frontend `*.test.tsx`: MergeButton opens picker, filters mocked corpus,
  excludes current item, calls `api.mergeItem`, success toast.
- e2e (optional): full flow with `GTD_AI_STUB_RESPONSE` (already in Playwright
  webServer config).

## Verification

1. `uv run pytest gtd_core/tests/test_merge.py gtd_api/tests/test_api.py` (+ full `uv run pytest`).
2. `cd frontend && npm test` then `npm run build`.
3. Manual: `uv run manage.py runserver 8765`, select item → "merge other" →
   pick second → confirm; current item gains merged title/body, keeps project/
   bucket; source in trash.
4. `./scripts/lint.sh`.

## Critical files

- `gtd_core/ai.py` — `ai_merge`, `_build_merge_prompt`, `AiMergeResult`, shared parse.
- `gtd_core/service.py` — `merge_items` (uses existing `update`, `delete`).
- `gtd_api/views.py`, `serializers.py`, `urls.py` — endpoint.
- `frontend/src/api.ts` — `mergeItem`.
- `frontend/src/MergeButton.tsx` (new) — reuses `useSearchIndex`, `Button`, `toast`, `invalidateItemQueries`.
- `frontend/src/WorkflowActions.tsx` — mount the button.