---
area: null
contexts:
- react
created: 2026-07-31 10:56:46.445136
defer_until: null
due: null
energy: medium
id: 2026-07-31T1056-reply-to-ramiro-in-epd-voice-voice-whatsapp-templa
order: null
output: |
  ## Agent run 2026-07-31T11:40:00+03:00

  Researched the code and drafted a reply to Ramiro's follow-ups (thread:
  https://canarytechnologies.slack.com/archives/C07R45PP9AS/p1785413767469249?thread_ts=1785346239.525699&cid=C07R45PP9AS).
  NOT posted — awaiting approval. Draft is below; say "send it" and I'll post it to the thread.

  ### Findings (code-verified)

  - The side effect = `VoiceMessageTemplateService.create_template_and_submit_for_approval`
    (backend/canary/voice/services/voice_message_template.py): creates the two voice WhatsApp
    content templates (VOICE_BOOKING_LINK, VOICE_FOLLOW_UP), submits them to Twilio/Meta for
    approval, and flips voice `Configuration.follow_up_message_channel` to WHATSAPP. Idempotent
    (existing templates skipped). Callback guard: `new_val and hotel.allow_send_whatsapp`.
  - It ALREADY runs on product addition: `activate_hotel_products` →
    `update_new_product_states` → `change_product_state(VOICE)` → the callback
    (backend/canary/onboarding/services/onboarding.py:933,1044).
  - On fresh creation it is effectively a no-op: `allow_send_whatsapp` defaults False and
    requires a WhatsApp number (set later, at the Twilio-config stage), so the guard drops it;
    the follow-up-channel flip targets a `voice.Configuration` row that doesn't exist yet.
    My earlier "wart" claim was overstated — semantically wrong but practically harmless.
  - Safety net: `ConfigureVoicePlan.post_success_hook`
    (backend/canary/onboarding/plans/configure_voice_plan.py:122) already dispatches the same
    idempotent task (`async_create_content_templates_for_voice`) when WhatsApp is enabled,
    so dropping VOICE from the creation-time fan-out loses nothing.

  ### Recommendation for Ramiro

  1. Keep the side effect on product addition — templates need Meta approval lead time, so
     submitting when the product is sold (before configure-voice runs) is useful; guard makes
     it safe. Even if his unification stops flipping `has_voice` on activation, keep firing
     `change_product_state(VOICE)` there (or dispatch the template task directly) so the early
     submission isn't lost.
  2. Skip it on creation — drop VOICE from HotelProductsPlan's `change_product_state` fan-out;
     configure-voice's post_success_hook covers the go-live moment.

  ### Draft Slack reply (to post in thread 1785346239.525699, channel C07R45PP9AS)

  Dug into the template side effect to answer properly — and a small correction to my last
  message first.

  What it actually does: creates the two voice WhatsApp content templates (booking-link +
  follow-up), submits them to Twilio/Meta for approval, and flips the voice config's follow-up
  channel to WhatsApp. WhatsApp only lets us send pre-approved templates and approval takes
  days, which is why we submit ahead of need. It's idempotent (existing templates are
  skipped) and guarded by `hotel.allow_send_whatsapp`.

  Should it run on product addition? It already does — `activate_hotel_products` →
  `update_new_product_states` → `change_product_state(VOICE)` → same callback. I'd keep it:
  for a live hotel with WhatsApp configured, submitting at product-sale time buys the Meta
  approval lead time before configure-voice actually turns voice on. If WhatsApp isn't
  enabled it no-ops. (Even if you stop flipping `has_voice` on activation per the earlier
  conclusion, I'd still fire this callback — or dispatch the template task directly — so we
  don't lose the early submission.)

  Should creation skip it? Yes — and correction: it effectively skips itself today, so my
  "wart" was overstated. At base configuration `allow_send_whatsapp` is still False (default
  False, requires a WhatsApp number that only gets set at the Twilio-config stage), so the
  guard drops it, and the follow-up-channel flip targets a `voice.Configuration` row that
  doesn't exist yet. Semantically wrong, practically a no-op.

  What makes skipping it free: `ConfigureVoicePlan.post_success_hook` already dispatches the
  same idempotent task (`async_create_content_templates_for_voice`) when WhatsApp is enabled.
  So for the unified code: keep the product-change callback (covers product addition + manual
  admin flips), drop VOICE from the creation-time `change_product_state` fan-out, and let
  configure-voice cover go-live.
project: null
source_id: https://canarytechnologies.slack.com/archives/C07R45PP9AS/p1785413767469249?thread_ts=1785346239.525699&cid=C07R45PP9AS
tags:
- morning-gtd
- slack
time_minutes: 15
title: 'Reply to Ramiro in #epd-voice: voice WhatsApp template side effects'
updated: 2026-07-31 12:53:18.936245
waiting_on: null
waiting_since: null
working_on: false
---

He accepted my analysis and asked follow-ups: should the WhatsApp-template side effect run on product addition? Skip on creation? https://canarytechnologies.slack.com/archives/C07R45PP9AS/p1785413767469249?thread_ts=1785346239.525699&cid=C07R45PP9AS