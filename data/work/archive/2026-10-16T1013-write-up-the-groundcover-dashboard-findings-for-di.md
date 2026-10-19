---
area: null
completed_at: 2026-10-16 13:16:53.207987
contexts:
- craft
created: 2026-10-16 10:13:46.599505
defer_until: null
due: 2026-10-16
energy: medium
id: 2026-10-16T1013-write-up-the-groundcover-dashboard-findings-for-di
order: null
output: |
  ## Agent run 2026-10-16T12:50

  Wrote the report for Diana: ~/projects/plans/wyndham-checkin-v3-groundcover-writeup-for-diana.md
  NOT sent or published anywhere. Creating a Claude Doc was blocked by the auto-mode classifier.
  Paste it into Notion or Slack yourself, or tell me to publish it as a private artifact or doc.

  Sources: the 2026-10-14 session (2d7dbcce), the ticket draft ~/projects/plans/wyndham-sdk-dropdown-422-ticket-draft.md,
  the Slack thread https://canarytechnologies.slack.com/archives/C0A4EN8SJLA/p1792076967828909?thread_ts=1792050531.422899&cid=C0A4EN8SJLA ,
  and the Groundcover monitor list.

  Contents:
  - How it was found: 8 steps, from the "Wyndham SDK Errors (SDK 1.4.1)" dashboard
    (https://app.groundcover.com/dashboards/98cab78a-3c88-4b5f-8795-6a0f8130786d) to AD-10328
    (https://linear.app/canary-technologies/issue/AD-10328). The key move was comparing failures with successes per hotel:
    0 accepted at wyndham-50930 and wyndham-53172.
  - Why no alert fired: checked live. "Step Submission 422 Rate" stayed Normal in us-west-2 for 7d because a global rate is
    diluted. "Step Submission 4xx Errors" is always alerting on 409 card declines. "Sessions but no step submissions"
    doesn't match, because the guests did submit.
  - Alerting ideas, with gcQL: (1) per-hotel "submits >= N and zero 200s"; (2) the same 422 repeated 5+ times on one session;
    (3) a backend log event when validation fails on a field that was never served (needs an A/D ticket);
    (4) split 409s out of the 4xx monitor; (5) Wyndham-scoped variants. The thresholds are untested against history.
  - Dashboard tweaks: exclude the expected session 404, and add a per-hotel success-rate table.

  Status: AD-10328 is Done (Guido Percu, High).

  Suggested Slack reply in the thread (not sent): "Hey Diana, here's the write-up: <link>. Short version: the error rate looked
  tiny (0.34%) because of 2 small hotels at 100% failure, and our monitors only alert on global rates. The alert we want is
  per hotel: 'submits are arriving and none succeed'. Happy to set it up with you."
project: null
source_id: https://canarytechnologies.slack.com/archives/C0A4EN8SJLA/p1792076967828909?thread_ts=1792050531.422899&cid=C0A4EN8SJLA
tags:
- morning-gtd
- slack
time_minutes: 45
title: Write up the Groundcover dashboard findings for Diana (how AD-10328 was found
  + alerting ideas)
updated: 2026-10-16 13:16:53.207982
waiting_on: null
waiting_since: null
working_on: false
---

I told Diana 'I can write up a report on what I did, probably tomorrow?' She asked how to add alerts so Wyndham check-in v3 issues get caught fast. Wyndham mobile app.
https://canarytechnologies.slack.com/archives/C0A4EN8SJLA/p1792076967828909?thread_ts=1792050531.422899&cid=C0A4EN8SJLA

The work for this fiding was done in a claude session this week, probably wednesday