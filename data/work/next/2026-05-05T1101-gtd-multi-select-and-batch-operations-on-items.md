---
area: engineering
contexts:
- deep
created: 2026-05-05 11:01:00
defer_until: null
due: null
energy: high
id: 2026-05-05T1101-gtd-multi-select-and-batch-operations-on-items
order: null
project: 2026-04-27-gtd
source_id: null
tags:
- gtd-meta
- frontend
- backend
time_minutes: 240
title: 'GTD: multi-select and batch operations on items'
updated: 2026-05-05 15:13:45.793830
waiting_on: null
waiting_since: null
working_on: false
---

**Problem.** No way to defer / move / complete / delete N items at
once. Every action is a single-item click + round-trip. Friction
spikes during weekly review and mid-week triage.

**Approach.**
- **Backend.** New endpoint
  `POST /api/envs/<env>/items/batch/` taking
  `{ ids: string[], action: "move"|"defer"|"complete"|"delete",
  payload: {...} }`. New service method
  `GtdService.batch_apply()` that loops over `update`/`move`/`delete`,
  collects per-id results, returns
  `{ succeeded: [...], failed: [{id, error}] }`. Reuse existing
  service methods — don't duplicate validation logic.
- **Frontend.** Add `selectedIds: Set<string>` to
  `SelectionContext`. `Shift+Click` extends; `x` toggles current
  item. Floating action bar
  (`frontend/src/BatchActionBar.tsx`) appears at bottom of viewport
  when `selectedIds.size > 1`. Buttons: Defer, Move, Complete,
  Delete. Reuse `WorkflowActions` patterns and existing date picker.
- Toast on completion: "5 items deferred (1 failed)" with retry
  affordance.

**Verification.**
- Unit tests for `batch_apply()` in `gtd_core/tests/`
- DRF endpoint tests in `gtd_api/tests/`
- Component test for `BatchActionBar`
- Playwright spec covering shift-click selection + batch defer

**Pairs naturally with item #5 (`/gtd-defer` skill).**

**Size.** L (~4h)