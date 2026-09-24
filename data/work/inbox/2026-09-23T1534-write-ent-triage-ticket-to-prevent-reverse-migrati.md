---
area: null
completed_at: null
contexts: []
created: 2026-09-23 15:34:32.112630
defer_until: null
due: null
energy: low
id: 2026-09-23T1534-write-ent-triage-ticket-to-prevent-reverse-migrati
order: null
output: |
  ## Agent run 2026-09-23T17:58:14

  Draft only, not filed. Source thread: https://canarytechnologies.slack.com/archives/C0B1Y5K9AMC/p1790166847031729

  Note before filing: the plan does not flip `checkin_version` back to v2. It overwrites the reg card and check-in step config, and the v3 sync signals re-seed the live v3 flow from that. Same outcome (A/D's work wiped), different mechanism. Draft below reflects the code.

  ### Draft ticket (ENT, "Issue" template)

  **Title:** Reg-card onboarding plan must fail loudly on hotels already on check-in v3

  **Current Functionality:**
  A/D are migrating live Wyndham Connect hotels to check-in v3 and are still monitoring. ENT onboarding scripts are not v3-aware yet. Re-running the Wyndham process on a v3 hotel overwrites the check-in reg card with the default template and rewrites the ID / additional-guest step config; the v3 sync signals then re-seed the live flow from that. No error, run reports success, A/D's v3 changes are lost.

  **Expected Functionality:**
  `AddRegistrationCardPlan` (or `WyndhamRegistrationCardProvider.perform_hotel_configuration`) checks `hotel.check_in_configuration.checkin_version` and raises an expected onboarding error when it is v3, before any write. Add a test for the v3 case.

  Related: AD-8074 https://linear.app/canary-technologies/issue/AD-8074, AD-8324 https://linear.app/canary-technologies/issue/AD-8324
  Slack: https://canarytechnologies.slack.com/archives/C0B1Y5K9AMC/p1790166847031729

  Priority: Medium.
  ## Agent run 2026-09-23T17:58:45

  Filed on user approval: ENT-7607 (https://linear.app/canary-technologies/issue/ENT-7607/reg-card-onboarding-plan-must-fail-loudly-on-hotels-already-on-check), Backlog, Medium, related to AD-8074 and AD-8324, Slack thread attached. No Slack reply posted.
project: null
source_id: null
tags: []
time_minutes: 5
title: Write ENT triage ticket to prevent reverse migration to check in v2
updated: 2026-09-23 17:58:45.598956
waiting_on: null
waiting_since: null
working_on: false
---

https://canarytechnologies.slack.com/archives/C0B1Y5K9AMC/p1790166847031729

Review thread, draft ticket