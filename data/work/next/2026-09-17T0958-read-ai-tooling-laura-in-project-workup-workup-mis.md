---
area: null
completed_at: null
contexts:
- consume
created: 2026-09-17 09:58:14.685749
defer_until: null
due: 2026-09-17
energy: low
id: 2026-09-17T0958-read-ai-tooling-laura-in-project-workup-workup-mis
order: null
output: |
  ## Agent run 2026-09-17T10:54

  Read Laura's post in #project-workup (https://canarytechnologies.slack.com/archives/C0AL1T2H43V/p1789616637872589). No replies as of 10:53 on 2026-09-17; Blake has not answered. It is addressed to Blake, not to you. Nothing is asked of you.

  **Numbers (since 2026-08-26)**
  - 25 Workup-investigated tickets were later closed as duplicates by a human. Workup flagged 7 and missed 18.
  - Of the 18 misses, 14 had a target that already existed when Workup ran. In 10 of those 14, Workup's own comment named the target. 5 of the 25 had targets created after the investigation, so they were unfindable.
  - Three comments say the target is "over 7 days old so it doesn't meet the pipeline's strict auto-duplicate bar", then declare Code fix. The rule fires only for same hotel + two matching identifiers + target under 7 days old.
  - MSG-3862 (50 Zendesk tickets attached) was missed four times in one week for that reason.
  - Two duplicate declarations named the ticket itself (self-reference bug).

  So the main failure is the rule, not search. Workup mostly finds the target and then talks itself out of calling it. Her Notion page tested the "can't find it because it never searches by symptom" theory and found it explains only part of the misses.

  **Her proposal**
  1. Keep duplicates in the next-step denominator; exclude only the 5 whose target was created after the investigation.
  2. Drop the 7-day window. Let a symptom-matched open target count, guarded against self-references and closed targets.
  3. Add symptom search to the Linear gatherer for the few targets it did not find.

  **Open questions to Blake**
  - What would justify auto-close instead of label-only? She floats a precision number from a few weeks in shadow mode, or same-hotel cases only at first. Every correct call so far was the same hotel re-filing within days (SDM-5043, MSG-6203, MSG-5602, CC-3227, PMS-10250).
  - Do feature-request duplicates stay in? Her view: "This is MSG-2073" beats "feature request", and Workup usually already knows it.

  **Not verified**
  - Full table (https://app.notion.com/p/3de8146861518193bb5bdf78c2488924) returned 404 to the Notion MCP integration, so the per-ticket breakdown is unread. Figures above are from the Slack post and its Notion preview only.
  - The post follows a meeting on the morning of 2026-09-16 that I did not look up.

  **If you want to weigh in (optional, nothing drafted or sent)**
  - Dropping the 7-day window looks right for long-lived umbrella tickets like MSG-3862, where age is the opposite of a disqualifier.
  - Dropping it removes the only guard that kept precision high. "Symptom-matched" is a looser test than two matching identifiers, so shadow-mode precision should be measured separately for same-hotel and cross-hotel matches before any auto-close.
project: 2026-09-08-workup
source_id: https://canarytechnologies.slack.com/archives/C0AL1T2H43V/p1789616637872589
tags:
- morning-gtd
- slack
- from-awareness
time_minutes: 10
title: 'Read: AI tooling: Laura in #project-workup - Workup missed 18 of 25 duplicate
  closes; proposes dropping the 7-day window and asks Blake what would justify auto-'
updated: 2026-09-17 12:19:51.768468
waiting_on: null
waiting_since: null
working_on: false
---

Workup missed 18 of 25 duplicate closes; proposes dropping the 7-day window and asks Blake what would justify auto-close
https://canarytechnologies.slack.com/archives/C0AL1T2H43V/p1789616637872589