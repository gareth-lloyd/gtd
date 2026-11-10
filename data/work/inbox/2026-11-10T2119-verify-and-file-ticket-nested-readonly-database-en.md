---
area: null
completed_at: null
contexts: []
created: &id001 2026-11-10 21:19:47.771669
defer_until: null
due: null
energy: null
id: 2026-11-10T2119-verify-and-file-ticket-nested-readonly-database-en
order: null
output: ''
project: null
source_id: null
tags: []
time_minutes: null
title: 'Verify and file ticket: Nested @readonly_database entries re-run the SELECT
  1 health check per selector call'
updated: *id001
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