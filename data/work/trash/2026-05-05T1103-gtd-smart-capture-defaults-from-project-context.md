---
area: engineering
contexts:
- deep
created: 2026-05-05 11:03:00
defer_until: null
due: null
energy: medium
id: 2026-05-05T1103-gtd-smart-capture-defaults-from-project-context
order: null
output: ''
project: 2026-04-27-gtd
source_id: null
tags:
- gtd-meta
- backend
- frontend
time_minutes: 120
title: 'GTD: smart-capture defaults from project context'
updated: 2026-05-08 15:16:22.770212
waiting_on: null
waiting_since: null
working_on: false
---

**Problem.** Many active items have `area: null` because capture
defaults are too thin. When a project is selected, area can be
inferred from the project's metadata, and the dominant context
across the project's recent items is a strong default.

**Approach.**
- **Backend.** Extend `GtdService.capture()` with
  `inherit_from_project: bool = True`. When True and `project` is
  known after the AI capture path resolves it (or a project is passed
  explicitly):
  - If `area` is unspecified, copy from project's `area`.
  - If `contexts` is empty, take the modal context across the
    project's last 5 items in `next/`. Skip if tied or empty.
- **AI capture.** In `gtd_core/ai.py`, after fuzzy project match,
  apply the same inheritance before returning to the API.
- **Frontend.** `CaptureBar.tsx` — when user picks a project,
  fetch project metadata (or use cached) and pre-fill area + contexts
  in the form (still editable).
- Don't touch existing items; only newly captured ones get
  defaults.

**Verification.**
- Backend tests covering precedence (explicit > inherited > none).
- E2E spec: capture with a project selected, assert area populated
  on the resulting item.

**Size.** M (~2h)