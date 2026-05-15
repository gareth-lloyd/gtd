---
area: null
contexts: []
created: 2026-05-15 07:19:30.613984
defer_until: null
due: 2026-05-15
energy: low
id: 2026-05-15T0719-run-more-ihg-hotelkey-hotels
order: -21
output: |
  ## Agent run 2026-05-15T14:05

  Reviewed ENT-6032 overview (backend/canary/tmp/investigations/) + consolidated.csv
  + git history. Note: investigation snapshot is 2026-05-13; nothing in canary/pms
  prod was re-read this run (read-only prod audit offered below, not executed).

  ### Recommendation: HOLD — do not run new HotelKey hotels yet. Two hard gates.

  **Gate 1 — env-166 V4 health unconfirmed (§9.13).** On 2026-05-13 a direct V4
  probe against IDACW (Yauheni's known-good bed from 05-01) returned 401, same as
  ATLPK. Until Yauheni/Mohak confirm env-166 is healthy (key fingerprint;
  FHKEX/HPNES still authenticating), any fresh `brand_identifier="ihg"` config on
  env 166 will 401-storm on every V4 call (brand_identifier is load-bearing — empty
  is currently *protective*; §13). No HotelKey forward-provisioning OR retrofit
  should run until this clears.

  **Gate 2 — rerun-idempotency fix not on master.** Commit 396f6bcdfbb ("Fix
  AttributeError on HotelKey accounts in PMS create-config plan", 2026-05-14) lives
  only on this branch (`ihg-hotelkey-account-attr`), NOT master. It adds
  `dump_hotelkey` so `ConfigurePMSIntegrationCreateConfigurationPlan` detects an
  already-configured account instead of re-upserting → duplicate-key error. Running
  the create-config plan in batch before this merges is unsafe (no rerun guard).
  Action: get this branch reviewed + merged first.

  ### Have they already run? No.
  Only the OnboardingValue layer was seeded (§14, 2026-05-13 one-off shell upsert:
  22 FREEDOMPAY + 17 HOTEL_KEY = 39 rows). The create-config *plan itself* has not
  been executed for any Wave-1 property. Existing pms-gateway HK configs (BHMBE,
  BHMBM, JAXWP, SBMWI + the 15 on env 2) are pre-rollout / legacy 1-way, not script
  output. Wave-0 FHKEX/HPNES never got OnboardingValues (not resolved in canary).

  ### Next hotels to run on (the queue, once gates clear)
  Cleanest = forward-provisioning Wave-1, NOT retrofit (avoids env-2→166 flip risk):
  - **PDXVN, SEACH** — pms-gateway Account exists, no HK config. Script creates a
    fresh HK config on env 166. HK OnboardingValues already seeded (§14).
  - **CAEAT, LOAOH, PLYMS, SCFWI** — no pms-gateway Account. Script creates Account
    + HK config. HK values seeded with *inferred* `canary-<code>` username (§14).
  These 6 are the right first batch: their OnboardingValues exist, they're not
  duplicate-prone retrofits, and they exercise both the create-Account and
  config-on-existing-Account paths.

  Explicitly NOT next:
  - 15 retrofit props (BHMBE…SRTVL) — env-2→166 flip, blocked on Gate 1.
  - MTSCO HK — held, GNVAC webhook_password contamination (§9.11), needs HK regen.
  - CIDMA, DXRCT, SPADC — no canary Hotel; blocked upstream.
  - All Wave-2 — premature.

  ### Suggested verification step (needs your approval — read-only prod)
  Before any run, audit pms-gateway prod HotelKey configs by
  `api_host LIKE '%us-west-2.na.ihg.hkclients.com%'` to confirm the 6 above have no
  HK config and capture current env_id/brand_identifier. I did NOT run this — say
  the word and I'll do the read-only query.

  ### Bottom line
  Nothing to run today. Unblock order: (1) Yauheni/Mohak verify env-166;
  (2) merge branch `ihg-hotelkey-account-attr`; (3) run the 6-property forward batch
  above; (4) revisit retrofit + MTSCO + CIDMA/DXRCT/SPADC separately.
project: 2026-04-16T1351-ship
source_id: null
tags: []
time_minutes: 5
title: Review the IHG hotels ready for HotelKey
updated: 2026-05-15 14:05:00.000000
waiting_on: null
waiting_since: null
working_on: false
---

read tmp/investigations/ENT-6032-ihg-hotelkey-pilot-overview.md

Choose next hotels to run on. 
Check whether they've already run