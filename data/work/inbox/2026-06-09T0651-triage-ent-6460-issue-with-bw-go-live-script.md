---
area: null
contexts:
- react
created: 2026-06-09 06:51:19.390431
defer_until: null
due: null
energy: medium
id: 2026-06-09T0651-triage-ent-6460-issue-with-bw-go-live-script
order: null
output: |
  ## Agent run 2026-06-09T08:48Z

  Triaged ENT-6460 (BW go-live script fails with "role name validation error").
  Root cause confirmed in code; already linked to TOOL-97 (the cause).

  ### What happened
  Melissa (mfairchild) ran a BW go-live via the cohort/batch onboarding UI and hit
  a role-name validation error. She set the hotel live manually and is blocked from
  using the script. P0/Urgent. Cohort 09db1c56.../batch 72f4f051...

  ### Root cause (code-confirmed, conclusive)
  TOOL-97 (PR #44658, merged 2026-05-20) added a duplicate-role-name check to
  `RoleService.create_role`. That check diverges from the idempotent get-or-create
  used by onboarding activation:

  - `permissions/services/activation.py:119-122` — `_get_or_create_role` looks up the
    existing role with `PropertyRole.objects.get(hotel=..., name=args.name)`:
    CASE-SENSITIVE (Postgres default collation) and UN-stripped.
  - `permissions/services/role.py:115-119` — `create_role` validates with
    `cleaned_name = args.name.strip()` + `PropertyRoleSelectors.name_taken_for_property_role(...)`,
    which uses `name__iexact` (selectors/property_role.py:79-83): CASE-INSENSITIVE + stripped.

  Trigger: the hotel already has a PropertyRole whose name matches an activation role
  name only after strip()/case-folding (e.g. stored "Hotel Staff" vs activation "hotel staff",
  or a trailing space). The `.get()` misses -> falls through to `create_role` -> the
  `__iexact` dup check hits the existing role -> raises RoleNameValidationError(DUPLICATE_NAME_CODE).
  Pre-TOOL-97 there was no dup check, so the mismatch was silently tolerated and the
  script worked. This is a regression, not a data problem.

  Note: full re-runs over an already-live hotel are guarded
  (`best_western_roles_and_permissions_provider.py:37-39`, hotel_has_gone_live_via_scripts),
  so the collision is happening WITHIN activation against a pre-existing role on the hotel,
  not from naive re-execution.

  ### Recommended fix (small, surgical)
  Align `_get_or_create_role`'s lookup to the same semantics as the new validation so
  get-or-create stays idempotent: strip the name and use `name__iexact` (mirroring
  `name_taken_for_property_role`). Apply to both the `.get()` and the
  `MultipleObjectsReturned` fallback filter (activation.py:119-132). This makes the
  existing role get found and returned instead of attempting a re-create. ~3-5 line change.
  Add a regression test: activation when a same-name-different-case PropertyRole already
  exists on the hotel.

  ### Observability note
  Checked Datadog: the relevant structlog events (`activation_service.creating_role`,
  `role_service.create_role`, `activation_service.role_already_exists`) are NOT indexed
  in the hot tier (0 hits over 14d), so I couldn't pull the exact colliding role name from
  logs. Datadog is the right place for backend app logs (not Groundcover, which is infra/k8s),
  but these particular events would only be in online archives. The exact role name isn't
  needed to confirm the fix; it can be obtained by reproducing locally against the affected hotel.

  ### Suggested triage disposition (user's call — not done)
  - Accept out of triage, team Enterprise (or Internal Tools, since TOOL-97 owner = Asher
    Davidson, project "user roles & permissions"). Branch already reserved:
    glloyd/ent-6460-issue-with-bw-go-live-script. This is my area (BW go-live).
  - Priority: keep Urgent — blocks scripted go-lives; manual workaround exists so not an
    active outage.
  - Next action candidate: implement the activation.py lookup fix + regression test.

  NOT done (await your call): no Linear writes, no status/priority change, no code change,
  no file move.
project: null
source_id: https://linear.app/canary-technologies/issue/ENT-6460/issue-with-bw-go-live-script
tags:
- morning-gtd
- linear
time_minutes: 20
title: 'Triage ENT-6460: Issue with BW go live script'
updated: 2026-06-09 08:48:24
waiting_on: null
waiting_since: null
working_on: false
---

ENT triage, priority Urgent (P0), raised by mfairchild. No detail yet — needs triage. BW go-live (my area). https://linear.app/canary-technologies/issue/ENT-6460/issue-with-bw-go-live-script