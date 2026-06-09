---
area: null
contexts: []
created: 2026-06-08 12:45:44.035913
defer_until: null
due: null
energy: low
id: 2026-06-08T1245-check-salesforce-opportunity-strategic-data-qualit
order: null
output: |
  ## Agent run 2026-06-08T11:32:00Z

  Context: Notion playbook §3 (EMEA Strategic Account Launch) entry criteria are
  Salesforce-driven. Discussion thread: you asked for an "Is Strategic" flag on the
  Opportunity (like the existing "is enterprise" flag); sales ops found one already
  exists. Your open question: is it used, and would repurposing it conflict? I queried
  prod Salesforce (read-only SOQL via debug shell) to assess data quality.

  FIELDS FOUND
  - Opportunity.Strategic_Account__c (boolean) — the deal-level flag. 62 True /
    100,913 (0.1%). THIS is the right field for the playbook.
  - Account.CS_Strategic_Account__c (boolean) — CS-owned, Account-grain. 3,187 True /
    711,242 (0.4%). NOT the one to use (wrong grain, already owned by CS, would conflict).
  - Baseline Enterprise_Deployment__c (the "is enterprise" analog): 27,159 True (26.9%)
    — what a genuinely-used flag looks like, for comparison.

  VERDICT
  - Opportunity.Strategic_Account__c is effectively a clean slate (0.1% populated vs
    26.9% for the enterprise flag) -> LOW conflict risk to adopt for the launch process.
  - Caveats before declaring it unused: (1) 62 records means someone sets it — confirm
    with sales ops what they are + whether any reports/validation rules/flows read it
    (SOQL can't see those). (2) The 0 OpportunityFieldHistory rows are INCONCLUSIVE
    (history tracking likely just not enabled for this field), not proof of disuse.
  - Account.CS_Strategic_Account__c: keep out of scope — Account-level, CS-owned, 50x
    more populated; repurposing would conflict.
  - Do NOT conflate with Canary-side Hotel.is_strategic_account (internal DB boolean,
    exists since 2022, separate system).

  DECIDING NEXT STEP (not yet run): pull the 62 flagged opportunities (Account name,
  BillingCountry, owner, stage, created date) to see if they're the EMEA strategic
  accounts the playbook targets (Grecotel/Eurostars/De Luna/Danubius/Travelodge). If
  yes, the field is already maintained for this purpose; if random, it's an unmaintained
  orphan that's safe to claim. Follow-up SOQL script was prepared and copied to clipboard
  during the session.

  No writes made. No external-service actions taken.

  ## Agent run 2026-06-08T11:40:00Z (follow-up: code refs + profile of the 62)

  CODE REFERENCES: Zero. Repo-wide grep finds NO references to Strategic_Account__c
  or CS_Strategic_Account__c anywhere (backend or frontend). Canary code neither reads
  nor writes either field -> no code-side conflict from repurposing. Any usage is
  purely Salesforce-side (manual edits / reports / validation rules / flows).

  PROFILE OF THE 62 FLAGGED OPPORTUNITIES (Opportunity.Strategic_Account__c = True):
  - It's a loose, manually-curated "marquee logo" sales tag, NOT an EMEA or process
    cohort. 68% US (42/62), Canada 5, only ~12 EMEA (Spain 3, Germany 3, Ireland 2,
    Switzerland/Italy/Hungary/UK x1).
  - Big enterprise logos: Wyndham (x6), Marriott, Hyatt, Four Seasons, IHG, Best
    Western, Choice, Caesars, Disney, Omni, Rosewood, Sonesta, Aimbridge, TUI, Dalata.
  - Full lifecycle incl. dead deals: Closed Lost 20, Closing 17, Closed Won 10, plus
    Demo/Trial/Verbal/Qualified. NOT gated to live/won.
  - Mixed grain: account-level ("(Parent Brand)"/"(Management Company)") AND
    product-level ("- Tipping"/"- Kiosk"/"- GMS"). Many different owners.

  DECISIVE FINDING: the flag does NOT identify the playbook's target EMEA launches.
  Of the named accounts (Grecotel, Eurostars, De Luna, Danubius, Travelodge), ONLY
  Danubius is flagged. Grecotel (the at-risk flagship the playbook is built around) is
  not tagged at all. So the field is not currently maintained for §3's purpose.

  WHEN USED (CreatedDate of flagged opps): spans 2022-08 -> 2026-05.
  2022:1, 2023:7, 2024:24, 2025:25, 2026-YTD:5. Most recent created 2026-05-15 (3 wks
  before query) => continuous, still-active manual use, not a one-off backfill.
  Caveat: field history is OFF, so CreatedDate != flag-set date; can't reconstruct a
  precise flag-set timeline from SOQL.

  REVISED VERDICT: No code conflict, but a real SEMANTIC/PROCESS conflict. AEs already
  use Strategic_Account__c as a broad all-region full-lifecycle "big logo" marker.
  Overloading it as the EMEA soft-launch trigger means inheriting 62 mostly-US,
  mostly-irrelevant records (20 dead), cleanup, and fighting the existing sales mental
  model -- and it doesn't even contain Grecotel.
  RECOMMENDATION: don't repurpose as the trigger. Prefer (a) a NEW dedicated field
  (e.g. EMEA_Soft_Launch_QA__c) -- cleanest; or (b) keep Strategic_Account__c as a soft
  marquee signal and gate the playbook trigger on a tightened definition + approver
  (per the Notion thread). Data favours (a).

  ## Agent run 2026-06-08T11:43:00Z (Type / Amount / parent-child of the 62)

  TYPE: 33 New Business / 29 Expansion (even land-and-grow split).

  SIZE: flag is NOT gated to deal value. 60 populated (2 null), min $0, median ~$6.9k,
  max $1.67M. Only 14/60 are >= $40k; 46 below the §3 bar. Caveat: opp Amount is
  per-product-line, not account ARR, so not a clean test of §3's account-ARR criterion
  -- but confirms the flag is subjective, uncorrelated with opp size.

  PARENT/CHILD: 0/62 are children (all top-level). 30/62 are parents with ~17,145 child
  opps total -- dominated by the big mandates: Wyndham NA GMS Mandate 6,521, Wyndham
  Tipping 5,541, Wyndham Connect Plus 1,888, Wyndham GMS Intl 1,274, Best Western GMS
  1,003, IHG GMS 439. The other 32 are standalone top-level opps (product demos/trials,
  many Closed Lost). => The flag lives on marquee PARENT/mandate deals; the thousands
  of per-property child opps are unflagged. Tooling filtering Strategic_Account__c=true
  gets the ~62 parents, not the 17k properties.

  FINAL READ (reinforced): account-level marquee-logo tag, in active use, zero code
  deps, but genuine semantic conflict with the playbook meaning and missing Grecotel +
  most EMEA targets. Recommendation unchanged: do NOT repurpose as the EMEA soft-launch
  trigger -- prefer a new dedicated field, or a tightened-definition + approver gate.
  Data favours a new field.

  FOLLOW-UP POSTED: a plain factual summary of these findings was posted to Linear
  TOOL-262 (Auto-label triage issues with the strategic SF deal a hotel belongs to),
  answering its step-2 due-diligence question. Confirmed the curated dict
  PARENT_OPPORTUNITY_ID_TO_ENTERPRISE_DEPLOYMENT (16 entries, all US/large enterprise)
  does not contain Grecotel/Eurostars/De Luna, and those three are not among the 62
  Strategic_Account__c=True opps either. Open: not yet queried whether those three
  accounts have parent opportunities in SF at all.

  Only external action taken: the TOOL-262 comment (user-approved). No data writes.
project: null
source_id: null
tags: []
time_minutes: 5
title: Check Salesforce opportunity strategic data quality
updated: 2026-06-08 14:46:01.763989
waiting_on: null
waiting_since: null
working_on: false
---

https://app.notion.com/p/canarytechnologies/Strategic-Account-Launch-Playbook-EMEA-Soft-Launch-QA-36781468615181b885cefd2197cd6207?source=copy_link#642d08880dd84cd2b6d2718dea127e1b