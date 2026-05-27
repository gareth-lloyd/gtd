---
area: null
contexts: []
created: 2026-05-27 15:09:18.754228
defer_until: null
due: null
energy: low
id: 2026-05-27T1509-clicking-defer-in-inbox-no-longer-hides-the-item-p
order: -1
output: |
  ## Agent run 2026-05-27T15:13

  **Root cause confirmed.** The grey-out commit (33662505 "feat(frontend):
  grey out inbox rows on process instead of removing") routed inline
  patches through `invalidateItemQueriesPreservingInbox`, so the inbox
  list cache no longer refetches on an inline edit. But `markProcessed`
  was only called from `WorkflowActions` (move/complete/delete) — not
  from `useItemPatch`. Result: clicking a defer preset on an inbox row
  silently set `defer_until` on the server, kept the row in the cached
  list, AND did not grey it out. So nothing visibly happened.

  **Fix:** in `frontend/src/ItemEdit.tsx` `useItemPatch.doFlush`, after a
  successful PATCH while on the inbox route, also call
  `markProcessed(itemId)` when the resulting item is hidden by defer
  (future `defer_until` and not overdue — reuses the existing
  `isHiddenByDefer` helper). Stashed `markProcessed` in a ref so the
  callback identity stays stable and doesn't reset the debounce timer.

  **Tests:** added 4 cases to `frontend/src/ItemEdit.test.tsx` under
  "useItemPatch — defer on inbox marks processed":
    1. future defer on /inbox → marks processed
    2. future defer on /next  → does NOT mark processed
    3. clearing defer on /inbox → does NOT mark processed
    4. past defer on /inbox → does NOT mark processed (not actually hidden)

  Confirmed red→green: case 1 failed before the fix, all 4 pass after.
  Full vitest run: 137/137. Typecheck, lint, and `npm run build` clean.

  **Files changed:**
    - frontend/src/ItemEdit.tsx  (~10 lines: ref + conditional markProcessed)
    - frontend/src/ItemEdit.test.tsx (new describe block, ~85 lines)

  **Not fixed (related but separate):** the same class of bug applies to
  any inline edit on /inbox that the server-side default list filter
  would exclude — most notably patching `project` to a non-null value
  (auto-moves the item to /next, but the row stays visible in the
  cached inbox list and is not greyed out). Left alone here since the
  task is specifically about defer. Flag if you want me to extend the
  same treatment to project moves.
project: 2026-04-27-gtd
source_id: null
tags: []
time_minutes: 5
title: Clicking defer in inbox no longer hides the item (probably result of the new
  "grey out" behavior
updated: 2026-05-27 15:13:00.000000
waiting_on: null
waiting_since: null
working_on: false
---