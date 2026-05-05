---
area: engineering
contexts:
- craft
created: 2026-05-05 11:04:00
defer_until: null
due: null
energy: medium
id: 2026-05-05T1104-gtd-new-skill-gtd-defer-for-batch-deferral
order: null
project: 2026-04-27-gtd
source_id: null
tags:
- gtd-meta
- skills
time_minutes: 60
title: 'GTD: new skill /gtd-defer for batch deferral'
updated: 2026-05-05 15:13:55.036611
waiting_on: null
waiting_since: null
working_on: false
---

**Problem.** Mid-week the next-actions list piles up with items I
won't get to today/this week. No fast way to triage by deferring N
items to a future date in one pass.

**Approach.**
- New skill file `.claude/skills/gtd-defer.md`. Look at
  `.claude/skills/gtd-coach.md` for tone/quality reference.
- Pairs with item #2 (batch ops). If the batch endpoint exists, the
  skill uses it; otherwise it loops PATCH calls.
- Flow: list `next/` items grouped by project. For each, ask
  `defer / keep / action`. Or "defer all to <date>" for bulk.
  Accepts shorthand like "tomorrow 9am", "next monday", "1w" —
  reuses `parse_human_datetime()` from `gtd_core/dates.py`.
- Voice: warm and direct, like `/gtd-coach`. No lecturing.
- Optional: persist a defer log in `data/<env>/digests/defer-log.md`
  so the user can see what they keep pushing.

**Verification.** Manual: run `/gtd-defer` against `data/work/`,
confirm items move/get `defer_until` set and the changes show up
in the UI.

**Size.** S (~1h)