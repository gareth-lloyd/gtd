---
area: null
completed_at: 2026-11-12 12:44:28.545412
contexts: []
created: 2026-11-10 21:19:47.888122
defer_until: null
due: null
energy: null
id: 2026-11-10T2119-verify-and-file-ticket-wallets-and-departments-lis
order: null
output: |-
  ## FILED 2026-11-12T12:39:32: TIP-5659 (https://linear.app/canary-technologies/issue/TIP-5659/wallets-and-departments-lists-run-7-8-queries-per-staff-member)

  Filed on your "file ticket" in Tipping, status Triage, no labels, no assignee, no priority, related to ENT-8148. Body is the brief-format text below. The "NOT FILED" line further down is from earlier in the same run. The fix and tests are still uncommitted on master.

  ## Agent run 2026-11-12T12:33:24

  NOT FILED. Verification passed; you chose "Don't file" when asked, so nothing was sent to Linear. Corrected ticket text is below, ready to file by hand in Tipping (TIP).

  ### Verified on 2026-11-12
  - After (fix in the main checkout): both repro tests pass, 4 passed. Counts 23/53 (wallets N=5/20), 25/55 (departments).
  - Before (clean checkout of HEAD afd8338fce62 in a scratch worktree, since removed, with the two test files copied in): 4 failed with 47/152 (wallets) and 57/177 (departments). Matches the draft table exactly.
  - Existing tests: the 16 test paths listed in backend/canary/tmp/dashboard_latency_repros/05_wallets_departments/REPORT.md give 398 passed, with -W ignore::jwt.warnings.InsecureKeyLengthWarning (borrowed venv). The draft said 402; the count has drifted.
  - Causes: read the cited code; all six match. The working-tree diff for the six files equals fix.diff (19 insertions, 14 deletions).
  - Duplicates: none found in Linear (searched TIP for wallets/departments/payout vendor/N+1/latency, and all TIP issues created in the last 14 days).
  - ENT-8148 (https://linear.app/canary-technologies/issue/ENT-8148/serialize-hotel-reads-tips-configuration-and-the-hotel-theme-from-the) is Backlog, unassigned, and is about serialize_hotel; related, not a duplicate. AD-10218 (https://linear.app/canary-technologies/issue/AD-10218/remove-the-remaining-n1-queries-in-ad-owned-backend-code-plan) is Backlog.

  ### Corrections to the draft
  1. Labels: TIP has no "backend" or "performance" label. File with no labels or pick one by hand.
  2. Tests line: replace "382 of 402 pass; the 20 failures are PyJWT..." with "398 existing wallet, department and tips tests pass".
  3. New review point, not in the draft: get_tip_payout_config is also called by tips/services/tip_payout.py:196 and :295 and wallets/selectors/wallet.py:164. Those reads also move from the writer to the replica. The writer routing dates from PR #24158 (https://github.com/canary-technologies-corp/canary/pull/24158, "no_readonly_db for onboarding used methods", 2025-04-17), which was aimed at onboarding, so it is probably safe, but Tipping should confirm for the payout path. I did not test replica-lag behaviour.

  ### Ticket text to file

  Team: Tipping (TIP)
  Title: Wallets and departments lists run 7-8 queries per staff member (payout vendor via a hotel slug refetch on the writer, terms accept, short link)
  Related: ENT-8148; mention AD-10218 section 6 (different endpoint)

  Body: use backend/canary/tmp/dashboard_latency_repros/tickets/06_TIP_wallets_departments.md (same as this item's body) with these edits:
  - In "Fix", replace the last bullet with: "Existing tests: 398 wallet, department and tips tests pass with the fix."
  - In "Fix", add: "Review point: `get_tip_payout_config` is also called by `tips/services/tip_payout.py:196`, `:295` and `wallets/selectors/wallet.py:164`. Those reads move from the writer to the replica too (on the writer since #24158). Confirm that is acceptable on the payout path."
  - In "Reproduction", add: "Re-verified 2026-11-12 against master afd8338fce62."
  - Attach or paste backend/canary/tmp/dashboard_latency_repros/05_wallets_departments/fix.diff into the Agent notes section.

  ### State left behind
  - Fix and the two new tests are still UNCOMMITTED on master in the main checkout, untouched by this run.
  - The draft file 06_TIP_wallets_departments.md was not edited.
  - Audit page: https://claude.ai/artifact/QzNanTU2XKUkdEscaJYJUD

  ### Ticket rewritten to the brief format (2026-11-12, supersedes "Ticket text to file" above)

  Team: Tipping (TIP). Labels: none. Related: ENT-8148.

  Title: Wallets and departments lists run 7-8 queries per staff member

  ## Summary

  `GET /api/hotels/{slug}/wallets` and `GET /api/hotels/{slug}/departments` serialize `WalletProfileSchema` per staff member, and each row costs 7-8 queries, one of them a tips configuration read on the writer. Departments takes 800-1,300 requests per 3h window at p95 2.2-2.8s; wallets runs 215 statements per request at p95 3.0-3.9s. A six-file change with no migration takes both to 2 queries per row.

  ## Context

  - `wallets/schemas/wallet_profile.py:42` `get_payout_vendor` calls `TipsSelector.get_payout_vendor_of_wallet` per row. That refetches the hotel by slug, reads `Configuration` through `get_config_by_hotel` (`@no_readonly_database` since #24158) and loads `payout_config` lazily.
  - `wallets/selectors/wallet.py:97` and `wallets/selectors/wallet_terms_accept.py:35` build fresh querysets, so a prefetch of terms acceptances is ignored.
  - `hotels/schemas/department.py:45` and `hotels/selectors/department.py:31` load tip links without `short_link`.
  - ENT-8148 covers the same writer read on the `serialize_hotel` path.

  ## Evidence

  Datadog spans, 2026-10-21 to 2026-11-04:

  | Endpoint | Requests per 3h | p50 | p95 | Statements per request |
  | --- | --- | --- | --- | --- |
  | wallets | about 60 | 0.82-1.01s | 3.0-3.9s | 215 (1.07s DB) |
  | departments | 800-1,300 | 0.16-0.20s | 2.2-2.8s | 105 (0.43s DB) |

  ## Reproduction

  Local, through the real views with `CaptureQueriesContext`, master at afd8338fce62. One hotel with a tips configuration and a Stripe payout configuration; N staff, each with a wallet, two terms acceptances and a tip link with a short link.

  | Endpoint | N | Queries now | With the fix |
  | --- | --- | --- | --- |
  | wallets | 5 | 47 | 23 |
  | wallets | 20 | 152 | 53 |
  | departments | 5 | 57 | 25 |
  | departments | 20 | 177 | 55 |

  ## Definition of done

  - Both endpoints add at most 2 queries per staff member, held by a query-count test on each.
  - Neither endpoint reads the tips configuration from the writer.

  +++ Agent notes

  - Gareth Lloyd has the fix (19 insertions, 14 deletions) and the two query-count tests uncommitted locally; 398 existing wallet, department and tips tests pass with it. Ask for the diff.
  - Fix shape: `get_tip_payout_config` reads `Configuration.objects.select_related("payout_config")` by hotel; `get_payout_vendor_of_wallet` uses `select_related("hotel")`; the terms selectors read `wallet.wallet_terms_accepts.all()`; both list querysets prefetch `wallet__wallet_terms_accepts` and join `tip_link__short_link`.
  - Review point: `get_tip_payout_config` is also called from `tips/services/tip_payout.py:196`, `:295` and `wallets/selectors/wallet.py:164`. With the fix those reads move to the replica too. Not tested for replica lag on the payout path.
  - The last 2 queries per row need the payout vendor annotated on the list queryset; `HotelWalletProfileSchema` is used by 4+ views, so it was left out.
  - The `SELECT 1` x53 on wallets is the nested `@readonly_database` health check, tracked separately.

  +++

  ### Wider duplicate search (2026-11-12, all teams, archived included)

  No open ticket covers this. Searched Linear by symbol (get_payout_vendor_of_wallet, WalletProfileSchema, get_tip_payout_config, get_config_by_hotel, wallet_terms_accepts, no_readonly_database), by endpoint path and by topic (N+1 tipping, dashboard latency). Judged on titles, plus the ENT-8148 description.
  - Related, open: ENT-8148 (https://linear.app/canary-technologies/issue/ENT-8148/serialize-hotel-reads-tips-configuration-and-the-hotel-theme-from-the), same get_config_by_hotel writer read, on serialize_hotel. Different endpoint.
  - Prior art, Done: TIP-718 "Improve Get Departments API Performance" (2023, https://linear.app/canary-technologies/issue/TIP-718/improve-get-departments-api-performance), TIP-2231 "Engineering Only Improvement for Get Hotel Wallets Api" (2024, https://linear.app/canary-technologies/issue/TIP-2231/engineering-only-improvement-for-get-hotel-wallets-api).
  - Bears on the replica review point: PMS-9441 (https://linear.app/canary-technologies/issue/PMS-9441/investigate-readonly-database-may-not-route-replica-reads-when-the), Backlog.
project: 2026-04-16T1351-ship
source_id: null
tags: []
time_minutes: null
title: 'Verify and file ticket: Wallets and departments lists run 7-8 queries per
  staff member'
updated: 2026-11-12 12:44:28.545406
waiting_on: null
waiting_since: null
working_on: false
---

**Team:** Tipping (TIP)

**Context:** Departments is high volume (800-1,300 req per 3h). Wallets runs 215 statements/request and reads tips config from the writer. Six files, no migration; 7 -> 2 queries per row.

Source: dashboard latency audit, agent run 2026-11-09 (GTD item 2026-11-04T1957-dashboard-latency-audit...). Draft, fix diff, repro test and SQL dumps: backend/canary/tmp/dashboard_latency_repros/ (gitignored). Fixes and new tests are UNCOMMITTED on master in the main canary checkout. Audit page: https://claude.ai/artifact/QzNanTU2XKUkdEscaJYJUD. Excluded as already covered: chat/threads (PR #63670, SRE-1535), chat/messages (SRE-1745), check-in search (AD-10218 1.1).

---

## Ticket draft (06_TIP_wallets_departments.md)

Team: Tipping (TIP)
Title: Wallets and departments lists run 7-8 queries per staff member (payout vendor via a hotel slug refetch on the writer, terms accept, short link)
Labels: backend, performance
Related: ENT-8148 (tips configuration read from the primary on a GET), AD-10218 section 6 (department disbursement N+1, different endpoint)
---
## Problem

Two dashboard endpoints serialize `WalletProfileSchema` per staff member and pay the same chain per row:

- `GET /api/hotels/{slug}/wallets`: p50 0.82-1.01s, p95 3.0-3.9s, about 60 requests per 3h window. 215 statements per request (1.07s DB): per wallet, hotelslug+hotel x26, tips_configuration x25, wallettermsaccept x25, payouts_configuration x25, hotelwalletprofile x25, hotel IN x25, plus `SELECT 1` x53.
- `GET /api/hotels/{slug}/departments`: p50 0.16-0.20s, p95 2.2-2.8s, 800-1,300 requests per 3h window. 105 statements per request (0.43s DB): the same chain per staff member x10 plus shortlink x14.

(Datadog spans, 2026-10-21 to 2026-11-04.) The tips configuration read goes to the writer (`@no_readonly_database`).

## Reproduction (local, through the real views)

Tests: `backend/canary/wallets/tests/views/test_hotel_wallets_query_count.py`, `backend/canary/hotels/tests/views/api/test_departments_query_count.py`. One hotel with a tips Configuration and a Stripe payout configuration; N wallets with a profile, two terms acceptances, a HotelWalletProfile in a department and an individual TipLink with a short link; two departments with department tip links.

| Endpoint | N | before | after | per row before | per row after |
| --- | --- | --- | --- | --- | --- |
| wallets | 5 | 47 | 23 | 7 | 2 |
| wallets | 20 | 152 | 53 | 7 | 2 |
| departments | 5 | 57 | 25 | 8 (+1 short link per department) | 2 |
| departments | 20 | 177 | 55 | 8 (+1 short link per department) | 2 |

The per-row shape matches the production statement list exactly.

## Causes (verified)

- `wallets/schemas/wallet_profile.py:42-43` `get_payout_vendor` -> `TipsSelector.get_payout_vendor_of_wallet` per wallet.
- `tips/selectors/tips.py:473` `hotelwalletprofile_set.prefetch_related("hotel")...first()`: a prefetch on a forward FK for one row is an extra `hotels_hotel IN (?)` query.
- `tips/selectors/tips.py:463` `get_tip_payout_config` -> `get_config_by_hotel_slug(hotel.slug_name)` -> `hotels/selectors/hotel.py:48` refetches the Hotel it was handed through `HotelSlug`; `tips.py:66-68` `get_config_by_hotel` is `@no_readonly_database` with no `select_related("payout_config")`, so the config read hits the writer and `:464` loads the payout config lazily.
- `wallets/selectors/wallet.py:97` `wallet_terms_accepts.latest(...)` and `wallets/selectors/wallet_terms_accept.py:35` `.exists()` build fresh querysets that ignore any prefetch.
- `hotels/schemas/department.py:45-46` staff queryset prefetches `tip_link` but not `short_link`; `hotels/selectors/department.py:31` same for department tip links.

## Fix (diff attached, 6 files, no migration)

- `get_tip_payout_config`: `get_canary_object_or_404(Configuration.objects.select_related("payout_config"), hotel=hotel)`; no slug round trip, stays on the replica. `get_payout_vendor_of_wallet`: `select_related("hotel")`.
- Terms selectors read `wallet.wallet_terms_accepts.all()` so a prefetch is honoured; the wallets view and the department staff queryset prefetch `wallet__wallet_terms_accepts`.
- `select_related("tip_link__short_link")` on the staff queryset and the department selector.
- Existing tests: 382 of 402 pass; the 20 failures are PyJWT `InsecureKeyLengthWarning` from a newer PyJWT on an 18-byte test key, unrelated (all pass with the warning ignored).

## Expected impact

Removes about 125 of the 162 non-health-check statements per wallets request and about 60 of 105 per departments request (800-1,300 requests per 3h window), and moves the tips configuration read off the writer.

Follow-up for the remaining 2 per row: annotate the payout vendor on the list queryset with a `Subquery` over `HotelWalletProfile` ordered by `hotel__created_at` and have `WalletProfileSchema.get_payout_vendor` read the annotation; touches a schema used by 4+ views.

+++ Agent notes

- `SELECT 1` x53 is the platform ticket (nested `@readonly_database`, `tips.py:460` and `:59` are two of the per-row entries).
- Run: `direnv exec . pytest wallets/tests/views/test_hotel_wallets_query_count.py hotels/tests/views/api/test_departments_query_count.py --nomigrations -q`.

+++