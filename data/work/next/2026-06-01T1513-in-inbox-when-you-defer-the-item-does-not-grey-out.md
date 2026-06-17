---
area: null
contexts: []
created: 2026-06-01 15:13:04.708676
defer_until: null
due: null
energy: low
id: 2026-06-01T1513-in-inbox-when-you-defer-the-item-does-not-grey-out
order: 17
output: |
  ## Agent run 2026-06-01T15:18

  **Root cause found and fixed.** Deferring an inbox item *did* already mark
  the row "processed" (commit 08c14268, 2026-05-27), but it never cleared the
  selection — so the row stayed `.item.processed.selected`, and the CSS rule
  at styles.css:885-888 deliberately pins that combination to `opacity: 1`.
  Result: no visible grey-out.

  Contrast with "→ next", which greys out correctly because
  WorkflowActions.invalidate() (WorkflowActions.tsx:24) calls `select(null)`
  after marking the row processed. The defer path (useItemPatch.doFlush in
  ItemEdit.tsx) marked processed but skipped the deselect, so the still-
  selected row never dimmed.

  **Fix** (frontend/src/ItemEdit.tsx): in the defer-into-future branch of
  `doFlush`, after `markProcessed`, also call `select(null)` — mirroring the
  WorkflowActions flow. Wired `useSelection()` into the hook via a ref so the
  debounced callback identity stays stable. `useSelection` has a no-op
  default context, so consumers without a SelectionProvider (and existing
  tests) are unaffected.

  **TDD**: added a failing test in ItemEdit.test.tsx ("clears selection when
  deferring into the future on the inbox route"), then made it pass.

  **Verification**:
  - `npm test` → 141 passed (12 files)
  - `npm run typecheck` → clean
  - `npm run lint` → clean
  - `npm run build` → succeeds

  Files changed: frontend/src/ItemEdit.tsx, frontend/src/ItemEdit.test.tsx.
  Frontend rebuilt (dist/). Not committed — left for your review.
project: 2026-04-27-gtd
source_id: null
tags: []
time_minutes: 5
title: In inbox, when you defer, the item does not "grey out" like it does when adding
  to next
updated: 2026-06-17 13:53:06.260581
waiting_on: null
waiting_since: null
working_on: false
---