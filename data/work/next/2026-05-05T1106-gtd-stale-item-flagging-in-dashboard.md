---
area: engineering
contexts:
- craft
created: 2026-05-05 11:06:00
defer_until: null
due: null
energy: low
id: 2026-05-05T1106-gtd-stale-item-flagging-in-dashboard
order: 8
output: ''
project: 2026-04-27-gtd
source_id: null
tags:
- gtd-meta
- skills
time_minutes: 30
title: 'GTD: stale-item flagging in dashboard'
updated: 2026-05-18 12:38:59.421745
waiting_on: null
waiting_since: null
working_on: false
---

**Problem.** Dashboard surfaces good signals but misses decay:
items in `next/` not touched in 30+ days, projects with zero next
actions, inbox items >24h old.

**Approach.**
- Edit `.claude/skills/gtd-dashboard.md` to compute and display:
  - Stale next: `count(next/* where updated < today-30d)` plus list
  - Stuck inbox: `count(inbox/* where created < today-1d)` (already
    partly there — verify and round out)
  - Projects with no actions: list project titles where no `next/`
    item references the project id
- Reuse existing service methods (`list_items`, `list_projects`).
- Cap surfaced lists at 10 entries each so dashboard stays scannable.

**Verification.** Run `/gtd-dashboard` against current data, verify
counts match a manual `grep` / `find` cross-check.

**Size.** S (~30 min)