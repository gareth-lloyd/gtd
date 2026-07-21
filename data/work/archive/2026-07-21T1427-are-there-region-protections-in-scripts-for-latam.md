---
area: null
contexts: []
created: 2026-07-21 14:27:23.939378
defer_until: null
due: null
energy: low
id: 2026-07-21T1427-are-there-region-protections-in-scripts-for-latam
order: null
output: |
  ## Agent run 2026-07-21T14:45:00

  **Yes — there are hard region protections that specifically exclude LATAM for Wyndham Connect Plus (WCP).** This is almost certainly why Marta sees "no option to create a WCP cohort" for the LATAM site ID.

  ### The single source of truth
  `backend/canary/onboarding/services/salesforce_onboarding_region_validation.py:40-66` —
  `CANARY_REGION_COUNTRY_MAP_BY_ONBOARDING_TYPE`. For WCP (lines 53-56):
  ```python
  OnboardingType.WYNDHAM_CONNECT_PLUS: {
      CanaryRegion.US: {Country.UNITED_STATES, Country.CANADA},
      CanaryRegion.EU: set(),
  },
  ```
  WCP is restricted to **US + Canada only**. LATAM is not present in any region for WCP.

  Contrast: `WYNDHAM_MSA` and `WYNDHAM_TIPPING` (lines 41-48) explicitly add `set(WYNDHAM_LATAM_COUNTRIES)` to their US-region set, so MSA/Tipping DO allow LATAM — WCP deliberately does not. `WYNDHAM_AI_VOICE` is likewise US/CAN only.

  `WYNDHAM_LATAM_COUNTRIES` (the 28-country set incl. Mexico, Brazil, Argentina, Dominican Republic, etc.) is defined in `backend/canary/onboarding/services/vendor/wyndham_definitions.py:53-85`.

  ### Two enforcement points, both driven by that map

  1. **Sync/routing filter (why the option is missing).**
     `onboarding/services/salesforce_onboarding_fields.py:331-349` `_is_opportunity_for_region()` calls `is_ent_opportunity_allowed_in_region()` (region_validation.py:200-211). A WCP opportunity whose country is a LATAM country is filtered OUT when syncing opportunities into the US region — so the WCP opportunity/account never becomes selectable in the tool for that site ID.

  2. **Cohort-creation guard (would block it even if attempted).**
     `SalesforceOnboardingRegionValidationService.validate_accounts_for_current_region()` (region_validation.py:151-198) raises `RegionNotAllowed` (422) for any account whose billing country is not in the allowed set. It is called from every cohort mutation path:
     - `onboarding/services/cohort_hotel.py:314` (`get_or_create_cohort_hotels_for_onboarding_type`)
     - `onboarding/services/cohort_hotel.py:351` (`get_or_create_cohort_hotels_for_cohort`)
     - `onboarding/services/cohort_hotel.py:406` (`add_to_cohort`)
     - `onboarding/services/onboarding_batch.py:422`

  ### Related (separate) region guards, for context
  - `onboarding/checks/wyndham.py:15-31` `check_hotel_country_against_region` — EMEA/SEAPR must deploy to EU, everything else must NOT be on EU/APAC. This is about EU-region routing, not the LATAM/WCP block.
  - `onboarding/checks/wyndham.py:34-52` payment-gateway check is US/Canada-only.

  ### Bottom line for the Slack thread
  The block is intentional config, not a bug: WCP's allowed-country map has never included LATAM. To launch the first LATAM WCP property, someone needs to **add the relevant LATAM country/countries to the `WYNDHAM_CONNECT_PLUS` US-region set** (mirroring how MSA/Tipping already include `WYNDHAM_LATAM_COUNTRIES`) — likely gated on whatever WCP LATAM readiness work (WhatsApp messaging, payments, phone provisioning) is actually done. Worth confirming with the WCP/enterprise team whether LATAM WCP is production-ready before flipping it, rather than just widening the allowlist. A one-line-ish code change + tests + deploy is the ticket Marta is asking about.

  Slack thread: https://canarytechnologies.slack.com/archives/C08P0M47GPQ/p1784555938264569
project: null
source_id: null
tags: []
time_minutes: 5
title: Are there region protections in scripts for LATAM wyndham connect plus properties?
  explore code
updated: 2026-07-21 14:33:12.764460
waiting_on: null
waiting_since: null
working_on: false
---

https://canarytechnologies.slack.com/archives/C08P0M47GPQ/p1784555938264569