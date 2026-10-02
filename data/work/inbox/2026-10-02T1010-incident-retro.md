---
area: null
completed_at: null
contexts:
- react
created: 2026-10-02 10:10:28.661209
defer_until: null
due: null
energy: low
id: 2026-10-02T1010-incident-retro
order: null
output: |-
  ## Agent run 2026-10-02T12:28:00+03:00

  Merged item `2026-10-02T1112-check-the-retrospective-for-incident-300-us-west-2`
  ("Check the retrospective for incident #300 (us-west-2 default celery queue backlog)")
  into this one. The other item is now in `trash/` under that id and can be recovered from there.

  - **Title**: kept this item's "Review incident … and plan retro" shape, added the other item's
    specifics (incident #300, us-west-2 default celery queue backlog).
  - **Body**: folded in the other item's full incident summary (opened 08:01 EEST Oct 2, IC shift 2,
    ~40k backlog from retries, Messaging / Mobile Key / Check-in affected, James Morton's hotfix
    #58869, Rootly postmortem + pin-messages ping, related INC-296) and its Rootly Gmail thread link.
    Both items' asks are kept as two bullets (check the retrospective/postmortem; plan the retro).
  - **De-duplicated**: the Slack channel link `C0C64K0SMFY` appeared in both bodies — kept once.
    The link labels ("Incident Slack channel", "Slack message", "Rootly email thread") are mine,
    inferred from context.
  - **Fields (applied by `merge_items`)**: contexts now `[react]`, tags `[morning-gtd, gmail]`
    (both from the other item). `energy: low` matched. `time_minutes` stays 5 — the other item's
    estimate was 10, not carried because the target already had a value. The other item's
    `source_id` (the Gmail thread URL) is not carried as a field, but the same URL is in the body.

  ## Agent run 2026-10-02T12:31:00+03:00

  **Bottom line.** INC-300 is resolved and the fix is holding. James Morton has already drafted most of the retrospective in Notion, so the retro is mainly about three things that draft does not cover: code review flagged this exact failure and the fix for the flag was still wrong; this is the second HIGH incident in a week with the same 600s-redelivery mechanism; and the incident was declared ~30 min after the cause was known. No retro meeting is on your calendar yet, and no follow-up tickets or PRs exist that I could find.

  ### Where things stand
  - Incident: INC-300, HIGH, us-west-2. Channel https://canarytechnologies.slack.com/archives/C0C64K0SMFY, Rootly https://rootly.com/account/incidents/300-us-west-2-default-celery-queue-backlog-increasing-due-to-retries. You were paged as Incident Commander at 05:01Z (08:01 EEST); Ashish Yadav was on-call engineer; James Morton found the cause, wrote the hotfix, and resolved and closed it at 05:47-05:48Z.
  - Retro doc (Rootly-generated, with a full "AI-Assisted Retrospective" section already written): https://app.notion.com/p/3ed81468615181ec9583dad5709db682. The template sections above it (Root causes / 5-whys, Mitigation, Lessons learnt, Action Items) are still empty.
  - Cause PR: #58293 (https://github.com/canary-technologies-corp/canary/pull/58293), Martin "Tincho" Rodriguez, approved by Andrés Figueira, merged 10-01 15:02Z, ticket ENT-6535 (https://linear.app/canary-technologies/issue/ENT-6535).
  - Fix PR: #58869 (https://github.com/canary-technologies-corp/canary/pull/58869), James Morton, approved by Elena Browne, merged 05:19Z, live ~05:34Z.
  - Original alert thread: https://canarytechnologies.slack.com/archives/C090ST96FK7/p1790912786887429
  - Z asked Tincho to look when back online (https://canarytechnologies.slack.com/archives/C0C64K0SMFY/p1790919332128929); no reply from Tincho in the channel yet.

  ### What happened (short)
  The new Best Western retry task reschedules itself with `countdown=900`. On our SQS transport the worker holds a countdown message unacked, and the default queue's visibility timeout is 600s, so SQS handed each held message to a second worker. Both copies ran and each scheduled the next attempt, so one check-in's chain doubled every 15 min from 23:53Z. Per the retro doc: default-queue work stalled four times (03:28-03:39, 04:10-04:23, 05:17-05:28, 05:32-05:38Z, ~43 min total), median wait peaked at 11-15 min, nothing reached the DLQ, and 95,745 duplicate copies were dropped once the fix was live. Delayed work: check-in PMS sync, mobile key activation, OTA thread linking, message eligibility, check-in emails.

  ### What the existing retro draft misses
  1. **Review flagged it, and the fix for the flag was wrong.** On 09-29 the Macroscope bot left a [blocking] comment on #58293 saying the countdowns exceed the SQS visibility timeout and the message would be redelivered. It quoted 120s (the stale value in `backend/canary/canary/celery/celery.py:129`) rather than the real 600s. The author changed +1h/+8h to 15-minute hops and replied "No countdown now exceeds `CELERY_TASK_MAX_COUNTDOWN` ... nothing is redelivered ahead of its ETA". 900s is still over 600s. The human review commented only on the monitor log line. This is the most useful retro topic, and it is a systems question, not a personal one: the repo itself teaches the wrong model.
  2. **The real visibility timeout is not discoverable from the code.** `celery.py:128-129` sets `visibility_timeout: 120` under a comment saying to ignore the line and check AWS. `canary/executors.py:19` has `CELERY_TASK_MAX_COUNTDOWN = 900  # 15 minutes` and a docstring about "the 15 minute limit of SQS". Anyone reading those would conclude 900s is safe.
  3. **Second incident in a week on the same mechanism.** INC-296 on 09-25 (https://canarytechnologies.slack.com/archives/C0C4JLVEFN0, retro https://app.notion.com/p/3e681468615181569879dc09cbf53675) was also 600s visibility timeout plus late ack redelivering default-queue tasks. Daga's summary (https://canarytechnologies.slack.com/archives/C0C4JLVEFN0/p1790331843541199) recommended a Celery-level fix and warned "any other task ... can loop the same way today". I did not find evidence that follow-up was ticketed or done.
  4. **Other countdowns over 600s exist on master.** `UPDATE_PAYMENT_CHALLENGE_TIMEOUT = 60 * 13` (780s, `payment_gateways/services/adyen.py:109`), `INQUIRY_COUNTDOWN = 14 * 60` (840s, `payment_gateways/services/antom.py:79`), and the scheduled-task executor up to 900s (`canary/executors.py:91,160`), which also re-queues with fresh group/dedup ids. I have not checked which queue each runs on or whether a duplicate delivery is harmful there; for payment status tasks a double run is worth a look. The draft's action item 1 covers the executor but not Adyen/Antom.
  5. **Late declaration.** Alert 03:46Z; first SRE Agent pass at 03:51Z said "nothing's broken now" and the alert was resolved from Slack at 03:55Z; James raised the retry theory at 04:32Z and the agent confirmed at 04:35Z; hotfix PR opened 04:36Z and approved 04:41Z; incident declared 05:01Z. So the IC and wider team were paged ~30 min after the cause was known, with the fix already approved. The Incident Response page (https://app.notion.com/p/1498b9c69fa9437dbc8ef5403b43163d) asks for a low barrier to declaring.
  6. **Approval to live took ~53 min** (approved 04:41Z, merged 05:19Z, live ~05:34Z), with two more stalls in that window. CI was the first test run because James had no working local venv. The new self-rescheduling task shipped with no flag or kill switch, so a code deploy was the only lever.
  7. **Record accuracy.** Rootly shows Started 05:01Z and "resolved in 47 mins", but impact began 03:28Z and the chain at 23:53Z. The draft timeline says "04:20 Root cause found" while Slack shows 04:32-04:35Z. #58293's description still says +1m/+1h/+8h while the code does 33 attempts at 15 min. The incident is already Closed in Rootly, which the process doc says happens after the retro.
  8. **Customer impact is unquantified**, and EU/AP were never confirmed clean (the SRE Agent noted they got the same release).

  ### Retro plan
  - **When:** Monday 2026-10-05. The Security Engineering retro template says within 72 hours of resolution, which lands 05:47Z Monday (I saw this in a search excerpt only, not the full page: https://app.notion.com/p/35181468615181bf8111f6959fb36df2). 45 minutes. I have not checked attendee calendars or time zones.
  - **Who:** James Morton (fix, retro author), Tincho (author of #58293), Andrés Figueira (reviewer), Ashish Yadav (on-call), Elena Browne (triaged alert, approved hotfix), Z, Daga (INC-296 Celery follow-up), plus whoever in Platform owns the Celery/SQS config. You facilitate as IC.
  - **Pre-work to ask for:** James moves the AI draft into the template sections and corrects the start time; Tincho reads the draft and adds their view of the review thread; someone from Platform confirms EU/AP and the status of the INC-296 Celery follow-up.
  - **Agenda:**
    1. Timeline and impact, confirm and correct (5 min). Real start, number of hotels/guests delayed, EU/AP.
    2. How it got through review (10 min). The Macroscope comment, the 120 vs 600 vs 900 confusion, tests that mock the scheduler. Keep it blameless: what would have let the author or reviewer see the real number.
    3. The systemic cause and the repeat of INC-296 (15 min). Countdown vs visibility timeout, why the earlier follow-up did not land, the other >600s countdowns.
    4. Detection and response (10 min). Four hours from chain start to alert, the "nothing's broken" first pass, declaring late, approval-to-live time, no kill switch.
    5. Action items with an owner and a Linear ticket each (5 min).
  - **Action items to propose** (the first five are from the draft; none has an owner or ticket yet):
    1. Keep countdowns under the visibility timeout; add a `BaseTask` guard that rejects a countdown at or above it; fix `CELERY_TASK_MAX_COUNTDOWN`.
    2. Alert on `ApproximateNumberOfMessagesNotVisible` for the us/eu/ap default queues.
    3. AWS support case on the FIFO empty receives during the four stalls.
    4. Finish the two review items deferred on #58869 (Redis error treated as duplicate; claim left set after a hard worker kill).
    5. Skip OTA thread linking for archived reservations in bulk resyncs.
    6. New: make the real visibility timeout one named constant in code and remove the misleading `120` line and "15 minute limit of SQS" comments.
    7. New: audit the Adyen (780s) and Antom (840s) countdowns for duplicate delivery.
    8. New: confirm status of the INC-296 Celery follow-up and ticket it if missing.
    9. New: require a flag or kill switch on new self-rescheduling tasks on the default queue.
    10. New: add in-flight (NotVisible) trend and fastest-growing task to the SRE Agent's first pass and the alert runbook (https://www.notion.so/canarytechnologies/Canary-Celery-Monitors-1f981468615180909393fb3f2c1655ed).
    11. New: correct the Rootly start time and the #58293 description.

  ### Draft message (NOT sent; for the incident channel C0C64K0SMFY if you want it)
  > Thanks again all for the fast fix last night. I'd like to hold a 45-min retro on Monday. James, thank you for the write-up in the retro doc (https://app.notion.com/p/3ed81468615181ec9583dad5709db682); could you move it into the template sections and set the real start time (first stall 03:28Z)? Tincho and Andrés, please read it beforehand and add anything on the review thread for #58293, since the bot did flag the visibility timeout and I want to understand why the numbers in our code pointed the wrong way. I'd also like someone from Platform to confirm EU/AP were clean and where the Celery follow-up from last week's INC-296 landed. I'll send an invite.

  ### Not verified
  - Whether EU/AP had retry chains, and the number of hotels or guests affected. I ran no Groundcover queries; figures above come from the Slack threads, #58869 and the Notion draft.
  - Whether action-item tickets exist in Linear. I checked ENT-6535 and GitHub PRs mentioning it only.
  - Queue routing and duplicate-run safety of the Adyen, Antom and scheduled-task countdowns.
  - Attendee time zones and availability.
  - Nothing was posted, edited or scheduled anywhere; all access was read-only.
project: null
source_id: null
tags:
- morning-gtd
- gmail
time_minutes: 5
title: 'Review incident #300 (us-west-2 default celery queue backlog) and plan retro'
updated: 2026-10-02 12:31:00.000000
waiting_on: null
waiting_since: null
working_on: false
---

HIGH incident #300 (us-west-2 default celery queue backlog) opened 08:01 EEST Oct 2 while you are on IC shift 2; backlog ~40k from retries, affected Messaging, Mobile Key, Check-in. James Morton resolved it in 47 min with hotfix #58869 (throttle retries). Rootly says a postmortem is being drafted and pinged you to pin messages for the retro. Related: INC-296.

- Check the retrospective / postmortem for the incident
- Plan the retro

Links:

- Incident Slack channel: https://canarytechnologies.slack.com/archives/C0C64K0SMFY
- Slack message: https://canarytechnologies.slack.com/archives/C090ST96FK7/p1790912786887429
- Rootly email thread: https://mail.google.com/mail/?authuser=glloyd@canarytechnologies.com#all/thread-f:1877912896407802150