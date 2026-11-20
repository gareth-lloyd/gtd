---
area: null
completed_at: null
contexts: []
created: 2026-11-20 15:30:09.688510
defer_until: null
due: null
energy: low
id: 2026-11-20T1530-figure-out-why-sync-is-faliing
order: -1
output: |
  ## Agent run 2026-11-20T15:31

  **Cause.** Sync refuses to commit because one item file no longer parses:
  `data/home/next/2026-11-20T0023-copy-quote-to-clipboard-marks-as-sent-and-prevents.md`
  has no `title:` line in its frontmatter. Everything else in the file is
  intact (three agent runs in `output:`). It is the only unloadable file in
  either env.

  **Evidence.** `logs/gtd.log` at 13:29:56 UTC today: `skipping unloadable
  item … : 'title'`, then `Conflict: /api/snapshot/` (the POST returned 409).
  `_snapshot_locked` in `gtd_core/snapshot.py` returns early without
  committing when `_scan_unloadable` finds anything, and the view maps that
  to 409. Running `_scan_unloadable` directly returns just this one file.

  **Likely origin (my inference).** The file is untracked, so there is no git
  history for it. It was last written at 01:39 on 20 Nov, in the middle of
  the agent runs logged in its `output:`, so one of those sessions probably
  dropped the `title:` line while editing the frontmatter.

  **Fix (not done, yours to make).** Add a `title:` line to that file; sync
  should then work. I did not add it because the filename slug is truncated
  ("copy quote to clipboard marks as sent and prevents…") and I can't
  recover the full original title. The last successful snapshot was
  24c4fed1 on 18 Nov, so the next sync will be a big one.

  **Fixed 2026-11-20T15:40 (at your request).** Five frontmatter lines had
  been dropped, not just the title: `project`, `source_id`, `tags`,
  `time_minutes`, `title`. Restored all five from the original values
  recorded in the earlier agent session's transcript (title: "Copy quote to
  clipboard marks as sent and prevents copy again", project
  `2026-05-25-villa-collective`, 5 min). The item loads again and
  `_scan_unloadable` returns nothing. I have not run a sync myself.

  **Side effect while it was broken.** The item is hidden from the home next
  list, because the repository skips unloadable files.
project: 2026-04-27-gtd
source_id: null
tags: []
time_minutes: 5
title: figure out why sync is faliing
updated: 2026-11-20 15:40:00
waiting_on: null
waiting_since: null
working_on: false
---