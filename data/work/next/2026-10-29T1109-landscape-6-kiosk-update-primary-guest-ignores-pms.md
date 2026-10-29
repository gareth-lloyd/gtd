---
area: null
completed_at: null
contexts: []
created: 2026-10-29 11:09:17.569769
defer_until: null
due: null
energy: null
id: 2026-10-29T1109-landscape-6-kiosk-update-primary-guest-ignores-pms
order: null
output: ''
project: 2026-10-21-config-registry
source_id: null
tags: []
time_minutes: null
title: 'Landscape #6: kiosk UPDATE_PRIMARY_GUEST ignores PMS auto-post flags'
updated: 2026-10-29 11:09:17.679800
waiting_on: null
waiting_since: null
working_on: false
---

Kiosk guest-profile push ignores `integration_auto_post_to_pms` and the phone/DOB/nationality/marketing sub-flags (honours passport only). Web and v3 honour all.

Source: `backend/canary/settings_field_guide/LANDSCAPE.md` on `glloyd/settings-field-guide` (commit 9501bfc4f19), finding 6.