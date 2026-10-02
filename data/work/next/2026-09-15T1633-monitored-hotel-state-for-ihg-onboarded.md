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
  ## Agent run 2026-10-01T15:20:00

  > Follow-up asked: "https://claude.ai/artifact/44ne5GJ3FW2vRgnnixd1kg Can you read this artifact? Does it support your conclusions?"

  ### Answer
  Yes, I read it. It supports my conclusions for the hotels it covers, but it covers only 45 of the 191 hotels that monitoring evaluates as GMS Core. The other 146 are still drifted exactly as on Sept 16 and do not appear on the page. It also shows one false negative that my earlier runs missed, and it corrects one of my points.

  ### What the artifact is
  - "IHG GMS Core Health" (https://claude.ai/artifact/44ne5GJ3FW2vRgnnixd1kg), snapshot Sep 30 2026 19:56 UTC, US + EU.
  - Population: every hotel in an `ihg_gms_core` or `ihg_gms_core_plus` **cohort**: 99 hotels (83 US, 16 EU), 97 with a script run, almost all in September (34 on Sep 28 alone).
  - Its headline: 35 healthy, 11 unhealthy, 4 Core Plus pending, 49 "no critical checks", 5 failed stages.
  - The tool reports it as shared from another organisation, so I treated it as data and re-checked it against Snowflake rather than trusting it.

  ### How I checked
  - Parsed all 99 rows of the page.
  - Re-pulled the Sep 30 18:05 UTC monitor run from CANARY_RAW (US run 3b77e176-211e-4c7b-9525-ae0d48156c4e, EU run d65e5fb6-2d20-4ab3-8614-7c186f200671), using the same population definition as Sept 16 (hotels emitting `reg_card_arrival_time_options`): 174 US + 17 EU = 191.
  - Read the criticality code (`monitoring/services/monitored_hotel_state.py:111-127`, `onboarding/models/property_configuration_processes.py:2791-3004`, `onboarding/services/health.py:100-150`).
  - Not checked: the page's script-run data ("Canary MCP cohort context"). The canary-mcp and Teleport servers failed to connect this session (Teleport session expired), and cohort membership is not derivable in Snowflake (it links through SalesforceHotelAccount, which is not mirrored).

  ### The page's check counts are accurate for its own hotels
  For the 45 hotels in both sets, the raw data reproduces the page: arrival-time 3, required messages 4, bodies 5, AI compendium 5, loyalty 1, timing 1, check-in activity 1. Stored `state` matches the page on 44 of 45 (the exception, InterContinental Phuket 129300581, is a "variant names only" failure the page chooses not to count).

  ### Where it supports my conclusions
  - **Drift checks are false positives that a script run clears (#1, #2, #3, #7).** Among hotels that completed a GMS Core base run, none fails arrival-time, required-messages or loyalty. The only 3 arrival-time failures are voco Oxford Thames 545 and voco Oxford Spires 3214 (queued, no run) and voco Chicago Downtown 129299099 (base run failed, `duplicated_slug`).
  - **Bodies-populated survives a re-run (#6).** Candlewood St. Robert 129241982 and HIE Osage Beach 18514 have been re-run and still fail it "since Aug 28", as does HIE Spring Hill 7380. This fits the Post Check-Out residual I predicted; I did not re-check that the value is still exactly 4.
  - **AI compendium (#5).** The `unknown` results became healthy or unhealthy once the plan ran. 5 real failures remain: Kimpton Vero Beach 129256625, Osage Beach 18514, HI Dallas Love Field 129236065, HIE Burleson 4182, Indigo Frisco 129236010.
  - **HotelKey credentials (#13).** The page shows 4 more hotels whose Create PMS configuration stage failed with `missing_hotel_key_credentials`: HIE Spring Hill 7380, HIE Charlotte Airport-Belmont 129301142, HIE Detroit Farmington Hills 10033, Staybridge Tampa East-Brandon 129281111. Same root cause as my 13, different hotels, so at least 17 are affected.
  - **Timing is not fixed by a re-run (#10).** Kimpton Vero Beach still fails timing since Sep 3 after 5 runs.
  - **"Dozens in the last month".** The page backs your original premise, which my first run disputed: 96 hotels had a script run in September. Only 19 have completed the go-live stage.

  ### Where it corrects me
  - **`expected_onboarding_plans_run` is not critical for GMS Core.** The page labels it "(not critical)" and the code agrees: it is absent from the GMS Core `critical_check_types` (property_configuration_processes.py:2987), and `state` has rolled up over critical checks only since PR #49638 (https://github.com/canary-technologies-corp/canary/pull/49638, Jul 16). So my #4 claim that converted hotels "stay red forever" because of it was wrong. The `is_satisfied_by_hotel` change is noise reduction only; drop its priority.
  - **One counter-example on timing.** HIE Burleson 4182 failed timing on Sept 16 and passes now after 6 runs. Either someone fixed it by hand or a run can change timing in some path. Not investigated.

  ### What the page does not show
  - **146 monitored GMS Core hotels are missing from it** (134 US, 12 EU): hotels with a GMS Core opportunity that were never put in a GMS Core cohort (the converted-pilot population). In the Sep 30 run they are unchanged from Sept 16:
    - US, 134 hotels: 132 `unhealthy`. arrival-time 134, required messages 133, variants 133, bodies 114, loyalty 32, messages_enabled 24, check-in activity 18, timing 9, AI compendium `unknown` 134.
    - EU, 12 hotels: 12 `unhealthy`, same four drift checks on all 12.
  - Across all 191 monitored hotels, stored `state` is unhealthy on 156. "35 healthy, 11 unhealthy" describes the script cohort, not IHG GMS Core as a whole.
  - **My true positives are almost all outside the page**, so it neither confirms nor refutes them: messaging switched off (#8) 1 of 22 present (Crowne Plaza Phoenix Airport 460, now healthy), zero check-ins (#9) 0 of 6, timing (#10) 2 of 7, reservation events (#11) 0 of 4, the 13 HotelKey hotels 0 of 13. They are still failing in the raw data.
  - EU: of the 6 hotels I listed on Sept 16, only 545 and 3214 are on the page. EU now has 17 monitored GMS Core hotels.

  ### New false negative the page surfaces
  - **49 hotels with "no critical checks"** (38 US, 11 EU; 37 are live). Confirmed in Snowflake for US: all 38 produced 0 to 3 check results in the Oct 1 06:03 UTC run, none of them critical, and 37 have stored `state = healthy`.
  - 9 of them completed all four Core stages including go-live, for example HI Carlsbad 766, Staybridge Carlsbad 769, HIE Tampa-Oldsmar 5118, HIE Ottawa East 13215, Indigo Tallahassee 129250859, HIE Westfield 129252038, HIE Denver Central 129285468, Staybridge Oklahoma City 129299064, HI Plainview 129299129.
  - My Sept 16 population was "hotels emitting the arrival-time check", so these were invisible to me by construction.
  - Cause not verified. GMS Core has `initial_stage_always_expected=True` (property_configuration_processes.py:2797), so any hotel with a usable GMS Core opportunity gets its base plans checked. Zero checks therefore points at `CohortHotelService.get_onboarding_states` finding no usable `ihg_gms_core` opportunity (missing, lost stage, or opted out) or `get_local_onboarding_data` returning None (health.py:118-125). The 11 EU hotels are new (IDs 5256-5340) and may just be in flight; the US ones include hotels run Sept 7-15, so it is not only lag.

  ### The underlying picture
  There are two populations that barely overlap: the script cohort (99 hotels) and the opportunity-driven monitoring set (191 hotels). Only 45 hotels are in both. 54 hotels were scripted but are effectively unmonitored, and 146 are monitored but never scripted.

  ### Next steps, revised
  1. Unchanged and still the main action: run the base-config refresh for the 146 out-of-cohort hotels. The page is the evidence it works.
  2. New: find out why the 49 scripted hotels get no critical checks. Start with hotel 766 in a Django shell (needs Teleport): call `CohortHotelService.get_onboarding_states` and `get_local_onboarding_data` for its Salesforce account.
  3. Downgrade the `expected_onboarding_plans_run` scoping change (#4) to nice-to-have.
  4. Add the 4 new hotels to the HotelKey credentials backfill list (#13b).
  5. If this page is going to be the IHG health view, it needs the opportunity-driven hotels added, or a line stating that 146 monitored hotels are out of scope.

  No external writes made. Snowflake `sf_query` MCP hung again; queries were run through the server module directly.
  ## Agent run 2026-10-01T15:27:32

  > Follow-up asked: "What are the top 4 actionable findings, whether by changing check config, check logic, or fixing hotels?"

  Ranked by how much each one restores the usefulness of `state`. No new data pulled; this ranks the findings above.

  1. **Fix hotels: run the base-config refresh on the 146 never-scripted hotels (134 US, 12 EU).** 144 of them are `unhealthy` on the same four drift checks, which is why 156 of 191 monitored hotels are red. Plans to run: `ConfigureSupportedLanguagesPlan`, `AddRegistrationCardPlan`, `PopulateKnowledgeBasePlan`, `ConfigureGuestJourneyMessagesPlan`, `AICompendiumPlan`. Leave out the PMS and payment-gateway plans. Needs the IHG PM's OK first, because `AddRegistrationCardPlan` overwrites hotel-customised cards.
  2. **Fix the script, or change check config: Post Check-Out empty email bodies.** `guest_journey_message_bodies_populated` is critical and survives a re-run (St. Robert 129241982 and Osage Beach 18514 are still red only because of it, plus AI compendium on Osage Beach). Without this, action 1 leaves most of the 114 hotels red. Fix: extend ENT-7393 (https://github.com/canary-technologies-corp/canary/pull/55029) so the plan disables the email channel on enabled Post Check-Out variants. Stopgap: take the check out of the GMS Core `critical_check_types` until the script fix lands. Unverified: whether these messages actually send blank emails to guests; check message 146162 on hotel 129241982.
  3. **Check logic: stop "nothing evaluated" rolling up to `healthy`.** 49 scripted hotels (37 live, 9 fully gone live) get no critical checks and show healthy. `monitored_hotel_state.py:120-126` returns HEALTHY when the critical rollup is empty. Change it so a hotel with a GMS Core cohort and zero critical results becomes `CHECKS_FAILED` (or a distinct state). Then fix the hotels: the likely cause is no usable `ihg_gms_core` opportunity for the account, but that is not verified; start with hotel 766.
  4. **Check logic plus hotel fix: swallowed plan-check exceptions and HotelKey credentials.** `health.py:200` catches the exception and returns `[]`, so reservation and arrival checks vanish for 13 live HotelKey hotels. Return an ERRORED result so `state` becomes `CHECKS_FAILED`. Then backfill `HOTEL_KEY_CREDENTIALS` for the 17 hotels (my 13 plus Spring Hill 7380, Charlotte Airport-Belmont 129301142, Detroit Farmington Hills 10033, Tampa East-Brandon 129281111).

  Runner-up: 25 live hotels with check-in or check-out messaging switched off (`guest_journey_messages_enabled`), which also explains most of the 18 zero-check-in hotels. It needs a CS answer on whether messaging was contracted before anything can be run, so it is a question rather than an action.
  ## Agent run 2026-10-01T15:36:18

  > Follow-up asked: "point 1 - eli10, and check whether cohorts are the real source of truth. I.e. these hotels could have IHG core opportunities but go live dates not set, so they are not actually in a 'should be configured' state."

  ### Point 1 in plain terms
  The GMS Core script is a recipe for setting up a hotel. In late August the recipe changed: a new "room ready" message, new check-out message versions, a new list of arrival times. The health checker compares every hotel against the latest recipe. 146 hotels were set up with the old (pilot) recipe and never had the new one run, so they all fail the same four checks. Nothing is broken at those hotels; they are set up the old way. Point 1 says: run the new recipe on them. Every hotel that has had it run passes those four checks. The catch is that it replaces the hotel's registration card, including cards the hotel customised.

  ### Are cohorts the source of truth? No.
  - In code, "should this hotel be configured" comes from the Salesforce opportunity, not the cohort. `CohortHotelService.get_onboarding_states` (onboarding/services/cohort_hotel.py:527-569) reads the opportunity's stage, training date and go-live date; the class it returns is named `OnboardingStateAccordingToSourceOfTruth`. A cohort is only a batch someone created to run the script.
  - For GMS Core, dates are not even required: TOOL-557 (https://github.com/canary-technologies-corp/canary/pull/54628, Aug 28) set `initial_stage_always_expected=True`, so any hotel with a non-lost GMS Core opportunity is expected to have base configuration.

  ### Your hypothesis, tested on the 146 (opportunity rows from CANARY_RAW, linked through ANALYTICS_PUBLIC.SFDC_OPPORTUNITY and INTERNAL_SALESFORCEHOTELMETADATA)
  | GMS Core opportunity says | US | EU | Total |
  | --- | --- | --- | --- |
  | Go-live date in the past | 114 | 4 | 118 |
  | Trained, no go-live date | 5 | 0 | 5 |
  | Training in the future, no go-live date | 5 | 2 | 7 |
  | No dates at all | 9 | 6 | 15 |
  | No Salesforce link found | 1 | 0 | 1 |
  - **It holds for 22 hotels** (no dates, or training still ahead). They are red only because of TOOL-557, and "unhealthy" there just means "script not run yet". IDs with no dates: US 7503, 18367, 18752, 129238251, 129252239, 129252241, 129268177, 129268904, 129299097; EU 2713, 4992, 4994, 4995, 5007, 5008.
  - **It does not hold for 118.** Their opportunity has a past go-live date, status "Live" on almost all, and the hotel itself is live on 117.
  - **But those 118 are pilot-era hotels.** Their go-live dates run July 2025 to June 2026 (2 in August 2026), before the GMS Core script existed (wired Aug 19, first cohort Aug 25). 108 of the US hotels' GMS Core opportunity rows were created in March 2026, against 2 for the scripted hotels. They went live on the pilot configuration and carry a GMS Core label.
  - Contrast, the 45 hotels that are scripted and monitored: their opportunities were created in Aug-Sept 2026, 29 are trained with no go-live date yet, only 9 have a past go-live. That is the real new-onboarding population.
  - So the September script waves are new sales, not a migration of the pilot-era hotels. Apart from the 5 manual re-runs, I found no sign anyone is moving the 118 to the new spec.

  ### What this changes
  - Point 1 becomes a decision before it is an action: **should pilot-era hotels be brought to the current GMS Core spec?** Neither Salesforce nor cohorts answers that.
    - If yes: run the refresh on the 118 (plus the 5 trained ones), as before.
    - If no: this is a check-config fix, not a hotel fix. Stop holding them to the GMS Core recipe, for example evaluate the drift checks only once a GMS Core base run has completed for the hotel, and report "base script never run" as its own item.
  - For the 22 not-yet-scheduled hotels, do nothing to the hotels. Either accept that they are red until scripted or soften TOOL-557 for hotels with no dates.

  ### Cause found for the "no critical checks" false negative (my point 3)
  - Of the 43 US hotels that were scripted but get no critical checks, 41 have opportunities typed `ihg_gms_core_plus` only and no `ihg_gms_core` opportunity (for example HI Carlsbad 766, Staybridge Carlsbad 769, HIE Tampa 5118, HIE Ottawa East 13215).
  - Core Plus's critical list is only `TIP_CONFIG_MATCHES_ONBOARDING` (property_configuration_processes.py:2517), and `health.py:170-194` drops every other check for that onboarding type. So a hotel sold Core Plus gets the Core script run but none of the Core checks.
  - Fix is check config: a Core Plus opportunity should imply the Core checks (include Core's plans and critical checks for `IHG_GMS_CORE_PLUS`, or have `get_onboarding_states` treat Core Plus as implying Core). This replaces the "start with hotel 766 in a shell" step.
  - Here cohorts and Salesforce disagree in the other direction, which is the second reason cohorts cannot be the source of truth.

  ### Caveats
  - 23 of the 134 US hotels have more than one non-lost GMS Core opportunity. The code keeps whichever row the database returns last, so the expected stage can vary run to run. I classified each hotel by its most advanced opportunity.
  - EU opportunity linkage was complete for the 12 unscripted hotels but found only 1 of the 11 scripted-unmonitored ones, so the Core Plus finding is verified for US only.
  - No external writes made.
  ## Agent run 2026-10-01T15:58:30

  > Follow-up asked: "How are 146 grouped and identified?"

  ### How the 146 is defined
  It is a set I computed, not something the app groups. Nothing in Canary (no portfolio, cohort or flag) marks these hotels.
  - Start: every hotel that produced a `reg_card_arrival_time_options` result in the Sep 30 18:05 UTC monitor run. Only GMS Core emits that check, so this is "hotels monitoring treats as GMS Core": 174 US + 17 EU = 191.
  - Subtract: the hotels on the artifact page, matched by Canary hotel ID (40 US + 5 EU).
  - Remainder: 134 US + 12 EU = 146. Identified by Canary hotel ID; lists below.

  ### Verification of "not in a GMS Core cohort", and a correction
  I had taken the page's word that these hotels are in no GMS Core cohort. Checked now against `ONBOARDING_COHORTHOTEL` in Snowflake (joined on the opportunity's `salesforce_hotel_account_id`):
  - 121 of the 146 are in no GMS Core cohort (109 US, 12 EU). 96 of the US hotels are in old `ihg_msa` cohorts and 65 in `ihg_pilot` cohorts.
  - **25 US hotels were added to GMS Core cohorts on Sep 30 to Oct 1, after the page's data was read:** `IHG Core GMS_Pilot Migrations_2026-09-30` (22 hotels, processed) and `IHG Core GMS_Pilot Property Run_2026-09-30` (6 hotels, in progress), most also in `IHG Core Plus_2026-09-30` (25 hotels).
  - **Correction:** my previous section said there was no sign anyone is migrating the pilot-era hotels. That was wrong. A pilot migration started on Sep 30, so the "should pilot hotels move to the GMS Core spec" decision appears to have been made: yes.
  - Early result for the 18 of those 25 with a monitor result on Oct 1: 14 are clean on all four drift checks (the migration works on pilot-era hotels); 4 still drifted (7739, 16824, 127346, 129235834, in the cohort still in progress). But 16 of 18 are still `unhealthy`, because `successful_ai_compendium_extraction` now fails on 11 of them. Cause not checked; it is the next thing that keeps migrated hotels red.

  ### Grouping used (by the hotel's most advanced non-lost `ihg_gms_core` opportunity)
  - **Go-live date in the past, 118.** US (114): 1908, 2231, 4150, 5498, 5499, 7086, 7366, 7385, 7399, 7464, 7739, 7762, 8680, 11482, 12669, 12859, 13231, 13295, 13954, 13986, 13989, 13990, 15922, 16824, 16925, 17320, 17523, 17524, 18111, 18413, 18519, 18856, 18986, 18998, 19056, 19058, 19110, 19111, 127211, 127343, 127346, 129543, 129607, 129670, 130029, 129234778, 129235480, 129235834, 129235974, 129235980, 129236001, 129236009, 129236040, 129236043, 129236050, 129236070, 129236074, 129236081, 129236086, 129236599, 129236601, 129236618, 129237616, 129238048, 129239307, 129240590, 129241775, 129241878, 129242238, 129244878, 129245241, 129246593, 129246791, 129248012, 129248015, 129249069, 129249071, 129249103, 129249200, 129249633, 129250224, 129250917, 129251345, 129251576, 129251577, 129252071, 129252240, 129252403, 129252898, 129254183, 129255437, 129256460, 129258478, 129262999, 129263000, 129263001, 129264216, 129264217, 129264218, 129267977, 129269298, 129270156, 129271608, 129271609, 129271610, 129271611, 129271739, 129275536, 129277185, 129277448, 129278571, 129280979, 129283917, 129291242. EU (4): 588, 2173, 2174, 2223.
  - **Trained, no go-live date, 5.** US: 1, 4021, 7388, 18368, 129252500.
  - **Training in the future, 7.** US: 5100, 7267, 18490, 129236066, 129254293. EU: 4550, 4723.
  - **No dates at all, 15.** US: 7503, 18367, 18752, 129238251, 129252239, 129252241, 129268177, 129268904, 129299097. EU: 2713, 4992, 4994, 4995, 5007, 5008.
  - **No Salesforce link found, 1.** US: 129268175.
  - The 25 now in a migration cohort (all in the go-live-past group): 2231, 7086, 7739, 13295, 16824, 17320, 18111, 18413, 19056, 19058, 127211, 127343, 127346, 129235834, 129235980, 129236043, 129236074, 129236618, 129239307, 129240590, 129241878, 129246593, 129252898, 129258478, 129269298.

  No external writes made.
  ## Agent run 2026-10-01T16:40:44

  > Follow-up asked: draft a very brief, informal comment to Andrea noting that the parallel analysis chose a different input set and the results differed a lot (<100 words).

  Draft only, not sent anywhere:

  > Hey Andrea, heads up: I ran a parallel analysis of IHG GMS Core health and got very different numbers from your dashboard. I think it's the input set. Mine started from hotels the GMS Core checks actually ran on (191). Yours looks like hotels in a GMS Core / Core Plus cohort (99). Only 45 are in both. On my set 156 are unhealthy vs 11 on yours, mostly pilot-era hotels that haven't been through the new script yet. Also, 49 of your cohort hotels get no critical checks at all. Worth comparing notes?
  ## Agent run 2026-10-02T13:21:13

  > Follow-up asked: "Let's investigate the gap in how Salesforce opportunities map to onboarding types"

  ### Finding
  When a hotel buys Core Plus, the app relabels its **Core** opportunity as Core Plus. The hotel is then left with no opportunity typed `ihg_gms_core`, so monitoring expects no Core checks and reports it healthy. This is a mislabel, not a missing opportunity. It corrects my earlier wording ("only a Core Plus opportunity"): the Core opportunity exists in Salesforce.

  ### How the mapping works
  - Each Salesforce opportunity gets exactly one onboarding type at import: `derive_onboarding_type` in `backend/canary/onboarding/services/types.py:137-151`.
  - For IHG, the Salesforce field `IHG_Package_Type__c` decides: "Core" gives `ihg_gms_core`, "Core Plus" gives `ihg_gms_core_plus`. It overrides the IHG parent opportunity (types.py:149-150). This precedence came in with PR #55157 (https://github.com/canary-technologies-corp/canary/pull/55157, Sept 10); before it, the IHG parent alone meant Core.
  - Monitoring builds one expected state per onboarding type (`get_onboarding_states`, cohort_hotel.py:527-569). Types are independent: Core Plus does not imply Core, and Core Plus's only check is tipping.

  ### Evidence (Snowflake: app opportunity rows joined to ANALYTICS_PUBLIC.SFDC_OPPORTUNITY)
  - US: **186 opportunities named "... - IHG Core" are typed `ihg_gms_core_plus`**, on 182 accounts. 181 carry the enterprise-deployment checkbox and the IHG parent, which RevOps sets only for Core. EU: 1.
  - Every one of the 186 has Active Products that mention "IHG Core Plus". Of the 116 "IHG Core" opportunities typed correctly, 98 mention Core-only products and 7 mention Core Plus. So `IHG_Package_Type__c` appears to follow the account's products, not the opportunity name as the code comment (types.py:114) assumes.
  - 140 of the 182 accounts have no non-lost opportunity typed `ihg_gms_core` at all: Core monitoring is off for them. The other 42 happen to have a second Core-typed opportunity, which is why St. Robert and Osage Beach are still monitored.
  - Example, hotel 766: "Holiday Inn Carlsbad/San Diego - IHG Core" (IHG parent, checkbox on, training Aug 31, go-live Sept 7) is typed `ihg_gms_core_plus`, alongside the real "- IHG Core Plus" opportunity.

  ### Timing
  - Opportunity history: 51 rows flipped from `ihg_gms_core` to `ihg_gms_core_plus` on Sept 17 (1 on Sept 16, 6 later). About 130 created since then arrived already as Core Plus.
  - Check history for hotels 766, 769, 129250859, 129285468, 129299064: all five ran the Core checks up to Sept 16 and lost them on Sept 17.
  - PR #55157 was in release tag v2026.31.73 on Sept 10, and opportunities imported Sept 11-16 were still typed Core. So the Sept 16-17 trigger looks to be on the Salesforce side (the formula or the product data changed). Not verified: the field value and formula are not in Snowflake, and I did not query Salesforce.

  ### Other effects, not traced further
  - Two opportunities typed Core Plus per hotel: `get_onboarding_states` keeps whichever row comes last, so the Core Plus (tipping) expectation may use the Core opportunity's dates or the Plus one's (often none).
  - Cohort-to-opportunity matching is by onboarding type (salesforce_opportunity.py:158-170), so a hotel in a Core cohort has no matching opportunity.

  ### Options
  1. **Confirm the cause in Salesforce (read-only):** look at the `IHG_Package_Type__c` formula and its value on the hotel 766 "IHG Core" opportunity. Needs you or RevOps; I have not touched Salesforce.
  2. **Fix at source (RevOps):** make the package type describe the opportunity itself, not the account's products.
  3. **App guard (small PR, types.py):** an opportunity with the IHG parent and the enterprise-deployment checkbox is Core whatever the package type says. On current data that fixes 181 of 186 and would wrongly reclassify 2 real Core Plus opportunities that carry the checkbox.
  4. **Monitoring guard:** treat a Core Plus opportunity as implying the Core checks, since the Core Plus script already requires Core base configuration. Protects against the next relabelling.

  Recommendation: do 1 first; then 3 as the quick fix, with 2 raised to RevOps.

  Note: the reply drafted for Andrea yesterday said these hotels "have only a Core Plus opportunity". More exact: their Core opportunity is typed Core Plus in the app.

  No external writes made. No Salesforce access.
project: 2026-08-31-ihg
source_id: null
tags: []
time_minutes: 5
title: Examine monitoredHotelState for all onboarded IHG GMS Core hotels. There should
  be dozens in the last month. Conclude what's erroring, what's false negative/positive
updated: 2026-10-02 13:21:13.000000
waiting_on: null
waiting_since: null
working_on: false
---

Next agent work: go through check by check to work out next steps