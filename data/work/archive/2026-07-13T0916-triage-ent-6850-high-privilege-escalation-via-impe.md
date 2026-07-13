---
area: null
contexts:
- react
created: 2026-07-13 09:16:05.929438
defer_until: null
due: null
energy: medium
id: 2026-07-13T0916-triage-ent-6850-high-privilege-escalation-via-impe
order: null
output: |
  ## Agent run 2026-07-13T12:05

  **Verdict: not a privilege escalation. The HIGH / CVSS 7.2 rating is not justified — recommend downgrade to Medium-at-most tech debt, and reroute out of ENT.**

  Ticket: https://linear.app/canary-technologies/issue/ENT-6850

  ### The code is exactly as described — but the threat model in the ticket is wrong

  The quoted branch in `backend/canary/canary/access_control/auth_validator.py:83-89` is real and unchanged. But the ticket's exploit sentence — "A regular user being impersonated by a staff member can open staff-only endpoints in a separate browser tab" — describes something that cannot happen. The impersonated regular user does not hold the session. The session, cookie and browser all belong to the **staff member**.

  Three things pin this down:

  1. `impersonation/views/impersonation.py` — the `impersonate` view is gated by `@login_required` + `@staff_member_required` + `@permission_required("impersonation.can_impersonate")`. Only a staff member can start an impersonation session. It also explicitly refuses to impersonate staff/superusers (`if user.is_superuser or user.is_staff: raise PermissionDenied`).
  2. `impersonation/middleware.py` — `ImpersonateMiddleware` only engages when `request.user.is_staff` **and** the session carries `impersonate_username`. It then sets `request.impersonator = <the session-authenticated staff user>` and swaps `request.user` to the impersonated user.
  3. Therefore `request.impersonator` is always the genuine, session-authenticated staff user. It is derived from Django's auth session and is **not client-controllable or spoofable**.

  So whoever opens that "separate browser tab" *is the staff member*. They already have `is_staff`; they could reach the same endpoints by simply not impersonating, or by hitting `/unimpersonate` first. No privilege boundary is crossed. CWE-269 does not apply — there is no lower-privileged principal that gains anything.

  ### The branch was deliberate, not an oversight

  `git log -S "impersonator.is_staff"` → commit `e453b627248`, "SUP-109: Fix auth validator to work after impersonation" (#29687, Laura DeWald, 2025-08-12). It was added to *fix* internal tooling that broke during impersonation. The middleware already skips `/canary-admin`, `/control-portfolio`, `/control-hotel` and `/impersonate`, so this branch exists specifically to let internal staff APIs served on normal paths keep working while a support agent is in "view as" mode. **Naively ripping it out (AC option 2, "deny staff-only access entirely during impersonation") would break internal support tooling.** The in-code TODO already names the correct fix: strip impersonation context for staff-only views.

  Existing tests already encode the current behaviour as *intended*: `backend/canary/canary/tests/test_access_control.py::TestIsStaffValidator::test_staff_impersonating_non_staff_passes_validation` asserts it passes, and `test_non_staff_impersonating_non_staff_fails_validation` asserts a non-staff impersonator is rejected. So the ticket's third AC ("add test verifying impersonated users cannot access staff endpoints") directly contradicts a test that is green on master today. That AC cannot be implemented as written without a product decision.

  ### What IS real (and worth keeping, at lower severity)

  Not escalation, but a genuine **confused-deputy / auth-clarity** smell: the gate passes on one identity (`request.impersonator`, staff) while the view body executes as a *different* identity (`request.user`, the non-staff hotel user). For the 56 call sites of `IsStaffValidator`, any staff-only endpoint that reads `request.user` for scoping or writes gets the impersonated user, not the staff actor. Two consequences worth a look:
  - **Audit attribution.** Actions on staff-only endpoints during impersonation are attributed to the impersonated hotel user. The middleware does set `_impersonated_by` / `_impersonating` precisely so audit logs can recover the real actor — so this may already be handled, but I did not verify the audit path end-to-end.
  - **Wrong-user scoping.** A staff endpoint assuming `request.user.is_staff` holds could make incorrect decisions. I did not audit all 56 call sites for this.

  ### Recommendation

  - **Severity:** downgrade from HIGH. This is not a vuln; at most Medium tech debt. It does not warrant security-incident handling.
  - **Owner:** not Enterprise. ENT's triage queue is Groundcover alerts and hotel support requests (see the rest of the queue — BW/IHG alerts, user-creation asks); `access_control` is platform/core. **Recommend reroute** to the team owning `canary/access_control/`, or close as won't-fix-with-rationale.
  - **Rewrite the ACs** before anyone picks it up — as written they'd break internal tooling and contradict a passing test.
  - **Provenance:** created 2026-03-10 by Bernard Pietraga, title literally begins with `?`, no labels, sat in Triage 4 months untouched. Reads like unreviewed output from an AI security scan. Worth checking whether sibling tickets from that batch carry the same inflated severities.

  ### Verification status
  Code-read only — I did **not** run the test suite, and did **not** attempt a live repro (would require a staff session; out of scope for triage and against the repo's remote-env rules). The claims above about who controls the session are from reading the view + middleware + validator, which is sufficient to refute the stated exploit path. The two "what is real" items are flagged as *unverified* and would need their own look.

  ### External writes

  Triage comment **posted** to ENT-6850 with the findings above, on explicit user approval:
  https://linear.app/canary-technologies/issue/ENT-6850#comment-f13b2f9e-2600-4f37-bab0-5d20c5319c44

  Nothing else changed — priority is still HIGH, status still Triage, still unassigned. The downgrade, reroute and AC rewrite remain recommendations awaiting a decision.
project: null
source_id: https://linear.app/canary-technologies/issue/ENT-6850
tags:
- morning-gtd
- linear
time_minutes: 20
title: 'Triage ENT-6850: [HIGH] Privilege escalation via impersonation to staff-only
  endpoints'
updated: 2026-07-13 14:06:06.972786
waiting_on: null
waiting_since: null
working_on: false
---

Security-flagged item sitting in the ENT triage queue — highest-signal item there; needs an owner and severity call.
https://linear.app/canary-technologies/issue/ENT-6850