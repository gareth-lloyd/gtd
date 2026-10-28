---
area: null
completed_at: null
contexts:
- deep
created: 2026-10-28 14:52:21.522860
defer_until: null
due: null
energy: high
id: 2026-10-28T1452-ask-ad-whether-enterprise-onboarding-providers-can
order: null
output: ''
project: null
source_id: null
tags: []
time_minutes: 30
title: Ask AD whether Enterprise onboarding providers can reuse TOOL-871's path (migrate_hotel_to_v3
  + move_to_catalog + catalog writes)
updated: 2026-10-28 16:23:22.693678
waiting_on: null
waiting_since: null
working_on: true
---

From: check-in v3 rollout research, 2026-10-28 (#ihg thread, #best-western thread, TOOL 'Automate Check-in V3 Onboarding' design)
Gareth's 2026-08-06 ask to Dana: AD owns a check-in config service; onboarding passes intent, never sets fields.
Internal Tools design (Sam Kariu, REVIEW ME!) does this for DEFAULT onboarding but puts Wyndham MSA, BW MSA, IHG Pilot, IHG GMS Core out of scope.
AD-10463 (Done 10-23) added a single V3MigrationService entry point. Not yet verified in code whether Enterprise providers can call it.
Restart the thread with Dana + Leandro after the Andrea sync.