---
area: null
completed_at: null
contexts: []
created: 2026-09-01 17:16:41.175964
defer_until: null
due: 2026-09-02
energy: low
id: 2026-09-01T1716-i-need-to-be-more-on-top-of-workup-i-m-behind-the
order: null
output: |
  ## Agent run 2026-09-02T14:30:00+03:00

  ### Headline
  The next Workup Agent Sync is TODAY 2026-09-02 18:30 EEST (08:30 PDT), you accepted, and the agenda for today is still empty (https://app.notion.com/p/3c281468615181a1a88fca0b5fea0b94). Laura's calendar replies say "out of office" for the 9/9 and 9/16 syncs, so today may be the last full sync with her for two weeks. Do Phase 0 below before 18:30.

  ### Where Workup stands (3-week catch-up in one screen)
  - What it is: production triage agent, runs on every Oncall handoff for MSG, CC and PMS tickets (not ENT), posts findings and declares one of 8 "next step" buckets which a judge grades against how the ticket resolved. Linear initiative (owner Laura): https://linear.app/canary-technologies/initiative/workup-2a7616f589a4. Dashboard: https://agents.cnry.land/workup. Bot page: https://agents.cnry.land/bots/workup.
  - Numbers (Laura, 26 Aug): 107 investigations across 14 teams in 14 days (MSG 30, PMS 18, INT 16, CC 14); ~$95/day (~$2.5-3k/month); ~1 run in 4 posts nothing; 12 runs hit the $30 cap, all dying in the multi-agent debate inside propose-hypothesis. First 28 next-step labels skewed code-fix 10 / ops-action 8 (Blake's read that it favours code change over config change is supported).
  - Decisions 26 Aug (doc you declined: https://docs.google.com/document/d/19XTmIdZfr7jU1cMNlcwoFRBLJFnIz3qibO4LwviTtxA/edit): no cost optimisation / model switching until new prompting lands; SQL tool uses Django raw SQL path, NOT direct DB from MCP server; deny-list of sensitive fields + cheap LLM (Luna) query gate; semicolons blocked; payment/HR/mobile-key gateways must stay queryable.
  - Decisions 12 Aug (https://docs.google.com/document/d/1kUbxDiMWronnnOD4AAq5cRVF_k6NvTPHvtnyJcJBXw4/edit): Canary MCP handed from Applied AI to Internal Tools; raw SQL for querying, ORM only for specific MCP tools; investigate skills migrate to MCP; PMS Gateway auth via user email; "next step" metric adopted; SQL tool is priority #2. Open: Teleport -> Pomerium status.
  - 5 Aug Triage Agent Sync (you were not invited then; https://docs.google.com/document/d/1pR_vFnbnykKd2v2vU9KVloIbG3ooAT1pCtiYngPp5xI/edit): audit logging + SIEM over obfuscation, restrict internet for headless agents with PII, Ingram/engram memory layer, Slack notifications for missing-info tickets.
  - Incident: engram memory nudge broke Workup posting ~13 Aug; memory flag turned OFF for Workup; fix is agents PR #132 (Jason, still OPEN: https://github.com/canary-technologies-corp/agents/pull/132) which also adds a mechanical submit_diagnosis contract. Thread: https://canarytechnologies.slack.com/archives/C0AR52PPU4Q/p1786566370592719
  - Shipped since 20 Aug (Laura, agents repo #141-#178, canary #53790/#54769/#54796/#54880/#54960): next-step labels + judge (pass A from Linear records, pass B LLM), dashboard rebuilt around next-step correctness, tool-mix and full tool-output capture, EU/AP handoff live, plugin core/bindings split, gatherers emit claims, hotel-level demo-mode / messaging-disabled checks, handoff crash fix (TOOL-597).
  - Project states: Accuracy = Implementation (https://linear.app/canary-technologies/project/ai-workup-accuracy-1bfe6e72996f); Canary MCP SQL Tool = Eng Design, lead Asher, project due 4 Sep (https://linear.app/canary-technologies/project/ai-workup-canary-mcp-sql-tool-72b25204de08); Interactive Investigations = Paused; Staged Rollout to Eng-Routed Teams = Planned, paused, "revisit ~Q4A" (https://linear.app/canary-technologies/project/ai-workup-staged-rollout-to-eng-routed-teams-7ca5cf153530); Team Enablement via KB = Planned; Faster/Cheaper Runs = Planned; Model Benchmark = Canceled (28 Aug); Next-Step Metric = Completed.

  ### Open threads right now (things people are waiting on)
  - SQL tool eng design awaiting review from Blake and Bernard since 27 Aug (TOOL-562 In Review: https://linear.app/canary-technologies/issue/TOOL-562). Doc: https://app.notion.com/p/3c8814686151808c8231f5997b870632. Requirements: https://app.notion.com/p/3c281468615180a6a89bc4b5b99a60dc. Seed blocklist draft: https://app.notion.com/p/3c681468615180f086b6f72a998f4a08. psycopg3 in backend/canary was CANCELED (TOOL-563; PR #54236 closed).
  - Team onboarding asks with no owner/answer: Joao Bueno (Tipping) asked "how do I onboard workup in my team" this morning (https://canarytechnologies.slack.com/archives/C0AL1T2H43V/p1788303495256679); Luiza (SDM) opened gatherer PR #54261 (https://github.com/canary-technologies-corp/canary/pull/54261) awaiting review. The Staged Rollout project that would answer this is paused.
  - Zendesk access missing in Workup sandboxes (Joshua Hart, https://canarytechnologies.slack.com/archives/C0AL1T2H43V/p1787839053048349); TOOL-581 + agents PR #179 (open, https://github.com/canary-technologies-corp/agents/pull/179).
  - Triage backlog on Internal Tools: TOOL-598 handoff failures should fall back to a comment; TOOL-609 include Groundcover links; TOOL-605 push-back misfire fixes (High, backlog).
  - Cost: Overlord cap $30 for workup (VOICEQUALITY_OVERLORD_MAX_COST_USD pattern in secrets); "already had one Golem/workup outage this week" (Laura, 27 Aug, https://canarytechnologies.slack.com/archives/C0AR52PPU4Q/p1787860715971269).

  ### Why you specifically need to be on top of it (evidence)
  - Ryan Rogers 1-1, 12 Aug: right under "Golem elevator pitch - great work" is "Be aware of workup. This..." (Bear note "Ryan Rogers", id EE569735-3FF3-470F-9BC2-80EF7E1FC060; the rest of the sentence is truncated in search, open it in Bear).
  - Golem's verdict rubric is already mapped onto the Workup judge (agent-plugins/claude-plugins/enterprise/docs/golem-verdict-rubric.md, "Workup judge mapping", ENT-7182) "so Golem runs can surface on agents.cnry.land later". ENT is the one eng-routed team with its own investigation agent; every other team is either on Workup or asking to be.
  - Your 5 Aug Enterprise block plan opens with "carve out more time and reduce IC frustration with Triage" (Bear "Enterprise"). Blake's note that Mattie found CSA-routing issues via Workup is "the exact problem space" (Bear "Blake Van Landingham").
  - You are on the sync as optional and were struck through on 26 Aug. Blake, Dylan, Julius, Garrett, Stephanie are the regulars.

  ### Catch-up investigation plan
  Phase 0 - before today's 18:30 sync (45 min)
  1. Read the initiative page and the 26 Aug agenda "Updates" block (links above). 10 min.
  2. Open agents.cnry.land/workup: note next-step correctness %, no-post rate, cap-kill count for the last 7 days vs the 26 Aug numbers. 10 min.
  3. Open Bear "Ryan Rogers" and read the full "Be aware of workup" line. 2 min.
  4. Add 1-2 discussion topics to today's agenda page (Discussion Topics list is empty). Candidates below. 5 min.
  5. Decide your stance on the ENT question (see Phase 3) enough to say one sentence about it if asked.

  Phase 1 - deep read of the design surface (2 h, this week)
  1. Unified investigate plugin design, normative (https://app.notion.com/p/3bf814686151816391a4d784f859afcd) and readable (https://app.notion.com/p/3bf81468615181e58428e5a18d91433c). This is the "new prompting" everyone is waiting on; it replaces the debate stage that burns the $30.
  2. Canary MCP SQL Tool eng design + requirements + blocklist (links above). Review with the PMS/enterprise lens: which payment/PMS/gateway tables must stay queryable, which enterprise-specific fields (SSO org secrets, onboarding scripts, credential-manager) must be denied. Blake asked for reviewers; you have standing here.
  3. PRD Interactive Investigations (https://app.notion.com/p/3b9814686151818b9e09f189f1499888): 30% of runs ask the reporter, 2% get a reply. Compare with Golem's missing-info behaviour.
  4. Next Step metric doc (https://app.notion.com/p/3b38146861518008b312fa94262e4ef4) and the Workup overview (https://app.notion.com/p/3b281468615181abab24cc07d8889847).
  5. Q3A Internal Tools planning notes, Workup section only (https://app.notion.com/p/38f81468615180b7abf6c50c43271dc6).

  Phase 2 - ground truth from runs (1.5 h)
  1. Linear view next-step-tickets (https://linear.app/canary-technologies/view/next-step-tickets-69f507a962f4): pick 5 PMS tickets with labels, read the Workup comment vs the actual resolution. Score them yourself using the Golem rubric so you can compare the two agents on like-for-like tickets.
  2. Pick 2 of the cap-killed runs (e.g. PMS-10139 https://linear.app/canary-technologies/issue/PMS-10139) and read the sandbox transcript on agents.cnry.land/sandboxes to see where the money goes.
  3. Pull Golem verdict rates via /enterprise:golem-metrics for the same window and put the two numbers side by side (accuracy, cost per correct diagnosis, no-post rate).

  Phase 3 - strategic questions to answer for the Strategy project (write up as a Bear note "Workup catch-up 2026-09")
  1. Should ENT move onto Workup, contribute an ENT gatherer, or keep Golem as a separate agent? What would we lose (enterprise KB playbook, DB-script mode, misroute detection) and what would we gain (shared judge, dashboard, SQL tool, EU/AP)?
  2. Who owns team onboarding now that Staged Rollout is paused? SDM and Tipping are self-serving via gatherer PRs with nobody reviewing. Is that the intended path (Team Enablement via KB) or drift?
  3. Cost governance: is $3k/month + 25% no-post acceptable to Blake beyond this block, and what is the trigger to revisit the cap policy after the unified plugin lands?
  4. Coverage risk: Laura is the only committer on ~30 PRs in 2 weeks and appears OOO for the next two syncs. Who runs the sync, reviews SDM/Tipping PRs and deploys the judge/prompting while she is out?
  5. Security posture of the SQL tool from an enterprise-customer standpoint (PII, PCI fields, credential-manager) - is a deny-list + LLM gate defensible in a customer security questionnaire?

  Phase 4 - close the loop
  1. 1-1 with Laura: ask for the 12 Aug handoff doc from Applied AI and whether she wants an ENT reviewer on the SQL tool.
  2. 1-1 with Ryan: finish the "be aware of workup" conversation with data from Phase 2.
  3. Decide whether to change your sync attendance from optional to regular for the next 4 weeks.

  ### Suggested agenda items for today (add to the Notion page before 18:30)
  - "Onboarding path for new teams (SDM #54261, Tipping): who reviews gatherer PRs while Staged Rollout is paused?"
  - "ENT/Golem alignment with the next-step judge: worth a joint eval on shared PMS tickets?"
  - "Coverage while Laura is OOO 9/9 and 9/16."

  ### Not verified this run
  - Notion design docs (unified plugin, SQL tool, PRD, Q3A) were not read: the subagent fetching them hit a rate limit. Links are provided for Phase 1.
  - The rest of Ryan's "Be aware of workup" sentence is truncated in Bear search; open the note directly.
  - Dashboard numbers were not pulled (agents.cnry.land needs your browser session); the figures above are Laura's from 26 Aug.
  - No external writes were made. Nothing posted to Slack, Linear, Notion or GitHub.
project: 2026-08-05-strategy
source_id: null
tags: []
time_minutes: 5
title: I need to be more on top of workup. I'm behind the curve. Plan a catch-up investigation
updated: 2026-09-02 14:32:00.000000
waiting_on: null
waiting_since: null
working_on: true
---

https://docs.google.com/document/d/19XTmIdZfr7jU1cMNlcwoFRBLJFnIz3qibO4LwviTtxA/edit?tab=t.t81tvqup3p4s