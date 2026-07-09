---
area: null
contexts:
- craft
- deep
created: 2026-05-19 16:45:58.164116
defer_until: null
due: null
energy: high
id: 2026-05-19T1645-good-idea-hotel-admin-that-detects-is-enterprise-h
order: -19
output: |
  ## Agent run 2026-07-01T16:02

  Turned this idea into an engineering design doc (design only; no code shipped).

  **Eng design doc:** Enterprise-aware Django admin — lock rules-controlled Hotel fields read-only
  https://app.notion.com/p/39081468615181d8a36cf15f032f626a
  (Canary ✏️ Design Doc Database · Team: Enterprise · Product: Onboarding · Status: WIP)

  ### What it proposes
  A reusable `ConformityLockedFieldsAdminMixin` for Django admin that makes rule-enforced
  Hotel fields read-only on the change form — but only when the field is FINAL-policy AND
  the hotel's current value already matches the rule ("if they match right value"). Never
  traps a drifted/wrong value as un-editable.

  ### Key findings from the codebase
  - "Rules-based config" = the **conformity system** at
    `backend/canary/rules_based_configuration/` (`services/conformity.py`, `ConformityService`).
  - "Detect enterprise" falls out for free: a non-enterprise hotel matches no config tree, so
    `get_all_setting_values_for_hotel_attributes` returns `{}` → nothing locked. No Salesforce
    call needed on render.
  - Extension point already exists: `HotelAdmin.get_readonly_fields` (`hotels/admin/hotel.py:2028`,
    the `pms` rule) — the mixin composes with it via the MRO.
  - **Gap the design fills:** the finalized conformity tree keeps each setting's value but drops
    its FINAL/FREE policy, so there's no public "which keys are FINAL for this hotel." Design adds
    a small `get_final_setting_keys_for_hotel_attributes` helper.

  ### Adversarial review already folded in (before writing the doc)
  - Use `ConformityService.hotel_conforms()` for the "matches" check, not hand-rolled `==`
    (handles ANY_NON_NULL / enums / NO_VALUE_DEFINED).
  - `get_readonly_fields` must fail open (never 500 the change page).
  - Resolve FINAL policy along the same tie-broken winning path as the value.
  - Guard against triggering the Salesforce fetch/create when `stored_hotel_attributes` is missing.
  - Honest scope: guard-rail against manual admin edits only — bypassable via shell/API and the
    admin's own Import/Export; real enforcement stays `apply_portfolio_settings` /
    `validate_hotel_on_save`.

  ### Open questions parked for review (in the doc)
  1. Is admin actually a meaningful drift vector vs. onboarding scripts? If not → PARK.
  2. Lock the Import/Export path too, or document the gap for v1?
  3. Engineering/superuser bypass, or is "a conforming FINAL value never needs hand-editing" enough?

  Local design/plan artifact: /Users/garethlloyd/.claude/plans/refactored-prancing-nova.md

  ## Agent run 2026-07-01T17:06 — cross-pod context (Check-In V3 configurator)

  Followed up on how this admin-lock idea connects to Leandro Alvarez's (A&D) Check-In V3
  Configuration work. Read the Slack group DM (Gareth/Leandro/Andrea Bradshaw) + Leandro's two
  design docs, and verified an onboarding-lens review of his tech spec against the code.

  ### The connection (why this idea matters beyond Django admin)
  - Leandro is building a **configurator**: a typed facade over existing config models
    (CheckInConfiguration, RegistrationCard, auth/payment) giving CS a UI to edit check-in v3
    config. It gates writes via per-field, per-audience **Exposure** (EDITABLE/READ_ONLY/HIDDEN).
  - His write path and this admin-lock idea need the **same missing primitive**: "which keys are
    FINAL for this hotel, enforced at a human write boundary." This design's proposed
    `get_final_setting_keys_for_hotel_attributes` is exactly what his Exposure gating would consume.
  - **Two surfaces, deliberately different FINAL semantics:**
    - *Admin (this doc):* lock a FINAL field only when the hotel already **conforms**, so an
      operator can still hand-fix a drifted value.
    - *Configurator (his):* refuse **all** writes to FINAL fields regardless of value, so CS can
      never *create* drift. Same helper, stricter policy.

  ### Ground truth verified in code (corrects a common misconception)
  - **Rules framework is NOT run at onboarding.** Seeding is done by imperative onboarding
    scripts / config-providers (AddRegistrationCardPlan + brand providers). `rules_based_configuration`
    only *validates* later — `apply_portfolio_settings` is a manual mgmt command (only self-refs;
    zero refs from onboarding/).
  - **Conformity save-signal is warn-only + admin-only** (`rules_based_configuration/signals.py`,
    fires on `hotel_admin_saved`, "Does not block saving"). Would not fire on a configurator API write.
  - **Onboarding never sets v3**; the v3 flow only materializes via a separate migration step.
  - **Additional-guests is a hard v3 blocker** (`v3_migration.py:70`: additional_guests_step != DISABLED).

  ### New gap surfaced (not covered by this doc)
  - **No provenance** anywhere ("set by rules/onboarding" vs "edited by hand"). Onboarding plans are
    idempotent/re-runnable, so a re-run silently clobbers CS edits. A manual-edit marker (or
    merge-based seeding) is a prerequisite before re-runnable seeding + human edits can coexist —
    worth its own capture. Relates to the same FINAL/FREE enforcement theme.

  No external writes made (no Notion/Linear/Slack). Handed the analysis back to Gareth in-session.
project: 2026-04-16T1348-ideas
source_id: null
tags: []
time_minutes: 30
title: 'good idea: hotel admin that detects is enterprise hotel and makes many fields
  read only (if they match right value)'
updated: 2026-07-09 13:45:44.559545
waiting_on: null
waiting_since: null
working_on: false
---

* Create a new django admin superclass that can conditionally make fields readonly if they're controlled by rules-based config
* Detect hotel's config
* make fields readonly

https://app.notion.com/p/canarytechnologies/Enterprise-aware-Django-admin-lock-rules-controlled-Hotel-fields-read-only-39081468615181d8a36cf15f032f626a?source=copy_link