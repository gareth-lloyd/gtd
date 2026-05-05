---
area: engineering
contexts:
- autopilot
created: &id001 2026-05-05 11:10:00
defer_until: null
due: null
energy: low
id: 2026-05-05T1110-gtd-dead-code-cleanup-mockup-migration-source-id
order: null
project: 2026-04-16T1348-ideas
source_id: null
tags:
- gtd-meta
- hygiene
time_minutes: 30
title: 'GTD: dead-code cleanup (mockup, migration, source_id)'
updated: *id001
waiting_on: null
waiting_since: null
working_on: false
---

**Problem.** Three concrete pieces of dead code identified during the
tyre-kicking pass:
- `mockup.html` at repo root — discarded UI prototype, ~27 KB,
  pre-Vite. No code references.
- `scripts/migrate_sequential_to_max_next_items.py` — one-off
  migration that already ran.
- `Item.source_id` — frontmatter field never set in capture and
  never read in any code path.

**Approach.**
- Delete `mockup.html`.
- Delete `scripts/migrate_sequential_to_max_next_items.py`.
- For `source_id`: grep across the whole repo (including
  `bear_reader/`, importer code, frontend, tests) before deleting.
  If genuinely unused, remove from `gtd_core/models.py`, storage
  serialization, and any serializers. If found used by an importer
  or external tool, leave it and add a one-line comment in
  `models.py` documenting purpose.
- Run pytest + lint + frontend tests after each deletion.

**Verification.**
`./scripts/lint.sh && uv run pytest && cd frontend && npm test`
all pass after the cleanup.

**Size.** S (~30 min)