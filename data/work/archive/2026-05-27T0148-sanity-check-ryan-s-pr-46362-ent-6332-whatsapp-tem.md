---
area: null
contexts:
- react
created: 2026-05-27 01:48:42.182226
defer_until: null
due: null
energy: medium
id: 2026-05-27T0148-sanity-check-ryan-s-pr-46362-ent-6332-whatsapp-tem
order: null
output: |
  ## Agent run 2026-05-27T07:08Z

  **Verdict: Ship it. Both layers of the fix correctly address ENT-6332. One small symmetry suggestion below, non-blocking.**

  ### Plan layer (configure_guest_journey_messages.py)
  Correct. Verified by tracing both paths:
  - `update_or_create_guest_journey_message` (L847-849): clears flag + body when `allow_whatsapp_templates=False`.
  - `update_or_create_custom_guest_journey_message` (L1013-1016): same.
  - Downstream proof: `GuestJourneyMessageService.create`/`.update` (guest_journey_message.py L314, L530) only build `whatsapp_template_data` when `message_template_detail.whatsapp_body_i18n` is truthy. So the previous one-line fix (flag only) was indeed insufficient — Ryan's diagnosis matches the code.

  ### Service layer (message_schedule_spec.py)
  Correct defense-in-depth. The DB row is still written via `WhatsappMessageTemplateService.create_or_update` at L339-347 (matches PR description: "DB template row still written; only Twilio submit suppressed"). The new gate at the renamed conditional only affects the Twilio submission path. This protects against any future caller that re-introduces the same shape (admin UI, ad-hoc script, different brand provider). The warning log includes `hotel_id` + `message_schedule_spec_id` + `message_type` — adequate for forensics.

  Caller audit: `_create_or_update_whatsapp_template` is private and only called from `MessageScheduleSpecService.create_or_update` (L167), which threads `is_whatsapp_template_enabled` correctly into `spec.is_whatsapp_enabled` via `set_if_not_none` at L138. No other call sites bypass the gate.

  ### One symmetry observation (non-blocking)
  The **variant builder** at L457-458 of configure_guest_journey_messages.py still sets only the flag (`is_whatsapp_message_enabled=False`) without clearing `whatsapp_body_i18n`. PR description correctly states this is safe because `GuestJourneyMessageVariantsService._create_whatsapp_template_if_enabled` (L213 of guest_journey_message_variants_service.py) gates on **both** flag AND body. So functionally fine today. But:
  - The non-variant path now has a different shape than the variant path (non-variant clears both; variant clears flag only).
  - If anyone refactors the variant downstream to gate on body-only (mirroring the non-variant pattern Ryan just fixed), the bug returns silently in the variant path.
  - Suggestion: mirror the `whatsapp_body_i18n = None` line at L458 for symmetry + future-proofing. Tiny diff, no behavior change today, removes the asymmetry that made the original bug possible.

  Worth a comment on the PR or a follow-up; not a blocker.

  ### Test coverage
  - Plan-layer test (`test_execute__no_whatsapp_template_when_allow_whatsapp_templates_false`): asserts no `WhatsappMessageTemplate` rows + no `spec.whatsapp_message_template` + `is_whatsapp_enabled is False` across all created messages. Hits both standard + custom paths. Good shape.
  - Service-layer test (`test_create_template__skips_twilio_submit_when_spec_whatsapp_disabled`): correctly sets `allow_send_whatsapp=True` + `is_whatsapp_template_enabled=False`, asserts no Twilio calls but DB row written. Confirms the gate's exact contract.
  - PR description claims both tests fail without the corresponding fix — that's the right discipline (tests prove they exercise the real bug path). Trust but didn't independently re-run.

  ### Other notes
  - Scope is right: fix is forward-only; cleanup of orphan rows is correctly punted to ENT-6333.
  - No risk to existing Wyndham hotels where `allow_whatsapp_templates=True` — gate only activates when `is_whatsapp_enabled=False` at the spec level (or when the plan was told to disable).
  - Compatible with callers that legitimately pre-stage a body before flipping the flag on (the DB row write is preserved).

  ### What I'd reply to Ryan
  > Sanity check passed. Plan-layer fix is correctly targeted — verified the downstream gate at guest_journey_message.py:314/530 only checks the body, so the flag-only fix was definitely insufficient. Service-layer gate is good defense-in-depth.
  >
  > One small thing: the variant builder path in configure_guest_journey_messages.py:457-458 also sets only the flag (no body clear). Safe today because `_create_whatsapp_template_if_enabled` gates on both, but worth mirroring the body-clear for symmetry — otherwise the same bug-shape can re-emerge if someone refactors the variant downstream. Not a blocker.
project: null
source_id: https://canarytechnologies.slack.com/archives/D07MJEGGV19/p1779835233661579
tags:
- morning-gtd
- slack
- from-awareness
time_minutes: 25
title: 'Sanity-check Ryan''s PR #46362 (ENT-6332 WhatsApp template guardrails)'
updated: 2026-05-27 14:03:10.919995
waiting_on: null
waiting_since: null
working_on: false
---

Ryan DM: WA Twilio updates triggered for hotels that shouldn't have WA enabled when GJ onboarding plan ran with updated templates; PR adds multiple guardrails — he wants a sanity check from knowledgeable eyes. https://canarytechnologies.slack.com/archives/D07MJEGGV19/p1779835233661579 — PR https://github.com/canary-technologies-corp/canary/pull/46362