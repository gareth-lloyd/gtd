---
area: null
contexts:
- thinking
created: 2026-04-21 09:27:25.596450
defer_until: null
due: null
energy: high
id: 2026-04-21T0927-triage-ent-5989-wyndham-cut-parent-ties-auto-batch
order: null
project: null
source_id: null
tags:
- morning-gtd
- linear
time_minutes: 90
title: 'Triage ENT-5989: Wyndham cut-parent-ties auto-batch blocks subsequent full-cut
  + state drift'
updated: 2026-04-27 10:13:58.961377
waiting_on: null
waiting_since: null
---

lmena created this after my cc on ENT-5978. Two bugs in the Wyndham deactivation flow: (1) auto-batch removes hotel from WYNDHAM portfolio, which permanently blocks the later manual full-cut batch via a guard in WyndhamRemoveHotelFromParentBrandProvider; (2) on hotel 7568 the brand+has_chat fields drifted back to Wyndham between 4/3 and 4/20 despite a completed cut. Likely affects other terminated Wyndham sites. https://linear.app/canary-technologies/issue/ENT-5989/wyndham-cut-parent-ties-flow-auto-batch-blocks-subsequent-full-cut