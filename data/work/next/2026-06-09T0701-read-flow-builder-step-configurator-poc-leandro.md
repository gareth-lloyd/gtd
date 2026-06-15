---
area: null
contexts:
- consume
created: 2026-06-09 07:01:12.676483
defer_until: null
due: null
energy: low
id: 2026-06-09T0701-read-flow-builder-step-configurator-poc-leandro
order: null
output: |
  ## Agent run 2026-06-09T12:05Z — read & digest

  **What this is:** Leandro Alvarez's working POC (PR #47372 "Guest Experience -
  Nested flow separate sessions POC", OPEN, +1499/-198, 39 files, Loom:
  loom.com/share/7b1da4ed9e6a476ba283f42b26cb2323). It implements end-to-end the
  design Matt Jeffery sketched in PR #47319 ("Nested Flows Step Framework"), to
  prove the approach is feasible and simple. Slack thread (C0A5Z7LE5AL) is just
  Leandro announcing the new version + tagging Matt/Dana/Guido/Gustavo; Matt
  replied "this looks pretty good… any new thoughts on the approach now that
  you've implemented both ways?" — i.e. an open design question still on the table.

  **The core idea (from Matt's #47319):** instead of a flow-level routing/DAG or
  cramming additional-guest identity into CheckInSession, treat nested flows as
  *child sessions*. Four primitives:
    1. `parent_session_uuid` + `parent_flow_slug` on the abstract SessionModel
       (only structural change to the framework).
    2. A service registry keyed by flow_slug — view resolves the right step-
       framework service per flow and delegates (session/submit views become
       flow-agnostic).
    3. A "go to child flow" step action: on submit, create a child session and
       return its URL via the existing redirect_url field (frontend just navigates).
    4. On child completion, `_get_redirect_url` bounces back to the parent.
  Identity ("which guest does this submission belong to?") is carried by the
  *session itself* via parent context — no guest/additional_guest fields scattered
  on CheckInSession.

  **What Leandro actually built (PR #47372 highlights):**
    - `step_framework/models/session.py` — parent pointer on base session.
    - New `AdditionalGuestSession` + `AdditionalGuestSubmittedValues` models;
      a `registry.py` + `additional_guest_step_framework.py` service; a
      `child_flow_navigation.py` step service.
    - `additional_guest_list_step` (handler/config/strings) — the "add guest"
      list step that spawns child sessions.
    - Generalized schema_form handler/configuration/service so reused steps
      (e.g. ID, schema forms) submit to the right subject generically.
    - Frontend: `GuestExperienceSessionRoot.vue`, `useSubmitStep.ts`,
      session store, and the AdditionalGuestList step view/config.
    - `seed_additional_guest_subflow` mgmt command for demoing.

  **Open design tensions Leandro flagged (these are the decision points):**
    - **N-level nesting is NOT solved** (issue comment #4653624920). This POC
      handles one level (additional-guest under check-in). Add an ID flow nested
      under additional-guest and the identity problem returns: an ID session could
      belong to primary OR additional guest, so either (a) submission target
      depends on which parent it's nested under (not standalone), (b) you put a
      primary/additional reference back in the ID session (back to square one), or
      (c) you split into PrimaryIdSession/AdditionalIdSession (proliferation of
      services + submission objects). Unresolved.
    - **"Many session types" vs "one session, many flows"** (Matt's two shapes).
      POC primitive is identical either way. Leandro built toward the cheap shape
      to validate navigation; can split to per-domain session tables later as a
      non-destructive migration.
    - Generic interface needs a narrowing mechanism — Leandro explicitly wants to
      AVOID writing Guest/AdditionalGuest-specific handlers for reused steps
      (schema_form/handler.py:76).
    - Flow slugs can no longer be arbitrary → he suggests making slugs an enum
      (views/session.py:40).
    - Schemaform field identification is a "quick hack" (using a tag); proper
      approach would use schemaform field tags.
    - Steps must be registered in BOTH framework implementations + typed
      accordingly (duplication noted as a cost).

  **Why this matters / where it's headed:** this is foundational architecture for
  the guest-experience flow builder (check-in + additional guests + ID capture as
  composable nested flows). Two competing implementations now exist (Matt's design
  doc #47319 vs Leandro's end-to-end #47372); Matt is asking Leandro for a
  recommendation. No decision recorded yet — the open question is whether to commit
  to this child-session primitive and which session-shape to standardize on,
  knowing N-level nesting is still unsolved.

  **No action taken** (read-only digest task). Possible follow-ups for the user:
  weigh in on Matt's "any new thoughts" question, or push on how N-level nesting
  (ID-inside-additional-guest) should resolve before this primitive is locked in.
  Did NOT watch the Loom (can't process video) or post anything to Slack/GitHub.
project: 2026-04-10T0840-ticket
source_id: https://canarytechnologies.slack.com/archives/C0A5Z7LE5AL/p1780952564125569?thread_ts=1780952564.125569&cid=C0A5Z7LE5AL
tags:
- morning-gtd
- slack
- from-awareness
time_minutes: 10
title: 'Read: flow-builder step-configurator POC (Leandro)'
updated: 2026-06-15 13:39:11.830360
waiting_on: null
waiting_since: null
working_on: false
---

New POC based on Matt's version. https://canarytechnologies.slack.com/archives/C0A5Z7LE5AL/p1780952564125569?thread_ts=1780952564.125569&cid=C0A5Z7LE5AL