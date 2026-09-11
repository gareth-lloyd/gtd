---
area: engineering
completed_at: null
contexts:
- deep
created: 2026-09-01 17:16:41.175964
defer_until: null
due: null
energy: high
id: 2026-09-01T1716-i-need-to-be-more-on-top-of-workup-i-m-behind-the
order: null
output: |
  # Workup catch-up: consolidated brief
  Last updated 2026-09-11. This merges the agent runs of 2026-09-02 and 2026-09-11, and supersedes both.

  ## 1. TL;DR
  - **Your role changed.** You now manage Laura, who owns Workup. Jason moves to an IC role working alongside her on Workup; his first metric is "triage tickets resolved without an engineer". This is CONFIDENTIAL until 14 Sep.
  - **Ryan's framing (12 Aug):** "Be aware of workup. This will be the main mechanism".
  - **State of play.** The SQL tool design is approved, with the build targeting 18 Sep. Accuracy work is on track for 6 Oct. Onboarding of new teams is paused until "next block". Interactive Investigations is paused.
  - **You owe Laura two things** (3 Sep 1-1): (a) review the dashboard and Linear metrics, and (b) read the investigate plugin redesign doc.
  - **Next touchpoints:**
    - Blake monthly, Tue 15 Sep 15:30.
    - Workup Agent Sync, Wed 16 Sep 18:30.
    - Laura 1-1, Wed 16 Sep 21:30.

  ## 2. Your role and commitments
  | Item | Source | Status |
  |---|---|---|
  | You manage Laura; Jason works alongside her on Workup (not an ownership handover) | Jason Flax mobile handover, 9 Sep (Granola 9ae56534-9bee-415b-9d65-c1b13b46a9c8); Blake 1-1, 3 Sep (Granola 99b0c662-1658-4dbb-97dc-0446e503ec04); #blake-directs https://canarytechnologies.slack.com/archives/C09MAQZ9LEN/p1788457392432539 | Confidential until 14 Sep |
  | Review the agent dashboard and Linear metrics | Laura 1-1, 3 Sep (Granola 0c031b32-87c3-441e-9d07-b7c15a2f6d4d) | OPEN |
  | Read the Workup plugin redesign doc | Laura 1-1, 3 Sep | OPEN (summary in section 9) |
  | Offered to help with grading | Laura 1-1, 9 Sep (Granola b4a5a969-ac49-4e75-a3da-c2e612552c24) | OPEN |
  | Said you'd "stay on top of it" and support it, while noting it competes with IHG/BW SSO work | Laura 1-1, 3 Sep | Ongoing |

  What you have said on record:
  - **Laura 1-1, 9 Sep:**
    - Metrics are "a foundation to build on", with "nothing too concerning".
    - Accuracy work is "high value".
    - Test whether the categories should be merged, but not just to make evaluation easier.
  - **Ryan 1-1, 10 Sep** (Granola 3c838ff3-9785-4eeb-af9b-7fbf0a47efdc): Workup runs in every team's triage queue and adds context plus a recommended next step. The current focus is metrics.

  ## 3. Calendar
  | When (Athens) | What | Your RSVP |
  |---|---|---|
  | Tue 15 Sep 15:30 | Gareth / Blake monthly | Not replied |
  | Wed 16, 23, 30 Sep 18:30-19:00 | Workup Agent Sync (organiser Laura, meet.google.com/dcu-sfhn-pcn, agenda https://app.notion.com/p/3c281468615181a1a88fca0b5fea0b94) | Optional; not replied (you declined 26 Aug) |
  | Wed 16 Sep 21:30, Wed 23 Sep 21:30 | Gareth <> Laura 1:1 | — |
  | Wed 14 Oct 20:45 | Ryan <> Gareth (none before then) | — |

  Sync regulars: Blake, Dylan Moradpour, Garrett Idler, Julius Seporaitis, Stephanie Barry, João Bueno, Nensy Auzina, Matías Marcó del Pont, Asher Davidson.

  ## 4. What Workup is
  - **What it does.** It is the production triage agent. It runs on the on-call handoff for MSG, CC and PMS tickets (not ENT). It posts findings and declares one of 8 "next step" buckets. A judge then grades that declaration against how the ticket was actually resolved.
  - **Links:**
    - Initiative (owner Laura DeWald): https://linear.app/canary-technologies/initiative/workup-2a7616f589a4
    - Dashboard: https://agents.cnry.land/workup
    - Bot page: https://agents.cnry.land/bots/workup
    - Overview: https://app.notion.com/p/3b281468615181abab24cc07d8889847
  - **Slack:**
    - #project-workup: https://canarytechnologies.slack.com/archives/C0AL1T2H43V
    - #eng-agents: https://canarytechnologies.slack.com/archives/C0AR52PPU4Q
  - **Code:**
    - The agents repo (canary-technologies-corp/agents).
    - canary_mcp and mcp-server, now owned by Internal Tools (canary #55513).

  ## 5. Project status (as of 11 Sep)
  | Project | State | Lead | Target | Notes |
  |---|---|---|---|---|
  | Canary MCP SQL Tool https://linear.app/canary-technologies/project/ai-workup-canary-mcp-sql-tool-72b25204de08 | Implementation | Asher Davidson | 18 Sep (slipped from 4 Sep) | Design approved 9 Sep; build tickets TOOL-618..665 |
  | Accuracy https://linear.app/canary-technologies/project/ai-workup-accuracy-1bfe6e72996f | Implementation | Laura | 6 Oct | On track, 8 Sep update: https://linear.app/canary-technologies/project/ai-workup-accuracy-1bfe6e72996f/activity#project-update-4c691305 |
  | Staged Rollout to Eng-Routed Teams https://linear.app/canary-technologies/project/ai-workup-staged-rollout-to-eng-routed-teams-7ca5cf153530 | Planned | Laura | none | No update since 10 Aug; "revisit ~Q4A" |
  | Team Enablement via KB https://linear.app/canary-technologies/project/ai-workup-team-enablement-via-knowledge-base-600f1d9cbf16 | Planned | Laura | none | No update since 11 Aug |
  | Faster, Cheaper Runs https://linear.app/canary-technologies/project/ai-workup-faster-cheaper-runs-cf1fd6c4d4a3 | Planned | Laura | none | No update since 10 Aug |
  | Interactive Investigations https://linear.app/canary-technologies/project/ai-workup-interactive-investigations-8e1ffa958fa5 | Paused (10 Sep) | Laura | none | — |
  | Workup guest data handling | Backlog | none | none | TOOL-642 (pseudonymize PII in captured outputs), TOOL-643 (a path for guest data-erasure requests), TOOL-644 (scope-check identifiers before posting) |
  | Next-Step Metric | Completed | — | — | Live since 24 Aug |
  | Model Benchmark | Canceled 28 Aug | — | — | — |

  Accuracy detail (8 Sep update):
  - **Done:** Phases 3a and 3b.
  - **In progress:** Phase 4, about half done.
  - **Shipped:**
    - Gatherers emit claims.
    - `select.py` decides which gatherers run.
    - Demo-mode and messaging-disabled checks run on every ticket.
    - Classification runs in shadow.
    - Full tool outputs are captured.
  - **Next:**
    - TOOL-607: classification drives gatherer selection.
    - TOOL-606: branch and short-circuit stages.
    - TOOL-608: config-vs-capability checks.
    - TOOL-655: read the Zendesk conversation (In Progress).
    - TOOL-652: the 2.0.0 release cut.
    - TOOL-654: posting gate in shadow.
  - **Risk:** if shadow classification disagrees with the team filter, TOOL-607 slips.

  ## 6. Key numbers
  - **Last 14 days (Laura, 26 Aug):**
    - 107 investigations across 14 teams (MSG 30, PMS 18, INT 16, CC 14).
    - About 1 run in 4 posts nothing.
    - 12 runs hit the cap, all dying in the multi-agent debate stage.
    - The first 28 next-step labels skewed code-fix 10 / ops-action 8. That supports Blake's read that Workup favours code changes over config changes.
  - **Cost (UNRESOLVED):** Laura's Slack says about $95/day (about $2.5-3k/month). The 26 Aug meeting notes say Blake called about $900-950/day acceptable "for now". Settle this from the dashboard.
  - **Cap:** raised from $15 to $30 on 26 Aug. The 9 Sep notes mention a run killed at a $40 cap (ONC-26129).
  - **Interactive baseline (PRD):** 34% of runs end by asking the reporter for info, and 2% of those asks get a reply.
  - **Activity:** 9 Sep sync reported about 45 commits in 2 weeks: 19 PRs in the agents repo and 24 commits to the investigate plugin.

  ## 7. Decision log
  - **5 Aug, Triage Agent Sync** (before you were invited): https://docs.google.com/document/d/1pR_vFnbnykKd2v2vU9KVloIbG3ooAT1pCtiYngPp5xI/edit
    - Prefer audit logging + SIEM over obfuscating data.
    - Restrict internet access for headless agents that handle PII.
    - Add the engram memory layer.
    - Send Slack notifications for tickets missing information.
  - **12 Aug:** https://docs.google.com/document/d/1kUbxDiMWronnnOD4AAq5cRVF_k6NvTPHvtnyJcJBXw4/edit
    - Canary MCP moves from Applied AI to Internal Tools.
    - Querying uses raw SQL; the ORM is used only inside specific MCP tools.
    - The investigate skills migrate to MCP.
    - PMS Gateway auth uses the user's email.
    - The "next step" metric is adopted.
    - The SQL tool is priority #2.
  - **26 Aug:** https://docs.google.com/document/d/19XTmIdZfr7jU1cMNlcwoFRBLJFnIz3qibO4LwviTtxA/edit?tab=t.t81tvqup3p4s
    - No cost or model optimisation until the new prompting lands.
    - Cap raised from $15 to $30.
    - The MCP server gets no direct DB access; the SQL tool goes through Django raw SQL.
    - SQL security is a deny-list (certificates, client secrets, private keys, access keys, card data) plus a Luna query judge. Semicolons are blocked.
    - Payment, HR and mobile-key gateway config stays queryable.
    - Actions: Laura deploys the judge; Blake reviews Asher's blocklist; Blake and Asher sync on security.
    - Ideas not adopted: a human continue/stop check at about $5 (Dylan); switching to a cheaper model mid-run (Garrett).
  - **3 Sep, Slack:** no new teams until the investigate plugin tweaks are done, "hopefully next block". https://canarytechnologies.slack.com/archives/C0AMJPBUH60/p1788461627370269
  - **9 Sep:** Gemini notes https://docs.google.com/document/d/1i-IOhiSYeRAbePmuEb51IfIaaxGOw2rhwz95pnkk7KM/edit; Notion agenda https://app.notion.com/p/3c281468615181a1a88fca0b5fea0b94
    - SQL tool approved: read-only, Workup-only.
    - The LLM judge does not block when it is down.
    - Auth is a Pomerium bearer token, then a permission check in Django.
    - Write actions are deferred as long as possible.
    - Rollout to non-EPD users comes after Workup.
    - Devin variants removed.
    - Actions: Laura sends her comms core checks PR to Matías for review; SQL tool progress update due next week.
    - Nothing was assigned to you.
  - **9 Sep, Laura 1-1:**
    - Fix the upstream checks before expanding to more teams.
    - Start bringing teams in next block.
    - Focus stays on Messaging.

  ## 8. Shipped and incidents since 20 Aug
  **Shipped, 20 Aug - 1 Sep:**
  - Agents repo #141-#178; canary #53790, #54769, #54796, #54880, #54960.
  - Next-step labels plus the judge. Pass A labels from Linear records; pass B is an LLM.
  - Dashboard rebuilt around next-step correctness.
  - Tool-mix view and full tool-output capture.
  - EU/AP handoff live.
  - Plugin split into core and bindings.
  - Gatherers emit claims.
  - Hotel-level demo-mode and messaging-disabled checks.
  - Handoff crash fix (TOOL-597).

  **Shipped, 2 - 11 Sep:**
  - agents #132: validated submit_diagnosis contract (fixes the engram incident). Merged 3 Sep. https://github.com/canary-technologies-corp/agents/pull/132
  - agents #179: short-lived Zendesk tokens (TOOL-581). Merged 2 Sep. https://github.com/canary-technologies-corp/agents/pull/179
  - agents #183: judge boundaries. https://github.com/canary-technologies-corp/agents/pull/183
  - agents #188: saves the evidence a report cites. https://github.com/canary-technologies-corp/agents/pull/188
  - agents #191: grader attribution. https://github.com/canary-technologies-corp/agents/pull/191
  - agents #192: removes the v1 investigator (TOOL-657). https://github.com/canary-technologies-corp/agents/pull/192
  - canary #54261: SDM authorizations gatherer (Luiza). https://github.com/canary-technologies-corp/canary/pull/54261
  - canary #55170: hotel-id regex fallback (TIP-5329). https://github.com/canary-technologies-corp/canary/pull/55170
  - canary #55858: posts a comment when a handoff fails (TOOL-598). https://github.com/canary-technologies-corp/canary/pull/55858
  - canary #55513: canary_mcp ownership moves to Internal Tools. https://github.com/canary-technologies-corp/canary/pull/55513
  - TOOL-605: fixes for push-back asking the wrong questions. Done 3 Sep.

  **Incidents:**
  - **About 13 Aug, engram memory nudge:** it broke Workup posting. Memory was turned off for Workup, and the fix is #132. https://canarytechnologies.slack.com/archives/C0AR52PPU4Q/p1786566370592719
  - **27 Aug, Golem/Workup outage:** https://canarytechnologies.slack.com/archives/C0AR52PPU4Q/p1787860715971269
  - **Early Sep, stale sandbox template:** the nightly E2B template rebuild failed for days, so agents ran stale skills. The cause was the npm mirror change. Fixed 11 Sep by agents #193; #194 adds an alert when the template goes stale. https://canarytechnologies.slack.com/archives/C0AR52PPU4Q/p1789058382055819
  - **Agent limits moving:** per-agent limits move from secrets to the dashboard, with a new `long_running` flag (EE-2022..2026, Yeh). This followed complaints about cost and caps. https://canarytechnologies.slack.com/archives/C0AR52PPU4Q/p1788981896770899

  ## 9. Design docs digest
  **Unified investigate plugin** (APPROVED). This is the redesign you promised Laura you'd read.
  - Links: readable https://app.notion.com/p/3bf81468615181e58428e5a18d91433c; normative https://app.notion.com/p/3bf814686151816391a4d784f859afcd
  - The pipeline has nine stages: subject, classify, resolve, checks, branch, loop, debate, report, telemetry.
  - Classification decides which resolvers run, never the verdict.
  - Every finding is a cited claim with a confidence level and an as-of time.
  - A run stops early only on an unopposed "observed" claim that is still valid at the time of the event.
  - A confidence gate (high / medium / low) sits before posting and ships in shadow first.
  - Teams own their checks, gatherers and resolvers; Internal Tools owns the core.
  - **Enterprise/PMS catch:** config-vs-capability checks are team-owned and not scheduled, with PMS expected first. Until one exists, the early-stop path can't fire.
  - Open: loop tuning, gate thresholds, redaction and retention of recordings, and what the learn loop may read.

  **Canary MCP SQL Tool** (APPROVED 9 Sep; 22 comment threads)
  - Links:
    - Design: https://app.notion.com/p/3c8814686151808c8231f5997b870632
    - Requirements: https://app.notion.com/p/3c281468615180a6a89bc4b5b99a60dc
    - Blocklist: https://app.notion.com/p/3c681468615180f086b6f72a998f4a08
    - TOOL-562: https://linear.app/canary-technologies/issue/TOOL-562
  - Sign-offs: Ben (27 Aug), Bernard on the blocklist (8 Sep), Alina for Security (9 Sep).
  - Query path:
    - A `run_sql` POST view runs as the `canary_mcp_ro` role.
    - `;` and `SELECT *` / whole-row forms are refused.
    - A named cursor bounds memory.
    - An EXPLAIN cost gate applies.
    - The Luna judge can only refuse, and fails open.
  - Limits: 30 requests/min and 200k rows / 50MB per day, held in Valkey and failing closed.
  - Auth:
    - Pomerium bearer token.
    - Cloudflare IP allowlist.
    - Egress through Agent Vault with pinned NAT IPs.
    - Teleport is out.
    - The Django check keyed on per-region user ID is the only per-tool authorization.
  - Audit: an `McpSqlQuery` table with 90-day retention.
  - Build in flight:
    - canary #55746 (SqlExecutionService) is approved but not merged. https://github.com/canary-technologies-corp/canary/pull/55746
    - TOOL-620: can a machine identity get an email claim Pomerium accepts? In Progress, Asher.
    - Egress: TOOL-664 and TOOL-665 must land before TOOL-656.
  - **Enterprise residual risks:**
    - It runs on the Django pool that also serves guest traffic.
    - Payment, mobile-key and HR gateway tables stay readable except for named columns, so column drift is the risk.
    - Three tables have a `cvv` column.
    - A steered single-guest read is an accepted risk.
    - Query predicates reach OpenAI through the judge, so zero-retention and no-training on the Luna key must be confirmed before launch.
  - Open review threads: Alina's large-row memory test; Overlord re-injecting credentials on resume.

  **Next Step metric** (APPROVED, live 24 Aug): https://app.notion.com/p/3b38146861518008b312fa94262e4ef4
  - Eight buckets: Config, Ops, Code fix, Feature request, Escalate, Request info, Duplicate, No action.
  - A declaration is correct only if the bucket matches AND it names the specific object to act on.
  - The secondary axis is an 11-value cause taxonomy.
  - Open:
    - Which tickets are eligible (selection bias).
    - Telling apart Request info / Duplicate / No action / Feature request.
    - Whether an Escalate was genuine or the agent gave up.
    - Config vs Ops confusion is still live (9 Sep).

  **PRD Interactive Investigations** (project paused): https://app.notion.com/p/3b9814686151818b9e09f189f1499888
  - Investigate first; ask one specific question inside the run, at most twice per ticket.
  - Waiting tickets get a `Workup: Needs Info` label.
  - Wait times follow the priority's SLA, and questions also go out as Slack DMs.
  - Open: does a plain comment count as an answer; does the SLA clock pause; should a CSM step be in the escalation order; spend caps.

  Also: Q3A Internal Tools planning, Workup section (not read): https://app.notion.com/p/38f81468615180b7abf6c50c43271dc6

  ## 10. Open threads (who is waiting on whom)
  | Thread | Waiting on | Link |
  |---|---|---|
  | Arrivals/Departures gatherer needs review; Guido is blocked by the onboarding pause | Internal Tools reviewer | https://github.com/canary-technologies-corp/canary/pull/55360 ; https://canarytechnologies.slack.com/archives/C029BPP02H0/p1788543620053219 |
  | Tipping (João Bueno) asked how to onboard and offered help; no task yet | Laura | https://canarytechnologies.slack.com/archives/C0AL1T2H43V/p1788303495256679 ; https://canarytechnologies.slack.com/archives/C0AL1T2H43V/p1788361777223959 |
  | Groundcover evidence links (TOOL-609), In Review | Reviewer | https://github.com/canary-technologies-corp/canary/pull/55953 |
  | SQL tool auth call: Asher with Bernard and Alina | Bernard/Alina | https://canarytechnologies.slack.com/archives/C0AL1T2H43V/p1788880113814539 |
  | Luna zero-retention confirmation before SQL tool launch | Asher/Security | SQL tool doc |
  | Comms core checks PR for Matías to review | Laura | 9 Sep notes |
  | 3 Planned projects with no status since Aug | Laura | section 5 |

  ## 11. Enterprise and Golem angle
  - **Rubric mapping:** Golem's verdict rubric is already mapped onto the Workup judge (agent-plugins/claude-plugins/enterprise/docs/golem-verdict-rubric.md, "Workup judge mapping", ENT-7182). The stated aim is that Golem runs surface on agents.cnry.land.
  - **Golem ownership:** "Platform team has taken Golem, ticket to get mcp access" (Bear "Laura Dewald"). Golem PRs #180-182 shipped live-branch support.
  - **Workup doesn't cover ENT:** ENT is the one eng-routed team with its own investigation agent. Neither sync mentions ENT or Golem.
  - **Evidence it's your problem space:**
    - Your 5 Aug Enterprise plan opens with "reduce IC frustration with Triage" (Bear "Enterprise").
    - Blake: Mattie found CSA-routing issues via Workup, which is "the exact problem space" (Bear "Blake Van Landingham").
  - **SQL tool notes** (Bear "Laura Dewald", 9 Sep):
    - Blocklist, not allowlist.
    - Locked down to Workup, and harden for dev use later.
    - Mine the queries to create rules.
    - Bernard is focused on PII.

  ## 12. Action plan
  **Before 15-16 Sep (about 2 h). This closes commitments (a) and (b).**
  - [ ] Dashboard (https://agents.cnry.land/workup): 7-day next-step correctness, no-post rate, cap-kills, $/day. This resolves the cost discrepancy. 20 min.
  - [ ] Read the unified plugin design, focusing on the checks, branch and ownership sections. Form a view on who writes the first PMS config-vs-capability check. 45 min.
  - [ ] Skim the Accuracy 8 Sep update and TOOL-606/607/608. 15 min.
  - [ ] RSVP to Blake (15 Sep) and the Workup sync (16 Sep). As Laura's manager, attend weekly through the end of the block. 2 min.
  - [ ] Grade 5 PMS tickets from https://linear.app/canary-technologies/view/next-step-tickets-69f507a962f4 using the Golem rubric. This gives you a baseline and makes the grading offer concrete. 40 min.

  **Later this block:**
  - [ ] Read the transcripts of 2 cap-killed runs (e.g. PMS-10139, https://linear.app/canary-technologies/issue/PMS-10139, and ONC-26129) via agents.cnry.land/sandboxes, to see where the money goes.
  - [ ] Put Golem numbers (/enterprise:golem-metrics) next to Workup's for the same window: accuracy, cost per correct diagnosis, no-post rate.
  - [ ] Write a Bear note "Workup catch-up 2026-09" answering the questions in section 14.

  ## 13. Agenda drafts
  **Blake monthly, 15 Sep**
  - What does Workup success look like this block? How do Laura's next-step correctness and Jason's "resolved without engineer" metric fit together without competing?
  - Cost ceiling: $95/day or $950/day? What triggers a revisit once the unified plugin lands?
  - Onboarding pause: is "next block" a commitment, and who tells the waiting teams (A/D, Tipping)?

  **Laura 1-1, 16 Sep**
  - Manager transition: expectations, cadence, and what she needs from you versus from Jason. Who sets Workup priorities?
  - Project hygiene: close, re-date, or post a status for Staged Rollout, Team Enablement, and Faster/Cheaper.
  - Onboarding: a dated re-open plan and a named reviewer for gatherer PRs (#55360).
  - SQL tool pre-launch (target 18 Sep):
    - Luna zero-retention.
    - `cvv` columns explicitly denied.
    - Load isolation from the guest-traffic Django pool.
    - TOOL-620.
  - Grading: take a slice of judge labels yourself, or lend an ENT engineer.
  - Ask for the 12 Aug handoff doc from Applied AI.

  **Workup sync, 16 Sep: candidate topics**
  - The onboarding re-open plan and who reviews gatherer PRs.
  - A joint eval of Golem and the Workup judge on shared PMS tickets.

  ## 14. Strategic questions
  1. **ENT and Golem:** now that Platform holds Golem, should ENT converge on Workup (contribute gatherers/checks and the PMS config-vs-capability check) or keep a separate agent?
     - Lose: the enterprise KB playbook, DB-script mode, misroute detection.
     - Gain: the shared judge, dashboard, SQL tool, EU/AP coverage.
  2. **Metric coherence:** next-step correctness (Laura) versus resolved-without-engineer (Jason).
  3. **Unstaffed checks:** team-owned checks have nobody scheduled to write them. Should you staff that from ENT/PMS?
  4. **Cost governance:** is the current spend plus a roughly 25% no-post rate acceptable past this block?
  5. **Security:** is a deny-list plus a fail-open LLM judge defensible in an enterprise customer security questionnaire (PII, PCI, credential-manager)?

  ## 15. Corrections and caveats
  - **Corrections to the 2 Sep run:**
    - Laura is NOT out of office. The "out of office" text is an old auto-comment on accepted invites, and she ran the 9 Sep sync.
    - There was no 2 Sep sync.
  - **Not verified:**
    - Dashboard numbers (needs your browser session).
    - Which daily cost figure is right.
    - Granola content comes from summaries, not transcripts.
    - The exact effective date of the org change.
  - No external writes were made. Nothing was posted or RSVP'd, and no Salesforce was touched.
project: 2026-09-08-workup
source_id: null
tags: []
time_minutes: 15
title: I need to be more on top of workup. I'm behind the curve. Plan a catch-up investigation
updated: 2026-09-11 16:07:30.928337
waiting_on: null
waiting_since: null
working_on: false
---

https://docs.google.com/document/d/19XTmIdZfr7jU1cMNlcwoFRBLJFnIz3qibO4LwviTtxA/edit?tab=t.t81tvqup3p4s