---
area: null
completed_at: null
contexts: []
created: 2026-08-06 13:35:33.929205
defer_until: null
due: null
energy: low
id: 2026-08-06T1335-default-onboarding-quick-wins-tickets
order: 2
output: |
  ## Agent run 2026-08-06T17:05

  Drafted the eng design. Full doc (markdown, ready to paste into Notion):
  `/private/tmp/claude-501/-Users-garethlloyd-projects-canary/b21e068b-e734-4fd6-a878-3e5af2be3ff2/scratchpad/default-onboarding-quick-wins-design.md`
  (scratchpad — session-scoped, copy it out if you want it kept). Nothing was posted
  anywhere; no Notion page, no Linear ticket, no comment.

  ### What the design says

  Framed around the two journeys that actually run on `OnboardingType.DEFAULT`
  (`backend/canary/onboarding/models/property_configuration_processes.py:2576`, one stage,
  ten plans): J1 = new individual hotel (`creating_new_hotel=True`), J2 = adding a product
  to an existing live hotel (same stage re-run, `creating_new_hotel=False`). J2 is the
  constraint that shapes everything.

  **Two findings that change the shape of the work — neither was in the research notes:**

  1. **The base stage is not safe to re-run on a live hotel, today.** `HotelProductsPlan`
     guards correctly (`is_live_hotel` -> `only_set_true`, `plans/hotel_products_plan.py:130`),
     but `DefaultRegistrationCardProvider` overwrites an existing hotel's registration card
     schema unconditionally (`plans/registration_card_plans.py:51-58`) and force-sets
     `rollout_check_in_v2_level=STABLE`. IHG already solved this —
     `_should_modify_registration_card()` in
     `configuration_providers/ihg/registration_card_provider.py:60-81` writes only when
     `creating_new_hotel`, no card exists, or the card still matches the default layout.
     This is a prerequisite for adding *any* new plan to DEFAULT, and if J2 is a real CS
     workflow it's a live data-loss bug. Ticket #1.

  2. **Correction to the "country conditionals are architecturally free" note.**
     `DeciderAttribute.HOTEL_COUNTRY` selects a provider *class* per country
     (`property_configuration_processes.py:391-413`) — unusable for ~90 countries of table
     data. Country-varying *data* wants one provider + a dict keyed on `data.hotel_country`
     (the `ConfigureSupportedLanguagesPlan` pattern). Reserve `HOTEL_COUNTRY` for country
     -specific *logic*.

  **Also worth knowing:** DEFAULT lists `GUEST_JOURNEY_MESSAGES_*` and `TWILIO_IS_CONFIGURED`
  in its `critical_check_types` (`:2733-2742`) while running no plan that configures either.
  Every DEFAULT hotel is monitored against config the script never writes.

  **Languages (confirmed as the cheapest win, with a caveat).** The plan is already generic
  and complete — writes `supported_languages`, `default_guest_language`,
  `rollout_staff_language_selection`, `supports_guest_language_preference=True`, and ships
  three MonitoredCheckTypes free. But the two existing tables are near-disjoint and disagree:
  BW = 40 countries (Americas-heavy, has US), Wyndham = 71 (EMEA/APAC-heavy, no US), union
  ~88, with **1 default-language conflict (PUERTO_RICO: BW `es` vs WY `en`) and 12
  additional-language conflicts** (SWITZERLAND `["en"]` vs `["fr","it","en"]`, BRAZIL,
  JAMAICA, CAYMAN_ISLANDS, BARBADOS, SAINT_KITTS_AND_NEVIS, + 5 LATAM where WY adds `pt`).
  Recommendation: build the generic table as the union with those 13 resolved once by CS,
  and leave the BW/Wyndham tables untouched in v1 — zero enterprise blast radius.
  Consolidation is a follow-up, not a prerequisite.

  **Voice (small, unblocked).** `DefaultVoiceConfigProvider` hard-fails without the
  `VOICE_AI_FORWARD_CALL_TO` OnboardingValue. Implementation gotcha: providers get
  `OnboardingPlanData`, not a `Hotel`, so the fallback can't read `hotel.phone` — use
  `data.sfdc_account.get(SF_FIELD_PHONE)`, the same source `HotelInfoPlan` uses to populate
  it (`configuration_providers/hotel_info_provider.py:87`). ~15 lines. `CONFIGURE_VOICE` is
  ad-hoc on DEFAULT so the re-run hazard doesn't apply.

  ### Proposed tickets (dependency order)

  1. Guard `DefaultRegistrationCardProvider` against clobbering a live hotel's card — S, unblocked
  2. `DefaultVoiceConfigProvider` -> fall back to Salesforce phone — S, unblocked
  3. Canonical country->language table (union, 13 conflicts resolved) — S, needs CS sign-off
  4. `DefaultSupportedLanguagesProvider` + wire the plan into DEFAULT with a re-run guard — M, needs #1 and #3
  5. Design spike: default guest-journey message set for individual hotels — M, needs CS content decision
  6. Twilio on DEFAULT — its own project, explicitly *not* a quick win (US/CA A2P vs per-country regulatory bundles)

  ### Parked / not ticketable yet

  - check-in/check-out times and silent hours: `HotelInfoConfig` carries them, the default
    provider never sets them, and no Salesforce field is mapped. Blocked on whether such a
    field exists.
  - Portfolio "Set up Dashboard / Grant User Management": **no such boolean fields exist on
    `hotels.models.Portfolio`**, and `AddToPortfolioPlan` is enterprise-portfolio *membership*,
    not the CS portfolio-creation step. The user-management half looks like a role grant
    (`permissions/constants/portfolio_permission.py`). Needs a field-level confirmation of what
    CS is actually clicking before it can be designed.
  - ID/OCR/GDPR settings: belongs to TOOL-415. One structural note for that design —
    `CheckInConfigurationUpdates` (`configuration_providers/configs/registration_card.py`) is
    the existing seam and the plan-side apply loop is already generic over its fields, so
    extend that dataclass with `purge_id_on_reservation_status_change` / `id_options` /
    `require_id_card_back` / `id_consent_text_i18n` rather than building a second mechanism.

  ### Context checked

  TOOL-415 "Eng design: Automate Check In Onboarding"
  (https://linear.app/canary-technologies/issue/TOOL-415/eng-design-automate-check-in-onboarding)
  is in Triage, labelled "Blocked: Needs Product". Its project was renamed to **Automate
  Check-in V3 Onboarding**
  (https://linear.app/canary-technologies/project/automate-check-in-v3-onboarding-617b22ca4b48),
  status Product Definition, lead Stephanie Barry, team Internal Tools, blocked on check-in v3.
  It's the only issue in the project. This design is deliberately the complement to it.

  ### Open questions for you

  1. Is J2 — re-running the base stage on a live hotel to add a product — a real current CS
     workflow or theoretical? `HotelProductsPlan`'s guard implies real. If real, ticket #1 is
     a live bug, not groundwork, and should be prioritised as such.
  2. Who resolves the 13 language conflicts, and is one list enough for them?
  3. Is there a Salesforce field for check-in/check-out time?
  4. Do you want these six raised as Linear tickets, and under which project? (Not created —
     no external writes were made.)

  ## Agent run 2026-08-06T17:52

  Four implementable ticket drafts, inlined below so they survive the scratchpad. Nothing
  created in Linear — no external writes. Suggested team: Internal Tools (TOOL).

  Sizes and order: #1 (S) and #2 (S) are unblocked today. #3 (S) carries one CS decision and
  can ship with the proposed default. #4 (M) depends on #1 and #3.

  Three things that changed while drafting, versus the earlier run:

  - #2 has a real gotcha: `get_sfdc_account_fields_for_plans` fetches only NAME +
    BILLING_ADDRESS plus each *stage's* providers' `REQUIRED_SALESFORCE_FIELDS`
    (`services/onboarding.py:136-140`), and `DefaultVoiceConfigProvider` declares none. Since
    `CONFIGURE_VOICE` is its own ad-hoc stage it can't ride on the hotel-info provider's fetch —
    without adding `REQUIRED_SALESFORCE_FIELDS = [SF_FIELD_PHONE]` the fallback reads an absent
    key and silently does nothing.
  - #3 shrank: taking the **superset** for additional languages resolves 12 of the 13 conflicts
    without a meeting, leaving only `PUERTO_RICO`'s default language for CS.
  - #4 shrank: no `KNOWN_PLANS` change needed, the plan is already registered
    (`services/plan.py:87`). It's a ~15-line provider plus one `PlanFactory` entry, and the
    re-run guard is the actual work.

  ---

  Four implementable tickets. #1 and #2 are unblocked today. #3 carries one CS decision that can
  ship with a proposed default. #4 depends on #1 and #3. Team: Internal Tools (TOOL).

  Design doc these come from: `default-onboarding-quick-wins-design.md`.
  Sibling work, deliberately excluded: TOOL-415 / *Automate Check-in V3 Onboarding*.

  ---

  ## 1. Stop the onboarding script overwriting a live hotel's registration card

  **Size:** S · **Blocked on:** nothing

  ### Problem

  `DefaultRegistrationCardProvider.perform_hotel_configuration` finds the hotel's existing
  `RegistrationCard` and overwrites `schema` with the stock template unconditionally, moving the old
  version to `legacy_schema` (`backend/canary/onboarding/plans/registration_card_plans.py:51-58`). It
  also force-sets `rollout_check_in_v2_level = STABLE` on every run.

  `AddRegistrationCardPlan` sits in the `BASE_CONFIGURATION_NEW` stage of `OnboardingType.DEFAULT`
  (`models/property_configuration_processes.py:2613-2616`), which is the same stage CS re-runs to add
  a product to an existing hotel. `HotelProductsPlan` in that stage explicitly handles this case —
  it computes `is_live_hotel` and only sets flags to true (`plans/hotel_products_plan.py:130,160`) —
  so re-running against a live hotel is an expected flow. The registration card plan has no
  equivalent guard, so a hotel that CS has customised gets reset to the stock card.

  ### What to do

  Port IHG's guard to the default provider. `IHGRegistrationCardProvider._should_modify_registration_card`
  (`configuration_providers/ihg/registration_card_provider.py:60-81`) already encodes the right rule:
  write when `data.creating_new_hotel` is true, or no card exists, or the existing card's layout still
  matches the default.

  - Move `_extract_layout_structure` and `_schema_layout_matches_default`
    (`ihg/registration_card_provider.py:26-49`) somewhere shared — they compare element `id`/`type`
    only and ignore i18n content, so nothing about them is IHG-specific. IHG keeps calling the shared
    version.
  - `DefaultRegistrationCardProvider` needs to hold onto `data` (it currently discards it) so it can
    read `creating_new_hotel`.
  - Leave the create path unchanged.
  - Decide whether `rollout_check_in_v2_level = STABLE` should also be gated. It comes from
    `CheckInConfigurationUpdates` on the config, applied by the plan's generic loop
    (`registration_card_plans.py:70-83`), so it's a separate write from the schema overwrite.
    Suggest: leave it unconditional (it's a monotonic rollout flag), but say so explicitly in the PR.

  ### Acceptance criteria

  - Re-running `BASE_CONFIGURATION_NEW` on a hotel whose card layout has been customised leaves
    `schema` and `legacy_schema` untouched.
  - Re-running against a hotel whose card still matches the default template still refreshes it.
  - A new hotel (`creating_new_hotel=True`) is unaffected.
  - IHG behaviour is unchanged.
  - Tests in `onboarding/tests/plans/test_registration_card_plans.py` (six existing cases construct
    `DefaultRegistrationCardProvider` directly, so they'll need `creating_new_hotel` set on the stub).

  ### Open question

  Do we want to know how often this has already fired? `legacy_schema` is populated on every
  overwrite, so a count of DEFAULT-path hotels with a non-null `legacy_schema` whose current schema
  equals the stock template would size the damage. Not required to ship the fix — worth knowing
  whether it needs a follow-up repair.

  ---

  ## 2. Default the voice forwarding number to the hotel's Salesforce phone

  **Size:** S · **Blocked on:** nothing

  ### Problem

  `DefaultVoiceConfigProvider` raises `ERROR_MISSING_FORWARD_CALL_TO` when the
  `VOICE_AI_FORWARD_CALL_TO` OnboardingValue is absent
  (`configuration_providers/default_voice_config_provider.py:20-26`), so the `CONFIGURE_VOICE` stage
  cannot run until someone enters it by hand. The CustOps Voice runbook
  (https://app.notion.com/p/33481468615180f59f01f6a76f99f540) says the forwarding number defaults to
  the hotel's own phone as a placeholder — so the manual step reproduces data we already hold.

  ### What to do

  Fall back to the Salesforce account phone when the OnboardingValue is absent; raise the existing
  expected error only when both are missing.

  Two things to get right:

  1. **Config providers receive `OnboardingPlanData`, not a `Hotel`** — there is no `hotel.phone` to
     read at construction time. Use `data.sfdc_account.get(SF_FIELD_PHONE)` (from
     `canary.salesforce_ids`), which is the same source `HotelInfoPlan` uses to populate
     `hotel.phone` in the first place (`configuration_providers/hotel_info_provider.py:87`).
  2. **The field is not fetched by default.** `get_sfdc_account_fields_for_plans` always fetches only
     `SF_FIELD_NAME` and `SF_FIELD_BILLING_ADDRESS`, then unions each stage's providers'
     `REQUIRED_SALESFORCE_FIELDS` (`services/onboarding.py:136-140`). `DefaultVoiceConfigProvider`
     declares none today, and `CONFIGURE_VOICE` is a separate ad-hoc stage from
     `BASE_CONFIGURATION_NEW`, so it cannot rely on the hotel-info provider having pulled the phone.
     Add `REQUIRED_SALESFORCE_FIELDS = [SF_FIELD_PHONE]`.

  No re-run hazard here — `CONFIGURE_VOICE` is ad-hoc on DEFAULT, not part of the base stage.

  ### Acceptance criteria

  - With the OnboardingValue set, behaviour is unchanged (it wins).
  - With it absent and a Salesforce phone present, `forward_call_to` is the Salesforce phone and the
    stage runs.
  - With both absent, `ERROR_MISSING_FORWARD_CALL_TO` still raises.
  - The Salesforce phone field is actually requested for the `CONFIGURE_VOICE` stage.
  - Tests in `onboarding/tests/plans/test_configure_voice_plan.py`.

  ### Open question

  Should the fallback be recorded so CS can see the number was inferred rather than chosen? The
  plan's result dict is the natural place. Suggest yes, as a `forward_call_to_source` key — cheap,
  and it makes the placeholder visible in the run output rather than silently plausible.

  ---

  ## 3. Canonical country → language table for non-enterprise hotels

  **Size:** S · **Blocked on:** one CS decision (can ship with the proposed defaults below)

  ### Problem

  `ConfigureSupportedLanguagesPlan` is generic and complete, but the only country→language tables in
  the tree are brand-owned: Best Western's
  (`configuration_providers/best_western/language_definitions.py`) and Wyndham's
  (`configuration_providers/wyndham/wyndham_supported_languages_provider.py`). There is no table a
  non-enterprise hotel can use. This ticket produces the data; ticket #4 wires it up.

  ### What to do

  Add a brand-neutral module holding `DEFAULT_GUEST_COMMUNICATION_LANGUAGE_BY_COUNTRY` and
  `ADDITIONAL_LANGUAGE_BY_COUNTRY`, built as the **union** of the two existing tables.

  **Do not modify the BW or Wyndham tables.** They keep their own copies and their behaviour is
  untouched — this ticket has zero enterprise blast radius. Consolidating all three into one source
  with brand overlays is a worthwhile follow-up, not a prerequisite.

  Coverage today: BW has 40 countries (Americas-heavy, includes `UNITED_STATES`), Wyndham has 71
  (EMEA/APAC-heavy, no `UNITED_STATES`). Union is ~88.

  ### The 13 conflicts

  Default language — 1:

  | Country | BW | Wyndham | Proposed |
  |---|---|---|---|
  | `PUERTO_RICO` | `es` | `en` | **needs CS** |

  Additional languages — 12:

  | Country | BW | Wyndham | Proposed |
  |---|---|---|---|
  | `SWITZERLAND` | `["en"]` | `["fr","it","en"]` | Wyndham (all national languages) |
  | `BRAZIL` | `["en"]` | `["en","es"]` | Wyndham |
  | `JAMAICA` | `[]` | `["fr","es"]` | Wyndham |
  | `CAYMAN_ISLANDS` | `[]` | `["es"]` | Wyndham |
  | `BARBADOS` | `[]` | `["es"]` | Wyndham |
  | `SAINT_KITTS_AND_NEVIS` | `[]` | `["es"]` | Wyndham |
  | `ARGENTINA` | `["en"]` | `["en","pt"]` | Wyndham |
  | `CHILE` | `["en"]` | `["en","pt"]` | Wyndham |
  | `COSTA_RICA` | `["en"]` | `["en","pt"]` | Wyndham |
  | `PARAGUAY` | `["en"]` | `["en","pt"]` | Wyndham |
  | `DOMINICAN_REPUBLIC` | `["en"]` | `["en","pt"]` | Wyndham |
  | `PUERTO_RICO` | `["en"]` | `["es"]` | follows the default decision above |

  Proposed rule for the additional-languages column: **take the superset** — an extra supported
  language is low-risk (guests opt in; `default_guest_language` is what drives outbound), so the
  union is the safe default and needs no meeting. That collapses the CS decision to `PUERTO_RICO`'s
  *default* language alone.

  Cite the Notion source in a module comment, as the Wyndham table does
  (https://www.notion.so/canarytechnologies/Supported-Languages-1d781468615180d29b17c998a0f5c47c).

  ### Acceptance criteria

  - One module exporting both dicts, typed as the existing ones are
    (`dict[Country, LANGUAGE_CODE]` / `dict[Country, list[LANGUAGE_CODE]]`).
  - Every country present in either source table is present in the union.
  - BW and Wyndham providers and tables are untouched.
  - A test asserting the union covers both source tables, so a future addition to either doesn't
    silently diverge.

  ### Open question

  **`PUERTO_RICO` default: `es` or `en`?** Ship `en` (Wyndham's, and the larger table) if no answer
  lands — it's a single entry, trivially changed later.

  ---

  ## 4. Configure supported languages on the DEFAULT onboarding path

  **Size:** M · **Blocked on:** #1 (guard convention) and #3 (the table)

  ### Problem

  `ConfigureSupportedLanguagesPlan` runs for Best Western and Wyndham but is not in the DEFAULT
  stage, so an individual hotel gets none of it. Every per-country CS checklist prescribes exactly
  what this plan writes, by hand, per hotel:

  - `supported_languages` and `default_guest_language` per country
  - `supports_guest_language_preference = Yes` — unconditional in every checklist; model default is
    `False` (`hotels/models/hotel.py:1211`)
  - `rollout_staff_language_selection`

  The plan also ships three monitored checks (`SUPPORTED_LANGUAGES_CONFIGURED`,
  `DEFAULT_GUEST_LANGUAGE_CONFIGURED`, `STAFF_LANGUAGE_SELECTION_CONFIGURED`) that come along for
  free once it's wired.

  ### What to do

  - Add `DefaultSupportedLanguagesProvider` — a near-copy of `BestWesternSupportedLanguagesProvider`
    (~15 lines) reading the table from #3.
  - Add a `PlanFactory(plan=ConfigureSupportedLanguagesPlan, config_provider=DefaultSupportedLanguagesProvider)`
    to `OnboardingType.DEFAULT`'s `BASE_CONFIGURATION_NEW` stage
    (`models/property_configuration_processes.py:2582-2720`).
  - No `KNOWN_PLANS` change needed — `ConfigureSupportedLanguagesPlan` is already registered
    (`services/plan.py:87`).

  **Re-run guard (this is the part to get right).** The plan currently writes
  `hotel.supported_languages` outright (`plans/configure_supported_languages_plan.py:73-84`). On a
  live hotel that discards languages CS added by hand. Apply the convention from #1:

  - Write the language *lists* only when `data.creating_new_hotel` is true, or the hotel is still at
    the model default — `supported_languages` defaults to `SUPPORTED_LANGUAGE_CODES["EN"]`
    (`hotels/models/hotel.py:1119-1125`), so the check is "empty, or exactly `{en}`".
  - `supports_guest_language_preference = True` can stay unconditional — it's prescribed everywhere
    and is monotonic.

  Where the guard lives is a judgement call: the plan is shared with BW/Wyndham, so putting it in
  the plan changes enterprise behaviour too. Prefer expressing it through the config/provider so
  DEFAULT opts in and the enterprise paths keep today's behaviour, unless the team wants it
  everywhere — worth a line in the PR description either way.

  Unknown countries already degrade sanely: the plan logs
  `configure_supported_languages.country_not_configured` and falls back to `["en"]` / `en` with
  `rollout_staff_language_selection=False`.

  ### Acceptance criteria

  - A new DEFAULT hotel in a country in the table gets the right `supported_languages`,
    `default_guest_language`, `rollout_staff_language_selection`, and
    `supports_guest_language_preference=True`.
  - A new DEFAULT hotel in a country *not* in the table gets `["en"]`/`en`, no crash, and the warning
    log fires.
  - Re-running the stage on a live hotel with hand-tuned languages does not change them.
  - BW and Wyndham onboarding behaviour is byte-for-byte unchanged.
  - Tests extend `onboarding/tests/plans/test_configure_supported_languages_plan.py`.

  ### Open question

  Should `rollout_staff_language_selection` be gated the same way as the language lists? It's a
  boolean rollout flag, so the monotonic argument applies, but the plan currently sets it to `False`
  for unrecognised countries — which on a re-run would turn it off for a hotel where CS had enabled
  it. Suggest: only ever set it to `True`, never back to `False`, on the DEFAULT path.

  ---

  ## Not in this batch

  - **Guest journey messages on DEFAULT** — the plan and seven enterprise providers exist, and
    DEFAULT already monitors `GUEST_JOURNEY_MESSAGES_*` as critical without configuring them, but
    what the default message set *is* for an individual hotel is CS content, not an eng decision.
    Needs a spike with CS first.
  - **Twilio on DEFAULT** — DEFAULT has no `ConfigureTwilioPlan` at all while listing
    `TWILIO_IS_CONFIGURED` as a critical check. The A2P form-fill is deterministic boilerplate, but
    the US/CA-versus-international split and `ConfigureTwilioPlan`'s registration branching make this
    its own project.
  - **Check-in / ID / GDPR settings** — TOOL-415. One note for that design: extend
    `CheckInConfigurationUpdates` (`configuration_providers/configs/registration_card.py`) rather
    than building a second mechanism; the plan-side apply loop is already generic over its fields.
  - **check-in/check-out times, silent hours** — `HotelInfoConfig` carries them and `HotelInfoPlan`
    writes them, but no Salesforce field is mapped. Blocked on whether one exists.
  - **Portfolio defaults** — no matching boolean fields exist on `hotels.models.Portfolio`; needs a
    field-level confirmation of what CS actually clicks.
project: 2026-04-10T0840-ticket
source_id: null
tags: []
time_minutes: 5
title: Draft eng design for quick win default onboarding improvements that would impact
  customer success creating individual hotels (non-enterprise) and adding products
  to existing hotels via onboarding scripts
updated: 2026-08-14 07:01:42.086288
waiting_on: null
waiting_since: null
working_on: false
---

Method: read the two example docs from James's Slack DMs, then fanned out 4 research agents — (1) core CS config docs, (2) comms-channel docs, (3) country/language deep-dive incl. Drive, (4) codebase map of what the DEFAULT onboarding script already stamps.

Job 1 — The doc store
The general store is "CustOps Process Documentation" (https://app.notion.com/p/13f8146861518045bf68e89e252adf6e), under Customer Operations Homebase → it's the CSA runbook index (~25 docs): Account Configuration & Onboarding App, Hotel Configuration/Setup, Branding (+ Enterprise Branding Rulebook DB), Form Builder Guide, Webchat, Voice, Twilio, WhatsApp, LINE/UIB, CSA Integrations, User Access, Demo Hotel, etc. James's two examples both hang off this tree.

A second, newer store matters even more for scripting: "Check in setup guide by country" (https://app.notion.com/p/32e81468615180dcb772eed63ff1fab5) — per-country checklists: Spain no-OCR (https://app.notion.com/p/2ce8146861518007a517d12f45e11e54), Greece no-OCR (https://app.notion.com/p/32e8146861518086a492c720528c827f), Greece OCR (https://app.notion.com/p/3498146861518097a0e7d74f55ccc7bc), UK OCR (https://app.notion.com/p/3b381468615180a6af53eddb4c9e9bf4), Australia no-OCR (https://app.notion.com/p/3b381468615180d68fd3fea10343f337). Also: EMEA reg-card meeting notes (https://app.notion.com/p/36681468615180928025c8db62f6e06a), "Registration card configuration" (https://app.notion.com/p/1d78146861518095830ad6923bda9163), and Isaac's Drive SOPs (Italy: https://docs.google.com/document/d/1xWBfa_Lu0nTPcFQXYCt146Y1QWsd0uQNQthZ-SgZKHo — note the referenced folder 1KMaVCOohiHPaicvUbuMmU6QIREYL2jSZ wasn't accessible to my Drive connector).

Job 2 — Country & language conditionals
What CS sets conditional on country today (all manual on the DEFAULT path):

Registration card fields — each country checklist prescribes exact fields+tags (Spain: second last name, ID support number for DNI, gender, DOB, nationality, ID details, additional-guest counts; UK: much lighter, Next Destination for non-UK guests; Italy per Drive SOP). Already scoped for automation by the "Automate Check-in Onboarding" project (https://app.notion.com/p/39e8146861518112abedc03bf47b0dc8, Linear: https://linear.app/canary-technologies/project/automate-registration-card-setup-by-country-in-the-onboarding-script-617b22ca4b48).
ID / OCR / accompanying-guest Django settings — the checklists also prescribe id_step_with_ocr (Optional vs Optional-with-OCR), id_options (Spain: 4 types; UK: passport only), require_id_card_back, purge_id_on_reservation_status_change=Yes (GDPR), per-country id_consent_text_i18n, and full accompanying-guest field requiredness matrices (Spain requires ~15 fields; UK 4). The check-in project covers the card + ID step; the accompanying-guest matrix is in-scope content it should also consume.
Languages — checklists set Language Settings per country (Spain: en+es; UK: en) and supports_guest_language_preference=Yes always. Crucially, ConfigureSupportedLanguagesPlan already exists in code (backend/canary/onboarding/plans/configure_supported_languages_plan.py) and does exactly this from country→language tables — but it only runs for Best Western and Wyndham; it is NOT in the DEFAULT stage. Standardizing = write a generic country→language table and add the plan to DEFAULT. Probably the single cheapest country-conditional win.
Twilio/SMS — US/CA: A2P registration (W9/CBN) with automated interim provisioning + auto-migration; everywhere else: per-country regulatory bundles, number type must match country. Channel selection is itself country-driven: SMS US/CA, WhatsApp international, LINE/WeChat for JP/CN-adjacent markets.
Region (US/EU/APAC hosting) drives webhook prefixes (LINE), test URLs, admin URLs. The script already does one country branch on DEFAULT: has_fallback_to_sms for EU/APAC (hotel_products_plan.py:81-83).
Infra note: DeciderAttribute.HOTEL_COUNTRY already exists and hotel_country is populated for every onboarding type — country-conditional providers are architecturally free.
Job 3 — Low-hanging "always set this" candidates
Add ConfigureSupportedLanguagesPlan to DEFAULT (see above). Sets supported_languages, default_guest_language, supports_guest_language_preference, staff language rollout.
supports_guest_language_preference = Yes — unconditional in every country checklist; currently untouched by DEFAULT.
GDPR ID purge (purge_id_on_reservation_status_change=Yes) — prescribed in both Spain and UK templates; a candidate default for EU/UK countries (trade-off documented: no ID on chargeback reports).
Voice defaults — CS docs say: multilingual OFF unless requested, and forwarding number defaults to the hotel's own phone as placeholder. The VOICE_AI_FORWARD_CALL_TO OnboardingValue is hard-required by DefaultVoiceConfigProvider; defaulting it to hotel phone would remove a manual step (CustOps Voice doc: https://app.notion.com/p/33481468615180f59f01f6a76f99f540).
Twilio A2P form fill — every field CS enters is deterministic boilerplate: use case always "Low Volume Mixed", Messaging Service always "Canary Messages", standard campaign description/sample messages, fallback contact Canary Support. The "Configure Twilio Interim Messaging" admin button already automates provisioning; the remaining form-fill is scriptable. Note DEFAULT stage has NO ConfigureTwilioPlan at all (Wyndham/BW do).
Portfolio creation defaults — "Set up Dashboard=True", "Grant User Management=True" always.
Webchat defaults — welcome/error message templates, default booking-link params string (adults={adults}&children={children}&checkin_date=...) are documented constants.
Branding presets pipeline exists — "Canary Hotel Branding Repository" DB (under https://app.notion.com/p/161814686151805780e2f8055ca4851f) has an "Added to Canary Onboarding App" checkbox per brand — the automation frontier is literally tracked in Notion; keep moving rows in.
Check-in/check-out times: HotelInfoPlan supports them but the default provider never sets them.