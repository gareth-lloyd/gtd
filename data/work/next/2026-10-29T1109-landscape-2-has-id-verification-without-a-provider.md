---
area: null
completed_at: null
contexts: []
created: 2026-10-29 11:09:17.119017
defer_until: null
due: null
energy: null
id: 2026-10-29T1109-landscape-2-has-id-verification-without-a-provider
order: null
output: ''
project: 2026-10-21-config-registry
source_id: null
tags: []
time_minutes: null
title: 'Landscape #2: has_id_verification without a provider gives ServerError on
  add-products path'
updated: 2026-10-29 11:09:17.228300
waiting_on: null
waiting_since: null
working_on: false
---

Adding ID Verify to an existing hotel sets `has_id_verification` but not `id_verification_provider`; the guest ID step raises ServerError. Same as SDM-3520. Candidate consistency rule.

Source: `backend/canary/settings_field_guide/LANDSCAPE.md` on `glloyd/settings-field-guide` (commit 9501bfc4f19), finding 2.