---
area: null
contexts: []
created: 2026-06-30 16:29:04.703184
defer_until: null
due: null
energy: low
id: 2026-06-30T1629-need-to-go-through-this-with-an-onboarding-script
order: null
output: |
  ## Agent run 2026-07-01 — Onboarding-script lens review

  Reviewed the Check-In V3 Configuration tech spec
  (https://www.notion.so/canarytechnologies/Check-In-V3-Configuration-365814686151808c805efb429b821412)
  against its PRD (https://app.notion.com/p/36d814686151801fbdcbfc67cebee86a) and the
  actual onboarding + rules-framework code. The doc leans hard on "enterprise owns
  seeding via onboarding scripts + rules framework" and scopes it out — but several of
  those load-bearing assumptions do NOT match how seeding works today.

  Linear project: [carryover] Step configurator flow builder
  (https://linear.app/canary-technologies/project/carryover-step-configurator-flow-builder-f9730800441c)
  — A&D team (lead Vibhor Sachdeva), target 2026-08-14, in Implementation. 8 tickets
  (AD-7907, AD-7828, AD-7836/7/8/9, AD-7843, AD-7243) — all configurator/read/write/UI.
  NONE cover seeding or generation.

  ### Ground truth (verified in code)
  - **Rules framework != onboarding seeding.** `rules_based_configuration` is declarative
    + validation-only. It is NOT run at onboarding; it's applied only via the manual
    `apply_portfolio_settings` mgmt command. FINAL/FREE = `OverridePolicy` enum in
    `rules_based_configuration/services/conformity.py`.
  - **The actual seeders are onboarding scripts / config providers.** `AddRegistrationCardPlan`
    (onboarding/plans/registration_card_plans.py:59) + brand providers (Wyndham/BW/IHG)
    create the `RegistrationCard`; `CheckInConfiguration` is lazily auto-created and its
    fields set by those providers.
  - **No provenance anywhere.** Nothing records "set by rules/onboarding" vs "edited by
    hand" on Hotel / CheckInConfiguration / RegistrationCard.
  - **Onboarding does NOT put hotels on v3.** `checkin_version` defaults to V2 and
    onboarding never sets v3. The v3 Flow/Step rows only materialize when
    `checkin_version=="v3"` fires `sync_v3_flow_on_config_save` -> `create_or_update_flow`
    (guest_experience/services/v3_migration.py). That's a separate migration step
    (migrate_hotel_to_v3 / dashboard), not onboarding.
  - **Additional-guests is split-brain + a v3 blocker.** Brand providers already set
    `additional_guests_*` on CheckInConfiguration at onboarding, but the v3 sub-flow step
    is seeded by a separate `seed_additional_guest_flow` command, AND
    `create_or_update_flow` currently BLOCKS v3 migration if
    `additional_guests_step != DISABLED` (v3_migration.py ~L70). So Wyndham hotels that
    require additional guests can't migrate to v3 today.
  - **The conformity save-signal is warn-only and admin-only.** `rules_based_configuration/signals.py`
    fires only on `hotel_admin_saved` (Django admin), never blocks ("warn mode"), and
    would not fire at all on the configurator's API write path.

  ### Findings (onboarding lens)
  1. **"Seeded by the enterprise rules framework at onboarding" is factually wrong.**
     Seeding is done by onboarding *scripts / config-providers* (imperative). The rules
     framework only validates conformity later, manually. Any A&D dependency on "the rules
     framework produces defaults" is misplaced. Fix the vocabulary and split the two
     cross-pod asks — they're different mechanisms/owners.
  2. **"Hotels arrive pre-configured [on v3]" is not true today.** Onboarding yields V2.
     The configurator's precondition (a hotel on v3 with a generated flow) comes from the
     v3 migration, not onboarding. Either onboarding starts seeding v3 directly, or the doc
     should say plainly that "defaults" come from the v3 migration path — and name the
     owner of v3 provisioning. The "scoped to hotels already on v3" rollout is fine; the
     "arrives pre-configured at onboarding" framing is aspirational.
  3. **PRD Job 1 (CS-triggered generation) is unowned — biggest gap.** PRD makes
     "Generate config" from the manage UI a core MVP requirement (brand->country->default
     hierarchy, review screen, "which standard applied"). The design scopes generation out
     to enterprise; the A&D project has no generation ticket; and today onboarding runs
     from Salesforce opportunities in batches, not an ad-hoc single-hotel "regenerate"
     button. A UI-triggerable, single-hotel, re-runnable generation is a real enterprise
     deliverable that no ticket owns.
  4. **Write-collision is real and currently unmitigatable.** Onboarding plans are
     idempotent/re-runnable (GOLIVE, re-onboarding, batch reprocessing). A re-run overwrites
     CS's configurator edits with brand defaults — silently, because there's no provenance.
     Without a "manually edited" marker (or non-destructive/merge generation) this can't be
     solved safely, and it gets worse once hotels self-serve. Should not be left "open."
  5. **FINAL/FREE and the configurator's Exposure are two disconnected locks over the same
     fields — and the compliance one is bypassable.** Exposure (per-audience,
     EDITABLE/READ_ONLY/HIDDEN, declared statically in code on buckets) knows nothing about
     the rules framework's FINAL/FREE (per-field, per-hotel-group; e.g. Wyndham marks
     GDPR-country ID collection FINAL). Nothing in the configurator write path consults
     FINAL, and the conformity signal is warn-only + admin-only, so a CS edit through the
     new API can silently violate an enterprise compliance lock. Also a statically-declared
     Exposure can't express "read-only only for hotels whose group locks it," so it can't
     faithfully mirror brand/country locking. Make this a decided design point, not open:
     at minimum the writer must reject edits to FINAL-locked fields (ideally derive Exposure
     from the hotel's resolved FINAL/FREE).
  6. **`get_compatibility_blockers` is not a conformity guard.** It only checks v3
     runnability. It will not catch a CS edit that diverges from a brand standard or
     violates a FINAL lock. The doc leans on it as the safety net; for enterprise
     correctness it isn't one.

  ### What the doc gets right
  - The facade-over-existing-models / single-source-of-truth call is correct and is exactly
    what keeps seeding and editing writing the same rows. A parallel config store would
    have broken seed<->edit consistency.
  - Correctly names write-collision as the real risk (vs schema break) and FINAL/FREE as an
    enterprise-alignment item — it just under-weights both.

  ### Asks I'd raise in the review (as enterprise/onboarding)
  - Correct the seeding description; separate onboarding-scripts/config-providers from
    `rules_based_configuration`.
  - Name owner + ticket for (a) v3 provisioning and (b) PRD Job 1 generation.
  - Move FINAL/FREE integration from "open" to "decided": write path must respect
    enterprise FINAL locks (GDPR ID, etc.).
  - Decide provenance up-front (manual-edit marker or merge-based generation) before
    re-runnable seeding can coexist with edits.
  - Reconcile additional-guests: who lifts the v3 blocker, and who owns seeding the sub-flow
    config vs the flow step, given brand providers already set the CheckInConfiguration
    fields.

  (No external writes made — no Notion/Linear/Slack comments posted. This is a local review
  to hand back to you.)
project: null
source_id: null
tags: []
time_minutes: 5
title: Need to go through this with an onboarding script lens
updated: 2026-07-01 16:30:49.456521
waiting_on: null
waiting_since: null
working_on: false
---

https://www.notion.so/canarytechnologies/Check-In-V3-Configuration-365814686151808c805efb429b821412?source=copy_link