---
area: null
completed_at: null
contexts: []
created: 2026-10-29 11:09:18.133286
defer_until: null
due: null
energy: null
id: 2026-10-29T1109-landscape-11-dead-webchat-ai-switches-auditor-disa
order: null
output: ''
project: 2026-10-21-config-registry
source_id: null
tags: []
time_minutes: null
title: 'Landscape #11: dead webchat AI switches; auditor_disabled dead on agentic
  threads'
updated: 2026-10-29 11:09:18.248321
waiting_on: null
waiting_since: null
working_on: false
---

Webchat `has_ai`, `is_ai_responding_enabled`, `has_managed_ai_answers`, `is_auditor_disabled` have no reader but are in admin; chat_configuration governs. Agentic `auditor_disabled` context field has no reader.

Source: `backend/canary/settings_field_guide/LANDSCAPE.md` on `glloyd/settings-field-guide` (commit 9501bfc4f19), finding 11.