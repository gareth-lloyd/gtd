---
area: null
completed_at: null
contexts: []
created: 2026-11-16 15:13:59.942607
defer_until: null
due: null
energy: low
id: 2026-11-16T1513-connect-with-jason-on-status-of-orbital-workup
order: null
output: |
  ## Agent run 2026-11-17T14:41

  Jason = Jason Flax (GitHub `jsflax`). Nothing was sent or posted; this is research only.

  ### Answer: yes, he is considering structural changes
  He said so in the Agentic dev workstream sync on 2026-11-16 (the page is titled 17 Nov):
  https://app.notion.com/p/41a81468615180af896eefc1e8c70605
  The transcript there has unlabelled speakers; I read speaker "D" as Jason from context.

  - He ran 108 Workup simulations on Orbital, "almost done". The delay was Orbital bugs found during the run.
  - Finding so far: simple tickets do not need today's 3-agent setup, one top model gives the same result. Complex tickets would get a multi-model swarm (he named GLM 5.3 plus a swarm of Haikus).
  - He wants a design discussion "very soon" on what the new structure on Orbital should be.
  - He rebuilt Laura's eval suite to run on Orbital and asked for someone to peer review it "to make sure I'm not cheating". No owner was named.
  - His view of the end state: engineering hands the tools to Stephanie's team, who then own discovery and improvement.

  ### Status and dates
  - Workup has NOT moved to Orbital. Blake said the same in Blake directs on 2026-11-16 ("right at the precipice").
  - Plan from the sync: study results shared by Wed 2026-11-18; design agreed this week; Workup runs on Orbital in parallel with Overlord (mock Linear) for 2 weeks; then review and switch. So the earliest switch decision is early December.
  - This has slipped once: on 2026-10-20 he said "replicating workup's flow over the next 2 weeks, then productionizing it" (https://canarytechnologies.slack.com/archives/C0AR52PPU4Q/p1792499895785949).
  - Notion monthly goal "Orbital", November: "usable by engineers and workup pilot success", status Not started (https://app.notion.com/p/4078146861518029af7cc7df173eac9e).
  - He told the sync he would rather push it through alone for now; Daga goes back to other work.

  ### What exists in code
  - Orbital repo has a `canary-workup` template in `Sources/OrbitalData/SwarmTemplates.swift`: one investigator seat, no referee, and a schema-bounded `diagnosis` artifact whose commit ends the run. The comment calls it "the Overlord workup agent's Orbital mount". This is the single-agent shape, already built.
  - A `workup-migration` starter in `Documentation/BuiltinRoomCatalog.md` (September): one Workup owner, sequential checks, human-reviewed diagnosis, "no production parity claim".
  - I could not find the study, its results, or the rebuilt eval suite in any PR, branch name, Slack post, Notion page, or Linear ticket. Branches named `*workup*` in Orbital are platform fixes (plugin sources, run-input isolation), not the eval.

  ### His recent PRs
  - Since 2026-11-01: 228 PRs in `canary-technologies-corp/Orbital` (85 merged, 137 open, 6 closed), plus about a dozen in `agents`. Nothing in `canary`.
  - All of it is platform work: startup and MCP bounds, perf on queries, roster/template fixes, Orb shell and skins, organisation schedules, Atlas context service (agents #586 https://github.com/canary-technologies-corp/agents/pull/586).
  - None of his PRs change Workup's current pipeline. Those changes are Sam Kariu's and Kevin Cormier's, e.g. TOOL-773 (https://linear.app/canary-technologies/issue/TOOL-773) and canary #65295 (https://github.com/canary-technologies-corp/canary/pull/65295).

  ### Linear
  - No ticket or project for "Workup on Orbital". His Orbital tickets (EE-2131 etc.) were last touched 2026-10-20.
  - Related: EE-2998 Move Orbital and Nest to the agents cluster, Triage (https://linear.app/canary-technologies/issue/EE-2998); TOOL-938 run the investigate resolvers in one forked sub-agent, Backlog, Laura's (https://linear.app/canary-technologies/issue/TOOL-938); ENT-7186 Align with Internal Tools on Workup vs Golem, Backlog (https://linear.app/canary-technologies/issue/ENT-7186).

  ### My read (inference, not something Jason said)
  - His changes are about orchestration shape and model choice. Nothing I found touches the next-step taxonomy, the judge, or the "does Canary act / who acts" errors from your accuracy audits. Those would carry over unchanged unless someone raises them in the design discussion this week.
  - His study is scored by a rebuilt eval that nobody has reviewed yet. The Workup Improvement Plan (https://app.notion.com/p/4188146861518179847fd617300bd320) warns that next-step gains against the judge alone can be judge noise, so "same results" for the single model needs that check.
  - You told Blake on 11-16 that the Orbital move is a good time to rethink architecture and to lean on Jason for it. The two open slots where you could plug in are the eval peer review and the design discussion.

  ### Not covered
  - Private Slack channels and DMs were not searched (needs your OK).
  - I did not open the Orbital repo beyond the files above, so the eval may live somewhere I did not look.

  ### Draft DM to Jason (not sent)
  > Hey Jason, I saw the notes from Monday's agents sync. Two things on Workup on Orbital: (1) can I see the study results when you share them Wednesday, and join the design discussion on the new structure? (2) I'm happy to peer review the rebuilt eval suite. Laura and I spent October auditing where the judge and the next-step labels go wrong, and I'd like to make sure those findings feed into the design. Where does the eval code live?
project: null
source_id: null
tags: []
time_minutes: 5
title: connect with Jason on status of orbital/workup
updated: 2026-11-17 14:41:30.000000
waiting_on: null
waiting_since: null
working_on: false
---

Is he considering architectural/structural changes to workup?

Start with linear, slack and notion searches. 

Review recent PRs from Jason across any accessible repository