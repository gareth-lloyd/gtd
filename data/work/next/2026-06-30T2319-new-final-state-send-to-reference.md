---
area: null
contexts: []
created: 2026-06-30 23:19:05.582675
defer_until: null
due: null
energy: low
id: 2026-06-30T2319-new-final-state-send-to-reference
order: null
output: |
  ## Agent run 2026-07-01 14:43

  Implemented "send to reference" as a workflow action. Shipped, not just proposed
  — the change was small and the backend already supported it.

  **Key finding: no backend work needed.** `service.move()` already accepts any
  Bucket including `REFERENCE`, and the generic `POST /envs/<env>/items/<id>/move/`
  endpoint already routes there. `reference` was already a first-class Bucket
  (`gtd_core/models.py:41`) and a valid `api.ts` Bucket type. The gap was purely
  that the UI never surfaced "reference" as a move target. So this was a
  frontend-only change in `frontend/src/WorkflowActions.tsx`.

  **What I changed (TDD — tests written, then component):**
  1. Active items (inbox/next/waiting/someday): added `reference` to the shared
     move-button row, so any active item now shows a `→ reference` button
     alongside `→ next/waiting/someday`. (Filing straight to reference — "not
     actionable, worth keeping" — is a legit GTD move from any active bucket.)
  2. Completed items (archive branch): this covers your follow-up
     ("it should also be possible to send a completed item to reference"). The
     archive branch previously offered only `↺ uncomplete` and `Delete`. Added a
     `→ reference` button there, so useful agent output that landed in archive can
     be re-filed as reference without first uncompleting it.

  Note: this adds a *manual* "→ reference" action; it does NOT change the default
  `✓ done` behaviour (still → archive) or auto-file agent output. If you wanted the
  agent-launch exit protocol to auto-route items with useful `output:` to reference
  instead of you archiving them, that'd be a separate, larger change (touching the
  agent protocol + likely a new completion mode). Flagging in case that was the
  original intent — happy to spec/build it. What I built is the on-demand version.

  **Files:**
  - `frontend/src/WorkflowActions.tsx` — added `→ reference` in both the active
    move-row and the archive branch.
  - `frontend/src/WorkflowActions.test.tsx` — new tests: `→ reference` from an
    active item calls `moveItem(...,'reference')`; `→ reference` from a completed
    (archive) item does too; updated the archive-bucket test for the new button set.

  **Verification:** `npm test` → 146 passed (13 files). `npm run lint`,
  `npm run typecheck`, `npm run build` all clean (pre-existing >500kB chunk-size
  warning only). Backend untouched, so `uv run pytest` not required for this change.

  **Not committed** — left in the working tree for you to review/commit. This is a
  code change (frontend/), so commit it as code, separate from any `data/` snapshot.
project: 2026-04-27-gtd
source_id: null
tags: []
time_minutes: 5
title: New final state - send to reference
updated: 2026-07-01 14:43:10.355892
waiting_on: null
waiting_since: null
working_on: false
---

Instead of just going to complete, useful agent output could be filed as reference