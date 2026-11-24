---
area: null
completed_at: 2026-11-23 14:35:00.516552
contexts:
- consume
created: 2026-11-20 00:00:00
defer_until: null
due: null
energy: low
id: 2026-11-20T0000-review-this-week-s-eng-leads-recording
order: null
output: |-
  ## Agent run 2026-11-23T14:18

  Source: Eng Leads Weekly, Thursday 2026-11-19, 63 min. Recording: https://tv.canary-engineering.com/watch/71df3032-248e-43c8-a352-b5c777693c3a (no passcode; Notion row https://app.notion.com/41e8146861518117b9d9c9ba6591ecac).

  How this was produced: I read the full CanaryTV auto-transcript (Whisper, 665 segments), not the video. The transcript has no speaker labels, so attributions below are inferred from context and names are as Whisper spelled them. Nothing shown on screen (Blake's security doc, the temperature board, chat) was captured. Timestamps are positions in the recording.

  ### Things that touch you

  - **Peter's demo (07:35, 08:47, 09:44).** Andy told the room he has already spoken to you about Peter recording a Friday demo (preset messages with attachments), since the live slot is a bad time for him, and that you will ask Peter whether he wants to. When someone asked if Peter knows, the answer was "not yet".
  - **Security sprint can override block plans (13:00-15:00).** Blake said the sprint comes ahead of all enterprise work and may jump anything from the block reviews that just happened. He will route each chosen project to the pod he thinks fits and says he will bring leads along on decisions in their product area.
  - **Production shell access (49:12).** Daga's topic: remove production shell access and keep it for break-glass only. Not discussed in the room; Blake said it needs a high-conviction strategy and will likely be handled inside the security sprint.
  - **DiffBird (49:40-62:00).** Only about 7-8 people have turned on the contributor team review feature. Each team is expected to write its own review instructions (code review folder at the monorepo root); without them, a DiffBird auto-approval triggered through another team can count as an approval on your code. Review-board policies can require a human approver for specific paths.
  - **"Garrett" and the GPT deprecation audit (36:46-39:44).** Someone transcribed as "Garrett" was in the room and took the audit of OpenAI model usage. I read this as a different person (Applied AI), not you, because they answered live. Worth a glance if that is wrong.

  ### Security sprint (Blake, 10:54-21:40)

  - Trigger: last week's incident. An endpoint that had existed for years was brute-forced and reservation data for about 15K reservations was taken. Blake called it very likely AI-assisted. A retro is planned and will go out to all of engineering.
  - Framing: assume every weak point will be exploited; human-in-the-loop warnings are not enough, so controls must restrict first and notify humans to undo.
  - Top company priority. Runs until Blake and SJ are both comfortable with the remaining known issues.
  - Scope: anything in the "Canary got hacked" category: data exfiltration, remote code execution, internal networks, developer machine takeover.
  - Plan: Blake coordinates. Discovery first (collect known risks already in Linear into one place, plus a post in the eng announcements channel asking everyone to file tickets for known issues), then fix what the core team can, then prioritise the rest into product teams.
  - Core team dropping other work: Blake, Andy, and "Yohini", Charles and Chris Carter where needed.
  - Priority order: data breach is the guiding light. Cost-abuse issues rank lower; data breach ranks above DDoS.
  - Product changes are in scope and expected; Blake and SJ make the calls. Examples given: the reservation lookup page, Workbench on Supabase (its reservation sync has exposure risk), and eliminating every case where Canary reads a card directly or returns a raw PAN to a customer.
  - A lead from payments asked for a single point of contact on ordering and deadlines given spillover; Blake said that is his role.

  ### Critical items (29:27-39:44)

  - Playwright critical end-to-end tests are now blocking; live with no problems.
  - Loom deprecation: last day was Friday 2026-11-20. Notion links migrated to CanaryTV; fewer than a handful of orphan videos. Users removed and account moved to the free tier.
  - Holiday on-call: one general slot left (January). Incident Commander about 50% filled; Alan may split it into single days or half shifts.
  - RDS CMK switchover: last one is EventsDB, Tuesday 2026-11-24.
  - Python 3.14: waiting on one team; pushed to after Thanksgiving.
  - Sign in with Google lockdown: unapproved apps are blocked from 2026-12-04. About 600 apps lose access immediately. SJ approved. Blocked users can request review via an IT ticket. Blake wants tight comms, ideally a personalised email listing each person's affected apps.
  - OpenAI model deprecations: the 2026-12-11 batch is GPT-5 models, believed unused, to be double-checked. GPT-5.4-mini and related models, which are used extensively, are dropped 2027-01-11 and get their own line in the critical items table. Direct OpenAI only; Bedrock usage is unaffected. Blake wants Applied AI to own tracking model deprecations.

  ### Temperature (24:43-29:20)

  - SIEM explained: central collection of security events (Google Workspace, AWS, Canary Admin audit logs) with rule-based alerting that tickets the security team.
  - Open-sourcing Sallyport, planned for December, was questioned as a risk for a secure access layer. A refactor to decouple Canary-specific parts is under way and security will review first. Agreed to take it into the security sprint.
  - One team ran a one-hour brainstorm (20 minutes silent ticket writing on a Figma board, 40 minutes discussion), got through under 10% of the ideas, and is repeating it next week.

  ### Discussion (39:52-62:30)

  - **Review delays and Camp Canary (Andrea).** Teams are frustrated that performance reviews are delayed and feel stale, and that Camp Canary was not answered at all hands while people hold off on personal travel. Blake agreed and is working on the review delay. Guidance: do not hold feedback back; give it informally now and have forward-looking conversations now if you judge that better. Negative feedback first heard at the review was delivered too late.
  - **Eng retreat.** No property is booked. Blake is comfortable saying there will be no retreat in March or April; the intent is a retreat later than April (end of May was the target). He wants two touchpoints a year and is trying to get that into budget; it may not be a full-team retreat. One lead argued for grouping by pod or product area over region and Blake agreed.
  - **Macroscope.** DiffBird is its replacement from an EE perspective, because Macroscope charges per PR. Daga will propose a deprecation date and post again; a repeat demo was requested for show and tell. Feedback from Andrea: platform comms need to say plainly whether a tool is required or just suggested. Blake: tooling approval does not remove the author's ownership of a change.
  - Two topics were not reached and carry to next week.

  ### Friday demos (05:16-10:40)

  - Andy is trialling a GrokBot automation that proposes demos from the Just Hatched and eng channels (robot emoji marks them). Agreed: Piotr, a short PSA on encrypted fields; Daniel, insights dashboard; Dylan, Canary Public MCP; Jason possibly. The face liveness POC was dropped as too early.

  No external writes were made. I fetched the transcript through the CanaryTV page in a browser session, which registered one view on the recording.
project: null
source_id: null
tags: []
time_minutes: 30
title: Review this week's Eng Leads recording
updated: 2026-11-23 14:35:00.516547
waiting_on: null
waiting_since: null
working_on: false
---

Watch this week's Eng Leads meeting recording (meets Thursdays; recording usually posted Thursday evening/Friday).

- Recordings DB (links + passcodes): https://app.notion.com/p/canarytechnologies/328814686151804588fae86f1fb42c87?v=32881468615180cf9f08000caf331759