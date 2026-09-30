---
area: null
completed_at: 2026-09-30 14:03:04.367084
contexts: []
created: 2026-09-30 09:08:51.199862
defer_until: null
due: null
energy: low
id: 2026-09-30T0908-add-thoughts-on-this-ticket
order: null
output: |
  ## Agent run 2026-09-30T13:55:03

  Ticket: ENT-7615 (https://linear.app/canary-technologies/issue/ENT-7615/wyndham-scripting-change-to-support-ohip-migration). Andrea Bradshaw asked for your high-level thoughts before the team picks it up. Nothing has been posted to Linear; draft below is for you to paste or edit.

  ### TL;DR
  Go with Option 1 (extend the existing OHIP_CREDENTIALS_BY_CHAIN_CODE value), but as flat optional `streaming_*` fields, not nested fetch/streaming objects. The onboarding-value change is the small part. The real gap is that the canary -> gateway config API does not carry streaming credentials at all, so most of the work lands in pms-gateway and has to ship first.

  ### What already exists (no work needed)
  - Gateway `OracleOhip` already has `streaming_app_key`, `streaming_client_id`, `streaming_client_secret` plus optional `streaming_username/password/enterprise_id` (PMS-10310, https://github.com/canary-technologies-corp/canary/pull/55124). The streaming socket was switched to use them in PMS-10312 (https://github.com/canary-technologies-corp/canary/pull/55129). Socket uses the streaming app_key/client_id/secret directly (no fallback to primary), and only falls back to primary username/password/enterprise_id when the streaming ones are blank. Polling and fetch use the primary creds. So the model already expresses exactly the canary1-fetch / canary2-stream split the ticket describes; hotel 21753 was presumably set up via admin or the bulk editor.
  - Model `clean_streaming_credentials()` rejects a partial set (needs all three of app_key/client_id/client_secret) and requires them when `business_events_fetch_method=STREAM`. There is a unique index on (host_name, streaming_app_key, chain_code, hotel_code).
  - Existing-hotel tooling already covers streaming fields: `OhipBulkEditForm` (per chain code) and the OHIP migration cockpit (Convert-to-STREAM). This ticket is only about the new-onboarding path.
  - Precedent for the value-shape change: ENT-7110 (https://github.com/canary-technologies-corp/canary/pull/52417) added optional `app_key`/`client_id` to `DynamicOhipValues` with fallbacks. Same pattern applies. Note the hardcoded fallback client_id is `canarytechnologies1_Client`, i.e. canary1, which is what the ticket wants as primary.

  ### Where the gap actually is (three layers)
  1. Onboarding value schema `DynamicOhipValuesSchema` in backend/canary/onboarding/services/pms_config.py has no streaming fields.
  2. Canary's `OhipConfiguration` dataclass (backend/canary/onboarding/configuration_providers/integrations_schemas/oracle_ohip.py) has no streaming fields, and `wyndham_pms_config_provider.py` does not pass any.
  3. Gateway `OracleOHIPConfigurationSchema` (backend/pms-gateway/vendors/integrations/oracle_ohip/schemas/configuration.py) has `unknown = EXCLUDE` and no streaming fields, and the upsert `INCLUDED_FIELDS` allowlist in services/configuration.py omits them. Anything the script sent today would be silently dropped.

  ### Option 1 vs Option 2
  Option 1, flat fields. Reasons:
  - The Wyndham provider does one lookup by `opera_chain_code`, and cohort_hotel.py registers one required value per chain. Option 2 adds a second required kind, a second lookup, and a second "missing value" failure mode in the cohort UI, for no benefit.
  - Flat rather than nested `{fetch: {...}, streaming: {...}}`: the admin form and the CSV field-mapping loader (`FieldMappingForm`, `KIND_SCHEMAS`) generate fields from the marshmallow schema, so flat fields keep the bulk-load tooling working and existing rows keep their shape. Nested objects would need form work and a data migration of existing values.
  - Backwards compatible: new fields `load_default=None`. Existing chain values, and Best Western's use of the same kind via best_western/pms_config_provider.py, keep working with no streaming creds.
  - Put the gateway's all-or-none rule for the three required streaming fields into the marshmallow schema too, so a half-filled value fails when the onboarding value is saved rather than at gateway upsert time during a script run.

  ### Suggested sequence (three PRs, gateway first)
  1. pms-gateway: add `streaming_*` to `OracleOHIPConfigurationSchema` and to `INCLUDED_FIELDS`. Re-run safety: the script upserts existing accounts (ENT-5945), and `common/utils/copy.py` does not overwrite a real value with None for included attributes, so canary must send None (not "") when the value has no streaming creds. Otherwise a re-run for a hotel already migrated via the cockpit would wipe its streaming creds. Worth a test.
  2. canary: extend `DynamicOhipValues`/schema, `OhipConfiguration`, and the wire mapping; pass through in the Wyndham provider (BW provider passthrough is harmless).
  3. Data: add the canary2 streaming creds to the WHRMP6 value (and any other Wyndham chain) in the OnboardingValue admin, and confirm the primary `client_id`/`app_key` on those values are the canary1 ones.

  ### Open questions for Connor
  - Fetch method at onboarding. The API does not expose `business_events_fetch_method`, so new US/CA hotels land on POLL with `supports_business_events=True`. Should the script set STREAM when streaming creds are present, or leave POLL and let the cockpit convert? Streaming needs the chain's publisher registered on canary2. My suggestion: ship the creds with POLL unchanged, run a few hotels through the cockpit, then decide on STREAM-at-onboarding as a follow-up. Going straight to STREAM also skips the cockpit's STREAM_POLLING / fetch_future_reservations step.
  - Non-US/CA Wyndham hotels get `supports_business_events=False`. Streaming creds on those rows are harmless (clean only demands them under STREAM). Confirm you want them populated regardless.
  - Staging: `STAGING_OHIP_CREDENTIALS_BY_IDENTIFIER` is a separate value. Leave it alone unless UAT also split portals.
project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 5
title: add thoughts on this ticket
updated: 2026-09-30 14:22:00.503564
waiting_on: null
waiting_since: null
working_on: false
---

https://linear.app/canary-technologies/issue/ENT-7615/wyndham-scripting-change-to-support-ohip-migration?noRedirect=1