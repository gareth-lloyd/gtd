---
area: null
contexts: []
created: 2026-06-03 11:14:57.848553
defer_until: null
due: null
energy: low
id: 2026-06-03T1114-from-conversation-with-james-get-salesforce-deal-i
order: null
output: |
  ## Agent run 2026-06-03T13:18:00

  Feasibility + design analysis. **Verdict: very feasible — most plumbing already
  exists.** This is mostly a small "join + new label set" feature, not a new
  integration.

  ### The key insight: "significant deals" are ALREADY a curated list
  The hand-maintained dict `PARENT_OPPORTUNITY_ID_TO_ENTERPRISE_DEPLOYMENT` in
  `backend/canary/onboarding/services/types.py:35-52` IS the answer to "how to
  identify SF deals / which are strategic". It maps 16 Salesforce **parent
  opportunity IDs** to an `EnterpriseDeployment` enum (Wyndham Connect GMS, BW GMS
  mandated/non-mandated, IHG Pilot, Aimbridge/Pyramid Digital Tipping, Marriott
  Vacations Worldwide, Four Seasons Payments, TUI Blue, etc.). Onboarding already
  treats exactly these as the strategic enterprise rollouts. We get the curation for
  free — no new "is this deal important?" heuristic needed for v1.

  ### Data is already cached locally with the right shape
  FK chain: `Hotel` → `SalesforceHotelAccount` (nullable FK `hotel`) →
  `SalesforceOpportunity` (related_name `opportunities`).
  - `SalesforceOpportunity.parent_opportunity_id` (`onboarding/models/salesforce_opportunity.py`)
    is the field to map through the dict above → `EnterpriseDeployment`.
  - The local cache is **already biased to significant deals**: the sync SOQL in
    `SalesforceOpportunityService.get_opportunities_for_account_from_salesforce`
    only pulls opps where `Enterprise_Deployment__c = true` OR (active stage:
    CLOSING/CLOSED_WON/CONFERENCE_SIGNED/TRIAL AND record type = Hotels). So a
    cached `SalesforceOpportunity` row with a parent_opportunity_id in the dict is
    a confirmed strategic deal membership.

  ### Recommended implementation (small)
  1. **New helper** (onboarding service), e.g.
     `SalesforceOpportunityService.get_enterprise_deployments_for_hotel(hotel) -> set[EnterpriseDeployment]`:
     read `hotel.salesforcehotelaccount.opportunities`, map each
     `parent_opportunity_id` through `PARENT_OPPORTUNITY_ID_TO_ENTERPRISE_DEPLOYMENT`,
     return the set. (Reuse `derive_onboarding_type` pattern that already does this
     lookup during sync.)
  2. **New Linear label set** — one label per `EnterpriseDeployment` (e.g.
     "Deal: Wyndham Connect GMS"). Add to `LinearLabelName` (`linear/constants.py`)
     and a `EnterpriseDeployment -> LinearLabelName` map. These form a label group
     so only one deal label applies (matches existing `filter_by_group` behavior).
  3. **Wire into label application** — `LabelApplicationService.apply_labels_to_issue`
     (`linear_agent/services/label_application.py`) already receives `resolved_hotels`
     and applies region/datacenter labels off the first resolved hotel. Add deal
     labels there using the same `resolved_hotels[0].entity` hotel. Lowest-risk
     insertion point; no LLM changes needed (deal detection is deterministic, not a
     prompt recommendation — keep it out of the LLM).

  ### Lazy-load / freshness (answers the item's open questions)
  - **Freshness signal:** use `SalesforceHotelAccount.last_salesforce_sync` (NOT
    `updated_at`). Both `SalesforceHotelAccount` and `SalesforceOpportunity` carry a
    dedicated `last_salesforce_sync` timestamp — that is the canonical "how fresh is
    the SF data" field. `updated_at` changes on any row write and is misleading.
  - **The "are all opps present locally?" trap:** absence of `SalesforceOpportunity`
    rows is ambiguous — it can mean "genuinely not in any enterprise deal" OR "never
    synced". Disambiguate with the **account-level** `last_salesforce_sync`: if the
    account was synced recently and produced zero enterprise opps, the hotel
    genuinely isn't in a strategic deal. So gate on the account, not on opp presence.
  - **Lazy refresh:** if `hotel.salesforcehotelaccount` is missing OR
    `account.last_salesforce_sync` is null/older than a threshold (suggest ~7 days),
    call `SalesforceOpportunityService.sync_opportunities_for_account(account_id)`
    to refresh from the SF API, then read locally. The on-demand sync method already
    exists and is idempotent (`update_or_create` upsert, `@transaction.atomic`).
  - **Caution — do NOT sync inline in the webhook hot path** for every triaged
    issue: `create_salesforce_client()` logs into Salesforce (cached 30 min TTL) and
    a SOQL round-trip adds latency + lockout risk. Triage already runs async via the
    `triage_issue_async` Celery task, so a lazy sync there is acceptable, but prefer
    "read cache; only sync if stale" rather than "always sync". For scale, consider a
    nightly cron that refreshes accounts for hotels with recent Linear activity so
    the cache is almost always warm and the agent never blocks on Salesforce.

  ### Scope / open questions for James (not decided here)
  - Label ALL enterprise deployments, or only a top-tier subset (e.g. the mandated
    GMS rollouts)? The dict is the natural v1 = label all 16.
  - Do we want the deal label only on the curated parent-opp list, or also a generic
    "Enterprise Deal" label for any opp with `Enterprise_Deployment__c=true` whose
    parent isn't yet in the dict (catches new deals before someone adds the ID)?
  - Where should the curated list live long-term? Today it's a Python dict in
    onboarding; if Linear triage also depends on it, that's fine (import it) but
    worth noting the coupling.

  ### Key files
  - `backend/canary/onboarding/services/types.py:13-71` — EnterpriseDeployment enum +
    PARENT_OPPORTUNITY_ID_TO_ENTERPRISE_DEPLOYMENT (the curated deal list)
  - `backend/canary/onboarding/models/salesforce_opportunity.py` — SalesforceOpportunity (parent_opportunity_id, last_salesforce_sync, stage, arr)
  - `backend/canary/onboarding/models/salesforce_hotel_account.py` — SalesforceHotelAccount (hotel FK, last_salesforce_sync)
  - `backend/canary/onboarding/services/salesforce_opportunity.py:268-347` — sync_opportunities_for_account (lazy-load entry point)
  - `backend/canary/linear_agent/services/label_application.py:30-90` — where to add deal labels (gets resolved_hotels)
  - `backend/canary/linear/constants.py` — LinearLabelName (add deal labels)

  No code changes made — this was analysis only.
project: null
source_id: null
tags: []
time_minutes: 5
title: 'From conversation with james: get salesforce deal into linear triage'
updated: 2026-06-03 13:18:00.000000
waiting_on: null
waiting_since: null
working_on: false
---

Linear agent should be able to detect from hotel which significant deal the hotel is part of, and label accordingly

* Will require analysis of salesforce opportunities, plus some knowledge of which deals are strategic / important
* Agent should be able to pick this up from `SalesforceOpportunity` locally cached data, which can lazily load, falling back to salesforce api if old or not present
  * Of course, we'd need to know taht all SF Opps were present locally. Use SalesforceHotelAccount updated_at to guess?

* How to identify SF deals?