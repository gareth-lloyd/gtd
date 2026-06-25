---
area: null
contexts: []
created: 2026-05-19 14:55:35.588068
defer_until: null
due: null
energy: low
id: 2026-05-19T1455-merge-search-merge
order: 2
output: ''
project: 2026-04-27-gtd
source_id: null
tags: []
time_minutes: 5
title: merge -> search -> merge
updated: 2026-06-25 12:17:54.394019
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