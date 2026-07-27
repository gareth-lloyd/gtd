---
area: null
contexts: []
created: 2026-07-23 21:58:56.184655
defer_until: null
due: null
energy: low
id: 2026-07-23T2158-laura-switched-to-new-agent-on-agents-framework-in
order: null
output: |
  ## Agent run 2026-07-24T10:30:00+01:00

  Found it. The "brand new agent on the agent framework" is Laura DeWald's **Workup agent**,
  which lives in the Overlord framework inside the `agents` repo (NOT the older
  `opencode-overlord` repo — that was Adil's April prototype, last touched 2026-04-14).

  **Defining code** (repo: https://github.com/canary-technologies-corp/agents):
  - `overlord/src/agents/workup/agent.ts` — the agent definition (`defineAgent`, `type: "tool"`,
    `mode: "shared"`, `linearBotName: "workup"`, `skipSessionCreatedAck: true`). Handles
    `workup-handoff-v2` payloads: claims the issue in a durable handoff store, self-creates a
    Linear agent session on the issue, posts the triage summary as a thought + rendered triage
    comment, and (phase 2) runs an interactive investigation in an E2B sandbox via the
    `investigate` plugin, with a live plan shown in the session.
  - `overlord/src/agents/workup/handoff-store.ts` — durable dedupe/claim store for handoffs.
  - `overlord/src/agents/workup/watchdog.ts` — session watchdog.
  - `overlord/src/clients/linear.ts` — `createAgentSessionOnIssue` helper.

  **Key PRs** (all Laura, ticket trail TOOL-405 then TOOL-450 "Workup"):
  - #78 "Add Overlord workup agent (owns its own Linear session)", merged 2026-07-13 —
    https://github.com/canary-technologies-corp/agents/pull/78. This is the re-homing of the
    linear_agent investigation handoff off the old fire-and-forget investigator onto an
    Overlord-owned interactive session.
  - #90 phase 2: interactive investigation inside the workup session (2026-07-20) —
    https://github.com/canary-technologies-corp/agents/pull/90
  - #92, #93, #94, #96 — follow-ups through 2026-07-24 (sandbox spawn fix, live plan,
    session UX + local pre-merge test harness, sandbox dashboard link).
  - Linear ticket: https://linear.app/canary-technologies/issue/TOOL-405

  **Canary side (the "comms core first" rollout lever):** the handoff trigger is
  `backend/canary/linear_agent/workup/trigger.py`, gated per-Linear-team by the
  `LINEAR_AGENT_WORKUP_TEAMS` env var (comma-separated team keys, defined at
  `backend/canary/canary/settings/base.py:1663`). Trying it with comms core first = putting
  that team's key in this var, then "backfilling other teams" = extending the list. The old
  path it replaces is `backend/canary/linear_agent/investigator/trigger.py`.

  ### Behavior summary

  1. Trigger: canary linear_agent triage POSTs a `workup-handoff-v2` payload (issue ID,
     triage summary, resolved entity UUIDs, data center) to Overlord `/events`;
     non-v2 payloads are dropped.
  2. Claim & dedupe: claims the issue in a durable handoff store so retries/replays
     don't double-post.
  3. Session: self-creates a Linear agent session on the issue, posts the triage summary
     as a thought + the rendered triage comment.
  4. Investigate (phase 2): if needed, dispatches an investigation prompt into an E2B
     sandbox running the `investigate` plugin, shows a live plan in the session, then
     completes it. Failures throw so the caller can retry or fall back.

  External mechanisms: Linear API via its own `workup` bot OAuth app
  (WORKUP_LINEAR_CLIENT_ID/SECRET/WEBHOOK_SECRET in the overlord k8s Secret); E2B
  sandboxes for the investigation leg; canary-mcp for tool access into Canary data;
  the LINEAR_AGENT_WORKUP_TEAMS gate on the canary side; the durable handoff store.
  Net: canary triages and gates per team; Overlord's workup agent owns the Linear
  session and does the interactive investigation in a sandbox.
project: null
source_id: null
tags: []
time_minutes: 5
title: 'Laura: switched to new agent on agents framework in overlord'
updated: 2026-07-24 10:33:54.636197
waiting_on: null
waiting_since: null
working_on: false
---

TRanscript excerpt:
And escalation yeah.

They didn't.

That would be cool definitely keep thinking about that I'd love to hear more.

I had a few messages a couple weeks ago just thinking how do we get triage agent or rather investigation agent turned on for all linear? Any thoughts or progress there.

Yeah.

I'm getting closer.

I think. I've. I've switched.

To.

Like, a brand new agent that's on. On the agent framework.

And I think I'm going to try it out with. With comms core first.

And then go back.

And backfill the other teams.

Yeah. Because I think.


TAsk: Find the relevant code defining the new agent.