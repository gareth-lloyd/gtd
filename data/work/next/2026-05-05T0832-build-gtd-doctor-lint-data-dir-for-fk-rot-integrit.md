---
area: engineering
contexts: []
created: 2026-05-05 08:32:00
defer_until: null
due: null
energy: high
id: 2026-05-05T0832-build-gtd-doctor-lint-data-dir-for-fk-rot-integrit
order: 11
output: ''
project: 2026-04-27-gtd
source_id: null
tags: []
time_minutes: 180
title: 'Build gtd-doctor: lint data dir for FK rot + integrity issues'
updated: 2026-06-17 13:53:06.260581
waiting_on: null
waiting_since: null
working_on: false
---

Single defensive CLI/management command that surfaces everything that can silently rot:

- Items with `project` pointing to a non-existent project.
- Items with contexts no longer in config.yml.
- Items with `area` no longer in config.yml.
- Same item id present in two buckets simultaneously (move-crash   legacy — should be rare post-atomic-relocate but still possible   from manual git surgery).
- Files where `path.stem != md['id']`.
- Active items in `complete` or `dropped` projects.
- Stale `.tmp` orphans under data/.

Report read-only by default; `--fix` for trivial repairs (delete tmp orphans, etc.). Run weekly as part of the review.