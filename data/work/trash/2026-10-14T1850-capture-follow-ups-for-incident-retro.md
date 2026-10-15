---
area: null
completed_at: null
contexts: []
created: 2026-10-14 18:50:38.562084
defer_until: null
due: 2026-10-15
energy: low
id: 2026-10-14T1850-capture-follow-ups-for-incident-retro
order: null
output: ''
project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 5
title: Capture follow ups for incident retro
updated: 2026-10-15 12:49:35.593986
waiting_on: null
waiting_since: null
working_on: false
---

ticket for James SRE: Platform: AWS support case on the FIFO empty receives during the four stall windows (03:28–03:39, 04:10–04:23, 05:17–05:28 and 05:32–05:38 UTC): SQS returned empty receives to about 100 idle workers with 11k to 145k messages visible, which unique message groups should not allow. Secondarily, whether per-message ChangeMessageVisibility from the Celery SQS transport is supportable.

Create another SRE ticket to ticket the action items?

https://app.notion.com/p/canarytechnologies/2026-10-01-us-west-2-default-celery-queue-backlog-increasing-due-to-retries-3ed81468615181ec9583dad5709db682?source=copy_link