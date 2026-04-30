---
area: null
contexts:
- computer
created: 2026-04-28 10:54:36.123520
defer_until: null
due: null
energy: medium
id: 2026-04-28T1054-reply-to-marta-in-wyndham-dual-collateral-still-fa
order: null
project: 2026-04-10T0840-people
source_id: https://canarytechnologies.slack.com/archives/C04STT7UPRQ/p1776779279913179#refresh-2026-04-28
tags:
- morning-gtd
- slack
time_minutes: 30
title: 'Reply to Marta in #wyndham: dual collateral still failing post go-live'
updated: 2026-04-30 10:27:16.174043
waiting_on: null
waiting_since: null
---

Marta says properties are still flagging dual collateral not enabled after go-live. She wants a root cause (scripting issue vs setup) so escalations stop. Pair or scope a quick investigation.

Deep-dive findings — root cause already identified upstream:
- The slack message links ENT-5977, which is in trash, but the actual driver ticket is ORDER-2156 ("Acrylic Collateral Designs needed - Registry Collection"), assigned to Jessica Riccardi on the Tipping Orders team. Status: Done.
- Root cause per ORDER-2156: "no acrylic collateral designs for the Registry Collection brand. If/when they are added, the acrylic will be visible." This is NOT a scripting bug — it's missing brand assets.
- Original example: The Monarch Hotel, HQ Collection New Orleans (hotel/129279527, wyndham-61090), only paper visible.
- Action: reply to Marta in #wyndham pointing her at ORDER-2156 — it's a design-asset issue per Wyndham brand, owned by Tipping Orders team, not Enterprise scripting. Loop in Jessica if the request is to enable other Registry Collection / soft-brand properties.

Slack: https://canarytechnologies.slack.com/archives/C04STT7UPRQ/p1776779279913179
Driver: https://linear.app/canary-technologies/issue/ORDER-2156/acrylic-collateral-designs-needed-registry-collection