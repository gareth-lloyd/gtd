---
area: null
completed_at: null
contexts:
- consume
created: 2026-09-30 21:35:14.568359
defer_until: null
due: 2026-10-01
energy: null
id: 2026-09-30T2135-read-and-absorb-workup-agent-sync-2026-09-30-mcp-s
order: 2
output: ''
project: 2026-09-08-workup
source_id: null
tags: []
time_minutes: null
title: 'Read and absorb: Workup Agent Sync 2026-09-30 (MCP SQL tool nearly live)'
updated: 2026-10-01 14:44:24.942212
waiting_on: null
waiting_since: null
working_on: true
---

Doc: https://docs.google.com/document/d/13FEf-8bolS9gMcHdETXpAHH3N04oxJiqHytydgJOdys/edit
(Gemini notes, shared by Laura DeWald 2026-09-30)

## Key points

**MCP SQL tool (Asher)**
- Staging validation passed 2026-09-29. Three PRs remained: one merged, one in merge queue, one needs small fixes. Then enable in prod US and iterate live.
- Auth/security verified. Workup already sees run_sql and has tried to call it (fails on the disabled gate). How it uses SQL is untested; Asher prefers enabling over more staging tests. Blake agreed, expects prompt tweaks.

**Flight recorder PR (Jason Flax)**
- Very large PR recording the evidence Workup uses at each decision point. Session history was not enough to reconstruct decisions (Stephanie Fernandez saw the same).
- Goal: data to offload decision steps to a Jev-style classifier for speed/cost. No behavior change, some runtime overhead. Jason offered to split it.
- Asher's SQL work took ~1,500 relevant lines from Jason's ~8,000-line PR.

**Orbital (Jason)**
- Install into Canary nearly done mechanically, not usable yet.
- Open permission questions: can teammates see each other's agent conversations/transcripts; what access agents have to other sessions.
- Workup decomposition needs its own working group (Laura + Jason to connect).

**Messaging asks (Matias)**
- Messaging volume high. Demetri wrote a doc of categories where Workup could act now: move to customer ops, close duplicates, close as needs-more-info.
- Laura shipped same-hotel duplicate auto-close this morning (cross-hotel accuracy worse), plus a change to reduce over-declared code fixes.
- Laura follows up on Matias's list as immediate next step.
- Many messaging tickets are config issues that look like bugs (poor UI errors). Laura/Blake want Workup-style triage inside Zendesk; later a debugging chat replacing the issues form for CS.

**Metrics (Laura, agents dashboard)**
- Next-step correctness 40% (about its highest). Quality 74% incl. partials.
- Expected-behavior and config-change categories strongest; duplicates improved.
- Nensy wants expected-behavior tickets routed to support enablement for KB review. Laura to add a label + Linear view. Blake: enable support, don't own it yourself.

**Rollout / other**
- Stephanie Barry to put Workup expansion to other eng teams on next agenda (was gated on SQL tool). Blake supports going out at current numbers; share model cost profile alongside.
- Ticket volume flat 3 months despite September efficiency sprint. Incidents well down.