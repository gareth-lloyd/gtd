---
area: engineering
completed_at: 2026-09-16 21:35:56.696587
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

  ## Agent run 2026-09-16T15:40:25

  **Follow-up asked:** "The agent output is not helping me catch up with the work that's been done on workup. Do more investigation and draft a Notion document to help me get full context for where the project is at, strategy, next priorities, and weaknesses"

  **What I did.** Ran seven parallel research passes: agents repo (PR history, architecture, judge code), canary repo at origin/master (investigate plugin, linear_agent trigger, canary_mcp, SQL tool), Linear (initiative, 9 projects, every issue, updates, labels, cycles), Notion (all design docs plus Q3B strategy pages and Jason's charter), Slack (#project-workup, #eng-agents, #epd-internal-tools, #blake-directs, searches), meeting notes (5/12/26 Aug and 9 Sep Google Docs, Granola transcripts for Laura 9 Sep, Ryan 10 Sep, Blake 14 Sep, Jason 9 Sep), the live dashboard at agents.cnry.land (auth worked), your calendar, and your Bear notes.

  **Deliverable.** The Notion document is DRAFTED LOCALLY below and at the scratchpad path /private/tmp/claude-501/-Users-garethlloyd-projects-canary/b4f6c1fd-2117-458a-9efa-0980340a7d49/scratchpad/workup-context-brief.md (about 6,900 words, 12 sections). It has NOT been created in Notion: that is an external write and needs your explicit go-ahead. Say "create it in Notion" and I will create it as a private page (or name a destination).

  **Headline findings that were not in the prior brief.**
  - Dashboard: next-step correctness 23% (7d) / 29% (30d), judge flagged `uncalibrated`, and 0 of 116 judged tickets resolved end to end by Workup. No-post rate has fallen from 20% to 1.7% this week; avg cost per run $8.64.
  - Cost discrepancy resolved: Workup lifetime spend $2,735 (57% of all agent spend), roughly $70-140/day. Blake's "900-950/day" is not supported by any dashboard number.
  - SQL tool: `SqlExecutionService` merged 14 Sep but nothing calls it; 54 of 79 points open, 14 tickets unowned, target 25 Sep. Auth fell back to a temporary "Option D" on 15-16 Sep with Alina's conditions only in a Slack reply. Bernard posted a new blocker on the design page today.
  - Team Enablement via KB was cancelled 14 Sep; the overview page still asks pods to write Pattern pages.
  - Laura is the only human grader and authored 54 of 104 canary commits and 62 agents-repo PRs on Workup; her parental leave is roughly three months out.
  - Engram (approved 5 Aug, caused the 13 Aug incident) is effectively unused: 77 remember calls across 6 runs.
  - ENT and CA prompt overrides already exist on the bot despite the onboarding pause; every retained Workup sandbox is an ONC ticket.
  - Calendar corrections: there was no Blake monthly on 15 Sep (Blake directs was Mon 14 Sep). You are needsAction on tonight's Workup sync (18:30) and on the Internal Tools Q3 Block 2 Review (Thu 24 Sep 21:15), and tentative on every Internal Tools weekly.

  **Not verified / caveats.** Normative plugin design page is not shared with the Notion integration. Cap-killed runs PMS-10139 and ONC-26129 are outside sandbox retention. Dashboard week-on-week delta direction unreadable. "Lauren" in the Jason handover Granola note is taken to be Laura. No external writes made; nothing posted, RSVP'd, or created anywhere.

  ---

  # DRAFT NOTION DOCUMENT (verbatim)

  # Workup: full context brief

  Prepared 16 Sep 2026 for Gareth Lloyd. Private draft. Sources: agents repo and canary repo (origin/master), Linear, Notion, Slack, Google Docs meeting notes, Granola transcripts, the live dashboard at agents.cnry.land, and Gareth's own notes. Anything marked *(inferred)* is a judgement, not a sourced fact.

  ---

  ## 1. One-page summary

  **What it is.** Workup is Canary's production triage agent. When an Oncall ticket is routed to an enabled team, the Linear triage agent hands it to Workup. Workup runs an investigation in a sandbox (logs, code, hotel config, Zendesk conversation), posts a diagnosis with evidence to the ticket, and declares one of eight machine-readable "next steps". An LLM judge later grades that declaration against how the ticket actually resolved. Laura DeWald (Internal Tools) owns it. Blake Van Landingham sponsors it. Asher Davidson builds the SQL tool. Jason Flax now works alongside as an IC on the AI platform. You manage Laura as of 14 Sep.

  **Why it matters.** Blake and SJ's Q3B framing: Canary spends 20-30% of engineering time on triage, oncall and investigation, and reducing that is the top focus for Q3 Block 2. Ryan's version: triage "knocks out one team member for a week every week". Ryan told you on 12 Aug that Workup "will be the main mechanism".

  **Where it is (16 Sep).**
  - Live for MSG, CC, PMS via the Oncall queue, plus EU/AP. About 8 runs a day at about $8.64 a run this week. Lifetime 433 runs, $2,735.
  - The measurement layer is built: next-step labels on every ticket since 24 Aug, a two-pass judge, and a quality dashboard. Headline next-step correctness is 23% (7d) / 29% (30d), and the judge is flagged `uncalibrated`.
  - 0 of 116 judged tickets were resolved end to end by Workup. That was Blake's stated goal on 5 Aug.
  - The investigate plugin is mid-rebuild (phases 4 and 5 of 6). Onboarding of new teams is paused until the rebuild lands, "next block".
  - The SQL tool design is approved but the build is about a quarter done, targets 25 Sep, and its auth path became a temporary workaround this week.

  **Strategy in one line.** Build an accountable investigation pipeline (cited claims, confidence, a posting gate) that can name the specific next step, prove it with a calibrated metric on Messaging first, then expand team by team. Everything else (interactive asks, KB, cost, model benchmark) has been paused, cancelled or folded in.

  **Next priorities as the team states them.** (1) Cut classification-driven selection over (TOOL-607) and land the first config-vs-capability check for Messaging (TOOL-608). (2) Ship the SQL tool to prod US. (3) Build the investigation loop (phase 5). (4) Posting gate in shadow (TOOL-654). (5) Re-open onboarding next block.

  **The five weaknesses that matter most.**
  1. The headline metric cannot be trusted yet: uncalibrated judge, wide interval, a shrinking denominator, and Laura is the only human grader.
  2. Delivery is concentrated on two people (Laura for Workup and the judge, Asher for the SQL tool) with parental leave for Laura about three months out. Nobody else has authored a core PR.
  3. The SQL tool is on a temporary security path (Option D) whose conditions live in a Slack reply, with a fresh blocker from Bernard today and 14 unowned tickets against a 25 Sep target.
  4. Roughly a third of investigated tickets carry no declared next step, 76% of runs execute with context gaps, and Engram memory, approved on 5 Aug, is effectively unused.
  5. The initiative has never posted a status update, four of nine projects are inert, and the overview page still tells teams to do work (Pattern pages) for a project that was cancelled on 14 Sep.

  ---

  ## 2. What Workup is and how it works

  ### The four parts and where they live

  | Part | Where | Owner |
  |---|---|---|
  | Runtime: the `workup` agent, judge, dashboard, sandboxes | agents repo (`overlord/src/agents/workup/`, `overlord/src/workup-quality/`, `dashboard/`) | Laura (agent, judge), Yeh Fang (platform), Bernard (security) |
  | Investigation framework: the investigate Claude plugin | canary repo `agent-plugins/claude-plugins/investigate/` (v1.15.0) | Internal Tools, Julius as co-owner |
  | Trigger: Linear triage agent to Workup handoff | canary repo `backend/canary/linear_agent/` | Internal Tools |
  | Data plane: Canary MCP servers, agent context providers, SQL tool | canary repo `backend/canary/canary_mcp/`, `backend/mcp-server/`, `backend/shared/shared/agent_context/` | Internal Tools (since 12 Aug, previously Applied AI) |

  Team-owned content (gatherers and checks) lives inside the investigate plugin under CODEOWNERS lines for each pod.

  ### An end-to-end run

  1. **Trigger.** A Linear webhook runs the LangGraph triage graph. It classifies the team, extracts entities, recommends labels. If the recommended team is in `LINEAR_AGENT_WORKUP_TEAMS` (currently MSG, CC, PMS via ONC/SBOX intake), it POSTs a `workup-handoff-v2` envelope to Overlord. If that fails it falls back to a plain triage comment (TOOL-598, 11 Sep).
  2. **Claim.** Overlord's `workup` agent runs in shared mode on the router pod. It dedupes via a durable handoff store, opens a Linear agent session, and posts the triage summary.
  3. **Investigate.** If investigation is needed, it dispatches an isolated E2B sandbox running Claude Code with the investigate plugin. The prompt names the region-specific Canary MCP server because a wrong-region miss reads as "not configured".
  4. **The pipeline** (`/investigate:investigate-ticket`, nine stages): start, gather (resolve subject, reservation, PMS integration, then a parallel gatherer wave filtered by team prefix plus an LLM description gate), classify area (shadow), sufficiency/duplicate/ceiling checks, cheap checks chosen by `select.py` (11 ship today, including nine ported from Bowerbird), branch (an unopposed "observed" diagnosis-class claim short-circuits straight to report), debate (6-7 sub-agents that no longer talk to each other), declare, summarise, trailer. Since TOOL-691 (15 Sep) every closed-form step is a Python subcommand, so the model acts on printed JSON rather than recomputing rules.
  5. **Post.** The sandbox posts only what it submits through a single-tool MCP server (`submit_diagnosis`), never the transcript. This exists because on 13 Aug an Engram memory nudge hijacked the model's final words and that became the posted diagnosis. The diagnosis ends with a `workup-result-v1` JSON trailer naming the bucket, the specific object, and the cause category. The trailer becomes a `Next Step:` label on the ticket and a row in `workup_declarations`.
  6. **Guardrails.** Per-attempt cost cap (`OVERLORD_MAX_COST_USD`, $30 for Workup, mid-loop SIGKILL), turn cap, a 5-minute watchdog that fails a session after 2 hours, evidence persisted at post time with redaction.
  7. **Grade.** An hourly cron syncs resolved tickets. Pass A grades mechanically from Linear records (human-corrected label, duplicate relation, working-as-intended cancel). If Pass A returns null, Pass B asks Sonnet 5 twice: first blind (declaration withheld) to pick the actual bucket, then, only if the buckets match, to grade whether the specific object matched. Correct means bucket match AND object match. Right bucket, wrong object is a "near miss" and counts as wrong.

  ### What the judge and dashboard actually compute

  - Correctness rate = correct / scored. Tickets the judge could not call (null) are excluded from the denominator and reported separately.
  - The calibration gate needs at least 50 hand labels, agreement at or above 70%, and a Wilson lower bound at or above 70%. Latest: 74% agreement on 95 labels, interval 64-81%. The lower bound is below the bar, and the dashboard flags the judge `uncalibrated` because the eval measured a different prompt than the one now running.
  - The taxonomy is maintained by hand in two repos (agents `next-step-label.ts` and canary `core/taxonomies/next-steps.md`). A bucket change needs a paired PR by convention only.

  ### Data access today

  Groundcover MCP for logs, Linear MCP, the region-scoped Canary MCP servers (about 30 read-only REST tools plus `get_agent_context`), Zendesk via short-lived tokens (since 2 Sep), Snowflake MCP. The Canary MCP trust boundary is a shared secret plus an unverified Teleport JWT, and read-only is enforced by a Python method check rather than a database grant. The SQL tool (TOOL-619) is the fix.

  ---

  ## 3. How we got here

  | When | What |
  |---|---|
  | Mar 2026 | PMS Gateway "drowning in triage" (queues 16 to 30+ overnight). Two tracks agreed: Golem prototyping (Julius, Ian) and a long-term LangGraph backbone from Laura's Linear triage agent. MCP was ruled out at the time as "a co-pilot tool, not a background agent framework". |
  | May 2026 | Ownership blow-up: Blake asked Julius to drive org-wide adoption without telling Laura; she threatened to hand off the Linear agent. Blake settled it: Internal Tools owns infra and process, Julius is leverage. Your note: "Not ownership but stewardship". |
  | 22 Jun | Directors: Golem "ASAP"; Platform takes Golem. Your ownership model: Laura owns the platform, Stephanie is product point, Julius pushes the frontier in PMS Gateway. |
  | 13 Jul | Workup agent born in the agents repo (PR #78), owning its own Linear session. |
  | 27 Jul | Quality stack ships: `workup_*` tables, cause judge, dashboard. Judge measuring accepted solutions at about 50%. |
  | 5 Aug | Triage Agent Sync (before you were invited). Engram memory adopted. Blake: "how can we get triage agent to have the same stack that a software engineer at Canary has". Write access deprioritised for triage. |
  | 6 Aug | Blake defines the Next Step metric and moves Canary MCP from Applied AI to Internal Tools with a commitment to a guarded SQL tool. |
  | 12 Aug | Workup Agent Sync: raw SQL over ORM; next-step metric adopted; SQL tool is priority 2. Ryan to you: "Be aware of Workup. This will be the main mechanism." |
  | 13-18 Aug | Engram incident. Memory nudge breaks posting; 8 of 12 audited runs post nothing; PMS-9985 finds the real cause then dies on the $15 cap after five memory writes; MSG-5501 goes undiagnosed and Jonathan redoes it by hand two days later. Fix is the validated `submit_diagnosis` contract (#132) plus three more bugs Laura found (#136). Memory turned off for Workup. |
  | 20-24 Aug | Investigate plugin v1.2.0 declares a next step; labels go live on production tickets 24 Aug. EU/AP live. |
  | 26 Aug | Sync: 107 investigations in 14 days; 1 in 4 posts nothing; 12 runs hit the $30 cap, all in the debate stage. Blake overrules cost optimisation: "we're not in a cost optimization phase". SQL security settled as deny-list plus LLM judge. |
  | 26 Aug - 8 Sep | The architectural fortnight: core/bindings split, claims, envelope v2, select.py, first checks, shadow classification, branch stage. Next-step judge built end to end (Pass A, Pass B, hand-grading, eval loop, dashboard rebuilt). |
  | 2-4 Sep | Tipping and A/D ask to onboard; told "not onboarding anyone else just yet". Guido reports himself blocked. |
  | 9 Sep | SQL tool design approved (Security sign-off). Devin variants removed. Sync ended early. |
  | 10-11 Sep | E2B template rebuild found silently broken since 5 Sep; agents ran stale skills. Fixed with GHA rebuild and a staleness alert. |
  | 11-16 Sep | Nine Bowerbird comms checks ported in; checks can now end a run early; Workup reads the Zendesk conversation; `pipeline.py` lands; Groundcover evidence links in reports; Team Enablement via KB cancelled (14 Sep); Jason's IC role announced (14 Sep); SQL tool auth falls back to Option D (14-16 Sep). |

  ---

  ## 4. Where the project is now

  ### Projects in the Workup initiative

  Initiative: https://linear.app/canary-technologies/initiative/workup-2a7616f589a4 (Active, owner Laura, no target date, no health, no initiative status update ever posted).

  | Project | State | Lead | Target | Reality |
  |---|---|---|---|---|
  | [Accuracy](https://linear.app/canary-technologies/project/ai-workup-accuracy-1bfe6e72996f) | Implementation, onTrack | Laura | 6 Oct | 23 of 35 issues done. Phases 2, 3a, 3b complete. Phase 4 (checks framework, classification, 2.0.0) 47%, went backwards from 59% because scope was added. Phase 5 (the loop) 13-50% and started before phase 4 closed. Phase 6 (learn loop) 0%. Six open issues unassigned including the 2.0.0 release cut itself. |
  | [Canary MCP SQL Tool](https://linear.app/canary-technologies/project/ai-workup-canary-mcp-sql-tool-72b25204de08) | Implementation | Asher | 25 Sep (was 18 Sep, was 4 Sep) | 6 of 31 done, 54 of 79 points open, 14 Todo tickets unassigned. Milestones: Build 24%, Staging 4%, Prod US 6%. `SqlExecutionService` merged 14 Sep but nothing calls it; there is no `run_sql` endpoint on master. Validation (Kevin), grants (Asher, six stacked PRs), admin/retention (Sam) all in review. TOOL-620 auth is labelled Blocked. |
  | [Next-Step Metric](https://linear.app/canary-technologies/project/ai-workup-next-step-metric-ec82c135119d) | Completed 28 Aug | Laura | | Labels and declarations shipped. The judge definitions were still moving on 9 Sep and the calibration bar has not been cleared. |
  | [Interactive Investigations](https://linear.app/canary-technologies/project/ai-workup-interactive-investigations-8e1ffa958fa5) | Paused 10 Sep | Laura | | PRD approved 26 Aug; zero issues. |
  | [Staged Rollout to Eng-Routed Teams](https://linear.app/canary-technologies/project/ai-workup-staged-rollout-to-eng-routed-teams-7ca5cf153530) | Planned, "Deprioritized" | Laura | | Zero issues, untouched since 10 Aug. "Revisit Q4A." |
  | [Faster, Cheaper Runs](https://linear.app/canary-technologies/project/ai-workup-faster-cheaper-runs-cf1fd6c4d4a3) | Planned | Laura | | One backlog issue (TOOL-475). Untouched since 10 Aug. |
  | [Team Enablement via KB](https://linear.app/canary-technologies/project/ai-workup-team-enablement-via-knowledge-base-600f1d9cbf16) | Cancelled 14 Sep | Laura | | "Folded into other Workup work." The overview page still asks teams to write Pattern pages. |
  | [Model Benchmark](https://linear.app/canary-technologies/project/ai-workup-model-benchmark-a2dc4ad77743) | Cancelled 28 Aug | | | Runtime is now restricted to Anthropic models anyway. |
  | [Workup guest data handling](https://linear.app/canary-technologies/project/workup-guest-data-handling-9dea5554cd38) | Backlog | none | | TOOL-642 (pseudonymise PII in captured outputs), TOOL-643 (erasure path), TOOL-644 (scope-check identifiers before posting). All unassigned, no priority. Full tool-output capture shipped on 31 Aug; the safeguards did not. |

  Outside the initiative: AI Workup: Misc (active), and the MSG-owned [Triage: Workup Investigation for Messaging Threads](https://linear.app/canary-technologies/project/triage-workup-investigation-for-messaging-threads-06c5ea2fe204) (Matías, target 28 Aug, never started). Jake Wilhelm's [Thread Investigation Playbook](https://linear.app/canary-technologies/document/thread-investigation-playbook-workup-reference-e18d46d50373) says about 1 in 5 Oncall tickets are "why did the AI do X on thread Y", and the existing gatherer reads an end-state dump rather than the real middleware trace.

  ### What shipped 11-16 Sep

  - Checks can end a run early; every check declares `class: diagnosis|rule-out` (TOOL-691 part 1).
  - All nine Bowerbird messaging checks run inside Workup (#55178), with post-merge fixes (TOOL-690).
  - Workup reads the actual Zendesk conversation, not just attachments (TOOL-655). Prod check: 13 of 45 runs kept a conversation file.
  - Closed-form pipeline steps in Python (TOOL-691 part 2): about 1,100 lines plus 88 tests; the orchestrating skill shrank by 317 lines; model-written tool-traffic telemetry deleted.
  - Groundcover evidence links in the report (TOOL-609, Sam). Explicit gatherer list for the loop's entry point (TOOL-694, Sam). Classify-area always gets ticket prose (TOOL-695, in review).
  - Fallback comment when the handoff fails (TOOL-598). Stop declaring a routed ticket a duplicate of itself. Tickets missing info are handed to Workup rather than short-circuited.
  - Agents repo: E2B template rebuild in GitHub Actions plus stale-template alert (#193, #194); a PreToolUse hook forcing synchronous sub-agent dispatch after production runs obeyed the prose instruction only half the time (#202, unverified in prod); Bun idle timeout fix (#196); Snowflake query attribution (#210).
  - SQL tool: `McpSqlQuery` audit model, `SqlExecutionService`, agent identity denial for URL scraping (TOOL-618, 624, 626).

  ### In flight and waiting

  | Item | Who | Waiting on |
  |---|---|---|
  | SQL tool auth (TOOL-620): Pomerium JWT bearer path is not in a Pomerium release until Oct-Jan. Option D (pass-through plus app-layer token check) accepted 15 Sep by Alina with conditions: token checked in mcp-server, issued only to Workup sandboxes, "missing or bad token must deny, with no fallback". Bernard vetoed a migration ticket to Sallyport; Aditya confirmed Sallyport is staging-only. | Asher | Nobody owns the eventual migration. |
  | Bernard's second-pass review of the SQL design (16 Sep, 8 comments, one he calls a blocker for US enablement): the design and seed blocklist disagree on whether prefix rules exist, so a new vendor table with a plain-text credential would be granted whole and the drift check keyed on `EncryptedCharField` cannot see it. Also: throttle and daily quota collapse into one control; data-modifying CTEs missing from the regression list; Agent Vault shared proxy token exposure. | Asher | Reconciliation. |
  | TOOL-611 dedicated OpenAI key with zero data retention for the SQL judge | Asher | Untouched since 3 Sep. |
  | Security PR stack in the agents repo (#197-#203): per-sandbox HMAC identity, the first PR CI, security toolkit at sandbox boot, `secagent`. About 5,400 lines, three days old, no reviewer assigned. | Bernard | A reviewer. |
  | Judge outbound-ask rule (#207) and redaction breaking JSON evidence (#211: 45 of 274 stored evidence rows unparseable) | Laura | Review. |
  | Arrivals/Departures gatherer (#55360) and agent_context providers (#55356) | Guido | Internal Tools review, 13 days. |
  | PMS-10486 gateway-content reads in the investigation formatter (four PRs) | shadowrider17 | Review. |
  | MCP Search KB tool (#55802) | Martijn | Review. |
  | Retire Teleport auth path SEC-586/587 (#54542) | Bernard | 20 days. |
  | Comms core checks PR to Monty | Laura | Sent (9 Sep action). |

  ---

  ## 5. The numbers

  All from https://agents.cnry.land on 16 Sep unless stated.

  **Next-step correctness (bucket AND specific object)**

  | Window | Correct | Scored | Right bucket only | Eligibility |
  |---|---|---|---|---|
  | 7 days | 23% | 39 | 33% | 43 of 51 resolved (84%) |
  | 30 days | 29% | 109 | 42% | 116 of 217 (53%) |
  | All time | 28% | 116 | 40% | 116 of 259 (45%) |

  Judge: `uncalibrated` (eval measured a different prompt). Agreement 74% (64-81%), n=95. Cause judge 83% all time. 11 human-vs-judge disagreements open. 14-28% of rows decided mechanically. 0 of 116 tickets resolved end to end by Workup.

  **Confusion.** Declared Code Fix (n=32) graded as Duplicate 9, Escalate 6, No Action 6, Config 4, correct 7. Declared Config Change (n=25) correct 14, leaks to No Action 5. Sharpness given the right bucket: Ops 7/7, Config 8/14, Code Fix 4/7, Escalate 3/7. Calibration: high-confidence runs are right 71% (n=151), medium 52%, low 33%. Incorrect runs make 1.2x the tool calls of correct ones.

  **Per team (judged correct, partials count half).** CC 86% (30), PAY 75% (7), CUSTOPS 73% (11), MSG 68% (94), STAY 63% (9), INT 60% (63), PMS 59% (131, 22 no-diagnosis), SDM 50% (37), AD 14% (8), AK 0% (6).

  **Cause categories.** configuration 36/89, code_bug 27/100, expected_behavior 16/27, not_implemented 10/36, onboarding 10/30. code_bug at 27% on the largest volume is the worst cell.

  **Operations**

  | | 7d | 30d | All |
  |---|---|---|---|
  | Runs | 58 | 250 | 433 |
  | Avg cost per run | $8.64 | $10.98 | $11.17 |
  | Posted nothing | 1 | 49 | 87 |

  No-post rate fell from 20% all time to 1.7% this week. 331 of 433 runs (76%) ran with context gaps. $1,205 lifetime spent on runs that posted nothing. Cost this week $183.

  **Cost discrepancy resolved.** Dashboard usage: Workup $2,735 lifetime, 57% of all agent spend ($4,830). At 8-13 runs a day and $9-11 a run that is $70-140 a day, consistent with Laura's "about $95/day". Blake's "900 or 950 a day" from the 26 Aug transcript is not supported by any dashboard figure *(inferred: a misstatement, or a different unit)*. The judge and eval sub-agents cost about $26 total, under 1% of what they measure. Runtime is restricted to Anthropic models; model is Sonnet 5.

  **Tool mix.** Context re-read 20,475 calls, code tracing 17,711, log queries 8,256 (`groundcover.query_logs` 7,450 across 312 runs). Engram: 77 remember calls across 6 runs, 8 recall calls across 3 runs. Snowflake MCP appears (73 calls, 12 runs). The Canary SQL tool does not appear yet.

  **Linear labels, 17 Aug to 16 Sep.** 161 next-step labels: Code Fix 38, Config 34, Ops 31, Escalate 20, Feature Request 19 (15 of them MSG), Duplicate 10, No Action 5, Request Info 4. `Workup: Investigated` about 230, `Workup` over 250. So roughly 70% of investigated tickets carry a declared next step. `Workup: Needs Info` has never been applied. Misrouted (AI routing, adjacent) 41.

  **Sandboxes.** Retention only reaches back to about 9 Sep, so the cap-killed runs PMS-10139 and ONC-26129 are gone. Every retained Workup sandbox is an ONC ticket. There is no cap-killed state in the UI.

  **Expansion signal.** The bot page shows team-level prompt overrides for Customer Activation and Enterprise already exist, despite the onboarding pause. *(inferred: check whether that is deliberate.)*

  ---

  ## 6. Strategy

  ### As stated in the docs

  - **Problem.** "Canary currently spends 20-30% of engineering time on triage, oncall, and investigation work... This will be the top focus for Q3 Block 2." (26Q3B: Prioritizing Triage Efficiency, Blake and SJ.)
  - **Org success metrics.** Number of Oncall issues; % of Zendesk tickets that become an Oncall issue; Oncall resolution latency p50/p90; "Next step acceptance rate for the Workup".
  - **Internal Tools throughline.** "Decrease Engineering Support Dependency." SJ via Blake: "avoid going too wide, laser focus on communications and messaging/comms core, reevaluate in 2-4 weeks." Second goal: "maximize end-to-end AI accomplishment", push tickets all the way through so support can close without engineering.
  - **Priority order (12 Aug).** 1 Next-Step Metric ("required before other workup work"), 2 Canary MCP takeover, 3 Accuracy, 4 Interactive Investigations, 5 KB, 6 Model Benchmark.
  - **Steph's block goal (1 Sep).** Workup "moves from posting a diagnosis to naming the exact next step and the specific record to act on."
  - **Harness direction.** Q3B plan says move toward OpenRouter rather than being locked into Claude Code. The runtime today restricts to Anthropic models.
  - **Data access doctrine (Blake, 5 Aug).** "Same stack that a software engineer at Canary has... without that level of data access we are always going to have a worse triage experience than a human." Obfuscation is not security; audit logging plus SIEM is. Write access deferred "as long as possible".
  - **Extensibility model.** Internal Tools owns the core pipeline; teams own gatherers, checks, resolvers and config-vs-capability instances.

  ### The bets underneath it *(inferred)*

  1. A calibrated next-step metric is the thing that lets leadership talk about trade-offs (Blake: "we found this problem with voice"). Everything else waits for it.
  2. Accuracy comes from structure, not model effort: cited claims, cheap checks first, branch before debate, a gate before posting. Evidence for the bet: incorrect runs do more work than correct ones, and the $8 Bowerbird plugin "may have the highest accuracy".
  3. Depth on Messaging beats breadth. Team-owned checks are the scaling mechanism; Internal Tools should not write every team's domain logic.
  4. Broad read access (SQL) unlocks the tickets Workup currently cannot investigate, and the audit log tells you which typed tools to build next.

  ### What has been dropped or paused

  Interactive asks (34% of runs end in an ask, 2% get a reply), KB Patterns, faster/cheaper runs as a project, model benchmark, Devin, cost optimisation until the new pipeline lands, onboarding new teams until next block.

  ---

  ## 7. Next priorities

  ### As the team states them

  1. **TOOL-607: selection goes live.** Shadow classification shipped 3 Sep; the 8 Sep update said cut over after "a few days of real data". Still Backlog, 1 point, and the 15 Sep update restates it as future. Named risk: if misclassification is common the team filter stays.
  2. **TOOL-608: config-vs-capability, Messaging first.** Unassigned. Laura ruled on 8 Sep that a check reads the value the sending code reads, and it should reuse `HotelService.validate_whatsapp_templates`. Prerequisite is a `whatsapp_templates` section on the hotel provider (TOOL-596, demoted to Medium). Until an instance exists, the branch stage "has nothing to short-circuit on, so the fast case stays theoretical".
  3. **SQL tool to prod US.** Grants, validation, admin, auth, egress pinning (TOOL-664/665), Cloudflare allowlist (TOOL-656), then staging validation (TOOL-637).
  4. **Phase 5, the loop** (TOOL-692, 693): termination conditions and debate gating.
  5. **TOOL-654 posting gate in shadow.** Unassigned, no priority. Laura's open design question: does evidence belong to a post or a run? Failed runs persist nothing.
  6. **TOOL-652 the 2.0.0 cut.** Unassigned, no priority.
  7. **Re-open onboarding next block** (Tipping, A/D, SDM already have gatherers), fix upstream checks first, "focus stays on Messaging".

  ### My read on what should be next *(inferred)*

  - **Re-run the judge eval before 24 Sep.** The Internal Tools block review is Thu 24 Sep. Right now there is no trustworthy headline number to present. The eval is cheap (under 1% of run cost). Get a second grader on the 26 pending and 11 disputed labels so the calibration is not Laura against Laura.
  - **Assign TOOL-607, 608, 652, 654.** These four are the critical path to the thing the strategy promises (short-circuit runs, a gate before posting, a release). Three are unowned.
  - **Decide the SQL tool date honestly.** 54 points open, 14 unowned tickets, a new blocker today, target in 9 days. Either staff it (Kevin and Sam are already helping) or move the date and say so.
  - **Write down the Option D conditions as a ticket.** Alina's deny-with-no-fallback conditions are the only thing between Workup sandboxes and the monolith DB and they live in a Slack reply.
  - **Confront 0% end to end.** Jason's metric is "triage tickets resolved without engineering in the loop". Workup's dashboard reports 0 of 116. Either the metric needs a definition that Workup can move, or Workup needs a path (the posting gate plus a support-facing next step) that lets a ticket close without an engineer.
  - **Onboarding: name a date and a reviewer.** Three teams did the work and are parked. Guido's PR is 13 days old. Goodwill is the scarce resource for a team-owned extensibility model.

  ---

  ## 8. Weaknesses and risks

  ### Quality and measurement

  - **Correctness is low and the number is soft.** 23-29% correct, judge uncalibrated, agreement interval 64-81%, and correctness excludes nulls so a rise can be a fall in coverage. Laura on 9 Sep: "the value for the actual correctness is pretty low right now. I'm trying not to focus too much on it." Defensible mid-rebuild, but there is no number for the block review.
  - **The taxonomy is disputed.** Config vs Ops is "hard for even me" (Laura). Escalate means vendor support to Blake and misrouting to Laura. No Action often should be Feature Request. You raised merging categories on 9 Sep; no owner or date was set. The judge rules (#169, #170, #183, #207) are being tuned against the same 95 labels they are evaluated on.
  - **One grader.** Laura does all hand grading and the judge is calibrated to her. 26 pending grades, 61 unjudged runs. She declined help on 9 Sep because seeing the errors is useful to her.
  - **Input quality, not reasoning effort.** 76% of runs have context gaps; 20,475 context re-read calls; incorrect runs do 1.2x the work. Six gatherers were silently parsing the wrong Groundcover path and returning "not found" for data that was present (found 9 Sep). Nothing in CI tests model-facing output quality; the only graded loop is the out-of-repo judge.
  - **A third of investigated tickets declare nothing.** 161 labels against about 230 investigated. `Workup: Needs Info` is defined and never used.
  - **Worst queues get no attention.** AK 0%, AD 14%, PMS 59% on the biggest volume with 22 no-diagnosis, code_bug correct on 27 of 100. None appear in any meeting notes.

  ### Cost

  - Blake deferred optimisation on 26 Aug and the numbers improved anyway ($11.17 to $8.64 per run, no-post 20% to 1.7%). The $30 cap has not been revisited. The cap is per attempt, so a retried run can spend multiples. There is no concurrent-sandbox limit (still unticked in the agents roadmap). Worst observed single invocation: about $57.
  - The cap truncates after the answer is found (PMS-9985). Garrett's cheaper-model idea is closed off by the Anthropic-only runtime; Dylan's $5 human checkpoint was parked.
  - Budget ceiling: Airbase card at $9k a month, "going to be filled up pretty soon" (27 Aug); Blake said he would raise it, not confirmed. Workup is 57% of agent spend and shares the pool with voice agents.
  - Budgets are meant to "tighten from telemetry, not taste", and the tool-traffic telemetry was deleted two weeks after it was added.

  ### Security and data

  - **SQL tool.** Threat model states plainly: "A steered single-row query about one named guest passes every volume cap and fires no monitor." One query on a granted join can assemble a guest's PII across any hotel; nothing bounds the aggregate. The Django user allowlist is now the only authorisation. The LLM judge fails open. `workup_run_id` is self-reported. The drift check keyed on `EncryptedCharField` already missed 182 sensitive columns across 89 tables on the first sweep; 75 tables have no Django model; four `cvv` columns exist; deprecated fields hide from Django but not Postgres. Alina's main pre-rollout concern (one very large row on the shared Django pool) is still an open thread.
  - **Auth is temporary.** Option D, no Pomerium JWT, Sallyport staging-only, no migration ticket. TOOL-611 zero-retention OpenAI key untouched since 3 Sep.
  - **Agents platform.** Every sandbox shares one `OVERLORD_API_KEY` and self-reports identity; signature verification is skipped in box mode; the fix (#197) is unmerged with no reviewer. Canary MCP trusts an unverified JWT behind a shared secret.
  - **Guest data.** Full tool outputs are persisted (31 Aug) and pseudonymisation, erasure and scope-check tickets are all unowned. Overlord's redaction corrupts JSON (`"generated_timestamp": GUEST_PHONE_35`), breaking 4 of 13 verification samples and 45 of 274 stored evidence rows; the JSON bug is in #211, the timestamp bug is not filed.
  - The 5 Aug "breaker" (cut internet once an agent touches PII) is still "Needs Further Discussion".

  ### Delivery and ownership

  - **Bus factor.** Laura: 54 of 104 canary commits on Workup paths, 62 agents-repo PRs, every design doc, every hand grade, essentially all of `core/` and `pipeline/`. Yeh Fang: 84 agents-repo PRs, all infra. Asher: alone on the SQL tool, holding all five in-progress tickets. Laura's parental leave is about three months out and she flagged it to you on 1 Sep.
  - **Reporting is absent.** No initiative update ever; six of nine projects never posted one; no health or target on the initiative. The only narrative is Laura's two Accuracy updates. Cycle 3 scope grew from 34 to 67 issues mid-cycle. Cycle 4 is empty.
  - **Half the initiative is inert or stale.** Four projects with zero issues; two cancelled; one paused. The overview page contradicts three of them (Patterns, more teams, faster runs).
  - **The pipeline is half-built and says so.** The branch "spares the debate, not the wave": every run still pays the full up-front gather cost. Classification gates check selection but not gathering. Resolvers are PMS-only. Nine comms checks now exist as copies in two plugins with nothing enforcing sync. The short-circuit bar text is mirrored in two skill files with an "edit there first" note.
  - **Prose contracts keep failing.** Three PreToolUse hooks now exist to force behaviour the prompt asked for and the model ignored (sync dispatch, Snowflake attribution, image reads). The submit contract exists because transcript scraping was hijacked in production. Each new instruction needs its own enforcement mechanism.
  - **Platform hygiene.** No PR CI in the agents repo (the first is unmerged in #198); no staging; 14 of 133 PRs merged with zero reviews; silent failures recur (template builds failed six nights with no signal; cron jobs vanish when a credential is rotated to empty; Bun returned 200s with truncated bodies). Four zombie PRs 100-170 days old. Local checkouts drift (yours is 596 commits behind master), and laptop runs record `pipeline.git_sha` as "unknown" from the marketplace cache.
  - **SQL tool integration risk.** About 1,000 lines merged with no caller, while validation, grants and admin are open across three authors, and a competing 48-day-old PR (#51853) from Applied AI is still open.
  - **Plugin and data-plane hygiene.** The bindings file routes entity config through both the old token-based script and the new MCP tool that "replaces" it; a team gatherer still carries a copy of the old client. The agent_context README points at a triage plugin that does not exist. The MCP tool docstring hard-codes the provider list. Only the dx plugin has a version-match test, so investigate 1.15.0 has no guard (the fix is #56250, open). Skill-quality review is workflow_dispatch only and the structure workflow posts advisory comments rather than failing, so the roughly 40 investigate skills have no blocking quality gate.

  ### Organisation and adoption

  - **Metric versus ownership.** Jason's first metric is triage tickets resolved without engineering; Workup stays owned by the pod. Blake and Jason already disagreed publicly (24 Aug) on how hard the framework is to adopt. Jason's charter (15 Sep) says pods own all AI infrastructure. Jason told you Laura "sends me too many claude outputs" and his coaching line is that she should explain generated output herself.
  - **Golem overlap unadjudicated.** Ryan read the Workup design, concluded "not too much overlap, but that may have evolved", and shelved Golem. Platform holds Golem. The Enterprise rubric is already mapped onto the Workup judge. Nobody has decided whether ENT converges. For comparison, Golem's 13 Aug calibration was 37% strict (one-shot) and 61% counting assists at half, on 40 tickets, against Workup's 28% bucket-and-object or 40% bucket-only. The two are not measuring the same thing.
  - **Adoption goodwill.** MSG is the only formally live pilot in the narrative, yet the dashboard shows 14 teams with runs and ENT/CA prompt overrides exist. Tipping, A/D and SDM are parked with gatherers written. Support is asking Workup to stop reopening Zendesk tickets (AWT Rule Adjustments, on hold).
  - **Thin engineer feedback.** For a production agent two months in, there is almost no written reaction from MSG, CC or INT engineers to actual diagnoses. The quality signal is Laura auditing her own agent. The one sharp user critique (João, TIP-5329): "When I put this in my Claude, the same ask, it was able to fetch the information needed." Laura fixed it the same day.
  - **Engram.** Approved 5 Aug, "enabled", caused the worst incident, and is now effectively unused (77 remember calls across 6 runs). Jason owned it; nobody has formally dropped it.
  - **Misroute rate rose** from 4.7% to 6.8% week on week (adjacent AI routing), with INT at 25% on small numbers, and INT is a team that wants Workup.
  - **Your own signal.** Tentative on every Internal Tools weekly, unanswered on every Workup sync and on the Internal Tools block review (Thu 24 Sep 21:15).

  ---

  ## 9. People

  | Person | Role in Workup | Notes |
  |---|---|---|
  | Laura DeWald | Owner. Agent, judge, dashboard quality view, plugin core, all docs, all grading | You manage her since 14 Sep. Parental leave roughly Dec. Jason and Blake both say she is at or above level and has grown; coaching theme is putting work in front of people and explaining it herself. |
  | Blake Van Landingham | Sponsor, final decision on security and cost | "Workup has to have the same workbench as a senior engineer." Holds an open question on whether Overlord is overbuilt versus buying. |
  | Jason Flax | IC on the AI platform since 14 Sep; Engram and dashboard author | Metric: tickets resolved without engineering. Sees Laura shifting toward "Workup GUI work as his orchestration layer matures". |
  | Asher Davidson | SQL tool, alone | "A little tired of writing design docs." Skip-level with you Thu 17 Sep. |
  | Sam Kariu | Second Workup contributor (TOOL-598, 609, 694, 695, 628) | Berlin, EU Blue Card route agreed. |
  | Kevin Cormier | SQL validation module (TOOL-625) | |
  | Yeh Fang | Agents platform, E2B, Golem infra | 84 PRs. |
  | Bernard Pietraga | Security; blocklist review; agents-repo security stack | Blocker comment today. |
  | Alina Glumova | Security sign-off | Conditional OK on Option D. |
  | Stephanie Barry | Product point; block goal author | Upstream Zendesk work not reported since 5 Aug. |
  | Julius Seporaitis | Plugin co-owner (CODEOWNERS); PMS frontier | |
  | Dylan Moradpour | Ex-owner of Canary MCP (Applied AI); author of the old SQL PR | |
  | Matías Marcó del Pont | MSG; comms checks reviewer; owns the never-started thread investigation project | |
  | Guido Percu, João Bueno, Luiza Manhães | A/D, Tipping, SDM gatherer authors | Parked. |
  | Ryan Rogers | Golem author (shelved) | "Be aware of Workup." |

  ---

  ## 10. Decisions log (compressed)

  - 5 Aug: Engram adopted; audit logging plus SIEM over obfuscation; write access for hotel setup not triage; auth-based tool scoping.
  - 6-12 Aug: Next Step metric adopted; Canary MCP to Internal Tools; raw SQL over ORM; investigate skills migrate to MCP; SQL tool priority 2.
  - 26 Aug: no cost or model optimisation until the new pattern lands; cap $15 to $30; SQL via Django raw SQL, deny-list not allow-list, semicolons blocked, LLM judge on OpenAI; payment, mobile-key and HR gateway config stay queryable.
  - 3 Sep: no new teams until plugin tweaks land, "hopefully next block".
  - 9 Sep: SQL tool approved, read-only, Workup-only; judge non-blocking; write actions deferred; rollout to non-EPD after Workup; Devin removed. Laura 1-1: fix upstream checks first, then teams, focus on Messaging.
  - 14 Sep: Team Enablement via KB cancelled. Jason's role live; Workup ownership stays with the pod.
  - 15-16 Sep: Option D auth for the SQL tool "for now"; Sallyport is staging-only.

  ---

  ## 11. Questions to settle and suggested agendas

  ### For Laura, tonight (Wed 16 Sep 21:30)

  1. Transition: cadence, what she needs from you versus Jason, who sets Workup priorities, how she wants Jason's feedback handled.
  2. The 24 Sep block review: what number will she present, and can the judge eval be re-run and a second grader added before then?
  3. Ownership of TOOL-607, 608, 652, 654. Who, and when?
  4. SQL tool: honest date, Bernard's blocker, staffing beyond Asher, writing Alina's conditions into a ticket, TOOL-611.
  5. Onboarding: a dated re-open plan and a named reviewer for #55360 and the SDM work. ENT and CA prompt overrides: deliberate?
  6. Parental leave: coverage plan for the judge, grading and the plugin core. Who is the second author?
  7. Project hygiene: close or re-date Staged Rollout and Faster/Cheaper; post an initiative update; fix the overview page.
  8. Engram: land it or drop it.
  9. Guest data handling tickets: owner and priority, given full outputs are already persisted.

  ### For the Workup sync (Wed 16 Sep 18:30) if you attend

  - Onboarding re-open plan and gatherer PR reviewers.
  - The 0% end-to-end number and what a Workup-resolvable ticket looks like.
  - A joint eval of Golem and the Workup judge on shared PMS tickets.

  ### For Asher skip-level (Thu 17 Sep 21:15)

  - What would make 25 Sep real. What he wants taken off his plate. Option D and the migration nobody owns.

  ### For Blake (next Directs, Mon 21 Sep)

  - How next-step correctness (Laura) and resolved-without-engineer (Jason) fit together without competing.
  - Cost ceiling and the Airbase raise.
  - Whether "next block" for onboarding is a commitment, and who tells the waiting teams.
  - Golem versus Workup for ENT.

  ### Strategic questions still open

  1. Should ENT converge on Workup (contribute gatherers, checks, the PMS config-vs-capability check) or keep Golem? Lose: KB playbook, DB-script mode, misroute detection. Gain: shared judge, dashboard, SQL tool, EU/AP.
  2. Is a deny-list plus a fail-open LLM judge defensible in an enterprise security questionnaire (PII, PCI, credential-manager)?
  3. Team-owned checks have nobody scheduled to write them. Staff from ENT/PMS?
  4. Is the current spend and a 76% context-gap rate acceptable past this block?
  5. Whose metric is it: next-step correctness or resolved-without-engineer?

  ---

  ## 12. Links

  **Dashboards and code**
  - Dashboard https://agents.cnry.land/workup · bot https://agents.cnry.land/bots/workup · usage https://agents.cnry.land/usage · sandboxes https://agents.cnry.land/sandboxes
  - agents repo https://github.com/canary-technologies-corp/agents (README rewritten 9 Sep is the best single source; `overlord/docs/ARCHITECTURE.md`)
  - canary repo: `agent-plugins/claude-plugins/investigate/` (read `core/pipeline.md`), `backend/canary/linear_agent/workup/`, `backend/canary/canary_mcp/`

  **Linear**
  - Initiative https://linear.app/canary-technologies/initiative/workup-2a7616f589a4
  - Accuracy update 15 Sep https://linear.app/canary-technologies/project/ai-workup-accuracy-1bfe6e72996f/activity#project-update-08615feb
  - Next-step tickets view https://linear.app/canary-technologies/view/next-step-tickets-69f507a962f4
  - Key issues: TOOL-607, TOOL-608, TOOL-620, TOOL-652, TOOL-654, TOOL-611, TOOL-642/643/644

  **Notion**
  - Overview https://app.notion.com/p/3b281468615181abab24cc07d8889847
  - Sync agenda https://app.notion.com/p/3c281468615181a1a88fca0b5fea0b94
  - Unified investigate plugin (readable) https://app.notion.com/p/3bf81468615181e58428e5a18d91433c
  - Next Step metric https://app.notion.com/p/3b38146861518008b312fa94262e4ef4 · judge spec https://app.notion.com/p/3c28146861518170a05fdbcf46a6f7d2 · how the judge works https://app.notion.com/p/3bb8146861518180a37adab608e88e5c
  - SQL tool design https://app.notion.com/p/3c8814686151808c8231f5997b870632 · requirements https://app.notion.com/p/3c281468615180a6a89bc4b5b99a60dc · seed blocklist https://app.notion.com/p/3c681468615181d2be85ff5f38d7ab26
  - Interactive Investigations PRD https://app.notion.com/p/3b9814686151818b9e09f189f1499888
  - Q3B triage efficiency https://app.notion.com/p/3ad81468615180c19a9bea1d7ef4e00a · Internal Tools Q3B plan https://app.notion.com/p/3b1814686151816cb470da06f103f965 · MCP handoff doc https://app.notion.com/p/3b88146861518094a6a1c2429d03ad84 · accuracy baseline https://app.notion.com/p/3b181468615181b08f37c0629c1619e8
  - Jason's charter https://app.notion.com/p/3dc81468615180169535c00ed0382183
  - Workup readiness by pod https://app.notion.com/p/0515d25d35674bac8ae2de616cda74f5

  **Meeting notes**
  - 5 Aug https://docs.google.com/document/d/1pR_vFnbnykKd2v2vU9KVloIbG3ooAT1pCtiYngPp5xI/edit
  - 12 Aug https://docs.google.com/document/d/1kUbxDiMWronnnOD4AAq5cRVF_k6NvTPHvtnyJcJBXw4/edit
  - 26 Aug https://docs.google.com/document/d/19XTmIdZfr7jU1cMNlcwoFRBLJFnIz3qibO4LwviTtxA/edit
  - 9 Sep https://docs.google.com/document/d/1i-IOhiSYeRAbePmuEb51IfIaaxGOw2rhwz95pnkk7KM/edit
  - Granola: Laura 1-1 9 Sep b4a5a969-ac49-4e75-a3da-c2e612552c24 · Ryan 10 Sep 3c838ff3-9785-4eeb-af9b-7fbf0a47efdc · Blake directs 14 Sep 37abd252-b8f9-4948-8761-9a4bc16fce03

  **Slack**
  - #project-workup https://canarytechnologies.slack.com/archives/C0AL1T2H43V · #eng-agents https://canarytechnologies.slack.com/archives/C0AR52PPU4Q · #epd-internal-tools https://canarytechnologies.slack.com/archives/C0AMJPBUH60
  - Engram incident audit https://canarytechnologies.slack.com/archives/C0AR52PPU4Q/p1786926224766839
  - Cap kills (Ashish) https://canarytechnologies.slack.com/archives/C0AR52PPU4Q/p1787644350359229
  - Budget thread https://canarytechnologies.slack.com/archives/C0AR52PPU4Q/p1787860102473649
  - Option D auth thread https://canarytechnologies.slack.com/archives/C0AL1T2H43V/p1789405419481249 · Alina's conditions https://canarytechnologies.slack.com/archives/C0AL1T2H43V/p1789491765071779 · Aditya on Sallyport https://canarytechnologies.slack.com/archives/C0AL1T2H43V/p1789548903262669
  - Luke Curran platform footguns https://canarytechnologies.slack.com/archives/C0AR52PPU4Q/p1788981896770899
  - Stale template incident https://canarytechnologies.slack.com/archives/C0AR52PPU4Q/p1789058382055819
  - Jason's role announcement https://canarytechnologies.slack.com/archives/C03P563GB4M/p1789393518374619
  - Guido blocked https://canarytechnologies.slack.com/archives/C029BPP02H0/p1788543620053219 · João TIP-5329 https://canarytechnologies.slack.com/archives/C0AL1T2H43V/p1788303495256679

  **Caveats**
  - The normative plugin design page is not shared with the Notion integration; the readable companion was used.
  - Cap-killed runs could not be inspected; sandbox retention only reaches 9 Sep.
  - The dashboard's week-on-week delta direction could not be read.
  - "Lauren" in Granola's Jason handover notes is taken to be Laura.
  - No external writes were made. Nothing was posted, RSVP'd, or created in Notion.


  ## Agent run 2026-09-16T16:04:32 (follow-up)

  **Asked:** "Review your draft. directive: I need condensed catch-up material not exhaustive context. Publish notion as private doc for me. Create a /gtd item to read it, in inbox"

  - Condensed the draft to about 1,600 words (what it is, where it is, last week, strategy, next priorities, eight weaknesses, this week's agendas, links).
  - Published as a PRIVATE Notion page with your approval: https://app.notion.com/p/3dd8146861518127a5baca7c17b32a0e ("Workup catch-up brief (16 Sep 2026)"). Not moved or shared.
  - Captured inbox item: data/work/inbox/2026-09-16T1604-read-the-workup-catch-up-brief-before-tonight-s-la.md
  - The exhaustive version remains in the previous agent-run section above and at the scratchpad path.
project: 2026-09-08-workup
source_id: null
tags: []
time_minutes: 15
title: I need to be more on top of workup. I'm behind the curve. Plan a catch-up investigation
updated: 2026-09-16 21:35:56.696579
waiting_on: null
waiting_since: null
working_on: false
---

https://docs.google.com/document/d/19XTmIdZfr7jU1cMNlcwoFRBLJFnIz3qibO4LwviTtxA/edit?tab=t.t81tvqup3p4s