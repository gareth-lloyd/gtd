---
area: null
completed_at: null
contexts: []
created: 2026-09-24 10:08:02.569987
defer_until: null
due: null
energy: low
id: 2026-09-24T1008-show-time-as-well-as-date-that-itme-was-created
order: null
output: |
  ## Agent run 2026-10-01T10:30:04

  Done and live: the created stamp now shows the time as well as the date,
  e.g. `created 2026-09-24 10:08` (24h, local time, no seconds).

  Where it changed:
  - Detail pane footer (`frontend/src/DetailPanel.tsx`): visible text is now
    `created YYYY-MM-DD HH:MM`.
  - Agent-log full view (`frontend/src/AgentLogView.tsx`): the hover tooltip
    on the "updated …" line now reads `created YYYY-MM-DD HH:MM`.

  How: new `fmtDateTime` helper in `frontend/src/format.ts` next to
  `fmtDate`. Tests written first in `format.test.ts`, `DetailPanel.test.tsx`
  and `AgentLogView.test.tsx`.

  Verification: frontend 170 tests pass, backend 664 pass, `./scripts/lint.sh`
  all clear. Frontend rebuilt and service restarted (`make rebuild-frontend`);
  localhost:8765 responds 200. Not checked by eye in a browser.

  Committed to main as de202b40 ("show created time as well as date on
  items"), code files only. Not pushed. Your uncommitted data changes
  (inbox triage) were left alone.

  Left as is — say if you want either changed:
  - `updated` is still date-only (detail pane tooltip, agent-log visible
    text). One-line swap to `fmtDateTime` in each place.
  - Collapsed item cards in the lists show no created stamp at all, so
    nothing changed there.
project: 2026-04-27-gtd
source_id: null
tags: []
time_minutes: 5
title: Show time as well as date that itme was created
updated: 2026-10-01 10:30:04.000000
waiting_on: null
waiting_since: null
working_on: false
---