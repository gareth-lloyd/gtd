---
area: null
completed_at: null
contexts:
- react
created: 2026-08-11 08:15:10.129996
defer_until: null
due: 2026-08-12
energy: medium
id: 2026-08-11T0815-reply-to-leandro-on-ad-8170-ad-8172-check-in-confi
order: null
output: |
  ## Agent run 2026-08-12T11:04

  Verified Leandro's two replies against the code, drafted replies for all three
  tickets. NOTHING POSTED — drafts below need your approval before they go to Linear.

  Tickets: AD-8170 https://linear.app/canary-technologies/issue/AD-8170/permissions-add-canary-staff-only-check-in-configuration-permissions
  AD-8171 https://linear.app/canary-technologies/issue/AD-8171/permissions-grant-the-advanced-configuration-role-to-training-users
  AD-8172 https://linear.app/canary-technologies/issue/AD-8172/permissions-re-gate-check-in-configuration-endpoints-for-adminland

  ### Verification summary (what I checked, so you can trust the drafts)

  His claims hold:

  - `create_admin_roles_for_products` (`permissions/services/activation.py:405-414`)
    does pass the whole `PERMISSIONS_BY_PRODUCT[product]` into `update_or_create_role`
    with no strength filter. Confirmed.
  - The other three role builders (`activation.py:504, 524, 544`) each `.intersection()`
    with a single strength (`STAFF`, `POWER_USER`, `ADMIN_EQUIVALENT_PERMISSIONS`), so
    they will not pick up a new strength. Confirmed.
  - A new `PermissionStrength` keeps the asserts green: `permissions/constants/permission.py:610`
    is `set(Permission) == _ALL_BY_STRENGTH`, and `ADMIN_EQUIVALENT_PERMISSIONS` is literally
    `PERMISSIONS_BY_STRENGTH[ADMIN]` (`permission.py:615`) — so `get_admins`
    (`hotels/services/hotel.py:345-351`) is untouched by construction. His fix is sound.
  - `HotelUserGatekeeper(hotel_permissions=...)` is the right mechanism
    (`canary/access_control/gatekeepers.py:72-79`).

  Three things I found that neither of us had written down:

  1. `update_or_create_role` (`activation.py:384-398`) tops up an EXISTING role with any
     missing permissions. So the leak isn't only on fresh activation — re-running
     activation on an already-live check-in hotel injects the new perms into its existing
     "Check In Admin" role. The exclusion is load-bearing for existing hotels, which is
     exactly the "no existing hotel user gains access on deploy" criterion.
  2. "A hotel admin can't create a role containing them" is ALREADY enforced, by the
     superset check in `CreateRoleRequestSchema.validate_object`
     (`permissions/views/list_create_roles.py:87-97`) and the update equivalent
     (`delete_update_role.py:119-144`): you can only grant permissions you hold. Worth
     writing into the ticket so nobody adds redundant enforcement.
  3. That same check is what creates the AD-8171 escalation path (see below) — a training
     user who holds the new role ALSO holds `PLATFORM_HAS_USER_MANAGEMENT_SETTING_ACCESS`
     from `PROPERTY_MANAGER`, so the superset check then permits them to mint a custom
     hotel role containing the staff-only perms.

  I swept every other `PERMISSIONS_BY_PRODUCT` consumer. All safe except one to eyeball:
  `permission.py:190` and `hotel_staff_user.py:880` are allowlist filters, not grants;
  `deactivation.py:42` removes the whole product set (correct); but
  `activate_new_permissions` (`activation.py:246`) builds `accessible_permissions`
  unfiltered and feeds `_create_roles_by_permission`. That path keys off legacy Django
  perms and only runs for hotels not yet on `has_new_permissions_only`, so brand-new
  permissions shouldn't land in any role — but it's the only other place that turns
  `accessible_permissions` into grants, so it deserves a test rather than an assumption.

  Also: adding a `DefaultPropertyRole` value changes a `models.TextChoices` used as
  `choices=` on CharFields across property/portfolio/corporate/analytics grant models —
  that generates `AlterField` migrations, and repo rules say migrations ship in their own
  PR. Worth planning the split up front.

  My call on the AD-8171 backfill question: no data migration needed.
  `grant_default_roles_to_user` is idempotent (`permissions/services/role.py:301-303`
  skips roles the user already has) and `get_or_create_training_user` reuses the existing
  user then re-grants. So provisioning is re-runnable — make the AD-8171 change, then run a
  one-time script over hotels with existing training users, scoped to check-in hotels.
  Precedent already exists: `tmp/onetime/20250725_audit_training_users.py` loops hotels
  calling `get_or_create_training_user`.

  ### DRAFT — reply on AD-8170 (as a reply in the existing thread)

  Checked this through and your fix is right — new strength, both perms still mapped to
  `CHECK_IN`, excluded in `create_admin_roles_for_products`. `ADMIN_EQUIVALENT_PERMISSIONS`
  is just `PERMISSIONS_BY_STRENGTH[ADMIN]`, so `get_admins` is unaffected by construction
  rather than by us being careful, which is the property we want. The `set(Permission) ==
  _ALL_BY_STRENGTH` assert stays green with a new bucket, and the other three builders each
  intersect one strength, so they won't pick it up.

  Three additions before you start:

  One — `update_or_create_role` tops up an existing role with missing permissions, so this
  isn't only a fresh-activation leak. Re-running activation on an already-live check-in
  hotel would inject the new perms into that hotel's existing "Check In Admin" role. That's
  the path that actually threatens the "no existing hotel user gains access on deploy"
  criterion, so please cover it with a test that runs activation twice against a hotel that
  already has the admin role.

  Two — "a hotel admin can't create a role containing them" is already enforced: role
  create and update both require the acting user's own permissions to be a superset of what
  they're granting (`list_create_roles.py:87-97`, `delete_update_role.py:119-144`). So
  that criterion holds for free as long as nobody at the property holds the permission. No
  new code needed — worth noting in the ticket so it doesn't get built twice.

  Three — one thing to eyeball rather than assume: `activate_new_permissions` builds
  `accessible_permissions` from the unfiltered product set and feeds
  `_create_roles_by_permission`. It keys off legacy Django perms and only runs for hotels
  not yet on `has_new_permissions_only`, so I expect new permissions can't land in a role
  there — but it's the only other place that set turns into grants, so let's confirm it.

  Last thing: adding a `DefaultPropertyRole` value changes `models.TextChoices` used as
  `choices=` on several grant models, which generates `AlterField` migrations. Migrations
  ship in their own PR here, so plan the split up front.

  ### DRAFT — reply on AD-8172 (as a reply in the existing thread)

  Agreed on all three, and the split you landed on is the right one — one gatekeeper
  requiring `CHECK_IN_HAS_SETTINGS_ACCESS` on both views, advanced access checked in the
  service against the field allowlist. A field name arrives in the body, so a gatekeeper
  can't gate on it; that was my point and you've got it.

  One detail that supports the "cross-hotel access structurally impossible" criterion:
  `HotelUserGatekeeper.check_permissions` raises `ServerError` when `hotel_permissions`
  are declared but no resource established a `hotel_id`. So declaring the permissions
  without the `HotelResource(authorize=AuthorizeHotel())` path param fails loudly instead
  of silently allowing — the two halves of the change can't be half-done. Worth a test
  that asserts the 403 comes from the URL's hotel, not from anything in request data.

  Still needs a decision: AD-8153 is in review against the old gatekeeper. I'd let it merge
  first and follow immediately after rather than folding it in — smaller diff to review,
  and the URL change is easier to reason about on its own.

  ### DRAFT — new comment on AD-8171

  Two calls needed here.

  Backfill: no data migration. `grant_default_roles_to_user` skips roles the user already
  holds, and `get_or_create_training_user` reuses an existing user and re-grants, so
  provisioning is re-runnable. Make the change, then run a one-time script over hotels that
  already have training users, scoped to check-in hotels —
  `tmp/onetime/20250725_audit_training_users.py` is the precedent.

  Escalation path, which I think is the more important one: a training user granted the new
  role also holds `PLATFORM_HAS_USER_MANAGEMENT_SETTING_ACCESS` from `PROPERTY_MANAGER`.
  Role creation only checks that you hold everything you're granting — so that training user
  can mint a custom role containing the staff-only permissions and grant it to a real
  property user. Impersonating a training user carries write access, so CS can reach it too.

  That means "Canary-staff-only" would be true incidentally (nobody holds it) rather than
  structurally (nobody can grant it). I'd rather it be structural: an explicit
  non-grantable set checked in the create and update `validate_object`, so the permissions
  can't be put in a custom role regardless of who's asking. It's cheap and it closes the
  hole AD-8171 opens. Happy to be argued out of it if you think pre-go-live-only scope
  makes it acceptable, but let's decide it deliberately rather than inherit it.

  ### Not done

  Nothing posted to Linear — all three drafts are awaiting your approval. AD-8153 fold-in
  vs follow-after is called in the draft but is ultimately yours/Leandro's to settle.
project: 2026-04-16T1210-unblock-team
source_id: https://linear.app/canary-technologies/issue/AD-8172/permissions-re-gate-check-in-configuration-endpoints-for-adminland
tags:
- morning-gtd
- linear
time_minutes: 20
title: Reply to Leandro on AD-8170 / AD-8172 check-in configuration permissions
updated: 2026-08-12 13:48:00.826806
waiting_on: null
waiting_since: null
working_on: true
---

He answered both review points: gatekeeper changed to HotelUserGatekeeper(hotel_permissions=...), and he found that create_admin_roles_for_products builds the Admin role from the whole PERMISSIONS_BY_PRODUCT[CHECK_IN] set without filtering by strength — so staff-only perms leak to admins. AD-8171 also needs a call on backfilling existing users.
https://linear.app/canary-technologies/issue/AD-8172/permissions-re-gate-check-in-configuration-endpoints-for-adminland
https://linear.app/canary-technologies/issue/AD-8170/permissions-add-canary-staff-only-check-in-configuration-permissions