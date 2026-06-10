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

  ## Agent run 2026-06-09T08:55Z (CORRECTION — supersedes the fix recommendation above)

  Re-examined the fix against the intent of the permissions service. My earlier
  "align lookup to strip + name__iexact" recommendation is NOT safe. Walking it back.

  Newly confirmed facts:
  - `_get_or_create_role` does not merely return a found role. On a hit it asserts
    `set(get_permissions_for_role(role)) == set(args.permissions)` and raises ValueError
    otherwise (activation.py:134-136). Intent is narrow and deliberate: reuse a role ONLY
    if it is exactly the one activation itself would have created (same name + same perms).
    The case-sensitive `.get()` is consistent with that strictness.
  - Activation role names are clean, distinct constants: ROLE_NAMES[legacy_permission]
    (activation.py:194) and DEFAULT_ROLE_NAME (activation.py:284). No stray whitespace;
    intra-run self-collision is implausible.
  - `activate_new_permissions` is @transaction.atomic (activation.py:202), so a failed
    prior run rolls back fully — it cannot leave half-created roles. The colliding role
    must therefore come from OUTSIDE this activation (SSO-managed role, manually-created
    role, or another onboarding step).
  - Dup selector matches case-insensitive + trimmed (property_role.py:79-83); the `.get()`
    matches exact + untrimmed. That divergence is the regression surface.

  Why the iexact fix is wrong:
  1. Right permissions? No. With iexact, a pre-existing case/space-variant role (likely
     SSO-managed or hotel-made, with DIFFERENT permissions) now gets FOUND -> perm-equality
     guard fails -> ValueError. Go-live stays blocked; I'd only have swapped one exception
     for another. In the rare case perms match exactly, it ADOPTS the pre-existing role
     instead of creating activation's standard role.
  2. Against intent? Yes, semantically. activate_new_permissions then GRANTS onboarding
     users into whatever _get_or_create_role returns (created_roles[...]). The iexact change
     would graft users onto the hotel's pre-existing (possibly SSO-managed) role rather than
     a clean standard role, and reinterprets the perm-equality guard from "a role I created"
     to "any same-named role the hotel happens to have." Not the original design.

  Correct path forward (needs the actual data + a product call, not a one-liner):
  - First REPRODUCE to identify the offending role: which hotel, the exact pre-existing
    role name/case/whitespace, its source (SSO-managed? manual?), and its permissions vs
    activation's computed set. (Datadog can't supply this — events not indexed; reproduce
    locally / inspect the affected hotel's PropertyRoles.)
  - Then choose among genuinely different fixes:
    (a) Data cleanup — if the colliding role is a stray/legacy duplicate, rename/remove it
        on that hotel; no code change. Possibly the fastest unblock (hotel already manual-live).
    (b) Activation-scoped create that bypasses the global TOOL-97 uniqueness check (internal
        trusted path / flag), restoring pre-TOOL-97 behavior of creating the standard role.
        Tradeoff: reintroduces a case-variant duplicate — exactly what TOOL-97 set out to
        prevent — so needs product sign-off.
    (c) Genuinely treat case-insensitive matches as "the same role" in activation — but then
        the perm-equality guard needs a defined behavior on mismatch (reconcile? error?),
        which is a design decision spanning TOOL-97's owners (Internal Tools / Asher Davidson)
        and onboarding.
  - Recommendation: triage out as a code bug, but the next action is REPRODUCE + decide
    between (a)/(b)/(c) with Internal Tools, not "ship the iexact change." Severity Urgent
    stands but manual workaround is in place.

  ## Agent run 2026-06-09T09:20Z (STACKTRACE FOUND — corrects the failing code path)

  Pulled the actual Datadog stacktrace. It REFUTES the specific function in both prior
  runs above. Right CLASS of bug (TOOL-97 dup-check breaks an onboarding role-creation
  path), but WRONG function — it is NOT ActivationService._get_or_create_role.

  Evidence (Datadog, hot tier, service:canary-celery-onboarding):
  - 5 identical failures on 2026-06-08 at 22:18, 22:20, 22:32, 22:43, 22:50 UTC
    (minutes before the ticket was filed at 22:57), hotel_id 129269400 (a BW MSA hotel
    in Melissa's cohort), logger onboarding.services.onboarding_batch,
    event onboarding_batch_service.script_run_attempt.salesforce_onboarding_service_error.
  - Confirmed it runs ASYNC via the batch worker (canary-celery-onboarding /
    cron_run_onboarding_script_batches), not a sync web request — which is why there is
    no request_failed/500 log; the exception is caught and stored as the batch run error
    and surfaced in the UI (the unhelpful "role name validation error" — the exception
    message is literally None, see below).

  Actual stacktrace (verbatim chain):
    onboarding/services/onboarding.py:493 run_plans_on_hotel -> plan.execute
    onboarding/plans/go_live_plan.py:97 execute
    onboarding/configuration_providers/best_western/go_live_provider.py:73
        DeactivationService.deactivate_product_permissions(hotel, BW_MSA_PRODUCTS)
    permissions/services/deactivation.py:76  new_role = RoleService.create_role(...)
    permissions/services/role.py:119  raise RoleNameValidationError(DUPLICATE_NAME_CODE)
    -> wrapped as onboarding.exceptions.OnboardingServiceError
    exception_message: RoleNameValidationError: None  (no human-readable message)

  Corrected root cause:
  - BW go-live's go_live_provider (NOT the roles_and_permissions_provider I read earlier)
    calls DeactivationService.deactivate_product_permissions to strip MSA-product
    permissions from custom hotel roles (those products are SSO-granted post-go-live).
  - deactivation.py:68-91 then converts each remaining DEFAULT-role grant into a concrete
    PropertyRole named after default_role.label (e.g. "Front Desk", "Property Manager"),
    calling RoleService.create_role DIRECTLY — no get-or-create, no pre-existence check.
  - TOOL-97's create_role dup check (role.py:118-119, case-insensitive + trimmed via
    name_taken_for_property_role) now fires because the hotel ALREADY has a PropertyRole
    whose name matches that default-role label under iexact. -> RoleNameValidationError.
  - It failed on the FIRST create in the loop (no deactivate_product_permissions.created_role
    log was emitted), and the method is @transaction.atomic, so every one of the 5 retries
    rolled back cleanly. The colliding role therefore PRE-EXISTED all 5 attempts (a survivor
    among the 16 custom roles being stripped — role_ids 91276-91287, 104453/4, 105188, 133365
    — that kept a non-MSA permission and happens to be named like a default role; or a
    concrete role left by an earlier successful conversion).

  What this means for the fix (supersedes the activation.py discussion above):
  - The fix belongs in DeactivationService.deactivate_product_permissions (deactivation.py:76),
    not ActivationService. That call site must be collision-safe: e.g. get-or-reuse an
    existing role with the same (trimmed/case-folded) name instead of blindly create_role,
    or otherwise reconcile. The same product question recurs (what if the existing same-named
    role's permissions differ from revised_permissions?) so this still needs a decision, but
    it is now scoped to ONE call site with a clear owner overlap (Internal Tools = TOOL-97,
    onboarding = us).
  - Immediate unblock for hotel 129269400: find the pre-existing PropertyRole whose name
    collides (case-insensitively) with a DefaultPropertyRole.label and rename/remove it, then
    re-run go-live. (Melissa already set the hotel live manually.)
  - Note: any BW hotel whose staff created a role named like a default role (very common:
    "Front Desk", "Property Manager") will hit this on go-live until the code is fixed —
    so expect recurrence across the BW cohort, not a one-off.

  Net: my high-level conclusion to Melissa (TOOL-97 caused it, needs a code fix) holds and
  is now stacktrace-proven. My intermediate code analysis pointed at the wrong function;
  the corrected failing path is deactivation.py:76 via the BW go_live_provider.

  ## Agent run 2026-06-09T09:35Z (prod DB confirmation via Django shell)

  Ran a read-only shell query on hotel 129269400 (Best Western Plus Dartmouth Hotel &
  Suites). Confirmed the exact dupe:
  - Blocking role: PropertyRole id=105188 name="Property Manager" (hotel-custom; sso_org=None,
    portfolio=None).
  - Hotel still has a leftover role=None grant for default_role=property_manager, so
    deactivate_product_permissions tries to create a concrete "Property Manager" and collides
    with 105188 via name__iexact. (Only property_manager has a lingering default grant; the
    other default labels don't collide.)
  - Telling detail: the hotel ALSO already has id=133365 "Property Staff" and id=105188
    "Property Manager" -- names identical to DefaultPropertyRole labels, with higher IDs than
    the original 91276-91287 role cluster. These are concrete roles a PRIOR
    deactivate_product_permissions run already created from default-role grants. So this is a
    RE-RUN collision: an earlier conversion created "Property Manager", a property_manager
    role=None grant lingered (or was added later), and the re-run tries to recreate it.
  - This is direct proof of the fix: deactivation.py:76 must get-or-REUSE the existing concrete
    role (105188) when re-pointing leftover default grants, not blindly create_role. An
    idempotent path would have reused 105188 instead of raising.

  Remediation: NOT performed (no prod writes). Hotel already set live manually by Melissa, so
  no urgent data fix needed. If we want the script itself to pass for this hotel before the code
  fix lands, the in-data option is to re-point the leftover property_manager role=None grant(s)
  to existing role 105188 and null their default_role (mirroring deactivation lines 93-99), or
  rename/remove the leftover -- to be drafted as a dry-run for explicit sign-off, not run ad hoc.
project: null
source_id: https://linear.app/canary-technologies/issue/ENT-6460/issue-with-bw-go-live-script
tags:
- morning-gtd
- linear
time_minutes: 20
title: 'Triage ENT-6460: Issue with BW go live script'
updated: 2026-06-09 15:19:14.805123
waiting_on: null
waiting_since: null
working_on: false
---

ENT triage, priority Urgent (P0), raised by mfairchild. No detail yet — needs triage. BW go-live (my area). https://linear.app/canary-technologies/issue/ENT-6460/issue-with-bw-go-live-script