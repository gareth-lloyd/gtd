---
area: null
contexts: []
created: &id001 2019-02-07 00:00:00
defer_until: null
due: null
energy: null
id: 2019-02-07T0000-scope-the-story-to-allow-ops-to-override
project: 2019-02-11T0000-reliability
tags: []
time_minutes: null
title: Scope the story to allow ops to override notice categories
updated: *id001
waiting_on: null
waiting_since: null
---

- Process AbsencePeriod up front, AbsencePeriodEffects in background
  - effects up front
  - comms happen in background
- transaction around absence period processing so we don't get half finished ones.
-