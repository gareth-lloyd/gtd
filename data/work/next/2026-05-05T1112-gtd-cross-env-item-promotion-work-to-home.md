---
area: engineering
contexts:
- deep
created: &id001 2026-05-05 11:12:00
defer_until: null
due: null
energy: medium
id: 2026-05-05T1112-gtd-cross-env-item-promotion-work-to-home
order: null
project: 2026-04-16T1348-ideas
source_id: null
tags:
- gtd-meta
- backend
- frontend
time_minutes: 90
title: 'GTD: cross-env item promotion (work to home)'
updated: *id001
waiting_on: null
waiting_since: null
working_on: false
---

**Problem.** When an item lands in `work/` but really belongs to
`home/` (or vice versa), there's no UI to move it. Today you'd shell
in and move the file manually, then fix any context/area mismatches.

**Approach.**
- **Backend.** New service method
  `GtdService.promote(env, item_id, target_env)`:
  - Validate target env exists
  - Validate contexts and area against target env's `config.yml`;
    drop invalid ones with a warning surfaced via the response
  - Move the file; preserve id, created, body, tags, working_on
  - Clear `project` (project belongs to source env's project list)
- New endpoint
  `POST /api/envs/<env>/items/<id>/promote/` taking
  `{ target_env: string }`.
- **Frontend.** Add to the move dropdown menu:
  "Promote to home" / "Promote to work" (label depends on current
  env). Confirm dialog if contexts/area would change.

**Verification.**
- Backend tests for promote with various context/area combos
  (full overlap, partial, none).
- E2E: capture an item in work, promote to home, confirm it
  disappears from work and appears in home/inbox.

**Size.** M (~90 min)