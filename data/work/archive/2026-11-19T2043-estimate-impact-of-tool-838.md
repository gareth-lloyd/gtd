---
area: null
completed_at: 2026-11-20 14:15:55.464885
contexts: []
created: 2026-11-19 20:43:24.854594
defer_until: null
due: null
energy: low
id: 2026-11-19T2043-estimate-impact-of-tool-838
order: null
output: |
  ## Agent run 2026-11-20T11:06:09Z

  TOOL-838 (https://linear.app/canary-technologies/issue/TOOL-838/workup-stop-copying-investigate-plugin-rules-into-the-agents-repo): Backlog, unassigned, no comments, filed 2026-10-09 by Laura DeWald in project "AI Workup: Accuracy Phase 1-5".

  I read "impact" as: what does doing it buy. Say if you meant effort or blast radius.

  ### Estimate

  - Production accuracy: about 0 points. The ticket scopes out any rule change ("each step keeps today's production behavior").
  - Production risk removed: small today. I found no live divergence in the copies production runs on.
  - Main gain: replay harness fidelity, and no second PR in canary-agents per rule change. That matters because the accuracy proposals (TOOL-937 and the 2026-11-02 set) get judged on the replay.
  - Size: medium, spanning both repos. Roughly 1,900 lines across the 7 named overlord files, plus a new `pipeline candidates` step and two schemas in the plugin. This is my guess, not a scoped estimate.

  ### Evidence (canary-agents origin/main c353893b and canary origin/master, both fetched today)

  Rule churn is high, so copies do go stale:
  - 24 commits touched the plugin's `core/rules` or `core/taxonomies` since 2026-10-09, about 4 a week. 44 if you include `scripts/`.
  - In the same six weeks I count about 5 overlord commits that exist only to follow a plugin change: #412 (TOOL-734 "Mirror the plugin's Request Info rule in the replay template"), #483 (TOOL-898 label rename), #467, #624, and #484 below. Counted from commit titles, not diffs.

  Part of the ticket is already done:
  - Step 1 and 4, partly: TOOL-909 (#484, 2026-10-23) made the replay build its taxonomy from a plugin checkout. `taxonomy.ts` (394 lines) keeps the embedded copy as a fallback. `replay/drive.ts` runs the plugin's own driver.
  - Still open: `applyRules` in `replay/debate.ts` (line 236), the closed-status list in `replay/tickets.ts`, `INCIDENT_TEAM_KEYS` and `CLOSED_STATE_TYPES` in `agents/workup/auto-close.ts`, the "update both together" slugs in `next-step-label.ts`, and the quoted heading in `sql-guidance.ts`.
  - Steps 2, 3 and 5 not started: no `pipeline candidates` step, and `core/schemas/` has no `hypothesis-v1` or declaration schema.

  Current drift, checked:
  - `auto-close.ts` `INCIDENT_TEAM_KEYS` equals the plugin's `incident_team_keys` (INCINT, INCWYN, INCBW, INCIHG). No divergence.
  - `auto-close.ts` has no VXP exclusion. No production effect, because `pipeline declare` rejects a VXP target before auto-close sees it.
  - `sql-guidance.ts` quotes the "Canary SQL" heading under "Canary MCP". The heading still exists in `bindings/claude-code.md` (line 83). Works today, breaks on a rename.
  - `tickets.ts` still treats `released` and `shipped` status names as closed, which the plugin rule does not name. Harness only.
  - The harness port of the duplicate rules (TOOL-837) is not on origin, so it is still uncommitted or gone. A replay that does not score through `--drive` ignores the VXP exclusion.
  - The ticket says the plugin does not treat a duplicate-closed target as closed. The plugin's `next-steps.md` now says a target "closed as a duplicate of another ticket" is never a merge target, so that part of the ticket looks stale. I did not read `steps.py` to confirm.

  ### Not measured

  - How many replay scores the remaining drift moves. Upper bound is the duplicate slice: 69 declared duplicates in 573 tickets since 09-21 (about 12%, from `backend/canary/tmp/data/workup_accuracy/NOTES.md`). Only candidates in VXP or in `released`/`shipped` status inside that slice can differ. A query on `workup_declarations` targets by team and status would give the real number.
  - Whether `next-step-label.ts` slugs match `next-steps.md` today. I did not diff them.

  ### Suggested call

  Low urgency for production. Worth doing before leaning on the replay to accept or reject a duplicate-rule change such as TOOL-937, since that is the slice where harness and driver disagree. Steps 2 and 5 carry most of the value. Step 1 is half done.
project: null
source_id: null
tags: []
time_minutes: 5
title: estimate impact of TOOL-838
updated: 2026-11-20 14:15:55.464877
waiting_on: null
waiting_since: null
working_on: false
---