---
area: null
contexts: []
created: 2026-05-13 22:45:10.661871
defer_until: null
due: 2026-05-14
energy: low
id: 2026-05-13T2245-committed-to-response-to-gaston-on-onboarding-valu
order: -20
output: "## Agent run 2026-05-14T13:00 UTC\n\n### Context recap\nGaston's ask (Slack
  thread C047K6WSUJY/p1778695412387899): voice\nsetup is moving into the Integrations
  tab (PRD: \"Voice Setup —\nIntegrations Tab\"). Writes there trigger the voice onboarding
  flow\n(purchase Twilio number, register forwarding number, etc.). The\ngeneral pattern
  is that Integrations writes are blocked under\nimpersonation. He's asking if it's
  OK to whitelist voice product\nconfiguration writes for impersonators so CS can
  actually use the\nnew UI. Stephanie noted this will become more common as we shift\nsettings
  out of Django admin.\n\n### Findings\n1. The whitelisting mechanism already exists
  and is well-used:\n   `backend/shared/shared/utilities/impersonation.py`\n   ::
  `IMPERSONATOR_URL_CONFIG` — a per-url-name allowlist with\n   explicit HTTP methods.
  There are ~50 entries, covering Tipping,\n   Guest Journey, Addons, Rooms, Authorization
  exports, Payment\n   Gateway, Hotel Devices, Kiosk, Chat, WhatsApp RTC templates,\n
  \  Segmentation, Knowledge Base, etc.\n2. **Direct precedent in the same Integrations
  tab**:\n   `pms_gateway_configurations` (PUT) and\n   `pms_gateway_configurations_validate`
  (POST) are already\n   whitelisted. PMS integration setup — also CS-driven, also
  lives\n   in Integrations — uses exactly the carve-out Gaston is asking\n   for.\n3.
  The PRD's whole motivation is *safety*: Meritage launched\n   without a forwarding
  number, Dupont Circle had the wrong number,\n   CS today runs two Django scripts
  with no guardrails. Moving to a\n   validated UI with E.164 enforcement and completeness
  gating is\n   strictly safer than the status quo. Blocking impersonation here\n
  \  forces CS to keep running the unsafe scripts and defeats the\n   point.\n4. Relevant
  url_name today: `voice_configuration` in\n   `backend/canary/voice/urls.py:37`.
  The new endpoint(s) that\n   trigger onboarding should be added as `_UrlConfig`
  entries with\n   the *minimum* methods needed (likely POST to create+trigger,\n
  \  PATCH to update the forwarding number). Avoid blanket \"all\n   methods\" — keep
  the scope tight.\n5. Audit: impersonator is captured via\n   `request_context_middleware.get_current_impersonator`.
  We should\n   confirm the voice configuration write path logs the impersonator\n
  \  on any mutation (model `*_log` table with `impersonator` FK is\n   the established
  pattern, e.g. `creditcardlog`). Worth verifying\n   in the PR.\n\n### Stephanie's
  point\nShe's right — this is now a recurring pattern (Integrations tab\nshift, settings
  out of Django). The per-url-name allowlist works\nbut won't scale gracefully if
  every new internal-facing settings\nview needs a new entry + reviewer roundtrip.
  Worth a follow-up\nconversation (not blocking this work) about whether we want a\ndecorator
  at the view layer (e.g. `@allow_impersonator_writes`)\nrather than a central list,
  or a role/permission-based gate that\ndoesn't conflate \"impersonator\" with \"read-only\".
  Not Gaston's\nproblem to solve today.\n\n### Draft Slack response (NOT YET SENT
  — needs Gareth's approval)\n\n> Thanks for the patient write-up. Short answer: yes,
  it's fine to\n> whitelist voice product configuration writes for impersonators.\n>\n>
  Three reasons:\n>\n> 1. The mechanism is exactly what the impersonator allowlist\n>
  \   (`IMPERSONATOR_URL_CONFIG` in\n>    `shared/shared/utilities/impersonation.py`)
  is for, and we\n>    already have a direct precedent in the same Integrations tab
  —\n>    PMS gateway configuration (`pms_gateway_configurations` PUT +\n>    `pms_gateway_configurations_validate`
  POST) is whitelisted for\n>    the same CS-driven workflow.\n> 2. The PRD's whole
  point is to *reduce* risk vs. the two-Django-\n>    script status quo (the Meritage
  / Dupont Circle incidents).\n>    Forcing CS to keep using those scripts because
  of the\n>    impersonation default would be a net safety loss.\n> 3. Voice config
  is internal-facing during onboarding — there is\n>    no scenario today where a
  hotel admin runs this without CS\n>    involvement.\n>\n> Two asks when you put
  up the PR:\n>\n> - Add the specific voice-onboarding url_name(s) to\n>   `IMPERSONATOR_URL_CONFIG`
  with the minimum methods needed\n>   (e.g. just POST + PATCH on the trigger endpoint),
  not a\n>   blanket unlock.\n> - Make sure the write path captures the impersonator
  for audit —\n>   same pattern as the credit card log\n>   (`creditcardlog.impersonator`
  FK). The trigger action mutates\n>   the hotel's Twilio state and we'll want a paper
  trail.\n>\n> To Stephanie's broader point: yep, agreed this will keep coming\n>
  up. Let's pick it up separately — I think we can do better than\n> a central list
  as the surface area grows, but it's not blocking\n> this work.\n\n### Next step\nAwaiting
  Gareth's approval to post (or edit) the draft above into\nthe Slack thread.\n"
project: 2026-04-16T1351-ship
source_id: null
tags: []
time_minutes: 15
title: committed to response to gaston on onboarding values for voice
updated: 2026-05-14 13:56:11.479308
waiting_on: null
waiting_since: null
working_on: false
---

https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1778695412387899