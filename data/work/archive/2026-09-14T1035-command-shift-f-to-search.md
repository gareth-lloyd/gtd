---
area: null
completed_at: 2026-09-16 09:22:20.869227
contexts: []
created: 2026-09-14 10:35:02.587070
defer_until: null
due: null
energy: low
id: 2026-09-14T1035-command-shift-f-to-search
order: null
output: |
  ## Agent run 2026-09-16T09:18

  Done. Added a Cmd/Ctrl+Shift+F keyboard shortcut that focuses the header
  search input. Committed to main as e016aa24, frontend rebuilt, local
  service restarted and verified serving the new bundle.

  What changed:
  - frontend/src/App.tsx: global keydown handler now checks for
    (Meta|Ctrl)+Shift+F before the existing "bail on any modifier" guard.
    Unlike the bare `/` shortcut, this one fires even when focus is inside
    another input/textarea (it's a chorded shortcut, so no typing conflict).
    Plain Cmd+F is untouched so browser find still works. Alt is excluded.
  - frontend/src/SearchComponents.tsx: header placeholder is now
    "Search… (/ or ⌘⇧F)".
  - frontend/src/App.test.tsx: 4 new tests (Cmd+Shift+F focuses search,
    Ctrl+Shift+F focuses search, works while typing in the capture bar,
    Cmd+F alone does NOT steal focus). Red first, then green.
  - CLAUDE.md: shortcut list updated.

  Verification: 152/152 frontend tests, 595/595 backend tests, lint.sh all
  clear (ruff, pyright, eslint, prettier, tsc), npm run build OK,
  `make restart-service` done and /static/assets bundle confirmed to contain
  the new hint.

  Not done / to decide:
  - Not pushed to any remote (local commit only).
  - Data files in the working tree were left uncommitted (snapshot is yours).
  - Hard-reload the browser tab to pick up the new bundle; then try
    Cmd+Shift+F from anywhere, including mid-typing in the capture bar.
project: 2026-04-27-gtd
source_id: null
tags: []
time_minutes: 5
title: command + shift + f to search
updated: 2026-09-16 09:22:20.869198
waiting_on: null
waiting_since: null
working_on: false
---