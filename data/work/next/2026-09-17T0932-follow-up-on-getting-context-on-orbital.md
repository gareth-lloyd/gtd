---
area: null
completed_at: null
contexts:
- consume
created: 2026-09-17 09:32:17.557834
defer_until: null
due: null
energy: low
id: 2026-09-17T0932-follow-up-on-getting-context-on-orbital
order: 3
output: |-
  ## Agent run 2026-09-21T14:55

  ### Correction to the item body
  Jason DID answer both DM questions on 2026-09-16 (they're in the DM, not threaded, so easy to miss):
  - Focus TLDR (https://canarytechnologies.slack.com/archives/D0A3G9PF066/p1789580769660799 and the ~8 messages after it): people alpha-test Orbital, "which is going to replace overlord (basically)" -> then he mounts it into Canary -> migrates Workup's workflow into Orbital -> adapts Laura's eval suite to prove output improves -> expands outward. He also wants to sit with your team to push operational workflows into Orbital, "so the sooner you start looping me in the better".
  - Target metric: "Loosely" / "Make workup great again" (https://canarytechnologies.slack.com/archives/D0A3G9PF066/p1789584415251759). So no hard number. The closest thing to a definition is the four axes in his channel explainer: correctness, ticket outcomes (incl. reopens/rework), human effort, time+cost per verified outcome, measured against Workup's current baseline.
  Nothing is outstanding with Jason on this item.

  ### One-line definitions
  - **Overlord** = the agent ROUTER that exists today. One pod (`overlord-web`, ns `canary-agents`, repo canary-technologies-corp/agents) that takes Slack/Linear/GitHub/API/cron events, matches an agent, and runs it in-process ("shared") or in a per-thread E2B sandbox ("isolated"). Turn primitive is `claude -p`. Supabase Postgres behind it, dashboard at agents.cnry.land. The README already calls it "the agent router"; "overlord" survives only in pod/env/secret/hostname names. (A June doc proposed renaming it "Perch"; Jason now says the name is going away in favour of Orbital or whatever Orbital gets renamed to.)
  - **Workup** = one of ~10 agents HOSTED BY Overlord (siblings: golem, triage, voicemine, voicequality, voiceinsights, pops, mephisto, showroom, pmscapabilities). `overlord/src/agents/workup/agent.ts`, Claude Code, Sonnet. Triage agent hands off -> Workup claims the Linear session -> gather context / debate hypotheses / deliver diagnosis in a sandbox, using the `investigate`, `comms-core`, `msg` plugins from the canary repo plus canary-mcp-{us,eu,ap}, groundcover, linear, engram. It can only post what goes through its one-tool `submit_diagnosis` MCP. Laura's quality suite (`overlord/src/workup-quality/`, hourly judge, agents.cnry.land/workup) scores each diagnosis against the eventual resolution.
  - **Engram** = the persistent-memory service. Jason's own project (Swift; `memory-hooks` binary; depends on his private jsflax/SwiftLM), server moved into the org as canary-technologies-corp/engram-server on 2026-08-11. Deployed as `engram-web` + `engram-tei` (embeddings) in the same namespace, secret `canary-agents-engram`. Two integration points: (1) an HTTP MCP (`mcp__engram__*`) the agent calls to recall/store, (2) Claude Code hooks that inject an "advise" block at session start and record the session. Overlord mints per-agent tokens (`overlord/src/core/engram.ts`), fail-open, gated by the per-agent `memory` dashboard flag. Went live for Workup on 2026-08-12. Memory graph is visualised on the dashboard agent page.
  - **Lattice** = the sync/data layer under both Engram and Orbital (rooms are `.lattice` files synced over WSS to a relay). You'll see it in ORB tickets; it is foundation, not a product.
  - **Orbital** = Jason's in-house "software factory": orchestration substrate + GUI + harness. Native macOS app + iOS companion (Swift), with a Linux headless port (`orbital-loop`, `orbital-mcp`) done in Aug. Core nouns: workspace -> rooms -> agent tree (spine / fan-out workers / referee) stamped from templates; autopilot states; gates for human intervention. Not a swarm itself: it's where you build, run and watch swarms. Lives in its own repos (Orbital, orbital-kit, orbital-server) - NOT in canary-agents.

  ### How they fit (best guess)
  Today:
  ```
  Linear / Slack / GitHub / cron
            |
            v
   +-------------------+        +-----------------+
   | OVERLORD (router) |------->| dashboard       |
   |  match agent      |        | agents.cnry.land|
   |  shared | isolated|        | (+ /workup eval)|
   +---------+---------+        +-----------------+
             | boots
             v
   +---------------------------+      +-----------------+
   | E2B sandbox               |<---->| ENGRAM          |
   |  claude -p  = WORKUP      | MCP  | memory graph    |
   |  plugins, canary-mcp,     | +    | per-agent token |
   |  submit_diagnosis         | hooks| advise/recall   |
   +-------------+-------------+      +-----------------+
                 v
        Linear agent session (diagnosis)
  ```
  Target (Jason's direction):
  ```
   humans (mac / iOS app)      agents (via orbital plugin/MCP)
              \                     /
               v                   v
        +-------------------------------+
        | ORBITAL  workspace            |
        |  rooms / tasks / swarms       |
        |  templates, gates, fleet view |
        +---------------+---------------+
                        | "Canary mount"
                        v
        +-------------------------------+     +---------+
        | Canary agent environment      |<--->| ENGRAM  |
        | (what Overlord is today:      |     | room id |
        |  triggers, sandboxes, creds,  |     | = session|
        |  Agent Vault, permissions)    |     +---------+
        |   WORKUP = durable agent      |
        |   placed in a room/workflow   |
        +-------------------------------+
  ```
  The layering, in one sentence: Engram is the memory, Workup is a worker, Overlord is the current dispatcher, Orbital is the intended control plane that sits above (and eventually absorbs) the dispatcher.

  ### The part that is genuinely ambiguous
  "Replace overlord" has two readings and the evidence is split:
  1. Aug 6 plan, Linear project "Orbital Orchestration v1" (https://linear.app/canary-technologies/project/orbital-orchestration-v1-68cf45a49fb1): Orbital runs UNDER Overlord. New runner `overlord/src/core/runners/orbital.ts` beside `claude-code.ts`; swarm-flagged tasks get a room bootstrapped inside the E2B sandbox; `claude -p` stays the turn primitive; rooms sync to a relay hosted on engram-server; dashboard gets a read-only live room view. Exit criterion: "one real swarm under overlord, observed live". Key tickets FRO-207 (https://linear.app/canary-technologies/issue/FRO-207) and FRO-208 engram-into-room-turns (https://linear.app/canary-technologies/issue/FRO-208). All still Backlog.
  2. Sep 16-18 framing: Orbital is the top-level product and workspace, Overlord "going away as a name" (https://canarytechnologies.slack.com/archives/C0C1Z7G3WS2/p1789583599727319). New Linear team ORB, project "Orbital alpha" (https://linear.app/canary-technologies/project/orbital-alpha-cd269a2d7960) whose description says Orchestration v1 "remains a separate historical Linux/Overlord program until ownership is reconciled".
  My read: (2) is the vision and the branding, (1) is still the only concrete mechanism for getting Canary's agents into Orbital, and nobody has reconciled them. Overlord's hard-won parts (webhook spine, sandbox trust boundary, Agent Vault, spend caps, ACLs) have no visible replacement in Orbital yet, so expect "Canary mount" to mean Orbital driving/observing Overlord for a good while rather than Overlord being deleted. Only trace in canary-agents today: unmerged, flag-gated `/fleet` dashboard embed on `origin/jflax/fleet-config-view` (commit 8d1df76, 2026-09-03).

  ### Things worth knowing for Workup specifically
  - Current ORB work is almost entirely app polish (performance, iOS parity, settings, chat UI). No ticket yet for mounting Workup or adapting the eval suite, so the "first business milestone" has no scheduled work behind it.
  - The Linux port tickets (ORB-31..35) are Done and "[TPL-1] First canary swarm template" (ORB-5) is In Review, so the headless prerequisite for path (1) exists.
  - Engram v1 gaps Jason/Stephanie listed themselves (Engram Memory v2, https://linear.app/canary-technologies/project/engram-memory-v2-87763f19d2bb): group graphs readable but never written, episodes unsupported, no vector index (every KNN is a seq scan), recall-precision view unused. So Workup's "persistent memory" is per-agent only and unmeasured today. Shared-graph poisoning is their named top risk - relevant if Workup memories start steering diagnoses.
  - Bus factor: Orbital, Engram, Lattice are all Jason-authored Swift with a private dependency; Laura had to patch SwiftLM out of the manifest to build Engram locally (https://canarytechnologies.slack.com/archives/C0AR52PPU4Q/p1787076274150269). Daga raised build-vs-buy on 2026-09-17 (https://canarytechnologies.slack.com/archives/C0C1Z7G3WS2/p1789648703469819); Jason's answer was firmly "own every piece".
  - Your Unified investigate plugin work is unaffected per Jason: "I don't think it changes my work... that's all the info bespoke to our process, which will just move to orbital." Plugins are the portable unit across both worlds.

  ### Where to read more
  - Jason's explainer + reading list: https://canarytechnologies.slack.com/archives/C0C1Z7G3WS2/p1789506612904989
  - Orbital/Workup/developer relationship: https://canarytechnologies.slack.com/archives/C0C1Z7G3WS2/p1789583812346249
  - Overlord ops doc (best current description of the router): https://app.notion.com/p/3d18146861518128a91ad4862bd1ef17 ; code-side: `README.md` and `overlord/docs/ARCHITECTURE.md` in ~/projects/canary-agents (local clone is at 2026-09-17)
  - Workup user doc: https://app.notion.com/p/3b281468615181abab24cc07d8889847
  - Workup session ownership -> Overlord design doc: https://app.notion.com/p/39981468615180daae10dcd10c72b779
  - Engram rollout PR: https://github.com/canary-technologies-corp/agents/pull/118
  - Orbital swarm postmortem (Guest App one-shot, Jul 9-10) - best look at what a swarm run is actually like: https://app.notion.com/p/39a81468615181b98178de2b6cbc8781 (not read this run)
  - Promised but unwritten: FRO-195 "Orbital in the Canary stack" enablement doc (Stephanie, Backlog) https://linear.app/canary-technologies/issue/FRO-195 ; "Canary Agentic Platform Roadmap 2026" is referenced by both Linear projects but I did not locate it.

  ### Not verified
  I have no access to the Orbital / orbital-server / engram-server repos, so Orbital's internals come from Linear ticket text and Slack only. The "target" diagram is inference. Teleport-backed MCPs were down (session expired) but weren't needed.
project: 2026-09-08-workup
source_id: https://canarytechnologies.slack.com/archives/D0A3G9PF066/p1789563894657179
tags:
- morning-gtd
- slack
time_minutes: 15
title: 'Follow up on: getting context on orbital'
updated: 2026-09-21 14:55:53.677904
waiting_on: null
waiting_since: null
working_on: false
---

I parked this on 2026-09-16: 'Where can I get context on orbital?' Jason's explainer is in #eng-orbital-internal; my later questions to him (focus TLDR, target metric) are still unanswered.
https://canarytechnologies.slack.com/archives/D0A3G9PF066/p1789563894657179
https://canarytechnologies.slack.com/archives/C0C1Z7G3WS2/p1789583812346249

Perform wider search and come up with a brief best guess of how orbital, workup and overlord fit together, with architecture diagrams if helpful