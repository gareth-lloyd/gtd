---
area: null
completed_at: 2026-10-08 12:23:41.656964
contexts:
- react
created: 2026-10-07 11:32:55.928791
defer_until: null
due: 2026-10-07
energy: medium
id: 2026-10-07T1132-host-and-close-out-the-retro-for-the-2026-10-01-us
order: null
output: |
  ## Agent run 2026-10-07T12:21:36

  Merged item `2026-10-06T0715-complete-retrospective-steps-for-incident-300-us-w` ("Schedule retro for incident; share retro doc", was in next/, now in trash/) into this item via `manage.py merge_items`.

  Folded in from the other item:
  - The full list of 4 Rootly retro steps (Gather & Confirm Data, Write the Retrospective Document, Host Retrospective Meeting, Share the Finalized Retrospective) and their deadline: 24h from 2026-10-05 18:00 EEST, i.e. 2026-10-06 18:00 EEST.
  - Slack link where Martin shared the retro draft (C0B1MN8F869/p1791219717995609).
  - The fix: PR #58919 (BW reservation-link retry).
  - Rootly incident 300 retrospective-tab link.
  - The other item's source Slack link (D08DWAQ4L5A/p1791212412205319).
  - `due: 2026-10-06` (this item had no due; filled from the other item by the merge command). Already past, so worth reviewing.

  De-duplicated: both bodies named Martin's retro draft and the Host/Share Rootly steps; merged into single mentions. Kept this item's title (verb-first, more specific). Contexts and tags were identical on both (react; morning-gtd, slack). `time_minutes` stayed 30 (this item's value; the other had 45).

  Recover the trashed item from data/work/trash/ if anything is missing.
project: 2026-04-16T1210-unblock-team
source_id: https://canarytechnologies.slack.com/archives/D08DWAQ4L5A/p1791298808631049
tags:
- morning-gtd
- slack
time_minutes: 30
title: Host and close out the retro for the 2026-10-01 us-west-2 celery queue backlog
  incident
updated: 2026-10-08 12:23:41.656938
waiting_on: null
waiting_since: null
working_on: false
---

I'm incident commander shift 2 this rotation. Rootly assigned me 4 retro steps for incident 300 (Gather & Confirm Data, Write the Retrospective Document, Host Retrospective Meeting, Share the Finalized Retrospective), all due 24h from 2026-10-05 18:00 EEST, i.e. 2026-10-06 18:00 EEST. The Host Retrospective Meeting and Share the Finalized Retrospective steps have pinged daily since Oct 5.

Martin Rodriguez drafted the retro doc: https://app.notion.com/p/canarytechnologies/2026-10-01-us-west-2-default-celery-queue-backlog-increasing-due-to-retries-3ed81468615181ec9583dad5709db682 (draft shared in Slack: https://canarytechnologies.slack.com/archives/C0B1MN8F869/p1791219717995609 ). The fix is PR #58919 (BW reservation-link retry). At handoff I noted "quite a few follow-ups to discuss on retro".

Links:
- Rootly retrospective tab: https://rootly.com/account/incidents/300-us-west-2-default-celery-queue-backlog-increasing-due-to-retries?tab=retrospective
- https://canarytechnologies.slack.com/archives/D08DWAQ4L5A/p1791298808631049
- https://canarytechnologies.slack.com/archives/D08DWAQ4L5A/p1791212412205319