---
area: null
completed_at: 2026-11-04 13:54:29.279115
contexts:
- deep
created: 2026-11-04 10:35:52.670279
defer_until: null
due: null
energy: high
id: 2026-11-04T1035-draft-engineering-design-gate-mobile-sdk-features
order: null
output: ''
project: null
source_id: https://canarytechnologies.slack.com/archives/C09M5GRJPL2/p1793710013611679?thread_ts=1790006579.628339&cid=C09M5GRJPL2
tags:
- morning-gtd
- slack
time_minutes: 60
title: 'Draft engineering design: gate mobile SDK features independently of dashboard
  flags (Wyndham not-live sites can use checkout)'
updated: 2026-11-04 13:54:29.279106
waiting_on: null
waiting_since: null
working_on: false
---

Missed yesterday: my #epd-mobile question got answered. Wyndham sites that are enabled-but-not-live expose checkout/messaging/tipping in the app because the SDK keys off has_* flags only; web has a second guest-facing step. Ani: must be independent for all enterprise; Connor: fast-track; Wyndham does NOT force-update, so old app versions stay broken. Caitlyn asked Diana for workarounds and asked Ani whether to shut off checkout. I said this needs a brief engineering design.
https://canarytechnologies.slack.com/archives/C09M5GRJPL2/p1793710013611679?thread_ts=1790006579.628339&cid=C09M5GRJPL2