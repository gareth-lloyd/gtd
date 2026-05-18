---
area: null
contexts: []
created: 2026-05-18 11:51:39.649834
defer_until: null
due: null
energy: low
id: 2026-05-18T1151-keep-next-as-a-selected-option
order: null
output: "## Agent run 2026-05-18T12:41\n\nDone. The bucket buttons in WorkflowActions
  previously *filtered out* the\nitem's current bucket, so a \"next\" item showed
  only → waiting / → someday\nand no indication it was already in \"next\". Now the
  current bucket among\nnext/waiting/someday is rendered as a selected, non-actionable
  button.\n\nChanges:\n- `frontend/src/WorkflowActions.tsx`: instead of `.filter(b
  => status !== b)`,\n  map all three buckets. The current one renders as a disabled
  `<Button\n  aria-pressed>` showing just the bucket name (no `→` arrow, since it's
  the\n  current state, not a move target); the others stay as `→ bucket` move\n  buttons.
  No moveItem call fires on the selected one.\n- `frontend/src/styles.css`: added
  `.item-actions button[aria-pressed=\"true\"]`\n  — accent fill + white text (mirrors
  the existing `.chip-toggle` selected\n  look), `cursor: default`, full opacity so
  it doesn't read as merely\n  disabled.\n- `frontend/src/WorkflowActions.test.tsx`:
  updated the \"current bucket\"\n  expectation and added a test asserting clicking
  the selected button does\n  not call moveItem.\n\nVerification: `npm test` 132/132
  pass, `npm run typecheck` clean,\n`npm run build` succeeds.\n\nNotes / scope:\n-
  The task also said \"generally speaking, keep the current state in a\n  selected
  form on item detail.\" This change covers the bucket/status row\n  (the explicit
  example). The detail editor's other fields (project,\n  contexts, energy, time,
  area) already reflect current state via\n  ChipToggleGroup `aria-pressed`. The one
  place current state was hidden\n  rather than shown-selected was this bucket row,
  which is now fixed. If\n  you want the same treatment somewhere else specific, point
  me at it.\n- Frontend `dist/` was rebuilt (committed assets changed). Treat as a
  code\n  change, not data.\n"
project: 2026-04-27-gtd
source_id: null
tags: []
time_minutes: 5
title: Keep "next" as a selected option in item detail. Currently if the item is "next",
  this optino is not visible
updated: 2026-05-18 13:24:58.456463
waiting_on: null
waiting_since: null
working_on: false
---

generally speaking, keep the current state in a selected form on item detail