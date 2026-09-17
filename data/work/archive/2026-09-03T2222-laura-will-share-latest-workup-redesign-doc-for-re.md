---
area: null
completed_at: 2026-09-17 12:26:40.012958
contexts:
- deep
created: 2026-09-03 22:22:33.141966
defer_until: null
due: 2026-09-08
energy: medium
id: 2026-09-03T2222-laura-will-share-latest-workup-redesign-doc-for-re
order: null
output: |
  ## Review: Unified investigate plugin design (rewritten 2026-09-11)

  Doc (readable version): https://app.notion.com/p/canarytechnologies/Unified-investigate-plugin-design-readable-version-3bf81468615181e58428e5a18d91433c
  Normative main doc: https://app.notion.com/p/3bf814686151816391a4d784f859afcd
  Judge spec: https://app.notion.com/p/3c28146861518170a05fdbcf46a6f7d2
  Owner: Laura DeWald. Status: APPROVED. Linear project: "AI Workup: Accuracy" (Internal Tools).

  ### Verdict
  The design is smart, but it isn't proven yet. It's well above typical agent designs because it's
  built to be measured and corrected rather than trusted. Whether it works in practice depends on
  numbers that don't exist yet, and on checks and worked examples that teams haven't written yet.

  ### What the system is
  `investigate` is a Claude Code plugin (canary/agent-plugins/claude-plugins/investigate/) that
  diagnoses Linear tickets. Workup (the production triage agent, in the agents repo under overlord)
  runs it on every handoff. The plugin decides what's true and what to recommend. The runner decides
  what the ticket sees.

  Pipeline, 9 stages: subject → classify → resolve → checks → branch → (loop → debate) → report → telemetry.
  - Classify: a cheap model names the problem area (a symptom, never a cause), reading every team's
    worked examples so the investigation isn't limited by which team's board the ticket landed on.
  - Resolve: works out the hotel's setup (its integrations and config flags) into resolved-context.json.
  - Checks: select.py (plain code, no model) picks cheap checks that match; they run in parallel.
  - Branch: an unopposed `observed` claim that held at the time of the problem and explains this
    ticket's symptom ends the run early (short-circuit). Missing context sends a push-back to the
    reporter. Anything else starts the loop.
  - Loop: works through suspects one at a time, running only that suspect's gatherers. The debate
    (adversarial agents) runs only if the loop ends unresolved.
  - Output: hypothesis.json holds the next step (one of 8 buckets, the exact object to act on, the
    owner, a completion condition, and what would change its mind). run-summary.json lists what was
    left unchecked. tool-traffic.jsonl records every tool call for hermetic replay.
  - Claims: every finding carries a confidence (observed/high/medium/low), an as-of time
    (read_time/event_time), a file citation, a hash and an excerpt.
  - Gate (runner-side, before posting): scores the declaration. High posts the full diagnosis plus
    the label. Medium posts what was checked and what wasn't, with no root cause asserted. Low posts
    intake facts only and sends the draft to an internal digest.
  - Judge (after resolution): grades the declaration against how the ticket actually resolved;
    "indeterminate" is an allowed verdict. The learn loop and fleet miner turn misses into proposed
    new checks.
  - Ownership: Internal Tools owns core/, bindings/, scripts/ and the orchestrator. Teams own their
    own checks, gatherers, resolvers and worked examples.

  ### What's smart about it
  1. **The output can be graded.** This is the key decision. A structured, cited next step can be
     measured, where prose can't.
  2. **It encodes real debugging lessons.** It separates what's true now from what was true at the
     time (someone flips demo mode off mid-incident). A cause can only be ruled out by evidence
     covering the ticket's full window, finding nothing isn't proof of absence, and a
     misconfiguration that exists isn't proof it caused this ticket.
  3. **Code and model have clear jobs.** select.py picks what runs deterministically; the model is
     used only for judgment. Cheap checks run first and the expensive debate runs last.
  4. **The gate never reads the investigator's reasoning.** It sees only the evidence and the
     declaration, so the investigator's own argument can't talk it into a high score.
  5. **Replays can't cheat.** The time filter refuses data newer than the ticket, so evals can't see
     the resolution. Many teams get this wrong and inflate their accuracy numbers.
  6. **A fault outside Canary counts as a result.** That guards against inventing internal causes
     for vendor-side problems.

  ### Where I'm skeptical
  1. **The framework is ahead of its content.** Value depends on checks and worked examples that
     teams are meant to write, and most don't exist yet. The doc admits the fast path is
     theoretical: TOOL-608 (messaging config-against-capability) is in Backlog, and the PMS instance
     is unscheduled. That's the classic platform trap.
  2. **The confidence levels are the model grading itself.** The hash-and-excerpt check proves the
     cited file contains the quoted text, not that the text supports the claim. Catching a wrong
     `observed` claim is the gate's job, and the gate isn't built yet.
  3. **The ground truth is weak.** Linear resolutions are sparse and most config changes leave no
     trace. If most judge verdicts come back "indeterminate", the feedback loop that justifies the
     whole thing is thin.
  4. **The safety step is shipping after the thing it guards.** Next Step labels have posted
     unscored since 2026-08-24, and the gate in shadow (TOOL-654) is still Todo. It should probably
     land before the 2.0.0 cut (TOOL-652).
  5. **Privacy.** TOOL-583 persists full tool outputs (64KB cap each) indefinitely, while redaction
     and retention are still listed as open questions. Outputs carry guest PII that the
     already-stored inputs mostly didn't, so this widens what's exposed.
  6. **Pace and concentration.** Phases 2 through 4 landed in about two weeks, nearly all by one
     person. That's great execution, but review is probably shallow, the bus factor is one, and the
     "teams own their checks" model hasn't been tested.

  ### Numbers that would settle whether it works
  - Short-circuit rate on real tickets: how often a run ends early on a direct observation.
  - Gate-vs-judge agreement: whether the pre-post score predicts the later grade.
  - Judge "indeterminate" rate: what share of verdicts can't be decided.
  - Number of team-authored checks: ones Internal Tools didn't write.
  If these look good in a couple of months, it's a genuinely good system. If they don't, it's
  well-built machinery with little running through it.

  ### Doc accuracy: the status sections are stale
  The header still says "v1.2.0 on trunk" and the Order-of-work table says phase 2 is in progress
  and phases 3a through 6 haven't started. Actual state as of 2026-09-11:
  - **Version:** the plugin on master is v1.9.0. core/, bindings/ and scripts/select.py all exist.
  - **Phase 2:** done. TOOL-568 (https://linear.app/canary-technologies/issue/TOOL-568) and TOOL-569
    (https://linear.app/canary-technologies/issue/TOOL-569) merged 2026-08-28.
  - **Phase 3a:** done. TOOL-591 (claim schema) and TOOL-594 (gatherers emit claims), 2026-08-31.
  - **Phase 3b:** done. TOOL-592 (resolve hotel setup), TOOL-593 (tool traffic) and TOOL-595
    (select.py), 2026-08-31.
  - **Out-of-table items:** done. TOOL-583 (https://linear.app/canary-technologies/issue/TOOL-583,
    agents PR https://github.com/canary-technologies-corp/agents/pull/164) and TOOL-584
    (https://linear.app/canary-technologies/issue/TOOL-584, canary PR
    https://github.com/canary-technologies-corp/canary/pull/54769).
  - **Phase 4:** about half done.
    - Done: TOOL-602 (scaffolders), TOOL-603 (checks through select.py), TOOL-604 (shadow
      classification), TOOL-605 (push-back fixes), TOOL-606 (branch stage), TOOL-648 (config
      authority, https://linear.app/canary-technologies/issue/TOOL-648) and TOOL-653 (persist cited
      evidence at post time).
    - Open: TOOL-649 (first config resolver), TOOL-650 (check-common-log-trace), TOOL-651 (CI lint
      gap), TOOL-652 (2.0.0 cut), TOOL-654 (gate in shadow), TOOL-607 (selection goes live) and
      TOOL-608 (messaging config check).
  - **Phase 6:** TOOL-599 (remove -devin variants) already shipped early, 2026-09-03.

  The config-authority open question is now resolved in the doc (TOOL-648). PMS uses the stored
  column. For messaging, the send-time snapshot is the event_time authority and the stored spec the
  read_time authority, and a disagreement between them is reported.

  ### Notion comment threads
  8 open, 5 resolved. The Ian Clark and Blake Vanlandingham threads on classification, short-circuit
  and the learn loop were answered and the doc updated. Arihant Daga's "how does the judge know
  better" was answered by Laura. Blake's "Claude estimates or our estimates?" is stale: it's anchored
  to an "Est." column that no longer exists, so it could be resolved.

  ### Draft reply to Laura (NOT sent)
  "Read the latest readable version. The design is strong, especially that the output is gradable,
  the read_time/event_time split, and the gate never seeing the transcript. The TOOL-648 ruling is
  clean. A few things: (1) the header (v1.2.0) and Order-of-work Status column are about two phases
  behind; master is at 1.9.0 with 2/3a/3b done and 4 half done. (2) Labels have been posting
  ungated since 08-24; should TOOL-654 land before the 2.0.0 cut? (3) TOOL-583 persists full tool
  outputs indefinitely while redaction is still an open question. Outputs carry guest data, so is a
  redaction pass or retention cap worth pulling forward? (4) Has any production run short-circuited
  yet, and what are you seeing for the judge's indeterminate rate? That's the number I'd watch to
  know whether the feedback loop has enough signal."

  No external writes were made (no Notion, Slack or Linear), and nothing touched Salesforce.

  ## Agent run 2026-09-16T09:30:00+01:00

  Follow-up asked: "Summarize the proposal and what's already been done"

  ### The proposal in one paragraph
  Replace Workup's freeform diagnosis with a measurable pipeline. The `investigate` Claude Code
  plugin (canary/agent-plugins/claude-plugins/investigate/) diagnoses a Linear ticket in nine
  stages: subject -> classify -> resolve -> checks -> branch -> (loop -> debate) -> report ->
  telemetry. Cheap deterministic checks run first, a suspect-by-suspect loop runs only if needed,
  and the adversarial debate runs last and only if the loop ends unresolved. Every finding is a
  claim with a confidence level (observed/high/medium/low), an as-of time (read_time vs
  event_time), and a cited, hashed file excerpt. The output is a structured next step
  (hypothesis.json) plus a list of what went unchecked (run-summary.json), so it can be graded.
  Workup (in the agents repo, overlord) is the runner: a gate scores the declaration before
  posting and decides how much the ticket sees, and a judge grades it against the real
  resolution afterwards. Misses feed a learn loop that proposes new checks. Internal Tools owns
  the framework; product teams own their checks, gatherers, resolvers and worked examples.

  Docs: readable version
  https://app.notion.com/p/canarytechnologies/Unified-investigate-plugin-design-readable-version-3bf81468615181e58428e5a18d91433c
  , normative doc https://app.notion.com/p/3bf814686151816391a4d784f859afcd , judge spec
  https://app.notion.com/p/3c28146861518170a05fdbcf46a6f7d2 . Owner Laura DeWald, status
  APPROVED. Linear project "AI Workup: Accuracy".

  ### What's already done (as of 2026-09-16)
  Plugin on master is v1.9.0. Roughly phases 2, 3a, 3b are complete and phase 4 is past half.
  - Phase 2, framework split (done 08-28): harness-agnostic core/ plus one bindings file
    (TOOL-568), problem-area vocabulary and domains directory (TOOL-569).
  - Phase 3a, claims (done 08-31): claim schema and evidence rules (TOOL-591), gatherers emit
    claims (TOOL-594).
  - Phase 3b, context and selection (done 08-31): resolve hotel setup (TOOL-592), tool-traffic
    recording for hermetic replay (TOOL-593), select.py picks what runs (TOOL-595).
  - Runner-side persistence (done 08-28 / 09-09): full tool outputs stored (TOOL-583,
    https://github.com/canary-technologies-corp/agents/pull/164), claim-cited evidence stored
    at post time (TOOL-653). First hotel-level checks for demo mode and disabled messaging
    (TOOL-584, https://github.com/canary-technologies-corp/canary/pull/54769).
  - Phase 4 so far: scaffolders (TOOL-602), checks routed through select.py (TOOL-603), shadow
    classification (TOOL-604), push-back misfire fixes (TOOL-605), branch stage (TOOL-606),
    config-authority ruling (TOOL-648: PMS uses the stored column; messaging uses the send-time
    snapshot for event_time and the stored spec for read_time).
  - New since the 09-11 review: pipeline.py puts the orchestrator's closed-form steps in code
    (TOOL-691, done 09-15,
    https://linear.app/canary-technologies/issue/TOOL-691); gather-context accepts an explicit
    gatherer list (TOOL-694, done 09-16, Sam Kariu); Workup reads the Zendesk conversation
    rather than just attachments (TOOL-655, done 09-15); comms-checks port follow-ups
    (TOOL-690, done 09-14). Sam Kariu is now a second contributor, which softens the
    bus-factor concern from the earlier review.
  - Phase 6 item shipped early: -devin variants removed (TOOL-599, 09-03).

  ### What's still open
  - In review: classify-area always gets ticket prose and emits event_ts (TOOL-695,
    https://linear.app/canary-technologies/issue/TOOL-695).
  - Todo: first configuration resolver (TOOL-649), check-common-log-trace (TOOL-650), CI lint
    gap (TOOL-651), the 2.0.0 cut (TOOL-652), posting gate in shadow (TOOL-654,
    https://linear.app/canary-technologies/issue/TOOL-654).
  - Backlog: selection goes live (TOOL-607), messaging config-against-capability check
    (TOOL-608), the loop (TOOL-692), termination conditions and debate gating (TOOL-693),
    Workup prompt trimmed to runner concerns (TOOL-696), hotel agent_context messaging
    section (TOOL-596).
  - So the pipeline stages that exist in code today are subject, classify, resolve, checks and
    branch. The loop, debate gating and the gate are still unbuilt, and labels have posted
    ungated since 08-24. The earlier review's ask that TOOL-654 land before the 2.0.0 cut still
    stands.

  No external writes were made (no Notion, Slack or Linear), and nothing touched Salesforce.
project: 2026-09-08-workup
source_id: null
tags: []
time_minutes: 15
title: laura will share latest Workup redesign doc for review
updated: 2026-09-17 12:26:40.012944
waiting_on: null
waiting_since: null
working_on: false
---

https://app.notion.com/p/canarytechnologies/Unified-investigate-plugin-design-readable-version-3bf81468615181e58428e5a18d91433c?source=copy_link