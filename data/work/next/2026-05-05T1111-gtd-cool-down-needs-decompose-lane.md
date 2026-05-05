---
area: engineering
contexts:
- deep
- fun
created: &id001 2026-05-05 11:11:00
defer_until: null
due: null
energy: medium
id: 2026-05-05T1111-gtd-cool-down-needs-decompose-lane
order: null
project: 2026-04-16T1348-ideas
source_id: null
tags:
- gtd-meta
- creative
time_minutes: 120
title: 'GTD: cool-down / needs-decompose lane'
updated: *id001
waiting_on: null
waiting_since: null
working_on: false
---

**Problem.** Some inbox items are really projects-in-disguise.
`/gtd-coach` detects this ad-hoc but there's no first-class signal
or surfaced lane. The detection is in the model's head, not in the
data.

**Approach.**
- Add `needs_decompose: bool = False` to the `Item` dataclass
  (`gtd_core/models.py`) plus storage round-trip.
- Update `.claude/skills/gtd-coach.md` and `.claude/skills/gtd-inbox.md`
  to set the flag (with user confirmation) when they detect a
  decompose candidate, instead of just suggesting it verbally.
- Dashboard surfaces "Needs decompose: N" with the list.
- New skill `/gtd-decompose` (or extension of `/gtd-coach`) walks
  through flagged items and helps create a project + first 1-3
  next actions per item. Clears the flag on success.

**Verification.**
- Backend test: round-trip the new field.
- Manual: run `/gtd-coach`, mark an item, observe flag persists,
  walk through `/gtd-decompose`, observe project + actions land in
  data.

**Size.** M (~2h)