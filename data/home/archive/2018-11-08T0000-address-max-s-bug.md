---
area: null
contexts: []
created: &id001 2018-11-08 00:00:00
defer_until: null
due: null
energy: medium
id: 2018-11-08T0000-address-max-s-bug
project: 2019-01-21T0000-red-flag
tags: []
time_minutes: 30
title: address Max's bug
updated: *id001
waiting_on: null
waiting_since: null
---

Create a failing test
- There is a job that a worker can do, but can't do first visit
- During a holiday response, the job gets auto-reassigned
- It should not go to that worker if they can't do first visit