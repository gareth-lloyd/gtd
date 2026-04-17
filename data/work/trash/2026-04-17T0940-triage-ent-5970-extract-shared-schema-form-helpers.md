---
area: null
contexts:
- triage
created: 2026-04-17 09:40:12.747476
defer_until: null
due: null
energy: low
id: 2026-04-17T0940-triage-ent-5970-extract-shared-schema-form-helpers
order: null
project: null
tags:
- morning-gtd
- linear
time_minutes: 10
title: 'Triage ENT-5970: Extract shared schema-form helpers (rrogers proposal)'
updated: 2026-04-17 07:11:48.060914
waiting_on: null
waiting_since: null
---

Refactor to break check_in ↔ guest_experience circular import by moving apply_pms_guest_count_constraints and LoyaltyInfo helpers to a new check_in/services/schema_form.py. No behavior change. https://linear.app/canary-technologies/issue/ENT-5970/extract-shared-schema-form-helpers-to-break-check-in-guest-experience