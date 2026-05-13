---
area: null
contexts: []
created: 2026-05-12 17:24:14.930329
defer_until: null
due: null
energy: low
id: 2026-05-12T1724-ensure-is-staff-is-covered-in-core-knowledge-base
order: -10
output: "## Agent run 2026-05-12T21:30Z\n\n### How `is_staff` gets set from Google
  groups\n\nSet in `backend/canary/canary_staff/services/canary_staff_service.py:1281`:\n```python\ndjango_user.is_staff
  = any(group[\"email\"] in GROUPS_WITH_STAFF_ACCESS for group in user_groups)\n```\n\n`GROUPS_WITH_STAFF_ACCESS`
  (lines 29-43 of same file) currently lists 13 groups:\nCSA_INTEGRATIONS, CUSTOMER_SUCCESS,
  ENGINEERING, EPD, IMPLEMENTATION,\nINTEGRATIONS, LEADERSHIP, OPERATIONS, SALES_CANARY_ADMINS,
  SALES_ENGINEERING,\nSUPPORT, SHOP_MANAGERS, SUPPORT_LEADS_AND_L2S.\n\nTrigger points
  (both call `CanaryStaffService.get_or_create_user_from_google_user`):\n- Google
  OAuth login — `canary_staff/views/oauth_views.py:87`\n- Cloudflare Zero Trust middleware
  — `canary/middleware/cloudflare_zero_trust_auth_middleware.py:29`\n- `cron_sync_django_google_users`
  management command iterates all `team@canarytechnologies.com` members and runs the
  shared `GoogleUserSyncService` path (which the canary-specific service wraps)\n\n`is_superuser`
  is set the same way via `GROUPS_WITH_SUPERUSER_ACCESS` (prod: ENGINEERING, LEADERSHIP)
  and `GROUPS_WITH_STAGING_SUPERUSER_ACCESS` (adds EPD on staging).\n\n### Is it covered
  in the Notion article?\n\nArticle: \"Managing Google Groups for Canary Internal
  Permissions\"\n(https://www.notion.so/canarytechnologies/34f8146861518167b5bcc97d7a6cde57)\n\nPartial
  coverage — `is_staff` is mentioned in two procedural steps but never\nexplained
  on its own terms:\n\n- **Create a New Group → Step 5**: \"add the email to `GROUPS_WITH_STAFF_ACCESS`\n
  \ for `is_staff=True`, and `GROUPS_WITH_SUPERUSER_ACCESS` /\n  `GROUPS_WITH_STAGING_SUPERUSER_ACCESS`
  for `is_superuser=True`.\"\n- **Delete a Group → Step 2**: mentions removing from
  `GROUPS_WITH_STAFF_ACCESS`.\n\nGaps worth filling:\n1. No explanation of what `is_staff`
  actually grants (Django admin login —\n   i.e. the ability to load `/canary-admin`
  at all, separate from the\n   model-level grants assembled via `GoogleUserPermissionSet`).\n2.
  The Overview frames \"Django permission set\" as the single output of group\n   membership,
  glossing over that `is_staff` / `is_superuser` are independent\n   top-level `User`
  booleans recomputed on the same login path.\n3. Existing list of `GROUPS_WITH_STAFF_ACCESS`
  groups isn't enumerated, so a\n   reader can't tell at a glance which roles get
  admin login today without\n   opening the code.\n4. No mention that `is_staff` is
  also re-evaluated every login — so removing\n   a user from a staff-granting group
  revokes admin access at next login (and\n   eventually via the cron sync), not instantly.\n\n###
  Recommendation\nAdd a short \"is_staff and is_superuser\" subsection under Overview,
  listing\nthe current member groups and clarifying what each flag unlocks (admin
  login\nvs. all-permissions bypass) and when revocation takes effect. Keep the\nexisting
  Step 5 / Step 2 procedural references — they're fine — but lift the\nconceptual
  explanation up to Overview so it's not buried in optional steps.\n"
project: null
source_id: null
tags: []
time_minutes: 5
title: ensure "is_staff" is covered in core knowledge base
updated: 2026-05-12 21:10:18.600210
waiting_on: null
waiting_since: null
working_on: false
---

How does is_staff get set on users according to Google groups? 

Is that covered in this article? https://www.notion.so/canarytechnologies/Managing-Google-Groups-for-Canary-Internal-Permissions-34f8146861518167b5bcc97d7a6cde57?source=copy_link