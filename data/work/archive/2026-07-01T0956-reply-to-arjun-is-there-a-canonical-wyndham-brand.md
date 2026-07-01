---
area: null
contexts:
- react
created: 2026-07-01 09:56:05.282340
defer_until: null
due: null
energy: medium
id: 2026-07-01T0956-reply-to-arjun-is-there-a-canonical-wyndham-brand
order: null
output: |
  ## Agent run 2026-07-01T15:40 (investigation + draft reply)

  ### The question
  Arjun (VOX-3314) is building the Wyndham GenRes booking voice agent. He hardcoded a
  brand-name → 2-letter CRS-code enum (`WyndhamBrand` StrEnum) in
  `backend/canary/voice/livekit/call_center/agents/wyndham/agents/genres/brand_codes.py`
  (PR #48821, https://github.com/canary-technologies-corp/canary/pull/48821), pulled from the
  FQA env because the Mulesoft token can't reach the property-search APIs in Prod yet. He asks
  if there's a canonical source he should consume instead.
  Andrea already pointed at the `Brand` model / `external_brand_code` field and asked me for
  concerns. Slack thread: https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1782833203540209

  ### What the enum encodes (PR #48821)
  16 brands, each `CODE = (code, *spoken_names)` — e.g. `DI = ("DI", "Days Inn")`,
  `WY = ("WY", "Wyndham", "Wyndham Garden", "Wyndham Grand")`. Two jobs:
  (a) the 2-letter `value` is matched against the Mulesoft `PropertyAvailability.hotel.brand`
  field to filter results (`_filter_brand`: `pa.hotel.brand.upper() == brand.value`); and
  (b) the `spoken_names` feed the LLM prompt so it can map conversational speech → code.

  ### Is there a canonical source? Yes, in principle — Andrea is right.
  - `Brand` model: `backend/canary/hotels/models/brand.py`. Has `external_brand_code`
    (CharField(max_length=16), null/blank) — help_text literally: "An external brand identifier
    used to map incoming data to brands in Canary. Example: 'CY' is 'Courtyard by Marriott'."
    That is exactly the shape of a CRS brand code.
  - `BrandSelector.get_wyndham_managed_brands()` already exists
    (`backend/canary/hotels/selectors/brand.py`): filters
    `Brand.objects.filter(parent_name="Wyndham Hotels & Resorts, Inc.")`. So Wyndham brand rows
    ARE in the table and there's already a scoped selector to pull them.
  - Brands are sourced from Salesforce (`SALESFORCE_BRAND_TO_BRAND_INSTANCE_SLUG` +
    `BrandService.get_or_create_brand`), so the table is the system of record for "which brands
    exist under Wyndham".
  - I found NO other canonical brand→2-letter-code table anywhere in the repo. `Brand.external_brand_code`
    is the only real candidate.

  ### Concerns to raise before flipping over (my informed opinion)
  1. **Empty today.** Andrea confirmed `external_brand_code` isn't populated for most Wyndham
     brands. Consuming from the DB yields nothing until someone backfills. So this is a
     backfill-first migration, not a same-PR swap. Arjun offered to backfill once he has
     Mulesoft Prod access — that's the right owner, but it gates the switch.
  2. **Global-uniqueness assumption / cross-parent collision risk — the biggest one.** Two
     existing consumers look the field up GLOBALLY and unscoped:
       - `onboarding/services/vendor/marriott_properties_batch_update_service.py:332`
         `Brand.objects.get(external_brand_code=row.brand_code.lower())`
       - `tips/services/brand_template.py:151` same pattern.
     These assume `external_brand_code` is globally unique (no unique constraint exists, but the
     `.get()` calls behave as if there is). Wyndham's 2-letter CRS codes could collide with
     Marriott's 2-letter codes (Marriott's own example is "CY"). If any Wyndham code equals an
     existing Marriott/other code, those `.get()` calls throw `MultipleObjectsReturned` and break
     the Marriott property batch update + tips brand-template flows — unrelated to voice.
     → Before backfilling, either (a) verify no code collisions across parents, or (b) scope
     those two lookups by parent. Arjun's own reads are safe as long as he stays within
     `get_wyndham_managed_brands()`.
  3. **Case convention.** Existing data is stored lowercased and looked up via `.lower()`
     (comment at marriott service :331 "We store the brand codes as `.lower()` strings").
     Arjun's enum + Mulesoft compare `.upper()`. Pick one normalization and apply on read/write.
  4. **Spoken-name aliases have no home in the Brand model.** Brand has only `name`/`parent_name`,
     no alias field. The enum's multi-alias rows (WY → Wyndham / Wyndham Garden / Wyndham Grand;
     BH → Hawthorn / Hawthorn Suites) partly map to separate Brand rows sharing one code, which
     is fine — but the hand-tuned conversational aliases for the LLM are presentation, not
     system-of-record. Reasonable to KEEP the spoken-name→code prompt list in code even after
     the code VALUES come from the DB.

  ### Recommendation
  Endorse Andrea's direction: `Brand.external_brand_code` (via `get_wyndham_managed_brands()`)
  is the right canonical home for the code list, and it avoids drift from a hand-maintained enum.
  But: (1) it's a backfill-first change — the enum is a fine interim for the FQA/search-only PR
  #48821, so no need to block that PR; (2) before backfilling, audit for 2-letter collisions with
  existing (Marriott) codes OR parent-scope the two unscoped `Brand.objects.get(external_brand_code=…)`
  lookups, else populating Wyndham codes can break Marriott/tips flows; (3) standardize case; (4) the
  conversational spoken-name aliases can stay in code. Suggest a small follow-up ticket to source
  the code values from the Brand model once populated + Prod access lands.

  ### Draft Slack reply (NOT SENT — awaiting Gareth's approval to post)
  > Dug in — agree with Andrea, `Brand.external_brand_code` is the right canonical home (and
  > `BrandSelector.get_wyndham_managed_brands()` already scopes to the Wyndham parent, so reading
  > the codes off those rows is clean). Two things I'd want handled before we backfill it, not
  > blockers for this search-only PR:
  > 1. Those codes are only 16 slow-moving values, so the enum is a fine interim — but the field
  >    is empty today, so this is backfill-first, then swap. Happy for you to fill it once you
  >    have Mulesoft Prod.
  > 2. Bigger one: `external_brand_code` is looked up GLOBALLY and unscoped in two places
  >    (marriott_properties_batch_update_service.py:332 and tips/brand_template.py:151 —
  >    `Brand.objects.get(external_brand_code=code.lower())`). No unique constraint, so if a
  >    Wyndham 2-letter code collides with an existing Marriott code (their example is "CY"),
  >    those `.get()`s start throwing MultipleObjectsReturned and break Marriott property + tips
  >    flows. Before backfilling let's either confirm no cross-parent collisions or parent-scope
  >    those two lookups. Also note the stored convention is lowercased (`.lower()` on read); your
  >    enum/Mulesoft compare `.upper()`, so normalize.
  > The conversational alias list (Wyndham/Wyndham Garden/Wyndham Grand → WY etc.) is fine to keep
  > in code as prompt tuning even after the code values move to the DB. Want me to file a small
  > follow-up to source the codes from the Brand model?

  ### Corroborating detail (repo-wide search)
  A full-repo sweep confirms there is NO name→2-letter-code lookup table anywhere; the codes
  flow in from Wyndham's Mulesoft/SynXis CRS and are stored per-hotel:
  - `crs_gateway/mulesoft/models/configuration.py:29-31` — `MulesoftConfiguration.brand_code`
    (from Mulesoft's `brandIdC`), populated per configured hotel from the API, not a mapping.
    This is a potential backfill source for `Brand.external_brand_code` (join configured Wyndham
    hotels' Mulesoft brand_code → their Brand rows).
  - `onboarding/services/vendor/ice_portal/api.py:37` — `WYNDHAM_CHAIN_CODE = "WY"` (chain-level
    constant, not the per-brand list).
  - `chat/services/amb_bot_flows/wyndham.py` — Wyndham booking flow uses `hotel.brand` for a
    specific hotel, not a brand→code map.
  - Watch out: 2-letter codes are ambiguous across domains — e.g. SynXis payment card types use
    "DI" = Discover (`pms-gateway/.../synxis/models/configuration.py:22`), unrelated to Days Inn.
    Reinforces concern #2: never look these up globally/unscoped.
project: null
source_id: https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1782833203540209
tags:
- morning-gtd
- slack
- from-awareness
time_minutes: 15
title: 'Reply to Arjun: is there a canonical Wyndham brand→CRS-code list for the booking
  voice agent?'
updated: 2026-07-01 15:24:19.758352
waiting_on: null
waiting_since: null
working_on: false
---

#epd-enterprise — Arjun hardcoded a brand-name→2-letter-CRS-code enum (pulled from FQA) for the Wyndham booking voice agent and asks if there's an existing canonical source he should consume instead. Your onboarding domain. https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1782833203540209