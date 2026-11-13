---
area: null
completed_at: 2026-11-12 12:44:24.550220
contexts: []
created: 2026-11-10 21:19:47.849588
defer_until: null
due: null
energy: null
id: 2026-11-10T2119-verify-and-file-ticket-get-api-contracts-runs-19-q
order: null
output: |-
  ## Agent run 2026-11-12

  **Status: verified. NOT filed. Filing in Linear needs your explicit yes.**

  ### Verified today (local, master at afd8338fce62)
  - Before the fix (clean throwaway worktree at HEAD, since removed): N=5 gives 118 queries and 20 Jinja compiles; N=20 gives 403 queries and 80 compiles. Matches the draft exactly.
  - After the fix (main checkout, uncommitted): N=5 gives 30 queries; N=20 gives 45 queries. Compiles: 2 on a cold process, 0 once warm.
  - Top repeated statements at N=20 match the draft: authorization configuration x62, hotel x61, first client signer x60, signers x40, contract x40, then 20 each.
  - 93 existing tests pass with the fix (same seven files as the draft plus the two new tests).
  - Behaviour check of the rewrite: `any`/`all` over the signer list equals the old `exists()` / `count() == 0` queries, and the old unordered `.first()` already used the model's default `signer_order` ordering, so the fallback signer is the same.
  - Current origin/master: three of the files are unchanged; `api_views.py` and `utilities.py` changed in unrelated hunks (IP allow-list check, `get_client_ip` logging). The causes still stand. `api_views.py` line numbers are one lower there.
  - No duplicate in Linear (searched SDM and workspace). The sibling soft-deleted signer ticket is not filed yet. SRE-1744 exists and is In Progress: https://linear.app/canary-technologies/issue/SRE-1744/pinning-j-contract-and-authorization-activity-logs-send-a-20-kb-event

  ### Not verified
  - The production numbers (p50 2.1-2.7s, 377 statements, 59 compiles per request). They come from the audit's Datadog spans; I did not re-query them.
  - Pyrefly and `make check-fix` on the fix were not run.

  ### Corrections made to the draft (tickets/03_SDM_contracts_perf.md)
  - Labels: SDM has no `backend` or `performance` label. Replaced with `Feature / SDM: Contracts`.
  - The perf fix is 4 files, not 5. The fifth file (`api_views.py`, one line) belongs to the sibling soft-deleted signer ticket.
  - "diff attached" was wrong: the diff only exists locally (03_contracts/fix.diff, gitignored). The draft now says so.
  - Added the master SHA for the line numbers and the re-run date.

  ### To file (waiting on you)
  - Destination: Linear team SDM, new issue, label `Feature / SDM: Contracts`, related to SRE-1744.
  - Title: GET /api/contracts runs 19 queries and 4 template compiles per contract: eager-load in the search combiner
  - Body: /Users/garethlloyd/projects/canary/backend/canary/tmp/dashboard_latency_repros/tickets/03_SDM_contracts_perf.md (everything below the `---` line)
  - Open choice: the fix is only on your machine. Either I paste the 4-file diff into the ticket's Agent notes, or you push a draft PR and the ticket links it.

  ### Side effects
  - Started the stopped docker container `canary-postgres-1` (needed for tests). Left running.
  - Test DB `test_canary_contracts_verify` created in it.

  ## Agent run 2026-11-12 (second pass)

  Rewrote the ticket to your Linear ticket guide (summary, context, evidence, reproduction, definition of done, agent notes). New text: tickets/03_SDM_contracts_perf.md. The earlier long version is kept beside it as 03_SDM_contracts_perf.long.md. Still NOT filed: waiting for your yes on the exact text.

  ## Agent run 2026-11-12 (third pass: production numbers)

  "Datadog spans" was wrong wording carried over from the audit. The data is in Groundcover (ddtrace-instrumented spans). Re-queried today with `env:production workload:django resource:"GET /api/contracts"`, last 3h: 38 requests, p50 2.15s, p95 8.8s. Three traces had full child spans: about 490 postgres.query spans (about 1.7s DB) and 68-80 jinja2.compile spans per request. That is in line with, and somewhat above, the audit's 377 and 59. Ticket Evidence section updated. The "Not verified" note above about production numbers no longer applies. Still NOT filed.

  ## Agent run 2026-11-12 (filed)

  Filed on your "file ticket": SDM-5353 https://linear.app/canary-technologies/issue/SDM-5353/contracts-dashboard-list-runs-19-queries-and-4-template-compiles-per
  Team SDM, status Triage, label Feature / SDM: Contracts, no assignee, no priority. SRE-1744 was requested as a related issue; it is linked in the body, relation not confirmed in the response. The fix and repro test are still uncommitted on master in the main checkout; the ticket tells SDM to ask you for the diff or a draft PR. The sibling soft-deleted signer ticket is still unfiled (its own GTD item).

  ## Agent run 2026-11-12 (reworded)

  At your request, reworded SDM-5353 so it does not read as accusatory. New title: "Contracts dashboard list: load signers and hotel config up front to cut per-contract queries". New URL: https://linear.app/canary-technologies/issue/SDM-5353/contracts-dashboard-list-load-signers-and-hotel-config-up-front-to-cut
  Changes: summary reframed as a contained win found in a review of all dashboard list endpoints; "worst", "nothing the serializer needs is loaded", "Expected/Actual" and "bug" wording replaced with neutral descriptions. Numbers and definition of done unchanged. The local draft file tickets/03_SDM_contracts_perf.md still has the earlier wording; Linear is the current version.
project: 2026-04-16T1351-ship
source_id: null
tags: []
time_minutes: null
title: 'Verify and file ticket: GET /api/contracts runs 19 queries and 4 template
  compiles per contract'
updated: 2026-11-12 12:44:24.550213
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