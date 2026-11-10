---
area: null
completed_at: 2026-11-10 12:46:25.950709
contexts:
- deep
created: 2026-11-04 19:57:26.337946
defer_until: null
due: null
energy: high
id: 2026-11-04T1957-dashboard-latency-audit-reproduce-each-finding-loc
order: null
output: |
  ## Agent run 2026-11-09T16:09:00+02:00

  Done: all nine findings reproduced locally with a query-count test through the real view (CaptureQueriesContext, seeded via testing.py stubs), a minimal fix applied for eight of them with before/after numbers, and ten ticket drafts written (one per finding; the contracts soft-delete bug split out). NOT done without your yes: filing the tickets to Linear, committing anything, posting to Slack. No external writes were made.

  ### Results (N=20 rows per page unless noted; all 20 new tests pass on the combined tree; ruff + pyrefly clean on all 34 changed files)
  | # | Endpoint | Linear team (CODEOWNERS) | Before -> after queries | Per row | Fix applied? |
  |---|---|---|---|---|---|
  | 1 | GET /api/chat/threads | MSG (pod-messaging) | 240 -> 42 | 10 -> 0 | yes, 3 files |
  | 2 | GET /api/chat/search | MSG | one UNION statement; plan captured (filter after 7-way join, 5 leading-wildcard LIKEs, UNION dedupe, sort before LIMIT) | n/a | no (rewrite design in ticket; MSG-6764 was cancelled for OpenSearch) |
  | 3 | GET /api/contracts | SDM (+ jordan-canary) | 403 -> 45; Jinja compiles 80 -> 0 warm | 19 -> 1 | yes, 5 files |
  | 3b | contracts Count("signers") soft-delete bug | SDM | test fails on master ([] == [url]), passes with the one-line filter | | yes, 1 line |
  | 4 | GET /api/ticket_gateway/recommended_tickets | MSG | 202 -> 38 (rows returned 42 -> 40: approved rows dropped) | 4.5 -> 0.5 | yes, 4 files + stubs |
  | 5 | GET /api/hotels/{slug}/wallets | TIP (pod-tipping) | 152 -> 53 | 7 -> 2 | yes, 6 files (shared with 6) |
  | 6 | GET /api/hotels/{slug}/departments | TIP | 177 -> 55 | 8 -> 2 | yes |
  | 7 | GET /api/authorizations | SDM | 381 -> 143 | 19 -> 1 card / 12 ACH | yes, 4 files; COUNT over UNION left (UI contract), options in ticket |
  | 8 | GET /api/hotels/{slug}/check_ins/search | AD (pod-arrivals-departures) | 288 -> 28 | 13 -> 0 | yes, 1 file; 3.5s COUNT left (UI contract) |
  | 9 | GET /api/chat/messages | MSG | 105 -> 21 (N=26) | 3.35 -> 0 | yes, 2 files |
  | 10 | nested @readonly_database SELECT 1 | PLAT (pod-platform) | 20 health checks -> 1 for 20 nested calls | 1 -> 0 | yes, 1 file (Django 5.2.14 mechanism pinned to source lines) |

  The audit's reading of the code held in every finding; line numbers were off by a few lines in places. New facts the audit missed: threads also builds Features(hotel) per thread (3 SQL/thread locally, probably the ~50 redis calls on prod); recommended_tickets' Knowcross path loads the Hotel per row; check_ins/search also pays 3 Incode-document EXISTS per row and a booking lookup; authorizations' payment method load is 10 statements (nine vendor probes), so prod's x4 means most rows lack a payment_method_uuid; GenericPrefetch with `.objects` would silently drop soft-deleted vendor tickets (fix uses `.every`).

  ### Overlaps found in Linear (link or merge before filing)
  - SRE-1535 (James Morton, Done 2026-10-16) is the same chat/threads analysis; its fix 2 (reservation N+1) is James's OPEN DRAFT PR #63670 https://github.com/canary-technologies-corp/canary/pull/63670 "Reuse prefetched reservations in the chat threads list": same cause as our fix 1. Coordinate rather than open a second PR.
  - SRE-1745 Pinning L (James, 2026-11-09) is chat/messages from the RDS-proxy pinning angle and already proposes dropping the hotel join + a query-count test: https://linear.app/canary-technologies/issue/SRE-1745 . Also SRE-1748 (Pinning D, threads), SRE-1752 (Pinning Q, the threads reservation lookup), SRE-1739 (Pinning C, check-in list), SRE-1744 (Pinning J, contract/auth logs).
  - MSG-6764 chat search (Dmitry) was cancelled 2026-11-06 by Matias: "Cancelled because we are planning to move to open search" https://linear.app/canary-technologies/issue/MSG-6764 . Draft 02 is framed as a decision: cutover date or interim rewrite.
  - AD-10218 item 1.1 (Pat Canny) already plans the exact check_ins/search fix https://linear.app/canary-technologies/issue/AD-10218 ; draft 07 should be a child/comment there, carrying the numbers and the diff.
  - ENT-8151 (yours) nav badges firing /api/chat/threads; STAY-5888 (Johannes, Triage) looping threads requests since 11-06; ENT-8148 (yours) tips config read from the primary; PMS-9441 readonly_database lazy querysets.
  - PR #63267 / ENT-8145 merged 2026-11-04 21:34Z.

  ### Where everything is (durable copy, gitignored): /Users/garethlloyd/projects/canary/backend/canary/tmp/dashboard_latency_repros/
  - tickets/00_README.md + 01..10 drafts (Team, Title, Labels, Related header, then the Linear description with +++ Agent notes +++).
  - <NN_slug>/REPORT.md, fix.diff, before_sql.txt (normalized SQL grouped by count), after_sql.txt; 02_chat_search/explain_before.txt + union_statement_n500.sql.
  - all_fixes.patch (1116 lines, 25 files) and all_changed_and_new_files.txt.
  - Working tree: /Users/garethlloyd/projects/canary is on master with 25 modified files + 10 new test files, UNCOMMITTED. The drafts point at scratchpad paths; before filing, the diffs need a durable home (suggest a branch `glloyd/dashboard-latency-repros` with one commit per finding, or attach each fix.diff to its ticket).

  ### Not done / caveats
  - "Reproduce in Groundcover" was not redone: the production p50/p95/req/SQL-per-request numbers in the tickets are the 2026-11-04 audit's Datadog-span figures. No production shell was used (would need your explicit OK; the local tests replace the /debug_in_shell validation).
  - Latency is not reproduced locally for the two single-statement findings (chat search 12.5s UNION, check-in COUNT 3.5s); plan shape and statement text are.
  - Fixes are minimal and uncommitted; each pod should own its PR. Remaining per-row costs are listed per ticket (wallets 2/row payout vendor, authorizations 1/row card type, recommended_tickets Knowcross category, contracts operation_logs).
  - Environment: the main backend/canary/.venv is stale (missing langchain_aws) and `uv sync` fails because pypi.cnry.cloud now redirects to a Cloudflare Access login (WARP connected is not enough); only you can re-authenticate. Tests ran with the synced venv from .claude/worktrees/ent-7726 and a per-run CANARY_TEST_DB_SUFFIX. Saved to memory. 20 wallet/mobile-search tests fail in that venv on PyJWT InsecureKeyLengthWarning (18-byte test key), unrelated.
  - The audit page https://claude.ai/artifact/QzNanTU2XKUkdEscaJYJUD is still private; share it before the tickets link to it.

  ### Needs your decision
  1. File the 10 tickets as drafted (MSG x4, SDM x3, TIP x1, AD x1, PLAT x1)? Or merge 01 into SRE-1535/#63670, 09 into SRE-1745, 07 into AD-10218 as comments instead of new tickets.
  2. Commit the repro tests + fixes to a branch so tickets can link commits (nothing committed yet).
  3. Post the findings table to the #engineering thread (draft from the 2026-11-04 run still unposted).
