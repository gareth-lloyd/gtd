---
area: null
completed_at: null
contexts: []
created: 2026-07-30 15:28:02.557778
defer_until: null
due: null
energy: low
id: 2026-07-30T1528-audit-the-provider-pattern-in-onboarding-where-are
order: null
output: |
  ## Agent run 2026-07-31T13:05:00

  Audited all 49 plans in `backend/canary/onboarding/plans/` and all ~50 provider
  `perform_hotel_configuration` overrides in `configuration_providers/`. 25 plans call the
  provider hook. Found three violation classes plus one structural root cause.

  ### Class A — shell plans (the EnableMSAProducts shape)

  `execute` is an empty delegator; the entire step lives in per-brand providers:

  - `EnableMsaProductsPlan` (plans/enable_msa_products_plan.py) — zero own logic. Providers: BW 61
    lines, Wyndham 74, IHG Pilot 79, IHG Messaging 23. `EnableMsaProductsConfig`
    (configuration_providers/configs/enable_msa_products.py) is an *empty dataclass* whose
    docstring codifies the violation: "providers act on the Hotel directly."
  - `PopulateCompendiumPlan` (6-line execute; BW 25-line, Wyndham 80-line providers)
  - `ConfigureHotelImagePlan` (6-line execute; Wyndham 36-line provider)
  - `ConfigureRoomUpgradesPlan` (8-line execute; Wyndham 86-line provider)
  - `WhatsAppPlan` (self-acknowledged "thin wrapper" comment in the file; WCP provider 31 lines)
  - `ReactivateHotelPlan` (13 lines)
  - Hybrids: `DeactivateHotelPlan` / `GoLivePlan` have real execute bodies but providers still
    carry 25–50 lines of step logic each.

  Drift is already visible in the MSA family: BW and Wyndham providers share ~60% of the same
  algorithm (product flags, outbound subdomain, gate has_*_messages until go-live,
  is_demo/is_active reset, feedback config, check-in config, PMS hookup) but use different
  go-live checks (`OnboardingBatchService.hotel_has_gone_live_via_scripts` vs
  `CohortHotelService.has_gone_live`), full `hotel.save()` vs `update_fields`, and inline
  imports. A fix to one brand won't propagate.

  ### Class B — generic algorithm copy-pasted across brand providers

  - Department providers (Crestline / Stonebridge / Raymond / Marriott): diffing them shows the
    "remove departments not in brand set (keep wallet-linked, keep tipped)" algorithm is
    IDENTICAL modulo brand constants — constants that already live in `DepartmentConfig`.
    `DepartmentPlan.execute` does the *add* half generically from config; the *remove* half is
    copy-pasted 4x in providers.
  - Tip config providers x9 brands (Aimbridge 82 lines, Buffalo, Crestline, Marriott, MVW,
    Pyramid, Raymond, Stonebridge, Wyndham): Stonebridge vs Buffalo differ only in UUID
    constants and one enum value. All expressible as config consumed by `ConfigureTippingPlan`.
  - Roles-and-permissions providers x4 similar (though `ConfigureRolesAndPermissionsPlan`
    itself has decent config-driven logic).

  ### Class C — hook as a late config builder (data-flow inversion)

  `IHGUpsellsConfigProvider.perform_hotel_configuration` (201 lines) *mutates
  `self.config.managed_addons`* inside the hook because the decision needs the hotel
  (`hotel.has_addons`), and `ConfigureDefaultUpsellsPlan.execute` consumes config afterwards.
  The hook has become a hidden config-construction phase; the plan-body-vs-hook ordering is
  load-bearing and implicit. Related: call ordering is inconsistent across plans (upsells/roles
  call the hook FIRST; booking gateway/department/registration card/association-ids call it
  LAST), so the hook has no defined contract about what hotel state it observes.

  ### Implications

  1. **Silent no-op onboarding steps.** `PlanFactory.assemble`
     (models/property_configuration_processes.py) returns `config_provider=None` when no
     decider matches and there is no DEFAULT_PROVIDER. Shell plans then return
     `{"status": "skipped"}` and the script batch records success while nothing was
     configured. Wiring a new onboarding type/brand without a provider mapping silently skips
     MSA product enablement, compendium, room upgrades, etc. Only caught if
     check_hotel_configuration monitoring exists for that brand.
  2. **Duplication → drift → brand-inconsistent bugs.** Fixes land per-brand; drift already
     observable in the MSA and department families.
  3. **Convention bypass.** Plan-level guarantees (idempotency, `raise_expected_error` codes,
     result-dict audit trail) live in plans by convention. Providers doing bulk work
     log-and-continue instead (Wyndham MSA logs and continues on NoDataAvailable) and return
     `{}`, so the OnboardingScriptRun records nothing about what changed.
  4. **New-brand cost + review surface.** Adding a brand means copying a 50–80-line imperative
     provider instead of declaring a small config dataclass; reviewers can't diff brands.
  5. **Structural root cause:** provider config is built in `__init__` from
     `OnboardingPlanData` only — no hotel available. Any hotel-dependent config decision
     can't use the config channel, so authors fall back to the imperative hook. That's what
     produced classes A and C.

  ### Recommendations (not applied — audit only)

  - Codify the rule in `onboarding/CLAUDE.md` ("bulk of operations in execute;
    perform_hotel_configuration only for brand special cases") — it currently documents the
    mechanics but not this rule.
  - Highest-leverage refactor first: `EnableMsaProducts` — enrich `EnableMsaProductsConfig`
    (product flags, outbound subdomain, feedback threshold, check-in text, go-live checker)
    and hoist the shared algorithm into execute. Biggest drift risk (4 providers, live brands).
  - Class B mechanical wins: move department *removal* into `DepartmentPlan.execute` driven by
    `DepartmentConfig`; collapse the 9 tip providers into config.
  - Make provider-mandatory shell plans fail loudly when `config_provider is None` instead of
    returning "skipped".
  - Consider a provider `build_config(hotel)` phase (or pass hotel into config construction)
    to eliminate class C's config mutation inside the hook.
project: null
source_id: null
tags: []
time_minutes: 5
title: Audit the plan / provider pattern in onboarding. Where are we violating? What's
  the implication?
updated: 2026-08-03 14:44:21.717722
waiting_on: null
waiting_since: null
working_on: false
---

Known violation example:
* EnableMSAProducts plan is a shall which depends entirely on calling provider.configure_hotel
* Most plans should have the bulk of their operations in `execute`, and configure_hotel should only have special cases.