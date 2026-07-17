---
area: null
contexts:
- react
created: 2026-07-17 10:40:19.956843
defer_until: null
due: null
energy: low
id: 2026-07-17T1040-answer-bonnie-wai-in-product-questions-broadcast-m
order: null
output: |
  ## Agent run 2026-07-17T11:15:00+01:00

  Researched the codebase — answer to Bonnie's question:

  **Bonnie's memory is correct: a dedicated broadcast permission used to exist, but it was removed in Sept 2023.**

  - `Permission.MESSAGES_CAN_SEND_BROADCASTS` ("Messages - Can Send Broadcasts") was added ~Sept 1 2023 in "Chat Permission Updates" (PR #9657, canarytech_dev, commit 2db97f33548).
  - It was removed ~11 days later, Sept 12 2023, in COR-432 (PR #9755, https://github.com/canary-technologies-corp/canarytech_dev/pull/9755, commit 2845c4e887e), along with MESSAGES_CAN_MANAGE_SCHEDULED_MESSAGES and MESSAGES_CONFIGURE_PRESET_TEMPLATES. Old values survive only in permission migration snapshots.

  **Current gating (verified in code today):**
  - Sending a broadcast (`ChatBroadcastPostRequestSchema`, backend/canary/chat/views/broadcast/broadcasts.py:76) requires `MESSAGES_CAN_MESSAGE_INDIVIDUAL_GUEST`.
  - Creating group broadcasts (api_group_broadcast.py:44) and editing group broadcast details also require `MESSAGES_CAN_MESSAGE_INDIVIDUAL_GUEST`.
  - Viewing broadcasts only needs `MESSAGES_HAS_PRODUCT_ACCESS`.
  - So there is NO broadcast-specific permission today: anyone who can message individual guests can also send broadcasts. Langham cannot restrict broadcasts separately from 1:1 messaging — that would be a feature request to reintroduce a dedicated permission.

  **Drafted Slack reply (NOT posted — needs your approval):**

  > Hi Bonnie — your memory is right: there *was* a dedicated "Messages - Can Send Broadcasts" permission, but it only existed briefly (added and removed in Sept 2023, COR-432). Today there's no broadcast-specific permission: sending broadcasts (including group broadcasts) is gated by the same "Messages - Can Message Individual Guest" permission as 1:1 messaging, and viewing them just needs Messages product access. So Langham can't currently restrict broadcasts separately from regular guest messaging — anyone who can message guests can broadcast. If they need broadcast-only restriction, that would be a feature request to reintroduce the dedicated permission.

  Thread: https://canarytechnologies.slack.com/archives/C01V4NYTQRH/p1784252528595799

  Say the word and I'll post it (or post it yourself).

  ## Agent run 2026-07-17T18:00:00+01:00

  User approved — reply POSTED to the thread: https://canarytechnologies.slack.com/archives/C01V4NYTQRH/p1784277361408229?thread_ts=1784252528.595799&cid=C01V4NYTQRH
project: null
source_id: https://canarytechnologies.slack.com/archives/C01V4NYTQRH/p1784252528595799
tags:
- morning-gtd
- slack
time_minutes: 10
title: 'Answer Bonnie Wai in #product-questions: broadcast-message permission for
  Langham'
updated: 2026-07-17 12:07:13.091784
waiting_on: null
waiting_since: null
working_on: false
---

"Is there a permission related to sending broadcast messages? I thought there was before. Langham is asking" — direct @mention, saved.
https://canarytechnologies.slack.com/archives/C01V4NYTQRH/p1784252528595799