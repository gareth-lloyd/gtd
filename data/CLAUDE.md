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
order: null
---

Notes go here as markdown body.
```

**Status is NOT in the frontmatter.** It's the parent directory name.
Moving `inbox/foo.md` to `next/foo.md` changes the item's status.

`order` is only meaningful when the item's project has a `max_next_items`
cap set. It sorts the project's actions and controls which N items surface
on the next-actions list (N = `max_next_items`).

## Project file format

```markdown
---
id: 2026-04-10T0915-launch-blog
title: Launch personal blog
created: 2026-04-10 09:15:00
updated: 2026-04-10 09:15:00
status: active           # active | on_hold | complete | dropped
outcome: Blog live with 3 posts
area: hobbies
tags: []
due: 2026-06-01          # optional hard deadline
priority: 2              # 1 (most urgent) … 5 (aspirational) or null
max_next_items: 1        # optional cap on next-list items per project (null = no cap, 1 = one at a time)
---

Project notes / context / outcome detail.
```

## config.yml

```yaml
name: work
contexts: [deep, craft, quick, consume, autopilot, listen, fun]
areas: [admin, engineering, management, writing]
default_energy: medium
```

Contexts are strict — the service layer rejects unknown values.
Areas are validated on update. Adding a new context/area means
editing this file.

Current real-world contexts:
- `work`: deep, craft, quick, consume, autopilot, listen, fun
  - `deep`: protected solo time for generative work (PRDs, plans, expansive synthesis)
  - `craft`: sustained careful writing where words matter (people writeups, polished comms, Looms)
  - `quick`: bursty 5–20m between-meeting work that needs attention (PR reviews, Slack/Linear replies)
  - `consume`: focused input — reading docs, briefing yourself before deciding
  - `autopilot`: low-cognitive-engagement execution (Linear cleanup, calendar admin, batch updates)
  - `listen`: audio-only work away from the computer (recorded meetings, podcasts)
  - `fun`: orthogonal axis — intrinsically rewarding work; can combine with any other context
- `home`: computer, errands, calls, home, watch, read, out, anywhere

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
