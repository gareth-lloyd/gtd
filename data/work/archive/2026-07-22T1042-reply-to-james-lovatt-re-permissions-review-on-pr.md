---
area: null
contexts:
- react
created: 2026-07-22 10:42:23.375314
defer_until: null
due: null
energy: medium
id: 2026-07-22T1042-reply-to-james-lovatt-re-permissions-review-on-pr
order: null
output: "## Agent run 2026-07-22T13:12 — Permissions review of PR #50441\n\nPR: MOB-1005
  \"add the service tickets section to the role editor\"\nhttps://github.com/canary-technologies-corp/canary/pull/50441\nAuthor:
  James Lovatt (jmslovatt) · state: OPEN · base: master\nDepends on #50416 (MOB-997,
  MERGED 2026-07-16):\nhttps://github.com/canary-technologies-corp/canary/pull/50416\n\n###
  Verdict\nApprovable from a permissions standpoint. The 6 `service_tickets_*` codenames\nin
  the frontend `Permission.ts` mirror the backend enum EXACTLY (verified\nagainst
  origin/master `backend/canary/permissions/constants/permission.py`),\nand the real
  enforcement/security boundary lives server-side and already\nlanded in #50416 —
  this PR is frontend surfacing + one serialize line, so it\ngrants nothing on its
  own. Gareth is a fine reviewer here (small, mostly\nmechanical); no need to route
  elsewhere. One substantive nuance to flag +\na minor test-coverage gap. Nothing
  blocking.\n\n### What I verified\n- Codename parity: FE enum values == BE codenames
  for all 6\n  (has_product_access, can_create_tickets, can_be_assigned,\n  can_bypass_auto_assignment,
  can_assign_tickets, can_manage_tickets). No typos\n  / no FE↔BE drift.\n- Enforcement
  is real: backend perms + product registration exist on\n  origin/master (`permission.py`,
  `default_role.py`). FE gating is UX only,\n  which is correct — the security check
  is server-side.\n- Kill-switch: every surface hides behind `hotel.has_service_tickets`,
  which\n  defaults false for all hotels, so zero live blast radius. `ROLLOUT_TASK_MANAGEMENT`\n
  \ is correctly dropped from adminland (last consumer tracked in MOB-885).\n- Default
  roles: PROPERTY_MANAGER holds all 6 incl. CAN_MANAGE_TICKETS;\n  PROPERTY_STAFF
  holds only product-access/create/be-assigned (NOT manage).\n  So the tightening
  claim in the PR body is accurate.\n\n### The one thing worth raising (sidebar vs
  route gating asymmetry)\nThe sidebar item and settings page are now gated on\n`SERVICE_TICKETS_CAN_MANAGE_TICKETS`,
  but the two gates disagree in strictness:\n- Sidebar (`AdminSidebar.vue`) uses `useUserAccessLevelToSettings(...,
  allowReadOnly:false)`\n  → STRICT: only manage-perm holders see it. PROPERTY_STAFF
  is hidden.\n- Route guard `canUseProduct` (`products.ts`) still has the\n  `userHasViewOnlyPermissions
  = PLATFORM_CAN_VIEW_GENERAL_SETTINGS` OR-branch,\n  which is NOT disabled. So a
  PROPERTY_STAFF user (who holds\n  PLATFORM_CAN_VIEW_GENERAL_SETTINGS) at a service-tickets-enabled
  hotel would\n  pass `canUseProduct` and could reach the page by direct URL —\n  `ServiceTicketsPage.vue`
  only re-checks `hotel.has_service_tickets`, not the perm.\nNet: sidebar hides it
  from read-only staff, but the route stays reachable for\nthem. This is the platform-wide
  \"read-only admins can view any settings page\"\npattern, so it may be intended
  — but the sidebar's `allowReadOnly:false`\nsignals the opposite intent for this
  product. Worth James confirming which he\nwants; if \"manage-only, full stop,\"
  the route guard doesn't enforce it. Not a\nnew hole this PR introduces (the OR-branch
  is pre-existing), and backend\nenforces write actions regardless (#50416).\n\n###
  Minor: test coverage gap\n`products.test.ts` rewrite dropped the assertion for the\nPLATFORM_CAN_VIEW_GENERAL_SETTINGS
  path. New test covers manage-perm +\nproduct-available combos but not the view-only
  escape hatch above — so the\nasymmetry is invisible in tests. A one-line assertion
  for\n`canUseProduct([PLATFORM_CAN_VIEW_GENERAL_SETTINGS], [\"service_tickets\"],
  SERVICE_TICKETS)`\nwould document the intended behavior either way.\n\n### Fine
  as-is\n- `PERMISSIONS_BY_PRODUCT_ACCESS` tree (parent + 5 children) matches the\n
  \ convention of the other products; exhaustiveness invariant is type-enforced.\n-
  i18n: English source strings only, 42-locale + manifest churn is generated\n  (correct
  — not hand-edited).\n- `serialize_hotel.py` one-liner + tests are correct.\n- No
  migration/backfill; rollout impact section is accurate.\n\n### Draft Slack reply
  to James (NOT SENT — awaiting Gareth's go-ahead)\nDM thread: https://canarytechnologies.slack.com/archives/D0B1X0GJQSZ/p1784652402755059\n---\nHad
  a look — from a perms angle this is good to go. The 6 service_tickets_*\ncodenames
  match the backend enum exactly and the real enforcement is server-side\nfrom #50416,
  so the FE change grants nothing on its own and has_service_tickets\n(false everywhere)
  is a clean kill-switch. \U0001F44D\n\nOne thing to sanity-check, not blocking: the
  sidebar hides Service Tickets from\nread-only staff (allowReadOnly:false → manage-perm
  only), but canUseProduct still\nhas the PLATFORM_CAN_VIEW_GENERAL_SETTINGS view-only
  OR-branch, so a read-only\nadmin at an enabled hotel could still reach the settings
  page by direct URL. It's\nthe same view-only pattern every other product uses, so
  probably intended — just\nflagging because your sidebar gate is stricter than your
  route gate. If you want\n\"manage-only, period,\" the route guard won't give you
  that today. Either way I'd\nadd the one dropped assertion back to products.test.ts
  to pin the intent.\n\nHappy to drop these as PR comments if useful — LMK.\n---\n"
project: null
source_id: https://canarytechnologies.slack.com/archives/D0B1X0GJQSZ/p1784652402755059
tags:
- morning-gtd
- slack
time_minutes: 20
title: 'Reply to James Lovatt re: permissions review on PR #50441'
updated: 2026-07-22 15:19:32.407374
waiting_on: null
waiting_since: null
working_on: false
---

DM (Jul 21): "you wrote the perms doc, could you have a quick gander at this, or point me to the right person?" — also pinged Jul 16 re PR #50416, same perms topic.
https://canarytechnologies.slack.com/archives/D0B1X0GJQSZ/p1784652402755059

Review the attached PR