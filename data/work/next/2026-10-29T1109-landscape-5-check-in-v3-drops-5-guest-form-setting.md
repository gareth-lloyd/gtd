---
area: null
completed_at: null
contexts: []
created: 2026-10-29 11:09:17.451340
defer_until: null
due: null
energy: null
id: 2026-10-29T1109-landscape-5-check-in-v3-drops-5-guest-form-setting
order: null
output: ''
project: 2026-10-21-config-registry
source_id: null
tags: []
time_minutes: null
title: 'Landscape #5: check-in v3 drops 5 guest form settings, v3 migration blockers
  miss them'
updated: 2026-10-29 11:09:17.569347
waiting_on: null
waiting_since: null
working_on: false
---

Protel/Ulyses relation dropdowns, `guest_gender_options`, additional guests full birth name and mother's maiden name. `V3MigrationService.get_compatibility_blockers` checks none. AD-8414 covers one.

Source: `backend/canary/settings_field_guide/LANDSCAPE.md` on `glloyd/settings-field-guide` (commit 9501bfc4f19), finding 5.