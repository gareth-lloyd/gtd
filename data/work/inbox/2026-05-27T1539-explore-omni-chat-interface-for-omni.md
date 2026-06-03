---
area: null
contexts: []
created: 2026-05-27 15:39:54.693115
defer_until: null
due: null
energy: low
id: 2026-05-27T1539-explore-omni-chat-interface-for-omni
order: null
output: |
  ## Agent run 2026-06-03T12:45:00

  **What it is.** Omni (omni.co, the BI/analytics platform — not Omnichat the
  CX vendor) has shipped an agentic chat UI inside its dashboards. Two distinct
  surfaces:

  1. **Dashboard Agent** — a chat panel that lives *on a published dashboard*
     (icon, bottom-right). You converse with the existing tiles in natural
     language: ask follow-ups, drill into subsets, re-aggregate, request
     summaries — without leaving the dashboard. You can focus the agent on one
     chart (click it or "Ask a follow up" from the tile menu), attach images for
     visual context (Chrome/Safari), and it can search Omni's own docs for
     how-to questions.
       - Requires Querier+ permission on the model; admin must enable
         "Read data result" (AI Hub > Setup) and the "AI on dashboard" doc
         ability. Rebrandable via AI branding; respects white-label (hides doc
         links when watermark is hidden).
       - Docs: https://docs.omni.co/ai/dashboard-assistant

  2. **AI chat (standalone) + multi-step agentic reasoning** — beyond the
     dashboard. Takes open-ended prompts ("How's my sales org doing?") and runs
     a full analytical workflow end-to-end: plans a task list, picks tools,
     runs queries, validates/iterates, synthesizes a narrative with evidence.
     A "coordinator" plans → selects actions → executes → evaluates. The task
     list is shown and checked off live, so reasoning stays transparent/
     debuggable. This is reportedly their fastest-growing feature.

  **Key architectural point (the moat).** All of it is grounded in Omni's
  built-in **semantic layer** — same governed metrics, joins, business logic,
  and row/column security as their dashboards. The semantic layer is the
  guardrail that keeps the agent from hallucinating metrics or going off-track.
  Models: AWS Bedrock-hosted **Claude** for most tasks; OpenAI only for advanced
  AI visualizations.

  **Surrounding context.** They also launched "AI Hub" (a command center to
  observe AI usage, improve the semantic model from real usage, and validate
  changes before prod). Omni raised a Series C ($120M @ $1.5B valuation, ICONIQ-
  led, ~4x YoY revenue), with AI consolidation of legacy BI as the thesis.

  **My read / relevance to us.** The pattern worth stealing is *agent grounded
  in a governed semantic layer with a visible, checkable task list* — that's how
  they get trustworthy, in-context answers rather than free-text SQL roulette.
  The "chat lives on the artifact you're already looking at" (Dashboard Agent)
  vs. "standalone agent that does multi-step research" split is a clean mental
  model if we think about agentic surfaces in our own product. Nothing here is
  hotel-specific; it's a BI tool. Pure competitive/UX intel.

  **Sources:**
  - https://omni.co/ai
  - https://docs.omni.co/ai/dashboard-assistant
  - https://omni.co/blog/moving-beyond-simple-questions-with-agentic-ai
  - https://omni.co/blog/building-omnis-architecture-for-agentic-analytics
  - https://omni.co/blog/introducing-ai-hub
  - https://omni.co/blog/2025-product-highlights
  - https://omni.co/blog/press-release-omni-series-c-funding
project: null
source_id: null
tags: []
time_minutes: 5
title: Evaluate omni chat interface for omni
updated: 2026-06-03 12:45:00.000000
waiting_on: null
waiting_since: null
working_on: false
---