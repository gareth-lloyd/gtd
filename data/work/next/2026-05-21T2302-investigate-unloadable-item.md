---
area: null
contexts: []
created: 2026-05-21 23:02:36.310522
defer_until: null
due: null
energy: low
id: 2026-05-21T2302-investigate-unloadable-item
order: -19
output: |
  ## Agent run 2026-05-22T10:30Z

  ### Identified the unloadable item
  `data/work/next/2026-05-14T1120-marriott-managed-situation.md`
  (only file in the repo that fails `storage.load_item`).

  ### Root cause
  The `output:` field opens as a single-quoted YAML scalar on line 10
  (`output: '## Agent run 2026-05-14T13:05Z`) but the closing `'` was
  missing. PyYAML died with
  `ScannerError: while scanning a quoted scalar, found unexpected end of stream`.

  Looking at the file structure, the first agent run (2026-05-14T13:05Z)
  was clearly written via the service layer / PyYAML serializer (heavy use
  of `''` escapes throughout the block, consistent indentation). A second
  section (`## Agent run 2026-05-21T10:30Z — FIX APPLIED`) was then appended
  in-place — most likely by a Claude agent editing the file directly — and
  the appended content was not properly terminated. The closing `'` that
  used to sit between "Source pointers" and `project:` got swallowed by the
  insert, leaving the entire scalar open all the way to EOF.

  ### Fix applied
  Added the missing closing `'` at the end of line 267 (after
  "Could be batch-cleared with a confirmation step."). Verified with:
    - `storage.load_item` on the file → loads cleanly, output is 11_767 chars.
    - Full scan of every bucket (inbox/next/waiting/someday/reference/
      archive/trash) → 0 load errors.

  ### Upstream risk (FYI — no action taken)
  This is a recurring failure mode for the `🤖 agent` flow. The agent
  launch prompt tells the agent to "append findings to `output:`", and
  agents that edit the YAML directly (rather than re-serialising the whole
  frontmatter through PyYAML or the service layer) can silently produce
  invalid YAML when the existing value is a single-quoted scalar with `''`
  escapes. Once the file is unloadable, the web UI can't open it, and
  `service.update_item()` can't be used to fix it (the load step blows up
  first), so the only recovery is direct file editing.

  Possible mitigations to consider in a separate task:
  1. Have the agent-launch prompt explicitly tell the agent to use the
     service / PATCH API rather than raw-edit the file, OR to re-write the
     `output:` value as a YAML literal block scalar (`|`) which is
     append-safe and needs no escaping.
  2. Add a `gtd doctor` / lint command that load-tests every item file and
     flags failures, so unloadable items are surfaced fast (the web UI
     today probably 500s or silently drops the item).
  3. Switch the storage layer to write `output:` (and any other long
     multi-line field) as a literal block scalar by default, since
     single-quoted multi-line scalars are needlessly brittle.

  Not filing those — leaving the decision to the user.
project: 2026-04-27-gtd
source_id: null
tags: []
time_minutes: 5
title: investigate unloadable item
updated: 2026-05-22 10:30:00.000000
waiting_on: null
waiting_since: null
working_on: false
---