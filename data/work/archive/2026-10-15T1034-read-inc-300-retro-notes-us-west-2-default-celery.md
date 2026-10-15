---
area: null
completed_at: 2026-10-15 13:25:12.738859
contexts:
- consume
created: 2026-10-15 10:34:12.854798
defer_until: null
due: 2026-10-15
energy: low
id: 2026-10-15T1034-read-inc-300-retro-notes-us-west-2-default-celery
order: null
output: |
  ## Agent run 2026-10-15T12:50:00

  Merged item 2026-10-14T1850-capture-follow-ups-for-incident-retro ("Capture follow ups for incident retro") into this one; the source is in data/work/trash/ if it needs recovering.

  - Title now covers both: reading the retro notes and capturing the follow-ups.
  - Body: kept the Gmail link and added the Notion incident doc link, plus both follow-ups word for word (the AWS support case ticket for James in SRE: Platform with all four stall windows, and the open question about creating another SRE ticket for the action items). Nothing was a duplicate, so nothing was dropped.
  - The merge command filled due (2026-10-15) from the source. The source had no contexts or tags to add.
  - Not carried over: the source was linked to project 2026-04-16T1210-unblock-team and sat in next/. The merge keeps this item's project (none) and bucket (inbox). Link it to that project yourself if you want it there.

  ## Agent run 2026-10-15T13:04:17

  Read the Gemini notes (https://mail.google.com/mail/?authuser=glloyd@canarytechnologies.com#all/thread-f:1879042512882535194), the Notion retro (https://app.notion.com/p/3ed81468615181ec9583dad5709db682) and its 2 open comments, and checked Linear for existing tickets. NOTHING was created in Linear. The drafts below are ready to file once you approve them.

  ### What the retro assigned
  Gemini lists 4 next steps:
  1. The group: add a pointer to the real queue visibility timeouts in the Canary repo docs.
  2. You: trim and consolidate the action items before ticketing them.
  3. James: investigate SQS FIFO empty receives and limits, and decide whether an AWS support case is needed.
  4. You: create tickets for the platform team covering the infra and queue-structure improvements. Gemini wrote "Jira S_SUR". That is almost certainly a mistranscription of SRE tickets in Linear.

  Other points from the discussion: Arihant proposed alerts at deploy time for config mismatches. The group explored splitting queues (high-priority vs long-running). James raised concerns about FIFO empty receives and throughput limits.

  ### Already done, so no tickets needed
  - Enterprise: ENT-7744 (https://linear.app/canary-technologies/issue/ENT-7744) is Done, and #58919 (https://github.com/canary-technologies-corp/canary/pull/58919) merged 2026-10-06. That covers the retry interval and the #58869 review items.
  - SRE-1445 (https://linear.app/canary-technologies/issue/SRE-1445), "SRE Agent skills for compounding Celery incidents", is Done.

  ### Existing tickets for the Platform action items
  None. I searched SRE for SQS, countdown and visibility, and looked through all SRE tickets created in the last 14 days. Only loosely related: SRE-128 (High age of oldest message, Triage) and SRE-1494 (ap celery queue age alert, Triage).

  ### Answer to "create another SRE ticket for the action items?"
  Yes, but split them rather than filing one umbrella ticket. They have different owners and different sizes, and the guard (B) is the only item that prevents a recurrence. Suggested set (all team SRE):

  **A. (James) Open an AWS support case: FIFO empty receives during the INC-300 stalls**
  > During INC-300 (2026-10-02, prod us-west-2, `canary-celery-us.fifo`), SQS returned empty receives to about 100 idle workers during four windows: 03:28–03:39, 04:10–04:23, 05:17–05:28 and 05:32–05:38 UTC. Between 11k and 145k messages were visible at the time. Our message groups are unique per task (`canary/celery/base_task.py:132-139`), so by AWS's FIFO docs a held message should block only its own group. Each stall ended when a held wave of in-flight retry copies (up to 102k, about 55k in flight by 05:25) ran and was deleted.
  > Ask AWS: (1) why receives came back empty with that many messages visible, and whether an in-flight or group limit explains it; (2) secondarily, whether calling `ChangeMessageVisibility` per message from the Celery SQS transport (to extend visibility for ETA-held messages) is supportable at our volume.
  > Done when: the case is filed with the four windows and queue ARN, AWS has answered, and the answer is recorded in the retro doc.
  > Retro: https://app.notion.com/p/3ed81468615181ec9583dad5709db682

  **B. (Platform) Reject Celery countdowns at or above the queue's visibility timeout**
  > A `BaseTask` guard that rejects any countdown or ETA at or above the target queue's SQS visibility timeout. It must read the per-queue limit from the same source canary-kubernetes uses (limits range from 120s to 900s per queue). Also fix `CELERY_TASK_MAX_COUNTDOWN = 900` in `canary/executors.py` for `process_scheduled_task` so it stops being treated as a ceiling. Fail loudly, with logging and alerting, the first time it trips at runtime. That covers Arihant's config-mismatch point. Include the repo-docs pointer to the real visibility timeouts (the retro's group action).
  > Why: this is the fifth redelivery-loop incident in five months (MSG-5949, AK-79, INFRA-558, MSG-6163, INC-300), and each was fixed locally.
  > Blocked by C.

  **C. (Platform, with the owning pods) Audit countdowns over 600s before the guard lands**
  > Move each one to a compliant interval or to a queue with a longer visibility timeout: `adyen.py` `UPDATE_PAYMENT_CHALLENGE_TIMEOUT` (780s), `antom.py` `INQUIRY_COUNTDOWN` (840s), and `executors.py` `async_scheduled_task` (up to 900s, with fresh group and dedup IDs on retry). The adyen and antom fixes probably belong in PAY tickets.

  **D. (Platform) Alert on in-flight count and redelivery rate on the default Celery queues**
  > Add an `ApproximateNumberOfMessagesNotVisible` monitor on `canary-celery-us.fifo`, `-eu` and `-ap` (normally 1–2k; it was 8.5k at 03:55 and 55k at 05:25, nearly 2h before the queue-time alert would have caught it). Add a redelivery signal too: `ApproximateReceiveCount > 1`, or bursts of `task_queue_time_seconds ≈ 600`.

  **E. (Platform, design first) Move check-in PMS sync and mobile key tasks off the default queue**
  > This was Johannes's Notion comment, and it matches the retro's discussion about splitting queues. These tasks waited up to 15 min in INC-300. Use a FIFO queue if a task needs ordering or dedup, because `canary-celery-high-priority` is not FIFO. This is a larger design item and could be a project rather than a single ticket.

  ### Owner-needed items, not SRE
  - Decide whether `link_ota_threads_to_reservation_task` should skip archived reservations in bulk resyncs. It accounted for 371k of the 454k delayed tasks. Related: SRE-1196 and #58708. This probably belongs to Messaging.
  - EMEA-704 (https://linear.app/canary-technologies/issue/EMEA-704) is still unassigned in Backlog. Note that its current title is "GDPR obfuscation search times out on portfolio scope", while the retro describes it as proposing a separate GDPR queue. Check that the retro's description is right before chasing it.

  ### Your next steps
  - Approve, edit or trim tickets A–E. I can file them in Linear (SRE team; A assigned to James Morton) once you give an explicit yes.
  - Optionally, reply to your own Notion comment "Note - ticket for James" with the ticket link once A exists.
  ## Agent run 2026-10-15T13:09:04

  Drafted tickets A, B and C in brief form, at ~/projects/plans/inc-300-sre-tickets-a-b-c.md. Nothing has been filed.
  Checked against the code, with these corrections to the retro:
  - process_scheduled_task (task_scheduler/tasks.py) takes no countdown, so it was only a victim in INC-300. The path that actually exceeds the limit is async_scheduled_task in canary/executors.py, on the high-priority standard queue (500s visibility per an old local copy of canary-kubernetes) with up to 900s. It re-queues itself, so it doubles like INC-300 did. It is a Django Q leftover and is a candidate for deletion.
  - The adyen (780s) and antom (840s) tasks are on the default 600s FIFO queue. max_retries=0 does not stop the redelivery.
  - Lead for A: AWS docs say a FIFO queue scans only the first 120k messages for available groups, and the 120k in-flight quota fails without an error (https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/quotas-fifo.html).
  - The visibility timeouts are in canary-kubernetes apps/canary/canary/values/production/<region>.yaml (visibilityTimeoutSeconds). The broker_transport_options visibility_timeout in canary/celery/celery.py has no effect on predefined queues.
  ## Agent run 2026-10-15T13:10:41

  Filed A, B and C to SRE Triage, with your approval:
  - SRE-1542 (https://linear.app/canary-technologies/issue/SRE-1542): AWS support case on the FIFO empty receives. Assigned to James Morton.
  - SRE-1541 (https://linear.app/canary-technologies/issue/SRE-1541): BaseTask guard that rejects a countdown at or above the visibility timeout. Blocked by SRE-1540.
  - SRE-1540 (https://linear.app/canary-technologies/issue/SRE-1540): fix the existing over-limit countdowns (adyen, antom, async_scheduled_task).
  Still open: D (in-flight alert), E (move check-in and mobile key tasks off the default queue), the owner-needed items, and an optional reply to your Notion comment "Note - ticket for James" linking SRE-1542.
  ## Agent run 2026-10-15T13:11:56

  DMed James Morton the three ticket links, with your approval: https://canarytechnologies.slack.com/archives/D0C66DSB7RQ/p1792059111403219
  ## Agent run 2026-10-15T13:24:42

  Checked whether EMEA-704 (https://linear.app/canary-technologies/issue/EMEA-704, which the retro calls the INC-296 ticket) shows the same redelivery bug. It does.
  - Groundcover, prod-main-us-west-2, 2026-09-25: 244 gdpr.tasks.obfuscation_plan_task tasks produced 1,322 task_failed events. That is 2 to 8 runs per task, about 5.4 on average, from 08:19 to 10:13 UTC. Nothing ran after 10:15.
  - Mechanism: each run takes the full 600s statement_timeout, which matches the default queue's 600s visibility timeout. SQS redelivered each message before the failure acked. The root cause is still the slow query; redelivery multiplied it about 5x, and that is the long-task form of the INC-300 bug.
  - EMEA-704 itself doesn't mention the redelivery. SRE-1541 covers countdowns only, not task runtime.
  - Not checked: whether each re-run also wrote another failed plan row (record_failed_plan).
project: null
source_id: https://mail.google.com/mail/?authuser=glloyd@canarytechnologies.com#all/thread-f:1879042512882535194
tags:
- morning-gtd
- gmail
time_minutes: 10
title: 'Read INC-300 retro notes and capture follow-ups: us-west-2 default celery
  queue backlog'
updated: 2026-10-15 13:25:12.738853
waiting_on: null
waiting_since: null
working_on: false
---

Gemini notes from the Oct 14 retro.
https://mail.google.com/mail/?authuser=glloyd@canarytechnologies.com#all/thread-f:1879042512882535194

Incident doc (Notion):
https://app.notion.com/p/canarytechnologies/2026-10-01-us-west-2-default-celery-queue-backlog-increasing-due-to-retries-3ed81468615181ec9583dad5709db682?source=copy_link

## Follow-ups to capture

- Ticket for James (SRE: Platform): AWS support case on the FIFO empty receives during the four stall windows (03:28–03:39, 04:10–04:23, 05:17–05:28 and 05:32–05:38 UTC): SQS returned empty receives to about 100 idle workers with 11k to 145k messages visible, which unique message groups should not allow. Secondarily, whether per-message ChangeMessageVisibility from the Celery SQS transport is supportable.
- Create another SRE ticket to ticket the action items?