---
area: engineering
contexts: []
created: 2026-05-05 08:30:00
defer_until: null
due: null
energy: medium
id: 2026-05-05T0830-validate-item-project-fk-cascade-on-project-delete
order: null
project: 2026-04-27-gtd
source_id: null
tags: []
time_minutes: 60
title: Validate item.project FK + cascade on project delete
updated: 2026-05-05 15:05:32.701116
waiting_on: null
waiting_since: null
working_on: false
---

Today `Item.project` can point to any string — `_validate_patch` doesn't check it. `delete_project` just unlinks the file, leaving items with `project: <dead-id>` that don't show in `no_project=true` filters and aren't visible in any project view.

Fix:
- `_validate_patch`: reject patches whose `project` is non-null but   not in `repo.list_projects(include_inactive=True)`.
- `delete_project`: count linked items first; either refuse,   cascade-clear, or move them to inbox (offer choice via API/UI).
- Same for `update_project(status='complete'|'dropped')` — surface   count of active actions, optionally archive them.