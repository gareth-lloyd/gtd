---
area: engineering
contexts: []
created: 2026-05-05 08:31:00
defer_until: null
due: null
energy: medium
id: 2026-05-05T0831-make-recurring-spawns-reliable-don-t-depend-on-man
order: null
project: 2026-04-27-gtd
source_id: null
tags: []
time_minutes: 90
title: Make recurring spawns reliable — don't depend on manual Sync
updated: 2026-05-05 15:05:34.583491
waiting_on: null
waiting_since: null
working_on: false
---

`spawn_recurring` only runs inside `snapshot_endpoint`. Skip a Sync on the scheduled day → that period's item is silently lost forever. Templates also never spawn at all if you only edit via CLI.

Options:
- Spawn on server start (lazy catch-up at boot).
- Add a periodic `manage.py spawn_recurring` cron / loop.
- Lazy-spawn inside `list_templates` or `list_items` if any   template is overdue.
- (Aggressive) walk last_spawned forward and create missed items.   Currently `is_due` is exact-day-only by design — reconsider.