---
area: null
completed_at: null
contexts:
- deep
created: 2026-09-03 22:22:33.141966
defer_until: null
due: 2026-09-08
energy: medium
id: 2026-09-03T2222-laura-will-share-latest-workup-redesign-doc-for-re
order: null
output: "## Review: Unified investigate plugin design (rewritten 2026-09-11)\n\nDoc\
  \ (readable version): https://app.notion.com/p/canarytechnologies/Unified-investigate-plugin-design-readable-version-3bf81468615181e58428e5a18d91433c\n\
  Normative main doc: https://app.notion.com/p/3bf814686151816391a4d784f859afcd\n\
  Judge spec: https://app.notion.com/p/3c28146861518170a05fdbcf46a6f7d2\nOwner: Laura\
  \ DeWald. Status: APPROVED. Linear project: \"AI Workup: Accuracy\" (Internal Tools).\n\
  \n### Verdict\nThe design is smart, but it isn't proven yet. It's well above typical\
  \ agent designs because it's\nbuilt to be measured and corrected rather than trusted.\
  \ Whether it works in practice depends on\nnumbers that don't exist yet, and on\
  \ checks and worked examples that teams haven't written yet.\n\n### What the system\
  \ is\n`investigate` is a Claude Code plugin (canary/agent-plugins/claude-plugins/investigate/)\
  \ that\ndiagnoses Linear tickets. Workup (the production triage agent, in the agents\
  \ repo under overlord)\nruns it on every handoff. The plugin decides what's true\
  \ and what to recommend. The runner decides\nwhat the ticket sees.\n\nPipeline,\
  \ 9 stages: subject \u2192 classify \u2192 resolve \u2192 checks \u2192 branch \u2192\
  \ (loop \u2192 debate) \u2192 report \u2192 telemetry.\n- Classify: a cheap model\
  \ names the problem area (a symptom, never a cause), reading every team's\n  worked\
  \ examples so the investigation isn't limited by which team's board the ticket landed\
  \ on.\n- Resolve: works out the hotel's setup (its integrations and config flags)\
  \ into resolved-context.json.\n- Checks: select.py (plain code, no model) picks\
  \ cheap checks that match; they run in parallel.\n- Branch: an unopposed `observed`\
  \ claim that held at the time of the problem and explains this\n  ticket's symptom\
  \ ends the run early (short-circuit). Missing context sends a push-back to the\n\
  \  reporter. Anything else starts the loop.\n- Loop: works through suspects one\
  \ at a time, running only that suspect's gatherers. The debate\n  (adversarial agents)\
  \ runs only if the loop ends unresolved.\n- Output: hypothesis.json holds the next\
  \ step (one of 8 buckets, the exact object to act on, the\n  owner, a completion\
  \ condition, and what would change its mind). run-summary.json lists what was\n\
  \  left unchecked. tool-traffic.jsonl records every tool call for hermetic replay.\n\
  - Claims: every finding carries a confidence (observed/high/medium/low), an as-of\
  \ time\n  (read_time/event_time), a file citation, a hash and an excerpt.\n- Gate\
  \ (runner-side, before posting): scores the declaration. High posts the full diagnosis\
  \ plus\n  the label. Medium posts what was checked and what wasn't, with no root\
  \ cause asserted. Low posts\n  intake facts only and sends the draft to an internal\
  \ digest.\n- Judge (after resolution): grades the declaration against how the ticket\
  \ actually resolved;\n  \"indeterminate\" is an allowed verdict. The learn loop\
  \ and fleet miner turn misses into proposed\n  new checks.\n- Ownership: Internal\
  \ Tools owns core/, bindings/, scripts/ and the orchestrator. Teams own their\n\
  \  own checks, gatherers, resolvers and worked examples.\n\n### What's smart about\
  \ it\n1. **The output can be graded.** This is the key decision. A structured, cited\
  \ next step can be\n   measured, where prose can't.\n2. **It encodes real debugging\
  \ lessons.** It separates what's true now from what was true at the\n   time (someone\
  \ flips demo mode off mid-incident). A cause can only be ruled out by evidence\n\
  \   covering the ticket's full window, finding nothing isn't proof of absence, and\
  \ a\n   misconfiguration that exists isn't proof it caused this ticket.\n3. **Code\
  \ and model have clear jobs.** select.py picks what runs deterministically; the\
  \ model is\n   used only for judgment. Cheap checks run first and the expensive\
  \ debate runs last.\n4. **The gate never reads the investigator's reasoning.** It\
  \ sees only the evidence and the\n   declaration, so the investigator's own argument\
  \ can't talk it into a high score.\n5. **Replays can't cheat.** The time filter\
  \ refuses data newer than the ticket, so evals can't see\n   the resolution. Many\
  \ teams get this wrong and inflate their accuracy numbers.\n6. **A fault outside\
  \ Canary counts as a result.** That guards against inventing internal causes\n \
  \  for vendor-side problems.\n\n### Where I'm skeptical\n1. **The framework is ahead\
  \ of its content.** Value depends on checks and worked examples that\n   teams are\
  \ meant to write, and most don't exist yet. The doc admits the fast path is\n  \
  \ theoretical: TOOL-608 (messaging config-against-capability) is in Backlog, and\
  \ the PMS instance\n   is unscheduled. That's the classic platform trap.\n2. **The\
  \ confidence levels are the model grading itself.** The hash-and-excerpt check proves\
  \ the\n   cited file contains the quoted text, not that the text supports the claim.\
  \ Catching a wrong\n   `observed` claim is the gate's job, and the gate isn't built\
  \ yet.\n3. **The ground truth is weak.** Linear resolutions are sparse and most\
  \ config changes leave no\n   trace. If most judge verdicts come back \"indeterminate\"\
  , the feedback loop that justifies the\n   whole thing is thin.\n4. **The safety\
  \ step is shipping after the thing it guards.** Next Step labels have posted\n \
  \  unscored since 2026-08-24, and the gate in shadow (TOOL-654) is still Todo. It\
  \ should probably\n   land before the 2.0.0 cut (TOOL-652).\n5. **Privacy.** TOOL-583\
  \ persists full tool outputs (64KB cap each) indefinitely, while redaction\n   and\
  \ retention are still listed as open questions. Outputs carry guest PII that the\n\
  \   already-stored inputs mostly didn't, so this widens what's exposed.\n6. **Pace\
  \ and concentration.** Phases 2 through 4 landed in about two weeks, nearly all\
  \ by one\n   person. That's great execution, but review is probably shallow, the\
  \ bus factor is one, and the\n   \"teams own their checks\" model hasn't been tested.\n\
  \n### Numbers that would settle whether it works\n- Short-circuit rate on real tickets:\
  \ how often a run ends early on a direct observation.\n- Gate-vs-judge agreement:\
  \ whether the pre-post score predicts the later grade.\n- Judge \"indeterminate\"\
  \ rate: what share of verdicts can't be decided.\n- Number of team-authored checks:\
  \ ones Internal Tools didn't write.\nIf these look good in a couple of months, it's\
  \ a genuinely good system. If they don't, it's\nwell-built machinery with little\
  \ running through it.\n\n### Doc accuracy: the status sections are stale\nThe header\
  \ still says \"v1.2.0 on trunk\" and the Order-of-work table says phase 2 is in\
  \ progress\nand phases 3a through 6 haven't started. Actual state as of 2026-09-11:\n\
  - **Version:** the plugin on master is v1.9.0. core/, bindings/ and scripts/select.py\
  \ all exist.\n- **Phase 2:** done. TOOL-568 (https://linear.app/canary-technologies/issue/TOOL-568)\
  \ and TOOL-569\n  (https://linear.app/canary-technologies/issue/TOOL-569) merged\
  \ 2026-08-28.\n- **Phase 3a:** done. TOOL-591 (claim schema) and TOOL-594 (gatherers\
  \ emit claims), 2026-08-31.\n- **Phase 3b:** done. TOOL-592 (resolve hotel setup),\
  \ TOOL-593 (tool traffic) and TOOL-595\n  (select.py), 2026-08-31.\n- **Out-of-table\
  \ items:** done. TOOL-583 (https://linear.app/canary-technologies/issue/TOOL-583,\n\
  \  agents PR https://github.com/canary-technologies-corp/agents/pull/164) and TOOL-584\n\
  \  (https://linear.app/canary-technologies/issue/TOOL-584, canary PR\n  https://github.com/canary-technologies-corp/canary/pull/54769).\n\
  - **Phase 4:** about half done.\n  - Done: TOOL-602 (scaffolders), TOOL-603 (checks\
  \ through select.py), TOOL-604 (shadow\n    classification), TOOL-605 (push-back\
  \ fixes), TOOL-606 (branch stage), TOOL-648 (config\n    authority, https://linear.app/canary-technologies/issue/TOOL-648)\
  \ and TOOL-653 (persist cited\n    evidence at post time).\n  - Open: TOOL-649 (first\
  \ config resolver), TOOL-650 (check-common-log-trace), TOOL-651 (CI lint\n    gap),\
  \ TOOL-652 (2.0.0 cut), TOOL-654 (gate in shadow), TOOL-607 (selection goes live)\
  \ and\n    TOOL-608 (messaging config check).\n- **Phase 6:** TOOL-599 (remove -devin\
  \ variants) already shipped early, 2026-09-03.\n\nThe config-authority open question\
  \ is now resolved in the doc (TOOL-648). PMS uses the stored\ncolumn. For messaging,\
  \ the send-time snapshot is the event_time authority and the stored spec the\nread_time\
  \ authority, and a disagreement between them is reported.\n\n### Notion comment\
  \ threads\n8 open, 5 resolved. The Ian Clark and Blake Vanlandingham threads on\
  \ classification, short-circuit\nand the learn loop were answered and the doc updated.\
  \ Arihant Daga's \"how does the judge know\nbetter\" was answered by Laura. Blake's\
  \ \"Claude estimates or our estimates?\" is stale: it's anchored\nto an \"Est.\"\
  \ column that no longer exists, so it could be resolved.\n\n### Draft reply to Laura\
  \ (NOT sent)\n\"Read the latest readable version. The design is strong, especially\
  \ that the output is gradable,\nthe read_time/event_time split, and the gate never\
  \ seeing the transcript. The TOOL-648 ruling is\nclean. A few things: (1) the header\
  \ (v1.2.0) and Order-of-work Status column are about two phases\nbehind; master\
  \ is at 1.9.0 with 2/3a/3b done and 4 half done. (2) Labels have been posting\n\
  ungated since 08-24; should TOOL-654 land before the 2.0.0 cut? (3) TOOL-583 persists\
  \ full tool\noutputs indefinitely while redaction is still an open question. Outputs\
  \ carry guest data, so is a\nredaction pass or retention cap worth pulling forward?\
  \ (4) Has any production run short-circuited\nyet, and what are you seeing for the\
  \ judge's indeterminate rate? That's the number I'd watch to\nknow whether the feedback\
  \ loop has enough signal.\"\n\nNo external writes were made (no Notion, Slack or\
  \ Linear), and nothing touched Salesforce.\n"
project: 2026-09-08-workup
source_id: null
tags: []
time_minutes: 15
title: laura will share latest Workup redesign doc for review
updated: 2026-09-11 15:30:34.925376
waiting_on: null
waiting_since: null
working_on: false
---

https://app.notion.com/p/canarytechnologies/Unified-investigate-plugin-design-readable-version-3bf81468615181e58428e5a18d91433c?source=copy_link