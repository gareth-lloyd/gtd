---
area: null
completed_at: 2026-11-06 16:31:17.399014
contexts: []
created: 2026-11-04 22:06:29.656035
defer_until: null
due: 2026-11-09
energy: low
id: 2026-11-04T2206-clean-up-perms-legacy-project-and-share-with-andre
order: null
output: |
  ## Agent run 2026-11-05T18:10 (Europe/London)

  ### Where it is
  Project: Clean up legacy permissions, P-ENT-2487 (https://linear.app/canary-technologies/project/clean-up-legacy-permissions-02fd9c30122f)
  Lead Gareth, only member Gareth. Status "Eng Design", no description, no target date, no status update ever posted, no docs.
  10 tickets, all Todo, all unassigned, all Low priority, all last touched 2026-10-02 (refreshed against master 09dcddac88c).
  Predecessor P-ENT-938 "Migrate out of legacy permissions" (Montse) is Completed, so this is the only live perms-cleanup project.
  `git grep DEAD-LEGACY-PERMISSIONS` on master = 0 hits, so ENT-7745 (the first ticket) has not started.

  Context (1:1 with Andrea 2026-11-04, Granola https://notes.granola.ai/d/1160bdb0-7875-49d9-a352-0ffca010addb): you said you'd share the project link; Andrea said not urgent, nobody has touched that UI, good "between the holidays / early January" project, and she'll bring it up as an option at Monday (2026-11-09) planning if you send the link. Andrea and Connor are separately brainstorming the bigger permissions/identity ownership question; she initially conflated the two, so the share should say this is dead-code deletion, not the roles/identity vision.

  ### Ticket validity (checked against origin/master c9c057a37c1, 2026-11-05)
  All 10 are still valid. Every symbol named still exists. Line numbers have drifted in 4 tickets. Two tickets need text edits for work that landed since Oct 2.

  - ENT-7745 Mark dead code with DEAD-LEGACY-PERMISSIONS (https://linear.app/canary-technologies/issue/ENT-7745) — valid, not started. docs/django/permissions.md still has the stale "being rolled out" warning. Line refs drifted for hotels/services/hotel.py (get_admins now :391-394), hotel_staff_user.py, onboarding_hotel_products.py, portfolios/services/portfolio.py, and hotels/views/api/user/user.py (see ENT-7127 note). Precondition count (no hotel with either flag False) still unverified; SQL below.
  - ENT-5669 Views (https://linear.app/canary-technologies/issue/ENT-5669) — valid. credit_card.py:125, billing.py:65 exact. views.py ~:1441 close. Part (d) user.py is stale: ENT-7127 (#62668, merged 2026-11-04, Tincho) deleted 258 lines from user.py (DELETE+PATCH handlers). Remaining legacy code is now user.py:100-108 (SSO non-attached branch, flag check) and :129-130 ("TODO: remove legacy-permissions logic" routing conditional).
  - ENT-5670 Services (https://linear.app/canary-technologies/issue/ENT-5670) — valid, all 5 refs exact.
  - ENT-7747 Remaining branches/guards (https://linear.app/canary-technologies/issue/ENT-7747) — valid. user_exists_on_hotel_with_legacy_permission, both exception classes, both guards, BW provider :40, pa_130/257/298 setup all present. Same user.py drift as above (:153 is now :100-108).
  - ENT-7746 Frontend dead reads (https://linear.app/canary-technologies/issue/ENT-7746) — valid, all 4 refs exact (CheckInModal :118, CheckInCreditCard :64, CheckOutModal :88, userStore.ts :41). CAN_USE_* enum members still present.
  - ENT-7748 Stop serializing (https://linear.app/canary-technologies/issue/ENT-7748) — valid. serialize_hotel.py:225-226, embedded :10 TODO, portfolio_hotels.py:54 exact; serialize_user.py:36 drifted (enum moved). It explicitly says "Close ENT-5671 against this ticket" and that has not been done.
  - ENT-5671 Serialization + frontend (https://linear.app/canary-technologies/issue/ENT-5671) — STALE. Frontend half shipped in #43419 (ENT-4469); the backend line is absorbed by ENT-7748. Should be cancelled as duplicate of ENT-7748.
  - ENT-5590 Deprecate ActivationService (https://linear.app/canary-technologies/issue/ENT-5590) — valid with 2 fixes: onboarding/management/commands/backfill_wyndham_permissions_for_sso_users.py and reset_wyndham_permissions.py no longer exist (drop those rows). ENT-7126 (Tincho, Aug 2026, #52852) already neutralised migrate_esa_to_new_permissions so it cannot rerun; file still exists and still needs deleting. Labelled Tech Debt + Starter project.
  - ENT-5672 Tests (https://linear.app/canary-technologies/issue/ENT-5672) — valid but underestimated: 173 test/fixture files reference has_new_permissions_only, 23 set it False, and stub_hotel_without_granular_permissions (hotels/testing.py:277, docstring confirms legacy-only) is called from 162 files. Ticket says "~100+" and "remove if it exists solely for legacy testing"; it does, so that helper and its 162 call sites are the bulk of the work. 4 points is light.
  - ENT-7749 Drop the two fields (https://linear.app/canary-technologies/issue/ENT-7749) — valid. 48 non-test backend files still reference has_new_permissions_only, 22 reference rollout_adminland_role_based_permissions_ui (config providers, fixtures, MCP grants, rules_based_configuration/types/setting_keys.py which is pod-enterprise CODEOWNERS). Blocked by all 7 others, correctly.

  Nothing else outside the project overlaps: ENT-5352 (SSO provisioning, Feb 2026) and ENT-7127 are Done and complementary.

  ### What still needs doing (none of these were done; all need your OK since they are Linear writes)
  1. Cancel ENT-5671 as duplicate of ENT-7748.
  2. ENT-5590: delete the two Wyndham command rows; add a note that ENT-7126 neutralised migrate_esa_to_new_permissions (still delete it).
  3. ENT-5669 (d) and ENT-7747: replace the user.py:153/:185 refs with :100-108 and :129-130 and cite #62668.
  4. ENT-7745 / ENT-7747 / ENT-7748: refresh line numbers against current master, or drop them and keep symbol names (they drift monthly; symbols have been stable).
  5. Project: add a description (draft below), change status from Eng Design to Backlog (design is done; nobody is working it), set a target date (Andrea suggested between-holidays / early Jan), add Andrea as a member.
  6. Optional: ENT-5672 estimate up from 4; label ENT-7745 Starter project too (comments only, builds the worklist).
  7. Verify the ENT-7745 precondition yourself (Workup run_sql needs a run id, prod-db hotel reads get classifier-blocked from an agent, DIM_HOTEL has no permission columns). Per region:
     ! canary prod-db query canary "SELECT count(*) AS legacy_hotels FROM hotels_hotel WHERE has_new_permissions_only = false OR rollout_adminland_role_based_permissions_ui = false"

  ### Draft project description (for Linear, not saved)
  Hotel users are authorized by role-based permissions only (PermissionService, the Permission enum). The Django-permission paths for hotel users have been unreachable since migration 0670 (Sep 2025) set has_new_permissions_only and rollout_adminland_role_based_permissions_ui to True for every hotel, and "Migrate out of legacy permissions" (P-ENT-938) completed. The code is still in the tree next to live Django-permission code for Canary staff, and readers (LLMs especially) copy it. This project deletes the dead paths, the finished migration tooling, and finally the two flags.

  Order (blocking relations are set on the tickets):
  ENT-7745 marker PR, comments only, produces the worklist
  → ENT-5669, ENT-5670, ENT-7747, ENT-7746 deletions, can run in parallel
  → ENT-5590 activation service, ENT-7748 serialization, ENT-5672 test helpers
  → ENT-7749 drop the fields via the 3-PR deprecate flow.

  Not urgent. Mechanical, well suited to Claude with a human reviewing. Out of scope: hotel_admin gates that are legacy but reachable (need a product decision on the replacement permission) and Canary-staff Django permissions (live). Done when git grep DEAD-LEGACY-PERMISSIONS returns nothing and the two fields are gone.

  ### Draft Slack DM to Andrea (not sent)
  Here's the legacy permissions cleanup project I mentioned yesterday: https://linear.app/canary-technologies/project/clean-up-legacy-permissions-02fd9c30122f
  To be clear it's not the roles/identity-ownership question you and Connor are looking at. It's deleting hotel-user code paths that use the old Django permissions, unreachable since every hotel moved to role-based perms in Sep 2025. 10 tickets, all specced with file lists, blocking order set (ENT-7745 first, ENT-7749 last). Mostly mechanical, good Claude-plus-review work, so a fit for the between-holidays slot if someone volunteers Monday. Not urgent. Happy to walk whoever picks it up through it.

  Done: research only. No Linear, Slack, or code writes.

  ## Agent run 2026-11-05T18:25 (Europe/London), edits applied on your approval

  Linear writes done:
  - Project P-ENT-2487: description added (the draft above, plus a Scope and Done-when section), summary set, status Eng Design -> Backlog, target date Jan 2027 (month resolution). Membership cannot be set through the MCP, so Andrea is not yet a member; add her in the UI if you want her to see it in her project list.
  - ENT-5671: state Duplicate, duplicateOf ENT-7748.
  - ENT-5590: Wyndham command rows removed; migrate_esa row notes ENT-7126 (#52852); callers list trimmed to hotel.py:220, hyatt:22, BW:41; onboarding.py ref 772 -> 977.
  - ENT-5669: user.py part (d) rewritten for post-ENT-7127 state (:129-130 routing, :99-108 SSO branch to ENT-7747), views.py range 1417-1462, refresh line updated.
  - ENT-5670: manual_user_merge.py 376 -> 377, refresh line updated.
  - ENT-7745: label Starter project added; 8 line refs refreshed (hotel.py:414, views.py:1443-1462, user.py:99-108/:129-130, manual_user_merge:376, hotel_staff_user:523, onboarding_hotel_products:70, portfolio.py:575, canary_staff_service:1394).
  - ENT-7746: refresh line updated (all refs were still exact).
  - ENT-7747: 7 line refs refreshed (hotel.py:414, user.py:99-108, hotel_staff_user:523, onboarding_hotel_products:70 and :35, portfolio.py:575 and :61).
  - ENT-7748: serialize_user.py 36 -> 46, serialize_hotel.py 225-226, note that ENT-5671 is closed against it.
  - ENT-7749: hotel.py CONFIG_FIELDS 286,302; onboarding.py 669.
  - ENT-5672: estimate 4 -> 8; "Size check" section appended with the 173 / 23 / 162 file counts.
  All refreshed refs are against master c9c057a37c1 (2026-11-05).

  Not done: Slack DM to Andrea (draft above, not sent; you did not ask for it).

  Shell script for the ENT-7745 precondition: written via /debug_in_shell, copied to clipboard, and shown in the session. Run it in a prod shell per region (US, EU, AP); it is read-only. If every region prints 0 legacy hotels, ENT-7745 can start.

  ## Precondition result 2026-11-05 (one region, 24,316 hotels, so almost certainly US)

  Hotels with a legacy flag False: 0. MigrationProgress granular_permissions measured 2026-11-05: remaining=0, total=24315, 100%.
  The metric is recorded daily, so for EU and AP the stored MigrationProgress row is enough; no shell needed there unless you want belt and braces.
  Gareth confirmed the same holds in every region. Noted on ENT-7745's Precondition section (2026-11-05). ENT-7745 can start.
project: null
source_id: null
tags: []
time_minutes: 5
title: clean up perms legacy project and share with andrea
updated: 2026-11-06 16:31:17.399007
waiting_on: null
waiting_since: null
working_on: false
---

find in linear under ent team. 

view existing legacy permissions clean up tickets and check validity / relevance

SEe what else needs doing.