---
area: null
completed_at: null
contexts: []
created: 2026-10-29 11:09:17.228782
defer_until: null
due: null
energy: null
id: 2026-10-29T1109-landscape-3-ai-booking-toggles-ignored-on-agentic
order: null
output: ''
project: 2026-10-21-config-registry
source_id: null
tags: []
time_minutes: null
title: 'Landscape #3: AI booking toggles ignored on agentic SMS and webchat; KB-only
  empties booking'
updated: 2026-10-29 11:09:17.338767
waiting_on: null
waiting_since: null
working_on: false
---

Agentic SMS/WhatsApp ignores `booking_link_enabled`, the webchat column is unread, and KB-only confidence mode returns an empty BookingConfig while the dashboard shows toggles on. MSG-5634, MSG-5181, MSG-5632, MSG-6645.

Source: `backend/canary/settings_field_guide/LANDSCAPE.md` on `glloyd/settings-field-guide` (commit 9501bfc4f19), finding 3.