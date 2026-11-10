---
area: null
completed_at: 2026-11-10 15:56:50.293569
contexts:
- react
created: 2026-11-10 11:45:29.958734
defer_until: null
due: null
energy: medium
id: 2026-11-10T1145-look-at-ent-8207-confirm-the-ihg-base-config-re-ru
order: null
output: |
  ## Agent run 2026-11-10T15:55 (EET)

  **Answer: no re-run is planned. But the risk is smaller than the heads-up says, and a cheaper run than a full base-config re-run exists.**

  ### 1. No re-run is scheduled or tracked
  - ENT-8207 (https://linear.app/canary-technologies/issue/ENT-8207) has no comments, no blocking relation and no sub-issue for a re-run. Its description only says "Plan the re-run before adding the language, or gate the check".
  - PR #63973 (https://github.com/canary-technologies-corp/canary/pull/63973) is still a draft with no reviews. Its body says "Land this just ahead of the next scheduled one", but I found no scheduled one: no ticket in the IHG Scripting - Q4A 2026 project, nothing in Slack (#ihg, #ihg-q3-deployment, #temp-ihg-scripting, #epd-enterprise). The only cadence on record is Tincho's line on ENT-8056 (https://linear.app/canary-technologies/issue/ENT-8056): "Re-runs will happen at least quarterly". No date, no owner.
  - Only mention of the risk in Slack is Tincho's Nov 9 standup: https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1794261652741629

  ### 2. The "every IHG hotel unhealthy" claim is overstated (verified in code on master)
  - True part: `IHG_LANGUAGES` feeds `IHGGmsCoreSupportedLanguagesProvider`, and `ConfigureSupportedLanguagesPlan.check_hotel_configuration_after_instantiation` marks `SUPPORTED_LANGUAGES_CONFIGURED` UNHEALTHY when a required language is missing from `hotel.supported_languages` (backend/canary/onboarding/plans/configure_supported_languages_plan.py:116-136). So that one check row flips on every IHG GMS Core hotel once the PR deploys.
  - Missed part: `SUPPORTED_LANGUAGES_CONFIGURED` is not in `critical_check_types` for `IHG_GMS_CORE` (backend/canary/onboarding/models/property_configuration_processes.py:3143-3161), nor for any other IHG type. It is critical only for Wyndham MSA and BW MSA. The aggregate hotel `state` rolls up critical checks only (backend/canary/monitoring/services/monitored_hotel_state.py:111-119). So IHG hotels should stay HEALTHY overall; only the per-check drill-down shows the failure.
  - Not verified: whether any dashboard or alert reads the per-check row directly (ENT-8152 Omni dashboard is still Backlog). Worth asking Tincho.

  ### 3. A cheaper targeted run does exist
  - The PR says "there is no cheaper targeted run". The rollout recipe framework already runs a single plan of the IHG GMS Core `BASE_CONFIGURATION_NEW` stage: see `IHG_GMS_CORE_FREEDOMPAY_GATEWAY_SUBSET` (`plan_names=("ConfigurePaymentGatewayIntegrationPlan",)`) and `HIDE_IHG_GREENER_STAY_ONE_NIGHT` in backend/canary/onboarding/models/rollouts.py:285 and :550. A recipe with `plan_names=("ConfigureSupportedLanguagesPlan",)`, `onboarding_type=IHG_GMS_CORE`, PORTFOLIO/ALL, staged, would write the language without touching add-on times, names, images or checkout (the things ENT-8056 was about).
  - Two things to know before running it on live hotels, full re-run or recipe: `execute` replaces `hotel.supported_languages` with exactly the IHG list (any extra language a hotel added is dropped), and resets `default_guest_language` to "en" and `rollout_staff_language_selection` to False (configure_supported_languages_plan.py:82-95). ENT-8056 did not rule on languages.
  - Related: ENT-8226 (https://linear.app/canary-technologies/issue/ENT-8226, Triage) notes a single-plan recipe batch counts as "base configuration done" for the go-live check. A PORTFOLIO recipe with CANARY_ACTIVE would reach not-live hotels, so that exposure applies.

  ### Suggested next step (nothing sent)
  Draft comment for ENT-8207 or the PR, for you to post or adapt:

  > Checked the re-run sequencing. Two things: (1) SUPPORTED_LANGUAGES_CONFIGURED isn't in IHG_GMS_CORE's critical_check_types, so hotels' overall state shouldn't flip, only the per-check row. Does anything alert or chart on that row directly? (2) Instead of waiting for a full base-config re-run, could we add a rollout recipe that runs only ConfigureSupportedLanguagesPlan for IHG_GMS_CORE (like ihg_gms_core_freedompay_gateway_subset), and launch it right after merge? It avoids the ENT-8056 resets. Caveat: the plan overwrites supported_languages and default_guest_language on live hotels, so worth a quick count of IHG hotels with extra languages or a non-"en" default first. Either way, can we put an owner and date on the run before this merges?

  Not done: no prod query for how many IHG hotels carry extra languages or a non-en default; no tests run (read-only investigation).
project: null
source_id: https://linear.app/canary-technologies/issue/ENT-8207
tags:
- morning-gtd
- linear
- from-awareness
time_minutes: 20
title: 'Look at ENT-8207: confirm the IHG base-config re-run is planned with the pt-BR
  language add'
updated: 2026-11-10 15:56:50.293558
waiting_on: null
waiting_since: null
working_on: false
---

Tincho is keying the IHG Brazilian Portuguese strings as pt-BR (PR #63973, In Progress). His heads-up: adding a language marks every IHG hotel unhealthy until a base-config re-run reaches it.
https://linear.app/canary-technologies/issue/ENT-8207