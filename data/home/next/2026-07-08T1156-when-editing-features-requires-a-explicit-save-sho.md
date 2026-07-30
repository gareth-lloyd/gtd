---
area: null
contexts: []
created: 2026-07-08 11:56:56.047862
defer_until: null
due: null
energy: low
id: 2026-07-08T1156-when-editing-features-requires-a-explicit-save-sho
order: 9
output: |
  ## Agent run 2026-07-29T14:43

  Captured as **GAP-083** in the villacollective design todo tier (files created, uncommitted on main):

  - Ticket: `django_res_design/todo/gap-083-features-dirty-flag-navigation-guard.md`
  - Index row added: `django_res_design/todo/INDEX.md` (after GAP-082)

  Grounded against the codebase before filing:
  - `frontend/src/features/properties/tabs/FeaturesTab.tsx` already computes an order-sensitive `isDirty` (~L153) — but the ONLY dirty signal is the Save/Reset buttons enabling. No visible "unsaved changes" indicator.
  - Tabs are route-based `NavLink`s in `PropertyDetailLayout.tsx`, so switching tab (or any navigation) unmounts FeaturesTab and silently discards edits. `grep useBlocker|beforeunload` over frontend/src: zero hits — no navigation-guard pattern exists anywhere yet.
  - App uses `createBrowserRouter` (React Router v7), so `useBlocker` is available for the in-app guard; `ConfirmDialog` exists for the discard prompt.

  Ticket scope: visible dirty flag + `useBlocker` confirm-discard dialog + `beforeunload` for hard exits, built as a reusable `useUnsavedChangesGuard` hook piloted on FeaturesTab (same hazard exists on SettingsTab/DescriptionsSection — roll-out is explicit follow-up, not in scope).

  Not done (left to you): commit the two doc files (suggest `docs(design): GAP-083 capture — features dirty flag + nav guard`); INDEX scoreboard count not bumped (already drifting — GAP-082's row still points at the todo/ path though its file moved to done/).
project: 2026-05-25-villa-collective
source_id: null
tags: []
time_minutes: 5
title: 'Capture as gap todo: When editing property features, requires a explicit save.
  Should be flagged that data has changed, and no navigate without explicit reject
  changes'
updated: 2026-07-29 14:43:12.000000
waiting_on: null
waiting_since: null
working_on: false
---