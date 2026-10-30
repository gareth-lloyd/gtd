---
area: null
completed_at: 2026-10-29 15:59:25.477733
contexts:
- deep
created: 2026-10-28 14:52:21.522860
defer_until: null
due: null
energy: high
id: 2026-10-28T1452-ask-ad-whether-enterprise-onboarding-providers-can
order: null
output: |
  ## Agent run 2026-10-29T13:35:55Z

  Checked the code on master (8bd2f4314f6). Nothing was sent: the Slack draft is below for you to post.

  ### Short answer
  Mechanically yes for Wyndham MSA, IHG Pilot and IHG GMS Core. Not for Best Western MSA hotels on the extendable card. That is a real gap AD has to decide on, not plumbing.

  ### What the code says
  - TOOL-871 (ca47b58a9d6, PR #60865 https://github.com/canary-technologies-corp/canary/pull/60865, Ramiro): adds `ConfigureCheckInPlan` (onboarding/plans/configure_check_in_plan.py). It takes `config_provider=None`, skips live hotels and hotels already on the catalog, then in one savepoint calls `V3MigrationService.migrate_hotel_to_v3` and `V3MigrationService.move_hotel_to_catalog`. It is wired only into `OnboardingType.DEFAULT`, right after `AddRegistrationCardPlan` (property_configuration_processes.py:3299). No Enterprise type uses it.
  - AD-10463 (7c7a49fd9b4, PR #61422 https://github.com/canary-technologies-corp/canary/pull/61422, Guido): adds `V3MigrationService.migrate_hotel_to_v3_and_catalog`. It does the same two writes in one transaction and returns a typed result: MIGRATED / ALREADY_MIGRATED / BLOCKED / FORMS_NOT_REPRODUCIBLE / PORTFOLIO_MANAGED / NO_FORM_STEP. TOOL-871's plan still calls the two methods separately, not this entry point.
  - Nothing in either path is DEFAULT-specific. Both take a `Hotel` and read state off it. Any onboarding type can reuse it by appending `PlanFactory(plan=ConfigureCheckInPlan, config_provider=None)` after its `AddRegistrationCardPlan`.
  - `AddRegistrationCardPlan` already handles a hotel that is on v3 and the catalog: it regenerates the catalog from the new card and fails the plan on a refusal (registration_card_plans.py `_regenerate_field_catalog`). So a later Enterprise rerun of the card plan does not silently diverge.

  ### What would actually stop each Enterprise type
  1. **BW MSA with the extendable card (hard stop).** When OnboardingValue `BW_USE_EXTENDABLE_REGISTRATION_CARD` is set, `BestWesternRegistrationCardProvider` writes a `RegistrationCardExtension` against the PMS's portfolio card. `GuestFieldsSourceService.move_to_catalog` then returns PORTFOLIO_MANAGED (via `RegistrationCardService.is_portfolio_managed`). The plan would fail with `ERROR_REGISTRATION_CARD_PORTFOLIO_MANAGED`. The catalog has no notion of a portfolio-owned form yet, so this needs an AD design decision (a portfolio catalog, or keep BW on card + v3 without the catalog). BW hotels on the legacy card path have no extension and would pass.
  2. **Compatibility blockers (data-dependent, all brands).** `get_compatibility_blockers` refuses on: CC upload policy ALWAYS/HIGH_RISK, surcharge manual correction, Canary-managed payments without hotel-wide deposits, or STB EVA without the JWT-only setup. The Enterprise card providers don't set any of these themselves, so it depends on what other plans or ops set. IHG FreedomPay/CMP hotels are the ones to check.
  3. **Wyndham MSA / IHG Pilot / IHG GMS Core.** Plain per-hotel cards with no extension, so the catalog move should succeed whenever extraction reproduces the card. Unverified: whether the brand card templates (Wyndham loyalty consent text, IHG per-country GMS Core cards, IHG kiosk card) all extract cleanly. A FORMS_NOT_REPRODUCIBLE refusal is the likely failure mode. Running `migrate_hotel_to_v3_and_catalog` in dry form, or the admin move_to_catalog view, against a few recently onboarded hotels per brand would answer this.
  4. **The 08-06 "intent, not fields" ask is still not met.** Every Enterprise card provider still sets `rollout_check_in_v2_level=STABLE` and its own check-in fields directly through `check_in_configuration_updates`. TOOL-871 adds a v3 flip after that; it does not replace field-setting with an intent call.

  ### Thread to restart
  The 2026-08-06 ask was in the group DM with Andrea, Vibhor, Connor, Dana and Stephanie, pointing at https://canarytechnologies.slack.com/archives/C04STT7UPRQ/p1778146926830239?thread_ts=1778005781.503109&cid=C04STT7UPRQ. Leandro is not in that DM, so either add him or start a new thread in the AD channel.

  ### Draft (not sent; post it yourself or tell me "send it" with the destination)
  > Picking this back up after the Andrea sync. TOOL-871 and AD-10463 landed, and I read the code: `ConfigureCheckInPlan` and `V3MigrationService.migrate_hotel_to_v3_and_catalog` have nothing DEFAULT-specific in them. Wyndham MSA, IHG Pilot and IHG GMS Core could append the same plan after their card plan. Three questions for AD:
  > 1. BW hotels on the extendable registration card come back PORTFOLIO_MANAGED and can't move to the catalog. What's the plan for portfolio-owned forms: a portfolio catalog, or BW stays on v3 + card for now?
  > 2. Are you confident the Wyndham and IHG (incl. per-country GMS Core) card templates extract cleanly? Or should we dry-run a few recent hotels per brand before Enterprise wires the plan in?
  > 3. Should Enterprise onboarding call `migrate_hotel_to_v3_and_catalog` (one typed result) rather than the two-call pattern TOOL-871 uses? And is that the first piece of the "onboarding passes intent" service, or something separate?
  > @Dana @Leandro

  Not done: no tests run, no prod data queried (e.g. counting BW hotels with a CURRENT RegistrationCardExtension, or Enterprise hotels hitting the blockers). Those counts would size question 1 and are a quick read-only `canary prod-db query` if you want them.
project: null
source_id: null
tags: []
time_minutes: 30
title: Ask AD whether Enterprise onboarding providers can reuse TOOL-871's path (migrate_hotel_to_v3
  + move_to_catalog + catalog writes)
updated: 2026-10-29 15:59:25.477717
waiting_on: null
waiting_since: null
working_on: true
---

From: check-in v3 rollout research, 2026-10-28 (#ihg thread, #best-western thread, TOOL 'Automate Check-in V3 Onboarding' design)
Gareth's 2026-08-06 ask to Dana: AD owns a check-in config service; onboarding passes intent, never sets fields.
Internal Tools design (Sam Kariu, REVIEW ME!) does this for DEFAULT onboarding but puts Wyndham MSA, BW MSA, IHG Pilot, IHG GMS Core out of scope.
AD-10463 (Done 10-23) added a single V3MigrationService entry point. Not yet verified in code whether Enterprise providers can call it.
Restart the thread with Dana + Leandro after the Andrea sync.