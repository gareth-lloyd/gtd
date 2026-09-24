---
area: null
completed_at: 2026-09-23 16:12:08.545409
contexts:
- react
created: 2026-09-22 09:50:30.915498
defer_until: null
due: null
energy: low
id: 2026-09-22T0950-reply-to-laura-re-workup-slack-follow-up-mechanism
order: null
output: |
  ## Agent run 2026-09-22T14:30:00+03:00

  ### Short answer
  Do not pull the full "AI Workup: Interactive Investigations" PRD into Q4A. It is a 14-19 engineer-week build that only Laura can do, and she already owns Accuracy (target 6 Oct) and the SQL tool. What eng leads actually asked for ("a mechanism like Lettuce to Slack people for follow-up info") is a much smaller slice: a one-way Slack DM nudge. That slice is roughly one engineer-week, needs no new infrastructure, and can go in the block as its own line item while the full PRD stays in Up Next.

  ### What "Lettuce-style" means
  Lettuce's mechanism is a scheduled one-way Slack DM: "you have outstanding items, here is the link", repeated daily until done (see the Lettuce bot DMs in your own Slack, e.g. https://canarytechnologies.slack.com/archives/D0C2EPFVAQY/p1789970436603099). No reply intake, no state machine. The PRD is a different animal: a full bidirectional loop (ask mid-run, park, resume from three channels, region ladder, SLA cancel, Zendesk mirroring).

  ### Sources reviewed
  - Laura's reply (Slack): https://canarytechnologies.slack.com/archives/C0A4BS2AREH/p1790003955102049
  - Q4A planning doc, Up Next section: https://app.notion.com/p/3db8146861518171aab0dbfe1d5b53ca#aa5cea48fdb844228b67ace52e0835fd
  - PRD (Laura + Steph, closed out 26 Aug): https://app.notion.com/p/3b9814686151818b9e09f189f1499888
  - Tracker (Complexity: M, Status: In Discovery): https://app.notion.com/p/39681468615181d7ba30f326690d3205
  - Linear project P-TOOL-2236 (status Product Definition, 0 issues, 0 documents): https://linear.app/canary-technologies/project/ai-workup-interactive-investigations-8e1ffa958fa5
  - Eng design: NOT FOUND in Notion (Design Doc Database) or Linear. Laura said it is "in progress"; the TOOL-450 plan was a local file on her machine, so this one probably is too. Ask her where it lives.
  - Codebase survey of both repos (canary + canary-agents/Overlord) for what already exists.

  ### Scope of the full PRD (11 Must-Haves) against the code today
  | PRD requirement | Exists? | Effort |
  |---|---|---|
  | ASK-001 delete the thin-ticket fork + legacy FOLLOW_UP loop | partial. Three forks live in canary (`linear_agent/tasks.py`, `services/webhook.py`). NOTE: on Workup teams ASK_FOR_ENTITIES is already flattened and handed off; only ambiguous-hotel and triage-failed still divert. The PRD's 39% "never investigated" claim may be stale | M |
  | ASK-002/003 stop mid-run, write resume bundle, post elicitation, park with `Workup: Needs Info` | missing. Good adjacent parts: `submit-mcp.ts` is a clonable pattern for a `request_info` tool; `evidence-store.ts` is ~60% of a bundle writer but nothing reads evidence back; Overlord's Linear client has no `elicitation` activity type | L + S |
  | ASK-004 Linear reply resumes in fresh seeded sandbox | partial. `routeToIsolatedBox` can boot a box with a seeded payload; but `match()` forces createSandbox:false on prompted events and `resolveMode` only goes isolated when a live box exists | M |
  | ASK-010 plain comment resumes | missing. Comment webhooks parse but `matchesAgent` only matches `@workup`; `match()` is synchronous, store lookup is async | M |
  | ASK-007 Slack DM ask + accept answer in DM | missing. Workup has no Slack app/bot identity; no DM-thread to issue mapping. Golem's `notifyAssignment` is a one-way precedent only | L (send) + L (receive) |
  | ASK-005 region ladder | partial. DynamoDB `hotel_slug_routing` already stores slug to region but nothing returns it; Zendesk to hotel to region does not exist; cross-region search has no orchestrator | M |
  | ASK-006 responsible-human ladder | partial. `resolveUserByEmail` + `getUserSourceId(user,"slack")` exist (zero call sites); `getIssue` does not select creator; no triage-owner concept | M |
  | ASK-008 SLA watchdog nudge then cancel | partial. `watchdog.ts` sweeps every 5 min with per-status deadlines; no SLA-by-priority table anywhere, no `slaBreachesAt` in the GraphQL selection | M |
  | ASK-009 Zendesk-linked asks as real comments | partial. `postComment` exists; Zendesk link detection needs attachments in `getIssue` | S-M |
  | ASK-011 metrics | missing. Overlord has no metrics system, only console Logger. Resume also breaks the one-run-per-ticket assumption in `workup_runs` and the judge joins (thread_key pinned to `api:workup:<uuid>`) | S-M |

  Totals: 2 S, 7 M, 3 L. At S = 2-3 days, M = 1-1.5 weeks, L = 2-3 weeks, single-threaded: 14-19 engineer-weeks. Even a "minimum PRD" that drops the Slack loop, Zendesk and region ladder is still 7-9 weeks. Only Laura is fluent in Overlord (catch-up brief: 62 of the agents-repo Workup PRs are hers), Asher is out 16-27 Oct, and Laura's leave is roughly three months out. It does not fit Q4A alongside Accuracy.

  ### Reduced scope that fits the block: "Slack nudge for existing asks" (~1 week, S)
  Attack the 2% reply rate directly, without touching the run/resume machinery. Two hooks, both using code that already exists:
  1. Legacy triage ask (canary). When triage posts an ask and while the ticket sits in `AWAITING_ENTITIES`, DM the ticket creator in Slack with the question and the Linear link; re-nudge daily; stop after N business days with a closing note. Canary already has `find_slack_user_by_email` and chat.postMessage in `internal_support/services/slack.py` (used today for Support Access Grant DMs), so no new Slack app. Answers are still typed in Linear and the existing FOLLOW_UP loop picks them up unchanged.
  2. Workup "request-info" exit (Overlord). When an investigation ends with the `Next Step: Request Info` label (already emitted by `next-step-label.ts`), DM the creator with the question and the link, using the existing `resolveUserByEmail` + `postMessage` (golem's `notifyAssignment` is the template). No reply intake in v1: the person answers in Linear; a comment on the ticket is the signal to stop nudging.
  Plus a two-line metric: nudges sent, and whether the ticket got a comment within the window. That is the answer-rate baseline the full PRD's success metric (≥50%) needs anyway.

  What this slice does not do: no mid-run stop or resume, no Slack reply intake, no region ladder, no SLA auto-cancel. Filers without Linear accounts (~14% of Oncall) get the DM only if the issues-form email is on the ticket, which needs a quick check.

  ### Suggested position for the planning call
  - Add the nudge slice to Q4A as its own small item (or as phase 0 of Interactive Investigations), owner TBD, ~1 week. It is what eng leads asked for and it produces the data the PRD needs.
  - Leave the full PRD in Up Next; revisit for Q4B with real answer-rate numbers.
  - Ask Laura: where is the eng design, and does it already split out a "notify only" phase? Also flag that the code has moved since the PRD (ASK_FOR_ENTITIES already handed off on Workup teams), so ASK-001 may be smaller than written.

  ### Draft reply to Laura (Slack, group DM with Steph). NOT SENT, for you to post.
  > Thanks. I read the PRD and had a look at what's already in both repos. The full Interactive Investigations build is big (my rough count: 3 L + 7 M pieces, most of it Overlord, so realistically you) and I don't think it fits Q4A next to Accuracy and SQL.
  >
  > But what eng leads actually asked for is narrower than the PRD: a Lettuce-style one-way Slack DM ("your ticket is waiting on X, here's the link", nudged daily) on the asks we already post, with a comment on the ticket as the stop signal. Canary already has the email-to-Slack lookup and DM sender from the SAG flow, and Overlord has resolveUserByEmail + postMessage with no callers. That looks like about a week and it gives us the answer-rate baseline the PRD's success metric needs.
  >
  > Proposal for the planning call: put that nudge slice in Q4A as its own line (or phase 0 of Interactive Investigations), keep the full PRD in Up Next for Q4B. Does your eng design already carve it that way? And where does the design live, I couldn't find it in Notion or on the Linear project.
  >
  > One thing I noticed: on Workup teams, ASK_FOR_ENTITIES tickets are already flattened and handed off; only ambiguous-hotel and triage-failed still divert to the legacy loop. So the "delete the fork" piece may be smaller than the PRD says.
  ## Agent run 2026-09-22T14:50:00+03:00
  Follow-up: confirmed Workup cannot resume on a Linear comment today (plain comments match no agent; @workup replies hit the stub once the sandbox is gone; no awaiting state or resume bundle exists). Revised Slack draft with the descope and its limitations, NOT SENT:
  > Thanks Laura. I read the PRD and poked around both repos to see what's already there, so here's my take for the planning call.
  >
  > The full Interactive Investigations build is a lot: stop mid-run, resume bundle, resume from Linear/comment/Slack, region ladder, SLA cancel, Zendesk mirroring. My rough count is 3 L and 7 M pieces, almost all in Overlord, so realistically all you, on top of Accuracy and SQL. I don't think it fits Q4A and I'd rather not pretend it does.
  >
  > What eng leads actually asked for is narrower: a Lettuce-style nudge. So a possible descope for this block:
  >
  > Phase 0, "Slack nudge for existing asks" (~1 week)
  > - When triage posts an ask, or an investigation ends with `Next Step: Request Info`, DM the ticket creator in Slack with the question and the Linear link.
  > - Re-nudge daily. A comment on the ticket stops the nudging. After N business days, stop and leave a closing note.
  > - Count nudges sent and whether the ticket got a comment in the window. That's the answer-rate baseline the PRD's >=50% target needs anyway.
  > - Reuses what exists: canary's email-to-Slack lookup and DM sender from the SAG flow, and Overlord's resolveUserByEmail + postMessage (currently no callers).
  >
  > Being honest about what that does NOT do:
  > - Workup does not resume. A comment on a finished investigation goes nowhere today (plain comments match no agent, and @workup replies hit the "can't take follow-ups" stub once the box is gone). The answer just lands on the ticket for a human.
  > - No Slack reply intake. People still answer in Linear.
  > - The legacy triage ask still parks tickets the way it does now. On Workup teams most missing-info tickets are already handed off anyway, so this mostly affects ambiguous-hotel and triage-failed cases.
  > - No region ladder, no SLA auto-cancel, no Zendesk mirroring.
  >
  > So it moves the 2% reply number and gives us data, but it doesn't turn a stalled run into a resolved one. That stays the full PRD, which I'd keep in Up Next for Q4B.
  >
  > Two questions: does your eng design already carve out a notify-only phase like this? And where does it live, I couldn't find it in Notion or on the Linear project.
  ## Agent run 2026-09-23T13:45:00+03:00
  Follow-up asked: "verify claims of the comment draft, and redraft to be shorter, less prescriptive and more suggestive"

  ### Claim check against both repos (canary master e3f5d1a, canary-agents b1943bd 2026-09-17)
  Holds up:
  - `Next Step: Request Info` label is real: defined in `overlord/src/agents/workup/next-step-label.ts:23` and applied at the end of every investigation (`agents/workup/agent.ts:518`).
  - Plain Linear comments never reach Workup: `sources/linear.ts` `matchesAgent` only matches when the body contains `@<linearBotName>`.
  - The follow-up stub exists verbatim at `agents/workup/agent.ts:704` ("I can't take follow-up questions on this ticket. A human will follow up here...").
  - Legacy triage ask is still live for triage-failed, ambiguous-hotel and non-Workup-team tickets; ASK_FOR_ENTITIES on Workup teams is rendered and handed off (`linear_agent/tasks.py:380-410`).
  - Canary has an email-to-Slack lookup (`internal_support/services/slack.py:81`, oncall token) and the SAG flow has its own lookup + `_post_chat_message` DM sender (`support_access_grant_slack.py:82`, support-access token). So no new Slack app is needed on the canary side, but it has to pick one of two existing tokens.

  Needs correcting in the draft:
  - "resolveUserByEmail + postMessage (currently no callers)" is half wrong. `resolveUserByEmail` (`overlord/src/clients/slack.ts:101`) has zero callers, but `postMessage` is used by Golem notify, the Slack source and the schedule source. Say "resolveUserByEmail has no callers yet" or drop the aside.
  - Workup has no Slack bot identity. Overlord loads per-agent `{SLUG}_SLACK_BOT_TOKEN`; there is no WORKUP_SLACK_BOT_TOKEN anywhere in canary-agents, canary-kubernetes or terraform. A Workup DM needs a Slack app (or borrowing Golem's), which is config work, not code, but it is not "already there".
  - Overlord does not know who filed the ticket. `ISSUE_FIELDS` in `clients/linear.ts:383` fetches assignee but not creator, and the canary handoff payload carries no filer email. Small GraphQL addition, but again not zero.
  - "3 L and 7 M" is the previous run's estimate; not re-derived today. Present it as rough.
  - Eng design location: not re-searched today; prior run found nothing in Notion or the Linear project. Keep it as a question.
  Net: the ~1 week for the nudge slice still looks right for the canary hook; the Overlord hook is closer to 1-1.5 weeks once a Slack app and creator lookup are included. "Reuses what exists" is fair for canary, generous for Overlord.

  ### Redraft (shorter, suggestive). NOT SENT.
  > Thanks Laura. I read the PRD and had a look at what's already in both repos before the planning call.
  >
  > The full Interactive Investigations build feels like a lot for Q4A next to Accuracy and SQL: stop mid-run, resume from Linear/Slack, region ladder, SLA cancel, Zendesk. Rough count is 3 L and 7 M pieces, most of them Overlord. Does that match your eng design's read?
  >
  > What eng leads asked for is narrower than the PRD, more of a Lettuce-style nudge. One way to slice it: when triage posts an ask, or an investigation ends with Next Step: Request Info, DM the filer in Slack with the question and the link, re-nudge daily, stop when the ticket gets a comment. No resume, no Slack reply intake, people still answer in Linear. Canary already has the email-to-Slack lookup and DM sender from the SAG flow; Overlord would need a Slack app for Workup and a creator lookup, so maybe a week or so. It would also give us a real answer-rate number, which the PRD's 50% target needs anyway.
  >
  > Not sure that belongs in Q4A either, but it seemed worth putting on the table as a phase 0 with the rest staying in Up Next. Curious whether your design already carves it that way, and where the design lives, I couldn't find it in Notion or on the Linear project.

  Sources: Laura's reply https://canarytechnologies.slack.com/archives/C0A4BS2AREH/p1790003955102049 ; PRD https://app.notion.com/p/3b9814686151818b9e09f189f1499888 ; Q4A Up Next https://app.notion.com/p/3db8146861518171aab0dbfe1d5b53ca#aa5cea48fdb844228b67ace52e0835fd ; Linear project https://linear.app/canary-technologies/project/ai-workup-interactive-investigations-8e1ffa958fa5
project: 2026-04-16T1210-unblock-team
source_id: https://canarytechnologies.slack.com/archives/C0A4BS2AREH/p1790003955102049
tags:
- morning-gtd
- slack
time_minutes: 10
title: 'Reply to Laura re: Workup Slack follow-up mechanism — pull into next block
  or leave in Up Next?'
updated: 2026-09-23 16:12:08.545403
waiting_on: null
waiting_since: null
working_on: false
---

I asked whether the Lettuce-style follow-up mechanism for Workup is explicitly in the next block. Laura: it's in the 'Up Next' section of the planning doc, no progress because higher priorities, eng design in progress. Block planning week: a prioritization call is implied.
https://canarytechnologies.slack.com/archives/C0A4BS2AREH/p1790003955102049

Review the notion doc and estimate scope. can scope be reduced to get this in block?