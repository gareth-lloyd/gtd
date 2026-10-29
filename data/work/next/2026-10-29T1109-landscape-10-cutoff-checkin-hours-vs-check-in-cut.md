---
area: null
completed_at: null
contexts: []
created: 2026-10-29 11:09:18.019546
defer_until: null
due: null
energy: null
id: 2026-10-29T1109-landscape-10-cutoff-checkin-hours-vs-check-in-cut
order: null
output: ''
project: 2026-10-21-config-registry
source_id: null
tags: []
time_minutes: null
title: 'Landscape #10: cutoff_checkin_hours vs check_in_cut_off_hour confusion'
updated: 2026-10-29 11:09:18.132768
waiting_on: null
waiting_since: null
working_on: false
---

Near-identical names, different meanings (assumed IN_HOUSE/broadcast/journey timing vs reservation lookup); neither help text names the other. MSG-5761.

Source: `backend/canary/settings_field_guide/LANDSCAPE.md` on `glloyd/settings-field-guide` (commit 9501bfc4f19), finding 10.