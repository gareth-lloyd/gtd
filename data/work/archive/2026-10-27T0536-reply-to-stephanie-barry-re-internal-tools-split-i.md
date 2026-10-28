---
area: null
completed_at: 2026-10-27 14:34:02.708865
contexts:
- react
created: 2026-10-27 05:36:42.380373
defer_until: null
due: null
energy: low
id: 2026-10-27T0536-reply-to-stephanie-barry-re-internal-tools-split-i
order: null
output: |
  ## Agent run 2026-10-27T08:40
  Read Stephanie's DM write-up (https://canarytechnologies.slack.com/archives/D09Q1PTAMTR/p1793023231941619) and checked Bear for your prior thinking. NOTHING SENT. Below is a draft reply. The "view" parts are my inference from your notes, so edit them to match what you actually think.

  Context from Bear:
  - In "Stephanie Barry 1-1" (1 Oct) you argued against "two tiny teams with duplicating coordination overhead, doing naturally overlapping work". That argument was used to fold Support Eng into Internal Tools/CA, and it favours one pod with two focus areas.
  - Capacity risks: Laura goes on parental leave in December, and she is interim eng lead and owns triage. Sam's support-eng continuity was framed as 4-8 weeks. The backfill justification in "Laura Dewald" says triage is already at its limit.
  - Resolution agent: Bear has nothing under that name. The closest is Sudarshan's customer-admin configuration agent, which you reviewed on 23 Oct (critique: drift, fails open on reads). It may be a different thing, so confirm before you reference it.

  DRAFT (Slack DM to Stephanie):
  ---
  Thanks Stephanie, this is really helpful and exactly what I was after. Both mandates feel like the right level of ambition, much better than polishing today's process.

  My initial view on the open questions:
  • *One pod or two:* I'd keep one pod with two focus areas. It spreads expertise across more of the team, so knowledge doesn't sit with one or two people per stream. It lets us move people fluidly between implementation and resolution as priorities shift. And it gives us resilience through Laura's parental leave in December, when a smaller split team would really feel the gap. We also only just merged support eng in to avoid two small teams duplicating coordination on overlapping work. Agent misses will show us where onboarding is broken and the other way round, so the streams feed each other.
  • *Capacity/timeline:* with Laura out from December and Sam's support-eng continuity time-boxed, I'd like to agree who keeps triage/BAU covered before we commit to dates, so it doesn't quietly eat the capacity for both initiatives.
  • *Product time on the resolution agent:* if most of your time goes to implementation, I think the agent needs a named owner on the product side, even part-time, plus a clear eng lead. Otherwise it drifts. Happy to think through who that could be.
  • *Sudarshan's work:* keen to build on it rather than restart. I'd like to understand how it overlaps with the triage/routing tooling Laura's team already owns.

  Happy to jam on the breakdown as it comes together this week. Feel free to send drafts early.
  ---
  Open for you: confirm "one pod" really is your view, and whether to name Laura's leave in this DM.

  ## Agent run 2026-10-27T08:50
  Revised the draft above: one pod, two focuses (confirmed). One-pod bullet now gives your reasons: shared expertise, fluid resourcing, resilience through Laura's leave, then the earlier coordination point. Capacity bullet trimmed so the leave isn't argued twice. Still NOT sent.
project: 2026-04-16T1210-unblock-team
source_id: https://canarytechnologies.slack.com/archives/D09Q1PTAMTR/p1793023231941619
tags:
- morning-gtd
- slack
time_minutes: 15
title: 'Reply to Stephanie Barry re: Internal Tools split (Implementation vs Customer
  Resolution)'
updated: 2026-10-27 14:34:02.708856
waiting_on: null
waiting_since: null
working_on: false
---

She sent the async write-up I asked for: split into Implementation (50% self-onboarding) and Customer Resolution (resolution agent), with open questions on one pod vs two, capacity, product time. Acknowledge and give my view.
https://canarytechnologies.slack.com/archives/D09Q1PTAMTR/p1793023231941619