---
area: null
completed_at: 2026-10-08 14:06:49.467137
contexts: []
created: 2026-10-08 13:57:43.714377
defer_until: null
due: null
energy: low
id: 2026-10-08T1357-summarize-these-notes-https-docs-google-com-docume
order: null
output: |-
  ## Agent run 2026-10-08

  Summary of "Workup Agent Sync - 2026/10/07 11:31 EDT - Notes by Gemini" (https://docs.google.com/document/d/18j25XS4qdipC2TrfXCQVb5tFxLvjW6bRSTVogo1kqm0/edit). The meeting was 16 minutes, run by Stephanie Barry. You were invited but never speak in the transcript, and Blake appears to have been absent.

  **Updates**
  - MCP run SQL tool (Asher): it went live in US last week. Fixes in progress: the judge is too restrictive and is being loosened to let more query types through, and the agent sometimes calls run SQL with the wrong arguments (a broader Overlord problem). It is being turned on in EU and AP now.
  - Quality monitoring (Stephanie Barry + Asher): they will add a monitoring and quality view to the Workup dashboard and set up a project for it. Until then, file tickets for any judging or quality problems you see. Laura noted the per-issue gap view already shows MCP gaps.
  - Messaging-pod config tickets (Laura + Dmitry): Workup will auto-close some configuration tickets. **Decision: Workup will not change configuration for now**, apart from a few hand-picked safe cases Laura is working on. Dmitry expects low volume to start and will tag Laura on any problems.
  - Orbital (Jason): build 72 is out. It links accounts to Canary and supports API-key agents on Canary's platform, and it now lives in and next to the agents repo instead of Jason's private servers or a local DMG. The UX is rough. The alpha opens to everyone in the next few days, with a public Orbital channel early next week. Jason asked people to keep this quiet until then. Build 73 aims to set up a version of the Workup flow inside Orbital once the obvious UX problems are fixed. DM Jason for a link now.
  - Workup nudge (Sam): just started. It uses Slack to ask people to add missing information to tickets.
  - Engram / agentic recall: since Amanda left, Stephanie Fernandez is fully on the accessibility deadline tied to the AOR contract for the next week or two. Jason is temporarily taking the Engram work back. Jason thinks Engram could be turned on for other agents, but Blake doesn't want that prioritised yet. Agentic recall gives better results than plain vector search, though vector search works fine. Productionising it is a large job. Cost: Haiku is about 5c per recall and recall runs several times per turn, so Jason thinks it is too expensive long term. Options being looked at: GPT-6 Luna (Stephanie F; reportedly cheaper than Haiku) and open-weights GLM on Fireworks (Jason; a fraction of a cent per recall). Local models would be the ideal.
  - Jason still needs Hugging Face access to get **the Jev work into a shareable state**. He is wary of pinging Z again; Laura thinks AJ now owns it. This matters for your Workup vs TypeSafe Jev backtest.

  **Action items (from Gemini's notes)**
  - Asher + Stephanie Barry: build the Workup quality monitoring dashboard.
  - Everyone: file tickets for judging or quality problems.
  - Jason: send the Orbital link to anyone who wants it; get Hugging Face access; hold the Engram work for now.
  - Stephanie Fernandez: evaluate GPT-6 Luna for agentic recall cost.
  - **You: no actions assigned.**

  Caveats: Gemini's summary expands "AOR" as "Agent-Oriented Research", which is probably wrong. The transcript only says "the contract for AOR".
project: null
source_id: null
tags: []
time_minutes: 5
title: 'Summarize these notes: https://docs.google.com/document/d/18j25XS4qdipC2TrfXCQVb5tFxLvjW6bRSTVogo1kqm0/edit?tab=t.cs99sn5igs5u'
updated: 2026-10-08 14:06:49.467128
waiting_on: null
waiting_since: null
working_on: false
---