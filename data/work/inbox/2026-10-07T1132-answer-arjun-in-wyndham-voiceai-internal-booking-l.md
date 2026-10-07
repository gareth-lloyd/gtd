---
area: null
completed_at: null
contexts:
- react
created: 2026-10-07 11:32:55.714000
defer_until: null
due: null
energy: medium
id: 2026-10-07T1132-answer-arjun-in-wyndham-voiceai-internal-booking-l
order: null
output: ''
project: null
source_id: https://canarytechnologies.slack.com/archives/C0AJ1ENFSSU/p1791306517953709?thread_ts=1790703003.314659&cid=C0AJ1ENFSSU
tags:
- morning-gtd
- slack
time_minutes: 15
title: 'Answer Arjun in #wyndham-voiceai-internal: booking_link_enabled flags ignored
  under USE_AGENTIC_GUEST_MESSAGING'
updated: 2026-10-07 11:32:55.816120
waiting_on: null
waiting_since: null
working_on: false
---

Arjun's FYI after my decision summary: with USE_AGENTIC_GUEST_MESSAGING on, chat.Configuration.booking_link_enabled is not respected and WebchatConfiguration.booking_link_enabled is never read, so links turn on as soon as a booking URL is set. Decide who files the cleanup ticket (ENT vs Voice). PR #59263 (remove auto-enable) merged Oct 6. Open 1 day, no reply from me.
https://canarytechnologies.slack.com/archives/C0AJ1ENFSSU/p1791306517953709?thread_ts=1790703003.314659&cid=C0AJ1ENFSSU