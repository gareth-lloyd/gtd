---
area: engineering
contexts:
- deep
created: &id001 2026-05-05 11:08:00
defer_until: null
due: null
energy: medium
id: 2026-05-05T1108-gtd-inline-edit-deferred-items
order: null
project: 2026-04-16T1348-ideas
source_id: null
tags:
- gtd-meta
- frontend
time_minutes: 60
title: 'GTD: inline-edit deferred items'
updated: *id001
waiting_on: null
waiting_since: null
working_on: false
---

**Problem.** Items with `defer_until` show a read-only banner +
separate "Edit scheduled item" unlock button in
`DetailPanel.tsx` and `ItemCard.tsx`. Two clicks where one would do.

**Approach.**
- Remove the unlock dance in both components.
- Replace the banner with a small "scheduled" hint chip showing the
  defer date.
- Keep all fields editable inline, same as non-deferred items.
- Optional: muted background to retain a visual signal that the
  item is scheduled.

**Verification.**
- Component test for deferred-item edit path.
- E2E: click into a deferred item, edit title, assert PATCH fires
  and persists.

**Size.** S (~1h)