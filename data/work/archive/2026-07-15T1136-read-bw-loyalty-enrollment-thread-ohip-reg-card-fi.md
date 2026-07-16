---
area: null
contexts:
- react
created: 2026-07-15 11:36:23.566548
defer_until: null
due: null
energy: low
id: 2026-07-15T1136-read-bw-loyalty-enrollment-thread-ohip-reg-card-fi
order: null
output: |
  ## Agent run 2026-07-15T14:10:00+03:00

  Read the full thread (8 messages, all from ~00:50–00:59 EEST 2026-07-15). Thread: https://canarytechnologies.slack.com/archives/C07BX379GQK/p1784065809347089?thread_ts=1784065809.347089&cid=C07BX379GQK

  **Issue 1 — OHIP reg card missing city/state/country (no live impact, no OHIP hotels live):**
  - Connor Swords: thinks Jason said NOT to include Opera hotels in loyalty enrollment — needs confirming.
  - Melissa Fairchild confirmed: OHIP was *intentionally excluded* because "their Opera acts weird with loyalty"; she'll dig up the official reason.
  - Resolution direction: Andrea will make the OHIP flow *not attempt* loyalty registration at all (rather than adding the fields).

  **Issue 2 — two live kiosk hotels edited post-configuration:**
  - bw-63012 (BW Plus Pembina Inn & Suites, Jonas/Manitoba CA): city AND country removed from tablet reg card — kiosk enrollments fail outright. Melissa asked Danny whether the hotel requested the removal; plan is to add fields back and email the hotel to explain (Salesforce account: https://canarytechnologies.lightning.force.com/lightning/r/Account/0015w000026HqznAAC/related/Opportunities/view). **Still open as of end of thread.**
  - bw-41096 (BW Plus Greenville South, AutoClerk/SC US): country was optional so enrollment failed when guests skipped it — Melissa already made country required again. **Fixed.**

  **Root-cause note:** IM team manages tablet-reg onboardings and likely customizes reg cards during onboarding — that's how required loyalty fields get dropped after configuration. No guardrail exists preventing removal of loyalty-required fields from reg cards.

  **No action needed from Gareth** — Andrea, Melissa, and Connor own the follow-ups (OHIP flow skip, official OHIP exclusion reason, bw-63012 field restore pending Danny/hotel confirmation). Possible watch items: whether a guardrail/validation for loyalty-required reg-card fields gets ticketed, and relation to broader BW loyalty work (cf. PMSX-419).
project: null
source_id: https://canarytechnologies.slack.com/archives/C07BX379GQK/p1784065809347089?thread_ts=1784065809.347089&cid=C07BX379GQK
tags:
- morning-gtd
- slack
- from-awareness
time_minutes: 10
title: 'Read: BW loyalty enrollment thread — OHIP reg card fields + bw-63012/bw-41096
  kiosk failures'
updated: 2026-07-15 16:25:12.929115
waiting_on: null
waiting_since: null
working_on: false
---

Andrea in #best-western: OHIP reg card missing city/state/country (no live impact); bw-63012 city+country removed (kiosk enrollments fail); bw-41096 country optional (fails when skipped — mfairchild re-required it).
https://canarytechnologies.slack.com/archives/C07BX379GQK/p1784065809347089?thread_ts=1784065809.347089&cid=C07BX379GQK