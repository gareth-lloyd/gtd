---
area: null
completed_at: 2026-10-06 13:39:32.105882
contexts:
- react
created: 2026-10-02 11:12:14.120341
defer_until: null
due: null
energy: low
id: 2026-10-02T1112-follow-up-on-wyndham-voice-ai-onboarding-script-mu
order: null
output: |-
  ## Agent run 2026-10-06T12:52 (EEST)

  **Nothing has moved since 9/30. As master stands, the late-October Wyndham batch will get voice booking links switched on again.**

  ### Where things stand

  - **Thread:** no replies after Arjun's 9/30 message; his decoupling question is unanswered. https://canarytechnologies.slack.com/archives/C0AJ1ENFSSU/p1790764694330389?thread_ts=1790703003.314659&cid=C0AJ1ENFSSU
  - **Ticket:** none. Searched Linear (ENT and all teams, created since 9/25) for booking link / voice / Wyndham onboarding. Only VOX-4064, the original change, exists (https://linear.app/canary-technologies/issue/VOX-4064/booking-link-enabled-for-voice-ai-properties-by-default).
  - **Code:** no PR, open or merged, touches the auto-enable. The block from #56163 (https://github.com/canary-technologies-corp/canary/pull/56163) is unchanged on master at `backend/canary/voice/services/configuration/voice_configuration.py:77-80`.
  - **Not checked:** whether Marta actually turned `booking_link_enabled` off on the 29 hotels from 9/24. The canary MCP servers and Teleport were down this session, and I kept the Snowflake MCP out of a session that has Slack send tools.

  ### Why it repeats

  - `ConfigureVoicePlan` calls `VoiceConfigurationService.enable()` with no way to opt out (`backend/canary/onboarding/plans/configure_voice_plan.py:89`).
  - On a brand-new voice config, `enable()` turns `booking_link_enabled` on whenever the hotel has a booking URL prefix.
  - Every Wyndham hotel has one. For full Connect Plus onboarding, `ChatSettingsPlan` writes it in the same stage, just before the voice plan runs (`onboarding/plans/chat_settings_plan.py:53-56`), so brand-new hotels are hit too, not only AMB hotels adding voice.

  ### One open PR changes the picture, but does not fix it

  - #59064, "[VOX-4025] Stop defaulting voice actions on for new hotels" (https://github.com/canary-technologies-corp/canary/pull/59064, open, chetna1726), flips the `make_reservation_enabled` default to off.
  - The call-time gate checks that flag first (`voice/livekit/orchestration_agent.py:281`), so a new Wyndham config would transfer booking calls to reservations and never reach the link flow.
  - If it merges before the batch, callers stop getting links. `booking_link_enabled` would still be set to true underneath, so links start the moment anyone turns "make a reservation" on for the hotel. It is also unmerged, so I would not rely on it.

  ### Suggested fix

  Small, one PR, no migration. It follows the existing `has_upsell_agent` opt-out, and is what Stephen proposed in the thread (let the onboarding script decide):

  1. `VoiceConfigurationService.enable()`: add a keyword argument, default true, that guards the `is_new_configuration` block.
  2. `VoiceAIConfig` (`onboarding/configuration_providers/configs/voice.py`): add the matching field, default true.
  3. `ConfigureVoicePlan.execute`: pass it through.
  4. `WyndhamVoiceAIConfigProvider`: set it to false. Both Wyndham processes that run the voice plan use this provider.
  5. Tests: mirror `test_execute__wyndham_hotel__does_not_enable_upsell_agent` in `onboarding/tests/plans/test_configure_voice_plan.py`, plus one case in `voice/tests/services/test_voice_configuration.py`.

  I did not write the code. Say the word and I will put it on a branch.

  ### Arjun's decoupling question

  - The flags are already separate: `chat.Configuration.booking_link_enabled` (messaging), `WebchatConfiguration.booking_link_enabled`, and voice `Configuration.booking_link_enabled`.
  - What still couples them is two bits of code that turn the voice flag on because the shared booking URL exists: the new-config block from #56163, and `_enable_voice_booking_link` on settings save from #47662 (https://github.com/canary-technologies-corp/canary/pull/47662, `chat/views/dashboard/configuration/booking_link_configuration.py:86-95`).
  - So saving booking link settings on a Wyndham hotel that has voice will also switch voice links on. The onboarding fix does not cover that; whether to remove both auto-enables is a Voice team call.
  - Separate trap: `backfill_wyndham_booking_params` sets voice `booking_link_enabled = True` on every hotel it updates (`chat/management/commands/backfill_wyndham_booking_params.py:82`). Do not rerun it for new batches as it stands.

  ### Drafts (nothing sent or created)

  **Linear ticket (ENT)**

  Title: Wyndham Voice AI onboarding must not auto-enable voice booking links

  > Since #56163 (merged 9/11), a new voice config gets `booking_link_enabled = true` whenever the hotel already has a booking URL. Every Wyndham hotel has one, because messaging uses it. All 29 hotels in the 9/24 batch got voice booking links; Wyndham should have neither booking links nor the booking agent on voice.
  >
  > The onboarding script has no way to opt out. Add an opt-out to `VoiceConfigurationService.enable()`, carry it on `VoiceAIConfig`, and set it off in `WyndhamVoiceAIConfigProvider` (same shape as `has_upsell_agent`).
  >
  > Needed before the next WAIC batch (late October).
  > Thread: https://canarytechnologies.slack.com/archives/C0AJ1ENFSSU/p1790703003314659

  **Slack reply in the thread**

  > Following up: nothing has changed in code yet, so the late-October batch would get voice booking links again. I'll ticket an onboarding opt-out for Wyndham (new voice configs skip the auto-enable).
  >
  > @Arjun on decoupling: the messaging, webchat and voice flags are already separate. The coupling is the two auto-enables that flip the voice flag when a booking URL exists (#56163 on new voice config, #47662 on settings save). The onboarding opt-out covers the first for Wyndham only; the settings-save one would still turn voice links on if someone edits booking link settings on a Wyndham hotel. Do you want to keep those auto-enables?
  >
  > @Marta did the 29 hotels from 9/24 get switched off?
project: null
source_id: https://canarytechnologies.slack.com/archives/C0AJ1ENFSSU/p1790764694330389?thread_ts=1790703003.314659&cid=C0AJ1ENFSSU
tags:
- morning-gtd
- slack
time_minutes: 10
title: 'Follow up on: Wyndham Voice AI onboarding script must not auto-enable booking
  links'
updated: 2026-10-06 13:39:32.105870
waiting_on: null
waiting_since: null
working_on: false
---

I parked this on 2026-09-30: 'When the subsequent batches of Wyndham hotels is onboarded to Voice AI we will get a repeat of this issue... We will need to make some onboarding script changes.' 29 of 29 hotels in the 9/24 batch got booking_link_enabled via #56163. Marta says the next WAIC batch is late October and will follow up with ENT; Arjun asks whether to decouple messaging vs voice booking links. No ticket seen yet.
https://canarytechnologies.slack.com/archives/C0AJ1ENFSSU/p1790764694330389?thread_ts=1790703003.314659&cid=C0AJ1ENFSSU