---
area: null
completed_at: 2026-08-31 22:30:56.803964
contexts:
- deep
created: 2026-08-31 14:04:10.879963
defer_until: null
due: null
energy: high
id: 2026-08-31T1404-sso-for-staff-app-decide-enterprise-engineer-capac
order: null
output: ''
project: 2026-08-31-ihg
source_id: null
tags: []
time_minutes: 30
title: SSO for Staff App — decide Enterprise engineer capacity/ownership (BWH deadline)
updated: 2026-08-31 22:30:56.803958
waiting_on: null
waiting_since: null
working_on: false
---

Slack thread: https://canarytechnologies.slack.com/archives/C0AN8AQ49UG/p1787935367405959
From Caitlyn Levine, 2026-08-28, tagging me + Andrea.

**Ask:** Can Enterprise free up an engineer for Staff App SSO now, or after IHG deployments are underway next week?

**Context:**
- Staff App cannot go GA without SSO support.
- Minimum scope: globalize the user profile table and the SSO settings table.
- Enterprise owns SSO and has the only team with the domain expertise. Longer-term intent is to shift ownership toward Identity, but the deadline requires prior SSO knowledge.

**Why urgent:** Best Western Convention 10/26 — goal is the BW COO demoing Staff App onstage to all their GMs. BWH properties need a couple of weeks of real usage/testing first to confirm it handles all 1,300 BWH properties. SSO is required for any BWH to go live on Staff App → SSO needed live by ~10/10.

**Thread replies (Connor):**
- Asked whether this was scoped in the Mobile/Staff Ops Linear project: Phase 2 Foundational Services (Guest App / Staff App white label).
- Wants to wait for me to be back next week to discuss ownership/capacity.
- "If needed, we can likely loan an ENT engineer towards this."

**Caitlyn's proposed split:**
1. UI for staff member entering email/username + continue — Mobile
2. Lookup of email/username to find account and check for SSO settings — Mobile
3. That lookup must hit *global* tables, not the regional ones we have today — ENT/Identity
4. If no SSO settings found, show email/pw option — Mobile

cc on thread: Connor, Jordan Sterling, Jason.

**Next:** conversation with Connor on ownership/capacity; decide whether to loan an ENT engineer and who.