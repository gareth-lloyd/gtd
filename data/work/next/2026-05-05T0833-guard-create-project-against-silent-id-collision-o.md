---
area: engineering
contexts: []
created: 2026-05-05 08:33:00
defer_until: null
due: null
energy: low
id: 2026-05-05T0833-guard-create-project-against-silent-id-collision-o
order: 9
output: ''
project: 2026-04-27-gtd
source_id: null
tags: []
time_minutes: 15
title: Guard create_project against silent ID collision overwrite
updated: 2026-06-25 12:17:49.616303
waiting_on: null
waiting_since: null
working_on: false
---

`create_project` calls `repo.save_project` which calls `dump_project` which overwrites blindly. If the user supplies an id that's already taken, the existing project is silently destroyed.

Same class of bug as the item collision we just fixed for captures. One-line fix in `service.create_project`: raise `ValueError` if `(env_root / 'projects' / f'{project_id}.md').exists()`. Surface as 409 Conflict in the API.