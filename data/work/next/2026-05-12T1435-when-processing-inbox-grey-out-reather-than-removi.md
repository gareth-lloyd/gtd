---
area: null
contexts: []
created: 2026-05-12 14:35:01.968666
defer_until: null
due: null
energy: low
id: 2026-05-12T1435-when-processing-inbox-grey-out-reather-than-removi
order: -9
output: |
  ## Agent run 2026-05-25T11:42

  Implemented Linear-style grey-out behaviour for inbox processing. When
  the user moves / completes / deletes an inbox item, the row now stays
  visible greyed out instead of vanishing; on the next mount of /inbox
  (navigation or reload) the list refetches and processed items drop off.

  ### Files

  - `frontend/src/ProcessedItemsContext.tsx` (new) — React context
    holding `processedIds` for the currently-mounted inbox view and a
    `markProcessed(id)` action.
  - `frontend/src/ItemEdit.tsx` — added
    `invalidateItemQueriesPreservingInbox()`, a sibling of
    `invalidateItemQueries()` that invalidates everything *except* the
    active inbox list query so the moved row remains in cache.
  - `frontend/src/WorkflowActions.tsx` — reads `useProcessedItems()`;
    when the context is present AND `item.status === "inbox"`, the
    mutation success path calls `markProcessed(id)` and uses the
    inbox-preserving invalidation. Otherwise behaviour is unchanged.
  - `frontend/src/ItemList.tsx` — `BucketView` wraps the inbox body in
    `<ProcessedItemsProvider>`, and on unmount fires a `refetchType:
    "none"` invalidation on `["items", env, "inbox"]` so the next visit
    refetches a clean list without waiting for the global 5s staleTime.
  - `frontend/src/ItemCard.tsx` — adds `processed` class to the card
    when `isProcessed(item.id)` is true.
  - `frontend/src/styles.css` — `.item.processed { opacity: 0.4 }` with
    a short transition; `:hover` lifts to 0.7 so the row remains
    legible/clickable for undo or detail-pane inspection.

  ### Test

  Added a unit test in `WorkflowActions.test.tsx` that renders the
  component inside `<ProcessedItemsProvider>` with `item.status =
  "inbox"`, clicks "→ next", and asserts (a) the processed-items
  context now returns true for the item id, and (b) the inbox list
  cache is preserved (still contains the item) — i.e. the list will
  not refetch the moved row away.

  All 133 frontend unit tests, `npm run typecheck`, `npm run lint`,
  and `npm run build` pass.

  ### Things NOT done — left for you to confirm

  - I did not start the dev server for a manual visual check of the
    opacity, since the agent guardrails point me at recording findings
    and stopping. Worth eyeballing once: grey-out on click, hover lift,
    and the row reappearing crisp on navigation back to /inbox.
  - Behaviour is intentionally scoped to inbox only. If you want the
    same Linear-style staleness in /next or /waiting, the same pattern
    (`ProcessedItemsProvider` + an "items, env, <bucket>"-preserving
    invalidator) drops in there easily — but you said inbox, so I left
    the other buckets alone.
  - Auto-animate continues to wrap the `<ul>`. Since processed items
    don't enter/leave during processing (only their class changes),
    there's no animation conflict; the smooth grey-out is the CSS
    transition on `.item.processed`.
project: 2026-04-27-gtd
source_id: null
tags: []
time_minutes: 5
title: When processing inbox, grey out reather than removing entries for deferred,
  next etc
updated: 2026-05-25 11:42:30.000000
waiting_on: null
waiting_since: null
working_on: false
---

inspired by linear behavior
on next reload or navigation, can stop displaying them