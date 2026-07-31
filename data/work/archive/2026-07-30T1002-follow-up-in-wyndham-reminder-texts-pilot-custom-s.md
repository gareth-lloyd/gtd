---
area: null
contexts:
- react
created: 2026-07-30 10:02:01.613417
defer_until: null
due: 2026-07-30
energy: medium
id: 2026-07-30T1002-follow-up-in-wyndham-reminder-texts-pilot-custom-s
order: null
output: |
  ## Agent run 2026-07-30T13:13

  Investigated the codebase + Linear history. Root cause is almost certainly the same one BW hit, and the BW fix pattern maps directly onto Wyndham. Draft Slack reply below — NOT posted, awaiting your approval.

  ### Findings

  1. **Why the 9am day-of texts aren't firing**: reminders attached to a check-in message get a scheduling window of `MAX(parent_message.scheduled_at + 24h, own send time)` (default `DEFAULT_REMINDER_START_WINDOW_OFFSET_HOURS = 24`, `backend/canary/guest_journey/services/guest_journey_message.py:1356-1374`). Wyndham's pre-arrival check-in sends 3pm day-before, so +24h pushes a day-of 9am reminder to 3pm day-of — guests are already arriving, and it may be suppressed entirely once they check in. This is exactly what BW hit in ENT-6464 (https://linear.app/canary-technologies/issue/ENT-6464) — "reminder fires at 3pm not 10am".
  2. **The BW "custom script"** Bryan remembers is not a one-off script: it's the BW onboarding config provider (`onboarding/configuration_providers/best_western/guest_journey_messages_provider.py`) defining `BW_CHECK_IN_WITH_REMINDER_SPEC` (day-of 10am reminder, `reminder_start_window_offset_hours=0` so its own send time wins), rolled out via the configure-guest-journey-messages plan (ENT-6433 https://linear.app/canary-technologies/issue/ENT-6433, ENT-6464 PR https://github.com/canary-technologies-corp/canary/pull/47450). The offset override is spec-only — it cannot be set from the GJ dashboard, which is why a dashboard-configured pilot can't work correctly.
  3. **Wyndham gap**: `wyndham_guest_journey_messages_provider.py` defines NO day-of reminder for US hotels (`CHECK_IN_24_HOURS_SPEC`, no reminder). Only SEAPR-region hotels get a reminder (and it's 24h-before, not day-of). So whatever was "set up in GJ" for the 25 pilot hotels was manual dashboard config subject to the 24h rule.
  4. **Recommended implementation (ENT-7030)**: pattern-match BW — add a pilot-gated reminder to the Wyndham check-in spec: `send_time=SendTime.NINE_AM` (exists in the enum), `delta=ZERO_DAYS`, `reminder_start_window_offset_hours=0`, gated to the 25 site IDs from ENT-7030 via a hotel-list module (BW precedent: `best_western/hotel_lists/experiment_checkin_reminder_hotels.py` from the ENT-5283 pilot), then re-run the config plan on those 25 hotels. Small effort — the generic offset mechanism already shipped with ENT-6464.
  5. **ENT-7030 status** (https://linear.app/canary-technologies/issue/ENT-7030): still in Triage, only has the 25-property list; Ani has not yet copied the GJ templates over (no comments as of 13:10).

  ### Not verified

  Live prod config of the pilot hotels (what exactly is configured in GJ for them). Snowflake query stalled on SSO auth; re-run `sf-login us` and I can confirm the exact state. Hypothesis is strong but unconfirmed against prod data.

  ## Agent run 2026-07-30T14:53

  User approved; reply POSTED to the thread: https://canarytechnologies.slack.com/archives/C04STT7UPRQ/p1785412424959739?thread_ts=1785354501.971389&cid=C04STT7UPRQ
  Promise fulfilled. Possible follow-ups: verify pilot hotels' live GJ config (needs `sf-login us`), and the ENT-7030 implementation itself once Ani adds templates.

  ### Slack reply as posted

  > Took a look as promised. This is the same issue we hit on the BW reminder launch (ENT-6433/ENT-6464): reminders attached to the pre-arrival check-in message have a default rule keeping them at least 24h after the parent message. Wyndham's pre-arrival sends 3pm day-before, so a 9am day-of reminder gets silently pushed to 3pm day-of — which is why they look like they're "not firing".
  >
  > For BW we fixed this with a per-spec override (`reminder_start_window_offset_hours=0`) that's only settable through the brand onboarding config, not the GJ dashboard — so Connor's right that we pattern-match that: add a pilot-gated day-of 9am reminder to the Wyndham guest-journey config for the 25 site IDs in ENT-7030 (same gating pattern as the BW reminder pilot), plus the templates Ani is copying over, then re-run the config plan on those hotels. Small change — the mechanism already exists from the BW work.
project: 2026-04-16T1351-ship
source_id: https://canarytechnologies.slack.com/archives/C04STT7UPRQ/p1785354501971389?thread_ts=1785354501.971389&cid=C04STT7UPRQ
tags:
- morning-gtd
- slack
time_minutes: 15
title: 'Follow up in #wyndham: reminder-texts pilot custom script (ENT-7030)'
updated: 2026-07-30 14:55:16.855536
waiting_on: null
waiting_since: null
working_on: false
---

I promised "I'll take a look tomorrow" (= today) in Bryan's thread: 25 Wyndham pilot properties, 9am day-of-arrival texts not firing; needs a custom script pattern-matched on BW (ENT-6433). Ani filed ENT-7030 and is copying the GJ template setup over today.
https://canarytechnologies.slack.com/archives/C04STT7UPRQ/p1785354501971389?thread_ts=1785354501.971389&cid=C04STT7UPRQ