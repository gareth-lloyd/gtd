---
area: null
completed_at: 2026-09-09 11:48:45.898467
contexts: []
created: 2026-09-09 11:22:42.311670
defer_until: null
due: null
energy: low
id: 2026-09-09T1122-debug-in-shell
order: null
output: ''
project: null
source_id: null
tags: []
time_minutes: 5
title: debug in shell
updated: 2026-09-09 11:48:45.898458
waiting_on: null
waiting_since: null
working_on: false
---

Twilio Messaging Service SID MG73e3b390bb… is provisioned across 47 hotels that each have a distinct Twilio subaccount, so sends fail with 20404 — a Messaging Service resolves only within its owning account. For the 13 affected IHG properties that is ~870 failed sends to ~720 guests over the last 7 days, of which 199 were staff-typed inbox replies; the error logs at warning and does not alert.