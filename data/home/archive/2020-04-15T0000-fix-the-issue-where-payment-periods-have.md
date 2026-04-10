---
area: null
contexts: []
created: &id001 2020-04-15 00:00:00
defer_until: null
due: null
energy: high
id: 2020-04-15T0000-fix-the-issue-where-payment-periods-have
project: 2020-04-17T0000-housekeep
tags: []
time_minutes: 60
title: Fix the issue where payment periods have relevant changes but are not brought
  forward.
updated: *id001
waiting_on: null
waiting_since: null
---

- Trace through the code and figure out scenarios for different pps
https://housekeep.com/hkadmin/workers/10385/#payments
https://housekeep.com/hkadmin/events/dgzgjp07mjz9/
- fix the method with GOOD tests.