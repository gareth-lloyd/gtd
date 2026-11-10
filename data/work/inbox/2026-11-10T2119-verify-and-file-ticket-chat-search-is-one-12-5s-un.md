---
area: null
completed_at: null
contexts: []
created: &id001 2026-11-10 21:19:47.421980
defer_until: null
due: null
energy: null
id: 2026-11-10T2119-verify-and-file-ticket-chat-search-is-one-12-5s-un
order: null
output: ''
project: null
source_id: null
tags: []
time_minutes: null
title: 'Verify and file ticket: Chat search is one 12.5s UNION statement; decide OpenSearch
  cutover date vs interim per-table rewrite'
updated: *id001
waiting_on: null
waiting_since: null
working_on: false
---

**Team:** Messaging (MSG)

**Context:** Largest DB load in the audit and unowned since MSG-6764 was cancelled on 2026-11-06 for OpenSearch. ~11k calls/day at 12s avg. Decision ticket plus a designed (not applied) interim rewrite. Assign to whoever owns the OpenSearch plan.

Source: dashboard latency audit, agent run 2026-11-09 (GTD item 2026-11-04T1957-dashboard-latency-audit...). Draft, fix diff, repro test and SQL dumps: backend/canary/tmp/dashboard_latency_repros/ (gitignored). Fixes and new tests are UNCOMMITTED on master in the main canary checkout. Audit page: https://claude.ai/artifact/QzNanTU2XKUkdEscaJYJUD. Excluded as already covered: chat/threads (PR #63670, SRE-1535), chat/messages (SRE-1745), check-in search (AD-10218 1.1).

---

## Ticket draft (02_MSG_chat_search.md)

Team: Messaging (MSG)
Title: Chat search is one 12.5s UNION statement that filters after a seven-table join; decide between the OpenSearch cutover date and an interim per-table rewrite
Labels: backend, performance
Related: MSG-6764 (Canceled 2026-11-06 "because we are planning to move to open search"; this ticket asks for the date or an interim fix), MSG-2634, MSG-5318, AI-775
---
## Problem

`GET /api/chat/search` (dashboard thread search): p50 1.2-3.3s, p95 39-75s, about 190 requests per 3h window (Datadog spans, 2026-10-21 to 2026-11-04). The request runs 15 statements; one of them, the UNION built by `ChatSearchService._make_search_queryset`, averages 12.5s. pganalyze (MSG-6764) has the same statement at 12s average, 400s peak, about 11k calls a day, reading 290 MB to 1.9 GB per run.

MSG-6764 was cancelled because chat search is moving to OpenSearch. Until that ships, every search on a large hotel holds a reader connection for 12s or more. This ticket is for a decision: either name the OpenSearch cutover date for dashboard search, or ship the interim rewrite below.

## Reproduction (local, plan shape only)

Test: `backend/canary/chat/tests/views/test_chat_search_query_count.py` seeds N=500 reservations, guests, phones and confirmation numbers, half with threads, runs the real endpoint and captures the UNION statement plus `EXPLAIN (ANALYZE, BUFFERS)` (attached: explain_before.txt, union_statement_n500.sql). Local runtime is milliseconds; what the plan shows is the shape:

- The eight-way OR search predicate appears once per UNION branch as a `Filter` on the output of the LEFT JOIN chain, never as an `Index Cond`. Postgres materializes every (thread x guest x reservation x confirmation number x check-in) row at the hotel before it tests the search text.
- Five leading-wildcard `LIKE '%x%'` predicates on phone columns, unindexable by construction.
- `Unique`/`HashAggregate` dedupe over all surviving rows (UNION, not UNION ALL), then a top-N sort, then `LIMIT 11`.

## Causes (`chat/services/search.py`, verified)

- `:147-205` docstring already names the problem and proposes the per-table split.
- `:222-237` the OR across guest search_vector, email, five phone `__contains` (`:227-232`), confirmation number and check-in search_vector; `:328-330` repeats three phone LIKEs on the guest branch.
- `:312-360` guest branch starts from every guest with a reservation at the hotel.
- `:277-293` `DISTINCT ON (uuid)` with a five-key ORDER BY when `deduplicate_by_thread=True` (the dashboard passes it).
- `:363-371` `.union()`, `:378-390` final ORDER BY over the whole UNION before the LIMIT.

## Interim fix design (not applied)

Every predicate except phone substring already has an index that serves it when it drives its own query: GIN on `guest_guest.search_vector` and `check_in_checkin.search_vector`, `UPPER(raw_email)` / `UPPER(confirmed_email)`, `UPPER(value)` on confirmation numbers, unique `(hotel_id, phone_number)`, `(hotel_id, arrival_date)`, unique `threadguest(guest_id, thread_id)`.

Replace the UNION with one hotel-scoped, id-only query per predicate group (guest name GIN, email prefix, confirmation number exact, check-in GIN, phone normalized to E.164 candidates via the unique phone index), map guest ids to thread ids through `ThreadGuest`, apply the arrival-date filter on `(hotel_id, arrival_date)`, rank in Python with today's keys, slice the page, then hand it to the existing `_get_objects_from_results`. Phone substring is the only predicate with no index; narrow it to exact or normalized match, or add a trigram index in a separate migration PR. Full design with the per-step queries: attached REPORT.md.

`UNION` to `UNION ALL` alone is not safe (within-branch duplicates when `deduplicate_by_thread=False`) and the plan shows the dedupe is cheap next to the join.

+++ Agent notes

- The thread branch has seven LEFT JOINs (guest_phone twice), not six as the audit said.
- `Reservation.primary_guest` is a OneToOneField, so "every reservation at the hotel" equals "every guest with a reservation".
- Check `\d guest_guest` and `\d guest_phone` in production before relying on the index list; the `UPPER(email)` indexes need a pattern-ops or C-collation opclass to serve a prefix LIKE.
- Run: `QUERY_DUMP_DIR=<dir> direnv exec . pytest chat/tests/views/test_chat_search_query_count.py --nomigrations -q -s`.

+++