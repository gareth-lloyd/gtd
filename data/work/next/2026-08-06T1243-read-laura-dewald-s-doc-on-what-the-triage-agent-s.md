---
area: null
completed_at: null
contexts:
- consume
created: 2026-08-06 12:43:12.863311
defer_until: null
due: 2026-08-06
energy: low
id: 2026-08-06T1243-read-laura-dewald-s-doc-on-what-the-triage-agent-s
order: 10
output: |
  ## Agent run 2026-08-06T13:05Z

  Read the doc (https://pages.cnry.cloud/workup-missing-info/) and the Slack thread
  (https://canarytechnologies.slack.com/archives/C0AL1T2H43V/p1785891086491339?thread_ts=1785891086.491339&cid=C0AL1T2H43V).

  ### What it is
  "When a ticket doesn't say enough" — Laura DeWald, Aug 2026. A proposal doc asking for a
  decision between Approach A / B / C on what the Workup agent does when a ticket lacks the
  concrete entity it needs. Grounded in both codebases as of Aug 3; scoped to the core flow
  (phase 2 explicitly excluded). Posted in Slack 2026-08-05 for "discussion tomorrow" — i.e.
  the meeting is today. Only one thread reply (Khushkaran: read the top box, sounds good), so
  nothing has been debated in writing yet. The room is where the decision happens.

  ### The core argument (one line)
  "Never gate triage on a human, and never start the spend without an anchor. The gap between
  those two is where asking belongs."

  Triage (team, urgency, summary) works fine on a thin ticket. Investigation is a sandboxed
  prod-data deep dive at a ~$9 median per run and cannot do anything without an *anchor* —
  hotel, reservation, sales booking, user, payment authorization, or wallet. Today those two
  are fused, which is the whole bug.

  ### Today's three failures
  1. **The fork** — a thin ticket leaves the workup path for a legacy bot and never returns,
     even after someone answers. Triage result is withheld, the team move is skipped. Two bots
     in one team.
  2. **The black hole** — the legacy bot's question has no deadline, no follow-up, no metric.
     Waits forever, invisible, and the waiting state blocks re-triage. Replies posted in the
     wrong place are silently dropped.
  3. **The dead-end ask** — when investigation *does* run and finds nothing, it writes a
     helpful "here's what I need" and then ends the conversation. Addressed to nobody, changes
     no state, no way to answer. (Fixing this is phase 2, out of scope.)

  ### Approach A (the recommendation)
  Every ticket goes to the workup agent. Triage posts immediately and routes normally. If the
  anchor is missing: one templated question + `Needs Info` label, ticket parks at zero cost in
  the destination team's Triage inbox. Reply in the ticket → resolved through the same lookup
  code triage already uses → investigation runs.
  - No answer, medium/low: nudge at ~1/3 of the priority SLA, then assigned back to the
    filer + Linear inbox ping, then Cancel at the SLA deadline with explicit reopen
    instructions (reopening restarts the flow).
  - No answer, urgent/high: escalates to the triage rotation within hours with the agent's
    partial findings. **Urgent tickets never auto-cancel.**
  - At most 2 asks total.

  Five design details worth knowing: the ask is templated from a fixed missing-field list (no
  LLM phrasing, no invented requirements, blocks only on what's genuinely required); replies
  are treated as search terms through one internal MCP lookup tool, never as instructions
  (prompt-injection closed by construction); all windows are computed live as fractions of the
  current SLA, so a priority bump re-routes at the next check; the ticket never enters an
  accepted/working state while unanchored; and Zendesk-escalated tickets get the question as a
  real comment so it syncs out and reopens the Zendesk ticket — routine agent chatter
  deliberately stays out of the comment stream to avoid spurious reopens.

  Build cost: small-to-medium, not a rewrite. Riskiest piece is resume-on-reply routing, and
  ~half that machinery already exists for mid-investigation prompts.

  Alternatives rejected: **B** (park with a note, never ask) — depends on someone noticing a
  label, and re-triggering rebuilds most of A anyway. **C** (patch the legacy bot: hand off on
  answer + add expiry) — keeps the two-bot experience and invests in a path already scheduled
  for deletion.

  ### Why this matters for the ENT triage-automation lever
  This doc is unusually good ammunition for the #eng-directors argument, and mostly on the
  economics rather than the ergonomics:
  - **It puts a price on the failure mode.** ~$9 per investigation run, and today we spend it
    on tickets that are structurally guaranteed to return "insufficient context." The anchor
    gate is a spend control, not a UX nicety — and "investigation runs avoided, in dollars" is
    one of the proposed success measures. That's the number to quote.
  - **It separates the cheap automatable half from the expensive half.** Triage — team,
    urgency, summary — needs no context and should never wait on a human. That's precisely the
    ENT triage lever: the argument doesn't depend on the agent being able to *solve* anything,
    only on it being able to *route and summarise* everything. Approach A makes that split
    explicit and defensible.
  - **It kills the "tickets vanish into the agent" objection.** `Needs Info` as a filterable
    state plus SLA-derived timeouts plus a human backstop for urgent means automation never
    silently swallows work. That is the standard directors' objection and the doc pre-answers it.
  - **It hands over the intake conversation.** "Share of tickets arriving thin" and "share of
    asked tickets that cancel unanswered" size the upstream problem — i.e. how much of the ENT
    load is CS-self-serve or misrouted rather than engineering work at all. That's the same
    argument the enterprise work-ticket playbook makes; the metric would make it arguable with
    numbers instead of anecdote.
  - **Caveat to be honest about:** the doc concedes the answer-rate data doesn't exist today
    (raw events are in the DB, nothing emits a metric, and replies in the wrong place leave no
    trace at all, so current data *undercuts* itself). So "we'll measure it" is a promise, not
    a baseline. Don't over-claim it in the directors thread.

  ### The seven open questions — where a view is probably wanted today
  1. Per-priority windows (medium: nudge at 1 business day, exit at day 3; urgent: hours).
  2. Re-ask limit — proposed 2 total.
  3. What a reply *after* close-out should do (reopen-with-info is decided; replies on
     fully-investigated tickets are not).
  4. Should plain comments outside the agent's thread count? Current lean: yes in v1, scoped to
     waiting tickets. **This one matters for ENT** — Zendesk-escalated tickets are exactly the
     case where the reply arrives as an ordinary comment.
  5. When phase 2 (resumable investigations) starts — proposed: after the core flow proves out.
  6. Does `Needs Info` pause the SLA clock? Reporting question, flow works either way.
  7. Teams that auto-assign triage tickets — leave the assignment alone until the nudge, or
     reassign to the filer immediately? Needs a decision *with* those teams.

  ### Suggested position
  Back Approach A. B and C both preserve the split-ownership problem that caused this. The
  parts to push on in the meeting: Q4 (plain-comment support in v1, because of Zendesk/ENT) and
  Q7 (auto-assigning teams) — those are the two that decide whether this actually works for the
  enterprise queue rather than just for tickets filed natively in Linear. Q6 is a reporting
  detail that shouldn't hold up the decision.

  ### Not done
  Nothing posted anywhere — no Slack reply, no Linear comment, no doc comment. Read-only run.
project: 2026-04-16T1210-unblock-team
source_id: https://canarytechnologies.slack.com/archives/C0AL1T2H43V/p1785891086491339?thread_ts=1785891086.491339&cid=C0AL1T2H43V
tags:
- morning-gtd
- slack
- from-awareness
time_minutes: 15
title: Read Laura DeWald's doc on what the triage agent should do when missing context
updated: 2026-08-06 16:06:09.939251
waiting_on: null
waiting_since: null
working_on: true
---

Laura prepared this to discuss what happens when the agent lacks the context it needs to act — directly relevant to the ENT triage-automation lever I'm arguing in #eng-directors.
https://pages.cnry.cloud/workup-missing-info/
Thread: https://canarytechnologies.slack.com/archives/C0AL1T2H43V/p1785891086491339?thread_ts=1785891086.491339&cid=C0AL1T2H43V