---
area: null
completed_at: null
contexts: []
created: 2026-10-29 11:09:17.339219
defer_until: null
due: null
energy: null
id: 2026-10-29T1109-landscape-4-two-blocked-card-lists-auth-vs-check-i
order: null
output: ''
project: 2026-10-21-config-registry
source_id: null
tags: []
time_minutes: null
title: 'Landscape #4: two blocked-card lists (auth vs check-in), kiosk reads neither'
updated: 2026-10-29 11:09:17.450846
waiting_on: null
waiting_since: null
working_on: false
---

`hotel.blocked_card_types`/`blocked_credit_card_networks` vs `check_in_configuration.blocked_card_types`/`blocked_card_networks`; kiosk and front desk read none. CUSTOPS-4301, SDM-4169.

Source: `backend/canary/settings_field_guide/LANDSCAPE.md` on `glloyd/settings-field-guide` (commit 9501bfc4f19), finding 4.