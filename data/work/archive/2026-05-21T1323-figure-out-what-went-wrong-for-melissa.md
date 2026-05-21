---
area: null
contexts: []
created: 2026-05-21 13:23:57.115666
defer_until: null
due: 2026-05-21
energy: low
id: 2026-05-21T1323-figure-out-what-went-wrong-for-melissa
order: null
output: "## Agent run 2026-05-21T11:05Z (root cause)\n\nMelissa entered the wrong\
  \ value for `environment_name` in the HOTEL_KEY_CREDENTIALS onboarding value for\
  \ Best Western Spartanburg I-26 / Winners Circle (hotel 127838, SFDC 001f200001m5gQUAAY,\
  \ BW property code 04080).\n\n- She uploaded: `'HotelKey Environment: production\
  \ (Best Western Prod)'` — that's the Django __str__() of the HotelKeyEnvironment\
  \ object (the label admin dropdowns render).\n- The gateway expects the underlying\
  \ `name` field value, which is `'Best Western Prod'` (HotelKeyEnvironment id=67\
  \ in prod gateway DB).\n\nGateway upsert does HotelKeyEnvironment.objects.get(name=env_name),\
  \ hit DoesNotExist, tried to raise HotelKeyEnvironmentNotFound.\n\n**Secondary bug\
  \ — why the user saw an opaque 500 instead of a clean 4xx.** `HotelKeyEnvironmentNotFound`\
  \ and `HotelKeyEnvironmentAmbiguous` in pms-gateway/vendors/integrations/hotelkey/services/configuration.py\
  \ extend CanaryException but do NOT declare the required `code` / `status` class\
  \ attributes. The gateway middleware at pms-gateway/common/utils/errors.py:117 does\
  \ HTTPStatus(exception.status) — that raises AttributeError on these subclasses,\
  \ so they fall through to the generic 500 handler with no useful response body.\
  \ This defeats the intent of commit bd2da194c68 (\"Surface a clear 4xx instead of\
  \ letting MultipleObjectsReturned bubble as a 500\"). Fix: add code=\"hotel_key_environment_not_found\"\
  \ / code=\"hotel_key_environment_ambiguous\" and status=HTTPStatus.BAD_REQUEST (or\
  \ NOT_FOUND / CONFLICT) on both exception classes.\n\n**What unblocked Melissa.**\
  \ She configured the gateway manually. Account 59952 now has type=hotelkey and a\
  \ HotelKey config row; integration is live (her 2026-05-20 23:23 message in-thread).\n\
  \n**Suggested follow-up.**\n1. Tell Melissa: the value to enter for BW prod environment_name\
  \ is `'Best Western Prod'` (NOT the dropdown label). Same trap will bite Connor\
  \ / future onboarders — worth turning that field into a dropdown of known env names\
  \ in the value-upload UI, or accepting both the name and display label server-side.\n\
  2. Land the CanaryException code/status fix above so the next person to mistype\
  \ this gets a clean 400 instead of an opaque 500.\n3. Re-run the original script\
  \ batch for the remaining 3 BW Hotelkey hotels Sharon flagged on 5/15 once #1 is\
  \ communicated.\n\n---\n\n## Agent run 2026-05-21T10:50Z (initial)\n\n**Context.**\
  \ Melissa's BW Hotelkey rollout.
  She uploaded onboarding\nvalues successfully for Best Western Winners Circle (hotel
  127838,\nSFDC 001f200001m5gQUAAY) but the `create_pms_configuration` script\nbatch
  failed for the one hotel. She manually migrated it as a workaround\nand confirmed
  integration is working in prod\n(`gateway/account/59952/change/`).\n\n**Batch.**
  `da173a37-5f18-4eee-bfbf-bb0298f29a06`, single hotel.\nRun `8021e88e-b7da-4a68-b367-9eb88aabf10a`,
  state=failed,\nran at 2026-05-20 20:22:21–23 UTC on v2026.17.400.\n\n**Error captured
  (canary side):**\n```\nOnboardingServiceError: 500 Server Error: Internal Server
  Error\nfor url: https://gateway.canarytechnologies.com/api/accounts/hotelkey\nfailed_plan:
  ConfigurePMSIntegrationCreateConfigurationPlan\nconfig_provider: BestWesternPmsConfigProvider\n```\n\n**Gateway
  side (Datadog).** Single 500 from PUT `/api/accounts/hotelkey`\non pid 9356, host
  i-00c866d94718abca6, integration-gateway v2026.17.395,\n299ms, 145-byte body. No
  application-level error log indexed in Datadog,\nand Sentry has no matching issue
  for either project. The uWSGI worker\nwas recycled right after the request (`work
  of process 9356 is done`),\nbut that looks like a normal lazy-apps respawn, not
  the cause — the\nrequest had already returned.\n\n**What I ruled out (by code reading):**\n-
  Canary-side credential schema validation (would raise\n  ERROR_MISSING_HOTEL_KEY_CREDENTIALS
  as a 4xx, not a 500).\n- `HotelKeyEnvironment.DoesNotExist` / `MultipleObjectsReturned`
  —\n  `vendors/integrations/hotelkey/services/configuration.py` already\n  converts
  both to 4xx (commit bd2da194c68 on 2026-05-13, deployed\n  before 5/20).\n- Unique-constraint
  duplicate — canary plan catches that string and\n  raises ERROR_PMS_CONFIGURATION_ALREADY_EXISTS
  (4xx-shaped).\n\n**Most plausible remaining causes (untested):**\n1. Bad/typo `environment_name`
  that matches multiple rows AND the\n   `HotelKeyEnvironmentAmbiguous` path somehow
  re-raised as 500\n   (worth verifying which version was actually live on the gateway
  —\n   integration-gateway was on v2026.17.395 while canary was on\n   v2026.17.400;
  possible the gateway lagged the fix).\n2. DB integrity error other than the one
  canary catches (e.g.\n   property_code uniqueness when an existing HotelKey row
  exists for\n   a different account).\n3. Schema validation error that bubbled as
  500 instead of 400 because\n   of how `UpsertConfigurationRequestSchema.pre_load`
  reshapes payload.\n\n**What I left for you:**\n- Two debug scripts prepared (canary
  + pms-gateway) to dump the\n  HOTEL_KEY_CREDENTIALS onboarding value and inspect\n
  \ `HotelKeyEnvironment` rows for the `environment_name` Melissa\n  uploaded. Pasted
  into chat — not run because remote shells need\n  to be opened by you.\n- No Sentry
  issue exists for this 500. If you want to actually find\n  the traceback, the fastest
  path is probably re-running the script\n  in a non-prod env with the same OnboardingValue
  and capturing\n  the gateway-side exception, or temporarily lowering the Sentry\n
  \ sample rate / catching this path in the gateway view.\n\n**Note on the broader
  thread.** Melissa unblocked herself by doing\nthe migration manually and confirmed
  the integration is live. The\nfollow-up work is: (a) make sure the scripted path
  works for the\nremaining 3 BW Hotelkey hotels Sharon flagged on 5/15; (b) standardize\nthe
  value-upload step for IHG too (mentioned in-thread, cc taykirch).\n"
project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 5
title: Figure out what went wrong for melissa
updated: 2026-05-21 13:50:12.574747
waiting_on: null
waiting_since: null
working_on: false
---

use debug_in_shell if nec
https://canarytechnologies.slack.com/archives/C07BX379GQK/p1779308630008149?thread_ts=1778842566.238089&cid=C07BX379GQK