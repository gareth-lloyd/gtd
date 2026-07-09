---
area: null
contexts: []
created: 2026-07-08 16:40:08.330014
defer_until: null
due: null
energy: low
id: 2026-07-08T1640-review-what-golem-is
order: null
output: |
  ## Agent run 2026-07-08T20:05 — What is Golem?

  ### TL;DR
  Golem is Canary's **autonomous coding agent**: assign it a Linear ticket (or
  @mention it in Slack/Linear/GitHub) and it investigates, writes code, opens a
  *draft* PR, spins up a live-branch preview when there's a visual change,
  responds to review comments, and fixes its own CI failures — owning a ticket
  end-to-end like an engineer would. It is one of several bots built on Canary's
  shared **Agents Framework** (siblings: Triage Bot, Kiosk Bot / "Pops",
  Showroom Bot, PMS Capabilities Bot, Mephisto).

  **Important nuance:** the code does NOT live in this monorepo. A recursive
  search for `*golem*` here returns only *integration hooks* (branch-name
  carve-outs, the `megolem` bot service account, the `ByGolem` PR label, live-
  branch deploy scripts). Golem's own source lives in a **separate repo**:
  `canary-technologies-corp/agents` (the "Overlord" server). See "Where it lives"
  below.

  ### What it actually provides
  - Delegated, end-to-end ticket execution in the cloud (no local dev env needed
    — usable by PMs/non-engineers too).
  - Listens across **three surfaces** and resumes the *same* sandbox/session on
    follow-ups (keeps full context): Slack (DM/@mention), Linear (assign/@golem/
    agent sessions), GitHub (PR comments; auto-reacts to its own CI failures).
  - **Live Branches**: auto-claims a per-PR preview env (`live-golem-*.env.
    canarytechnologies.com`) when a change is visually verifiable, deploys its
    commit, posts the URL. (Requires Cloudflare WARP to view.)
  - Runtime = **Claude Code CLI** (`claude -p --dangerously-skip-permissions`)
    inside an **isolated E2B sandbox** with a full clone of the canary repo.
    Default model **Claude Sonnet 4.6** (centrally configured, admin-only).
  - Uses the repo's own `CLAUDE.md`/rules + the **canary-plugins** marketplace
    (core, backend, testing, dx bundles). Integrations: Linear, log search,
    live-branch tools, Slack, read-only DB workbench, Groundcover (MCP), Notion,
    Sentry, Datadog.
  - Dashboard at **https://agents.cnry.land** — per-ticket cost/usage, run
    progress, prompt stack (global agent prompt → team prompt → personal prompt),
    connected accounts.

  ### Where it lives (code-wise)
  - **Own source (external):** `canary-technologies-corp/agents` — the "Overlord"
    server (Bun on EKS/Karpenter). Not in this monorepo. To read the agent loop /
    prompts / control plane, look there. Grep terms: `Overlord`, `megolem`,
    `defineAgent`, `claimLiteEnv`, `execLiteEnv`.
  - **v1 architecture:** Deno monorepo, 4 Fly.io apps (orchestrator, scanner,
    syncer, dashboard) + E2B sandbox-per-work-item + Supabase (state/metrics) +
    Anthropic. Substrate moved Fly VMs → E2B along the way.
  - **v2 architecture:** collapses the 4 Fly apps into a single **Overlord**
    server on EKS. Ingests Slack/Linear/GitHub webhooks + a direct API, matches
    events to agents, runs them in-process (Pops, Mephisto) or in an E2B sandbox
    (Golem, OpenCode session; 90-min base timeout, +40 min per event). Messages
    stream to Supabase Realtime; per-ticket cost via E2B lifecycle webhooks into a
    `golem_ticket_costs` view.
  - **Integration hooks in THIS repo** (for reference, not the framework itself):
    - `CLAUDE.md:75` — names Golem as an autonomous no-human runtime.
    - `backend/pms-gateway/CLAUDE.md:22-31` — "Running in Golem (E2B sandbox)".
    - `.github/workflows/live-branch-dev.yml:136-214` — `golem/*` branch lifecycle
      carve-outs (Golem claims its own pod via `claimLiteEnv`).
    - `.github/live-branch/lite-env-deploy.sh`, `.github/live-branch/k8s/
      overlord-rbac.yaml` — overlord-mediated deploy/exec + RBAC.
    - `.github/scripts/workflow_monitor.py:846` — `megolem` GitHub service account.
    - `scripts/github_action_backend_lint.sh:24`, `canary_front_end.yml:157` —
      `ByGolem` PR label opts into auto-lint-fix.

  ### Advantages
  - **Real throughput lift** (per the internal retro): teams shipped ~75
    tickets/wk before Golem, ~93/wk after; in Golem weeks, 50%+ of shipped tickets
    were Golem's. Cheap: **$2.28 avg/ticket** ($1.79 p50, $6.27 p95).
  - Great for **well-scoped pipelines**: the standout win was **Sentry → Linear
    ticket → investigate → PR** automation, clearing long-tail low-priority bugs
    no one would otherwise touch. Also lowers the bar for "quick" PM asks.
  - Parallelism: fire off many tickets, plan the next while they run.
  - Background execution — works while the human is away.
  - Built on the shared Agents Framework, so shipping a *new* bot is cheap
    ("as little as an hour").

  ### Disadvantages / limitations
  - **Bad runs are painful**: "a good Golem experience is great, but a bad one is
    absolutely terrible" — you're half-invested in a direction that may not work,
    stuck steering an agent awkwardly over GitHub/Linear. Retro advice: better
    selection criteria + revert early rather than push through.
  - **Review burden**: AI PRs need special attention; long review lists can leave
    PRs stuck. Perceived (not measured) slowdown from this.
  - **Narrow scope**: only solves a slice of "partial coding agents" (repo, no
    full dev env). No background/generic-goal agents, no full dev environment
    (no pnpm install / Postgres / Redis / migrations at job time — worker image is
    scoped to lint/tests).
  - **Bespoke-infra debt** (the core argument of the "Golem → Cloudflare" design
    doc): no durable execution (sandbox death loses in-memory state), weak secret
    boundary (secrets live *inside* the sandbox; tokens embedded in git remotes),
    no HITL/approval primitives, no sub-agents, no MCP governance, hand-rolled
    scheduling/queues/observability. Output quality is directly proportional to
    tokens burned (throttled thinking → worse output).

  ### Strategic direction (as of Apr–Jul 2026)
  There's an active design doc — **"Golem → Cloudflare"** (Status: TODO, Team: AI)
  — arguing Golem proved the *product shape* but the *runtime layer* should move
  onto Cloudflare's Agents platform (Durable Objects, Workflows, HITL primitives,
  sub-agents, MCP governance, safer sandboxes via `outboundByHost`). Thesis:
  "Own the product layer. Do not own the commodity runtime layer." E2B would
  remain only as a long-lived-execution escape hatch (Cloudflare Sandbox caps
  sessions at 30 min) until that cap lifts. Not yet decided/executed.

  ### Key sources (Notion / Linear)
  - Meet Golem (Agents Framework) — user guide:
    https://app.notion.com/p/390814686151814c9100f817708f84ba
  - Agents Framework (overview / other bots):
    https://app.notion.com/p/32d814686151807f8e3ce199e984ad37
  - Golem → Cloudflare (design doc, v1/v2 architecture + tradeoffs):
    https://app.notion.com/p/34b81468615180a09fbff9099f147cf7
  - Summary (productivity retro / metrics):
    https://app.notion.com/p/3538146861518012a371d3a158387103
  - Canary's Agent Platform:
    https://app.notion.com/p/3668146861518076b427c6fcd546c261
  - Linear project "Golem Experiment" (e.g. GOL-14 Research Open SWE):
    https://linear.app/canary-technologies/issue/919ae944-b2b5-4f04-8ac1-a5e3dcfe8472
project: null
source_id: null
tags: []
time_minutes: 5
title: review what golem is
updated: 2026-07-09 13:37:31.521781
waiting_on: null
waiting_since: null
working_on: false
---