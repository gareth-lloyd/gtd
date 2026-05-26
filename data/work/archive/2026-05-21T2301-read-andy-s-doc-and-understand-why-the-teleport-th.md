---
area: null
contexts: []
created: 2026-05-21 23:01:54.764799
defer_until: null
due: 2026-05-25
energy: medium
id: 2026-05-21T2301-read-andy-s-doc-and-understand-why-the-teleport-th
order: null
output: |
  ## Agent run 2026-05-21T20:03Z

  Read Andy Bray's "Canary's Agent Platform" Notion doc. Teleport is mentioned
  once, as a constraint on the proposed Claude Managed Agents (CMA) platform.

  **TL;DR of the blocker**
  Andy is proposing Canary standardize internal agents on Anthropic's Claude
  Managed Agents (replacing Golem, Devin, Triage Agent, Copilot flows). CMAs
  can't currently reach MCPs that live inside Canary's internal network —
  i.e., anything you'd normally need Teleport to get to. So any agent flow
  that depends on an internal-only MCP can't run on CMAs as-is.

  **What Teleport actually is in this context**
  Teleport is just the stand-in for "stuff behind our corp network perimeter."
  The blocker isn't Teleport-the-product; it's that CMAs run outside that
  perimeter and have no tunnel to MCPs hosted inside it.

  **What would unblock it (per the doc)**
  Three options on the table, no decision yet:
  1. Wait for Anthropic's forthcoming MCP tunnels feature
     (platform.claude.com/docs/en/agents-and-tools/mcp-tunnels/overview).
  2. Build a Cloudflare Tunnels stopgap.
  3. Push Anthropic for early access.

  **Who's blocked**
  Owner of the doc / platform proposal: Andy Bray. No named owner for the
  Teleport/MCP-tunnel workstream specifically. MVP milestones (Slack/Linear
  bot, Triage Agent 2.0) are explicitly scoped to *avoid* needing internal
  MCPs, so the Teleport-zone work is deferred past MVP — it's a blocker for
  the broader rollout, not for the first milestone.

  **My take**
  Not a near-term blocker for me/anything I'm shipping. It's a strategic
  blocker on consolidating *everything* onto CMAs. If/when an agent I care
  about needs a corp-internal MCP, this becomes load-bearing.

  Source: Notion — Canary's Agent Platform
  (https://www.notion.so/3668146861518076b427c6fcd546c261)

  ## Agent run 2026-05-22T07:10Z — technical explanation

  Adding the basic-but-comprehensive technical picture of why this is
  actually a blocker.

  **The three pieces involved**

  1. **Teleport.** An identity-aware access proxy (goteleport.com). Engineers
     SSO into Teleport, get short-lived certs, and Teleport then proxies them
     into private resources (SSH boxes, k8s clusters, internal databases,
     internal HTTP apps) that aren't exposed to the public internet. At
     Canary it's the gate in front of corp-internal stuff. Auditing + MFA
     baked in.

  2. **MCP (Model Context Protocol).** Anthropic's open standard for how an
     agent talks to external tools/data. An "MCP server" is a process that
     exposes tools (functions the agent can call) and resources (data the
     agent can read) over JSON-RPC, typically over stdio or HTTP/SSE. An
     agent ("MCP client") connects to one or more MCP servers and the model
     decides when to call them. Canary already runs internal MCPs that wrap
     things like the Django shell, hotel lookups, Sentry, Datadog, etc. —
     several of those servers are only reachable from inside the corp
     network.

  3. **Claude Managed Agents (CMAs).** Anthropic's hosted agent runtime.
     Instead of you running the agent loop on your own infra (model call →
     tool call → model call → ...), Anthropic runs it in their cloud. You
     define the system prompt, tools, and MCP servers, and Anthropic
     executes. Tool calls can either run on Anthropic's sandboxes or, with
     "self-hosted sandboxes," on a sandbox you provide.

  **Where the blocker actually sits**

  Network topology. The CMA runtime — and any sandbox it talks to — lives
  outside Canary's network. When the agent decides to invoke a tool that
  lives on an internal MCP server (something normally reached via Teleport),
  there's no route. Anthropic's cloud cannot dial into Canary's private
  network, and we are not going to put those MCPs on the public internet.

  Self-hosted sandboxes only partly help: they move *tool execution* onto
  your iron, but the sandbox still has to reach the MCP server. If the
  sandbox is hosted by Anthropic-adjacent infra, the same network gap
  exists. If we host the sandbox ourselves inside the corp network, we're
  back to running our own agent infra — which is exactly what the CMA
  proposal is trying to get *out* of.

  **What "MCP tunnels" would do**

  A reverse tunnel: a small agent process running *inside* Canary's network
  initiates an outbound TLS connection to Anthropic (outbound is allowed,
  inbound isn't). Anthropic then routes the CMA's MCP traffic back through
  that tunnel to reach the internal MCP server. The tunnel endpoint is
  authenticated and scoped to specific MCPs. Same pattern as Cloudflare
  Tunnels, ngrok, frp, or Tailscale Funnel — just productized by Anthropic
  for the MCP protocol specifically.

  Cloudflare Tunnels is the obvious stopgap because Canary already uses
  Cloudflare; you'd stand up a `cloudflared` connector inside the perimeter,
  expose a hostname like `mcp-internal.canary.internal.cloudflare`, lock it
  down with Cloudflare Access (SSO/JWT), and point CMAs at that URL. Works,
  but it's another piece of infra to own and another auth surface.

  **Why this is "a blocker" not just "a limitation"**

  The agent platform proposal is to *consolidate*. The whole point is one
  runtime, one set of patterns, one place to add tools. If half of Canary's
  most useful MCPs (the corp-internal ones — Django shell, internal data
  pulls, prod-adjacent observability) can't be reached from CMAs, then CMAs
  can't actually replace the existing agents. You'd end up with CMAs for
  the external-only flows and the legacy stuff still running elsewhere for
  the internal flows — i.e., the consolidation goal fails.

  Hence Andy scoping MVP milestones (Slack/Linear bot, Triage Agent 2.0)
  to deliberately avoid internal MCPs: those milestones can ship without
  solving the tunnel problem, but the broader rollout can't.
project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 5
title: read andy's doc and understand why the teleport thing is a blocker
updated: 2026-05-26 13:40:48.853777
waiting_on: null
waiting_since: null
working_on: false
---

https://www.notion.so/Canary-s-Agent-Platform-3668146861518076b427c6fcd546c261?d=36781468615180338586001c86763cfa&source=copy_link#3668146861518017adf7d1d1470457ac