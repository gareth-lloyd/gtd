---
area: null
completed_at: 2026-11-05 16:00:59.166964
contexts:
- react
created: 2026-11-05 15:03:03.230985
defer_until: null
due: 2026-11-05
energy: high
id: 2026-11-05T1503-review-francisco-s-sdk-feature-flags-plan-and-weig
order: null
output: ''
project: null
source_id: https://canarytechnologies.slack.com/archives/C09M5GRJPL2/p1793831851859389?thread_ts=1790006579.628339&cid=C09M5GRJPL2
tags:
- morning-gtd
- slack
time_minutes: 30
title: Review Francisco's SDK feature-flags plan and weigh in on Caitlyn's 4 questions
  (#epd-mobile, Wyndham)
updated: 2026-11-05 16:00:59.166953
waiting_on: null
waiting_since: null
working_on: false
---

Francisco's plan: per-hotel SDK flags (Has Checkout SDK, Has Tipping SDK, ...) combined into an sdk_features block; and a no-app-update fix that returns 'don't show' values to SDK traffic for hotels whose SDK flag is off. He starts implementing today unless someone objects. Caitlyn asks: does it hide flows immediately, has_check_in_mobile vs has_check_in_sdk, do onboarding scripts need to set the SDK flags, and should there be a master 'SDK live' switch. Diana @'d me; I said 'I'll also take a look'.
Plan: https://app.notion.com/p/40e81468615181fcb472cb0a1d491dd0
Thread: https://canarytechnologies.slack.com/archives/C09M5GRJPL2/p1793831851859389?thread_ts=1790006579.628339&cid=C09M5GRJPL2