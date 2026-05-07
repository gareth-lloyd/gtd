---
area: null
contexts:
- react
created: 2026-05-07 11:15:35.011627
defer_until: null
due: null
energy: medium
id: 2026-05-07T1115-review-pr-44778-add-deactivatetippingplan-onboardi
order: null
output: "## Agent run 2026-05-07T13:45Z — review of PR #44778\n\nReviewed locally
  against master. Diff: +187 / -0 across 4 files. CI not checked.\n\n### Verdict\nApprove
  once the message-vs-state inconsistency below is addressed (or explicitly\nwaved
  off). Everything else is optional polish. Solid, small, well-tested PR that\nfixes
  a real ergonomic issue with `ConfigureTippingPlan`'s early-return guard\n(configure_tipping_plan.py:25-28).\n\n###
  Strengths\n- Idempotent. Six tests cover all branches of a ~30-line plan.\n- Type
  annotation `OnboardingPlan[ConfigProvider[None]]` matches the existing\n  no-config-provider
  pattern (PMSSwitchArchivePlan, WhatsAppPlan, TippingGoLivePlan,\n  PopulateDemoDataPlan).\n-
  Wires through `KNOWN_PLANS` so the plan name is selectable in\n  `OnboardingScriptBatch.plan_names`.
  Adoption stays opt-in per batch — placing\n  the `PlanFactory` in `ONBOARDING_TYPE_CONFIG`
  does not auto-run it; only batches\n  that explicitly list `DeactivateTippingPlan`
  in `plan_names` execute it. The PR\n  description calls this out correctly.\n- Direct
  `hotel.save(update_fields=[\"has_tipping\"])` and use of\n  `ConfigurationService.set_can_be_tipped`
  are consistent with the existing\n  deactivation pattern (cf. wyndham_deactivate_hotel_provider.py:50,\n
  \ wyndham_remove_hotel_from_parent_brand_provider.py:72, hotels/admin/hotel.py:1802).\n-
  Coverage of all 9 dedicated `CONFIGURE_TIPPING` stages\n  (Wyndham/Marriott/MVW/Aimbridge/Pyramid/Buffalo/Stonebridge/Raymond/Crestline-Payroll)\n
  \ matches the count of `ConfigureTippingPlan` occurrences in\n  `CONFIGURE_TIPPING`
  script types — nothing missed.\n- The decision to skip `BASE_CONFIGURATION_NEW`
  flows is correct: those are\n  first-time-setup paths where the early-return guard
  is the desired safety.\n\n### Substantive nit (worth fixing)\n**Misleading message
  when both states diverge.** In\n`deactivate_tipping_plan.py:32-37`, when `hotel.has_tipping=True`
  but no\n`Configuration` row exists, the plan flips `has_tipping` to False and then\nreturns
  `message=\"No tipping configuration\"`. The `hotel_has_tipping_disabled`\nfield
  is `True` (truthful), but a human reading just the message will conclude\nno work
  was done. Test `test_execute__no_configuration_row__sets_hotel_flag_only`\ncodifies
  the inconsistency.\n\nSuggestion: when any flag was actually flipped, prefer the
  \"Tipping deactivated\"\nmessage and add a separate `no_tipping_configuration: True`
  field (or include it\nin the message), so both signals are visible. Or refactor
  to compute\n`message` once at the end based on what changed, rather than via early
  return.\n\n### Optional improvements\n1. **No log at start of `execute()`.** Most
  other plans (`ConfigureTippingPlan`,\n   `DeactivateHotelPlan`) emit `logger.info(\"execute\",
  **hotel.structlog_log_context())`\n   at the top. The new plan logs only at result
  branches. Adding the start log\n   helps when correlating with a batch run.\n2.
  **No test for the wiring change itself.** The PR adds 9 insertions in\n   `property_configuration_processes.py`
  and relies on existing\n   `test_configure_tipping_plan.py` for regression coverage.
  A tiny parametrized\n   test over the 9 onboarding types asserting `DeactivateTippingPlan`
  appears\n   immediately before `ConfigureTippingPlan` in their `CONFIGURE_TIPPING`
  stage\n   would lock in the ordering invariant the PR description calls out.\n3.
  **Docstring could note opt-in semantics.** Adding \"Adoption is opt-in per\n   `OnboardingScriptBatch.plan_names`;
  wiring into `ONBOARDING_TYPE_CONFIG`\n   does not auto-run this plan.\" to the docstring
  would save the next reader\n   a trip through the batch service.\n4. **Two queries
  for one Configuration.** The plan fetches via\n   `Configuration.objects.filter(hotel=hotel).first()`,
  then\n   `set_can_be_tipped` re-fetches via `TipsSelector.get_config_by_hotel`.\n
  \  Within a single transaction this is cheap, but is redundant.\n\n### Did not flag
  (looked OK)\n- Service-vs-direct-write split for `has_tipping`: existing codebase
  pattern.\n- Test stubs `stub_hotel_with_role_based_permissions`, `stub_tips_config`
  exist\n  and are the right ones.\n- `Configuration.hotel` is a `OneToOneField` (cascade
  on hotel delete);\n  `Configuration` is a plain `TimeStampedModel`, not soft-delete
  — the\n  `.filter().first()` approach is appropriate.\n- Hotel.has_tipping is in
  `PRODUCT_FIELDS`; `hotel.save(update_fields=...)`\n  will still flow through any
  `EventableModelMixin` save signals.\n\n### What I did NOT do\n- Did not run the
  test suite locally.\n- Did not check CI status.\n- Did not post any comment on the
  PR. Drafted the above for the user to review\n  and decide if/how to send it.\n\n###
  Suggested next action\nIf the user wants, I can post a condensed version of the
  substantive nit (#1)\n+ the wiring-test suggestion (#2) as a single PR comment —
  but I will not do\nthat without explicit approval per the session rules.\n"
project: null
source_id: https://github.com/canary-technologies-corp/canary/pull/44778
tags:
- morning-gtd
- github
time_minutes: 20
title: 'Review PR #44778: Add DeactivateTippingPlan onboarding plan'
updated: 2026-05-07 13:34:40.613369
waiting_on: null
waiting_since: null
working_on: false
---

Personally requested by @martinrodriguezcanary. ENT-5943.
https://github.com/canary-technologies-corp/canary/pull/44778