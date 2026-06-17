---
area: null
contexts: []
created: 2026-06-16 13:29:49.019946
defer_until: null
due: null
energy: low
id: 2026-06-16T1329-review-this-notion-design
order: null
output: "## Agent run 2026-06-16T10:33:14Z\n\nReviewed the PRD \"\U0001F916 Automated
  Hotel Creation from Canary Opportunity\"\n(https://app.notion.com/p/Automated-Hotel-Creation-from-Canary-Opportunity-37281468615181d68527e71ebf07a696).\nCross-checked
  its technical claims against the canary backend and against the sibling\neng-investigation
  doc.\n\nVerdict: solid, well-structured PRD. The pivot from webhook → reusing the
  existing\n4-hour SF sync is the right call and is the doc's strongest decision.
  But there are a\nfew substantive issues an eng spec should resolve before building,
  and one strategic\nquestion the doc dodges. Details below, ordered by importance.\n\n###
  1. The doc doesn't confront its own sibling research's conclusion (strategic)\nThe
  linked \"Automate onboarding creation investigation\"\n(https://app.notion.com/p/379814686151808e806dd25314b74c68)
  concludes the payoff here\nis marginal: anyone who needs a hotel immediately already
  creates it manually in ~2 min\nvia /manage/onboarding/create; the 4hr lag only affects
  hotels nobody needed urgently;\n\"time spent onboarding a hotel will not change.\"
  That conclusion was aimed at the\nwebhook approach — but it bites HARDER under the
  chosen 4-hour-sync approach, because\nthe sync gives ~0 latency improvement (still
  up to 4hr). So the ENTIRE payoff of v1 is\n\"remove the manual click,\" not latency.
  The PRD's Problem section still leads with\n\"0–4+ hours of latency\" and the Success
  Metrics still track median opp→hotel time\n(<4hr) — but the 4hr-sync design cannot
  move that needle, and that metric is trivially\nmet by construction (sync cadence
  bounds it). Recommend: explicitly re-frame the value\nprop as capacity/click-removal
  + removing the DISABLED interim-state confusion, drop or\ndemote the latency framing,
  and reconcile head-on with the investigation's skepticism so\nreviewers don't read
  the two docs and find them contradictory.\n\n### 2. Trigger condition is imprecisely
  worded throughout (precision)\nHOTEL-AUTO-001 and several spots say the trigger
  is \"when a Salesforce opportunity is\ncreated.\" Per the investigation doc the
  real condition is when an opportunity changes\nSTAGE to match the \"ready to be
  onboarded\" criteria — not creation. This matters: eng\ncould wire the gate to the
  wrong event. The JTBD already says it correctly (\"marked\nready for implementation\").
  Make the requirement language match the JTBD.\n\n### 3. \"The sync already creates
  the property row\" — half true; tighten it (correctness)\nCode check: the 4-hour
  sync (SalesforceEnterpriseDeploymentService.\nsync_accounts_and_opportunities_for_region)
  creates/updates CohortHotel + Salesforce\nmetadata rows — that's the row that shows
  on the Properties page in DISABLED limbo. It\ndoes NOT create the Hotel object today;
  that still happens via onboard_hotel_from_\nsalesforce_account(). So HOTEL-AUTO-001's
  lift is \"have the sync also call onboard_hotel_\nfrom_salesforce_account() in the
  same run.\" The rationale's phrasing (\"already creates\nthe property row\") blurs
  CohortHotel-row vs Hotel-object and undersells what's being\nadded. Confirmed onboard_hotel_from_salesforce_account()
  IS wrapped in\ntransaction.atomic() (onboarding/services/onboarding.py ~L342), so
  the doc's atomicity\nclaim holds — good.\n\n### 4. HOTEL-AUTO-004 AC#2 is blocked
  on Open Question #4 — flag the contradiction\nAC#2 (\"operator sets Account.Canary_Environment__c
  beforehand to force an env\") depends\non the field being readable BEFORE creation.
  But Open Question #4 + Rami's Slack answer\nestablish that Canary_Environment__c
  is written by Canary's SF push AFTER the hotel is\ncreated (it's a post-creation
  mirror, empty at trigger time for net-new). So AC#2 as\nwritten describes behavior
  that does not exist and is gated on an unresolved question\nabout inverting that
  dependency. For v1 the only tier that actually fires for net-new is\nthe country
  fallback (BillingAddress). Recommend: either move AC#2 out of v1 / mark it\nexplicitly
  blocked-on-OQ#4, or scope OQ#4 first. Also: I could confirm the country→region\nfallback
  exists (canary/region.py, COUNTRY_TO_CANARY_REGION) but could NOT confirm the\n\"enterprise
  brand + country overrides win first\" tier-1 logic in code — eng should verify\nthat
  tier-1 path exists before the AC assumes it.\n\n### 5. Idempotency / double-creation
  needs to be an explicit requirement (risk)\nRami's doc flagged guarding against
  the sync tripping creation twice. Since v1 IS the\nrecurring sync, every 4hr tick
  re-sees the same eligible opportunities. The design leans\non onboard_hotel_from_salesforce_account()
  being get-or-create (it creates the Hotel\n\"if one doesn't exist\"), which is probably
  sufficient — but it's load-bearing and isn't\ncalled out. Add an explicit idempotency
  requirement + a test that a second sync run over\nthe same opp is a no-op (not a
  duplicate/exception).\n\n### 6. Smaller points\n- HOTEL-AUTO-003 gate is real: can_create_new_hotels
  is a per-OnboardingType flag\n  (onboarding/models/property_configuration_processes.py);
  enterprise/cohort types are\n  False, DEFAULT is True. Gate maps cleanly. Good —
  but the \"Confirm with enterprise\n  team\" caveat appears in 3 places; it's a real
  launch blocker, surface it once in\n  Dependencies and reference it.\n- HOTEL-AUTO-005
  retry semantics (retry-next-tick vs park-and-wait) is a Must-Have with\n  undecided
  behavior (Open Q #2). Fine to defer to eng spec, but the observability\n  surface
  depends on the choice — note that dependency.\n- Product Configuration Activity
  (the proposed log surface) is event-backed\n  (onboarding/views/product_activation_events.py,
  /api/product-configuration-activity/),\n  not a standalone model — confirm an auto-trigger
  \"fire\" maps to an Event the feed\n  queries, or the events won't show up there.\n-
  Release Plan (Phase 1/2) and Feature flag are empty/TBD — needs filling before kickoff.\n-
  Success Metric \"% created without manual click ≥80%\" is the right headline metric
  and\n  actually measures the v1 payoff; promote it over the latency metric (see
  #1).\n\nNote: did NOT post anything to Notion. This review is recorded here only
  — paste/adapt\ninto a Notion comment yourself if you want it on the doc.\n"
project: null
source_id: null
tags: []
time_minutes: 5
title: review this notion design
updated: 2026-06-16 15:19:45.026162
waiting_on: null
waiting_since: null
working_on: false
---

https://app.notion.com/p/Automated-Hotel-Creation-from-Canary-Opportunity-37281468615181d68527e71ebf07a696?pvs=0