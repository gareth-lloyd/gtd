---
area: null
completed_at: null
contexts: []
created: &id001 2026-11-10 21:19:47.888122
defer_until: null
due: null
energy: null
id: 2026-11-10T2119-verify-and-file-ticket-wallets-and-departments-lis
order: null
output: ''
project: null
source_id: null
tags: []
time_minutes: null
title: 'Verify and file ticket: Wallets and departments lists run 7-8 queries per
  staff member'
updated: *id001
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