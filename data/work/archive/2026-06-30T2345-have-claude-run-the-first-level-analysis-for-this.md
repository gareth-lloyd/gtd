---
area: null
contexts: []
created: 2026-06-30 23:45:00.384854
defer_until: null
due: null
energy: low
id: 2026-06-30T2345-have-claude-run-the-first-level-analysis-for-this
order: null
output: |
  ## Agent run 2026-07-01T12:36:30Z — First-level analysis: is_staff-only endpoints

  Source thread: https://canarytechnologies.slack.com/archives/C0AJJ518YMQ/p1782755394220549
  Trigger ticket: TOOL-285 (https://linear.app/canary-technologies/issue/TOOL-285) — adding
  ACCOUNT_EXECUTIVES to GROUPS_WITH_STAFF_ACCESS would grant them every is_staff-only endpoint.

  ### TL;DR
  Confirmed the problem. ~14 internal Google Groups already hold `is_staff`
  (GROUPS_WITH_STAFF_ACCESS in canary_staff/services/canary_staff_service.py). A large set of
  endpoints treat `is_staff` as the ONLY authz gate — including payment-capable ones. Adding AEs
  widens that blast radius. Good news from the Groundcover survey: a meaningful chunk of these
  endpoints are cold (near-zero traffic) and are delete/lock-down candidates rather than
  narrow-the-permission work.

  ### The four is_staff-only mechanisms (what to grep for)
  1. `StaffUserGatekeeper()` with NO `staff_permissions` — Request Framework v2
     (canary/access_control/gatekeepers.py). If `staff_permissions=[...]` is set it is NOT
     is_staff-only (that's the fix pattern).
  2. `@validate_request(auth=IsStaffValidator)` — legacy (canary/access_control/auth_validator.py).
  3. `ensure_user_is_staff` decorator / `DEFAULT_DECORATORS_STAFF` (canary/decorators_api.py,
     hotels/constants.py).
  4. `StaffRequiredMixin` (and `CompanyManagementPermission` = company_admin OR is_staff) —
     canary/mixins.py.

  ### Endpoint inventory by owning app (is_staff-ONLY only) + Groundcover usage
  Usage = Groundcover Datadog-tracer spans on `workload:django`, weekday window 2026-06-24→27
  (3 days) unless noted. Traces are SAMPLED and retention is only ~20 days, so treat these as an
  order-of-magnitude "hot vs cold" signal, not exact call counts.

  | Owning app / group | ~#endpoints | Mechanism | 3-day usage | Bucket |
  |---|---|---|---|---|
  | payment_gateways — payment_intents create/cancel/reverse | ~5 | IsStaff + ensure_staff | 37,834 | HOT — can create/cancel/reverse charges. Narrow, do NOT delete |
  | kiosk — onboarding (kiosk_api/onboarding/*) | ~20 | IsStaffValidator | 39,481 | HOT |
  | internal_support (api/internal_support/*) incl AI tools | ~21 | IsStaffValidator | 26,859 (AI subset 725) | HOT |
  | tips — canary_staff qr/branding (api/qrcode*, api/staff/hotels/*) | ~4-6 | DEFAULT_DECORATORS_STAFF | 1,950 | WARM |
  | kiosk — configurator (kiosk_api/configurator/*) | ~4 | IsStaffValidator | 502 | WARM |
  | onboarding — staff pages (hotels, onboardings, salesforce, scheduled_trainings, staff-users, demo-hotels) | ~9 | StaffRequiredMixin + IsStaff | 376 | WARM |
  | guest — reservation search (api/hotels/<slug>/reservations/search) | 1-2 | StaffUserGatekeeper() | 334 | WARM |
  | voice — admin (api/voice/admin/*) | ~6-7 | ensure_user_is_staff | 69 | WARM (light) |
  | front_desk — workbench (api/front_desk/workbench/*) | 10 | StaffUserGatekeeper() | 0 | COLD ⚠️ PAYMENT-CAPABLE (terminal charge/capture, take_payment) — confirm live before treating as dead |
  | shops (/shops/*) | ~12 | IsStaffValidator | 0 | COLD — likely pre-launch |
  | payment_gateways — surcharge-policies + shiji_user_login | ~5 | IsStaff | 0 | COLD |
  | linear_agent — issues (api/linear-agent/issues*) | 3 | IsStaffValidator | 2 | COLD (the 18k of /api/linear-agent/ traffic is all oauth/webhook, not these) |
  | internal — migration_progress dashboard (+api) | 2 | ensure_user_is_staff | 1 | COLD |
  | hotels — reservation-message-status | 1 | StaffUserGatekeeper() | not measured (query kept timing out) | low priority |

  Rough total is_staff-ONLY: ~100-110 endpoints across 11 apps — consistent with the "138" in
  the thread (that count also swept in the already-protected + admin-autocomplete routes below).

  ### Already-protected — these are the REMEDIATION MODEL, not part of the problem
  These use the same staff surface but correctly add a Django permission on top. Copy this pattern:
  - infra_self_service/views/self_service_request.py — `StaffUserGatekeeper(staff_permissions=[...])`
  - monitoring/views/monitored_hotel_states.py — `StaffUserGatekeeper(staff_permissions=[_REQUIRED_PERMISSION])`
  - onboarding cohorts/cohort/cohort_hotel(s)/onboarding_script_*/plan_choices/onboarding_value —
    `ensure_user_is_staff` + `permission_required("onboarding.view_*")` (so most of the onboarding
    app is already fine; only the staff-pages row above is bare is_staff)
  - internal_support/views/support_access_grant.py — StaffUserGatekeeper() but calls `_require_perm()`
    in-handler, so effectively permissioned (grant-approval flow)

  ### Recommended first cut of the work (matches Gareth's "break into blocks" + "survey for unused")
  1. DELETE / hard-lock the COLD blocks first — biggest risk reduction per effort, no product impact:
     - front_desk/workbench/* (⚠️ payment-capable, 0 traffic — CONFIRM the workbench feature is
       actually rolled out; if not live, delete or gate behind a real permission now)
     - shops/* (0 traffic — pre-launch; add a `shops.*` permission before it ships)
     - payment_gateways surcharge-policies + shiji_user_login (0)
     - linear_agent/issues (2), internal/migration_progress (1)
  2. NARROW the HOT payment surface next — payment_gateways payment_intents create/cancel/reverse.
     These are is_staff-only AND high-volume AND can move money. Add a Payments permission
     (view/charge) using the infra_self_service pattern; owner = Payments team.
  3. Then the HOT internal-tools surfaces (kiosk onboarding/configurator, internal_support) — owned
     by their respective teams (Kiosk, Internal Tools/Support), ENT coordinating per the thread.
  4. Ownership: per Gareth in-thread, the team that makes/uses each endpoint owns the narrowing;
     ENT coordinates and tracks. Suggest one parent Linear epic + per-app child tickets seeded from
     the table above.

  ### Methodology / caveats (for whoever picks this up)
  - Grep the four mechanisms above; exclude tests/tmp; for each hit check it doesn't ALSO layer a
    permission (staff_permissions=, permission_required(), in-handler has_perm/_require_perm).
  - Usage source: Groundcover tenant `canary`, `query_traces`, field `resource` = "METHOD /path".
    `resource` carries concrete IDs/slugs so match by path PREFIX. Trace queries time out beyond
    ~3 days and retention is ~20 days — for a defensible delete decision, re-confirm each COLD
    endpoint over a longer window in Datadog directly (longer retention, same spans) before removing.
  - Weekend windows under-count staff tools badly (internal_support/ai read 0 on a weekend, 725 on
    weekdays) — always use a weekday window.

  ### Not done (needs human decision — I did not touch any external service)
  - Did NOT post to the Slack thread or Linear. Happy to draft a thread reply summarizing the
    hot/cold split + proposed epic structure, or open the parent Linear ticket, on your say-so.
  - front_desk/workbench "is it live?" needs a product/eng confirm before it's called dead.

  ### Posted (user-approved 2026-07-01)
  - High-level categorized summary posted to the Slack thread:
    https://canarytechnologies.slack.com/archives/C0AJJ518YMQ/p1782910340889939?thread_ts=1782755394.220549
  - Per-category endpoint breakdown (code block) posted to the thread:
    https://canarytechnologies.slack.com/archives/C0AJJ518YMQ/p1782910529903039?thread_ts=1782755394.220549

  ### Code-age signal on COLD endpoints (git, as of 2026-07-01) — refines delete vs keep
  COLD + NEW (not dead, just pre-ramp → keep & gate, do NOT delete):
  - front_desk/workbench: added 2026-06-10 (3 wks), active build (KSK-5706 server-side Stripe
    terminal). ⚠ payment-capable — gate before rollout.
  - pg surcharge-policies: added 2026-02-10, last 2026-06-16 (SDM-4506). Recent, low adoption.
  COLD + OLD/STALE (strong delete/archive candidates):
  - shops: added 2025-09-08, untouched ~9mo (last commit "deprecates hotel from shops").
  - internal migration dashboard: added 2024-12-19, no functional change ~18mo.
  - pg shiji_user_login: added 2025-07-15, single commit, untouched ~11.5mo.
  - hotels reservation-message-status: added 2025-08-20, only change since is RF-v2 plumbing.
  COLD + MID (owner check, then gate/delete):
  - linear_agent/issues: added 2026-03-16, single commit, untouched ~3.5mo (internal tool).
  Net: age flips front_desk/workbench + surcharge-policies OUT of the delete pile (new/active);
  hardens shops, internal migration dashboard, shiji_user_login, reservation-message-status as
  abandoned-code deletes.
  - Code-age signal (code block) posted to the thread:
    https://canarytechnologies.slack.com/archives/C0AJJ518YMQ/p1782910717462089?thread_ts=1782755394.220549
project: null
source_id: null
tags: []
time_minutes: 5
title: Have claude run the first level analysis for this security is_staff ticket
updated: 2026-07-01 16:13:29.059053
waiting_on: null
waiting_since: null
working_on: false
---

https://canarytechnologies.slack.com/archives/C0AJJ518YMQ/p1782755394220549

/debug_in_shell

Use groundcover or datadog to check whether endpoints actually in use