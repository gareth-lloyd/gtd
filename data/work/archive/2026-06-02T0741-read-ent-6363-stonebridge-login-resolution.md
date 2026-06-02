---
area: null
contexts:
- consume
created: 2026-06-02 07:41:51.450345
defer_until: null
due: null
energy: low
id: 2026-06-02T0741-read-ent-6363-stonebridge-login-resolution
order: null
output: |
  ## Agent run 2026-06-02T14:25:00

  Read ENT-6363 (Deployed/resolved, owner: Tincho). Skim of the fix pattern:

  Symptom: Rachel Smoller hit errors impersonating Sharad Chand (schand@sbcos.com,
  user id 3939419) on some Stonebridge tipping properties. Came out of ENT-6359
  (property rename) but was unrelated to the rename.

  Root cause: permissions gap, not a code bug. Sharad is a Stonebridge Portfolio
  Administrator + full Property Manager on 54 props, but on 40 OLDER props he sat on
  a legacy per-hotel "Staff" custom role that hides tipping_view_activity_and_export_data
  (Tips card) and tipping_has_disbursement_access (Disbursement tab -> 403, confirmed
  in Datadog).

  Fix pattern: one-off INTERACTIVE production shell_plus script (us-west-2, rw, run by
  a human) -- NOT a code change/migration. For each of Sharad's custom-role grants:
    1. RoleService.grant_default_role_to_user(user, DefaultPropertyRole.PROPERTY_MANAGER,
       hotel_id, granted_by=acting)   # idempotent
    2. RoleService.remove_property_role_grants_from_user(user, roles=[staff_role], hotel_id)
  Guards: assert user.email matches; refuse if any custom role != "Staff"; verify
  post-state (0 remaining custom grants, 94 property_manager grants). Touched only
  Sharad's grants; Rachel approved before run.

  Reusable takeaway: when a portfolio admin gets tipping view / disbursement 403s,
  look for legacy per-hotel "Staff" custom roles -> promote to PROPERTY_MANAGER via
  RoleService, guarded by an assert that the only custom role converted is "Staff".

  No action needed from me; ticket is Deployed.
project: null
source_id: https://linear.app/canary-technologies/issue/ENT-6363/error-logging-into-stonebridge-portfolio-properties
tags:
- morning-gtd
- linear
- from-awareness
time_minutes: 5
title: 'Read ENT-6363: Stonebridge login resolution'
updated: 2026-06-02 14:25:25.217592
waiting_on: null
waiting_since: null
working_on: false
---

tincho promoted Sharad Chand to Property Manager on 40 legacy-Staff props; deployed/resolved. Skim for the fix pattern.
https://linear.app/canary-technologies/issue/ENT-6363/error-logging-into-stonebridge-portfolio-properties