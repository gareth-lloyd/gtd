---
area: null
completed_at: null
contexts: []
created: 2026-10-21 09:48:50.341701
defer_until: null
due: null
energy: low
id: 2026-10-21T0948-within-a-grab-bag-sort-completed-deferred-or-refer
order: null
output: |
  ## Agent run 2026-10-21T09:51

  Implemented and committed on main as 966be0e9 (frontend only, no backend change).

  Behaviour in the grab-bag detail view (`/<env>/grab-bags/<id>`):
  - "Set aside" items sort to the bottom: completed (`completed_at` set), status archive/trash/reference, or deferred into the future. Overdue items are never set aside (mirrors `isHiddenByDefer`).
  - Grab order is preserved within the live group and within the set-aside group.
  - Set-aside cards get `.item.parked`: opacity 0.5, back to full on hover / selected / editing (same treatment as inbox `.processed`). Still fully interactive.
  - Header chip reads "N items · M set aside" when any are parked.

  Code:
  - frontend/src/GrabBags.tsx: `isSetAside()`, `sortBagItems()`, wired into `GrabBagDetailView`.
  - frontend/src/ItemList.tsx: optional `isParked` predicate prop; ItemCard.tsx: optional `parked` flag → `parked` class.
  - frontend/src/styles.css: `.item.parked` rules.
  - frontend/src/GrabBags.test.tsx: 3 new tests (predicate edge cases, ordering, rendered order + class + chip). Red first, then green.
  - CLAUDE.md grab-bags bullet updated.

  Verification: vitest 196/196, pytest 695/695, eslint/prettier/tsc clean, `npm run build` done. Pre-commit hooks passed.

  Notes / open choices for you:
  - Sorting is client-side; the API still returns items in grab order (service docstring unchanged). Fine unless the CLI needs the same ordering.
  - Trash and archive are treated as set aside too, though the backend prunes a bag once *every* item is archived/trashed, so you'll only see them mixed with live ones.
  - Someday items are NOT dimmed (not in the ask). Easy to add to `isSetAside` if wanted.
  - Service needs `make restart-service` to pick up the new bundle (launchd gunicorn doesn't reload).
project: 2026-04-27-gtd
source_id: null
tags: []
time_minutes: 5
title: Within a grab bag, sort completed, deferred or reference items at the bottom,
  and gray them out?
updated: 2026-10-21 09:51:18.907170
waiting_on: null
waiting_since: null
working_on: false
---