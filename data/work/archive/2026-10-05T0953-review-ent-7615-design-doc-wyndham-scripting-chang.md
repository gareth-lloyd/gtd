---
area: null
completed_at: 2026-10-05 11:18:34.395449
contexts:
- react
created: 2026-10-05 09:53:06.745604
defer_until: null
due: null
energy: medium
id: 2026-10-05T0953-review-ent-7615-design-doc-wyndham-scripting-chang
order: null
output: |
  ## Agent run 2026-10-05T11:14:16

  Verdict: approve the direction. Every code claim in the doc checks out against master. Four things to add before Ryan starts, one of which is a product question for Connor/Khush, not a code nit.

  Doc: https://app.notion.com/p/canarytechnologies/ENT-7615-Wyndham-scripting-change-to-support-OHIP-migration-3ed814686151812db733f7f9f2490d27
  Issue: https://linear.app/canary-technologies/issue/ENT-7615/wyndham-scripting-change-to-support-ohip-migration
  Notion already has one page comment "This looks good to me." (2026-10-05 08:10, author not resolved).

  ### Claims verified against the repo
  - Gateway `OracleOHIPConfigurationSchema` has no streaming fields and sets `unknown = EXCLUDE`, so today it silently drops them (backend/pms-gateway/vendors/integrations/oracle_ohip/schemas/configuration.py).
  - `INCLUDED_FIELDS` in the gateway config service has no streaming entries; `upsert_configuration` goes through `common.utils.copy`, and `AccountService.__upsert_configuration` calls plain `configuration.save()` with no `full_clean()`, so `OracleOhip.clean_streaming_credentials` only runs from admin (accounts/services/account.py:483).
  - `copy()` skips `None` AND blank/whitespace strings, so a payload without streaming keys leaves stored streaming creds untouched. Correct as the doc says, and it also means the API can never clear them.
  - Model has the six `streaming_*` columns (PMS-10310, PR #55124). Socket only streams rows with `business_events_fetch_method=STREAM` and non-empty `streaming_app_key`, one socket per distinct (host, chain, streaming_app_key).
  - Canary sends `OhipConfiguration` via `dataclasses.asdict`, so adding fields to the dataclass is enough; the doc's file list is complete (the other `pms_gateway/schemas/configuration/oracle_ohip.py` is response-only).
  - UPDATE_PMS_CONFIGURATION risk is real: the Wyndham process runs `ConfigurePMSIntegrationUpdateConfigurationPlan` with `WyndhamPMSConfigProvider`, which re-PUTs the full config.

  ### Points to raise
  1. **The manual gateway step does not go away (product question).** New rows stay POLL. The ticket's goal is web events on canary2, which is STREAM mode. With this design every new Wyndham OHIP hotel still polls on canary1 until someone flips it in gateway admin, so the "keep using the bulk editor" alternative's downside is only half removed. Either state that plainly in the doc as accepted, or add `business_events_fetch_method` to the API as a follow-up. Connor and Khush should answer this; I would not block on it.
  2. **Gateway partial-set validation must treat blank as missing.** Because `copy()` drops "" as well as None, use truthiness (`data.get(k)`) in the `@validates_schema` check, otherwise `""` passes the all-or-none check and then never lands. Mirror the fetch-field length validators (app_key 3-64, client_id 3-127, client_secret 6-127).
  3. **Narrow the stated UPDATE_PMS_CONFIGURATION risk.** `copy()` only writes when values differ, and the optional `streaming_username/password/enterprise_id` are not in the proposed INCLUDED_FIELDS, so they survive. Only the three required creds get replaced, and only if the hand-set ones differ from the chain-code value. Same class of overwrite the stage already does for fetch creds today. Worth saying so Integrations is not scared off the update stage.
  4. **Canary-side all-or-none belongs in `DynamicOhipValuesSchema`** via `validates_schema`, so the OnboardingValue admin form rejects a partial value at edit time (there are form tests in onboarding/tests/admin/test_onboarding_value_form.py to extend). Also note Best Western and `cohort_hotel.py` / hotels agent_context read `DynamicOhipValues`; optional fields keep them unchanged.

  ### Answers to the open questions
  - Flat `streaming_` keys (my call): they match the gateway column names, need no rewrite of existing values, and pass through `asdict` untouched. Nested buys nothing.
  - Streaming unique index (host, streaming_app_key, chain, hotel) is fine with a shared canary2 app key per chain since hotel_code differs per row.
  - `_moved_onto_non_polling_client` save hook is not triggered here because top-level `client_id` stays canary1. That is exactly why open question 4 (do all chain-code values hold canary1 creds today) matters: a canary2 client_id at top level would silently disable housekeeping-overview fetch on save.

  ### Tests to ask for
  - Gateway: schema rejects a partial set and a blank member; upsert lands all three; payload without streaming keys preserves stored values.
  - Canary: provider passes the three through; existing value without the keys still loads; admin form rejects a partial set.

  ### Reviewers / next steps (for Gareth to do by hand)
  - Per Andrea, tag Khush on the gateway PR. I can take the Canary PR.
  - Suggested Linear reply (not posted):
    "Reviewed the doc, direction is good and the code claims check out. Four asks before implementation: (1) call out that new rows still stay POLL until gateway flips them, or add business_events_fetch_method to the API as a follow-up, Connor/Khush to decide; (2) gateway all-or-none check must treat blank strings as missing since copy() drops them; (3) the UPDATE_PMS_CONFIGURATION risk is narrower than stated, optional streaming_* fields survive and only differing required creds get replaced; (4) put the same all-or-none rule in DynamicOhipValuesSchema so the admin form rejects partial values. Flat streaming_ keys. Tag @khush on the gateway PR, I'll review the Canary one."
project: 2026-04-16T1210-unblock-team
source_id: https://linear.app/canary-technologies/issue/ENT-7615/wyndham-scripting-change-to-support-ohip-migration#comment-75699049
tags:
- morning-gtd
- linear
time_minutes: 30
title: 'Review ENT-7615 design doc: Wyndham scripting change to support OHIP migration'
updated: 2026-10-05 11:18:34.395441
waiting_on: null
waiting_since: null
working_on: false
---

2 new comments. Ryan posted the lightweight design doc and asked Andrea who should review; Andrea said tag Khush for anything touching gateway. Wyndham onboarding scripts are Enterprise-owned, so this needs my eyes.
Doc: https://app.notion.com/p/canarytechnologies/ENT-7615-Wyndham-scripting-change-to-support-OHIP-migration-3ed814686151812db733f7f9f2490d27
Issue: https://linear.app/canary-technologies/issue/ENT-7615/wyndham-scripting-change-to-support-ohip-migration