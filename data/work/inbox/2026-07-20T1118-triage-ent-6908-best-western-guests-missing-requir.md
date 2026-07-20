---
area: null
contexts:
- react
created: 2026-07-20 11:18:41.388575
defer_until: null
due: null
energy: medium
id: 2026-07-20T1118-triage-ent-6908-best-western-guests-missing-requir
order: null
output: ''
project: null
source_id: https://linear.app/canary-technologies/issue/ENT-6908/groundcover-best-western-missing-required-address-fields-production-us
tags:
- morning-gtd
- linear
time_minutes: 20
title: 'Triage ENT-6908: Best Western guests missing required address fields'
updated: 2026-07-20 11:18:41.463838
waiting_on: null
waiting_since: null
working_on: false
---

Guests missing city/country block BW enrollment (us-west-2), unassigned since Friday. Almost certainly the same root cause Andrea raised in #best-western: bw-63012 had city AND country removed, bw-41096 made country optional. Link the two.
https://linear.app/canary-technologies/issue/ENT-6908/groundcover-best-western-missing-required-address-fields-production-us