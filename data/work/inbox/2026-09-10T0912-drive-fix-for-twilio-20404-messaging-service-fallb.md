---
area: null
completed_at: null
contexts:
- react
created: 2026-09-10 09:12:48.774338
defer_until: null
due: null
energy: high
id: 2026-09-10T0912-drive-fix-for-twilio-20404-messaging-service-fallb
order: null
output: ''
project: null
source_id: https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1788942078138569?thread_ts=1788942078.138569&cid=C047K6WSUJY
tags:
- morning-gtd
- slack
time_minutes: 30
title: 'Drive fix for Twilio 20404 messaging-service fallback: 13 IHG properties with
  SMS fully dark'
updated: 2026-09-10 09:12:48.846550
waiting_on: null
waiting_since: null
working_on: false
---

Martijn flagged ~870 failed sends to ~720 IHG guests in 7 days (199 staff replies never left). I posted the investigation and proposed fix (send platform-default traffic on the main account; add 20404 to TWILIO_HIGH_SEVERITY_ERROR_CODES). Thread ends on my summary: no ticket, no owner yet.
https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1788942078138569?thread_ts=1788942078.138569&cid=C047K6WSUJY