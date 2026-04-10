---
area: null
contexts: []
created: &id001 2019-11-13 00:00:00
defer_until: null
due: null
energy: null
id: 2019-11-13T0000-time-out-connection-attempts
project: null
tags: []
time_minutes: null
title: Time out connection attempts
updated: *id001
waiting_on: null
waiting_since: null
---

1. Come up with well defined, reproducible steps.

- new connection attempt means cancel any existing time out
- If not connected in x amount of time, move to disconnected, display error. 

- Remove added dsiconnect logic in component