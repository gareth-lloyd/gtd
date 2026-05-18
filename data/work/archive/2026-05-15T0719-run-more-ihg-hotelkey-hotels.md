---
area: null
contexts: []
created: 2026-05-15 07:19:30.613984
defer_until: null
due: 2026-05-15
energy: low
id: 2026-05-15T0719-run-more-ihg-hotelkey-hotels
order: -21
output: "## Agent run 2026-05-15T14:05\n\nReviewed ENT-6032 overview (backend/canary/tmp/investigations/)
  + consolidated.csv\n+ git history. Note: investigation snapshot is 2026-05-13; nothing
  in canary/pms\nprod was re-read this run (read-only prod audit offered below, not
  executed).\n\n### Recommendation: HOLD — do not run new HotelKey hotels yet. Two
  hard gates.\n\n**Gate 1 — env-166 V4 health unconfirmed (§9.13).** On 2026-05-13
  a direct V4\nprobe against IDACW (Yauheni's known-good bed from 05-01) returned
  401, same as\nATLPK. Until Yauheni/Mohak confirm env-166 is healthy (key fingerprint;\nFHKEX/HPNES
  still authenticating), any fresh `brand_identifier=\"ihg\"` config on\nenv 166 will
  401-storm on every V4 call (brand_identifier is load-bearing — empty\nis currently
  *protective*; §13). No HotelKey forward-provisioning OR retrofit\nshould run until
  this clears.\n\n**Gate 2 — rerun-idempotency fix not on master.** Commit 396f6bcdfbb
  (\"Fix\nAttributeError on HotelKey accounts in PMS create-config plan\", 2026-05-14)
  lives\nonly on this branch (`ihg-hotelkey-account-attr`), NOT master. It adds\n`dump_hotelkey`
  so `ConfigurePMSIntegrationCreateConfigurationPlan` detects an\nalready-configured
  account instead of re-upserting → duplicate-key error. Running\nthe create-config
  plan in batch before this merges is unsafe (no rerun guard).\nAction: get this branch
  reviewed + merged first.\n\n### Have they already run? No.\nOnly the OnboardingValue
  layer was seeded (§14, 2026-05-13 one-off shell upsert:\n22 FREEDOMPAY + 17 HOTEL_KEY
  = 39 rows). The create-config *plan itself* has not\nbeen executed for any Wave-1
  property. Existing pms-gateway HK configs (BHMBE,\nBHMBM, JAXWP, SBMWI + the 15
  on env 2) are pre-rollout / legacy 1-way, not script\noutput. Wave-0 FHKEX/HPNES
  never got OnboardingValues (not resolved in canary).\n\n### Next hotels to run on
  (the queue, once gates clear)\nCleanest = forward-provisioning Wave-1, NOT retrofit
  (avoids env-2→166 flip risk):\n- **PDXVN, SEACH** — pms-gateway Account exists,
  no HK config. Script creates a\n  fresh HK config on env 166. HK OnboardingValues
  already seeded (§14).\n- **CAEAT, LOAOH, PLYMS, SCFWI** — no pms-gateway Account.
  Script creates Account\n  + HK config. HK values seeded with *inferred* `canary-<code>`
  username (§14).\nThese 6 are the right first batch: their OnboardingValues exist,
  they're not\nduplicate-prone retrofits, and they exercise both the create-Account
  and\nconfig-on-existing-Account paths.\n\nExplicitly NOT next:\n- 15 retrofit props
  (BHMBE…SRTVL) — env-2→166 flip, blocked on Gate 1.\n- MTSCO HK — held, GNVAC webhook_password
  contamination (§9.11), needs HK regen.\n- CIDMA, DXRCT, SPADC — no canary Hotel;
  blocked upstream.\n- All Wave-2 — premature.\n\n### Suggested verification step
  (needs your approval — read-only prod)\nBefore any run, audit pms-gateway prod HotelKey
  configs by\n`api_host LIKE '%us-west-2.na.ihg.hkclients.com%'` to confirm the 6
  above have no\nHK config and capture current env_id/brand_identifier. I did NOT
  run this — say\nthe word and I'll do the read-only query.\n\n### Bottom line\nNothing
  to run today. Unblock order: (1) Yauheni/Mohak verify env-166;\n(2) merge branch
  `ihg-hotelkey-account-attr`; (3) run the 6-property forward batch\nabove; (4) revisit
  retrofit + MTSCO + CIDMA/DXRCT/SPADC separately.\n"
project: 2026-04-16T1351-ship
source_id: null
tags: []
time_minutes: 5
title: Review the IHG hotels ready for HotelKey
updated: 2026-05-15 14:21:31.531746
waiting_on: null
waiting_since: null
working_on: false
---

read tmp/investigations/ENT-6032-ihg-hotelkey-pilot-overview.md

Choose next hotels to run on. 
Check whether they've already run