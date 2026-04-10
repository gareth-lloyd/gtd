---
area: null
contexts: []
created: &id001 2025-03-13 00:00:00
defer_until: null
due: null
energy: null
id: 2025-03-13T0000-check-in-retries
project: null
tags: []
time_minutes: null
title: Check-in retries
updated: *id001
waiting_on: null
waiting_since: null
---

hypothesis: race condition
Needs locking

* Check cached token before operating
* Reproduce error if you get a chance
* Otherwise, run once, then run slowly