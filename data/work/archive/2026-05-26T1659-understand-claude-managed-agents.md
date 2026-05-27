---
area: null
contexts: []
created: 2026-05-26 16:59:42.289978
defer_until: null
due: 2026-05-27
energy: low
id: 2026-05-26T1659-understand-claude-managed-agents
order: null
output: |
  ## Agent run 2026-05-27T11:05Z

  **TL;DR:** Claude Managed Agents is Anthropic's hosted agent harness — you
  hand them an agent config + a user message, they run the loop (tool calls,
  sandboxed container, web access, MCP) and stream events back. Launched as
  public beta at Code with Claude on 2026-04-08. Sits *between* the Messages
  API (BYO loop) and the Agent SDK (client-side harness).

  ### Mental model (three primitives)

  - **Agent** — persisted, versioned config: model, system prompt, tools,
    MCP servers, skills. Create once, reuse the ID. Don't put `agents.create()`
    in your hot path.
  - **Environment** — where sessions execute: Anthropic-managed cloud
    container *or* a self-hosted sandbox on your own infra (for compliance /
    data residency).
  - **Session** — a single running instance against one (agent, environment)
    pair. Stateful: persistent filesystem, conversation history, outputs all
    held server-side. Long-running (minutes → hours), pauses cleanly, resumes.
  - **Events** — bi-directional stream: user turns in, agent turns / tool
    calls / status out. SSE; persisted server-side so you can list/replay
    after a stream drop.

  ### Built-in tools

  Bash, file ops (read/write/edit/glob/grep), web search + fetch, MCP server
  hookups. Auth for MCP servers must go through Vaults (separate API), never
  inline in agent config. Anthropic refreshes OAuth tokens for you.

  ### When to actually reach for it

  - Long-running / async tasks where you don't want to babysit a loop.
  - Need a sandbox container with file I/O + bash without building one.
  - Stateful multi-turn work that needs to survive process restarts.
  - Multi-agent coordination (built-in `multiagent` config).

  ### When NOT to use it

  - Simple request/response → just use Messages API.
  - You want full control of the loop / custom orchestration → Agent SDK
    (client-side).
  - **PCI / strict PII / HIPAA workloads** — Managed Agents is *not* ZDR
    eligible and not under BAA coverage because state is server-side by
    design. Hard blocker for some Canary surfaces.

  ### Pricing

  Standard Claude token rates **+ $0.08 per session-hour** for the managed
  infra. So idle sessions cost real money — close them.

  ### Gotchas worth remembering

  - Beta header `managed-agents-2026-04-01` required on every request
    (SDK adds it automatically).
  - SSE has **no replay**: if you reconnect, list events and dedupe by
    `event.id` or you can deadlock the session on a missing tool result.
  - Agent updates are immutable versioned bumps; running sessions pin to
    their creation-time version, new sessions get latest by default. Pin
    explicitly if you need reproducibility.
  - Rate limits: 300 create / 600 read RPM org-wide, on top of normal
    tier limits.
  - Also available on Claude Platform on AWS with some feature deltas.

  ### So what for Canary / Unblock team?

  Most of our agent work today is LangChain/LangGraph tool-calling agents
  per `backend:ai-agent-cookie-cutter` — client-side harness, deterministic
  control flow, our infra. Managed Agents is interesting where we'd
  otherwise have to build:

  1. A sandboxed code-execution surface (none today; would need one for
     anything browsing/scripting on behalf of staff).
  2. Long-running background agents that survive worker restarts and need
     a persistent FS (e.g. ops automations, doc-processing pipelines).
  3. A "Claude Agent" embedded surface where the marketing/branding is
     allowed and we don't want to own the harness.

  Where it's a poor fit for us:

  - Anything touching PCI / PII (Wyndham OHIP, payments, guest data) —
    ZDR/HIPAA exclusion kills it for our hot path.
  - Chat / messaging agents we already run via LangGraph — replacing the
    loop buys us little; we'd lose deterministic control over retries,
    tool whitelisting, observability via Datadog/Sentry.
  - Anything where the $0.08/session-hour is going to dominate at our
    volumes — would need a real cost model before adopting.

  ### Suggested follow-ups (not done — your call)

  - Skim Code with Claude 2026 talks for production patterns and the
    Notion / Sentry / Rakuten case studies — they're the cited early
    adopters.
  - Decide whether to spike a self-hosted sandbox env for our infra so we
    could use Managed Agents on PHI-adjacent surfaces. (Probably not worth
    it yet.)
  - If the team wants this as a deliverable, write a 1-pager comparing
    Managed Agents vs. our LangGraph stack for a specific use case (e.g.
    long-running onboarding-script agent).

  ### Sources

  - Docs: https://platform.claude.com/docs/en/managed-agents/overview
  - Quickstart: https://platform.claude.com/docs/en/managed-agents/quickstart
  - Developer guidance (anthropics/skills repo):
    https://github.com/anthropics/skills/blob/main/skills/claude-api/shared/managed-agents-overview.md
  - Launch coverage: https://www.infoq.com/news/2026/05/code-with-claude/
  - VentureBeat (enterprise / lock-in angle):
    https://venturebeat.com/orchestration/anthropics-claude-managed-agents-gives-enterprises-a-new-one-stop-shop-but
project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 5
title: Understand claude managed agents
updated: 2026-05-27 14:12:42.932420
waiting_on: null
waiting_since: null
working_on: false
---