---
area: null
contexts: []
created: &id001 2017-05-12 00:00:00
defer_until: null
due: null
energy: medium
id: 2017-05-12T0000-make-rq-jobs-requeuable-one-time
project: 2019-02-11T0000-scoping
tags: []
time_minutes: 60
title: Make RQ jobs requeuable one time
updated: *id001
waiting_on: null
waiting_since: null
---

- go through queue. For each job retry if hasn't been retried
- use created time, enqueued time as an indication of whether it has already been retried