---
area: null
completed_at: 2026-08-12 11:47:07.286648
contexts:
- react
created: 2026-08-10 11:40:43.106123
defer_until: null
due: 2026-08-10
energy: medium
id: 2026-08-10T1140-review-ad-8170-8171-8172-permissions-scoping-for-l
order: null
output: |
  ## Agent run 2026-08-10T14:07:10Z

  Reviewed all three tickets against the code on `master`. Nothing was posted to Linear or
  Slack — this is a local review for you to send (or edit) yourself.

  Tickets:
  - AD-8170 https://linear.app/canary-technologies/issue/AD-8170/permissions-add-canary-staff-only-check-in-configuration-permissions (4 pts)
  - AD-8171 https://linear.app/canary-technologies/issue/AD-8171/permissions-grant-the-advanced-configuration-role-to-training-users (1 pt)
  - AD-8172 https://linear.app/canary-technologies/issue/AD-8172/permissions-re-gate-check-in-configuration-endpoints-for-adminland (2 pts)
  - Thread: https://canarytechnologies.slack.com/archives/C0BKDAG8FMY/p1786111203037999?thread_ts=1785851167.958619&cid=C0BKDAG8FMY

  Overall: the shape is right and the tickets are unusually well-specified. Three things are
  wrong or missing in a way that would bite during implementation, plus one production-impact
  hazard the tickets don't mention at all.

  ### 1. BLOCKER — filing the permission under product CHECK_IN will silently empty `get_admins()`

  This is the one I'd fix before anyone picks up AD-8170.

  `HotelService.get_admins()` (`backend/canary/hotels/services/hotel.py:334-372`) builds
  `admin_permissions_for_products` as `PERMISSIONS_NOT_BY_PRODUCT ∩ ADMIN_EQUIVALENT` plus,
  for every active product, `PERMISSIONS_BY_PRODUCT[product] ∩ ADMIN_EQUIVALENT`, then calls
  `PermissionService.get_all_users_with_permissions_for_hotel(...)`. That selector uses
  `user_permissions.issuperset(permissions)` (`permissions/services/permission.py:328-332`) —
  **ALL semantics, not ANY**.

  Today `PERMISSIONS_BY_PRODUCT[CHECK_IN] ∩ ADMIN_EQUIVALENT` = {`CHECK_IN_HAS_SETTINGS_ACCESS`,
  `CHECK_IN_HAS_REGISTRATION_CARD_SETTINGS_ACCESS`}, and PROPERTY_MANAGER holds both, so it works.

  AD-8170 instructs (correctly, for its own goal) *not* to add the new permissions to
  PROPERTY_MANAGER. If they are also filed under product CHECK_IN at strength ADMIN, then on
  every check-in hotel `get_admins()` starts requiring a permission no property manager holds
  and returns **zero admins**. Consumers that break:

  - `credit_card/management/commands/cron_send_admin_cc_digest.py:153`
  - `hotels/services/user.py:228`
  - `hotels/twilio.py:75`
  - `hotels/models/hotel.py:1942` (`Hotel.admins`)
  - `hotels/views/api/user/user.py:188`
  - `tips/services/tip.py:1272`, `tips/management/commands/cron_send_departmental_tip_report_emails.py:148`
  - `incidents/management/commands/cron_send_reservation_sync_alerts.py:130`
  - `contracts/services/contract_notification.py:1128`, `authorization/services/authorization.py:2444`
    (these two pass `limit_to_products`, so they're safe)

  Note this fails *silently* — no error, admin emails just stop.

  Safe filing, given the constraints:
  - **Strength**: `STAFF` or `POWER_USER`, **not** `ADMIN`. Keeping them out of
    `ADMIN_EQUIVALENT_PERMISSIONS` also keeps them out of `has_adminland_access_for_hotel`
    (`hotels/services/hotel.py:375-380`), which is ANY-semantics — so an advanced-config
    permission alone will not open adminland. That's fine for training users and SAG support
    users because they also hold PROPERTY_MANAGER, but it's worth stating explicitly in the
    ticket so nobody expects the permission to be self-sufficient.
  - **Product**: `PERMISSIONS_NOT_BY_PRODUCT`, not `PERMISSIONS_BY_PRODUCT[CHECK_IN]`.
    `ActivationService.create_admin_roles_for_products` (`permissions/services/activation.py:410`)
    uses the **entire** `PERMISSIONS_BY_PRODUCT[product]` set with no strength intersection, so
    filing under CHECK_IN leaks into the auto-created "Check In Admin" role regardless of strength.
    `create_roles_for_new_product` (`activation.py:504-548`) leaks at each of STAFF, POWER_USER
    and ADMIN too.

  AD-8170's AC #2 currently says *"Filing them under strength ADMIN together with product CHECK_IN
  would auto-grant them to hotel admins on activation"*. That's true but too narrow — any strength
  under product CHECK_IN leaks. Worth widening the AC and the guard test to "no strength × CHECK_IN
  combination", and adding an AC that `get_admins()` returns the same users before and after.

  ### 2. AD-8172 names the wrong permission mechanism

  The ticket says *"Declare `__permissions__` per endpoint"*. `__permissions__` is the **legacy v1**
  `RequestSchema` idiom (see `permissions/views/list_create_roles.py:52`). `check_in_configuration.py`
  is Request Framework **v2** — permissions there are a constructor kwarg on the class-level
  gatekeeper:

      gatekeeper = HotelUserGatekeeper(
          hotel_permissions=HotelPermissions(hotel_all=[Permission.CHECK_IN_HAS_SETTINGS_ACCESS]),
      )

  (fields are `hotel_all` / `hotel_any` — `canary/access_control/permissions.py:12-27`; canonical
  example at `task_management/views/departments.py:46-49`.)

  The consequence matters: **the gatekeeper is class-level, so it cannot vary per HTTP method.**
  AD-8172 wants "hotel-facing reads on `CHECK_IN_HAS_SETTINGS_ACCESS`, staff-only buckets on
  `CHECK_IN_HAS_ADVANCED_CONFIGURATION_ACCESS`" — GET and PATCH live on the same
  `CheckInConfigurationBucketView`, so that can't be expressed by the gatekeeper alone. Options:
  set the gatekeeper to the loosest permission and do an explicit in-handler check for the stricter
  one, or split the view classes. Either way it should be decided in the ticket, not discovered
  mid-PR. (`task_management/views/departments.py:51` carries a `NOTE:` about exactly this
  limitation.)

  Also needed and not mentioned: the hotel currently arrives as a **query param**
  (`CheckInConfigurationQueryParams.hotel_slug`) and the URLs have no hotel segment
  (`guest_experience/urls/configuration_urls.py`). Re-gating means moving to
  `Annotated[Hotel, HotelResource(authorize=AuthorizeHotel(), data_key="hotel_slug")]` in
  `path_params` **and changing the URL patterns** — which breaks the existing manage-app frontend
  callers. AD-8173 (the UI move) is listed as blocked by 8172, so the sequencing works, but the
  URL change should be called out as an explicit deliverable.

  ### 3. The field-level gating mechanism — Leandro's original question — is still unspecified

  This is the part the tickets are thinnest on, and it's the thing he actually asked about.

  The existing axis is `ConfigurationBucket.CS_EDITABLE_FIELDS`
  (`guest_experience/configuration_library/buckets/base.py:36`), surfaced as `editable` by
  `serialize_bucket` → `_serialize_field` (`configuration_library/serialization.py:8-17`). But that
  axis means *"CS may edit this"* in a world where the whole surface is already CS-only. Once the
  surface is hotel-facing, the needed axis is different: *"who may see/edit this — hotel or Canary
  staff"*. `CS_EDITABLE_FIELDS` cannot be reused as-is.

  Concretely missing from AD-8172:
  - a declaration for the new axis on the bucket class (e.g. `ADVANCED_FIELDS: frozenset[str]`,
    or a `FIELD_PERMISSIONS: dict[str, Permission]` if you want to keep the granular-capability
    idiom you described in the thread);
  - `serialize_bucket` / `_serialize_field` currently take **no user or permission context** at all
    — that signature change ripples through `CheckInConfigurationView`,
    `CheckInConfigurationBucketView`, and the tests;
  - the write path: `CheckInConfigurationWriteService.update_id_configuration`
    (`configuration_library/service.py:~100`) has no field-permission check — a caller without the
    advanced permission must be rejected on gated keys, not silently allowed.

  With all that, **2 points for AD-8172 looks light** — I'd expect 3–5. Splitting "swap the
  gatekeeper + move the hotel to a path param" from "add field-level permission gating" into two
  tickets would probably be cleaner.

  Related: AD-8170 adds `CHECK_IN_CAN_MANAGE_PMS_REGISTRATION_CARD_MAPPING`, but **no ticket in the
  set ever enforces it**. Either add the enforcement to AD-8172's scope or drop the permission from
  AD-8170 until the reg-card mapping work lands (an unenforced permission is dead weight and will
  confuse the next person).

  ### 4. Missing implementation steps in AD-8170

  Checked against `agent-plugins/claude-plugins/backend/skills/add-canary-permission/SKILL.md`
  (the repo's own procedure for this). Not in the ticket:

  - **Migrations.** Adding a `Permission` member requires
    `permissions/migrations/NNNN_alter_permissiongrant_granted_permission.py` (last one is 0067/0068).
    Adding a `DefaultPropertyRole` member ALSO generates migrations — `default_role` is a
    `CharField(max_length=30, choices=DefaultPropertyRole.choices)` on `PropertyRoleGrant`
    (`permissions/models/property_role_grant.py:39-41`), plus `AnalyticsRoleGrant` and
    `PortfolioWidePropertyRoleGrant`, plus
    `task_management/models/hotel_department.py:39` (`ArrayField` base field with the same choices).
    → Per repo policy these ship in **their own PR**. AD-8170 as written mixes migration + enum +
    frontend, which the canary PR linter will reject. Worth splitting in the ticket.
  - **`max_length=30` on the new default role value.** `check_in_advanced_configuration` is 31 chars
    and will not fit. Pick something like `advanced_configuration` (22) — or widen the column, which
    is a bigger change than it looks (4 models).
  - **`REQUIRES_MFA_PERMISSIONS`** (`permission.py`) — not mentioned. Every `*_HAS_SETTINGS_ACCESS`
    permission is in there; an advanced-configuration permission almost certainly should be too.
  - **Locale keys + `make translate`.** `permissions.<value>` and
    `permissionsStandaloneName.<value>` in `frontend/packages/canary-ui/src/locale/en.json`
    (97 such keys today), then `make translate` from the repo root. Missing these fails
    `make translate-check` in CI.
  - **Which union in `Permission.ts`.** The ticket says only "present and typed". There are two
    slots: `PERMISSIONS_BY_PRODUCT_ACCESS` (which drives
    `frontend/packages/shared/components/PropertyRolePermissionsForm.vue` — the hotel-facing custom
    role editor) and `IntentionallyExcludedPermissions`
    (`Permission.ts:243-255`). These must go in **`IntentionallyExcludedPermissions`**, otherwise
    hotel admins get a checkbox in the role editor that the backend then 400s on
    (`CreateRoleRequestSchema.validate_object`, `permissions/views/list_create_roles.py:88-98`).
    Not a privilege escalation, but a visible broken control. Worth spelling out.

  ### 5. AD-8170's AC about role visibility is satisfied — worth saying so

  I checked whether a new `DefaultPropertyRole` would leak into the hotel-facing role picker. It
  won't: `ListCreateRolesView.get` (`permissions/views/list_create_roles.py:106-124`) hard-codes
  PROPERTY_MANAGER and PROPERTY_STAFF rather than iterating the enum. Good, but that means it's
  *incidental* — worth an explicit test so someone refactoring that view to iterate the enum doesn't
  quietly expose the staff role.

  ### 6. AD-8171 — answering Leandro's backfill question

  His question: *"changing it will work for new users, but we will also need a one-time command to
  prefill existing ones with the role I think?"*

  Yes, and importantly it is **not** the usual permission backfill. Two mechanisms exist and neither
  fits:
  - `permissions/management/commands/update_roles_with_new_permissions.py` operates on
    `PropertyRole` / `PermissionGrant` rows via a proxy permission. Training users hold a
    **default-role grant** (`PropertyRoleGrant.default_role`), not a custom role — this command
    won't touch them.
  - `PermissionGrantBackfillService.add_permission_to_matching_roles` — same problem.

  What's actually needed is a small one-time command that finds existing training users
  (`CompanyHotelUser.objects.filter(user__email=TrainingUsersService.TRAINING_USER_EMAIL)` —
  `onboarding/services/training_users.py:15`) and calls
  `RoleService.grant_default_role_to_user(user, <new role>, hotel_id)`. That's safe: multiple default
  role grants per user/hotel are supported and deduped
  (`RoleService.grant_default_roles_to_user`, `permissions/services/role.py:289-308`). Cheap — I'd
  keep it inside AD-8171 rather than a separate ticket, and bump the estimate from 1 to 2.

  One trap for whoever writes it: `grant_default_roles_to_user` routes on
  `DEFAULT_ROLE_PERMISSION_CONTEXT[default_role]` — if the new role isn't mapped to
  `PermissionContext.PROPERTY` in `default_role.py`, it silently creates an `AnalyticsRoleGrant`
  instead. The module-level assert catches a *missing* entry but not a *wrong* one.

  ### 7. Cohort AD-8171 doesn't cover

  Canary staff on the Demo and EPD Test portfolios are granted `PROPERTY_MANAGER` via
  `canary_staff/services/canary_staff_service.py:62-83` (`GROUP_ACCESS_SPECS`, incl.
  `GoogleGroups.WHOLE_TEAM` → EPD Test Portfolio). They use the configurator today purely via
  `is_staff`, and will lose it. Either add them to AD-8171's scope or add an explicit
  "out of scope / accepted" line so it isn't a surprise on deploy.

  ### 8. Sequencing note

  AD-8172 flags AD-8153 (payment bucket write,
  https://linear.app/canary-technologies/issue/AD-8153/, PR
  https://github.com/canary-technologies-corp/canary/pull/52174) as in review against the old
  gatekeeper. It's still **In Review** as of this run — the "fold it in or follow immediately" note
  is still live and worth a nudge so 8153 doesn't sit and force a rebase.

  ### Suggested reply to Leandro (draft — NOT sent)

  > Went through all three. Shape is right, and the tickets are more thorough than most — a few
  > corrections:
  >
  > 1. Don't file the new permissions under product CHECK_IN, and don't put them at strength ADMIN.
  >    `HotelService.get_admins()` requires ALL admin-equivalent permissions for a hotel's active
  >    products, so a CHECK_IN+ADMIN permission that no property manager holds makes `get_admins()`
  >    return empty — silently killing admin CC digests, tip reports and sync alerts. Use
  >    `PERMISSIONS_NOT_BY_PRODUCT` + STAFF/POWER_USER strength.
  > 2. AD-8172 says `__permissions__` — that's the v1 idiom. This view is RF v2, so it's
  >    `HotelUserGatekeeper(hotel_permissions=HotelPermissions(hotel_all=[...]))`, and the gatekeeper
  >    is class-level so GET and PATCH can't have different permissions without splitting the view or
  >    checking in-handler. Also, the hotel is a query param today — re-gating means a URL change.
  > 3. Field-level gating is still the open bit. `CS_EDITABLE_FIELDS` is the wrong axis now
  >    (it means "CS may edit" in a CS-only world). You'll need a new bucket ClassVar for
  >    hotel-vs-staff, `serialize_bucket` needs permission context passed in (it takes none today),
  >    and the write service needs to reject gated fields. I think AD-8172 is more like 4 points, or
  >    two tickets.
  > 4. On the backfill: yes, and it's not `update_roles_with_new_permissions` — training users hold a
  >    default-role grant, not a custom role. It's a small command that calls
  >    `RoleService.grant_default_role_to_user` for existing training users. Keep it in AD-8171.
  > 5. AD-8170 is also missing the migrations (adding a DefaultPropertyRole changes 4 models' choices
  >    — and note `max_length=30`, so the role value has to be short), `REQUIRES_MFA_PERMISSIONS`, and
  >    the locale keys + `make translate`. Migrations need their own PR.

  ### Verification status

  All claims above were checked against the working tree on branch
  `glloyd/ent-7078-modify-country-china-to-greater-china` (clean) by reading source. **No tests were
  run and no code was changed** — this is a read-only review.
project: 2026-04-16T1210-unblock-team
source_id: https://canarytechnologies.slack.com/archives/C0BKDAG8FMY/p1786111203037999?thread_ts=1785851167.958619&cid=C0BKDAG8FMY
tags:
- morning-gtd
- slack
time_minutes: 30
title: Craft feedback on Leandro's tickets
updated: 2026-08-12 11:47:07.286642
waiting_on: null
waiting_since: null
working_on: false
---

I said "Thank you! I'll review" on Aug 7. Canary-staff-only check-in config permissions, re-gating adminland endpoints, granting the advanced-configuration role to training users (+ open question on a backfill command for existing users).
https://canarytechnologies.slack.com/archives/C0BKDAG8FMY/p1786111203037999?thread_ts=1785851167.958619&cid=C0BKDAG8FMY