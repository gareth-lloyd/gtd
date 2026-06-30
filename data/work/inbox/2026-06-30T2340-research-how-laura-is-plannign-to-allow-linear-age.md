---
area: null
contexts: []
created: 2026-06-30 23:40:41.646751
defer_until: null
due: null
energy: low
id: 2026-06-30T2340-research-how-laura-is-plannign-to-allow-linear-age
order: null
output: |
  ## Agent run 2026-06-30T21:10Z

  **Source:** Laura DeWald DM, 2026-06-30 (https://canarytechnologies.slack.com/archives/D07U6KK5W1G/p1782841610127859). No design doc yet — the plan is captured in the message + 3 PRs (all now MERGED).

  ### The plan (Laura's TL;DR)
  Let the `linear_agent` triage bot hand its **investigation step** off to an LLM agent — Overlord's `investigate` plugin running in an E2B sandbox — instead of the hand-written deterministic routines.
  - Triage still posts its routing comment **instantly**; the diagnosis lands **afterward, out-of-band**, in the *same* Linear agent session.
  - **Flag-gated, default OFF**, scoped to the **PMS team**. Inert until the flag is set; deterministic routines run unchanged when off.
  - PII/risk posture is unchanged from the already-deployed triage agent — same plugin, same data, same sandboxes. This re-points an existing capability and adds a hardened callback.

  ### How the handoff works (architecture)
  1. **Delegation + two-phase response** (canary #48775): triage's investigation node builds a `workup-handoff-v1` payload and fires it to the Overlord investigator *after* the triage comment posts, with `awaitResponse=false`. Overlord acks immediately and runs the (multi-minute) investigation in the background (fire-and-forget avoids the sandbox per-command timeout).
  2. **Investigator agent** (agents #52, `src/agents/investigator/`): minimal `handleEvent` that runs canary's `investigate` plugin (`investigate-ticket` → `gather-context` + the `propose-hypothesis` multi-agent debate) against the payload. Pinned to `Model.Sonnet`. **Never** touches Linear/Slack directly — only reports back via the canary callback.
  3. **Callback** (`linear_agent/views/activities.py`, the ActivitiesView in #48775): the single inbound surface. Relays the investigator's `thought` and `response` activities back into the same Linear session. Triage posts `respond(complete_session=False)`; the investigator's final `response` completes the session.

  ### Security posture
  - **Session-bound JWT** is the one inbound surface: `build_investigator_payload` mints a short-lived HS256 JWT per handoff (signed with `INVESTIGATOR_CALLBACK_SIGNING_KEY`, bound to `linear_session_id`, 45-min window). `InvestigatorCallbackAuthValidator` verifies signature + audience and binds the `sid` claim to the URL's session — a leaked token only works for its own session. Investigator relays the token from the payload, so it needs no callback secret of its own.
  - **Hardening:** Overlord 401/403 logged at error (`trigger_auth_failed`) so a shared-secret mismatch pages instead of vanishing; null-status guards; per-entity guards in eager-gather so one bad entity can't fail triage.

  ### Performance optimization — "eager-gather"
  - `linear_agent/investigator/eager_gather.py` (#48775, producer half): during triage, serialize entities already resolved (hotels, reservations) through their `agent_context` providers and thread them into the handoff as `pregathered_*_context`, so the investigator consumes pre-resolved context instead of re-fetching in its sandbox. Default on, kill switch `LINEAR_AGENT_INVESTIGATOR_EAGER_GATHER`.
  - Consumer half (#48984, prompt-only): the `gather-common-hotel-context` and `resolve-reservation` skills read the bundle when present, else fall back to normal HTTP `agent_context` / MCP fetch. Backward-compatible, so the two halves can land in either order.

  ### Flags / env
  - `LINEAR_AGENT_INVESTIGATOR_ENABLED` (default off) — master switch.
  - `LINEAR_AGENT_INVESTIGATOR_EAGER_GATHER` — eager-gather kill switch.
  - `INVESTIGATOR_CALLBACK_SIGNING_KEY` — JWT signing.
  - `AGENT_CONTEXT_SECRET_TOKEN` forwarded into sandboxes via Overlord global env so the investigator's `agent_context` calls work.

  ### The three PRs (all MERGED, author: Laura DeWald)
  1. canary #48984 — investigate skills consume triage's pre-gathered context (consumer half, prompt-only): https://github.com/canary-technologies-corp/canary/pull/48984
  2. agents #52 — Investigator agent for linear_agent triage handoffs: https://github.com/canary-technologies-corp/agents/pull/52
  3. canary #48775 — Delegate linear_agent triage investigation to the Overlord investigator (producer half: delegation, eager-gather, session-bound JWT, callback endpoint): https://github.com/canary-technologies-corp/canary/pull/48775

  **Status:** all three merged; feature flag-gated default-off, PMS-team scoped. Validated end-to-end in a real E2B sandbox. No design doc exists yet.
project: null
source_id: null
tags: []
time_minutes: 5
title: 'research how Laura is plannign to allow linear agent to hand off to investigation
  agent:'
updated: 2026-06-30 21:10:00.000000
waiting_on: null
waiting_since: null
working_on: false
---

https://canarytechnologies.slack.com/archives/D07U6KK5W1G/p1782841610127859