# data/

This directory IS the GTD system. Every item and project is a file here.
It's tracked in the same git repo as the code.

## Structure

```
data/
├── work/                     One directory per environment
│   ├── config.yml            Contexts, areas, defaults
│   ├── inbox/                Unclarified captures
│   ├── next/                 Committed next actions
│   ├── waiting/              Delegated / blocked
│   ├── someday/              Not committed, review periodically
│   ├── reference/            Not actionable, worth keeping
│   ├── projects/             Project metadata files
│   ├── templates/            Recurring item templates (see below)
│   ├── archive/              Completed items
│   └── trash/                Soft-deleted items
└── home/
    └── (same structure)
```

## Item file format

Each item is a markdown file. Filename = immutable ID.

```markdown
---
id: 2026-04-10T0915-call-dentist
title: Call dentist to reschedule cleaning
created: 2026-04-10 09:15:00
updated: 2026-04-10 09:15:00
contexts: [calls, errands]
energy: low
time_minutes: 5
project: null
area: health
tags: [dentist]
due: null
defer_until: null
waiting_on: null
waiting_since: null
---

Notes go here as markdown body.
```

**Status is NOT in the frontmatter.** It's the parent directory name.
Moving `inbox/foo.md` to `next/foo.md` changes the item's status.

## config.yml

```yaml
name: work
contexts: [anywhere, calls, computer, errands, meetings, office]
areas: [admin, engineering, management, writing]
default_energy: medium
```

Contexts are strict — the service layer rejects unknown values.
Areas are validated on update. Adding a new context/area means
editing this file.

## Reading data in a Claude CLI session

Read files directly — no server needed:

```sh
ls data/work/inbox/           # what's in the inbox?
cat data/work/next/*.md       # all next actions
grep -l "project: p1" data/work/next/*.md   # actions for project p1
```

Or use the service layer in Python:

```python
from pathlib import Path
from gtd_core.service import GtdService
svc = GtdService(Path("data"))
for item in svc.filter_next("work", contexts=["calls"]):
    print(item.title)
```

## Recurring templates

Files in `data/<env>/templates/` are item templates with a `recurrence` field:

```yaml
recurrence: weekly          # daily|weekly|biweekly|monthly|quarterly|yearly|every_N_days
last_spawned: 2026-04-10    # updated automatically after each spawn
```

Every snapshot (Sync button or `manage.py snapshot`) checks all templates
and spawns inbox items for any that are due. The spawned item copies the
template's title, body, contexts, energy, time, project, area, and tags.

## Committing data changes

Data changes are committed separately from code via the snapshot mechanism:

```sh
uv run manage.py snapshot                    # auto-generated message
uv run manage.py snapshot -m "weekly review" # custom message
uv run manage.py snapshot --push             # commit + push
```

Or via the Sync button in the web UI.
