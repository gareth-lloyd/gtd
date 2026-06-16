---
area: null
contexts: []
created: 2026-06-16 13:29:49.019946
defer_until: null
due: null
energy: low
id: 2026-06-16T1329-review-this-notion-design
order: null
output: |
  ## Agent run 2026-06-16T10:33:14Z

  Reviewed the PRD "🤖 Automated Hotel Creation from Canary Opportunity"
  (https://app.notion.com/p/Automated-Hotel-Creation-from-Canary-Opportunity-37281468615181d68527e71ebf07a696).
  Cross-checked its technical claims against the canary backend and against the sibling
  eng-investigation doc.

  Verdict: solid, well-structured PRD. The pivot from webhook → reusing the existing
  4-hour SF sync is the right call and is the doc's strongest decision. But there are a
  few substantive issues an eng spec should resolve before building, and one strategic
  question the doc dodges. Details below, ordered by importance.

  ### 1. The doc doesn't confront its own sibling research's conclusion (strategic)
  The linked "Automate onboarding creation investigation"
  (https://app.notion.com/p/379814686151808e806dd25314b74c68) concludes the payoff here
  is marginal: anyone who needs a hotel immediately already creates it manually in ~2 min
  via /manage/onboarding/create; the 4hr lag only affects hotels nobody needed urgently;
  "time spent onboarding a hotel will not change." That conclusion was aimed at the
  webhook approach — but it bites HARDER under the chosen 4-hour-sync approach, because
  the sync gives ~0 latency improvement (still up to 4hr). So the ENTIRE payoff of v1 is
  "remove the manual click," not latency. The PRD's Problem section still leads with
  "0–4+ hours of latency" and the Success Metrics still track median opp→hotel time
  (<4hr) — but the 4hr-sync design cannot move that needle, and that metric is trivially
  met by construction (sync cadence bounds it). Recommend: explicitly re-frame the value
  prop as capacity/click-removal + removing the DISABLED interim-state confusion, drop or
  demote the latency framing, and reconcile head-on with the investigation's skepticism so
  reviewers don't read the two docs and find them contradictory.

  ### 2. Trigger condition is imprecisely worded throughout (precision)
  HOTEL-AUTO-001 and several spots say the trigger is "when a Salesforce opportunity is
  created." Per the investigation doc the real condition is when an opportunity changes
  STAGE to match the "ready to be onboarded" criteria — not creation. This matters: eng
  could wire the gate to the wrong event. The JTBD already says it correctly ("marked
  ready for implementation"). Make the requirement language match the JTBD.

  ### 3. "The sync already creates the property row" — half true; tighten it (correctness)
  Code check: the 4-hour sync (SalesforceEnterpriseDeploymentService.
  sync_accounts_and_opportunities_for_region) creates/updates CohortHotel + Salesforce
  metadata rows — that's the row that shows on the Properties page in DISABLED limbo. It
  does NOT create the Hotel object today; that still happens via onboard_hotel_from_
  salesforce_account(). So HOTEL-AUTO-001's lift is "have the sync also call onboard_hotel_
  from_salesforce_account() in the same run." The rationale's phrasing ("already creates
  the property row") blurs CohortHotel-row vs Hotel-object and undersells what's being
  added. Confirmed onboard_hotel_from_salesforce_account() IS wrapped in
  transaction.atomic() (onboarding/services/onboarding.py ~L342), so the doc's atomicity
  claim holds — good.

  ### 4. HOTEL-AUTO-004 AC#2 is blocked on Open Question #4 — flag the contradiction
  AC#2 ("operator sets Account.Canary_Environment__c beforehand to force an env") depends
  on the field being readable BEFORE creation. But Open Question #4 + Rami's Slack answer
  establish that Canary_Environment__c is written by Canary's SF push AFTER the hotel is
  created (it's a post-creation mirror, empty at trigger time for net-new). So AC#2 as
  written describes behavior that does not exist and is gated on an unresolved question
  about inverting that dependency. For v1 the only tier that actually fires for net-new is
  the country fallback (BillingAddress). Recommend: either move AC#2 out of v1 / mark it
  explicitly blocked-on-OQ#4, or scope OQ#4 first. Also: I could confirm the country→region
  fallback exists (canary/region.py, COUNTRY_TO_CANARY_REGION) but could NOT confirm the
  "enterprise brand + country overrides win first" tier-1 logic in code — eng should verify
  that tier-1 path exists before the AC assumes it.

  ### 5. Idempotency / double-creation needs to be an explicit requirement (risk)
  Rami's doc flagged guarding against the sync tripping creation twice. Since v1 IS the
  recurring sync, every 4hr tick re-sees the same eligible opportunities. The design leans
  on onboard_hotel_from_salesforce_account() being get-or-create (it creates the Hotel
  "if one doesn't exist"), which is probably sufficient — but it's load-bearing and isn't
  called out. Add an explicit idempotency requirement + a test that a second sync run over
  the same opp is a no-op (not a duplicate/exception).

  ### 6. Smaller points
  - HOTEL-AUTO-003 gate is real: can_create_new_hotels is a per-OnboardingType flag
    (onboarding/models/property_configuration_processes.py); enterprise/cohort types are
    False, DEFAULT is True. Gate maps cleanly. Good — but the "Confirm with enterprise
    team" caveat appears in 3 places; it's a real launch blocker, surface it once in
    Dependencies and reference it.
  - HOTEL-AUTO-005 retry semantics (retry-next-tick vs park-and-wait) is a Must-Have with
    undecided behavior (Open Q #2). Fine to defer to eng spec, but the observability
    surface depends on the choice — note that dependency.
  - Product Configuration Activity (the proposed log surface) is event-backed
    (onboarding/views/product_activation_events.py, /api/product-configuration-activity/),
    not a standalone model — confirm an auto-trigger "fire" maps to an Event the feed
    queries, or the events won't show up there.
  - Release Plan (Phase 1/2) and Feature flag are empty/TBD — needs filling before kickoff.
  - Success Metric "% created without manual click ≥80%" is the right headline metric and
    actually measures the v1 payoff; promote it over the latency metric (see #1).

  Note: did NOT post anything to Notion. This review is recorded here only — paste/adapt
  into a Notion comment yourself if you want it on the doc.
project: null
source_id: null
tags: []
time_minutes: 5
title: review this notion design
updated: 2026-06-16 10:33:14.000000
waiting_on: null
waiting_since: null
working_on: false
---

https://app.notion.com/p/Automated-Hotel-Creation-from-Canary-Opportunity-37281468615181d68527e71ebf07a696?pvs=0