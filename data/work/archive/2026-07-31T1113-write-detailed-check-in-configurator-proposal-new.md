---
area: null
contexts:
- react
created: 2026-07-31 11:13:26.957988
defer_until: null
due: null
energy: medium
id: 2026-07-31T1113-write-detailed-check-in-configurator-proposal-new
order: null
output: |
  ## Agent run 2026-07-31T11:40:00+03:00

  Researched the permissions machinery in backend/canary and drafted the detailed
  expansion of the Slack proposal
  (https://canarytechnologies.slack.com/archives/C0BKDAG8FMY/p1785419100835479).
  Nothing was posted anywhere — the draft below is ready for you to review and post
  to #tmp-check-in-configuration-location (or turn into a doc).

  ### Key code findings the draft rests on

  - `backend/canary/permissions/constants/permission.py` — the `Permission` enum, with a
    startup assert that every permission has a `PERMISSIONS_BY_STRENGTH` bucket.
  - `backend/canary/permissions/constants/default_role.py:144` — **an assert requires every
    permission to appear in the union of the default roles, and Property Manager is the
    de-facto catch-all.** Not granting PM the new perms therefore needs one structural
    tweak: an explicit `CANARY_STAFF_ONLY_PERMISSIONS` set that the assert unions in.
    This is the only non-mechanical change; everything else is checklist work.
  - Default-role grants resolve **dynamically at check time**
    (`PermissionService.get_permissions_for_default_role` reads `DEFAULT_ROLE_PERMISSIONS`
    live), so leaving the perms out of PM means zero hotel exposure everywhere, instantly —
    and adding them later is equally instant for default-role holders.
  - Hotels cannot self-escalate: `ListCreateRolesView` (`permissions/views/list_create_roles.py:88-98`)
    rejects creating/editing a role containing any permission the acting user doesn't hold.
    Since no hotel user holds the new perms, no hotel-created role can ever contain them.
  - The `backend:add-canary-permission` skill's checklist applies (strength bucket, product
    mapping, MFA set, choices migration, frontend `Permission.ts` mirror, en.json keys +
    `make translate`). Its "PROPERTY_MANAGER always gets every new permission" rule is the
    thing this proposal deliberately deviates from — flagged in the draft, and the skill's
    rollout guide should get an update if we adopt this.
  - Note for accuracy: master still models Property Manager as a *dynamic* default role
    (only Property Staff has the concretization rollout:
    `Hotel.rollout_hide_property_staff_default_role` + `migrate_property_staff_to_custom_roles`).
    Your Slack message "property manager is no longer modeled as a default role" reads as
    ahead of master — the draft is written to be correct in both worlds.

  ### Draft Slack post (expansion: the new permissions)

  ---

  Expanding on the permissions part of my proposal above — concretely, what we add and
  what it buys us.

  *The new permissions*

  Two to start, under the Check-In section of `permissions/constants/permission.py`:

  • `CHECK_IN_HAS_ADVANCED_CONFIGURATION_ACCESS` / "Check-in - Has Advanced Configuration
  Access" — umbrella for the staff-only sections of the configurator.
  • `CHECK_IN_CAN_MANAGE_PMS_REGISTRATION_CARD_MAPPING` / "Check-in - Can Manage PMS
  Registration Card Mapping" — the reg-card field-mapping surface specifically.

  The pattern scales: each future staff-only capability gets its own permission, and
  "extend hotels' abilities as the UI is refined" is then a grant change, not a code change.

  Plus the routine registrations every permission needs: `PERMISSIONS_BY_STRENGTH`
  (ADMIN bucket), `permissions_by_product.py` under `CanaryProducts.CHECK_IN` (so they're
  automatically inert on hotels without check-in), the `granted_permission` choices
  migration, the frontend `Permission.ts` mirror + locale keys. One open decision:
  whether to add them to `REQUIRES_MFA_PERMISSIONS` — consistent with every other
  settings-access permission (yes by default), but we should confirm MFA plays well with
  the impersonated-session flow before enforcing.

  *What NOT adding them to Property Manager implies*

  • One deliberate deviation from convention: today `default_role.py` asserts that every
  permission belongs to some default role, with Property Manager as the catch-all. We add
  an explicit `CANARY_STAFF_ONLY_PERMISSIONS` set and union it into that assert. That set
  becomes the self-documenting registry of "permissions no hotel role gets by default".
  • Zero hotel exposure on deploy. Default-role permissions resolve dynamically at check
  time, so no PM user anywhere gains access — nothing to backfill, nothing to claw back.
  This is a pure "new functionality" rollout: views can enforce from day one.
  • Hotels can't self-escalate. Role create/edit already requires the acting user to hold
  every permission they grant, so no hotel admin can mint a role containing these. They
  are only grantable from Canary-side tooling.
  • Extending to hotels later is config-only: add to the PM defaults (instant for
  default-role holders) and run the existing
  `update_roles_with_new_permissions --proxy-permissions=check_in_has_settings_access --new-permissions=...`
  backfill for concrete custom/SSO/portfolio roles. No view or frontend changes.
  • Who *does* hold them: the user attached to a check-in-configuration-type SAG (granted
  a Canary-managed role containing them), and training users pre-go-live (simple config,
  as discussed with Stephanie). Regular, non-targeted SAG users: not granted.

  *Lea and Dana are unblocked now*

  The UI work doesn't wait for the SAG "type of grant" mechanism. Gating is the completely
  normal pattern used by every adminland page:

  • Backend: staff-only endpoints declare
  `__permissions__ = [Permission.CHECK_IN_HAS_ADVANCED_CONFIGURATION_ACCESS]` on their
  Request Framework schema; hotel-facing endpoints keep `CHECK_IN_HAS_SETTINGS_ACCESS` /
  `CHECK_IN_HAS_REGISTRATION_CARD_SETTINGS_ACCESS`.
  • Frontend: standard permission checks against the mirrored `Permission.ts` entries —
  sections simply don't render without the permission. No `is_staff`, no
  impersonation-awareness anywhere in views or components.
  • Dev/test: grant a local user a role containing the new perms (e.g. via
  `dev_set_up_permissions_scenarios`). The SAG plumbing lands independently and just
  determines *who* holds the permissions in production.

  Sequencing: PR 1 = enum + migration + registrations + frontend mirror (no enforcement,
  safe to merge any time); the configurator PRs then enforce as they build.

  ---

  ### Suggested next steps (yours to decide)

  - Review/edit the draft and post it to the thread.
  - If the direction is adopted, the implementation is a clean `backend:add-canary-permission`
    run with the one PM deviation (+ update the skill's rollout guide so "PM always gets
    every new permission" documents the staff-only escape hatch).
project: null
source_id: https://canarytechnologies.slack.com/archives/C0BKDAG8FMY/p1785419100835479
tags:
- morning-gtd
- slack
- from-awareness
time_minutes: 30
title: 'Write detailed check-in configurator proposal: new permissions'
updated: 2026-07-31 12:47:06.017551
waiting_on: null
waiting_since: null
working_on: false
---

Expand my #tmp-check-in-configuration-location proposal, specifically the new permissions: add them under django permissions/constants/permission.py; explain what NOT adding them to the Property Manager role implies; Lea and Dana can continue UI work, gating functionality with permissions in the completely normal way.
https://canarytechnologies.slack.com/archives/C0BKDAG8FMY/p1785419100835479