---
area: null
contexts:
- react
created: 2026-06-15 11:38:19.334204
defer_until: null
due: null
energy: medium
id: 2026-06-15T1138-investigate-ramada-encore-by-wyndham-konya-selcukl
order: null
output: |
  ## Agent run 2026-06-15T12:55:00

  ### Summary
  Two onboarding-script failure emails for **Ramada Encore by Wyndham Konya Selcuklu**
  (SF account `001Qj000012BBKXIA4`, EU region). Both fired ~2026-06-12 19:33–19:34 UTC.
  **Both failures share one root cause: the PMS gateway cannot talk to / authenticate
  with this hotel's PMS.** This is almost certainly an onboarding-in-progress hotel whose
  PMS integration is not yet live (bad/missing credentials, account not activated, or
  IP not whitelisted) — not a code bug in the onboarding scripts.

  ### The two failures
  1. **validate_pms_configuration** (batch "Wyndham MSA - Validate PMS Config", plan
     `ConfigurePMSIntegrationValidatePlan`)
     - Error code: `pms_validation_failed_fetch_reservation`
     - "Gateway tried to fetch a reservation, but it failed."
     - Suggested action (from email): verify reservations exist on Gateway; if none, run
       PRE_POPULATE_RESERVATIONS; otherwise retry, then escalate to Enterprise.
     - Admin batch: https://eu.canarytechnologies.com/manage/onboarding/cohorts/58928695-8c7d-4f84-b257-9d9a2094217c/batches/f63a83ec-3ba3-409c-aacb-f170fc5677d3

  2. **configure_room_upgrades** (batch "57569 - config room upgrades", plan
     `ConfigureRoomUpgradesPlan`)
     - Error code: `pms_auth_error`
     - "Gateway cannot authenticate with the hotel's PMS." ← clearest signal
     - Admin batch: https://eu.canarytechnologies.com/manage/onboarding/cohorts/58928695-8c7d-4f84-b257-9d9a2094217c/batches/8ed3c1fd-bd70-414f-a9bf-3270318501f6

  Emails:
  - validate: https://mail.google.com/mail/u/0/#all/19ebd53a4dcb99d3
  - room upgrades: https://mail.google.com/mail/u/0/#all/19ebd542a6484c57

  ### Analysis
  The room-upgrades batch failed with `pms_auth_error` — Gateway could not authenticate
  with the PMS. The validate batch's `pms_validation_failed_fetch_reservation` is a
  consistent downstream symptom: if Gateway cannot authenticate, the FETCH_RESERVATION
  validation (which fetches the first reservation within ±6 days of today) will also fail.
  So the single underlying problem is **PMS connectivity/auth for this property**, with
  two plausible (non-exclusive) sub-causes:
  - Wrong / missing / not-yet-provisioned PMS credentials for the gateway account, or
    PMS-side access not enabled (account activation / IP whitelist), OR
  - No reservations have been fetched onto Gateway yet (PRE_POPULATE_RESERVATIONS not run).
    Given the parallel hard auth error, credentials/auth is the primary suspect.

  Code reference (where these errors are raised):
  - backend/canary/onboarding/plans/configure_pms_integration_validate_plan.py:76-83
    (maps each ValidationKind failure → pms_validation_failed_* error)
  - backend/canary/onboarding/configuration_providers/wyndham/wyndham_room_upgrades_provider.py
    (fetches rooms from PMS Gateway; auth failure surfaces as pms_auth_error)
  - Failure-email logic: backend/canary/onboarding/tasks/notify_run_failure.py (only
    ConfigurePMSIntegrationValidatePlan / ConfigureTwilioPlan / ConfigureRoomUpgradesPlan
    are monitored; one email per first failure per OnboardingScriptHotel).

  ### Could NOT verify live
  - canary-local MCP: down ("All connection attempts failed").
  - Datadog MCP: returned 0 results — it is wired to the US org, but this hotel/batches
    are EU (eu.canarytechnologies.com), so EU pms-gateway logs aren't reachable from here.

  ### Suggested next steps (for the user)
  1. Open the EU admin batch links above and check gateway integration health + the PMS
     gateway account credentials for this hotel.
  2. Confirm PMS type and that PMS-side access is enabled (credentials valid, IP whitelisted,
     account activated). The `pms_auth_error` is the thing to chase first.
  3. Once auth is fixed: re-run validate. If it then fails only on fetch_reservation because
     no reservations exist, run PRE_POPULATE_RESERVATIONS, then re-run validate + room upgrades.
  4. If this hotel simply isn't integration-ready yet, this is expected onboarding noise and
     can be re-attempted once Integrations confirms the PMS connection.
project: null
source_id: https://mail.google.com/mail/u/0/#all/19ebd53a4dcb99d3
tags:
- morning-gtd
- gmail
time_minutes: 20
title: Investigate Ramada Encore by Wyndham Konya Selcuklu onboarding failures (validate_pms_configuration
  + configure_room_upgrades)
updated: 2026-06-15 12:55:00.000000
waiting_on: null
waiting_since: null
working_on: false
---

Onboarding script failure emails Jun 13. Same hotel failed both validate PMS config and room upgrades.
https://mail.google.com/mail/u/0/#all/19ebd53a4dcb99d3