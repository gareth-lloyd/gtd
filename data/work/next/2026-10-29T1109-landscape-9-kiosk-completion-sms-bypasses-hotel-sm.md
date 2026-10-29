---
area: null
completed_at: null
contexts: []
created: 2026-10-29 11:09:17.911132
defer_until: null
due: null
energy: null
id: 2026-10-29T1109-landscape-9-kiosk-completion-sms-bypasses-hotel-sm
order: null
output: ''
project: 2026-10-21-config-registry
source_id: null
tags: []
time_minutes: null
title: 'Landscape #9: kiosk completion SMS bypasses hotel SMS switches'
updated: 2026-10-29 11:09:18.019132
waiting_on: null
waiting_since: null
working_on: false
---

`send_sms_on_completion` sends via Twilio directly, ignoring `has_check_in_messages`, `disable_sms_channel`, `allow_send_text`.

Source: `backend/canary/settings_field_guide/LANDSCAPE.md` on `glloyd/settings-field-guide` (commit 9501bfc4f19), finding 9.