---
area: null
completed_at: 2026-10-15 14:55:21.045459
contexts:
- consume
created: 2026-10-13 10:40:19.991550
defer_until: null
due: 2026-10-13
energy: null
id: 2026-10-13T1040-review-eng-leads-2026-10-08-workup-triage-discussi
order: null
output: |
  ## Agent run 2026-10-13T15:02

  Checked the body against the transcript (~/Downloads/GMT20261008-162948_Recording.transcript.vtt, cues at about lines 1080-1460) and against backend/canary/tmp/data/workup_typesafe/NOTES.md.

  ### Summary
  The body is mostly accurate. Seven points need fixing or softening. The main thing missing is how it lines up with the backtest. The 52.7% figure measures something different from Sudarshan's 80%. The backtest also says the expansion Matías asked for (problem 3) targets the bucket where Workup is weakest.

  ### Corrections to the body
  1. **Owners are mostly inferred.** The only explicit commitments are:
     - Sudarshan offered Laura a Slack brainstorm ("happy to discuss further... take this to slack").
     - Matías said "I could also double-click into... how useful" the Workup explanations are, and Laura replied "that would be helpful".
     - Matías said Dmitry "is working on that, is thinking about that. We'll probably see some comments from him, Laura."

     Nobody assigned problem 1 (Matías raised it) or problems 3, 4, 6 and 7. Jason was not in the conversation; Blake mentioned him only in passing.
  2. **Problem 1, the retro.** Matías said "we had a temperature check on retro, and everyone was yellow". He didn't say the vote was on triage specifically, but the context makes triage the obvious subject.
  3. **Problem 1, the numbers.** Blake asked "is it, like, 100 tickets a week?" and Matías answered "Between 75 and, yeah, 90... 10 per day. Or more". Laura asked whether all of them come through on-call. Matías: "The vast majority are."
  4. **Problem 2, the order of events.** Blake gave the go-ahead *before* Sudarshan's 80% junior-engineer argument, not in response to it. His words: "you are all clear to do some ramping up on aggression of rolling out things we think are gonna improve our speed, knowing that there's a backstop." The 80% figure is a hypothetical bar. Nobody said Workup is at 80%.
  5. **Problem 3.** The transcript reads "around AI and around gastronomy messages". "Guest journey" is a reasonable guess, but it is a guess. Blake gave a soft endorsement right after: "because you're seeing enough accuracy, it can comment back in, mark done, yeah?" Matías: "Yeah."
  6. **The garbled cues** ("Bived from checking World Cup. Ottilie Viola, outputs haven't really measured it."). These are Matías, between the expected-behavior point and the 80% argument. One plausible reading is "based on checking Workup's outputs... haven't really measured it", meaning Matías's accuracy view is anecdotal. Don't quote it. Throughout the transcript, "World Cup" is a mis-transcription of "Workup".
  7. **Problem 6.** Laura said it with a rising, questioning tone: "It has dropped the time to close tickets? For messaging?" Then: "a little hard to measure because of the merging of the teams." Treat it as an unverified claim, not a measured result.

  ### How it maps onto the Workup vs TypeSafe backtest (window 2026-08-20 to 2026-09-18)
  - **52.7% is not the same quantity as Sudarshan's 80%.** The backtest scores Workup's 8-way next-step bucket against 91 human labels (95% CI 43-63%). Sudarshan's 80% is about whether the diagnosis is "mostly correct". A ticket can get the right diagnosis and the wrong bucket. The labels are also anchored, because graders saw Workup's `Next Step:` first (85 of 91 labels came after the declaration), and the labelled subset is not random. The data also predates the improvement Laura reports. Don't put 52.7 next to 80 without saying all of this.
  - **Without no-action tickets, Workup scores 44/70 (63%).** The gap to 80% is concentrated in no-action.
  - **Problem 3 runs straight into Workup's weakest bucket.** Humans said no-action on 21 of 91 (23%), and Workup got 4 of those 21. "Expected behavior, send it back with an explanation" is essentially the no-action / works-as-designed case. Extending auto-close there is the riskiest version of "more aggressive", not the safest. The common failure on those tickets was a confident file-and-line code or config theory with no observed failure on the ticket's own object. That is the opposite of "explain it's expected".
  - **Duplicates support the current auto-close.** Workup got 5 of 8 labelled duplicates in v1. The judge-side check got 10 of 10. The config-change bucket isn't broken out for Workup in the notes, so there's no number for next week's config-change auto-close.
  - **Problem 5 (readability).** The same confident, long gatherer theories are the decoys in the backtest. Making correct output terse may help, but on no-action misses a terse wrong answer is just as wrong.
  - **Problem 6 (measurement).** The backtest has a ready-made measure, agreement of the next-step judge with human labels (production judge 72.4% on 105). It doesn't measure impact, though. Laura's time-to-close needs a comparison that accounts for the team merge, for example per-ticket-type, before vs after.

  ### Possible follow-ups (none done; your call)
  - Send Laura and Sudarshan the no-action caveat (4 of 21) before the expected-behavior expansion, and suggest gating it on the judge's works-as-designed signal or a higher confidence threshold. I haven't drafted anything and posted nothing.
  - Ask Laura for a Workup accuracy number after 2026-09-18, so 52.7% can be replaced with a current figure.

  No external writes were made.

  ## Agent run 2026-10-13T15:06: what prompting shapes Workup's output (problem 5)
  Sources: canary agent-plugins/claude-plugins/investigate (master) and canary-agents origin/main 77eade62 (2026-10-10).

  The comment Workup posts is whatever the agent passes to `submit_diagnosis`. That is free markdown of 40 to 10,000 characters, with the json trailer stripped out before posting (overlord/src/agents/workup/submit-contract.ts, next-step-label.ts). The overlord prompt (`buildInvestigationPrompt` in overlord/src/agents/workup/agent.ts) sets no format at all, only that the diagnosis must be submitted and must end with the trailer.

  The format comes from the investigate plugin:
  - `skills/investigate-ticket/SKILL.md` Step 3 always runs the base `propose-hypothesis`. It never runs `propose-hypothesis-msg`. Steps 2b, 2c and 2d each have their own templates (push-back, duplicate, partial), and Step 4 tells the agent to add one-line notes (code_bug_remapped, judged_duplicate_rejected).
  - `skills/propose-hypothesis/SKILL.md` Step 7 sets the template: next step, then hypotheses with collapsible Effects, Verify and Debate sections, then SMEs, similar issues, recent changes, a cause table covering all 11 categories, admin actions, links and evidence. It sets no length limit. It even requires the empty sections ("Unable to determine", "None found").
  - Step 5 requires an `expected_behavior` hypothesis to carry an `explanation` that is "not a one-liner": thorough, covering the feature's design, the logic and why it is correct. Every hypothesis also gets a 2-sentence `cs_summary`.
  - `skills/propose-hypothesis-msg/SKILL.md` already defines a compact format for messaging: lead with the diagnosis, under 60 lines, ruled-out causes collapsed into one row, empty sections omitted, CS summary last. Nothing in the pipeline calls it. It appears only in the README as a manual command, so messaging tickets get the verbose base format.

  Levers, cheapest first: route MSG tickets to the -msg Step 7, or bring its formatting rules into the base. Give the base template a length target and a BLUF line. Cap the expected_behavior explanation, since it is the bucket Matías wants auto-handled and the place where verbosity hurts most. Check with Dmitry and Laura first, because Dmitry is already on the output format.

  ## Agent run 2026-10-14T13:49: Dmitry's Workup output work
  I found no output-format work by Dmitry Ryzhkov (GitHub dryzhkov-canary).
  - canary: none of his PRs since 2026-09-15 touch agent-plugins/claude-plugins/investigate. His open PRs are scheduler V2 work (MSG-5838, MSG-6545).
  - agents repo: he has no PRs and no commits.
  - Linear: he filed no Workup tickets, and none of the Workup tickets updated in the last 30 days are assigned to him.
  - Slack: no messages from him about format or readability.

  The only Workup item from him is the messaging triage stats for the week of Oct 5, which Matías forwarded to #project-workup on 2026-10-09 (https://canarytechnologies.slack.com/archives/C0AL1T2H43V/p1791551518858509):
  - about 50 tickets, about 15 cleared a day against 12 arriving
  - top issues: AI reply quality ~27%, GJ scheduling/timing ~24%, Booking.com/Expedia ~19%
  - about half resolved during triage
  - "Workup initial investigations: about 50% accurate"

  Laura asked him for detail. He called the 50% "a bit of crude estimate" and posted a breakdown image (https://canarytechnologies.slack.com/archives/C0AL1T2H43V/p1791561456967539), which I couldn't read through the tools. His 50% is roughly consistent with the backtest's 52.7%.

  Conclusion: Matías's "Dmitry is thinking about that" (2026-10-08) has not yet produced a visible artifact. Related: Laura's TOOL-842 (No Action auto-close, shadow first) https://linear.app/canary-technologies/issue/TOOL-842 and TOOL-825 (config auto-close, In Review) https://linear.app/canary-technologies/issue/TOOL-825.

  ## Agent run 2026-10-14T17:47: Workup workstreams (PRs 2026-09-14 to 10-14) vs Linear
  Sources: canary origin/master and open PRs touching agent-plugins/claude-plugins/investigate, backend/canary/linear_agent, canary_mcp, backend/mcp-server; agents repo PRs (gh) in the window. About 150 PRs. Joined against Linear TOOL issues. No external writes.

  ### Workstreams and their Linear projects
  1. Accuracy: declarations, duplicates, auto-close (Laura, ~35 PRs). Project "AI Workup: Accuracy Phase 1-5" (P-TOOL-2140), Implementation, target 2026-10-06 (passed; last update 09-30). Covers TOOL-706/708/709/755/756/757/822/837/839 duplicates auto-close, TOOL-833 No Action declare, TOOL-825 config auto-close (In Review, agents#409 + canary#59747 open), TOOL-842 No Action auto-close (Backlog), TOOL-773 gathering unskippable for Sonnet 5.5 (In Progress, no PR seen).
  2. Investigate plugin pipeline/loop/selection (Laura, Sam, Kevin): TOOL-607/691/692/694/695/705/712/713/715/716/717/724/733/744/745/795. Same project.
  3. run_sql for Workup (Asher, ~30 PRs). "AI Workup: Canary MCP SQL Tool" (P-TOOL-2219), Completed 10-01. Follow-ons TOOL-813 EU/AP enablement (In Review, canary#59133, agents#389) and TOOL-790/797/804/807/815/818 under "Canary MCP: Permissions and Reliability".
  4. Nudge for Info (Sam). "AI Workup: Nudge for Info" (P-TOOL-2236), target 2026-10-16. TOOL-734/736-740 all In Review/In Progress, open PRs agents#400/406/410/412/417/424, canary#59276. TOOL-741 metrics and TOOL-742 turn-on-for-all-teams unassigned Todo.
  5. Handoff reliability and monitoring (Sam, Kevin). "AI Workup: Monitoring" (P-TOOL-2482) holds TOOL-765/823 only. TOOL-609/646/748/751/752/786/824 have no project.
  6. Replay harness and offline evaluation (Laura). TOOL-743 (Done) in Accuracy covers agents#376/381-384; #290/291/292/401 have no ticket.

  ### Work not well tracked in Linear
  - Jason Flax's Workup research stack: agents#232/235/236/237/242/243/244/293/332 (decision capture, isolated local runner, Jeb proposal selection, Jeb shadow eval, regional SQL confinement) and canary drafts #57639/#57644/#57670. All open. No Linear ticket; his Linear is Orbital (ORB-*), none mention Workup. agents#237 overlaps TOOL-813. #332 says "Workup owners still need to discuss storage". This is the Orbital path Blake described on 10-08.
  - canary#59753 "Make the Workup diagnosis report compact" (Laura, open, updated 10-13): 350-word template, from a 1,000-word median; MSG wrapper reuses the base. This is the readability problem from the 10-08 meeting and the lever from run 2. No ticket.
  - Next-step judge and Quality page: agents#408 (score unanswered asks), #207, #375 (Quality page readable). No ticket; "Next-Step Metric" project is Completed (Aug).
  - Model and runtime config: agents#334 (pin Sonnet 5), #335 (price Sonnet 5.5), #394 (deny Workflow/ScheduleWakeup), #202 (sync sub-agent hook). No tickets. "Faster, Cheaper Runs" (P-TOOL-2141) is Planned and untouched since Aug.
  - Routing and handoff tweaks: canary#56391 (missing-info tickets to Workup), #56276 (routed ticket is not its own duplicate), #58172 (Jason, deployment env in handoffs), #59858 (drop shadow selection, open). No tickets.
  - Other teams adding checks and gatherers: Luiza #59257 (cites SDM-5164/5166 only), CT-fgario SDM-5126, Joshua Hart SDM-4981, Ashish PMS-10486/10492, Guido #55360 / AD-8340 (open since 09-03, stale). Tracked in their teams but not linked to any Workup project. "Staged Rollout to Eng-Routed Teams" (P-TOOL-2148) is Planned and untouched since 08-10.
  - Engram eval (Stephanie): agents#245, canary#58938 drafts under FRO-252 / EE-2178 ("Engram Memory v2"). Tracked, but outside Workup.
  - Stale or empty: "Workup Plugin Phase 6" (P-TOOL-2473) has no issues. SEC-809 "Send the /events trigger key" is Backlog, but the work shipped in canary#58516 under TOOL-639. MSG project "Triage: Workup Investigation for Messaging Threads" (P-MSG-2154) is Backlog, target 08-28. Accuracy Phase 1-5 is past its target date.

  ## Agent run 2026-10-15T14:54: handoff doc
  Wrote ~/projects/plans/workup-workstreams-handoff.md so another session can pick this up. It summarizes all four runs, the binding rules, the open follow-ups and how to rerun the PR scan.
project: 2026-09-08-workup
source_id: null
tags: []
time_minutes: 15
title: 'Review Eng Leads 2026-10-08 Workup triage discussion: problems and owners'
updated: 2026-10-15 14:55:21.045454
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