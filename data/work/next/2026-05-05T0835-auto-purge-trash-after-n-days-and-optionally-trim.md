---
area: engineering
contexts: []
created: 2026-05-05 08:35:00
defer_until: null
due: null
energy: low
id: 2026-05-05T0835-auto-purge-trash-after-n-days-and-optionally-trim
order: null
project: 2026-04-27-gtd
source_id: null
tags: []
time_minutes: 45
title: Auto-purge trash after N days (and optionally trim archive)
updated: 2026-05-05 15:05:41.179989
waiting_on: null
waiting_since: null
working_on: false
---

`service.delete()` is soft (move to trash). Nothing GCs trash — it accumulates forever. `repo.get()` will resurrect a trashed item by ID lookup (scans all buckets), and the directory grows unbounded.

Fix: `manage.py purge_trash --older-than 30d` or similar, plus an optional sweep step in `snapshot_endpoint`. Optionally trim archive entries > N months for performance (list_done already paginates but file scans get slow).