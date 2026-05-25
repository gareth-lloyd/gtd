---
area: null
contexts: []
created: 2026-05-21 23:02:36.310522
defer_until: null
due: null
energy: low
id: 2026-05-21T2302-investigate-unloadable-item
order: -19
output: "## Agent run 2026-05-22T10:30Z\n\n### Identified the unloadable item\n`data/work/next/2026-05-14T1120-marriott-managed-situation.md`\n(only
  file in the repo that fails `storage.load_item`).\n\n### Root cause\nThe `output:`
  field opens as a single-quoted YAML scalar on line 10\n(`output: '## Agent run 2026-05-14T13:05Z`)
  but the closing `'` was\nmissing. PyYAML died with\n`ScannerError: while scanning
  a quoted scalar, found unexpected end of stream`.\n\nLooking at the file structure,
  the first agent run (2026-05-14T13:05Z)\nwas clearly written via the service layer
  / PyYAML serializer (heavy use\nof `''` escapes throughout the block, consistent
  indentation). A second\nsection (`## Agent run 2026-05-21T10:30Z — FIX APPLIED`)
  was then appended\nin-place — most likely by a Claude agent editing the file directly
  — and\nthe appended content was not properly terminated. The closing `'` that\nused
  to sit between \"Source pointers\" and `project:` got swallowed by the\ninsert,
  leaving the entire scalar open all the way to EOF.\n\n### Fix applied\nAdded the
  missing closing `'` at the end of line 267 (after\n\"Could be batch-cleared with
  a confirmation step.\"). Verified with:\n  - `storage.load_item` on the file → loads
  cleanly, output is 11_767 chars.\n  - Full scan of every bucket (inbox/next/waiting/someday/reference/\n
  \   archive/trash) → 0 load errors.\n\n### Upstream risk (FYI — no action taken)\nThis
  is a recurring failure mode for the `\U0001F916 agent` flow. The agent\nlaunch prompt
  tells the agent to \"append findings to `output:`\", and\nagents that edit the YAML
  directly (rather than re-serialising the whole\nfrontmatter through PyYAML or the
  service layer) can silently produce\ninvalid YAML when the existing value is a single-quoted
  scalar with `''`\nescapes. Once the file is unloadable, the web UI can't open it,
  and\n`service.update_item()` can't be used to fix it (the load step blows up\nfirst),
  so the only recovery is direct file editing.\n\nPossible mitigations to consider
  in a separate task:\n1. Have the agent-launch prompt explicitly tell the agent to
  use the\n   service / PATCH API rather than raw-edit the file, OR to re-write the\n
  \  `output:` value as a YAML literal block scalar (`|`) which is\n   append-safe
  and needs no escaping.\n2. Add a `gtd doctor` / lint command that load-tests every
  item file and\n   flags failures, so unloadable items are surfaced fast (the web
  UI\n   today probably 500s or silently drops the item).\n3. Switch the storage layer
  to write `output:` (and any other long\n   multi-line field) as a literal block
  scalar by default, since\n   single-quoted multi-line scalars are needlessly brittle.\n\nNot
  filing those — leaving the decision to the user.\n"
project: 2026-04-27-gtd
source_id: null
tags: []
time_minutes: 5
title: investigate unloadable item
updated: 2026-05-25 11:33:29.059515
waiting_on: null
waiting_since: null
working_on: false
---