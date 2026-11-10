---
area: null
completed_at: null
contexts: []
created: &id001 2026-11-10 21:19:47.849588
defer_until: null
due: null
energy: null
id: 2026-11-10T2119-verify-and-file-ticket-get-api-contracts-runs-19-q
order: null
output: ''
project: null
source_id: null
tags: []
time_minutes: null
title: 'Verify and file ticket: GET /api/contracts runs 19 queries and 4 template
  compiles per contract'
updated: *id001
waiting_on: null
waiting_since: null
working_on: false
---

**Team:** SDM

**Context:** Worst p50 on the dashboard (2.1-2.7s). Local 403 -> 45 queries and 80 -> 0 Jinja compiles at 20 rows. Five files, no migration. Sibling of the soft-deleted signer bug.

Source: dashboard latency audit, agent run 2026-11-09 (GTD item 2026-11-04T1957-dashboard-latency-audit...). Draft, fix diff, repro test and SQL dumps: backend/canary/tmp/dashboard_latency_repros/ (gitignored). Fixes and new tests are UNCOMMITTED on master in the main canary checkout. Audit page: https://claude.ai/artifact/QzNanTU2XKUkdEscaJYJUD. Excluded as already covered: chat/threads (PR #63670, SRE-1535), chat/messages (SRE-1745), check-in search (AD-10218 1.1).

---

## Ticket draft (03_SDM_contracts_perf.md)

Team: SDM (SDM)
Title: GET /api/contracts runs 19 queries and 4 template compiles per contract: eager-load in the search combiner
Labels: backend, performance
Related: SRE-1744 (Pinning J, contract activity logs), the sibling ticket "contracts folder filters count soft-deleted signers" (split from this finding)
---
## Problem

`GET /api/contracts` (dashboard contracts list): p50 2.1-2.7s, p95 5.8-8.7s, about 75 requests per 3h window (Datadog spans, 2026-10-21 to 2026-11-04). Each request runs about 377 SQL statements (2.2s of DB time) and 59 Jinja template compiles, about 29 statements per contract on the page.

## Reproduction (local, through the real view)

Test: `backend/canary/contracts/tests/views/test_contracts_list_query_count.py`. N contracts in `DASHBOARD`, two client signers each (one signed), `limit=50`, logged in hotel user.

| N contracts | before queries | after | before Jinja compiles | after |
| --- | --- | --- | --- | --- |
| 5 | 118 | 30 | 20 | 0 (warm) / 2 per process |
| 20 | 403 | 45 | 80 | 0 (warm) / 2 per process |

19 queries per contract before, 1 after (the remaining one is `operation_logs` in `dump_logs`). Production's 29 per contract also includes authform, log and note reads that this seed does not create and this fix does not touch.

Repeated statements at N=20: `authorization_authorizationconfiguration WHERE hotel_id = ?` x62, `hotels_hotel WHERE id = ?` x61, `contracts_contractsigner ... ORDER BY signer_order LIMIT 1` x60, `contracts_contractsigner WHERE contract_id = ?` x40, `contracts_contract WHERE id = ?` x40, then 20 each of signer `exists()`, signer `COUNT(*)`, ordered signers, hellosign contract, contract logs, internal notes.

## Causes (verified against master)

- `contracts/models/contract_models_search_combiner.py:61-65` refetches `Contract.objects.filter(url__in=...)` with only `prefetch_related("authform")`, discarding the view's annotated queryset (`api_views.py:682-726`). No `select_related` for hotel, authorization configuration, created_by, hellosign contract or booking; no signers prefetch.
- `contracts/schemas/contract.py:323-324` `email_subject` and `email_body` each call `_make_contract_link_email`: one signer query and two `from_string` compiles each, so 2 queries and 4 compiles per contract.
- `contracts/schemas/contract.py:366-391` `pre_dump` runs three signer queries per contract (`exists`, `COUNT`, ordered fetch); `post_dump` and `dump_contract_folder` run more.
- `contracts/services/contract_selector.py:232-245` `get_signer_groups` re-reads `signer.contract`, `signer.hotel` and `hotel.authorization_configuration` per signer; `:71-76` `get_guest_facing_domain` reads the configuration on whatever Hotel instance it is handed.
- `backend/shared/shared/utilities/utilities.py:103-117` compiles the Jinja template on every call with no cache.

## Fix (diff attached, 5 files, no migration)

- Combiner: `select_related("hotel__authorization_configuration", "created_by", "hellosign_contract", "booking")`, `prefetch_related("authform", "internal_notes__created_by", Prefetch("signers", ContractSigner.objects.select_related(...).order_by("signer_order")))`.
- `ContractSelector.get_signers_for_contract_in_order(contract)` reads the prefetch when loaded, else the old ordered query. Existing queryset selectors untouched (50 other callers).
- `DashboardContractSchema` resolves the signer list and the link email once per contract.
- `functools.lru_cache` around the sandboxed Jinja `from_string`.
- Existing tests: 93 passed (contracts api views, schemas, selectors, search, views, authorization template security).

## Expected impact

Removes roughly two thirds of the statements per request and all per-contract template compiles. The authform-driven reads (scheduled payments, auth logs, credit card logs) remain and are the next target.

+++ Agent notes

- `ContractSelector` lives at `contracts/services/contract_selector.py`, not `contracts/selectors/`.
- Single-contract views dump the same schema without the prefetch and fall back to the old queries (no worse than before).
- Local run needs `-W "ignore::jwt.warnings.InsecureKeyLengthWarning"` with a current PyJWT (18-byte test key), unrelated to this change.

+++