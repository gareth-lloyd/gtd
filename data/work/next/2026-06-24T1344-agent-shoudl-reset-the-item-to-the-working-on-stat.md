---
area: null
contexts: []
created: 2026-06-24 13:44:22.059992
defer_until: null
due: null
energy: low
id: 2026-06-24T1344-agent-shoudl-reset-the-item-to-the-working-on-stat
order: null
output: |
  ## Agent run 2026-06-24T14:05

  Done. The agent exit protocol now restores the item's *prior* working_on
  state instead of always clearing it to false.

  ### The bug
  `service.launch_agent_session()` sets `working_on: true` on launch. The
  generated prompt then told the agent to "set `working_on: false`" as its
  exit protocol — unconditionally. So an item the user had *already pinned*
  before launching the agent would get silently un-pinned (dropped off the
  working-on list) when the agent finished. That's the "always reset to not
  working on" behaviour you flagged.

  ### The fix
  - `service.py:launch_agent_session()` — capture `prior_working_on =
    item.working_on` BEFORE the launch flips it to true, and pass it into
    `build_prompt(..., prior_working_on=...)`.
  - `agent_launch.py:build_prompt()` — new `prior_working_on: bool = False`
    kwarg. Computes `working_on_target = "true" if prior_working_on else
    "false"` and threads it through both spots in the prompt that name the
    exit value (the "## STRICT" exit-protocol bullet and the "## Working on"
    section). When the item was pre-pinned the prompt now instructs the
    agent to restore `working_on: true` and explains *why* (clearing it
    would drop it off the user's active list); otherwise it keeps the
    existing clear-to-false behaviour.

  Net: fresh launches still clear the flag on finish (unchanged); launches
  of an already-pinned item leave it pinned.

  ### Tests (red/green TDD)
  - `gtd_core/tests/test_agent_launch.py` — added
    `test_exit_clears_working_on_when_not_previously_pinned` and
    `test_exit_restores_prior_pin_when_already_working_on`.
  - `gtd_core/tests/test_service.py` (TestLaunchAgentSession) — added
    `test_prompt_clears_pin_when_not_previously_working_on` and
    `test_prompt_restores_prior_pin_when_already_working_on`.

  Full backend suite: 561 passed. `ruff check` clean. No frontend changes
  (the prompt is built entirely server-side).

  ### Notes / open questions for you
  - This is uncommitted. Per project rules I have NOT committed code or run
    a data snapshot — that's your call.
  - The change only affects what the *generated prompt* tells the agent to
    do on exit. It relies on the agent following the instruction. If you'd
    rather enforce it mechanically (e.g. have the service restore the prior
    state when the agent session ends), that'd be a larger change — flag it
    if you want it.
project: 2026-04-27-gtd
source_id: null
tags: []
time_minutes: 5
title: agent shoudl reset the item to the working-on state encountered WHEN it picked
  up the ticket, not always reset to "not working on"
updated: 2026-06-24 14:05:00.000000
waiting_on: null
waiting_since: null
working_on: false
---