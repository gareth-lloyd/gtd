---
area: null
contexts:
- react
created: 2026-06-10 11:43:19.326873
defer_until: null
due: null
energy: medium
id: 2026-06-10T1143-review-pr-47444-ent-6460-make-deactivate-product-p
order: null
output: |
  ## Agent run 2026-06-10T15:45:00

  Reviewed PR #47444 (megolem, 2 files, +42). Verdict: approach is right and safe,
  but there is ONE real gap that can re-trigger the exact go-live blocker, plus minor
  polish items. CI fully green (backend tests + E2E; only cancelled deploy/gatekeeper
  checks outstanding). No review posted to GitHub — draft below awaits your approval.

  ### Main finding: lookup is case/whitespace-sensitive, validation is not
  `create_role` rejects duplicates via `name_taken_for_property_role`, which matches
  `name__iexact` on a TRIMMED name (permissions/selectors/property_role.py:83). The new
  reuse lookup is `PropertyRole.objects.filter(hotel=hotel, name=default_role.label)` —
  exact match. A pre-existing hotel role named "property manager", "PROPERTY MANAGER",
  or "Property Manager " dodges the reuse lookup but still raises
  RoleNameValidationError in create_role → the BW go-live script still crashes.
  Since the root cause is operator-created duplicate names (TOOL-97), case variants
  are plausible in the wild. Fix: `name__iexact=default_role.label.strip()`, and add a
  test with a case-variant name.

  ### Minor points
  1. `.first()` without `order_by` — pre-TOOL-97 data can hold MULTIPLE same-name roles
     per hotel (that was the TOOL-97 problem); which one gets reused is nondeterministic.
     Suggest `.order_by("id").first()`.
  2. Reused role keeps its own permission set, not `revised_permissions`. Safety-wise OK:
     the pre-existing role is hotel-managed, so the earlier grant-deletion pass already
     stripped the deactivated product's permissions from it (or deleted it if emptied,
     in which case the create path runs). But users converted off the default role get
     whatever the manual role happens to grant — they can silently LOSE the rest of the
     default-role permissions. Fine for BW MSA go-live (perms move to SSO roles anyway),
     but the service is generic — worth logging the permission diff in the reuse branch
     or acknowledging the choice in the PR description.
  3. Reuse doesn't check `permission_context` — could attach property grants to a
     same-name role with a legacy non-PROPERTY context. Not a regression (old code
     crashed on those too), but a log/assert would make reuse safer.
  4. Optional: a `reused_roles` field on DeactivationResults would help go-live script
     reporting; reused roles currently appear nowhere in results.

  ### What I verified
  - Read full deactivation flow: ordering protects the reuse path (product permission
    grants are stripped from ALL hotel-managed roles before the reuse lookup runs).
  - Lookup bucket (hotel=hotel) correctly mirrors validation bucket (hotel_id scope);
    PropertyRole is hard-delete so no soft-delete manager pitfalls.
  - Sole production caller is BW go_live_provider.perform_hotel_configuration.
  - Updated test is correct and asserts grant redirection + no created roles.

  ### Draft review comment (NOT posted — needs your go-ahead)
  "Approach looks right and the ordering makes the reuse safe (product grants are
  stripped before the lookup). One gap: create_role validates duplicates with
  name__iexact on a trimmed name, but the reuse lookup is exact-match — a role named
  'property manager' or 'Property Manager ' still crashes the go-live script. Suggest
  name__iexact=default_role.label.strip() plus a case-variant test, and
  .order_by('id').first() since pre-TOOL-97 hotels can have multiple same-name roles.
  Also worth noting in the description that converted users inherit the pre-existing
  role's permission set rather than revised_permissions."
project: null
source_id: https://github.com/canary-technologies-corp/canary/pull/47444
tags:
- morning-gtd
- github
- from-awareness
time_minutes: 20
title: 'Review PR #47444: [ENT-6460] Make deactivate_product_permissions idempotent
  on role-name collision'
updated: 2026-06-10 16:37:57.484343
waiting_on: null
waiting_since: null
working_on: false
---

golem's fix for the BW go-live script blocker (Andrea/Melissa). Root cause TOOL-97 duplicate role names. Pairs with Andrea's sync ask.
https://github.com/canary-technologies-corp/canary/pull/47444