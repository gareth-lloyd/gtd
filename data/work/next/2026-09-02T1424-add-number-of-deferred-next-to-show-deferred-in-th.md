---
area: null
completed_at: null
contexts: []
created: 2026-09-02 14:24:10.447019
defer_until: null
due: null
energy: low
id: 2026-09-02T1424-add-number-of-deferred-next-to-show-deferred-in-th
order: null
output: |
  ## Agent run 2026-09-16T09:42:12

  Done: the inbox "Show deferred" toggle now reads e.g. "Show deferred (2)",
  the count being the number of inbox items currently hidden by defer_until.
  When nothing is deferred the count is omitted (same convention as the
  side-nav inbox badge).

  Implementation (frontend/src/ItemList.tsx, BucketView):
  - On the inbox route, a second react-query fetch loads the inbox with
    include_deferred=true. It shares the cache key ["items", env, "inbox",
    true] with the toggled-on list fetch, so flipping the toggle on is
    instant and nothing is fetched twice.
  - Count = items in that list where isHiddenByDefer() is true (mirrors the
    backend rule: hidden only if defer_until is in the future and the item
    is not overdue).
  - The default (non-deferred) fetch and its cache key, which App.tsx shares
    for the nav badge, are untouched.

  Tests (frontend/src/App.test.tsx, red/green): two new cases, count shown
  with deferred items present and count omitted when none. Frontend 158
  passed, backend 602 passed, scripts/lint.sh all clear.

  Commit 13f8debf on main. Frontend rebuilt, `make restart-service` run,
  localhost:8765 confirmed serving the new bundle (index-DxGLHeuJ.js).

  Known limitation: the count reflects the last fetch. If you defer an item
  while processing the inbox, the row greys out immediately but the toggle
  count only updates on the next visit to the inbox (the inbox caches are
  deliberately not refetched mid-processing so greyed rows keep their slot).
project: 2026-04-27-gtd
source_id: null
tags: []
time_minutes: 5
title: add number of deferred next to "show deferred" in the invox
updated: 2026-09-16 09:42:12.281776
waiting_on: null
waiting_since: null
working_on: false
---