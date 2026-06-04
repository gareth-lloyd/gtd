---
area: null
contexts: []
created: 2026-06-03 19:47:15.449689
defer_until: null
due: null
energy: low
id: 2026-06-03T1947-do-the-due-diligence-on-tool-262-to-see-if-this-wo
order: null
output: |
  ## Agent run 2026-06-04T10:17Z — Due diligence on TOOL-262 (deal auto-labelling for Grecotel/Eurostars/De Luna)

  ### Bottom line
  v1 as written in TOOL-262 (map `parent_opportunity_id` → curated
  `PARENT_OPPORTUNITY_ID_TO_ENTERPRISE_DEPLOYMENT` dict) will label **nothing** for
  Grecotel, Eurostars, or De Luna. None of them are in the curated list, and the
  proposed `Enterprise_Deployment__c = true` fallback almost certainly won't catch them
  either. The mechanism is sound for the mandated brand rollouts it was built for
  (BW/Wyndham/IHG/Marriott) — it just doesn't reach EMEA strategic SMB chains. To cover
  the accounts that actually motivated the playbook, we need a deal-level signal that
  Sales/CS own, i.e. effectively a "strategic" flag. So: answer to Q2 is **yes, lean
  toward a flag**; answer to Q1 is **only partially / not for these accounts as-is**.

  ### Q1 — Can we actually use Salesforce this way?
  Mechanically the FK chain exists and works:
  `Hotel → SalesforceHotelAccount → SalesforceOpportunity.parent_opportunity_id`
  (`onboarding/models/salesforce_opportunity.py:29,98`). It is exactly what onboarding
  already uses (`onboarding/salesforce.py:346`, `services/types.py:101 derive_onboarding_type`).
  Two problems specific to Grecotel/Eurostars/De Luna:

  1. **The curated dict is 16 mandated enterprise rollouts only** — all BW / Wyndham /
     IHG / Aimbridge / Pyramid / Four Seasons / Marriott Vacations / Drury / TUI
     (`onboarding/services/types.py:35-52`). Zero EMEA strategic accounts. A Grecotel
     opp's `parent_opportunity_id` (if it has one) returns `None` from the dict → no label.
  2. **We store only the parent opp *ID*, never its name** (model has
     `parent_opportunity_id` but no name field). So an ID that isn't in the dict is
     opaque — you can't tell "this is Grecotel" without a separate Salesforce lookup.
     Identifying + hardcoding each EMEA parent ID is manual and doesn't scale.

  Will the data even be in the local cache? The sync SOQL
  (`services/salesforce_opportunity.py:242-265`) pulls opps where
  `Enterprise_Deployment__c = true` **OR** (`StageName IN (Closed Won/Closed Lost/
  Negotiation/Proposal) AND Account_Record_Type__c = 'Hotels'`). A live Grecotel
  property = Closed Won + Hotels record type, so its opp **would** sync *if an account
  sync has ever run for that hotel*. But:
  - `Enterprise_Deployment__c` is almost certainly **false** for these (they're not in
    the mandated-deployment program), so the ticket's proposed generic "Enterprise Deal"
    fallback label also misses them.
  - Whether a single shared **parent opportunity** even exists per EMEA chain is unknown.
    Parent/child opp structure is a Salesforce convention used for the big multi-brand
    mandated rollouts; a boutique chain or single-property deal may have no parent opp at
    all, or one parent per property. **This is the one fact I could not verify from code —
    it needs a prod/Salesforce read (see "Not yet verified" below).**

  ### Q2 — Do we need an "is strategic parent opportunity" flag on Opportunity?
  Recommend **yes** (or an equivalent Salesforce-owned signal). Rationale:
  - The curated Python dict requires an engineer to hand-add each parent ID and stores no
    name — wrong tool for a sales-driven, growing set of strategic launches. It will
    chronically lag reality (the ticket's own open question admits this).
  - There is **no deal-level strategic concept in Salesforce today**. The only existing
    flag is `Enterprise_Deployment__c` (`services/salesforce_opportunity.py:31`), which
    means "mandated enterprise rollout", not "strategic launch we're QA-gating". They are
    not the same set — the playbook's strategic accounts (Grecotel/Eurostars/De Luna/
    Danubius/Travelodge) are mostly NOT enterprise deployments.
  - There IS already a `Hotel.is_strategic_account` boolean (`hotels/models/hotel.py:525`,
    admin-editable) — but it's a manual *hotel-level* internal flag, tells you nothing
    about *which deal*, and isn't sourced from Salesforce. Useful as a coarse prioritise
    signal, not as the deal attribution TOOL-262 wants.

  A Salesforce checkbox like `Is_Strategic_Launch__c` (set by Sales/CS at deal level),
  synced down onto `SalesforceOpportunity`, would: cover EMEA accounts the dict can't,
  remove the need to hardcode IDs, and give triage a declarative "is this a strategic
  launch" signal. If we also sync the parent opp **name**, the label can be
  self-describing without a dict at all.

  ### Suggested shape for TOOL-262
  - Keep the curated-dict path for the mandated rollouts (it's correct + deterministic).
  - Add a Salesforce-sourced strategic flag (+ ideally parent/opp name) as the primary
    signal for everything else, so Grecotel/Eurostars/De Luna get labelled without code
    changes per deal. This is the bit that makes the playbook's at-risk accounts visible
    in triage, which is the whole point of the ticket.
  - Confirm the lazy-sync freshness guard still applies (account-level
    `last_salesforce_sync`, async task only — never in the webhook hot path; matches the
    ticket).

  ### Not yet verified (needs a read-only prod/Salesforce lookup — did NOT run, no approval)
  Per repo + GTD-agent safety rules I did not query staging/prod. To close the loop, run
  (read-only) for each of Grecotel / Eurostars / De Luna:
  - Does a `Hotel` exist, and does it have a `SalesforceHotelAccount` with a non-null
    `last_salesforce_sync`?
  - Do its `SalesforceOpportunity` rows have a `parent_opportunity_id`? Is it shared
    across the chain's hotels (= a real parent opp) or null/per-property?
  - Is `Enterprise_Deployment__c` / our `deployment_segment` set on any of them?
  I can draft the exact ORM/SOQL and run it if you approve hitting prod read-only, or you
  can hand it to onboarding/RevOps. The empirical answer determines whether "add their
  parent IDs to the dict" is even possible, or whether the flag is mandatory.

  ### Key references
  - `onboarding/services/types.py:13-55` — EnterpriseDeployment enum + curated dict (16 IDs)
  - `onboarding/services/salesforce_opportunity.py:242-265` — sync SOQL + filters
  - `onboarding/services/salesforce_opportunity.py:31` — `Enterprise_Deployment__c`
  - `onboarding/salesforce.py:346`, `services/types.py:101` — dict consumption
  - `onboarding/models/salesforce_opportunity.py:29,98` — FK chain + parent_opportunity_id (no name stored)
  - `hotels/models/hotel.py:525` — existing manual `is_strategic_account` hotel flag
  - `linear_agent/services/label_application.py` — where deal labels would be wired in
project: null
source_id: null
tags: []
time_minutes: 5
title: Do the "due diligence" on TOOL-262 to see if this would work for grecotel,
  Del Luna etc
updated: 2026-06-04 10:17:34
waiting_on: null
waiting_since: null
working_on: false
---

* Can we actually use salesforce this way?
* Do we need an "is strategic parent opportunity" flag on opportunity? 

context: https://www.notion.so/canarytechnologies/Strategic-Account-Launch-Playbook-EMEA-Soft-Launch-QA-36781468615181b885cefd2197cd6207?source=copy_link