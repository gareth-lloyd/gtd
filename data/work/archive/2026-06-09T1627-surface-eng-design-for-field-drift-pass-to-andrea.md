---
area: null
contexts: []
created: 2026-06-09 16:27:46.715334
defer_until: null
due: null
energy: low
id: 2026-06-09T1627-surface-eng-design-for-field-drift-pass-to-andrea
order: null
output: |
  ## Agent run 2026-06-11T13:43

  Drafted the PRD: /Users/garethlloyd/projects/gtd/drafts/drift-detection-prd.md

  Grounded it in the actual code in the canary repo
  (backend/canary/rules_based_configuration/): StoredHotelAttributes model,
  ConformityService (diamond tree, FINAL vs FREE override policies),
  MSA enum, and management/commands/detect_drift.py (currently manual,
  log-only, Wyndham Connect GMS only via MSA_HOTEL_PROVIDERS).

  PRD structure: problem (drift from contractual enterprise rules is
  invisible until incident), goals/non-goals (V1 = detect & surface only;
  no auto-remediation, no alerting), background on conformity machinery,
  proposed V1 — (a) cached `drifts` ArrayField + `drifts_calculated_at`
  on StoredHotelAttributes, (b) Django Admin filters by MSA / brand
  attributes / drifted keys with expected-vs-actual on detail page,
  (c) daily job building on detect_drift.py that writes results to the
  cached field — plus user flows, success criteria, risks (false
  positives, cohort coverage gaps, array-filter UX, triage ownership),
  and post-V1 directions.

  Next steps (yours): review the draft, then pass to Andrea — happy to
  push it to Notion/Google Docs on request (external write, needs your
  approval).

  ## Agent run 2026-06-11T13:47

  Per your approval, created a private Notion page with the full PRD:
  "PRD: Configuration Drift Detection for Enterprise Hotels"
  (https://app.notion.com/p/37c814686151813884b7d338378b5c18).
  It's a workspace-level private page — share with Andrea when ready.
project: null
source_id: null
tags: []
time_minutes: 5
title: Create a high-level PRD for "drift detection" relative to the rules-based configuration
  for enterprises (Wyndham, Best Western, etc)
updated: 2026-06-11 14:09:44.303178
waiting_on: null
waiting_since: null
working_on: false
---

This is a PRODUCT document, not an engineering design. Anchor on product aims, but DO include the specific implementation details sketched out here. 

Should cover the aims of this (highlight departure from rules in enterprises)

where it should be surfaced: V1 is a Django Admin for StoredHotelAttributes which can expose drift
* Filter by MSA
* Filter by other attributes
* Filter by a cached `drifts` field which notes all attribute keys that have drifted.

Regular job to calculate. build on rules_based_configuration/management/commands/detect_drift.py