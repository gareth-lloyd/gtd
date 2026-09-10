---
area: null
completed_at: null
contexts: []
created: 2026-09-09 12:52:59.521462
defer_until: null
due: null
energy: low
id: 2026-09-09T1252-note-https-linear-app-canary-technologies-issue-en
order: null
output: |
  ## Agent run 2026-09-10

  **Ticket:** ENT-7113 "Scope US-centric FINAL rules by region/capability" (https://linear.app/canary-technologies/issue/ENT-7113) — Backlog, assigned Tincho, project Configuration Drift Detection, 2 pts. No comments on it.

  ### Headline: instance 1 (tokenization) is already scoped; the ticket's premise is stale

  - The tokenization FINALs are NOT "mandated for every Wyndham hotel". In `backend/canary/enterprise_wyndham/configs/wyndham.py` they are defined on `WYNDHAM_NORTH_AMERICA_LIVE` = `GroupAttributes(parent_brand_id=WYNDHAM, msa=GMS, live_msa=GMS, countries={US, CA})`. Group added 2026-01-06 (PR #35650), rules moved onto it 2026-02-18 by Ryan in ENT-5355 (PR #38593, https://github.com/canary-technologies-corp/canary/pull/38593). Ticket was filed 2026-08-06, so the scoping predates it by ~6 months.
  - What the engine actually flags (Groundcover `detect_drift.non_conforming`, run 2026-09-09 07:46 UTC, cohort 4904 hotels, 64 with drift, 103 drift rows total):
    - `is_tokenizing_with_hotel_payment_gateway`: 45 hotels — 32 CA, 13 US. Zero MX/AR/EC/CL/DO.
    - `payment_gateway_config_id`: 35 hotels (subset of the 45 — the ones with no gateway at all).
    - `has_check_out`: 10 (ENT-7115's all-inclusive case; see below).
    - `integration_auto_post_to_pms`: 0. Sub-flags: only `_udf` on 1 hotel (Georgian Bay Hotel, id 5285).
  - The ticket's "154 drifting, Mexico 58, Canada 35..." is a raw-settings count across all Wyndham hotels, ignoring the region scope. Reproduced in Snowflake (CANARY_RAW): active wyndhamconnect hotels with tokenization off or no gateway = MX 63, CA 37, US ~17, AR 12, BR 6, EC 6, CL 5, DO 4... Same shape as the ticket, so that's where the numbers came from, not from the engine.

  ### The 45 US/CA hotels look like real drift, not PMS-native-by-design

  - 35/45 have NO payment_gateway_config at all (tokenization off); 10/45 have a gateway but tokenization off. All 45 have credit_card_step = required, all Opera Cloud except 3 Synxis.
  - Onboarding (`wyndham_enable_msa_products_provider.py:138`) only flips tokenization on when a gateway config exists — so these are hotels that went live without a Canary gateway ever being configured.
  - Concentrated in Canadian franchise groups: Holloway Lodging (7 Super 8, BC/AB/NWT), Royal Hotel Group (4), D3H Hospitality (4 Days Inn), Realstar (3), First Canadian Mgmt (2); plus 13 scattered US (La Quinta x3, AmericInn x3, Ramada x3, Wingate x2...). 136 other Canadian Opera Cloud hotels conform, so Canada's mainstream IS the hotel-gateway path.
  - Open business question (Implementation/Wyndham, not code): are these 45 allowed to be live collecting cards with no Canary gateway? If yes -> narrow the group to US-only (one-line change, drop `Country.CANADA`) or add a management-company carve-out. If no -> the rule is doing its job and the fix is to configure gateways.

  ### Instance 2 (auto-post family) is not a live problem

  - Engine flags 0 hotels on the parent flag and 1 on `_udf`. No Desbravador hotels in the live GMS cohort (pms is Opera Cloud / Synxis / NONE / null). The ticket's example may have come from a different cohort or from the pre-ENT-7042 roll-up era.
  - Capability gating is still a sound future-proofing idea but there is no current drift to fix.

  ### Pattern / mechanism findings

  - Region scoping already exists and is the reusable pattern: `GroupAttributes.countries` and `.canary_region` (see also IHG per-country configs in `enterprise_ihg/configs/countries/`). The "done when: a pattern others can reuse" is arguably satisfied by documenting this.
  - Capability scoping does NOT exist: `GroupAttributes` matches only on msa / live_msa / brand / parent_brand / management_company / countries / canary_region; `HotelAttributes` carries no capabilities. Adding it means (a) a `pms_capabilities` field on `HotelAttributes` fed from `hotel.pms_capabilities` (locally-synced M2M via `HotelPMSCapabilitiesService`), (b) a required-capabilities attribute on `GroupAttributes` with `matches_hotel` + `is_mutually_exclusive_with` semantics (negative predicates like "lacks PRE_CHECKIN" are awkward in the diamond-tree model).
  - Prior art to reuse instead: `pms_gateway/capability_driven_config/constants.py` already maps `integration_auto_post_to_pms <- Capability.PRE_CHECKIN in caps` (+ 7 sub-flags) as capability-derived defaults for CloudBeds. SDM-5045 (https://linear.app/canary-technologies/issue/SDM-5045) proposes exposing gateway/PMS capabilities as settings keys, which is the cleaner vehicle; ENT-7113 is linked to it as a consumer.

  ### ENT-7115 cross-check (has_check_out)

  Engine flags 10: 8 Decameron all-inclusives (MX/JM), Wyndham Quito Airport (EC), Wyndham Grand Costa Del Sol Lima Airport (PE), La Quinta Cincinnati Sharonville (US, also drifts has_check_in/has_chat — looks like a product-off hotel). Ticket's "~10 of 12 are Decameron" is roughly right (8 of 10).

  ### Recommended action (user decides)

  1. Comment on ENT-7113 correcting the premise and re-scoping it. Draft below — NOT posted, needs your OK.
  2. Either hand the 45-hotel list to Implementation (gateway not configured) or decide with Tincho to narrow the NA group to US-only. The hotel ids: CA no-gateway: 129240356,130153,17756,1872,1945,7651,129235940,15479,1578,129395,1934,15489,15487,2151,129234889,129234426,124156,1352,15495,17457,1577,17758,1317,15848,129823,1952,1598; CA gateway-but-off: 15496,2227,129234251,1624,1579; US no-gateway: 15440,2627,130003,129872,18464,18454,129993,124875; US gateway-but-off: 15449,15404,129245193,123996,125394.
  3. Consider re-estimating: instance 1 is done or a 1-line change; instance 2 folds into SDM-5045.

  ### Draft Linear comment for ENT-7113 (not posted)

  > Checked this against master and the live drift output (cron_detect_drift, 2026-09-09):
  >
  > **1. Tokenization** — already region-scoped. Both FINALs live on `WYNDHAM_NORTH_AMERICA_LIVE` (US + Canada, live GMS only) since ENT-5355 (Feb 2026). The engine flags 45 hotels on `is_tokenizing_with_hotel_payment_gateway` and 35 on `payment_gateway_config_id`, all US/CA — no Mexico, Argentina, Ecuador etc. The 154 / Mexico-58 figures are a raw-settings count over all Wyndham hotels, not engine drift.
  >
  > Of the 45: 35 have no payment gateway configured at all and 10 have one but tokenization off; all require a card at check-in. Onboarding only enables tokenization when a gateway exists, so these look like hotels that went live without a Canary gateway (mostly Canadian franchise groups: Holloway, Royal Hotel Group, D3H, Realstar). 136 other Canadian Opera Cloud hotels conform. Whether that is legitimate is a question for Implementation, not a rule-scoping bug. If it is legitimate, the fix is dropping `Country.CANADA` from the group.
  >
  > **2. Auto-post family** — engine flags 0 hotels on `integration_auto_post_to_pms` and 1 on `_udf`. No Desbravador hotels in the live GMS cohort. Nothing to fix today; capability gating would be future-proofing. `GroupAttributes` has no capability attribute, and adding one is non-trivial in the diamond-tree model. SDM-5045 (capability settings keys) is the better vehicle, and `pms_gateway/capability_driven_config` already encodes the PRE_CHECKIN -> auto-post mapping we'd want to reuse.
  >
  > Suggest re-scoping this to: (a) decide with Implementation on the 45 US/CA no-gateway hotels, (b) fold capability gating into SDM-5045, (c) document `GroupAttributes.countries` / `canary_region` as the region-scoping pattern.

  ### Evidence / sources

  - Code: `backend/canary/enterprise_wyndham/configs/wyndham.py` (groups L16-64, tokenization FINALs L359-366), `rules_based_configuration/services/conformity.py` (GroupAttributes L75-165, resolution L362-414), `rules_based_configuration/services/drift.py`, `pms_gateway/capability_driven_config/constants.py:65`.
  - Groundcover logs: `event:detect_drift.non_conforming` last 24h; `detect_drift.complete` 2026-09-09 07:46 UTC (hotels_checked 4904, hotels_with_drift 64, total_drift_count 103).
  - Snowflake CANARY_RAW.CANARY: HOTELS_HOTEL, CHECK_IN_CONFIGURATION, INTERNAL_SALESFORCEHOTELMETADATA (StoredHotelAttributes is not mirrored, so drift itself had to come from logs).
  - Related: ENT-7115 (https://linear.app/canary-technologies/issue/ENT-7115), ENT-7042 done (https://linear.app/canary-technologies/issue/ENT-7042), SDM-5045 (https://linear.app/canary-technologies/issue/SDM-5045).
  - No external writes made. No Salesforce access used.
project: null
source_id: null
tags: []
time_minutes: 5
title: note https://linear.app/canary-technologies/issue/ENT-7113/scope-us-centric-final-rules-by-regioncapability
  for investigation and action
updated: 2026-09-10 10:31:14.559503
waiting_on: null
waiting_since: null
working_on: false
---