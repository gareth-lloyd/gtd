---
area: null
contexts:
- react
created: 2026-05-20 10:18:44.790047
defer_until: null
due: null
energy: low
id: 2026-05-20T1018-respond-on-ent-6268-shahzan-hotel-idsnext-onboardi
order: null
output: '## Agent run 2026-05-20T15:05:00


  Investigated ENT-6268. Confirmed it''s the same bug pattern as PR #45517 (HotelKey),
  this time for IDS Next.


  **Root cause**: `ConfigurePMSIntegrationCreateConfigurationPlan.execute` (backend/canary/onboarding/plans/configure_pms_integration_create_configuration_plan.py:78)
  does `getattr(account, vendor.value)` where `Vendor.IDS_NEXT.value == "ids_next"`.
  The canary `Account` dataclass + `AccountSchema` (backend/canary/pms_gateway/schemas/account.py)
  has no `ids_next` field, so the lookup raises `AttributeError` and surfaces as `OnboardingServiceError`
  on the Configure PMS step. `PMS_VENDOR_MAP` already wires `IDSNextConfiguration
  → Vendor.IDS_NEXT` (configure_pms_integration_base.py:32), so any IDS Next hotel
  will hit this on re-run.


  **Fix scope** (mirror PR #45517):

  1. New `IDSNextConfiguration` schema at `backend/canary/pms_gateway/schemas/configuration/ids_next.py`

  2. Add `ids_next` field on `Account` dataclass + `AccountSchema`

  3. Add `dump_ids_next` on `GetAccountResponseSchema` in `backend/pms-gateway/accounts/views/account.py`


  **Workaround for Shahzan**: skip `CREATE_PMS_CONFIGURATION`, resume from `VALIDATE_PMS_CONFIGURATION`
  — IDS Next config already exists in the gateway.


  Drafted two Linear updates (NOT posted — waiting for user approval):

  - Comment to mziaei explaining the bug + workaround

  - Reworked ticket title/description/labels turning ENT-6268 into a proper bug ticket
  (proposed title: "ConfigurePMSIntegrationCreateConfigurationPlan raises AttributeError
  for IDS Next accounts"; add `Bug` label; keep Medium priority and Triage status)


  Both drafts shown in chat. User needs to confirm before I touch Linear, and likely
  needs to decide whether to take the fix on this branch or spin up a separate one.


  ## Agent run 2026-05-20T15:15:00


  User cleared the ticket rework only. Updated ENT-6268:

  - New title: "ConfigurePMSIntegrationCreateConfigurationPlan raises AttributeError
  for IDS Next accounts"

  - Description rewritten as a bug ticket with root cause, fix scope, and workaround.
  Inciting incident (Marta''s report) + cohort/admin/gateway links preserved under
  "Inciting incident".

  - Added `Bug` label (kept `Wyndham`, `Canary Admin`)

  - Priority Medium, status Triage unchanged


  Marta comment (Draft A) NOT posted — separate approval needed. The reworked ticket
  body now contains enough for her to self-serve if she sees the update.

  '
project: null
source_id: https://linear.app/canary-technologies/issue/ENT-6268/missing-onboarding-values-for-idsnext-57785-shahzan-hotel-kuantan
tags:
- morning-gtd
- linear
time_minutes: 15
title: 'Respond on ENT-6268: Shahzan Hotel IDSNext onboarding error'
updated: 2026-05-20 14:42:54.736188
waiting_on: null
waiting_since: null
working_on: false
---

mziaei added the IDSNext ID I gave her but got OnboardingServiceError on Configure PMS step. https://linear.app/canary-technologies/issue/ENT-6268/missing-onboarding-values-for-idsnext-57785-shahzan-hotel-kuantan

This is a real bug we encountered for hotelkey: https://github.com/canary-technologies-corp/canary/pull/45517

Rework the ticket as an ENT triage bug ticket