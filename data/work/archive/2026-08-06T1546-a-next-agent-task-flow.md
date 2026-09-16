---
area: null
completed_at: 2026-09-16 09:37:41.617335
contexts: []
created: 2026-08-06 15:46:13.964014
defer_until: null
due: null
energy: low
id: 2026-08-06T1546-a-next-agent-task-flow
order: null
output: "## Agent run 2026-09-16T09:26:42\n\nImplemented the \"Next agent work\" flow
  end to end. Committed to main as 5a3d35c3 (code only — data/ untouched). Service
  restarted via `make restart-service`.\n\n**UI**: the agent-log Full view (`/work/items/<id>/agent`)
  now has a \"▶ Next agent work\" box at the top, above the log. Type a follow-up,
  then click `\U0001F916 agent` or `\U0001F5A5️ desktop agent` (⌘↵ launches in iTerm).
  Buttons stay disabled while the box is blank. On launch the box clears, a toast
  confirms, and the item query is invalidated so the working_on pin shows.\n\n**Prompt**:
  the new session gets the item + its existing `output:` (the \"Prior agent runs\"
  section already existed) + a final `## Next agent work` section containing your
  text. That section tells the agent to treat the follow-up as the primary instruction,
  use the prior output as context rather than redo it, and quote the follow-up at
  the top of its new `## Agent run` section so the log records what was asked. The
  follow-up itself is not stored on the item.\n\n**Wiring**:\n- `gtd_core/agent_launch.py`
  `build_prompt(..., next_task=None)` — blank/whitespace treated as absent\n- `GtdService.launch_agent_session(...,
  next_task=None)` passthrough\n- `POST /api/envs/<env>/items/<id>/launch-agent/`
  accepts `next_task` in the body\n- `api.launchAgent(env, id, target, nextTask?)`\n-
  `AutoGrowTextarea` now forwards `id` so the label binds (was dropped before)\n-
  CLAUDE.md: new \"Next agent work\" bullet under Key conventions\n\n**Tests** (red
  → green): 4 new build_prompt tests, 1 service test, 2 API tests, 4 AgentLogView
  tests. Full run: 602 backend passed, 156 frontend passed, `./scripts/lint.sh` clean,
  `npm run build` ok.\n\n**Not verified in a browser** — jsdom tests only. Worth a
  quick look at the box's spacing on the Full view once you open it.\n"
project: 2026-04-27-gtd
source_id: null
tags: []
time_minutes: 5
title: A "next agent task" flow
updated: 2026-09-16 09:37:41.617329
waiting_on: null
waiting_since: null
working_on: false
---

Present a new input box at the top of the "Full view" of agent output: "Next agent work". 

It should be possible to write the next task and then click to launch a new agent session. This gets the old output and new task to work on.