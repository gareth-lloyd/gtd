---
area: null
completed_at: null
contexts: []
created: 2026-10-29 11:09:17.000483
defer_until: null
due: null
energy: null
id: 2026-10-29T1109-landscape-1-ihg-australia-id-purge-sets-the-dead-f
order: null
output: ''
project: 2026-10-21-config-registry
source_id: null
tags: []
time_minutes: null
title: 'Landscape #1: IHG Australia ID purge sets the dead flag, kiosk ignores id_purge_strategy'
updated: 2026-10-29 11:09:17.118542
waiting_on: null
waiting_since: null
working_on: false
---

IHG Australia brand tree and onboarding set `purge_id_on_reservation_status_change` (dead) and never `id_purge_strategy`, so ID images stay until departure + 181 days. Kiosk ignores `id_purge_strategy` in the 7 IHG countries pinned to immediate purge. APAC-94 (open) wrongly says the flag is only in the model and a migration.

Source: `backend/canary/settings_field_guide/LANDSCAPE.md` on `glloyd/settings-field-guide` (commit 9501bfc4f19), finding 1.