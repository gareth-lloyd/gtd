---
area: null
contexts: []
created: &id001 2020-05-28 00:00:00
defer_until: null
due: null
energy: null
id: 2020-05-28T0000-refactor-audit-with-m2m-and-update-with
project: 2020-05-28T0000-platform-pariti-io
tags: []
time_minutes: null
title: Refactor audit_with_m2m and update_with_audit
updated: *id001
waiting_on: null
waiting_since: null
---

Q1. Do we want these on the model instance, so that you can go "update with audit"?
- if no, move to audit api
- if yes, move audit_with_m2m logic to model utils.