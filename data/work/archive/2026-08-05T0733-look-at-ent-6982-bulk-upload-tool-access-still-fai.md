---
area: null
completed_at: 2026-08-05 13:51:38.573424
contexts:
- react
created: 2026-08-05 07:33:51.620803
defer_until: null
due: null
energy: low
id: 2026-08-05T0733-look-at-ent-6982-bulk-upload-tool-access-still-fai
order: null
output: |
  ## Agent run 2026-08-05T14:05:00Z

  Diagnosed from code + Groundcover prod logs (read-only; nothing posted anywhere).

  **TL;DR: it's a login-timing issue, not a group-membership problem. Both users likely
  just need to log out and back in (via Google) in the failing region. No code or DB
  change is required to unblock them.**

  ### How access to the tool actually works
  - The bulk-upload tool is the Django admin page `/canary-admin/hotel_staff/userdataimport/`
    (built in ENT-5114). Access needs `is_staff` + `hotel_staff.*` model permissions.
  - Both are recomputed from the user's **Google** group memberships ONLY during a Google
    OAuth login, per region (US/EU/AP are separate DBs and separate sessions) —
    `CanaryStaffService.get_or_create_user_from_google_user`
    (backend/canary/canary_staff/services/canary_staff_service.py:1298), called from
    `oauth_views.py:87`. The nightly `cron_sync_django_google_users` does NOT assign
    permissions (it calls the shared sync which only handles users/groups).
  - Permissions for `user-data-import-admins@canarytechnologies.com`
    (GoogleGroups.USER_DATA_IMPORT_ADMINS) are added directly to `user_permissions` —
    they do NOT depend on a Django `Group` row existing.

  ### Timeline from prod logs (all Aug 4, UTC)
  - 16:47 — Ana's last **EU** login: Google returned only `team@` for her, NOT
    `user-data-import-admins@` → IT's add was not yet visible to the Google API → her EU
    user got no hotel_staff perms. This is why EU still fails for her.
  - 17:49–17:50 — membership visible: Ari's EU + AP logins and Ana's AP login all show
    `user-data-import-admins@` being returned → perms granted in those regions.
  - 21:47 — AC comments on ENT-6982 that Ana (EU) and Ari (US) still fail.
  - 22:45 — Ari re-logged into **US** (heading to /kiosk-agents), membership now visible
    → her US perms should have been granted then, i.e. AFTER the complaint was written.
    She hasn't retried the tool in US since.

  ### Recommended reply to the ticket (draft — NOT posted, needs your approval/wording)
  Ask Ana to fully log out of eu.canarytechnologies.com and log back in with Google, and
  Ari to retry on www.canarytechnologies.com (log out/in via Google if it still fails),
  then open /canary-admin/hotel_staff/userdataimport/. Group changes only take effect at
  the next Google login in each region.

  ### Secondary findings (the thing your Linear comment suspected — real, but not the blocker)
  - The Django `Group` rows named after ~13 GoogleGroups emails (incl.
    `user-data-import-admins@`, `team@`, `implementation@`, `portfolio-admins@`,
    `onboarding-admins@`...) are missing in ALL prod regions (US/EU/AP). This only
    affects `django_user.groups` mirroring, not permissions, but it fires
    `sync_user_groups.google_group_not_in_django` ~19k times/day across clusters.
    Optional cleanup: create the Group rows per region (or auto-create in
    `GoogleUserSyncService._sync_user_groups`, shared/auth/google_user_sync.py:179).
  - Worth knowing for future requests: `USER_DATA_IMPORT_ADMINS` is not in
    `GROUPS_WITH_STAFF_ACCESS` (canary_staff_service.py:29), so the group alone never
    grants admin access — requesters must already be staff via another group (CS/CSA
    etc.), which these users are.

  Ticket: https://linear.app/canary-technologies/issue/ENT-6982/request-access-to-bulk-upload-tool
  Parent/tool: https://linear.app/canary-technologies/issue/ENT-5114/bulk-upload-of-users
project: null
source_id: https://linear.app/canary-technologies/issue/ENT-6982/request-access-to-bulk-upload-tool
tags:
- morning-gtd
- linear
- from-awareness
time_minutes: 10
title: 'Look at ENT-6982: bulk-upload tool access still failing for Ana (EU) and Ari
  (US)'
updated: 2026-08-05 13:51:38.573403
waiting_on: null
waiting_since: null
working_on: false
---

IT added the group members but access errors persist in both regions; you're named as the Google-group owner (ref ENT-5114).
https://linear.app/canary-technologies/issue/ENT-6982/request-access-to-bulk-upload-tool