---
area: null
contexts:
- consume
created: 2026-05-25 04:18:16.758275
defer_until: null
due: null
energy: medium
id: 2026-05-25T0418-read-andy-s-notion-agent-platform-doc-review-reque
order: null
output: |
  ## Agent run 2026-05-25T11:55Z

  **Doc**: ⛸️ Canary's Agent Platform (Notion, IN REVIEW, Design Doc DB)
  https://www.notion.so/canarytechnologies/Canary-s-Agent-Platform-3668146861518076b427c6fcd546c261
  Author: Andy Monroe. Created 2026-05-20, last edited 2026-05-21. 22 discussion threads.

  ### Andy's ask
  Originally asked Daga + An Nguyen for a review pass. Garrett pushed back ("org-wide
  feedback or eng-e8t consensus first?"), Andy opened it to org-wide. Garrett then
  cc'd Laura + you (me, Gareth) saying it's "highly relevant to the discussion/
  decision we had yesterday" (i.e. May 20). An Nguyen deferred (firefighting merge
  queue). Bernard committed to going through it. Goal: close the directional
  decision this week so people can stop debating platform and start shipping.

  ### The proposal in one line
  Commit to **Claude Managed Agents (CMAs)** as THE platform for all internal
  agents at Canary.

  ### Why CMAs (Andy's case)
  - Anthropic is the leader in agentic models + tooling (Tools, MCP, CLAUDE.md,
    Skills); industry follows their lead; Canary already uses them at scale with
    high reliability.
  - **Self-hosted sandboxes** — run compute where we want (cheap AWS), control
    network/access, can host inside internal network → expose internal systems
    via scoped tools.
  - UI in Claude console for non-engineer creators (Andy clarifies: PMs /
    "Gurtej types", not literal non-technical users).
  - Public docs, multi-agent sessions, **Vaults** (creds), **Memory Stores**.

  ### Drawbacks Andy acknowledges (with his responses)
  - Claude-only, no OpenAI/Gemini/open source. Andy: token-cost loss but
    acceptable; the bigger problem is enabling workflows at all.
  - Have to re-implement existing agents (Golem, Triage, Linear/Slack bots).
    Andy: porting is unavoidable on any path.
  - **CMAs are beta** — could change underneath us. Andy: comfortable with risk,
    Anthropic ships well, Notion built on top of CMAs.
  - **CMAs can't currently access MCPs inside our network (Teleport-gated)**.
    Andy: Anthropic working on MCP tunnels; Cloudflare Tunnels as workaround;
    short-term issue.
  - "I don't like Claude" → Lebowski "that's like your opinion man" gif.

  ### Implementation (loose, direction-only)
  1. Example Slack/Linear bot as a CMA (no self-hosted sandbox, no tunneling).
  2. Triage Agent 2.0 as a CMA (same MCP/tools/skills as today; sandbox optional
     for MVP).
  3. MVP **Code Review Agent** (per-pod? auto-requested as CODEOWNER?). Will
     need self-hosted sandboxes.
  4. Devin 2.0 as a CMA ("Cevin"). Andy admits he doesn't know how Devin is used.
  5. Golem 2.0 as a CMA. Will need self-hosted sandboxes.
  Andy says per-agent estimates / cutover / rollback are out of scope for this
  doc — they'll be separate projects.

  ### Open threads / pushback (the substance you'd actually be reviewing)

  **1. MCP tunnels = unresolved P0 blocker.** Stuart Bowman (most active reviewer):
  MCP tunnels is research preview with no uptime/support/continuity commitment;
  Mephisto, Triage, anything touching internal systems is blocked without it;
  Cloudflare Tunnels workaround deserves its own design, not a parenthetical;
  needs a network-security review (segmentation, hardened reverse proxy, logging,
  break-glass). Another reviewer (28fd...): "P0. Not worth considering until
  there is a concrete solution." Andy's counter (in-thread): just give the MCP
  server a domain + OAuth, drop Teleport — "like a day of work" — and argues
  Teleport itself is platform risk. Another reviewer (2b7d...) seconded: not
  a hard problem, but a platform decision (Teleport → OAuth). **This is the
  hottest unresolved decision in the doc.**

  **2. Vaults — two separate concerns.**
  - Coverage: today Vaults only supports `static_bearer` + `mcp_oauth`. Our
    agents hit Slack, Linear, GitHub, Datadog (→ Groundcover), Supabase,
    Tailscale, mostly via SDK clients not MCP. Wrapping each = weeks, no new
    capability → currently a *drawback*. Andy: most of those have remote MCPs
    with OAuth already; just wire-up.
  - Security: storing all our secrets on Anthropic = vendor concentration —
    encryption model? Anthropic-side access? breach SLA? blast radius? Andy:
    fast key-revocation is enough for MVP; we already trust Anthropic with the
    whole codebase, secrets leak into API requests anyway.

  **3. Prompt injection is the #1 threat for every agent on the list.** Triage
  reads tickets/Slack, Code Review reads diffs, Golem reads task descriptions —
  all attacker-controlled. Reviewer (317d...) wants: instruction/data separation,
  least-privilege tool scopes, action logs tied to inputs, human-in-the-loop
  for destructive ops, threat model per agent, security-review gate as a
  checkbox in the implementation list. Andy: serious, but case-by-case; modern
  Claude models are hard to inject; don't get hung up before MVP.

  **4. No security section at all** (full top-level comment from 317d...).
  Missing: threat model, data classification (what's allowed to transit
  Anthropic — PII, customer data, secrets? what's their retention/training
  policy?), access control / least privilege, audit logging strategy, incident
  response / kill-switch.

  **5. Internal-network sandboxes = lateral-movement attack surface.** Framed
  as a benefit in the doc but no controls described. Need: VPC/VLAN isolation
  with per-service allowlists, egress filtering (else agent = exfil bridge),
  FS/process isolation for arbitrary code execution, per-agent rate limits.

  **6. Multi-agent sessions = confused-deputy risk.** What stops low-privilege
  Agent B from instructing high-privilege Agent A? Per-agent cred scoping,
  transitive tool invocation, prompt-injection chaining across the boundary —
  all unspecified.

  **7. Vendor concentration risk.** Creds + memory + execution + internal
  network access all on one beta vendor. Need fallback ability to run
  Triage/Golem on own infra, fast cred revocation, contractual SLAs,
  abstraction layer so agent logic stays portable. "The author is comfortable
  with this risk" is not a security control.

  **8. UI-for-non-technical claim challenged.** Stuart: benefit applies only
  to one *type* of agent (small personal); doesn't help eng-owned services
  with webhooks/routing — nobody builds those in a UI. Another reviewer (1a8d...):
  tried the UI, it ran on Haiku and would obliterate YAML — forward-looking
  assumption, not current state. Andy: clarified he means PMs/systems-thinkers,
  not literal non-engineers.

  **9. E2B cost claim under-evidenced.** Stuart: ~$1k/mo of E2B vs CMA
  self-hosted sandbox compute + tokens at the new agent's projected volume —
  compare with real numbers before using cost as the reason. Also: there's
  already a plan to move off E2B to ephemeral envs anyway. Andy: AWS pricing
  at our volume will beat E2B; will get hard numbers.

  **10. Devin pain wasn't specified.** "Limited flexibility" → MCP auth, startup
  times, session handling, lack of memory integration (per 317d...). Reviewer
  2b7d... says auth issue is now resolved; cost is the dominant problem anyway.
  No clear Devin POC; Felipe(?) built MSG Devin skills — bullet should reduce
  to "migrate Felipe's playbooks to CMA."

  **11. "Paralysis vs shipping" framing.** Reviewer 2b7d... argues priority
  should be: (1) build lots of great local agents, (2) any cloud env for
  scale even if short/medium term, (3) durable solution later. Andy: that's
  exactly what this doc is trying to unblock — we're closing the decision so
  we can stop talking.

  **12. Re-implementation plan absent.** Reviewer wants per-agent estimates,
  dual-run during cutover, rollback path, ready-to-replace criteria. Andy:
  separate projects; this doc is direction-only.

  **13. Naming/ownership noise.** Multiple "Triage Agents" floating around:
  `linear_agent` → `Workup`, plus `Triage Bot` inside the agents framework
  that `Workup` will replace. Reviewer requested clarification in doc.

  ### What's relevant for *your* review (Gareth-specific)
  - Garrett explicitly flagged this as relevant to a May 20 conversation/
    decision involving you + Laura — worth recalling what that was before you
    weigh in.
  - You've worked across the agent stack (LangChain/LangGraph cookbook, MCP
    tools, agent_context providers, event-logging, Mephisto). The MCP-tunnels /
    Teleport-vs-OAuth question and the SDK-client-vs-MCP coverage question are
    the two places where your direct codebase knowledge is most valuable to
    push on.
  - Andy is trying to close direction this week and is comfortable defending
    every drawback in the doc. The thing he's most likely to move on, based on
    thread tone, is the MCP-tunnel / OAuth-on-MCP-server piece (he's already
    arguing for it in-thread). Adding a security-review gate as a checkbox
    in each implementation bullet is the cheapest concrete addition that
    would unblock the security-skeptical reviewers without re-litigating
    the direction.

  ### Status
  Read complete. No external writes/comments posted. Awaiting your decision
  on whether/how to leave feedback.
project: null
source_id: https://canarytechnologies.slack.com/archives/C09D2A5LYN9/p1779311725245969?thread_ts=1779311725.245969&cid=C09D2A5LYN9
tags:
- morning-gtd
- slack
- from-awareness
time_minutes: 20
title: 'Read: Andy''s Notion agent-platform doc (review request to Daga/An Nguyen)'
updated: 2026-05-25 11:57:21.088246
waiting_on: null
waiting_since: null
working_on: false
---

Andy asking Daga + An Nguyen to do a review pass on the Canary Agent Platform Notion doc. https://canarytechnologies.slack.com/archives/C09D2A5LYN9/p1779311725245969?thread_ts=1779311725.245969&cid=C09D2A5LYN9