---
area: null
completed_at: 2026-09-22 13:49:25.161997
contexts:
- react
created: 2026-09-22 09:50:30.837267
defer_until: null
due: 2026-09-22
energy: medium
id: 2026-09-22T0950-review-pr-57237-ent-7557-give-epd-department-admin
order: null
output: |
  ## Agent run 2026-09-22 10:21:13.403923

  **Verdict: approve with two asks.** One-line, low-risk permission grant; Blake already approved the EPD change. Nothing blocks merge, but the PR may be solving a narrower problem than Mike has.

  PR: https://github.com/canary-technologies-corp/canary/pull/57237 (abrad, `abradshaw/ENT-7557/epd-department-permissions`)
  Ticket: https://linear.app/canary-technologies/issue/ENT-7557

  ### What it does
  Adds `hotels.department: view/change/add/delete` to `_EPD_PERMISSION_SET_MODEL_GRANTS` (`backend/canary/canary_staff/services/canary_staff_service.py:393`). Sales Engineering inherits the same map, so they get it too.

  ### Risk assessment (low)
  - **CS and Support already have full CRUD on `hotels.department`** (same file, lines 124 and ~1102). EPD getting it is not a new class of access; Macroscope's "human_required / overgrant" flag is overstated.
  - **Delete is mostly PROTECTed, not cascading.** `HotelUserProfile`, `Allocation`, `DepartmentDisbursement`, `TipIntent` all FK to Department with `on_delete=PROTECT`, so admin refuses to delete any department with staff, allocations or tip history. Only `TipLink.department` (OneToOne) cascades and `HotelWalletProfile` SET_NULLs. The PR caveat "delete cascades to related tipping data" is inaccurate in the safe direction; worth a one-line correction in the PR body.
  - **Permissions are additive at login and never revoked** — known property of this map, not specific to this PR.
  - **No test change.** `test_canary_staff_service.py` has a parametrized EPD/SE grants test (line 42); adding `hotels.department` to its expected dict would be cheap. Nice-to-have, not blocking.
  - CI: two Playwright critical failures (additional-guest check-in flows) are unrelated to a permissions-map change.

  ### Ask 1: is `hotels.Department` the right model? (unresolved)
  There are two department models:
  - `hotels.Department` — tipping/staff departments, has Django admin (`DepartmentAdmin` + inline on Hotel admin). This is what the PR grants.
  - `task_management.HotelDepartment` — roles-based departments for the staff-ops ticketing/housekeeping products (`backend/canary/task_management/models/hotel_department.py`), with its own API (`api/task_management/<hotel>/departments`), `seed_departments` and `manage_department` management commands, and **no Django admin at all**.

  Andrea asked Mike exactly this on Linear (2026-09-21) and Mike didn't answer which model; he said "James [Lovatt] helped me update the departments directly yesterday". Ticket types in the ticketing product carry a `department_uuid` (`frontend/packages/shared/schemas/taskManagement/TicketType.ts`) but I could not find in the repo which model that UUID resolves against; the staff assignment endpoint (`hotel_staff/views/assignable_departments.py`) uses `hotels.Department`. If the pilot's departments are `HotelDepartment`, this PR gives Mike nothing useful and the actual fix is a `manage_department` recipe. Suggest confirming with James/Mike before merge, or just merging (harmless either way) and following up.

  ### Ask 2: usability gotcha for Mike
  `DepartmentAdmin.readonly_fields` includes `hotel` (`backend/canary/hotels/admin/department.py:37`), so the standalone "Add department" form cannot set the hotel and will fail on save. Departments must be added via the collapsed **Departments inline on the Hotel admin page**. Put that in the PR body / handoff note to Mike, or he'll file a "permission doesn't work" ticket.

  ### Process point (Andrea's 100-property concern)
  Agree with Andrea. For `hotels.Department` there is already `hotels.services.department.DepartmentService` used by the onboarding configuration providers (marriott/crestline/raymond/stonebridge `*_department_provider.py`), so a brand-level department config + provider is the repeatable path. For `HotelDepartment` the `seed_departments` command already does the pilot's standard set (Front desk, Housekeeping, Engineering, Valet). Either way the admin grant is a stopgap; a follow-up ticket for the scripted rollout is worth opening.

  ### Not verified
  - Couldn't check prod admin LogEntry to see which model James edited (Teleport session expired; canary-mcp-* servers didn't connect).
  - The PR caveat about a "ticket-type catalog seed matching English names (Banquets, Engineering, F&B, Front Desk, Housekeeping, IT, Security)" doesn't correspond to anything in this repo; `seed_departments` uses a different list. May live in the ticketing microservice. Ask Andrea where that came from.

  No comments posted anywhere; nothing written to GitHub/Linear.
project: 2026-04-16T1210-unblock-team
source_id: https://github.com/canary-technologies-corp/canary/pull/57237
tags:
- morning-gtd
- github
time_minutes: 20
title: 'Review PR #57237: [ENT-7557] Give EPD department admin permissions'
updated: 2026-09-22 13:49:25.161983
waiting_on: null
waiting_since: null
working_on: false
---

Author abrad, branch abradshaw/ENT-7557/epd-department-permissions. Personally requested. Context: product (Mike Hu) needs to add departments for staff-ops ticketing pilot hotels; Andrea wants a process if 100 properties get configured.
https://github.com/canary-technologies-corp/canary/pull/57237