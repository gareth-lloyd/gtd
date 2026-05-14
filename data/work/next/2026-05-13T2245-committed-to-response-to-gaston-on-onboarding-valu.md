---
area: null
contexts: []
created: 2026-05-13 22:45:10.661871
defer_until: null
due: 2026-05-14
energy: low
id: 2026-05-13T2245-committed-to-response-to-gaston-on-onboarding-valu
order: -20
output: |
  ## Agent run 2026-05-14T13:00 UTC

  ### Context recap
  Gaston's ask (Slack thread C047K6WSUJY/p1778695412387899): voice
  setup is moving into the Integrations tab (PRD: "Voice Setup —
  Integrations Tab"). Writes there trigger the voice onboarding flow
  (purchase Twilio number, register forwarding number, etc.). The
  general pattern is that Integrations writes are blocked under
  impersonation. He's asking if it's OK to whitelist voice product
  configuration writes for impersonators so CS can actually use the
  new UI. Stephanie noted this will become more common as we shift
  settings out of Django admin.

  ### Findings
  1. The whitelisting mechanism already exists and is well-used:
     `backend/shared/shared/utilities/impersonation.py`
     :: `IMPERSONATOR_URL_CONFIG` — a per-url-name allowlist with
     explicit HTTP methods. There are ~50 entries, covering Tipping,
     Guest Journey, Addons, Rooms, Authorization exports, Payment
     Gateway, Hotel Devices, Kiosk, Chat, WhatsApp RTC templates,
     Segmentation, Knowledge Base, etc.
  2. **Direct precedent in the same Integrations tab**:
     `pms_gateway_configurations` (PUT) and
     `pms_gateway_configurations_validate` (POST) are already
     whitelisted. PMS integration setup — also CS-driven, also lives
     in Integrations — uses exactly the carve-out Gaston is asking
     for.
  3. The PRD's whole motivation is *safety*: Meritage launched
     without a forwarding number, Dupont Circle had the wrong number,
     CS today runs two Django scripts with no guardrails. Moving to a
     validated UI with E.164 enforcement and completeness gating is
     strictly safer than the status quo. Blocking impersonation here
     forces CS to keep running the unsafe scripts and defeats the
     point.
  4. Relevant url_name today: `voice_configuration` in
     `backend/canary/voice/urls.py:37`. The new endpoint(s) that
     trigger onboarding should be added as `_UrlConfig` entries with
     the *minimum* methods needed (likely POST to create+trigger,
     PATCH to update the forwarding number). Avoid blanket "all
     methods" — keep the scope tight.
  5. Audit: impersonator is captured via
     `request_context_middleware.get_current_impersonator`. We should
     confirm the voice configuration write path logs the impersonator
     on any mutation (model `*_log` table with `impersonator` FK is
     the established pattern, e.g. `creditcardlog`). Worth verifying
     in the PR.

  ### Stephanie's point
  She's right — this is now a recurring pattern (Integrations tab
  shift, settings out of Django). The per-url-name allowlist works
  but won't scale gracefully if every new internal-facing settings
  view needs a new entry + reviewer roundtrip. Worth a follow-up
  conversation (not blocking this work) about whether we want a
  decorator at the view layer (e.g. `@allow_impersonator_writes`)
  rather than a central list, or a role/permission-based gate that
  doesn't conflate "impersonator" with "read-only". Not Gaston's
  problem to solve today.

  ### Draft Slack response (NOT YET SENT — needs Gareth's approval)

  > Thanks for the patient write-up. Short answer: yes, it's fine to
  > whitelist voice product configuration writes for impersonators.
  >
  > Three reasons:
  >
  > 1. The mechanism is exactly what the impersonator allowlist
  >    (`IMPERSONATOR_URL_CONFIG` in
  >    `shared/shared/utilities/impersonation.py`) is for, and we
  >    already have a direct precedent in the same Integrations tab —
  >    PMS gateway configuration (`pms_gateway_configurations` PUT +
  >    `pms_gateway_configurations_validate` POST) is whitelisted for
  >    the same CS-driven workflow.
  > 2. The PRD's whole point is to *reduce* risk vs. the two-Django-
  >    script status quo (the Meritage / Dupont Circle incidents).
  >    Forcing CS to keep using those scripts because of the
  >    impersonation default would be a net safety loss.
  > 3. Voice config is internal-facing during onboarding — there is
  >    no scenario today where a hotel admin runs this without CS
  >    involvement.
  >
  > Two asks when you put up the PR:
  >
  > - Add the specific voice-onboarding url_name(s) to
  >   `IMPERSONATOR_URL_CONFIG` with the minimum methods needed
  >   (e.g. just POST + PATCH on the trigger endpoint), not a
  >   blanket unlock.
  > - Make sure the write path captures the impersonator for audit —
  >   same pattern as the credit card log
  >   (`creditcardlog.impersonator` FK). The trigger action mutates
  >   the hotel's Twilio state and we'll want a paper trail.
  >
  > To Stephanie's broader point: yep, agreed this will keep coming
  > up. Let's pick it up separately — I think we can do better than
  > a central list as the surface area grows, but it's not blocking
  > this work.

  ### Next step
  Awaiting Gareth's approval to post (or edit) the draft above into
  the Slack thread.
project: 2026-04-16T1351-ship
source_id: null
tags: []
time_minutes: 15
title: committed to response to gaston on onboarding values for voice
updated: 2026-05-14 13:00:00.000000
waiting_on: null
waiting_since: null
working_on: false
---

https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1778695412387899