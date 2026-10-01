---
area: null
completed_at: 2026-10-01 16:41:12.091485
contexts: []
created: 2026-10-01 16:31:50.006257
defer_until: null
due: null
energy: low
id: 2026-10-01T1631-review-laura-s-report
order: null
output: |-
  ## Agent run 2026-10-01T16:42 (local), rewritten after a second pass against the code

  **Verdict:** Laura's diagnosis is right and both fixes are correct. Reading the code changes the story in one important way: Sonnet 5.5 was not really disobeying a procedure, because nothing Workup enforces, and nothing in the prompt Workup builds, requires the procedure. Sonnet 5 inferred it; Sonnet 5.5 took the prompt literally. The alias change was the trigger, and it was a deliberate design choice, not an oversight.

  Sources:
  - Laura's post (https://canarytechnologies.slack.com/archives/C0AL1T2H43V/p1790818758872119), no replies
  - agents PR #334, merged, pins Workup to Sonnet 5 (https://github.com/canary-technologies-corp/agents/pull/334)
  - agents PR #335, merged, prices Sonnet 5.5 (https://github.com/canary-technologies-corp/agents/pull/335)
  - agents PR #106, 2026-07-29, the change that unpinned the CLI (https://github.com/canary-technologies-corp/agents/pull/106)
  - TOOL-773, Backlog, assigned to Laura (https://linear.app/canary-technologies/issue/TOOL-773/investigate-plugin-make-gathering-unskippable-so-workup-can-move-to)
  - agents repo read at `origin/main` b27dfc03 (after both fixes); investigate plugin read at canary master 09dcddac88c

  ### Why it happened, with the code behind each point

  **1. The float was chosen on purpose, with nothing to catch a bad upgrade.**
  - `overlord/scripts/rebuild-template.ts:305-317` installs Claude Code with `curl ... install.sh | bash`, placed below a cache-bust. The comment says this is "what lets the versionless CLI aliases track new releases". PR #106 ("unfreeze baked CLI so opus alias tracks latest", EE-1779) made it so on 2026-07-29.
  - `.github/workflows/rebuild-e2b-template.yml:14` runs that rebuild nightly at 03:00 UTC. The only check on the new CLI is `claude --version`.
  - `overlord/src/types.ts:244-250` documents `Model.Sonnet` and `Model.Opus` as aliases that "track the tier's latest model". The dashboard offers them as "Claude Sonnet (latest)" (`dashboard/src/constants/models.ts`), and an agent with no model gets the sonnet alias by default (`overlord/src/core/registry.ts:189`).
  - So every nightly rebuild could change the model and the harness for every Claude Code agent, by design, with no trial run, no notice and no record of which CLI version landed.

  **2. The prompt Workup builds never asks for the procedure.**
  - `overlord/src/agents/workup/agent.ts:153` is the whole instruction: "Investigate the root cause using the <region MCP> tools and the investigate plugin." No file in the agents repo names `investigate-ticket` or the pipeline.
  - The only MANDATORY line in the prompt is to call `submit_diagnosis` (`agent.ts:189`).
  - The trailer instruction even describes the no-pipeline path as legitimate: when there is "a flow that writes no hypothesis.json at all", the model should pick the next step from its own analysis (`next-step-label.ts:58`).
  - Working the ticket by hand with the MCP tools and then submitting is therefore a literal reading of the prompt. This fits Laura's finding that rewording the skill does not help: the skipped skill's wording is never read.
  - Caveat: Workup's ground rules live in the dashboard's global Agent Prompt (`agent.ts:677`), which is not in the repo. It may name the skill. I could not read it.

  **3. The only enforced contract is "submit at least 40 characters".**
  - `submit-mcp.ts` and `submit-contract.ts` check length (40 to 10,000), the hash, the run id and the timestamp. Neither looks for a gatherer manifest, evidence or a run summary.
  - A missing run summary is tolerated: `readRunSummary` returns null and the run carries on (`agent.ts:544`). A missing trailer is a `log.warn`.
  - A run with no evidence is posted and labelled "Workup: Investigated" exactly like a full one, so the reader of the ticket cannot tell them apart.
  - The plugin's own gates only bind a run that enters the pipeline. `scripts/pipeline/run.py` refuses a step without `manifest.json`, but a run that never calls the pipeline never meets that check.
  - Gathering is two layers of prose: one paragraph in `investigate-ticket/SKILL.md:74` says to execute `gather-context`, itself a 319-line skill that dispatches each gatherer.
  - The one guard that does work, on `classification.json`, is a Claude Code hook in the agents repo (`overlord/src/agents/workup/hooks/guard-classification.sh`), not in the plugin.

  **4. The harness saw the model change and discarded it.**
  - Every stream event carries the concrete model, and `claude-code.ts:858` reads it, but only to pick a price.
  - The unpriced-model notice is one `log.warn` per run to pod logs (`claude-code.ts:868`). Nothing alerts on it.
  - The final result's per-model usage is summed and the model names dropped (`sumModelUsage`, `claude-code.ts:124`).
  - The Workup usage row writes a constant (`agent.ts:362`): the alias before #334, `Model.Sonnet5` after it. Usage data therefore said "sonnet" throughout and will say "Sonnet 5" whatever actually runs.

  **5. The evals covered the stage that was fine.** The 119-ticket replay tests synthesis, where Sonnet 5.5 is as good as Sonnet 5 (13 incorrect against 27, p = 0.17). Orchestration, the stage that broke, had no eval until Laura built the box reruns.

  ### Still open after the two PRs

  - **The CLI still floats nightly.** Neither PR touches `rebuild-template.ts`. The next release can change the system prompt, tools or aliases again.
  - **Three agents still use the alias:** `voiceinsights/agent.ts:43`, `voicemine/agent.ts:53`, `voicequality/agent.ts:41`. They have run Sonnet 5.5 since 9/29, and nothing I read says anyone checked them.
  - **Gatherers still float.** `bindings/claude-code.md:16` passes each skill's `model:` value straight to the sub-agent. 18 files in the investigate plugin declare an alias (16 `sonnet`, 2 `haiku`), and 31 do across `agent-plugins/claude-plugins/`. Workup is now a Sonnet 5 orchestrator dispatching Sonnet 5.5 gatherers, and nobody has measured the quality of 5.5's gathering.
  - **Sonnet 5.5 cannot be chosen by id.** It has a price row but no `Model` member, no `CLAUDE_MODEL_MAP` entry and no dashboard option, so the alias is the only way to run it.
  - **The usage row is still a constant** (point 4), so a repeat by another route would be invisible again.
  - **The new test covers Workup only.** It asserts `Model.Sonnet5` exactly.
  - **TOOL-773 scopes the fix to the plugin in the canary repo.** The guard it cites as precedent lives in overlord, and so does the submit path. A check in `submit-mcp.ts`, or a hook on `submit_diagnosis`, would bind a run that never enters the pipeline; a plugin-side gate would not. The prompt at `agent.ts:153` also needs to name the skill.
  - **Verification gaps.** #334's post-deploy check is unticked. #335 was approved with "Didn't verify values". The rerun harness sits on Laura's machine only.

  ### Lessons to take into account

  1. A floating dependency needs a counterweight. Either pin the CLI and the model and upgrade by PR, or keep the float and add a trial run plus a notice when the resolved model or CLI version changes.
  2. A model does what the enforced contract and the literal prompt ask. Anything else is one model's habit and will not survive an upgrade. Each step that must happen needs a gate at the one point every run passes through, which here is `submit_diagnosis`.
  3. Say what you want in the prompt you control. "Use the investigate plugin" left the choice of method to the model.
  4. Evaluate each stage a model swap touches, and score process (dispatch, evidence, run summary) as well as answer quality. Laura's harness is that gate once it is committed.
  5. Record what ran, not what was configured. The data was already in hand on every turn.
  6. A degraded run should look degraded. Posting a no-evidence diagnosis under the same "Investigated" label hides the failure from the people best placed to notice it.
  7. Workup results either side of 9/29 are not comparable. Tag any Workup numbers you set against something else, such as the TypeSafe backtest baseline, with the model that ran.

  ### Not checked

  - The dashboard's global Agent Prompt for Workup, which may name the skill (point 2).
  - Production data: whether post-deploy runs are healthy, and whether the voice agents regressed.
  - The Sonnet 5.5 prices in #335.
  - Which model Golem's runtime uses. The enterprise plugin declares no aliases.
project: null
source_id: null
tags: []
time_minutes: 5
title: Review laura's report
updated: 2026-10-01 16:42:06.070849
waiting_on: null
waiting_since: null
working_on: false
---

https://canarytechnologies.slack.com/archives/C0AL1T2H43V/p1790818758872119

Any lessons or underlying reasons WHY these failures happen that should be taken into account?