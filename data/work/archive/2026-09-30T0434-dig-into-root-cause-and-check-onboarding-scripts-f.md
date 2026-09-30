---
area: null
completed_at: 2026-09-30 13:38:49.535386
contexts: []
created: 2026-09-30 04:34:45.767810
defer_until: null
due: null
energy: low
id: 2026-09-30T0434-dig-into-root-cause-and-check-onboarding-scripts-f
order: null
output: |
  ## Agent run 2026-09-30T13:24:58.871876

  Thread: https://canarytechnologies.slack.com/archives/C0AJ1ENFSSU/p1790703003314659

  ### Root cause (confirmed in code)
  kli's diagnosis in the thread is right. Two things combine:

  1. PR #56163 "VOX-4064 Enable booking link if config exists" (https://github.com/canary-technologies-corp/canary/pull/56163, Arjun, merged 2026-09-11) added to `VoiceConfigurationService.enable()` (backend/canary/voice/services/configuration/voice_configuration.py:79-84): when the voice config is brand new and the hotel already has a `BookingLinkConfiguration` with a `booking_url_prefix`, set `booking_link_enabled=True`. The originating ticket VOX-4064 (https://linear.app/canary-technologies/issue/VOX-4064) was an EU self-serve hotel (Lifestyle Suites Rome) raised by Lia; the fix was applied generically to every caller of `enable()`, and there are exactly two: the self-serve `voice_setup_activate` view and the onboarding `ConfigureVoicePlan`.

  2. Every Wyndham Connect Plus hotel already has that booking link config. `WyndhamConnectPlusChatConfigProvider` (onboarding/configuration_providers/wyndham/wyndham_connect_plus_chat_config_provider.py) hardcodes `BOOKING_URL_PREFIX = "https://www.wyndhamhotels.com/hotels/{wyndham_site_id}?cid=VN:ihlp98d6ismlqw9&"` and `ChatSettingsPlan` writes it to `BookingLinkConfiguration.booking_url_prefix` (onboarding/plans/chat_settings_plan.py:52-56). That came from PR #28948 "Incorporate booking URL into Wyndham Connect Plus scripts" (https://github.com/canary-technologies-corp/canary/pull/28948, Ramiro, 2025-07-28) and exists for the messaging AI, which does send booking links for Wyndham (chat `booking_link_enabled` is on for 1,668 of 1,818 Wyndham voice hotels). Not from `backfill_wyndham_booking_params` as the thread guessed: that command only rewrites params/date format for AMB hotels that already have a voice config, though note it also sets voice `booking_link_enabled=True` (chat/management/commands/backfill_wyndham_booking_params.py:79), so it must not be re-run for Wyndham voice hotels either.

  Runtime effect: `voice/livekit/orchestration_agent.py:286` routes to `BookingLinkAgent` when `booking_link_enabled and not has_booking_agent`, which is exactly the "asked for dates, texted a link, never quoted rates" behaviour kli hit on Baymont Arlington.

  ### Are the Wyndham onboarding scripts doing the right thing?
  The Wyndham scripts themselves are correct in intent but are now undermined by the service:
  - `WyndhamVoiceAIConfigProvider` + `ConfigureVoicePlan` never touch `booking_link_enabled` or `has_booking_agent`. `VoiceAIConfig` has no booking field at all, so the script has no way to say "no booking links".
  - Both Wyndham processes hit the bug. `WYNDHAM_AI_VOICE` (the WAIC add-on batch, onboarding/models/property_configuration_processes.py:779) runs `ConfigureVoicePlan` on hotels that already have the WCP booking link config. `WYNDHAM_CONNECT_PLUS` (new hotels) runs `ChatSettingsPlan` before `ConfigureVoicePlan` inside the same BASE_CONFIGURATION_NEW stage, so the prefix exists by the time voice is created. The late-October WAIC batch will reproduce this unless the code is changed.
  - Second exposure path, unrelated to scripts: the dashboard booking-link PATCH (`_enable_voice_booking_link`, chat/views/dashboard/configuration/booking_link_configuration.py:86) flips voice `booking_link_enabled` on whenever anyone saves booking link params/date format for a hotel with a voice config. Any Wyndham hotel whose booking link settings are edited in the dashboard will get voice booking links too.

  ### Prod state (Snowflake CANARY_RAW, deduped CDC rows, extracted 2026-09-29 18:31 UTC)
  | Wyndham voice configs created | n | voice booking_link_enabled | has_booking_agent |
  | 2026-09-01 batch | 38 | 0 | 0 |
  | 2026-09-10 batch | 27 | 0 | 0 |
  | 2026-09-24 batch | 29 | 0 (was 29) | 0 |
  All 29 from 9/24 were updated at 18:01 UTC on 9/29, i.e. Marta already turned the flag off (she said she would at 20:49 EEST). Across all 1,818 Wyndham voice hotels, voice booking links are now on for 0, so no stragglers via the dashboard path yet. 101 Wyndham hotels have `has_booking_agent` on (call-center/booking pilots, expected).

  ### Recommended fix (matches Stephen's suggestion in the thread)
  Make the auto-enable an explicit `enable()` argument rather than a hidden default: add `booking_link_enabled: bool | None = None` to `VoiceConfigurationService.enable()`; when None keep today's behaviour only for the self-serve activate view (or have that view pass True explicitly, which preserves the VOX-4064 fix), and have `ConfigureVoicePlan` pass `config.booking_link_enabled` from a new `VoiceAIConfig` field defaulting to False. Wyndham's provider then leaves it False. A Wyndham portfolio check inside the service (kli's option) works too but hides brand policy in a generic service and would not protect other brands with pre-seeded booking URLs. Separately consider whether `_enable_voice_booking_link` in the dashboard PATCH should also respect brand policy, since it is the remaining way Wyndham hotels can get voice booking links turned on.

  No code was changed and nothing was posted anywhere. Suggested next step: a VOX/ENT ticket for the `enable()` signature change before the late-Oct WAIC batch, owner Voice team (Arjun) with Marta as stakeholder.

  ### Side observation (not this task)
  Wyndham chat configs created since 2026-08 have chat `booking_link_enabled=False` (0 of 54 in Aug, 0 of 12 in Sep) while older ones are mostly True. `ChatSettingsPlan` sets the URL prefix but never sets the chat flag, and the one-time backfill that flipped it only ran as of 2026-06-03. If messaging booking links are meant to be on for WCP, the messaging script may have the mirror-image gap.
project: null
source_id: null
tags: []
time_minutes: 5
title: Dig into root cause and check onboarding scripts for Wyndham are doing the
  right thing
updated: 2026-09-30 13:38:49.535377
waiting_on: null
waiting_since: null
working_on: false
---

https://canarytechnologies.slack.com/archives/C0AJ1ENFSSU/p1790703003314659