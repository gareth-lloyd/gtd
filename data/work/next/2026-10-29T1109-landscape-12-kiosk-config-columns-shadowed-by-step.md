---
area: null
completed_at: null
contexts: []
created: 2026-10-29 11:09:18.248776
defer_until: null
due: null
energy: null
id: 2026-10-29T1109-landscape-12-kiosk-config-columns-shadowed-by-step
order: null
output: ''
project: 2026-10-21-config-registry
source_id: null
tags: []
time_minutes: null
title: 'Landscape #12: kiosk config columns shadowed by step configuration on payment
  v2'
updated: 2026-10-29 11:09:18.361294
waiting_on: null
waiting_since: null
working_on: false
---

`block_kiosk_check_in_for_special_requests`, `skip_payment_for_special_requests`, `skip_payment_for_payment_methods` are in kiosk admin but payment v2 reads the step-configuration twins.

Source: `backend/canary/settings_field_guide/LANDSCAPE.md` on `glloyd/settings-field-guide` (commit 9501bfc4f19), finding 12.