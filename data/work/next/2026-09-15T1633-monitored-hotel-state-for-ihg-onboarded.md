---
area: null
completed_at: null
contexts: []
created: 2026-09-15 16:33:21.670612
defer_until: null
due: null
energy: low
id: 2026-09-15T1633-monitored-hotel-state-for-ihg-onboarded
order: null
output: |
  ## Agent run 2026-09-16T09:10:05

  ### Scope and caveats
  - Data source: Snowflake CDC mirror CANARY_RAW.CANARY (US region only). The canary-mcp-* Teleport servers were down (session expired), so EU/AP were NOT examined. Run `tsh login` and re-run for a full picture.
  - Cohort: 256 `ihg_gms_core` SalesforceOpportunity rows in US; 118 have no Canary hotel yet; ~110 hotels received checks in the latest cron_monitor_hotels run (2026-09-16 00:00–03:00 UTC, run uuid 23d3416b-5350-4443-8cf4-6d3c2088b223).
  - "Dozens onboarded in the last month" does not hold in US: only 12 GMS Core opps have go_live_date >= 2026-08-16 (all Sept 3–10), 1 in August. Most GMS Core MonitoredHotelState rows were created Feb–Apr 2026 (bulk conversion). EU/AP may add more.

  ### Headline
  Every monitored IHG GMS Core hotel except ~4 is `unhealthy`. 104 of 110 fail the same four config checks in lockstep, and the flip happened on **2026-08-28** (variants_configured 10→102, specified_messages_all_enabled 3→102, reg_card_arrival_time_options appeared at 102/102, compendium_extraction appeared as 102 unknown). That is script drift from the Aug 21–31 GMS Core script changes, not per-hotel breakage. The aggregate `state` is therefore currently useless for spotting real regressions.

  ### FALSE POSITIVES (script drift; a base-config re-run clears them — proven by the 5 hotels re-run since Aug 31: Candlewood St. Robert 129241982, HIE Osage Beach 18514, HI Greensboro Coliseum 129240128, HI Dallas Love Field 129236065, HI Resort Kissimmee 16014, which are clean on all four)
  1. `specified_guest_journey_messages_all_enabled` — 104/110. Missing use case is `room_ready_message` for all; added to the script by ENT-7016 (https://github.com/canary-technologies-corp/canary/pull/54070, Aug 26). Existing hotels never got it.
  2. `guest_journey_message_variants_configured` — 104/110. `room_ready_message: message_not_found` plus `pilot_checkout` missing the Club/Loyalty/Non-members variants introduced by ENT-7318 (https://github.com/canary-technologies-corp/canary/pull/54174, Aug 26).
  3. `reg_card_arrival_time_options` — 104/110. Check added by ENT-6979 (https://github.com/canary-technologies-corp/canary/pull/53731, Aug 21) and requires exact list equality with the new 30-option list. Found: 53 hotels on a custom 18-option list starting 3:00 PM, 14 on the older 24-option list, 4 on the previous 30-option list starting 9:00, 9 with no arrival-time element at all, rest misc. Also note TOOL-557 (https://github.com/canary-technologies-corp/canary/pull/54628, Aug 28: expect base configuration whatever the dates say) is why these checks now run on every hotel incl. pre-live ones.
  4. `expected_onboarding_plans_run` — 105/110 (was already 95/99 in July, so partly pre-existing). Missed plans: ConfigureSupportedLanguagesPlan (ENT-7060 https://github.com/canary-technologies-corp/canary/pull/54513), PopulateKnowledgeBasePlan (ENT-7204 https://github.com/canary-technologies-corp/canary/pull/54072), AICompendiumPlan (ENT-7206 https://github.com/canary-technologies-corp/canary/pull/54674) on essentially all hotels; ConfigurePMSIntegrationCreate/Validate + ConfigurePaymentGatewayIntegrationPlan on ~87 hotels (converted from IHG pilot, never ran under GMS Core); GoLivePlan missing on 23 hotels Salesforce says are Live (went live under the pilot).
  5. `successful_ai_compendium_extraction` — 104 `unknown` ("No extraction has finished for this hotel yet"; plan added Aug 31 by https://github.com/canary-technologies-corp/canary/pull/54674 / check by TOOL-557 https://github.com/canary-technologies-corp/canary/pull/54096). `unknown` does not affect `state`, so harmless but noisy. 2 genuine unhealthy: Kimpton Vero Beach (url_unreachable on ihg.com page) and one existing_unmanaged_content skip.
  6. `guest_journey_message_bodies_populated` — 97/110, steady ~88 since July (so NOT part of the Aug 28 flip). Value ≈14 per hotel: Welcome Message email-channel variants (First-time Non-members, Returning Non-members, ...) enabled with empty bodies. One root cause in the script provisioning, not 97 hotel problems. Needs a decision: is email meant to be enabled on those variants? If not, fix the script and re-run; if yes, it is a real content gap.

  ### Probably TRUE POSITIVES (worth triage)
  - `regn_card_configured_for_loyalty` — 20 hotels (11 in July → 18 on Aug 28 → 20 now). Loyalty checkbox missing on the check-in card. The rise coincides with the reg-card overwrite PRs ENT-7365 (https://github.com/canary-technologies-corp/canary/pull/54681) / https://github.com/canary-technologies-corp/canary/pull/54758; check whether the overwrite drops the loyalty element on some cards. One hotel has no check-in card at all.
  - `guest_journey_messages_enabled` — 16 Live hotels where has_check_in/out_messages does not match the GoLive config.
  - `guest_journey_message_timing_configured` — 7 hotels (3× pilot_checkout sends 9:00 vs expected 8:00; others check_in_message delta/time drift).
  - Operational: `check_in_n_completed_last_7_days`=0 on 8 Live hotels; `reservation_events_last_24_hours` false on 3 (PMS sync present, no events); arrivals 0 on ~2.
  - `tip_config_matches_onboarding` unhealthy on HIE Osage Beach 18514 (Core Plus check surfacing on a hotel with both Core and Core Plus opps).

  ### FALSE NEGATIVES
  - Swallowed check exceptions: `OnboardedPropertyHealthService.check_onboarding_plan_against_hotel` (backend/canary/onboarding/services/health.py ~line 200) catches Exception, logs `check_onboarding_plan_against_hotel.error` at warning, and returns [] — the plan's checks simply vanish, no ERRORED result, state never becomes CHECKS_FAILED. Overnight run (Groundcover, c-monitor-hotels): 14 IHG GMS Core hotels affected in us-west-2 (13 on ConfigurePMSIntegrationCreateConfigurationPlan: HIE Fishkill, HIE&S Yuma, HIE&S Chester, HIE&S Sterling, HIE Sheboygan-Kohler, Candlewood Austin Airport, HIE&S Peru-Lasalle, HIE&S Jacksonville SE, Staybridge Columbia Baltimore, HIE&S Montrose, HIE&S Bessemer, HIE&S Salinas, Candlewood Bessemer; plus "Stacy Test Account 1" on ConfigureGuestJourneyMessagesPlan). Same 12+1 the day before, so it is stable. Across all brands: 57 us-west-2 + 29 eu-central-1 per run. Also 70 `conformity_check_error` ("Invalid Salesforce ID length: 14") in EU — not IHG.
  - `MonitoredHotelState.go_live` is NULL on 31 of 107 Salesforce-Live GMS Core hotels; it is only stamped by a completed GOLIVE batch (onboarding_batch.py ~1058) and converted pilot hotels never ran one. Where it is set, "first go-live wins" so it shows the Feb 2026 pilot date, not the GMS Core go-live. Any go-live-based reporting off this field undercounts.
  - Because ~all hotels are already UNHEALTHY from the drift above, a genuine new failure on any hotel changes nothing visible. That is the practical false negative today.

  ### Suggested actions (none taken)
  1. Re-run BASE_CONFIGURATION_NEW for the ~104 drifted US hotels (the re-run hotels prove it clears checks 1–4), or explicitly baseline: make room_ready optional / accept the older option lists until re-run.
  2. Make `check_onboarding_plan_against_hotel` return an ERRORED result instead of [] so swallowed exceptions surface as CHECKS_FAILED; then fix why ConfigurePMSIntegrationCreateConfigurationPlan.check raises for those 13 hotels.
  3. Scope `expected_onboarding_plans_run` to plans in stages that actually ran for the hotel's onboarding path (converted pilot hotels will otherwise stay red forever).
  4. Decide the Welcome Message email-variant question (check 6) and the loyalty-checkbox regression (reg-card overwrite PRs).
  5. Repeat this analysis for EU/AP once Teleport is re-logged.
  ## Agent run 2026-09-16T09:24:00

  Check-by-check next steps, grounded in the code (`backend/canary/onboarding/services/health.py`, `plans/configure_guest_journey_messages.py`, `configuration_providers/ihg/*`) and a fresh Snowflake pull of the 2026-09-16 00:00 UTC run (uuid 23d3416b-5350-4443-8cf4-6d3c2088b223). No external writes made.

  ### Corrections to the first run
  - US cohort is **174** monitored GMS Core hotels (every hotel emitting `reg_card_arrival_time_options` in that run), of which **117** are Salesforce-live (the GoLive checks only run on those). The earlier "110" undercounted. 30 hotels are already clean on the drift checks (the Sept 3–10 creations plus the 5 manual re-runs), 22 have a fully `healthy` state.
  - **EU examined via Snowflake** (Teleport MCPs still down, but `sf_query region=eu` works): 6 GMS Core hotels, all UK (voco Oxford Thames 545, Crowne Plaza London Docklands 588, Holiday Inn Oxford 2173, Crowne Plaza Birmingham NEC 2174, HIE London Southwark 2223, voco Oxford Spires 3214). All 6 fail exactly the same 4 drift checks + bodies_populated (14–15) + missed plans; Southwark also fails loyalty and messages_enabled (no GoLivePlan). Same fix applies. **AP: zero GMS Core hotels.**
  - Pre-live hotels do **not** self-heal: `trained_stage` only widens what health.py *expects* (health.py:65); nothing creates a BASE_CONFIGURATION_NEW batch at training time (cohorts.py only creates `initial_stage` batches at creation). So the 32 pre-live drifted hotels stay drifted until someone re-runs them.

  ### 1. `reg_card_arrival_time_options` — 144/174 unhealthy (112 live, 32 pre-live) — FALSE POSITIVE
  - Cause confirmed: exact-list equality against `GMS_CORE_ARRIVAL_TIME_OPTIONS` (gms_core_ihg_registration_card_provider.py:447); cards written before ENT-6979 (Aug 21) can never match.
  - Fix: re-run `AddRegistrationCardPlan`. 0 of the 30 re-run hotels fail it. No code change needed.
  - Caveat to confirm with the IHG PM before running at scale: since #54758 the plan overwrites *customized* cards too (legacy layout kept as `legacy schema`). Running it on 112 live hotels will replace any hotel-edited card. That is the ENT-7365 decision, but it has only been exercised on 5 live hotels so far.

  ### 2. `specified_guest_journey_messages_all_enabled` — 143/174 — FALSE POSITIVE
  ### 3. `guest_journey_message_variants_configured` — 143/174 — FALSE POSITIVE
  - Both are `room_ready_message` (ENT-7016) + `pilot_checkout` variants (ENT-7318) missing on pre-Aug-26 hotels. Re-running `ConfigureGuestJourneyMessagesPlan` clears both (30/30 re-run hotels clean). Timing is untouched by a re-run (plan sets delta/send_time only on creation, configure_guest_journey_messages.py:1404–1433), so this is safe for hotel-customised schedules.

  ### 4. `expected_onboarding_plans_run` — 147/174 — MIXED, needs a code change
  Three distinct populations inside the one check:
  - **Base-stage plans never run** (`ConfigureSupportedLanguagesPlan`, `PopulateKnowledgeBasePlan`, `AICompendiumPlan` on ~140 hotels): cleared by the refresh rollout below.
  - **PMS + payment gateway plans** (`ConfigurePMSIntegrationCreateConfigurationPlan`, `...ValidatePlan`, `ConfigurePaymentGatewayIntegrationPlan` on ~87 converted-from-pilot hotels): these were configured by hand and must NOT be re-run blindly. `ConfigurePaymentGatewayIntegrationPlan._reset_if_vendor_mismatch` (configure_payment_gateway_integration_plan.py:46) resets a hotel's gateway if it isn't FreedomPay; the PMS provider raises for HotelKey hotels without credentials (see #14). They will stay "missed" forever.
  - **`GoLivePlan` missing on 43 live hotels** (went live under the pilot).
  - Recommended fix (TOOL ticket): give `OnboardingPlan` an optional `is_satisfied_by_hotel(hotel) -> bool` classmethod and have `OnboardedPropertyHealthService.check()` (health.py:118) consult it before adding to `missed_onboarding_plans`. Implement for the three PMS/payment plans (PMS gateway account exists with the expected vendor config; `check_in_configuration.payment_gateway_config_id` set) and `GoLivePlan` (`hotel.is_live`). Keeps the check honest for new hotels, stops converted hotels being red forever. Alternative if that is too much: report those plans under a separate `not_applicable_plan_names` key without affecting outcome.

  ### 5. `successful_ai_compendium_extraction` — 144 unknown / 3 unhealthy / 27 healthy — NOISE + 3 real
  - `unknown` does not affect state; the refresh rollout runs `AICompendiumPlan`, which converts them to healthy/unhealthy.
  - Real: Kimpton Vero Beach 129256625 (`url_unreachable`, ihg.com page), HIE Osage Beach 18514 (`existing_unmanaged_content`, skip is by design), one more. After the refresh, use the existing `AI_COMPENDIUM` ad-hoc stage on whatever remains unhealthy.

  ### 6. `guest_journey_message_bodies_populated` — 116/174 — FALSE POSITIVE except Post Check-Out
  - Detail (hotel 11482 Sterling, value 14): the *email* channel on every pilot-era variant — Welcome Message ×7, Post Check-Out ×4, Mid-Stay, Pre Arrival, Greener Stay — flagged enabled with no body. Pilot-era `_build_variant_data_list` auto-detected email; the GMS Core provider now forces `override_enable_email=False` on variants (`_with_email_disabled`, since #53730 Aug 20).
  - Re-run fixes all of them **except Post Check-Out**: all 4 re-run hotels still report exactly 4 empties (Non-members / Club Members / Loyalty Members / Default on Post Check-Out, e.g. message 146162 on Candlewood St. Robert). The spec creates Post Check-Out as a placeholder with no variants, and ENT-7393 (#55029) only rebuilds it when the message is *disabled* (`use_cases_to_delete_if_disabled`); on live hotels it is enabled so the pilot variants survive. The send path takes the chosen variant's `is_email_enabled` (scheduled_campaign.py:660), so if these messages are actually sending, guests may be getting blank emails.
  - Next steps: (a) verify on one hotel (129241982, message 146162) whether Post Check-Out is enabled and has sent email recently; (b) extend ENT-7393 so the plan also disables the email channel on enabled Post Check-Out variants (or deletes the segmented variants) — ENT ticket for the GMS Core script owner; (c) until then, expect ~4 per hotel to remain after the refresh.

  ### 7. `regn_card_configured_for_loyalty` — 44/174 — FALSE POSITIVE (cleared by re-run)
  - 0 of the 30 hotels with a post-Aug-21 card fail it; every failure is an old dashboard-default / pilot card. The Aug 28 jump was TOOL-557 widening the population, not the overwrite PRs. Fixed by the same `AddRegistrationCardPlan` re-run as #1. Drop the suspicion of ENT-7365/#54758.

  ### 8. `guest_journey_messages_enabled` (GoLive settings) — 22/117 live — TRUE POSITIVE, product question
  - All 21 named hotels have `has_check_in_messages` and/or `has_check_out_messages` = false; 20 of them also never ran `GoLivePlan` (pilot go-lives). Hotels: Crowne Plaza Phoenix Airport 460, HIE Manchester Airport 5498, HIE Cherry Hills 7464, HIE Santa Ana 129543, HIE Frazier Park 129234778, HIE Dallas Fair Park 129235980 (out off), HIE Red Deer North 129236040 (in off), HIE Sunnyvale 129236043 (out off), HI Erie 129245241, Indigo San Diego Gaslamp 129246791, Staybridge Saskatoon 129248012, HIE Saskatoon East 129248015, HIE Yuma 129249633, voco Moab 129250224 (in off), Indigo Atlanta Airport 129250917, HIE Willmar 129252898 (out off), Crowne Plaza Peachtree City 129271608, HIE Atlanta Airport NE 129271609, HIE Atlanta SW Fairburn 129271610 (out off), HIE Atlanta West 129271611, Staybridge Atlanta Airport 129271739, Candlewood Columbia-Fort Jackson 129280979.
  - Next: ask the IHG CS lead whether these were contracted for messaging. If yes, run the GOLIVE stage for them (GoLivePlan flips the flags and enables the use cases, and stamps `go_live`). If no, the check is correct and this is a contract/data gap to record in Salesforce (by hand).

  ### 9. `check_in_n_completed_last_7_days` = 0 — 16/117 live — TRUE POSITIVE for 6
  - 10 of the 16 have check-in messaging switched off (overlap with #8), so zero check-ins is expected there.
  - 6 have messaging on and still zero: HIE Sterling 11482, Indigo Austin Downtown 17523, HIE Austin Downtown University 17524, Candlewood Austin Airport 129264218, Kimpton Era Midtown 129269298, HIE Plymouth 129283917. Sterling and Austin Airport are in the HotelKey list in #14. Hand to IHG CS for triage.

  ### 10. `guest_journey_message_timing_configured` — 7 — TRUE POSITIVE, needs a decision
  - HIE Burleson 4182, HI Tacoma Mall 18856, HIE The Dalles 129607, HI Philadelphia Airport 129235974, Crowne Plaza Newark Airport 129249071, Kimpton Vero Beach 129256625, InterContinental Fiji 129268177 (plus Crowne Plaza Birmingham NEC in EU). A re-run will not change timing. Either hotels chose these times (then the check must tolerate operator edits, e.g. only compare when the message was never edited after creation) or they are pilot defaults (then reset by hand). Ask CS per hotel; if mostly hotel-chosen, file a TOOL ticket to soften the check.

  ### 11. `reservation_events_last_24_hours` false — 4 — TRUE POSITIVE
  - HIE Taylor 7086, HIE Peru-Lasalle 13989, HI Philadelphia Airport 129235974, Candlewood Austin Airport 129264218. Peru-Lasalle and Austin Airport are HotelKey hotels from #14. PMS-integration triage (HotelKey feed).

  ### 12. Minor: `guest_journey_message_variants_flag` 8 (rollout flag off, refresh sets it), `sso_*` 3, `guest_journey_messages_scheduled` 3, `reservation_arrivals_today` 3, `tip_config_matches_onboarding` 3 (Core Plus drift on Osage Beach: variant 0 vs 1, max tip 10000 vs 20000, review flow — Core Plus owner).

  ### 13. Swallowed check exceptions — FALSE NEGATIVE, cause confirmed
  - Groundcover, us-west-2 overnight run: all 13 `check_onboarding_plan_against_hotel.error` lines for IHG GMS Core have `pms_2__c = "Hotelkey"` and plan `ConfigurePMSIntegrationCreateConfigurationPlan` (Fishkill, Yuma, Chester, Sterling, Sheboygan-Kohler, Candlewood Austin Airport, Peru-Lasalle, Jacksonville SE, Staybridge Columbia Baltimore, Montrose, Bessemer ×2, Salinas). `IHGGmsCorePmsConfigProvider.__init__` calls `_build_hotel_key_configuration`, which raises `ERROR_MISSING_HOTEL_KEY_CREDENTIALS` when there is no `HOTEL_KEY_CREDENTIALS` OnboardingValue (gms_core_ihg_pms_config_provider.py:55–69). health.py:200 catches it and returns `[]`, so `RESERVATION_ARRIVALS_*`, `RESERVATION_EVENTS_LAST_24_HOURS`, `ACCOUNT_GROUPS_MATCH` etc. silently vanish for these 13 live hotels. The 14th is "Stacy Test Account 1" (Zimmer PMS, GJM plan) — ignore.
  - Next steps: (a) TOOL ticket, health.py: log with `exc_info=True`, and add `errored_plan_names` to the `EXPECTED_ONBOARDING_PLANS_RUN` result with outcome `ERRORED` when non-empty so the state becomes `CHECKS_FAILED` (monitored_hotel_state.py:121–126 already maps ERRORED → CHECKS_FAILED). (b) Onboarding: backfill `HOTEL_KEY_CREDENTIALS` OnboardingValues for the 13 (they look like the ENT-6032 HotelKey wave; the credentials must already exist in the PMS gateway). Also note the same swallow hides 57 us-west-2 + 29 eu-central-1 errors per run across Wyndham/BW.

  ### 14. `MonitoredHotelState.go_live` — FALSE NEGATIVE for reporting
  - NULL on 40 of 117 Salesforce-live GMS Core hotels; 43 never ran `GoLivePlan`. `set_go_live` is first-wins (monitored_hotel_state.py:204). Next: management command to backfill `go_live` from the GMS Core `SalesforceOpportunity.go_live_date` where NULL, and make go-live reporting read the opportunity date rather than this field.

  ### Recommended execution order
  1. **Code, one PR each (TOOL):**
     - Rollout recipe `ihg_gms_core_base_config_refresh` in `onboarding/models/rollouts.py`: `plan_names=("ConfigureSupportedLanguagesPlan","AddRegistrationCardPlan","PopulateKnowledgeBasePlan","ConfigureGuestJourneyMessagesPlan","AICompendiumPlan")`, `onboarding_type=IHG_GMS_CORE`, `base_population=LIVE`, `selection_mode=ALL`, `script_type=BASE_CONFIGURATION_NEW`, `stage_sizes=(5,10,500)`. Deliberately excludes the PMS and payment-gateway plans (#4) and HotelInfo/Branding/SSO/Portfolio/MSA (not failing, no reason to touch). Add a `_subset` twin with `NOT_LIVE_SALESFORCE_IDS` for the 32 pre-live hotels. LIVE is valid for IHG_GMS_CORE (the PORTFOLIO-only invariant in `tests/rollouts/test_rollout_recipes.py` is the other direction).
     - health.py errored surfacing (#13a).
     - `is_satisfied_by_hotel` scoping for `expected_onboarding_plans_run` (#4).
     - `go_live` backfill command (#14).
  2. **Run the refresh** stage 1 (5 hotels) in US, wait one monitor run, confirm #1/#2/#3/#7 flip and #6 drops to ~4, then stages 2–3; then EU (6 hotels) and the pre-live subset. Get the IHG PM's OK on the card overwrite before stage 3.
  3. **Hand to CS/PM:** #8 (messaging contracted?), #9 (6 hotels), #10 (7 hotels), #11 (4 hotels), #13b (HotelKey credentials for 13 hotels).
  4. **Script owner (ENT):** Post Check-Out email channel on enabled messages (#6).
project: 2026-08-31-ihg
source_id: null
tags: []
time_minutes: 5
title: Examine monitoredHotelState for all onboarded IHG GMS Core hotels. There should
  be dozens in the last month. Conclude what's erroring, what's false negative/positive
updated: 2026-09-16 09:30:59.866504
waiting_on: null
waiting_since: null
working_on: true
---

Next agent work: go through check by check to work out next steps