---
area: null
contexts: []
created: 2026-05-28 20:51:52.135098
defer_until: null
due: null
energy: low
id: 2026-05-28T2051-ent-6326-is-it-idempotent
order: null
output: |
  ## Agent run 2026-05-29T07:21:59Z

  Question: ENT-6326 — "is it idempotent?" Re the new WYNDHAM_ENABLE_MSA_PRODUCTS
  rollout recipe (working-tree diff on backend/canary/onboarding/models/rollouts.py),
  which wires EnableMsaProductsPlan for Wyndham hotels.

  VERDICT: Yes — idempotent. Re-running the plan against an already-configured
  hotel converges to the same end-state and creates no duplicate rows.

  Traced the full execution path:
  - EnableMsaProductsPlan.execute() just delegates to the config provider's
    perform_hotel_configuration() (plans/enable_msa_products_plan.py).
  - For Wyndham the provider is WyndhamEnableMsaProductsProvider
    (configuration_providers/wyndham/wyndham_enable_msa_products_provider.py).
    perform_hotel_configuration() runs in a single transaction.atomic() and only
    SETS deterministic values: is_demo=False, has_addons/has_check_in/has_check_out/
    has_chat=True, fixed i18n message, region-mapped outbound_url_subdomain,
    is_active=True, rollout_whatsapp_integration=True, check-in V2 level=STABLE.
    Setting constants is inherently idempotent.
  - Branchy bits are all deterministic on hotel state, not on run count:
      * has_check_in_messages / has_check_out_messages set False only if NOT gone
        live (CohortHotelService.has_gone_live) — same outcome every run.
      * check-in/out times come from WyndhamCheckInOutTimeService (deterministic
        external read; NoDataAvailable just logs + leaves times unchanged).
  - FeedbackConfigurationService.update_or_create(...) — upsert, idempotent.
  - configure_wyndham_hotel_for_pms_integration() (wyndham_pms_config_provider.py):
    sets flags; pms_payment_slot_identifier_auths is "set only if empty"
    (convergent). Calls AddonConfigurationService.enable().
  - AddonConfigurationService.enable() (addons/services/addon_configuration.py):
    only flips flags / sets codes — NO row creation.

  Row-creation candidates (the two methods the unit test mocks) are both guarded:
  - Hotel.save() (hotels/models/hotel.py:1403-1410) wraps the default-seeders in
    existence checks: ensure_default_addons_exist() only when has_addons, and
    create_default_room_upgrade_tiers() only `if not self.room_upgrade_tiers.exists()`.
  - AddonManagementService.ensure_default_addons_exist() is itself .exists()-guarded
    per addon type.
  - NB: create_default_room_upgrade_tiers() itself is UNGUARDED (creates 2 tiers
    unconditionally), but its only production caller is the guarded Hotel.save()
    branch, so no duplicate tiers in practice.

  No list-appends, counters, or increments anywhere in the path.

  Caveat worth flagging on the ticket (not a true idempotency bug):
  - Most flags are FORCE-set to MSA defaults, so a re-run will overwrite any manual
    operator tweaks made after the first run (resets them to MSA values). That is
    "idempotent" in the convergence sense but destructive to manual divergence.
    Exceptions that preserve existing values: pms_payment_slot_identifier_auths
    (set-if-empty) and feedback config (update_or_create).
  - Rollout-orchestration layer: re-running the rollout creates NEW
    OnboardingScriptBatch records and re-executes plans. Hotel end-state converges,
    but you accumulate batch-history rows — bookkeeping, not hotel-state duplication.

  Existing tests: onboarding/tests/plans/test_enable_msa_products_plan.py (did not
  run them; static trace only). No code change made.
project: null
source_id: null
tags: []
time_minutes: 5
title: Solve the issue of non-idempotent rollouts. Allow config providers to supply
  different config on first and subsequent runs
updated: 2026-05-29 11:20:16.153959
waiting_on: null
waiting_since: null
working_on: false
---

Create a high-level Design sequence doc for the following:
 add first execution flag, and allow config providers to do what they want

* CPs initialized with `is_first_execution_on_hotel`
* Config providers decide how to configure the config object based on the flag

Pros:
* Very light change

dangers:
* Softens idempotency in a vague way
* Different plans will do it differently
* Makes assumptions about the future. Sometimes we *will* want the full rollout