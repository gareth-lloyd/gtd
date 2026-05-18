---
area: null
contexts: []
created: 2026-05-18 11:51:39.649834
defer_until: null
due: null
energy: low
id: 2026-05-18T1151-keep-next-as-a-selected-option
order: null
output: |
  ## Agent run 2026-05-18T12:41

  Done. The bucket buttons in WorkflowActions previously *filtered out* the
  item's current bucket, so a "next" item showed only → waiting / → someday
  and no indication it was already in "next". Now the current bucket among
  next/waiting/someday is rendered as a selected, non-actionable button.

  Changes:
  - `frontend/src/WorkflowActions.tsx`: instead of `.filter(b => status !== b)`,
    map all three buckets. The current one renders as a disabled `<Button
    aria-pressed>` showing just the bucket name (no `→` arrow, since it's the
    current state, not a move target); the others stay as `→ bucket` move
    buttons. No moveItem call fires on the selected one.
  - `frontend/src/styles.css`: added `.item-actions button[aria-pressed="true"]`
    — accent fill + white text (mirrors the existing `.chip-toggle` selected
    look), `cursor: default`, full opacity so it doesn't read as merely
    disabled.
  - `frontend/src/WorkflowActions.test.tsx`: updated the "current bucket"
    expectation and added a test asserting clicking the selected button does
    not call moveItem.

  Verification: `npm test` 132/132 pass, `npm run typecheck` clean,
  `npm run build` succeeds.

  Notes / scope:
  - The task also said "generally speaking, keep the current state in a
    selected form on item detail." This change covers the bucket/status row
    (the explicit example). The detail editor's other fields (project,
    contexts, energy, time, area) already reflect current state via
    ChipToggleGroup `aria-pressed`. The one place current state was hidden
    rather than shown-selected was this bucket row, which is now fixed. If
    you want the same treatment somewhere else specific, point me at it.
  - Frontend `dist/` was rebuilt (committed assets changed). Treat as a code
    change, not data.
project: 2026-04-27-gtd
source_id: null
tags: []
time_minutes: 5
title: Keep "next" as a selected option in item detail. Currently if the item is "next",
  this optino is not visible
updated: 2026-05-18 12:41:30.000000
waiting_on: null
waiting_since: null
working_on: false
---

generally speaking, keep the current state in a selected form on item detail