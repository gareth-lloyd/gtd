---
area: null
contexts: []
created: 2026-06-17 13:52:49.935120
defer_until: null
due: null
energy: low
id: 2026-06-17T1352-reordering-in-a-project-does-not-seem-to-work
order: 10
output: |
  ## Agent run 2026-06-17T13:56

  ### TL;DR
  Reordering DOES persist — the backend, API and service layers are all
  correct. The complaint is a frontend perception bug: after a successful
  drag the list briefly snaps back to the pre-drag order before settling
  into the new order, which reads as "it didn't take".

  ### Evidence the data layer works
  - Repro on a copy of real data: dragged the last action to the front via
    `GtdService.reorder_project_items`, then re-read via
    `actions_for_project` — the new sequence is reflected exactly
    (order rewritten 1..N, sort honours it).
  - `git diff` on this project's items shows the reorder you did today
    (updated 2026-06-17 13:53) actually landed: orders were rewritten to a
    clean 1..19, e.g. `merge -> search -> merge` went from `order: -22` to
    `order: 1`. So your drag persisted to disk.
  - Backend sort key (`gtd_core/service.py:601` `_item_sort_key`) sorts
    ordered items by `(overdue_rank, 0, order, id)`; none of these items
    have due dates, so it's a pure `order` sort. No interference.

  ### Root cause of the perceived failure (frontend)
  `frontend/src/ProjectComponents.tsx:367-377`, `reorderMut.onSuccess`:
  ```
  onSuccess: () => {
    setLocalFullOrder(null);              // clears optimistic order SYNCHRONOUSLY
    invalidateProjectQueries(qc, ...);    // refetch is ASYNC
    qc.invalidateQueries({ queryKey: ["items", env] });
  }
  ```
  The optimistic `localFullOrder` (which shows the dragged order
  immediately) is cleared the instant the mutation resolves, but the
  `["project", env, projectId, "full"]` query only refetches afterwards.
  React Query keeps the *old* `data` on screen during a background refetch,
  so for the duration of that round-trip the list renders the STALE
  pre-drag order — a visible snap-back — then jumps to the correct order
  once the refetch lands. On a slow/janky request this looks like the
  reorder was rejected.

  ### Recommended fix (not yet applied)
  Don't drop the optimistic order until the fresh data is in. Either:
  - In `onSuccess`, write the new order straight into the project cache
    with `qc.setQueryData(["project", env, projectId, "full"], ...)` so
    there's no stale window, OR
  - Move `setLocalFullOrder(null)` into `onSettled` and `await` the
    invalidation/refetch before clearing, keeping the optimistic order
    visible until real data replaces it.
  This is a ~5-line change in `SortableActionList`. The duplicate item
  `2026-06-17T1352-re-ordering-within-a-project-by-drag-and-drop-does`
  is the same report.

  ### Caveat
  I confirmed the backend round-trip and the persisted-orders evidence
  directly. The snap-back is diagnosed from the code path, not from a live
  drag in a browser (drag-and-drop is hard to drive headlessly). If you
  want, I can implement the fix and verify with a Playwright e2e drag.
project: 2026-04-27-gtd
source_id: null
tags: []
time_minutes: 5
title: reordering in a project does not seem to work
updated: 2026-06-17 14:02:46.008791
waiting_on: null
waiting_since: null
working_on: false
---