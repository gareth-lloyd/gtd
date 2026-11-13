---
area: null
completed_at: 2026-11-12 12:44:22.010096
contexts: []
created: 2026-11-10 21:19:47.421980
defer_until: null
due: null
energy: null
id: 2026-11-10T2119-verify-and-file-ticket-chat-search-is-one-12-5s-un
order: null
output: |-
  ## Agent run 2026-11-12T12:20Z

  STATUS: verified, NOT filed. Filing a Linear issue is an outbound write and needs your explicit go-ahead.

  Revised draft (ready to file): /Users/garethlloyd/projects/canary/backend/canary/tmp/dashboard_latency_repros/tickets/02_MSG_chat_search.md

  ### Verified
  - Code claims hold against master (chat/services/search.py, last touched 2026-10-27, no local edits). Seven LEFT JOINs on the thread branch and eight LIKE '%x%' confirmed in union_statement_n500.sql.
  - MSG-6764 (https://linear.app/canary-technologies/issue/MSG-6764/investigate-slow-chat-dashboard-search-query-12s-avg-up-to-400s) is Canceled 2026-11-06 by Matias Marco del Pont: "Cancelled because we are planning to move to open search". pganalyze figures in the draft match it.
  - No duplicate: no Messaging issue created since 2026-11-05 covers chat search. MSG-6990 is the inbox list, a different endpoint.
  - Still slow now, and worse than the audit said. Groundcover traces, us-west-2 django, GET /api/chat/search, 3h windows: 2026-11-10 17-20Z 571 req, p50 2.8s, p95 161s, max 301s; 2026-11-11 17-20Z 872 req, p50 9.4s, p95 105s, max 346s; 2026-11-12 09-12Z 106 req, p50 1.0s, p95 87s. EU and AP are under 0.7s p95, so this is US-only.

  ### Corrected in the draft
  - "Eight-way OR" was wrong: ten terms on the thread branch, eight on the guest branch.
  - "Five-key ORDER BY" was wrong: four keys on the dashboard path, six with link_reservation_thread.
  - OR block is :220-241 (was :222-237); final ORDER BY is :377-390.
  - Labels backend/performance do not exist on the Messaging team; dropped.
  - MSG-5318 dropped from Related (a Duplicate customer complaint, adds nothing). AI-775 swapped for AI-756.
  - Latency table now uses the Groundcover samples. The audit's Datadog numbers (p95 39-75s, ~190 req/3h) were not re-checked and moved to agent notes.
  - Email index claim softened: the UPPER(email) indexes were added for __iexact; whether they serve a prefix LIKE needs a prod check.

  ### New finding that sharpens the ask
  "Moving to OpenSearch" has no ticket for this endpoint's read path.
  - Project "Message Content and Metadata Search" (https://linear.app/canary-technologies/project/message-content-and-metadata-search-56dbd8382a46), Applied AI, lead Garrett Idler, status Clean-up. Only open issue is AI-756 reconciliation (https://linear.app/canary-technologies/issue/AI-756/opensearch-chat-and-metadata-search-scheduled-message-and-thread), unassigned.
  - A chat-threads index exists (chat/opensearch/threads/: guest name, email, phone, confirmation numbers) but nothing in chat/services/search.py reads it.
  - The index is thread-keyed, so the guest-without-thread half of the UNION is not covered. AI-756 names a 90-day default retention; search takes any arrival-date range.

  ### Not verified
  - Datadog figures from the original audit.
  - Production index definitions (\d guest_guest, \d guest_phone) and a production EXPLAIN. No prod DB access was used.
  - The repro test was not re-run this session.
  - The interim design is still paper only.

  ### To file (needs your yes)
  Linear create in team Messaging with the draft's title and body, relatedTo MSG-6764, MSG-2634, AI-756, no labels. Proposed assignee Matias Marco del Pont (he made the OpenSearch call); alternative is unassigned into MSG triage. Attachments (REPORT.md, explain_before.txt, union_statement_n500.sql from tmp/dashboard_latency_repros/02_chat_search/) would need uploading too; say if you want them attached or pasted into agent notes.

  ## Agent run 2026-11-12T12:40Z

  Rewrote the draft to the pasted ticket format (Summary, Context, Evidence, Reproduction, Definition of done, collapsed Agent notes). Same path. Still NOT filed.
  - The interim rewrite design moved out of the body into agent notes plus REPORT.md, since the approach is not decided.
  - Definition of done proposes a target of p95 under 3s in us-west-2. That number is my proposal, not an agreed SLO.

  ## Agent run 2026-11-12T13:00Z: search for overlapping tickets

  No open ticket covers this with evidence or an owner. Draft updated; still NOT filed.
  - MSG-3976 "Improve search speed and broaden search scope" (https://linear.app/canary-technologies/issue/MSG-3976/improve-search-speed-and-broaden-search-scope): the only open overlap. Backlog, unassigned, no priority, created 2026-03-17 by Jake Wilhelm from a Slack thread (https://canarytechnologies.slack.com/archives/C08R2NVL1PB/p1773764221201269). No measurements, and it mixes speed with message-content search. Agustin Brana commented 2026-07-23 that another property raised it. Options: file new and relate (my recommendation), or rewrite MSG-3976 in place.
  - Customer reports of the same slowness, both closed as duplicates: MSG-5318 (dup of MSG-3976) and MSG-6853 (https://linear.app/canary-technologies/issue/MSG-6853/ui-slow-to-respond, dup of the cancelled MSG-6764, so it now points at nothing live).
  - Closed or cancelled, same area: MSG-6764 (cancelled), MSG-4381 (cancelled, search scope), MSG-4040 (cancelled, match metrics), MSG-6357 (cancelled, mobile dedupe), MSG-2634 (done, dedupe).
  - Adjacent, different endpoint: MSG-6990, MSG-4657, MSG-2769, SRE-1535, SRE-1748, ENT-8151, STAY-5888 (all /api/chat/threads); SRE-1747 (OpenSearch indexer query size).
  - Design doc (https://app.notion.com/p/3a3814686151801b8424f14d44d55fed, WIP, last edited 2026-10-06) corrects one earlier claim of mine. The guest-without-thread half is planned: it comes from the PMS Gateway reservation-search index, rolling out per hotel behind a flag. The doc says chat_threads "replaces today's thread search" and gives "query construction and search UX" to the Chat team. No ticket exists for that item; AI project issues are all ingestion-side.

  ## Agent run 2026-11-12T12:40Z: FILED

  Filed on your instruction as MSG-7027 (https://linear.app/canary-technologies/issue/MSG-7027/dashboard-chat-search-filters-after-a-seven-table-join-p95-87-161s-in), team Messaging, status Triage.
  - Related: MSG-6764, MSG-3976, MSG-2634, AI-756. No labels, no priority.
  - Linear auto-assigned it to Rick Schieck (triage). I set no assignee.
  - Attached: REPORT.md and test_chat_search_query_count.py.
  - REPORT.md is the 2026-11-09 audit file unedited. It still says "six tables", "eight-way OR", "five-key ORDER BY" and quotes the Datadog figures. The ticket body has the corrected versions.
project: 2026-04-16T1351-ship
source_id: null
tags: []
time_minutes: null
title: 'Verify and file ticket: Chat search is one 12.5s UNION statement; decide OpenSearch
  cutover date vs interim per-table rewrite'
updated: 2026-11-12 12:44:22.010079
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