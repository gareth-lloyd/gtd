---
area: null
completed_at: 2026-10-02 16:26:10.607557
contexts: []
created: 2026-09-30 22:27:59.881862
defer_until: null
due: 2026-10-02
energy: low
id: 2026-09-30T2227-check-whether-old-permissions-code-has-been-fully
order: null
output: |
  ## Agent run 2026-10-02T12:11:30Z

  **Verdict: no, the old Django-permission code is not fully removed from the UI.**
  The `has_new_permissions_only` flag is gone from the frontend (0 references, PR #43419
  https://github.com/canary-technologies-corp/canary/pull/43419), but the UI still reads
  Django permission codenames from `user.permissions` in 11 production files. Checked
  against master at 09dcddac88c by code search only; nothing was run and no prod data
  was queried.

  ### How the old permissions still reach the UI

  - Backend `hotels/utils/api/serialize_user.py` still sends `permissions`, filtered to the
    9 codenames in its `LegacyPermission` enum (comment: "Aim to remove all of these").
  - Frontend mirror: `LegacyPermission` enum in `frontend/packages/shared/schemas/canary/User.ts`,
    typed onto `User.permissions` and `CurrentUser.permissions`.
  - 3 of the 9 codenames are never read by the UI: `can_use_amenities`, `can_use_contracts`,
    `can_use_authorizations`. They can be dropped from both enums now.

  ### Live UI gates still on `hotel_admin` (user-global Django perm, not per-hotel)

  | Where | What it gates |
  | --- | --- |
  | `hotels/src/checkIns/CheckInModal/CheckInModalHeader.vue:104` | Delete check-in button |
  | `hotels/src/checkOuts/CheckOutModal/CheckOutModalHeader.vue:79` | Delete check-out button |
  | `hotels/src/contracts/ContractModal/ContractModalDocument.vue:109` | Admin may countersign on behalf of the named signer |
  | `hotels/src/App.vue:305`, `hotels/src/components/Header/Header.vue:127`, `adminland/src/App.vue:140`, `adminland/src/components/Header/Header.vue:31` | `HeaderDelinquent` banner: "ask your admin" text vs billing-settings button |
  | `packages/shared/components/internal-app-layout/ProfileMenu.vue:26` | "Administrator" / "Staff Member" label |

  ### Why this matters: the checks are likely wrong, not just stale

  - Only one code path still writes these Django perms from roles:
    `SSOOrganizationService.map_and_assign_roles` (`sso/services/sso_organization.py:825`).
    The role-based `hotel_staff` API writes none.
  - So a non-SSO Property Admin created through the current staff UI should have an empty
    `permissions` list: no delete buttons, "ask your admin" on the delinquent banner,
    labelled "Staff Member". **Not verified against a real user.** Worth a 2-minute check
    with a recently created non-SSO admin.
  - The backend does not match these gates anyway: check-in delete only requires
    `CHECK_IN_HAS_PRODUCT_ACCESS` and check-out delete `CHECK_OUT_HAS_PRODUCT_ACCESS`,
    so the admin-only restriction is UI-only.
  - `hotel_admin` is user-global, so an SSO user with settings access at hotel A reads
    as admin at hotel B.

  ### Dead code (safe to delete, no template reads them)

  - `CheckInModal.vue:118-123` `isAdmin`, `hasViewCCPermission`
  - `CheckInCreditCard.vue:64` `hasViewCCPermission` (template already uses
    `Permission.CHECK_IN_CAN_VIEW_CC`). This is the only `view_cc` read left.
  - `CheckOutModal.vue:88` `isAdmin`
  - `adminland/src/userStore.ts` `adminUsers`: nothing reads it, but `initialize` awaits
    the query, so it costs a users request on every adminland load.
  - `can_refund_payments` has no reader in the UI.

  ### Legacy in name only

  - `AdminSidebar.vue:85` calls `GET users?permission=hotel_admin` for the "ask your admin"
    tooltips. The backend resolves it through `HotelService.get_admins` (role-based) when
    `has_new_permissions_only` is true (`hotels/views/api/user/user.py:182-195`), so the
    behaviour is new and only the wire string is old.

  ### Probably intentional: Canary-staff Django perms in the manage app

  - `manage/src/navigation/manageNavConfig.ts` and `manage/src/components/manageMenuSections.ts`
    gate Cohorts and Purchase Order cleanup on `view_cohort`, `view_cohorthotel`,
    `staff_delete_purchaseorder`, always combined with `is_canary_staff`. These are model
    perms for internal staff, added on purpose (PR #23458
    https://github.com/canary-technologies-corp/canary/pull/23458, PR #54240
    https://github.com/canary-technologies-corp/canary/pull/54240), and fit the
    "cut Django permissions except for staff" intent of ENT-2240
    (https://linear.app/canary-technologies/issue/ENT-2240/completely-cut-use-of-django-permissions-except-for-staff, Canceled).
    They are only mislabelled "Legacy". The two menu files duplicate the same checks.

  ### Other UI surfaces

  - Server-rendered: `backend/canary/hotels/templates/header-admin.html:57,67` uses
    `{% if perms.hotels.hotel_admin %}`, included by 10 legacy Django templates
    (payments, create-new, spreadsheet user upload, hotel_analytics, manage-auth-permissions).
  - mobile / desktop / agents / cli: no references.
  - The frontend no longer sends legacy `permissions` when creating or editing users; the
    backend still accepts them (`set_permissions_for_user`, `user.py:384,529`).

  ### Backend state (context, outside the "UI" ask)

  - `has_new_permissions_only` still has ~55 non-test references, including live legacy
    branches in `contracts/services/contract.py:1093`, `credit_card/views/credit_card.py:118`,
    `hotels/views/api/billing.py:59`, `hotels/views/views.py:1415`, and it is still serialized
    in `hotels/utils/api/serialize_hotel.py:226`.
  - ENT-4469 (https://linear.app/canary-technologies/issue/ENT-4469/remove-all-usage-of-has-new-permissions-only)
    is marked Deployed but only its frontend part shipped.

  ### Ticket coverage

  - Open in "Clean up legacy permissions": ENT-5669 views
    (https://linear.app/canary-technologies/issue/ENT-5669/remove-has-new-permissions-only-from-views),
    ENT-5670 services
    (https://linear.app/canary-technologies/issue/ENT-5670/remove-has-new-permissions-only-from-remaining-services),
    ENT-5671 serialization + frontend
    (https://linear.app/canary-technologies/issue/ENT-5671/remove-has-new-permissions-only-from-serialization-frontend).
    All Todo, unassigned, and all about the flag.
  - Related: ENT-5672 test helpers
    (https://linear.app/canary-technologies/issue/ENT-5672/remove-has-new-permissions-only-from-test-helpers-and-test-files),
    ENT-7127 retire legacy `UserAPIView.delete`
    (https://linear.app/canary-technologies/issue/ENT-7127/retire-the-legacy-userapiviewdelete-route-and-view).
  - **Gap: I found no open ticket for removing the `LegacyPermission` reads from the UI.**
    The old one, ENT-2446 `hotels.utils.api.serialize_user`
    (https://linear.app/canary-technologies/issue/ENT-2446/hotelsutilsapiserialize-user), was canceled.
    The search was a title/description query on the ENT team, first page only, so a ticket
    on another team could exist.

  ### Suggested next step (not done, nothing written to Linear)

  One ticket: "Remove `LegacyPermission` reads from hotels/adminland UI".
  1. Delete the dead computeds and the unused `adminUsers` store query.
  2. Replace the `hotel_admin` gates with `hotel.user_permissions_for_hotel` checks.
     Needs a product call on which permission: `PLATFORM_HAS_BILLING_AND_PAYMENTS_SETTING_ACCESS`
     is the obvious fit for the delinquent banner; delete check-in/check-out and contract
     countersign override have no dedicated permission today.
  3. Rename the 3 staff codenames out of `LegacyPermission` (e.g. `StaffPermission`) and trim
     both enums to those 3.
  4. Then drop `LegacyPermissionMappingService` and the `perms.hotels.hotel_admin` template check.

  ## Agent run 2026-10-02T12:22:11Z: ticket plan for dead code

  Drafts only. **Nothing has been created or edited in Linear.** Target project:
  "Clean up legacy permissions" (ENT team). Line refs are as of master 09dcddac88c.

  ### Correction to the run above

  - `LegacyPermissionMappingService` and `POST /api/users` are **live**, not dead. The mapping
    still runs for SSO users and feeds the UI `hotel_admin` gates. ENT-7127 records 17 POSTs a
    week to the create handler, which calls `set_permissions_for_user`.
  - `CanaryStaffService` grants the `hotel_admin` Django codename to staff
    (`canary_staff/services/canary_staff_service.py:1371`), so `hotel_admin` checks outside a
    flag branch are reachable by staff and must not be marked dead.

  ### Series and order

  | # | Ticket | Status | Depends on |
  | --- | --- | --- | --- |
  | A | Mark dead legacy-permission code with a `DEAD-LEGACY-PERMISSIONS` comment | NEW | prod flag check |
  | B | Delete dead legacy-permission reads from the frontend | NEW | A |
  | - | ENT-5669 Remove flag from views (https://linear.app/canary-technologies/issue/ENT-5669/remove-has-new-permissions-only-from-views) | exists, refresh line refs | A |
  | - | ENT-5670 Remove flag from services (https://linear.app/canary-technologies/issue/ENT-5670/remove-has-new-permissions-only-from-remaining-services) | exists, refresh line refs | A |
  | C | Remove unreachable legacy branches and guards not covered by ENT-5669 / ENT-5670 | NEW | A |
  | D | Stop serializing unused legacy permission data | NEW, absorbs backend half of ENT-5671 | B |
  | - | ENT-5590 Deprecate permissions activation service (https://linear.app/canary-technologies/issue/ENT-5590/deprecate-permissions-activation-service) | exists in "Eng Improvements"; move here, drop its step 4 | C |
  | - | ENT-5672 Remove flag from test helpers (https://linear.app/canary-technologies/issue/ENT-5672/remove-has-new-permissions-only-from-test-helpers-and-test-files) | exists | 5669, 5670, C |
  | E | Deprecate `has_new_permissions_only` and `rollout_adminland_role_based_permissions_ui` | NEW | everything above |

  Related, already tracked: ENT-7127 retire `UserAPIView.delete`
  (https://linear.app/canary-technologies/issue/ENT-7127/retire-the-legacy-userapiviewdelete-route-and-view),
  ENT-7126 neutralize `migrate_esa_to_new_permissions`
  (https://linear.app/canary-technologies/issue/ENT-7126/neutralize-migrate-esa-to-new-permissions-so-it-cannot-be-rerun).
  ENT-5671 (https://linear.app/canary-technologies/issue/ENT-5671/remove-has-new-permissions-only-from-serialization-frontend)
  lists 7 frontend files that already shipped in PR #43419; only its `serialize_hotel.py` line is left.

  ### Ticket A: Mark dead legacy-permission code with a `DEAD-LEGACY-PERMISSIONS` comment

  **Context.** Hotel users are authorized only by role-based permissions (`PermissionService`,
  `Permission` enum). The Django-permission paths for hotel users are unreachable but still in
  the tree, next to live Django-permission code for Canary staff. Readers, LLMs especially,
  copy the dead paths or mistake the live staff ones for legacy. Comment-only PR, no behaviour change.

  **Precondition.** Confirm in every region that no hotel has either flag False:
  `Hotel.objects.filter(Q(has_new_permissions_only=False) | Q(rollout_adminland_role_based_permissions_ui=False)).count() == 0`.
  `MigrationProgressService.record_granular_permissions_progress` already records this number,
  so the stored metric may be enough. Note `mobile_key/verification/pa_130`, `pa_257`, `pa_298`
  `setup.py` create hotels with the flag False; confirm they only run locally.

  **Marker.** One greppable token, reason varies by case, two lines at most, no ticket IDs:
  - Python: `# DEAD-LEGACY-PERMISSIONS: unreachable. Every hotel has has_new_permissions_only=True. Do not extend or copy.`
  - Other reasons: `always returns False`, `never raises`, `never read`, `one-off migration, finished`.
  - TS/Vue: `// DEAD-LEGACY-PERMISSIONS: never read. ...`
  - `git grep DEAD-LEGACY-PERMISSIONS` then becomes the worklist for B, C, ENT-5669, ENT-5670 and
    ENT-5590; the series is done when it returns nothing.

  **Mark these (backend, unreachable branches).**
  - `contracts/services/contract.py:1095` else
  - `credit_card/views/credit_card.py:125` else
  - `hotels/views/api/billing.py:65` else
  - `hotels/services/hotel.py:410` else in `get_admins`
  - `hotels/views/views.py:1441-1458` legacy tail of the impersonation-user lookup
  - `hotels/views/api/user/user.py:153` SSO non-attached users branch, `:185` legacy filter
  - `chat/services/message_escalation.py:461` legacy SSO branch
  - `sso/services/manual_user_merge.py:375` Django-permission transfer block
  - `onboarding/configuration_providers/best_western/best_western_roles_and_permissions_provider.py:40`

  **Mark these (always False / never fires).**
  - `permissions/services/permission.py:413` `user_exists_on_hotel_with_legacy_permission`, and its
    call at `hotel_staff/services/hotel_staff_user.py:486`
  - `salesforce/services/salesforce_contact.py:40` `_user_is_legacy_admin`
  - Guards: `onboarding/views/onboarding_hotel_products.py:64`,
    `onboarding/views/preview_product_permissions.py:121`, `permissions/services/deactivation.py:35`,
    `permissions/services/activation.py:540`, `portfolios/services/portfolio.py:486`

  **Mark these (finished migration tooling).**
  - `permissions/services/activation.py`: `activate_new_permissions` past the early return at `:216`,
    `_create_roles_by_permission` (`:146`), `_some_hotel_user_has_legacy_permission` (`:108`)
  - Commands, one comment at module top: `permissions/management/commands/turn_on_permissions.py`,
    `turn_on_permissions_bulk.py`, `migrate_esa_to_new_permissions.py`,
    `hotels/management/commands/migrate_esa_hotels_to_authv2.py`
  - `internal/services/migration_progress.py:62` `record_granular_permissions_progress`

  **Mark these (frontend).**
  - `hotels/src/checkIns/CheckInModal/CheckInModal.vue:118-123` `isAdmin`, `hasViewCCPermission`
  - `hotels/src/checkIns/CheckInModal/CheckInCreditCard.vue:64` `hasViewCCPermission`
  - `hotels/src/checkOuts/CheckOutModal/CheckOutModal.vue:88` `isAdmin`
  - `adminland/src/userStore.ts:41-63` `adminUsers` query
  - Enum members `CAN_USE_AMENITIES`, `CAN_USE_CONTRACTS`, `CAN_USE_AUTHORIZATIONS`,
    `CAN_REFUND_PAYMENTS` in `packages/shared/schemas/canary/User.ts` and in
    `hotels/utils/api/serialize_user.py`

  **Do NOT mark: live Django permissions for Canary staff.**
  - `canary_staff/services/canary_staff_service.py` (sets Django perms from Google groups)
  - `frontend/manage/**` nav gates, and the 3 staff codenames `view_cohort`, `view_cohorthotel`,
    `staff_delete_purchaseorder` in both `LegacyPermission` enums. Add a one-line comment there
    saying these three are live staff permissions, since the enum name says otherwise.
  - Staff/admin checks: `impersonation.*`, `onboarding.*` cohort and script views,
    `internal_support.*`, `hotels.has_admin_rest_api` (MCP and REST), `tips.change_configuration`,
    `check_in.can_generate_chargeback_report*`, `auth.can_write_to_readonly_fields`,
    `hotels.can_bypass_mfa`, `hotels.change_hotel`, `canary/access_control/gatekeepers.py`,
    `onboarding/validators/is_staff_with_permission.py`, Django admin

  **Do NOT mark: legacy but reachable (needs migration, separate work).**
  - UI `hotel_admin` gates: delete check-in/check-out, contract countersign, `HeaderDelinquent`,
    `ProfileMenu`; `AdminSidebar.vue` `permission=hotel_admin` query
  - `LegacyPermissionMappingService` and its SSO call; `serialize_user` `permissions` field;
    `set_permissions_for_user` and `UserAPIView.post`
  - `permission_required(HOTEL_ADMIN)` in `payment_links/views/*` and `pms_gateway/views/validation.py`;
    `hotels/views/api/auth.py:14`; `amenities/api_views.py:416`; `authorization/models/models.py:532`;
    `canary/canary_products.py:84-86`; `hotels/views/views.py:655,1177`; `hotels/emails.py:20-26`;
    `reports/fs_report.py`, `reports/user_report.py`; `rest/views/users.py`;
    `internal/views/chargeback_report.py`; `demos/views`; `internal/views/views.py`;
    `onboarding/views/common.py`; `amadeus/services/amadeus.py:1121`; `hotels/templates/header-admin.html`

  **Also in this PR (my addition, drop if unwanted).** Replace the stale "currently being rolled out"
  warning in `docs/django/permissions.md` with three lines: hotel users use role-based permissions
  only; Django permissions are for Canary staff only; what the marker means.

  **Done when.** Every location above carries the marker, nothing in the two do-not-mark lists does,
  and the diff contains comments and the doc change only.

  ### Ticket B: Delete dead legacy-permission reads from the frontend

  - Delete the unread computeds in `CheckInModal.vue`, `CheckInCreditCard.vue`, `CheckOutModal.vue`
    and their `LegacyPermission` imports.
  - Delete the `adminUsers` query from `adminland/src/userStore.ts`, including the await in
    `initialize`. This removes one users request per adminland load; check the store spec.
  - Remove the 4 unread members from the frontend `LegacyPermission` enum, plus `VIEW_CC` once its
    last (dead) reader is gone.
  - Out of scope: the live `hotel_admin` gates and the manage app.
  - Verify: `pnpm typecheck`, `pnpm lint`, vitest for the touched apps.

  ### Ticket C: Remove unreachable legacy branches and guards not covered by ENT-5669 / ENT-5670

  - `hotels/services/hotel.py:410` `get_admins` else branch
  - `chat/services/message_escalation.py:461` and `hotels/views/api/user/user.py:153` SSO non-attached branches
  - `PermissionService.user_exists_on_hotel_with_legacy_permission` and its caller in `hotel_staff_user.py:486`
  - Never-firing guards in `onboarding_hotel_products.py:64`, `preview_product_permissions.py:121`,
    `activation.py:540`, `portfolios/services/portfolio.py:486`, with the exception classes
    `HotelNotOnGranularPermissionsError` and `CannotRemoveHotelWithoutGranularPermissionsFromPortfolio`
    if nothing else raises them
  - `best_western_roles_and_permissions_provider.py:40` dead branch
  - `mobile_key/verification/pa_130`, `pa_257`, `pa_298` setups: stop creating hotels with the flag False
  - Alternative: fold these into ENT-5669 and ENT-5670 instead of a new ticket. They are 2 points
    each today and this would roughly double them.

  ### Ticket D: Stop serializing unused legacy permission data

  - Trim backend `LegacyPermission` in `serialize_user.py` to the codenames the UI still reads
    (`hotel_admin` plus the 3 staff codenames).
  - Remove `has_new_permissions_only` and `rollout_adminland_role_based_permissions_ui` from
    `serialize_hotel.py:226-227` (this is the remaining part of ENT-5671; close ENT-5671 against it).
  - `HotelEmbed.permissions` (`serialize_hotel_embedded_in_user.py:12-18`): I found no frontend
    reader, but the search was narrow. Verify, then remove.
  - Check `portfolios/views/portfolio_hotels.py:54-132`, which also serializes the flag.
  - Regenerate OpenAPI if a Request Framework v2 view changes shape.

  ### Ticket E: Deprecate the two Hotel flag fields

  - Last in the series. `backend:deprecate_field` 3-PR flow, migration in its own PR.
  - Remaining references by then: `Hotel.CONFIG_FIELDS` (`hotels/models/hotel.py:287,303`), onboarding
    config providers (aimbridge, buffalo, crestline, marriott, mvw, pyramid, raymond, stonebridge),
    `ActivationService.turn_on_permissions_settings` and its 4 live callers, `hotels/agent_context/schemas.py`,
    `rules_based_configuration/services/conformity.pyi`, `canary_mcp/sql_grants`, fixtures,
    `MigrationType.GRANULAR_PERMISSIONS`.
  - `rules_based_configuration/` is pod-enterprise CODEOWNERS territory.
  - This replaces step 4 of ENT-5590.

  ### Decisions for Gareth

  1. Create A, B, C, D, E in Linear as drafted? (C could instead be folded into ENT-5669 / ENT-5670.)
  2. Move ENT-5590 into this project and strip its step 4?
  3. Keep the `docs/django/permissions.md` change inside ticket A?

  ## Agent run 2026-10-02T13:31:30Z: tickets created in Linear

  Follow-up asked: "I approve the ticket plan. Proceed"

  Read as yes to all three decisions above: create A to E as drafted (C as its own ticket), move
  ENT-5590 and strip its step 4, keep the docs change in ticket A. **All Linear writes below are done.**
  No code was changed, nothing was run against any environment.

  ### Created (ENT team, project "Clean up legacy permissions", Todo, Low, unassigned, no estimate)

  | Plan | Ticket | Blocked by |
  | --- | --- | --- |
  | A | ENT-7745 Mark dead legacy-permission code with a `DEAD-LEGACY-PERMISSIONS` comment (https://linear.app/canary-technologies/issue/ENT-7745/mark-dead-legacy-permission-code-with-a-dead-legacy-permissions) | prod flag check (no ticket) |
  | B | ENT-7746 Delete dead legacy-permission reads from the frontend (https://linear.app/canary-technologies/issue/ENT-7746/delete-dead-legacy-permission-reads-from-the-frontend) | ENT-7745 |
  | C | ENT-7747 Remove unreachable legacy branches and guards not covered by ENT-5669 / ENT-5670 (https://linear.app/canary-technologies/issue/ENT-7747/remove-unreachable-legacy-branches-and-guards-not-covered-by-ent-5669) | ENT-7745 |
  | D | ENT-7748 Stop serializing unused legacy permission data (https://linear.app/canary-technologies/issue/ENT-7748/stop-serializing-unused-legacy-permission-data) | ENT-7746; related to ENT-5671 |
  | E | ENT-7749 Deprecate `has_new_permissions_only` and `rollout_adminland_role_based_permissions_ui` (https://linear.app/canary-technologies/issue/ENT-7749/deprecate-has-new-permissions-only-and-rollout-adminland-role-based) | ENT-7746, ENT-7747, ENT-7748, ENT-5669, ENT-5670, ENT-5590, ENT-5672 |

  Project: https://linear.app/canary-technologies/project/clean-up-legacy-permissions-02fd9c30122f

  ### Edited existing tickets

  - ENT-5669 (https://linear.app/canary-technologies/issue/ENT-5669/remove-has-new-permissions-only-from-views):
    blocked by ENT-7745. Line refs refreshed: `credit_card.py` 138-154 -> 118-134, `views.py` 1109-1148 -> 1415-1458,
    `user.py` now names `:185` and hands the `:153` branch to ENT-7747.
  - ENT-5670 (https://linear.app/canary-technologies/issue/ENT-5670/remove-has-new-permissions-only-from-remaining-services):
    blocked by ENT-7745. Line refs refreshed: `contract.py` 1036 -> 1093, `activation.py` 214 -> 216,
    `manual_user_merge.py` 371 -> 376, `salesforce_contact.py` now 40-45.
  - ENT-5672 (https://linear.app/canary-technologies/issue/ENT-5672/remove-has-new-permissions-only-from-test-helpers-and-test-files):
    blocked by ENT-5669, ENT-5670, ENT-7747. Description untouched.
  - ENT-5590 (https://linear.app/canary-technologies/issue/ENT-5590/deprecate-permissions-activation-service):
    moved from "Eng Improvements" to "Clean up legacy permissions", blocked by ENT-7747. Step 4 replaced by a
    pointer to ENT-7749; the risk note now points at ENT-5672 and ENT-7749 instead of "step 4". Still Backlog,
    labels kept. The move drops its old "Clean up" milestone, which belonged to "Eng Improvements".

  ### Changes from the draft text

  Line refs were re-checked against master 09dcddac88c (unchanged since the draft) before creating. All held. Fixes:
  - E: `MigrationType.GRANULAR_PERMISSIONS` does not exist. The real name is
    `MigrationProgressService.MigrationName.GRANULAR_PERMISSIONS` (`internal/services/migration_progress.py:20`).
  - E: added flag references the draft missed: `onboarding/services/vendor/marriott_tipping_onboarding_service.py`,
    `permissions/management/commands/dev_set_up_permissions_scenarios.py`,
    `addons/management/commands/load_in_stay_fixtures.py`,
    `onboarding/management/commands/onetime_nightly_upsells_flag.py`. Named the 4 live callers of
    `turn_on_permissions_settings`.
  - B: also removes `adminUsers` from the store type (`userStore.ts:26`) and return value (`:109`).
    Test commands are `make check-fix` and `pnpm exec vitest run` rather than `pnpm typecheck` / `pnpm lint`.
  - C: confirmed both exception classes are raised only by the guards being removed.
  - D: confirmed the frontend has 0 references to either flag.

  ### Not done, needs Gareth

  1. **ENT-5671 is still open in Todo**
     (https://linear.app/canary-technologies/issue/ENT-5671/remove-has-new-permissions-only-from-serialization-frontend).
     Its frontend half shipped in PR #43419 (https://github.com/canary-technologies-corp/canary/pull/43419) and
     ENT-7748 covers its one remaining backend line. I linked the two as related and left its status alone,
     because closing it was not one of the three decisions. Suggest marking it duplicate of ENT-7748.
  2. **Prod flag check for ENT-7745 is not run.** The precondition (no hotel with either flag False, every region)
     is in the ticket. I did not query prod or Snowflake.
  3. **No estimates** on the 5 new tickets. Siblings carry 2 or 4 points.
  4. New tickets went straight to Todo to match the 4 existing tickets in the project, skipping Triage.
     Move them to Backlog if Todo means "committed" on ENT.
  5. Still no ticket for migrating the live `hotel_admin` UI gates (delete check-in/check-out, countersign,
     `HeaderDelinquent`, `ProfileMenu`) to role-based permissions. That was the gap from run 1 and is outside
     this dead-code series. It needs a product call on which permission replaces each gate.

  ### Housekeeping

  - This item was already in `archive/` with `completed_at` set when I started (archived 16:26:10 local, the
    launch prompt pointed at `next/`). I wrote here and did not move it. `working_on` was already false.
  - Cosmetic: ENT-7748 shows the PR #43419 link twice in one sentence (Linear auto-linked both the number and the URL).
project: 2026-04-16T1351-ship
source_id: null
tags: []
time_minutes: 5
title: Check whether old permissions code has been fully removed from UI in particular
updated: 2026-10-02 16:31:30.000000
waiting_on: null
waiting_since: null
working_on: false
---

Based on Django built-in permissions