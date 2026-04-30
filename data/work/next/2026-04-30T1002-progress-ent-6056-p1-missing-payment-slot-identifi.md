---
area: null
contexts:
- deep
created: 2026-04-30 10:02:08.693226
defer_until: null
due: null
energy: high
id: 2026-04-30T1002-progress-ent-6056-p1-missing-payment-slot-identifi
order: 1
project: 2026-04-10T0840-ticket
source_id: https://linear.app/canary-technologies/issue/ENT-6056/p1-auth-form-cc-posting-fails-on-428-hotels-missing-payment-slot
tags:
- morning-gtd
- linear
time_minutes: 90
title: 'Progress ENT-6056: P1 missing payment slot identifier (417 hotels)'
updated: 2026-04-30 10:58:12.424117
waiting_on: null
waiting_since: null
---

P1 newly assigned. dthomson posted hotel list (417 hotels, 12,366 failures/7d) sorted by failure count: https://docs.google.com/spreadsheets/d/1LNo1NBe9ztm2PkfQjgrOqPsgyio_mvU3oAnBrxlg6Ms

dthomson @s me with proposal: most affected hotels have 'Check In - Pms payment slot identifier' filled but not 'PMS Integration - Pms payment slot identifier auths'. Suggests scripting the copy from check-in slot to PMS Integration slot, then surfacing the remaining few. Wyndham recommended value is 3.

https://linear.app/canary-technologies/issue/ENT-6056
Thread: https://canarytechnologies.slack.com/archives/C04STT7UPRQ/p1777501210457089?thread_ts=1777497151.022479&cid=C04STT7UPRQ