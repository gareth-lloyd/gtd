---
area: null
completed_at: null
contexts:
- react
created: 2026-08-11 08:15:10.129996
defer_until: null
due: null
energy: medium
id: 2026-08-11T0815-reply-to-leandro-on-ad-8170-ad-8172-check-in-confi
order: null
output: ''
project: null
source_id: https://linear.app/canary-technologies/issue/AD-8172/permissions-re-gate-check-in-configuration-endpoints-for-adminland
tags:
- morning-gtd
- linear
time_minutes: 20
title: Reply to Leandro on AD-8170 / AD-8172 check-in configuration permissions
updated: 2026-08-11 08:15:10.196696
waiting_on: null
waiting_since: null
working_on: false
---

He answered both review points: gatekeeper changed to HotelUserGatekeeper(hotel_permissions=...), and he found that create_admin_roles_for_products builds the Admin role from the whole PERMISSIONS_BY_PRODUCT[CHECK_IN] set without filtering by strength — so staff-only perms leak to admins. AD-8171 also needs a call on backfilling existing users.
https://linear.app/canary-technologies/issue/AD-8172/permissions-re-gate-check-in-configuration-endpoints-for-adminland
https://linear.app/canary-technologies/issue/AD-8170/permissions-add-canary-staff-only-check-in-configuration-permissions