---
area: null
contexts:
- react
created: 2026-07-28 11:13:53.989211
defer_until: null
due: 2026-07-28
energy: low
id: 2026-07-28T1113-answer-mat-as-in-eng-general-is-hotel-country-code
order: null
output: |
  ## Agent run 2026-07-28T13:10:00+03:00

  Researched both Slack threads and the codebase; drafted a reply for #eng-general
  (below) — NOT posted, awaiting your approval.

  ### State of the discussion
  - #eng-general thread (https://canarytechnologies.slack.com/archives/C019TQLQDJP/p1785180037712559):
    Jason LeMoine said `country` is unreliable and `country_code` "not 100%";
    Agustin pointed Matías at `backend/shared/shared/geo/country/country_group.py`
    (https://github.com/canary-technologies-corp/canary/blob/master/backend/shared/shared/geo/country/country_group.py#L17)
    and Matías said "that's probably what we want".
  - Parallel #epd-emea-gdpr thread (https://canarytechnologies.slack.com/archives/C0B3EUYPRL4/p1785181236511559):
    Martijn Dekker clarified the real driver is the **EU AI Act** (AI-disclosure
    signature on chat), not GDPR; confirmed same country set (EU) and that the
    `CountryGroup.EUROPEAN_UNION` list is accurate. So the *legal* question is
    settled; the open bit in #eng-general is the *data-quality* question —
    "is country_code generally accurate?" — which nobody answered.

  ### Codebase facts (verified)
  - `Hotel.country_code` (backend/canary/hotels/models/hotel.py:516) is a
    CharField with `choices=Country.choices` (ISO alpha-2), `blank=True` — so
    values are always valid Country codes, but can be empty.
  - `Hotel.country` is free-text `CharField(max_length=255)`, no choices — never
    use it for logic. `shared.geo.country.get_country()` exists to parse such
    strings (alpha-2/alpha-3/label/Salesforce+OCR aliases).
  - Onboarding sets `country_code` from Salesforce for brand-onboarded hotels
    (onboarding/configuration_providers/hotel_info_provider.py:85 — falls back to
    `""` if Salesforce billing country doesn't parse; hotel_info_plan.py:57 applies it).
  - Membership check: `COUNTRY_GROUP_MEMBERS[CountryGroup.EUROPEAN_UNION]` in
    shared/geo/country/country_group.py (matches the official EU-27 list).
  - Precedent: onboarding/management/commands/onetime_wyndham_disable_id_capture_gdpr.py
    gated by `country_code__in=[...]` with a hardcoded GDPR country list — the
    country_group approach is cleaner.
  - Nuance worth flagging: GDPR proper covers EEA (NO/IS/LI) + UK-GDPR, which
    `EUROPEAN_UNION` excludes; for the AI Act (Matías's actual use case) EU-only
    is correct per Martijn.
  - Could NOT quantify blank-country_code coverage in prod: canary-snowflake
    sf_query hung on stale SSO (browser login needed) and was aborted. If you
    want the number first: `SELECT count(*), count_if(country_code = '') FROM
    <hotels_hotel> WHERE is_active` via sf_query after `sf-login us`.

  ### Draft reply for the #eng-general thread (needs your approval to post)
  > Late addition on the "is it generally accurate?" part, since that didn't get
  > answered: `hotel.country` is free text (no choices, straight from
  > Salesforce/manual entry) — don't use it for logic; if you ever have to parse
  > it, `shared.geo.country.get_country()` handles codes/names/aliases.
  > `hotel.country_code` is the right field: it's constrained to the `Country`
  > enum and onboarding populates it from Salesforce billing country for
  > brand-onboarded hotels, so when it's set it's trustworthy. The gap is that
  > it's `blank=True`, so some older/manually-created hotels have it empty —
  > worth deciding whether blank fails open or closed for the disclosure (I'd
  > show the signature when blank + hotel-level config to override, which
  > matches what you proposed). For the check itself,
  > `COUNTRY_GROUP_MEMBERS[CountryGroup.EUROPEAN_UNION]` from
  > `shared/geo/country/country_group.py` is exactly right per Martijn in
  > #epd-emea-gdpr (AI Act = EU list). Only if this ever extends to GDPR proper:
  > that group excludes EEA (NO/IS/LI) and UK, which GDPR/UK-GDPR cover.
  > There's precedent for this gating in
  > `onetime_wyndham_disable_id_capture_gdpr.py` (country_code__in filter on
  > Wyndham ID capture).

  Next step: say "post it" (optionally after edits) and I'll reply in the
  #eng-general thread; or post it yourself.

  ## Agent run 2026-07-28T13:35:00+03:00

  Snowflake SSO now working — ran the coverage queries (read-only,
  analytics.analytics.hotels_hotel_clean deduped per id, US + EU regions).
  **country_code is well-populated; the draft below supersedes the earlier
  one.** (Item was archived by user mid-run; results recorded here for the
  record.)

  ### Prod numbers (active, non-demo hotels)
  - US region: 20,120 hotels, 349 blank country_code (1.7%). Live-only:
    16,231 hotels, 44 blank (0.27%).
  - EU region: 834 hotels, 20 blank (2.4%). Live-only: 484 hotels, 4 blank (0.8%).
  - Hotels an EU-27 country_code gate would catch: 189 (US region) + 421
    (EU region) ≈ 610 total. Top: IT 152, ES 117, FR 72, DE 53.
  - Couldn't cross-check blanks against free-text `country` — that column is
    PII-masked in Snowflake.

  ### Final draft reply for #eng-general (needs approval to post)
  > Late addition on the "is it generally accurate?" part since that didn't get
  > answered with data: yes — `country_code` is reliable. It's constrained to
  > the `Country` enum (so never garbage when set) and onboarding populates it
  > from Salesforce billing country. I checked prod: of active non-demo hotels
  > it's blank for ~1.7% (US region) / ~2.4% (EU region), and for *live* hotels
  > only 0.27% / 0.8% — so gate on it confidently, just decide what blank means
  > (I'd fail safe: show the disclosure when blank, with your hotel-level
  > config as the override). Don't use `hotel.country` — free text, no choices;
  > if you ever must parse it, `shared.geo.country.get_country()` handles
  > codes/names/aliases. `COUNTRY_GROUP_MEMBERS[CountryGroup.EUROPEAN_UNION]`
  > is the right membership check per Martijn in #epd-emea-gdpr (AI Act = EU
  > list; note that group correctly excludes EEA/UK, which only matter if this
  > ever extends to GDPR proper). FWIW that gate catches ~610 hotels today.
  > Precedent for the same pattern:
  > `onetime_wyndham_disable_id_capture_gdpr.py` filters
  > `country_code__in=[...]` for Wyndham ID capture.

  ## Agent run 2026-07-28T14:25:00+03:00

  POSTED (user-approved) a shortened reply — prod numbers + method only — to
  the #eng-general thread:
  https://canarytechnologies.slack.com/archives/C019TQLQDJP/p1785242588649429?thread_ts=1785180037.712559&cid=C019TQLQDJP
  Task fully done.
project: 2026-04-16T1210-unblock-team
source_id: https://canarytechnologies.slack.com/archives/C019TQLQDJP/p1785180037712559?thread_ts=1785180037.712559&cid=C019TQLQDJP
tags:
- morning-gtd
- slack
- from-awareness
time_minutes: 5
title: 'Answer Matías in #eng-general: is hotel.country_code accurate for GDPR liability?'
updated: 2026-07-28 14:25:00.000000
waiting_on: null
waiting_since: null
working_on: false
---

Matías asks how to determine GDPR liability in code — whether hotel.country_code is generally accurate (8 replies in thread). Your standing guidance: use hotel.country_code with get_country(), not the free-text hotel.country.
https://canarytechnologies.slack.com/archives/C019TQLQDJP/p1785180037712559