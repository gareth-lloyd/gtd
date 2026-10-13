---
area: null
completed_at: null
contexts:
- consume
created: 2026-10-13 10:40:19.991550
defer_until: null
due: 2026-10-13
energy: null
id: 2026-10-13T1040-review-eng-leads-2026-10-08-workup-triage-discussi
order: null
output: ''
project: 2026-09-08-workup
source_id: null
tags: []
time_minutes: 15
title: 'Review Eng Leads 2026-10-08 Workup triage discussion: problems and owners'
updated: 2026-10-13 11:07:48.831513
waiting_on: null
waiting_since: null
working_on: false
---

Source: Eng Leads 2026-10-08 (Zoom transcript ~/Downloads/GMT20261008-162948_Recording.transcript.vtt), temperatures section. Discussion started from Laura's temperature update and Sudarshan's push. Transcript is garbled in places (e.g. lines ~339-340), so check before quoting anyone.

## Where Workup is today (Laura)
- Working with the messaging and PMS gateway teams; accuracy rising.
- Auto-closes only exact duplicates that match one-to-one for the same hotel.
- On close it comments and tags the triage engineer and the person who filed the ticket. That's the human safety net.
- Next week: auto-close tickets that only need a configuration change.

## Problems, with owners

### 1. Triage load is hurting messaging team morale
- About 75-90 tickets a week (~10 a day), most coming through on-call. Workup touches most of them.
- Everyone voted yellow on triage in the retro. Other engineers keep jumping in because one person on triage can't keep up with the queue.
- The two biggest triage loads were merged into one rotation.
- **Owner:** Matías (team lead), with Sudarshan.

### 2. Auto-close is too conservative for its potential
- Sudarshan: tickets are filed by internal staff who can reopen a wrong close. A junior engineer who diagnosed 80% correctly would be acceptable, so the agent should be too. So far the impact doesn't match the time and technology invested.
- Laura's only reason for caution: not wanting to frustrate the people filing tickets.
- **Decision (Blake):** cleared to be more aggressive with rollouts, because people reopening wrong closes act as the backstop.
- **Owner:** Laura, brainstorming with Sudarshan on Slack.

### 3. Expand to "expected behavior" tickets
- Matías: config changes are mostly not done by eng anyway, so commenting and handing back to CS or the customer is fine.
- Wants the same approach for tickets about expected behavior of AI and guest journey messages: send them back with an explanation.
- **Owner:** Matías and Laura (not explicitly assigned).

### 4. Impact paradox (open question)
- Blake: if Workup is right, there should already be a big impact, because engineers just read it, verify and close. If verifying is expensive, nothing has really been saved. Both can't be true.
- **Owner:** none. Blake raised it; it frames problems 5 and 6.

### 5. Output is hard to digest
- Matías: how much engineers trust Workup's output varies by person. Explanations are often correct but hard to read.
- Sudarshan: the last 10% may be turning correct but hard-to-read into correct and short. That may be what gets it over the line.
- **Owners:** Dmitry (output format; will comment to Laura). Matías (check how useful engineers find the explanations).

### 6. Impact is hard to measure
- Laura: time-to-close for messaging has dropped, but the team merge muddies the comparison.
- **Owner:** none assigned. Laura is the natural owner.

### 7. Accuracy ceiling
- Blake firmly believes Orbital, which Jason is chasing, is the fastest path to much better accuracy, and that it is moving as fast as possible. Part of him wants to wait for that tooling, but he accepts the messaging team's pain now.
- **Owner:** Jason (Orbital).

## Why this matters to me
This overlaps the Workup vs TypeSafe/Jev backtest (backend/canary/tmp/data/workup_typesafe/NOTES.md). Raw accuracy was 52.7% in that backtest, against Sudarshan's 80% benchmark. Also relevant to the readability problem (5) and the measurement problem (6).