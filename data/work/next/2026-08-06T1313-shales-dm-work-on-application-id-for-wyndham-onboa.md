---
area: null
completed_at: null
contexts: []
created: 2026-08-06 13:13:16.434210
defer_until: null
due: 2026-08-06
energy: low
id: 2026-08-06T1313-shales-dm-work-on-application-id-for-wyndham-onboa
order: null
output: |
  ## Agent run 2026-08-06T14:05

  Researched ENT-7110 (https://linear.app/canary-technologies/issue/ENT-7110/store-ohip-application-id-in-canary-admin-onboarding-values-by-ohip)
  and drafted a rewrite. NOTHING POSTED TO LINEAR — draft is local only, at
  `/private/tmp/claude-501/-Users-garethlloyd-projects-canary/a83c6708-c10c-4154-b132-8900832c11d7/scratchpad/ent-7110-draft.md`

  Ticket is currently in Triage, no priority, no comments, created by Sharon Hales 2026-08-06.

  ### The key finding the ticket is missing

  The ticket says "add the OHIP Application ID as an onboarding value". It does not say
  **where it lives today**: the production App Key is a hardcoded literal
  `484c08ef-06e4-4e15-a108-dcf69d3b6d21`, identical for every chain code and both brands, in
  exactly two places:
    - backend/canary/onboarding/configuration_providers/wyndham/wyndham_pms_config_provider.py:167
    - backend/canary/onboarding/configuration_providers/best_western/pms_config_provider.py:181
    - (backend/pms-gateway/fixtures/oracle_ohip.json:91 — local fixture only)

  Every OTHER OHIP credential is already a per-chain-code onboarding value:
  `OnboardingValue.Kind.OHIP_CREDENTIALS_BY_CHAIN_CODE` (id type OHIP_CHAIN_CODE), read via
  `PmsConfigFromOnboardingValuesService.get_ohip_secrets_for_chain_code()`, shaped by
  `DynamicOhipValues` / `DynamicOhipValuesSchema` in
  backend/canary/onboarding/services/pms_config.py:22-44. The comment at pms_config.py:65 says it
  outright: *"the production schema omits app_key because production hardcodes it."*

  So this is a small, well-shaped change — and the staging twin
  (`STAGING_OHIP_CREDENTIALS_BY_IDENTIFIER` / `DynamicStagingOhipValues`, pms_config.py:47-76)
  ALREADY carries `app_key`, so the exact pattern is already proven in the codebase.

  ### Implementation shape (for the ticket)

  1. Add `app_key` to `DynamicOhipValues` + schema, optional at first. **No Django migration** —
     `OnboardingValue.data` is a JSONField and the Kind already exists. The kind is already in
     `SECRET_VALUE_KINDS` (models/onboarding_values.py:107) so it's masked in admin for free, and
     the admin form picks it up via `KIND_SCHEMAS` (onboarding/admin/onboarding_value.py:99).
  2. Both providers read `config_set.app_key or LEGACY_OHIP_APP_KEY` during migration.
  3. Backfill existing rows with the legacy key, then flip chain codes one at a time.
  4. Follow-up: make it required, delete the fallback.

  ### Scope split worth insisting on

  Ticket is ambiguous about **existing live hotels**. That's a data change on gateway `OracleOhip`
  rows, not an onboarding change, and should be a separate ticket. Tooling already exists — the
  gateway admin has a chain-code-scoped bulk editor that writes app_key
  (backend/pms-gateway/vendors/integrations/oracle_ohip/forms.py, `OhipBulkEditForm`).
  Two facts that de-risk it: app_key is part of the OAuth token cache key
  (oracle_ohip/models/configuration.py:428) so a flip invalidates tokens naturally; and it's part
  of the unique constraint (host_name, app_key, chain_code, hotel_code) (configuration.py:348) so
  in-place flips are safe and parallel rows are technically possible.

  ### Questions to put to Sharon (the actual value of this task)

  1. Does the new App Key come with a new client_id/client_secret? OHIP's x-app-key is normally
     bound to the OAuth client. If they move together this is "one more field on a row we already
     edit"; if independent, they need separate flips. Determines the runbook.
  2. New onboardings only, or existing hotels too? Description implies new only — confirm and split.
  3. Wyndham AND Best Western share the one hardcoded key today. Keying by chain code covers both
     automatically, but same schedule or Wyndham-first?
  4. UAT: staging value already has an app_key. Does the new portal issue a new UAT key too, and is
     UAT cut over first?
  5. Missing app_key for a chain code — silent fallback to legacy, or fail loud via
     `raise_expected_error` + pre-run check + `cohort_hotel.py` required-value entry?
  6. Is there a chain-code -> new App Key mapping from Oracle already, and how many chain codes?
     Sizing decides script vs. a few admin edits.

  ### Background found

  Sharon's own precursor message, #epd-pms-gateway 2026-05-08:
  https://canarytechnologies.slack.com/archives/C023K54M812/p1778220205174859
  "oracle ... suggested creating a new app-key - but that would mean we have to update every OHIP
  across every environment and every onboarding value!" — that is exactly the pain ENT-7110 fixes.
  (Thread itself then diverts into streaming/business-events config, not app keys.)

  Also relevant, migration is live now — Sharon in #ihg 2026-08-04:
  https://canarytechnologies.slack.com/archives/C03V5P4B48P/p1785858601317969
  "We are in the process of migrating environments... please drop the streaming set-up with the new
  OHIP ID here."

  ### Not done / caveats

  - Did NOT find the actual Shales DM — Slack search doesn't appear to index DMs. If the DM has
    constraints or a deadline, paste it and I'll fold it in.
  - Could not size the blast radius: `oracle_ohip_*` tables are not in the Snowflake gateway_raw
    CDC mirror, and no pg_query tool is connected. Needs a prod read (canary MCP / shell) to count
    chain codes and configs per chain code.
  ### Posted 2026-08-06T14:20

  On your approval, appended two sections to the ENT-7110 description (after the existing `## Why`,
  nothing else changed — still Triage, no priority/assignee/labels, title untouched):
    - `## Code change` — where the App Key is hardcoded, that the per-chain-code onboarding value
      already exists and just omits `app_key`, that no Django migration is needed, and that the
      staging schema already proves the pattern.
    - `## Open question` — does the new App Key arrive with a new client_id/client_secret.

  NOT added (deliberately, you said "no more") — still worth raising with Sharon separately:
    - scope split: existing live hotels are a gateway `OracleOhip` data change, separate ticket,
      `OhipBulkEditForm` already does the bulk flip by chain code
    - fail-loud vs silent fallback when a chain code has no app_key
    - UAT/staging cutover ordering; Wyndham-vs-BW schedule; sizing of the chain-code list

project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 5
title: Shales DM - clarify and improve ticket on application Id for wyndham onboarding
updated: 2026-08-06 14:20:00.000000
waiting_on: null
waiting_since: null
working_on: false
---

https://linear.app/canary-technologies/issue/ENT-7110/store-ohip-application-id-in-canary-admin-onboarding-values-by-ohip