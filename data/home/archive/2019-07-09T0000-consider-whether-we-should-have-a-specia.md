---
area: null
contexts: []
created: &id001 2019-07-09 00:00:00
defer_until: null
due: null
energy: null
id: 2019-07-09T0000-consider-whether-we-should-have-a-specia
project: 2019-07-16T0000-ch-comms-rollout
tags: []
time_minutes: null
title: Consider whether we should have a special "disabled" value for token, and return
  a never resolving promise.
updated: *id001
waiting_on: null
waiting_since: null
---

- create a new Promise which does not call resolve
- return this so it's set as clientPromise
- Set a timeout to reset and try again?