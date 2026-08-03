---
area: null
contexts: []
created: 2026-07-31 12:43:40.443507
defer_until: null
due: null
energy: low
id: 2026-07-31T1243-if-an-item-is-not-finished-clicking-reference-shou
order: -1
output: |
  ## Agent run 2026-07-31T12:55

  Implemented and committed to main as 5fe127da (18 files, all tests green).

  Design decision: "complete" was previously implied purely by the archive
  bucket, so filing an unfinished item to reference/ left no trace of the work
  (e.g. /eod scans archive/ mtimes and missed "review X" items you finished
  and filed as reference, like the GDPR email thread review on Jul 30). Fix
  lives in the service layer: items now carry a durable `completed_at`
  datetime in frontmatter.

  Behaviour of service.move():
  - Move to archive OR reference: stamps completed_at (if not already set) —
    clicking "→ reference" on an unfinished item now also marks it complete.
  - Already-completed items re-filed archive → reference keep their original
    stamp (the "if an item is not finished" conditional).
  - Move back to inbox/next/waiting/someday: clears the stamp (uncomplete).
  - Trash: preserves whatever state the item died in.
  - Legacy files without the key load as completed_at: null.

  Also: exposed completed_at in the API item payload and frontend Item type;
  added a tooltip on the active-item "→ reference" button ("File as reference
  — also marks the item complete"); updated CLAUDE.md + data/CLAUDE.md docs
  (the data/CLAUDE.md edit is uncommitted so it rides the next snapshot,
  keeping code and data commits separate).

  TDD: 9 new backend tests (service move semantics + storage round-trip) and
  2 API tests, written red-first. Full battery green: 583 backend, 146
  frontend, lint.sh clean, frontend rebuilt (npm run build).

  Possible follow-ups (not done): surface completed_at in the Done view or
  reference list UI; teach /eod to also grep reference/ for
  completed_at: <today>.
project: 2026-04-27-gtd
source_id: null
tags: []
time_minutes: 5
title: If an item is not finished, clicking "Reference" should also mark it as complete
updated: 2026-07-31 12:55:02
waiting_on: null
waiting_since: null
working_on: false
---