project: null
source_id: null
tags: []
time_minutes: 240
title: 'Dashboard latency audit: reproduce each finding in groundcover and validate
  fix on /debug_in_shell  and file tickets to the owning pods'
updated: 2026-11-10 12:46:25.950701
waiting_on: null
waiting_since: null
working_on: false
---

Follow-up to the 2026-11-04 dashboard latency audit (one item, nine findings).

## Action
1. For each finding, reproduce locally with a query-count assertion (django_assert_num_queries or CaptureQueriesContext) against seeded data, so the ticket carries a before/after number rather than a reading of the code.
2. File one ticket per finding to the owning pod (map paths via CODEOWNERS), with the file:line, the repeated SQL, the fix, and the impact estimate. Link the audit page.

## Findings to ticket (owner area -> endpoints)
- Messaging: GET /api/chat/threads (fresh Reservation query per thread discards prefetch), GET /api/chat/search (single 12.5s UNION/LIKE query), GET /api/chat/messages (hotel+config join on every row, missing select_related)
- Contracts / auths: GET /api/contracts (combiner refetch, 377 q/req, Jinja compiles; plus Count("signers") soft-delete bug at api_views.py:691), GET /api/authorizations (COUNT over UNION for num_pages, per-row payment method fetch)
- Tipping: GET /api/hotels/{slug}/wallets and /departments (per-wallet payout vendor chain, terms latest())
- Arrivals: GET /api/hotels/{slug}/check_ins/search (3.5s count, missing relations block)
- Ticketing: GET /api/ticket_gateway/recommended_tickets (unbounded queryset, GFK N+1, 890 q/req)
- Platform: SELECT 1 health check reset on nested @readonly_database (readonly_database.py:40-41)

## Sources
- Audit page (private until shared): https://claude.ai/artifact/QzNanTU2XKUkdEscaJYJUD
- Full evidence in the source GTD item output: data/work/inbox/2026-11-04T1921-claude-made-that-discovery-so-easy-just-then-worth.md
- hotels/{slug} fix already in flight: https://github.com/canary-technologies-corp/canary/pull/63267
- Discovery thread: https://canarytechnologies.slack.com/archives/C019TQLQDJP/p1793811389605919?thread_ts=1793808707.680909&cid=C019TQLQDJP