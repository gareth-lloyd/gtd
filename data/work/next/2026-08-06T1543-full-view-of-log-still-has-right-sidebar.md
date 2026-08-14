---
area: null
completed_at: null
contexts: []
created: 2026-08-06 15:43:05.668557
defer_until: null
due: null
energy: low
id: 2026-08-06T1543-full-view-of-log-still-has-right-sidebar
order: null
output: |
  ## Agent run 2026-08-14T07:00

  Done — and it did NOT need extensive surgery (3 lines of TSX + a CSS tweak),
  so I didn't stop for approval.

  **Cause**: `ContentArea` in `frontend/src/App.tsx` unconditionally renders
  `<DetailPanel>` next to `<main>`, and `.detail-panel` is `flex: 0 0 50%`.
  Every route — including the agent log view — therefore loses half the
  content column to the right pane. On the log route it was pure waste: the
  pane just showed "Select an item to edit".

  **Fix**
  - `frontend/src/App.tsx` — `ContentArea` now checks
    `useMatch(":env/items/:itemId/agent")` and skips `<DetailPanel>` on that
    route only. `main` is `flex: 1`, so it expands to the full column.
  - `frontend/src/styles.css` — `.agent-log-view` max-width raised 60rem →
    80rem (~1280px), plus `width: 100%; margin: 0 auto` so it centres in the
    wider column instead of hugging the nav.

  Net result: log now spans everything right of the left nav, capped at 80rem.

  **Tests** (red/green): added two cases to `AgentLogView.test.tsx` —
  detail panel absent on `/work/items/:id/agent`, still present on
  `/work/next` (guards against accidentally killing it everywhere). First
  failed, then passed. Full suite green: 148 tests, 13 files. `npm run
  typecheck`, `npm run lint`, `npm run build` all clean; `dist/` rebuilt.

  **Not committed** — left in the working tree so you can eyeball the width
  in the browser first. 80rem was my judgement call; say the word if you want
  it wider/narrower or left-aligned rather than centred.

  Files touched: `frontend/src/App.tsx`, `frontend/src/styles.css`,
  `frontend/src/AgentLogView.test.tsx` (+ rebuilt `frontend/dist/`).

project: 2026-04-27-gtd
source_id: null
tags: []
time_minutes: 5
title: Full view of log still has right sidebar
updated: 2026-08-14 07:00:12.000000
waiting_on: null
waiting_since: null
working_on: false
---

I would like it to take up the whole screen apart from left sidebar, up to a useful max width. 

If this requires extensive surgery on the frontend structure, it may not be worthwhile. pause for my approval