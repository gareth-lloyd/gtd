---
area: null
contexts: []
created: &id001 2020-01-06 00:00:00
defer_until: null
due: null
energy: medium
id: 2020-01-06T0000-read-the-code-and-understand-the-solutio
project: 2020-01-06T0000-uptime-monitoring-and-caching
tags: []
time_minutes: 15
title: Read the code and understand the solution suggested
updated: *id001
waiting_on: null
waiting_since: null
---

- The logic of the `delay` is modified:
  - Stores the time that a first value was found as well as the time that the current problem started.
  - Delay logic is only allowed to apply after the time since first value was found exceeds `delay`.