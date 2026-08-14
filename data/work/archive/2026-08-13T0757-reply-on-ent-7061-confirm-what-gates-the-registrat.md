---
area: null
completed_at: 2026-08-13 15:26:36.319206
contexts:
- react
created: 2026-08-13 07:57:17.333632
defer_until: null
due: 2026-08-13
energy: low
id: 2026-08-13T0757-reply-on-ent-7061-confirm-what-gates-the-registrat
order: 6
output: |
  ## Agent run 2026-08-13T05:08:40Z

  Traced the full gate in the codebase. **Andrea's guess is wrong — this is NOT a
  role/permission issue.** The nav item is missing because of a hotel config flag
  the IHG scripts never set.

  Ticket: https://linear.app/canary-technologies/issue/ENT-7061/expose-registration-card-in-product-settingsadminland-when-we-run-ihg

  ### What actually hides the nav item

  Only one place declares it — `frontend/adminland/src/components/AdminSidebar.vue:678-703`.
  The `v-if` (lines 679-682) has exactly TWO conditions:

  1. `hotel.has_check_in`
  2. `hotel.check_in_configuration.has_registration_card_settings`

  Everything else in Andrea's 5-condition list is a *different layer*:

  - **Free plan** (`!hotel.is_free`, AdminSidebar.vue:686) sits in `enabled-for-user`,
    so it greys the item out, does not hide it. It does hard-block the route
    (AdminRouterView.vue:41-47, 72-77).
  - **`check_in_has_registration_card_settings_access`** (AdminSidebar.vue:104,
    via `useUserAccessLevelToSettings`) also only greys it out — renders disabled
    with a "You do not have permission" tooltip. Item still visible.
  - **`has_registration_card_canary_ui`** — REFUTED as a gate. Only picks new vs
    legacy editor once you're on the page (RegistrationCardContentEditor.vue:221).
  - **`registration_card_step`** — REFUTED. Guest-side check-in flow only
    (CheckInStore.ts:396-398). Zero adminland involvement.

  ### Root cause for IHG

  - `has_registration_card_settings` model default is **False**
    (`backend/canary/check_in/models/configuration.py:1105-1109`, help_text:
    "Rollout flag: Enable hotel-facing registration card settings").
  - IHG scripts set `has_check_in = True`
    (`onboarding/configuration_providers/ihg/enable_msa_products_provider.py:41`,
    and `enterprise_ihg/configs/ihg_pilot.py:29`) — so condition 1 is already met.
  - IHG scripts **never touch `has_registration_card_settings`**. The IHG
    `enable_msa_products_provider.py:55-78` sets ~14 check-in config fields but not
    that one. `IHGRegistrationCardProvider` (registration_card_provider.py:123-222)
    only writes the RegistrationCard schema rows and leaves
    `check_in_configuration_updates = None` (line 58), so `AddRegistrationCardPlan`
    (`onboarding/plans/registration_card_plans.py:71-83`) makes zero config writes.

  **BW and Wyndham both DO set it**, right next to each other:
  - `onboarding/configuration_providers/best_western/enable_msa_products_provider.py:84-85`
  - `onboarding/configuration_providers/wyndham/wyndham_enable_msa_products_provider.py:133-134`
  - declarative equivalent `enterprise_wyndham/configs/wyndham.py:233-234`

  Both set `has_registration_card_settings = True` AND
  `has_registration_card_canary_ui = True`. IHG is simply the odd one out — this
  looks like an omission, not a deliberate choice.

  ### Answer to "should IHG scripts set it?"

  Yes. Two-line change mirroring BW/Wyndham in
  `onboarding/configuration_providers/ihg/enable_msa_products_provider.py`, plus the
  declarative equivalent in `enterprise_ihg/configs/ihg_pilot.py` (which today only
  has `push_registration_card_email_to_pms` at line 66).

  ### Permission side — separate, and needs a decision

  Once the flag is on, the item appears but may render greyed for IHG staff.

  - Permission granted by default only to `DefaultPropertyRole.PROPERTY_MANAGER`
    (`permissions/constants/default_role.py:90`). `PROPERTY_STAFF` does NOT have it
    (:22-51).
  - New hotels get only the generic "Property Staff" role from
    `ActivationService.turn_on_permissions_settings`
    (`permissions/services/activation.py:361-381`) — which excludes it.
  - BUT `PERMISSIONS_BY_PRODUCT` (`permissions/constants/permissions_by_product.py:102-106`)
    maps `REGISTRATION_CARD_SETTINGS -> {CHECK_IN_HAS_REGISTRATION_CARD_SETTINGS_ACCESS}`,
    and `create_admin_roles_for_products` (activation.py:400-413) auto-creates an
    Admin role per active product. So turning the flag on also makes the permission
    grantable/auto-granted via that path.
  - **IHG-specific wrinkle**: no IHG onboarding provider creates or assigns roles at
    all. IHG staff roles come from SSO group mappings at SAML login
    (`sso/models/organization_role_mapping.py`, `sso/services/sso_organization.py:436,505,633`)
    — DB rows configured outside the script. So if IHG's mapped roles are custom
    PropertyRoles, someone has to add the permission to those mappings as data. That
    is a config task, not a script change.

  ### Two things worth flagging to the team

  1. **The permission is admin-strength.** It's in
     `PERMISSIONS_BY_STRENGTH[PermissionStrength.ADMIN]` (`permissions/constants/permission.py:514`)
     and `ADMIN_EQUIVALENT_PERMISSIONS = PERMISSIONS_BY_STRENGTH[ADMIN]` (:615) — so
     granting it broadly to IHG front-desk roles makes those users admin-equivalent
     for some checks. Worth a deliberate decision before mapping it widely.
     (It is deliberately NOT MFA-gated — absent from `REQUIRES_MFA_PERMISSIONS`
     (:456-496) and test-pinned at
     `hotels/tests/services/test_multi_factor_authentication.py:244-262`.)
  2. **Pre-existing inconsistency (not IHG-specific).**
     `canary/canary_products.py:82-83` adds `REGISTRATION_CARD_SETTINGS` to
     `available_products` based on `has_registration_card_settings` alone, without
     checking `has_check_in`. The sidebar `v-if` checks both. So a hotel with
     `has_check_in=False` + flag True is directly navigable by URL (and can even be
     picked as the landing page via `PREFERRED_DEFAULT_ORDER`, helpers/products.ts:272)
     while the nav item never renders — and `check_in_configuration` serializes as
     `None` in that case (`hotels/utils/api/serialize_hotel.py:397-399`), so the page
     reads null. Doesn't bite IHG (they set `has_check_in=True`) but it's a latent bug.

  ### Status

  Draft Linear reply prepared but **NOT posted** — awaiting your approval. Draft text
  is in the session transcript; ask me to re-print it.

  ## Agent run 2026-08-13T12:28:45Z — verification pass

  Re-read ticket + comments and independently re-verified every code claim above
  (did not rely on the subagent reports). **All code facts confirmed.** Corrections
  are to framing, plus three things missed on the first pass.

  ### Independently re-verified (all CONFIRMED)

  - `AdminSidebar.vue:679-682` — v-if is exactly `hotel.has_check_in && hotel.check_in_configuration?.has_registration_card_settings`. Read the literal source.
  - `AdminSidebar.vue:685-689` — `!hotel.is_free && registrationCardAccessLevel !== NONE` is in `enabled-for-user`, NOT the v-if.
  - `SidebarItem.vue:100-101` — `disabled = !enabledForUser || !enabledForHotel`; applies `--disabled` class (:129/:281), nulls href (:151), swallows click (:163), shows contact-admin (:137) + tooltip (:190). `hidden` is a SEPARATE prop and the reg-card item never passes it. So disabled != hidden. Crux claim holds.
  - `check_in/models/configuration.py` — `has_registration_card_settings` default **False**; `has_registration_card_canary_ui` default True; `registration_card_step` default REQUIRED. Read verbatim.
  - `grep -rn "has_registration_card" onboarding/configuration_providers/ihg/ enterprise_ihg/` -> **zero matches**. Stronger than first reported.
  - BW `enable_msa_products_provider.py:84-85`, Wyndham `wyndham_enable_msa_products_provider.py:133-134`, `enterprise_wyndham/configs/wyndham.py:233-234` — all set both flags. Confirmed.
  - `registration_card_plans.py:70` — `if self.config_provider.config.check_in_configuration_updates:` guard; IHG provider `:57` builds `RegistrationCardConfig(brand=data.brand_id)` with no updates -> falsy -> zero config writes. Confirmed.
  - `default_role.py:90` sits inside `PROPERTY_MANAGER` frozenset (block 52-138); `PROPERTY_STAFF` is 22-51 with no match. Confirmed.
  - `permission.py:514` sits inside `PermissionStrength.ADMIN` frozenset (block 510-541); `ADMIN_EQUIVALENT_PERMISSIONS` = that set at :615. Admin-strength claim holds.

  ### Products discrepancy — STRENGTHENED, not weakened

  I initially cited only the legacy per-user block (`canary_products.py:82-83`). There
  are two paths. `Hotel.available_products` (`hotels/models/hotel.py:1889-1893`) ->
  `get_available_products` -> `PRODUCT_ACTIVATION_RULES` (:288), and the reg-card rule
  (:344-348) is `_hotel_field_rule(..., "check_in_configuration__has_registration_card_settings", ...)`.
  **Neither path checks `has_check_in`**, while the sidebar v-if does. The
  inconsistency is real under the live path, not just the legacy one.

  ### Correction to my framing of Andrea's list

  I was unfair to it in the first draft. Andrea's list came "per claude" and item 5 was
  explicitly labelled **"Optional behavior knobs"** — it never claimed those were gates.
  Calling it "REFUTED" attacked a strawman. Andrea's actual ask was *"I don't understand
  point 5"*, so the reply should EXPLAIN point 5, not rebut it.

  Items 1-4 are all genuine conditions for a user to *use* the page. The list's only real
  gap is that it doesn't separate **hidden** (1-2) from **greyed out** (3-4) — and that
  distinction is exactly what identifies the IHG cause. Andrea's "role/permission issue?"
  guess is a reasonable hypothesis about a real gate; it just isn't the one failing here,
  because for IHG the item is entirely absent rather than greyed.

  ### Missed on first pass

  - **Related ticket ENT-7124** "IHG - All Regions - Default Registration Card Policies"
    (https://linear.app/canary-technologies/issue/ENT-7124/ihg-all-regions-default-registration-card-policies),
    same "Registration Cards" milestone, links ENT-7061 and ENT-7062. Defines default
    policy text for new IHG properties — complementary to this ticket.
  - **The IHG script already builds the reg card content.** `IHGRegistrationCardProvider.perform_hotel_configuration()`
    creates the CHECK_IN + KIOSK `RegistrationCard` schema rows. IHG hotels *have*
    registration cards — only the hotel-facing settings surface is hidden. That reframes
    the ticket as "expose the existing thing", matching Connor's title.
  - **No branch/commits exist yet** for ENT-7061 (`git branch --list "*7061*"` empty; the
    `gitBranchName` on the ticket is Linear's auto-generated suggestion).

  ### Net conclusion (unchanged)

  Root cause is `has_registration_card_settings` defaulting to False with no IHG script
  ever setting it. Fix mirrors BW/Wyndham. Permission side is a separate, genuine
  follow-up needing a decision, because the permission is admin-equivalent and IHG roles
  come from SSO mappings configured as data.
project: 2026-04-16T1210-unblock-team
source_id: https://linear.app/canary-technologies/issue/ENT-7061/expose-registration-card-in-product-settingsadminland-when-we-run-ihg
tags:
- morning-gtd
- linear
time_minutes: 15
title: 'Reply on ENT-7061: confirm what gates the Registration Card settings page
  (IHG scripts)'
updated: 2026-08-13 15:28:45.723342
waiting_on: null
waiting_since: null
working_on: false
---

Connor: "@andrea @glloyd do you know what controls this?" Andrea posted the 5-condition answer and asked "my guess is this is a role/permission issue?" — unresolved. The gate is almost certainly the role permission check_in_has_registration_card_settings_access; confirm and say whether IHG scripts should set it.
https://linear.app/canary-technologies/issue/ENT-7061/expose-registration-card-in-product-settingsadminland-when-we-run-ihg