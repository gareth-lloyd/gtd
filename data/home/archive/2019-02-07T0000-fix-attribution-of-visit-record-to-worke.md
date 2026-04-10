---
area: null
contexts: []
created: &id001 2019-02-07 00:00:00
defer_until: null
due: null
energy: null
id: 2019-02-07T0000-fix-attribution-of-visit-record-to-worke
project: null
tags: []
time_minutes: null
title: Fix attribution of visit record to worker when already skipped
updated: *id001
waiting_on: null
waiting_since: null
---

- The VR is being unassigned during absence period actioning
- The worker is gone by the time we look for it.

- Solution - do as you're currently doing, but exclude the unassign event.