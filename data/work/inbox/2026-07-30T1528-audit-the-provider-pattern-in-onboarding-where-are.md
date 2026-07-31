---
area: null
contexts: []
created: 2026-07-30 15:28:02.557778
defer_until: null
due: null
energy: low
id: 2026-07-30T1528-audit-the-provider-pattern-in-onboarding-where-are
order: null
output: ''
project: null
source_id: null
tags: []
time_minutes: 5
title: Audit the plan / provider pattern in onboarding. Where are we violating? What's
  the implication?
updated: 2026-07-31 12:49:55.678625
waiting_on: null
waiting_since: null
working_on: true
---

Known violation example:
* EnableMSAProducts plan is a shall which depends entirely on calling provider.configure_hotel
* Most plans should have the bulk of their operations in `execute`, and configure_hotel should only have special cases.