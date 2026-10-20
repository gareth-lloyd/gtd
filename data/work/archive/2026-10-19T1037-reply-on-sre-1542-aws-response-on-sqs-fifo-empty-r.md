---
area: null
completed_at: 2026-10-19 12:47:21.792323
contexts:
- react
created: 2026-10-19 10:37:05.746705
defer_until: null
due: null
energy: low
id: 2026-10-19T1037-reply-on-sre-1542-aws-response-on-sqs-fifo-empty-r
order: null
output: ''
project: null
source_id: https://linear.app/canary-technologies/issue/SRE-1542/open-an-aws-support-case-on-sqs-fifo-empty-receives-during-inc-300#comment-4c83bc25
tags:
- morning-gtd
- linear
time_minutes: 10
title: 'Reply on SRE-1542: AWS response on SQS FIFO empty receives (INC-300)'
updated: 2026-10-19 12:47:21.792308
waiting_on: null
waiting_since: null
working_on: false
---

James posted AWS's answer: the empty receives came from held messages in the same message group, not from the queue withholding readable messages. State: In Review.
https://linear.app/canary-technologies/issue/SRE-1542/open-an-aws-support-case-on-sqs-fifo-empty-receives-during-inc-300