---
area: null
contexts:
- react
created: 2026-06-08 11:35:20.627125
defer_until: null
due: null
energy: low
id: 2026-06-08T1135-follow-up-on-front-desk-forward-call-to-rule-for-w
order: null
output: |
  ## Agent run 2026-06-08T12:06

  ### TL;DR
  The open question in this thread is effectively already answered. **Connor Swords
  confirmed the rule in-thread on 2026-06-01** (reply 4): "Yes - I can confirm that the
  default/fallback `forward_call_to` for all Wyndhams should be the same as their
  `front_desk` number." The codebase already implements exactly this. The likely
  remaining action is a short acknowledgement to close the loop (and decide whether
  to encode it as an invariant / test), not a new investigation.

  ### Thread state (C047K6WSUJY, parent ts 1780081180.659859)
  - Gaston (2026-06-01): asked to confirm it's a rule that always holds that we want
    `front_desk` as `forward_call_to` for Wyndhams. Noted he left Wyndhams as-is to
    avoid disrupting workflows I'd flagged. cc'd Becca, Connor, Stephen.
  - Connor Swords (2026-06-01): confirmed — default/fallback `forward_call_to` for ALL
    Wyndhams = their `front_desk` number. (got a :ty: from Gaston)
  - My later replies (2026-06-02) were architecture feedback on the PRs (onboarding
    values refactor, VoiceAIConfig provider, hoisting voice logic out of
    ConfigureVoicePlan) — separate from the forward_call_to rule.

  ### Codebase confirms the rule is already enforced for Wyndhams
  `backend/canary/onboarding/configuration_providers/wyndham/wyndham_voice_ai_config_provider.py`:
  - Pulls the FRONT_DESK entry from the forwarding configuration
    (`forward_spec.category == ForwardNumber.Category.FRONT_DESK`).
  - Raises `ERROR_NO_FRONT_DESK_NUMBER_IN_ONBOARDING_VALUES` if there is no front desk
    number — i.e. front desk is mandatory for Wyndhams.
  - Sets `VoiceAIConfig(..., forward_call_to=front_desk_number)`.
  So by construction, for Wyndhams `forward_call_to` IS the front desk number; there is
  no path where a Wyndham gets a different general forwarding number.

  Contrast: `default_voice_config_provider.py` (non-Wyndham) sets `forward_call_to=None`
  and relies on the general/explicit forwarding configuration instead — consistent with
  Gaston's plan to make the general `forward_call_to` mandatory for non-Wyndhams.

  ### My read on "does the rule always hold?"
  Yes, with one nuance worth saying back to Gaston: it holds because the Wyndham
  provider *defines* forward_call_to as the front desk number and front desk is a
  required onboarding value. So it's not just a convention we hope holds — it's
  structurally guaranteed in the provider. The only way it could break is if someone
  changed the provider or made front desk optional for Wyndhams. If we want to lock it
  in, the cheap insurance is a unit test asserting
  `WyndhamVoiceAIConfigProvider.config.forward_call_to == front_desk_number`
  (there's already a test file: onboarding/tests/configuration_providers/wyndham/
  test_wyndham_voice_ai_config_provider.py — worth checking it covers this).

  ### Suggested next action (NOT yet sent — needs your approval to post to Slack)
  Connor already gave the confirmation, so a brief close-out is probably all that's
  needed. Draft reply:
    "Thanks Connor — that matches the code: the Wyndham voice config provider already
    pins `forward_call_to` to the required `front_desk` number and errors out if it's
    missing, so the rule is structurally enforced, not just convention. Happy to leave
    Wyndhams as-is. I'll make sure we have a test asserting forward_call_to == front_desk
    for Wyndhams so it stays that way."
  Want me to post this (or a trimmed version) to the thread? I won't send anything
  without an explicit go-ahead.
project: null
source_id: https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1780329800831359?thread_ts=1780081180.659859&cid=C047K6WSUJY
tags:
- morning-gtd
- slack
- from-awareness
time_minutes: 10
title: Follow up on front_desk = forward_call_to rule for Wyndhams
updated: 2026-06-08 12:06:37
waiting_on: null
waiting_since: null
working_on: false
---

Gaston: confirm it's a rule that always holds that we want front_desk as forward_call_to for Wyndhams (he left them as-is per your point). #epd-enterprise.
https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1780329800831359?thread_ts=1780081180.659859&cid=C047K6WSUJY