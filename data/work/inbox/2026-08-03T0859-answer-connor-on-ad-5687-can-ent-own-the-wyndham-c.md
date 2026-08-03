---
area: null
completed_at: null
contexts:
- react
created: 2026-08-03 08:59:34.446915
defer_until: null
due: 2026-08-03
energy: medium
id: 2026-08-03T0859-answer-connor-on-ad-5687-can-ent-own-the-wyndham-c
order: null
output: |
  ## Agent run 2026-08-03T07:27Z

  Researched AD-5687 to answer Connor's two questions. Nothing sent anywhere — Slack
  reply drafted below, awaiting your approval.

  Links: [AD-5687](https://linear.app/canary-technologies/issue/AD-5687/reg-remove-chinese-territories-from-country-dropdown)
  · [Slack thread](https://canarytechnologies.slack.com/archives/C04STT7UPRQ/p1785715264112599)
  · [PR #28894](https://github.com/canary-technologies-corp/canary/pull/28894)

  ### Q1: Is the country list easily editable per customer? — No. It isn't editable at all.

  The dropdown is built entirely client-side from the `i18n-iso-countries` npm package;
  there is no backend country API. The single chokepoint is
  `frontend/packages/shared/helpers/CountryNamingHelper.ts` → `getCountryNames()` (L575).

  PR #28894 added a **hardcoded slug allowlist**, not a config:
  - `HIDDEN_COUNTRIES_FOR_SPECIFIC_HOTELS` (L205) = `["HK", "MO", "TW", "RE"]`
  - `HOTEL_SLUGS_TO_HIDE_COUNTRIES_OF_CHINA` (L212) = `["local-hotel", "grandover-resort-conference-centerspagolf"]`

  So exactly **one** real hotel has ever had this applied — Grandover Resort
  (= Wyndham Greensboro, sso_hotel_id 57283). That answers Ani's question in the thread:
  it wasn't applied to all sites because there was never a mechanism to; the "fix" was
  adding one string to a TypeScript array.

  Correction to Vibhor's part 1: the hidden-codes list **already covers all four**
  (HK, MO, TW, RE) including Macao. Part 1 as scoped is close to a no-op — what's
  missing is *scope*, not coverage. Worth a separate decision on whether more codes
  are wanted, but don't budget engineering time for "add the missing countries".

  Separate second list in the same file: `CHINESE_COUNTRY_NAME_OVERRIDE_HOTEL_LIST`
  (~30 slugs, L168) which **renames** rather than removes (Mainland China / Hong Kong SAR
  / Macao SAR / Taiwan, China). Two lists must be kept in sync — the `CN → "China"`
  relabel at L644 only fires when a slug is in *both*.

  Scale check: ~6,551 Wyndham slugs in `backend/canary/tmp/onetime/wyn/Hotel-2025-06-27.csv`
  (approximate, June-2025 onboarding file). A slug allowlist is definitively not the answer.

  ### Q2: Can/should ENT handle it? — Parts 2+3 yes, but they're blocked, and there's a cheaper today-fix.

  Parts 2+3 ("apply config to all existing Wyndhams", "update onboarding scripts") are
  exactly ENT-shaped and I'm happy to own them — but they can't start, because **there is
  no config to apply**. Part 1 is a hard blocker and it's a platform/schema change, not ENT.

  Two options, and I'd recommend doing A today and B properly:

  **Option A — ships today, frontend-only, ~half a day.** The check-in hotel payload
  already carries `portfolio_identifiers`, and there is already an `isWyndham()` helper at
  `frontend/packages/shared/helpers/hotel.ts:42` used elsewhere in check-in. Swap the slug
  allowlist for a portfolio check. Covers all ~6.5k Wyndhams instantly — **no backfill, no
  onboarding-script change, parts 2 and 3 disappear for today's ask**. Explicitly a stopgap.

  **Option B — the real fix (Vibhor's config).** Cheapest correct home is a new field on
  `check_in.Configuration` (`backend/canary/check_in/models/configuration.py:185`),
  serialized through `CheckInConfigurationSchemaExternal`
  (`backend/canary/check_in/schemas/check_in_configuration_external.py`). That payload
  already lands on `hotelStore.hotel.check_in_configuration` in **both** check-in v1 and
  guest-experience v2/v3 — one backend change covers both frontends. Precedent for the
  shape: `guest_gender_options` ArrayField (configuration.py:937), `blocked_card_networks`
  (L531). Then parts 2+3 are a straightforward ENT backfill + onboarding script.

  Note on Vibhor's "config on the reg card builder": that's the more *correct* home, but
  it's meaningfully more work — `CountryElementAttributes`
  (`backend/canary/schema_form/schemas/elements/country_element.py`) currently has only
  label/placeholder/is_required/is_readonly, so it needs new attrs + builder UI +
  extendable/extension merge handling. And it makes part 2 a backfill over reg-card JSON
  for 6.5k hotels instead of one config column. Worth flagging that trade before we commit.

  ### Bugs to flag regardless of which option we pick

  1. **The existing mechanism is silently dead on v2/v3 check-in.**
     `frontend/guest-experience/src/views/check_in/steps/schema_form/SchemaFormStep.vue:227`
     renders `<SchemaForm>` **without** `:hotel-slug`. `SchemaForm.vue:71` defaults it to
     `undefined`, so `getCountryNames()` gets `null` and all hiding/renaming no-ops. If
     Grandover is on v2/v3, PR #28894 is *already not working* there. Any fix must key off
     `hotelStore` config (which v2/v3 does have) rather than the slug prop — Option B fixes
     this incidentally, Option A must thread the prop or read the store.
  2. **Hiding is cosmetic.** Submit-side validation accepts any ISO-2 code —
     `country_element.py:8 is_iso_country()` only checks `len == 2`, and
     `frontend/check-in/src/checkIn/RegistrationCardSubmitter.ts:743 isValidCountry()`
     checks the raw unfiltered list. A PMS-prefilled `TW` still submits fine.
  3. **The reg-card builder's "Default value" picker is a separate hardcoded list**
     (`frontend/packages/schemaform/components/editor/attributes/CountryAttributes.vue:15`,
     `COUNTRIES_LIST`) and is not filtered — staff can still set a default of TW/HK.
  4. **`zh-HK` is a completely separate code path** (L588-603) off a hand-maintained
     250-country map. Anything added must be duplicated there.
  5. **The hiding behaviour is untested** — `CountryNamingHelper.test.ts` only exercises
     `hotelSlug = null`.

  ### Draft Slack reply (NOT sent — needs your approval)

  > Looked into this. Answering the two questions:
  >
  > **1) Is it easily editable per customer?** No — it isn't editable at all today. The
  > dropdown is built client-side from the `i18n-iso-countries` package, and #28894 added a
  > hardcoded slug allowlist in `CountryNamingHelper.ts`, not a config. Exactly one real
  > hotel is in it (Grandover / Wyndham Greensboro). @Ani — that's why it was never applied
  > to all sites: there was no mechanism to, it was one string in a TS array.
  >
  > One correction to the 3-parter: part 1's hidden-country list **already includes all four**
  > (HK, MO, TW, RE) including Macao. What's missing is scope, not coverage — so part 1 is
  > really "build the config", not "add the missing countries".
  >
  > **2) Can/should ENT handle it?** Parts 2+3 are ENT-shaped and I'll own them — but they're
  > blocked on part 1, because there's no config to apply, and part 1 is a platform/schema
  > change rather than ENT work. Wyndham is ~6.5k properties, so a slug list is out.
  >
  > For **today**, there's a much cheaper path that skips parts 2 and 3 entirely: the check-in
  > hotel payload already carries `portfolio_identifiers` and we already have an `isWyndham()`
  > helper. Swapping the slug allowlist for a portfolio check covers every Wyndham
  > immediately — no backfill, no onboarding script change, frontend-only, ~half a day.
  > I'd propose we ship that today as an explicit stopgap and build the real per-hotel config
  > behind it.
  >
  > For the **real fix**, cheapest correct home is a field on `check_in.Configuration` — that
  > payload already reaches both check-in v1 and guest-experience v2/v3, so one backend change
  > covers both frontends, and part 2 becomes a one-column backfill. Putting it on the reg card
  > builder instead (as discussed) is more correct but meaningfully more work: the country
  > element has no options/attrs surface today, and part 2 becomes a backfill over reg-card
  > JSON for 6.5k hotels. Happy either way, just want that trade explicit before we commit.
  >
  > ⚠️ One thing worth knowing regardless: **the existing mechanism is silently inert on v2/v3
  > check-in.** `SchemaFormStep.vue` doesn't pass `hotel-slug` into `SchemaForm`, so the filter
  > no-ops there. If Grandover is on v2/v3, #28894 isn't actually working today. Also worth
  > noting the hiding is cosmetic — submit-side validation still accepts `TW`/`HK`, so a
  > PMS-prefilled value goes through either way.

  ### Suggested next steps for you

  - Approve/edit the Slack reply above and I'll post it (I have not sent anything).
  - Decide Option A vs B, or A-then-B. If A-then-B, someone should own the follow-up ticket
    so the stopgap doesn't become permanent (it did last time).
  - Confirm whether Grandover is on v2/v3 check-in — that determines whether #28894 is
    currently working at all, and it changes the urgency framing.
  - Connor offered to create a separate ENT ticket with Marta. Worth saying yes for parts
    2+3, but only after part 1's shape is decided, since it determines what the backfill is.
project: null
source_id: https://linear.app/canary-technologies/issue/AD-5687/reg-remove-chinese-territories-from-country-dropdown
tags:
- morning-gtd
- linear
time_minutes: 20
title: 'Answer Connor on AD-5687: can ENT own the Wyndham Chinese-territories country-list
  fix?'
updated: 2026-08-03 10:27:10.000000
waiting_on: null
waiting_since: null
working_on: false
---

Connor @-mentioned me directly at 03:01 today: 1) is the country list easily editable per customer, 2) can/should ENT handle it. Thread already converged on "config on the reg card builder" (Vibhor), with parts 2+3 (apply config to all existing Wyndhams + update onboarding scripts) landing on Enterprise. Prior one-off was PR #28894. Wyndham wants it fixed TODAY.
https://linear.app/canary-technologies/issue/AD-5687/reg-remove-chinese-territories-from-country-dropdown
https://canarytechnologies.slack.com/archives/C04STT7UPRQ/p1785715264112599