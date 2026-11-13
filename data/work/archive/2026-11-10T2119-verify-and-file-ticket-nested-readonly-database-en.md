---
area: null
completed_at: 2026-11-12 12:44:26.758093
contexts: []
created: 2026-11-10 21:19:47.771669
defer_until: null
due: null
energy: null
id: 2026-11-10T2119-verify-and-file-ticket-nested-readonly-database-en
order: null
output: |
  ## Agent run 2026-11-12T12:30

  **Status: verified, NOT filed.** Filing needs your explicit yes (Linear write). The draft's impact claim was wrong for wallets, so I rewrote the ticket.

  ### Verified
  - Mechanism is correct against installed Django 5.2.14 and master afd8338fce62. One line-ref nit: close_if_health_check_failed is base.py:578-589, not 575-589.
  - Fix diff (readonly_database.py, +8/-1) is still uncommitted on master and does what it says.
  - Tests pass with the fix: repro test + test_readonly_database.py + test_decorators.py + test_db_routers.py = 39 passed (borrowed ent-7726 venv via tmp/dashboard_latency_repros/run_tests.sh). I did not re-run hotels/tests/selectors/.
  - No duplicate in Linear. Closest: PMS-9441 (https://linear.app/canary-technologies/issue/PMS-9441, Backlog, different bug) and SRE-1535 (https://linear.app/canary-technologies/issue/SRE-1535, Done; its table lists "~18 SELECT 1, source not found yet (likely .exists())").

  ### Corrected: impact numbers
  I measured SELECT 1 per request through the real endpoints (throwaway probe in a temporary HEAD worktree, production connection lifecycle, before vs after the fix):

  | Request | before | after |
  | --- | --- | --- |
  | chat/threads, 20 threads, master | 45 | 1 |
  | chat/threads, 5 threads, master | 15 | 1 |
  | wallets, 25 wallets, master | 53 | 28 |
  | wallets, 5 wallets, master | 13 | 8 |
  | chat/threads, 20 threads, with the other audit fixes applied | 7 | 1 |
  | wallets, 25 wallets, with the other audit fixes applied | 53 | 28 |

  - Wallets reproduces production's 53 exactly, but the fix removes 25 of them, not "53 of 215". The wallets view has no @readonly_database, so each wallet's selector call is a top-level entry and keeps its SELECT 1.
  - Threads is fully nested (view is @readonly_database), so the fix removes all but one. "19 of 167" was a Datadog-derived figure I could not re-derive; the ticket now quotes the measured local numbers instead.
  - Entries with no query between them collapse into one SELECT 1, so "one per selector call" overstated it too.

  ### New risk the draft did not mention
  A long-lived outer readonly context (Celery task or command looping inside one @readonly_database function) now validates the reader connection once, at entry. Today each nested entry re-validates, so a dropped reader connection heals mid-loop; after the fix the next query fails instead. Request-scoped use is unaffected. It is in the ticket as a review point; I did not audit which long-running jobs nest this way.

  ### Things for you to decide before filing
  1. Team: PLAT's recent tickets are all auto-filed Groundcover alerts in Triage (PLAT-4813..4817). SRE owns SRE-1535 and the related query work. I kept PLAT as you specified; say if you want SRE.
  2. Labels: PLAT has no "backend" or "performance" label that I could find (first 100 labels checked), so the draft files with none.
  3. The fix is uncommitted and has no PR. The ticket embeds the diff; you may want a PR to link instead.

  ### Revised ticket (ready to file on your yes)
  Full text: /Users/garethlloyd/projects/canary/backend/canary/tmp/dashboard_latency_repros/tickets/10_PLAT_readonly_select1.v2.md
  Title: Nested @readonly_database entries re-run the connection health check: 45 extra SELECT 1 on a 20-thread chat page, 25 on a 25-wallet page
  Team: Platform (PLAT). Related: SRE-1535, PMS-9441. No labels.

  ### Left behind
  - Probe scripts (not committed, scratch only): /private/tmp/claude-501/-Users-garethlloyd-projects-canary/df53c6c9-e586-46a1-88d8-9869472b61ca/scratchpad/select1_probe_wallets.py and select1_probe_threads.py
  - Temporary worktree removed; main checkout untouched apart from the new v2 draft file under tmp/ (gitignored).
  - Ticket 06 (TIP wallets) says "SELECT 1 x53 is the platform ticket"; that line now overstates it too, since 28 remain after this fix.

  ## Agent run 2026-11-12T12:45

  Rewrote the ticket to your ticket-writing guide (Summary / Context / Evidence / Reproduction / Definition of done, diff and risk moved to Agent notes). Current version: /Users/garethlloyd/projects/canary/backend/canary/tmp/dashboard_latency_repros/tickets/10_PLAT_readonly_select1.v3.md (supersedes v2). Still NOT filed; waiting on your explicit yes and the team choice (PLAT vs SRE).

  ## Agent run 2026-11-12T13:00

  Linear search for related tickets (9 queries). No duplicate. Worth linking:
  - SRE-1535 (https://linear.app/canary-technologies/issue/SRE-1535) Done, James Morton: the "~18 SELECT 1, source not found" sighting.
  - SRE-1748 (https://linear.app/canary-technologies/issue/SRE-1748) In Progress, James Morton: chat inbox query volume on us-west-2 canary-ro, child of SRE-629. Same endpoint, same reader.
  - PMS-9441 (https://linear.app/canary-technologies/issue/PMS-9441) Backlog, unassigned: other open bug in the same decorator (lazy querysets escape routing).
  - ENT-8148 (https://linear.app/canary-technologies/issue/ENT-8148) Backlog: @no_readonly_database escapes inside a readonly view (get_config_by_hotel). Same tips selector chain as wallets.
  Context only: MSG-4657 (threads latency, Backlog), STAY-5888 and ENT-8151 (dashboard refetches /api/chat/threads, which multiplies this cost), SRE-1745 (chat messages).
  Checked and unrelated: SRE-1099 (pganalyze double counting on the reader), SRE-1737 (readiness probe SETs).
  The active owner of all adjacent work is James Morton on SRE, not PLAT.

  ## Agent run 2026-11-12T13:10

  FILED on SRE at your instruction: SRE-1790 (https://linear.app/canary-technologies/issue/SRE-1790/nested-readonly-database-entries-re-run-the-reader-connection-health). Status Triage, unassigned, no labels, no priority. Related: SRE-1535, PMS-9441. Body is the v3 draft. SRE-1748 and ENT-8148 are not linked (you did not confirm them). The fix and repro test are still uncommitted on master; no PR.
project: 2026-04-16T1351-ship
source_id: null
tags: []
time_minutes: null
title: 'Verify and file ticket: Nested @readonly_database entries re-run the SELECT
  1 health check per selector call'
updated: 2026-11-12 12:44:26.758089
waiting_on: null
waiting_since: null
working_on: false
---

**Team:** Platform (PLAT)

**Context:** Cross-cutting, one-file fix in canary/utilities/readonly_database.py. Removes 19 of 167 statements on chat/threads and 53 of 215 on wallets. SRE-1535 saw the SELECT 1s but never found the source.

Source: dashboard latency audit, agent run 2026-11-09 (GTD item 2026-11-04T1957-dashboard-latency-audit...). Draft, fix diff, repro test and SQL dumps: backend/canary/tmp/dashboard_latency_repros/ (gitignored). Fixes and new tests are UNCOMMITTED on master in the main canary checkout. Audit page: https://claude.ai/artifact/QzNanTU2XKUkdEscaJYJUD. Excluded as already covered: chat/threads (PR #63670, SRE-1535), chat/messages (SRE-1745), check-in search (AD-10218 1.1).

---

## Ticket draft (10_PLAT_readonly_select1.md)

Team: Platform (PLAT)
Title: Nested @readonly_database entries re-run the connection health check, one SELECT 1 per selector call (20-50 per dashboard request)
Labels: backend, performance
Related: PMS-9441 (readonly_database routing with lazy querysets), SRE-1535 ("~18 SELECT 1, source not found yet")
---
## Problem

`SELECT 1` appears 20-50 times per request on `GET /api/chat/threads` and `GET /api/hotels/{slug}/wallets` (Datadog spans; about 12k per 20 minutes on threads alone). Each one is a full round trip to the reader endpoint before a real query.

## Mechanism (Django 5.2.14, verified in the installed source)

- `backend/canary/canary/utilities/readonly_database.py:40-41` `ReadonlyDatabaseContext.__enter__` calls `connections[db_override].close_if_unusable_or_obsolete()` on every entry, nested or not.
- `django/db/backends/base/base.py:591-597` `close_if_unusable_or_obsolete()` sets `health_check_done = False` whenever the connection is open.
- `base.py:294-295` `_cursor()` calls `close_if_health_check_failed()` before every query; `base.py:575-589` runs `is_usable()` when `health_check_enabled and not health_check_done`.
- `django/db/backends/postgresql/base.py:485-491` `is_usable()` executes `SELECT 1` on a raw psycopg cursor, bypassing Django's query logging (so `CaptureQueriesContext` and `assertNumQueries` never see it).
- `canary/settings/base.py:457-458` `CONN_HEALTH_CHECKS: True`, `CONN_MAX_AGE: 3600`.
- Per-row nested entries in the audited endpoints: `guest/selectors/guest.py:45`, `tips/selectors/tips.py:59` and `:460` (two entries per call), `hotels/selectors/hotel.py:45` and `:118`.

## Reproduction

Test: `backend/canary/canary/tests/utilities/test_readonly_database_health_check_count.py`. An outer `@readonly_database` function loops N inner `@readonly_database` selector calls, each one trivial Hotel query, with the connection at production lifecycle values (`health_check_enabled=True`, `close_at=None`) and `DEFAULT_READONLY_DATABASE` aliased to `default` (tests have no replica). Health checks are counted by wrapping `connection.is_usable`.

| N inner calls | ORM queries | SELECT 1 before | after |
| --- | --- | --- | --- |
| 5 | 5 | 5 | 1 |
| 20 | 20 | 20 | 1 |

## Fix (diff attached, one file)

`__enter__` skips `close_if_unusable_or_obsolete()` when `prev_value == db_override`, i.e. the thread is already inside a readonly context. The outermost entry still validates the connection as before. Routing is unchanged: the thread-local flag is still set on every entry and `ReadonlyDatabaseRouter.db_for_read` (`canary/db_routers.py:289-292`) reads only that flag. `no_readonly_database` never took this branch.

Existing tests pass: `canary/tests/utilities/test_readonly_database.py`, `test_decorators.py`, `canary/tests/test_db_routers.py`, `hotels/tests/selectors/`.

## Expected impact

Removes every nested `SELECT 1`: 19 of 167 statements on threads, 53 of 215 on wallets, and the same pattern on every endpoint that calls a `@readonly_database` selector per row. Sibling top-level entries from a non-readonly view still cost one each; whether to drop the explicit check in favour of Django's per-request `close_old_connections` is a follow-up decision for the pod.

+++ Agent notes

- The new test needs `transactional_db`: inside the `db` fixture's atomic block the autocommit mismatch makes `close_if_unusable_or_obsolete()` close the connection instead.
- Not reproduced through the audited endpoints; the test isolates the mechanism with a synthetic outer/inner pair.
- Run: `direnv exec . pytest canary/tests/utilities/test_readonly_database_health_check_count.py --nomigrations -q`.

+++