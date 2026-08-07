---
area: null
completed_at: null
contexts: []
created: 2026-08-06 13:35:33.929205
defer_until: null
due: 2026-08-06
energy: low
id: 2026-08-06T1335-default-onboarding-quick-wins-tickets
order: 2
output: "## Agent run 2026-08-06T17:05\n\nDrafted the eng design. Full doc (markdown,
  ready to paste into Notion):\n`/private/tmp/claude-501/-Users-garethlloyd-projects-canary/b21e068b-e734-4fd6-a878-3e5af2be3ff2/scratchpad/default-onboarding-quick-wins-design.md`\n(scratchpad
  — session-scoped, copy it out if you want it kept). Nothing was posted\nanywhere;
  no Notion page, no Linear ticket, no comment.\n\n### What the design says\n\nFramed
  around the two journeys that actually run on `OnboardingType.DEFAULT`\n(`backend/canary/onboarding/models/property_configuration_processes.py:2576`,
  one stage,\nten plans): J1 = new individual hotel (`creating_new_hotel=True`), J2
  = adding a product\nto an existing live hotel (same stage re-run, `creating_new_hotel=False`).
  J2 is the\nconstraint that shapes everything.\n\n**Two findings that change the
  shape of the work — neither was in the research notes:**\n\n1. **The base stage
  is not safe to re-run on a live hotel, today.** `HotelProductsPlan`\n   guards correctly
  (`is_live_hotel` -> `only_set_true`, `plans/hotel_products_plan.py:130`),\n   but
  `DefaultRegistrationCardProvider` overwrites an existing hotel's registration card\n
  \  schema unconditionally (`plans/registration_card_plans.py:51-58`) and force-sets\n
  \  `rollout_check_in_v2_level=STABLE`. IHG already solved this —\n   `_should_modify_registration_card()`
  in\n   `configuration_providers/ihg/registration_card_provider.py:60-81` writes
  only when\n   `creating_new_hotel`, no card exists, or the card still matches the
  default layout.\n   This is a prerequisite for adding *any* new plan to DEFAULT,
  and if J2 is a real CS\n   workflow it's a live data-loss bug. Ticket #1.\n\n2.
  **Correction to the \"country conditionals are architecturally free\" note.**\n
  \  `DeciderAttribute.HOTEL_COUNTRY` selects a provider *class* per country\n   (`property_configuration_processes.py:391-413`)
  — unusable for ~90 countries of table\n   data. Country-varying *data* wants one
  provider + a dict keyed on `data.hotel_country`\n   (the `ConfigureSupportedLanguagesPlan`
  pattern). Reserve `HOTEL_COUNTRY` for country\n   -specific *logic*.\n\n**Also worth
  knowing:** DEFAULT lists `GUEST_JOURNEY_MESSAGES_*` and `TWILIO_IS_CONFIGURED`\nin
  its `critical_check_types` (`:2733-2742`) while running no plan that configures
  either.\nEvery DEFAULT hotel is monitored against config the script never writes.\n\n**Languages
  (confirmed as the cheapest win, with a caveat).** The plan is already generic\nand
  complete — writes `supported_languages`, `default_guest_language`,\n`rollout_staff_language_selection`,
  `supports_guest_language_preference=True`, and ships\nthree MonitoredCheckTypes
  free. But the two existing tables are near-disjoint and disagree:\nBW = 40 countries
  (Americas-heavy, has US), Wyndham = 71 (EMEA/APAC-heavy, no US), union\n~88, with
  **1 default-language conflict (PUERTO_RICO: BW `es` vs WY `en`) and 12\nadditional-language
  conflicts** (SWITZERLAND `[\"en\"]` vs `[\"fr\",\"it\",\"en\"]`, BRAZIL,\nJAMAICA,
  CAYMAN_ISLANDS, BARBADOS, SAINT_KITTS_AND_NEVIS, + 5 LATAM where WY adds `pt`).\nRecommendation:
  build the generic table as the union with those 13 resolved once by CS,\nand leave
  the BW/Wyndham tables untouched in v1 — zero enterprise blast radius.\nConsolidation
  is a follow-up, not a prerequisite.\n\n**Voice (small, unblocked).** `DefaultVoiceConfigProvider`
  hard-fails without the\n`VOICE_AI_FORWARD_CALL_TO` OnboardingValue. Implementation
  gotcha: providers get\n`OnboardingPlanData`, not a `Hotel`, so the fallback can't
  read `hotel.phone` — use\n`data.sfdc_account.get(SF_FIELD_PHONE)`, the same source
  `HotelInfoPlan` uses to populate\nit (`configuration_providers/hotel_info_provider.py:87`).
  ~15 lines. `CONFIGURE_VOICE` is\nad-hoc on DEFAULT so the re-run hazard doesn't
  apply.\n\n### Proposed tickets (dependency order)\n\n1. Guard `DefaultRegistrationCardProvider`
  against clobbering a live hotel's card — S, unblocked\n2. `DefaultVoiceConfigProvider`
  -> fall back to Salesforce phone — S, unblocked\n3. Canonical country->language
  table (union, 13 conflicts resolved) — S, needs CS sign-off\n4. `DefaultSupportedLanguagesProvider`
  + wire the plan into DEFAULT with a re-run guard — M, needs #1 and #3\n5. Design
  spike: default guest-journey message set for individual hotels — M, needs CS content
  decision\n6. Twilio on DEFAULT — its own project, explicitly *not* a quick win (US/CA
  A2P vs per-country regulatory bundles)\n\n### Parked / not ticketable yet\n\n- check-in/check-out
  times and silent hours: `HotelInfoConfig` carries them, the default\n  provider
  never sets them, and no Salesforce field is mapped. Blocked on whether such a\n
  \ field exists.\n- Portfolio \"Set up Dashboard / Grant User Management\": **no
  such boolean fields exist on\n  `hotels.models.Portfolio`**, and `AddToPortfolioPlan`
  is enterprise-portfolio *membership*,\n  not the CS portfolio-creation step. The
  user-management half looks like a role grant\n  (`permissions/constants/portfolio_permission.py`).
  Needs a field-level confirmation of what\n  CS is actually clicking before it can
  be designed.\n- ID/OCR/GDPR settings: belongs to TOOL-415. One structural note for
  that design —\n  `CheckInConfigurationUpdates` (`configuration_providers/configs/registration_card.py`)
  is\n  the existing seam and the plan-side apply loop is already generic over its
  fields, so\n  extend that dataclass with `purge_id_on_reservation_status_change`
  / `id_options` /\n  `require_id_card_back` / `id_consent_text_i18n` rather than
  building a second mechanism.\n\n### Context checked\n\nTOOL-415 \"Eng design: Automate
  Check In Onboarding\"\n(https://linear.app/canary-technologies/issue/TOOL-415/eng-design-automate-check-in-onboarding)\nis
  in Triage, labelled \"Blocked: Needs Product\". Its project was renamed to **Automate\nCheck-in
  V3 Onboarding**\n(https://linear.app/canary-technologies/project/automate-check-in-v3-onboarding-617b22ca4b48),\nstatus
  Product Definition, lead Stephanie Barry, team Internal Tools, blocked on check-in
  v3.\nIt's the only issue in the project. This design is deliberately the complement
  to it.\n\n### Open questions for you\n\n1. Is J2 — re-running the base stage on
  a live hotel to add a product — a real current CS\n   workflow or theoretical? `HotelProductsPlan`'s
  guard implies real. If real, ticket #1 is\n   a live bug, not groundwork, and should
  be prioritised as such.\n2. Who resolves the 13 language conflicts, and is one list
  enough for them?\n3. Is there a Salesforce field for check-in/check-out time?\n4.
  Do you want these six raised as Linear tickets, and under which project? (Not created
  —\n   no external writes were made.)\n\n## Agent run 2026-08-06T17:52\n\nFour implementable
  ticket drafts, inlined below so they survive the scratchpad. Nothing\ncreated in
  Linear — no external writes. Suggested team: Internal Tools (TOOL).\n\nSizes and
  order: #1 (S) and #2 (S) are unblocked today. #3 (S) carries one CS decision and\ncan
  ship with the proposed default. #4 (M) depends on #1 and #3.\n\nThree things that
  changed while drafting, versus the earlier run:\n\n- #2 has a real gotcha: `get_sfdc_account_fields_for_plans`
  fetches only NAME +\n  BILLING_ADDRESS plus each *stage's* providers' `REQUIRED_SALESFORCE_FIELDS`\n
  \ (`services/onboarding.py:136-140`), and `DefaultVoiceConfigProvider` declares
  none. Since\n  `CONFIGURE_VOICE` is its own ad-hoc stage it can't ride on the hotel-info
  provider's fetch —\n  without adding `REQUIRED_SALESFORCE_FIELDS = [SF_FIELD_PHONE]`
  the fallback reads an absent\n  key and silently does nothing.\n- #3 shrank: taking
  the **superset** for additional languages resolves 12 of the 13 conflicts\n  without
  a meeting, leaving only `PUERTO_RICO`'s default language for CS.\n- #4 shrank: no
  `KNOWN_PLANS` change needed, the plan is already registered\n  (`services/plan.py:87`).
  It's a ~15-line provider plus one `PlanFactory` entry, and the\n  re-run guard is
  the actual work.\n\n---\n\nFour implementable tickets. #1 and #2 are unblocked today.
  #3 carries one CS decision that can\nship with a proposed default. #4 depends on
  #1 and #3. Team: Internal Tools (TOOL).\n\nDesign doc these come from: `default-onboarding-quick-wins-design.md`.\nSibling
  work, deliberately excluded: TOOL-415 / *Automate Check-in V3 Onboarding*.\n\n---\n\n##
  1. Stop the onboarding script overwriting a live hotel's registration card\n\n**Size:**
  S · **Blocked on:** nothing\n\n### Problem\n\n`DefaultRegistrationCardProvider.perform_hotel_configuration`
  finds the hotel's existing\n`RegistrationCard` and overwrites `schema` with the
  stock template unconditionally, moving the old\nversion to `legacy_schema` (`backend/canary/onboarding/plans/registration_card_plans.py:51-58`).
  It\nalso force-sets `rollout_check_in_v2_level = STABLE` on every run.\n\n`AddRegistrationCardPlan`
  sits in the `BASE_CONFIGURATION_NEW` stage of `OnboardingType.DEFAULT`\n(`models/property_configuration_processes.py:2613-2616`),
  which is the same stage CS re-runs to add\na product to an existing hotel. `HotelProductsPlan`
  in that stage explicitly handles this case —\nit computes `is_live_hotel` and only
  sets flags to true (`plans/hotel_products_plan.py:130,160`) —\nso re-running against
  a live hotel is an expected flow. The registration card plan has no\nequivalent
  guard, so a hotel that CS has customised gets reset to the stock card.\n\n### What
  to do\n\nPort IHG's guard to the default provider. `IHGRegistrationCardProvider._should_modify_registration_card`\n(`configuration_providers/ihg/registration_card_provider.py:60-81`)
  already encodes the right rule:\nwrite when `data.creating_new_hotel` is true, or
  no card exists, or the existing card's layout still\nmatches the default.\n\n- Move
  `_extract_layout_structure` and `_schema_layout_matches_default`\n  (`ihg/registration_card_provider.py:26-49`)
  somewhere shared — they compare element `id`/`type`\n  only and ignore i18n content,
  so nothing about them is IHG-specific. IHG keeps calling the shared\n  version.\n-
  `DefaultRegistrationCardProvider` needs to hold onto `data` (it currently discards
  it) so it can\n  read `creating_new_hotel`.\n- Leave the create path unchanged.\n-
  Decide whether `rollout_check_in_v2_level = STABLE` should also be gated. It comes
  from\n  `CheckInConfigurationUpdates` on the config, applied by the plan's generic
  loop\n  (`registration_card_plans.py:70-83`), so it's a separate write from the
  schema overwrite.\n  Suggest: leave it unconditional (it's a monotonic rollout flag),
  but say so explicitly in the PR.\n\n### Acceptance criteria\n\n- Re-running `BASE_CONFIGURATION_NEW`
  on a hotel whose card layout has been customised leaves\n  `schema` and `legacy_schema`
  untouched.\n- Re-running against a hotel whose card still matches the default template
  still refreshes it.\n- A new hotel (`creating_new_hotel=True`) is unaffected.\n-
  IHG behaviour is unchanged.\n- Tests in `onboarding/tests/plans/test_registration_card_plans.py`
  (six existing cases construct\n  `DefaultRegistrationCardProvider` directly, so
  they'll need `creating_new_hotel` set on the stub).\n\n### Open question\n\nDo we
  want to know how often this has already fired? `legacy_schema` is populated on every\noverwrite,
  so a count of DEFAULT-path hotels with a non-null `legacy_schema` whose current
  schema\nequals the stock template would size the damage. Not required to ship the
  fix — worth knowing\nwhether it needs a follow-up repair.\n\n---\n\n## 2. Default
  the voice forwarding number to the hotel's Salesforce phone\n\n**Size:** S · **Blocked
  on:** nothing\n\n### Problem\n\n`DefaultVoiceConfigProvider` raises `ERROR_MISSING_FORWARD_CALL_TO`
  when the\n`VOICE_AI_FORWARD_CALL_TO` OnboardingValue is absent\n(`configuration_providers/default_voice_config_provider.py:20-26`),
  so the `CONFIGURE_VOICE` stage\ncannot run until someone enters it by hand. The
  CustOps Voice runbook\n(https://app.notion.com/p/33481468615180f59f01f6a76f99f540)
  says the forwarding number defaults to\nthe hotel's own phone as a placeholder —
  so the manual step reproduces data we already hold.\n\n### What to do\n\nFall back
  to the Salesforce account phone when the OnboardingValue is absent; raise the existing\nexpected
  error only when both are missing.\n\nTwo things to get right:\n\n1. **Config providers
  receive `OnboardingPlanData`, not a `Hotel`** — there is no `hotel.phone` to\n   read
  at construction time. Use `data.sfdc_account.get(SF_FIELD_PHONE)` (from\n   `canary.salesforce_ids`),
  which is the same source `HotelInfoPlan` uses to populate\n   `hotel.phone` in the
  first place (`configuration_providers/hotel_info_provider.py:87`).\n2. **The field
  is not fetched by default.** `get_sfdc_account_fields_for_plans` always fetches
  only\n   `SF_FIELD_NAME` and `SF_FIELD_BILLING_ADDRESS`, then unions each stage's
  providers'\n   `REQUIRED_SALESFORCE_FIELDS` (`services/onboarding.py:136-140`).
  `DefaultVoiceConfigProvider`\n   declares none today, and `CONFIGURE_VOICE` is a
  separate ad-hoc stage from\n   `BASE_CONFIGURATION_NEW`, so it cannot rely on the
  hotel-info provider having pulled the phone.\n   Add `REQUIRED_SALESFORCE_FIELDS
  = [SF_FIELD_PHONE]`.\n\nNo re-run hazard here — `CONFIGURE_VOICE` is ad-hoc on DEFAULT,
  not part of the base stage.\n\n### Acceptance criteria\n\n- With the OnboardingValue
  set, behaviour is unchanged (it wins).\n- With it absent and a Salesforce phone
  present, `forward_call_to` is the Salesforce phone and the\n  stage runs.\n- With
  both absent, `ERROR_MISSING_FORWARD_CALL_TO` still raises.\n- The Salesforce phone
  field is actually requested for the `CONFIGURE_VOICE` stage.\n- Tests in `onboarding/tests/plans/test_configure_voice_plan.py`.\n\n###
  Open question\n\nShould the fallback be recorded so CS can see the number was inferred
  rather than chosen? The\nplan's result dict is the natural place. Suggest yes, as
  a `forward_call_to_source` key — cheap,\nand it makes the placeholder visible in
  the run output rather than silently plausible.\n\n---\n\n## 3. Canonical country
  → language table for non-enterprise hotels\n\n**Size:** S · **Blocked on:** one
  CS decision (can ship with the proposed defaults below)\n\n### Problem\n\n`ConfigureSupportedLanguagesPlan`
  is generic and complete, but the only country→language tables in\nthe tree are brand-owned:
  Best Western's\n(`configuration_providers/best_western/language_definitions.py`)
  and Wyndham's\n(`configuration_providers/wyndham/wyndham_supported_languages_provider.py`).
  There is no table a\nnon-enterprise hotel can use. This ticket produces the data;
  ticket #4 wires it up.\n\n### What to do\n\nAdd a brand-neutral module holding `DEFAULT_GUEST_COMMUNICATION_LANGUAGE_BY_COUNTRY`
  and\n`ADDITIONAL_LANGUAGE_BY_COUNTRY`, built as the **union** of the two existing
  tables.\n\n**Do not modify the BW or Wyndham tables.** They keep their own copies
  and their behaviour is\nuntouched — this ticket has zero enterprise blast radius.
  Consolidating all three into one source\nwith brand overlays is a worthwhile follow-up,
  not a prerequisite.\n\nCoverage today: BW has 40 countries (Americas-heavy, includes
  `UNITED_STATES`), Wyndham has 71\n(EMEA/APAC-heavy, no `UNITED_STATES`). Union is
  ~88.\n\n### The 13 conflicts\n\nDefault language — 1:\n\n| Country | BW | Wyndham
  | Proposed |\n|---|---|---|---|\n| `PUERTO_RICO` | `es` | `en` | **needs CS** |\n\nAdditional
  languages — 12:\n\n| Country | BW | Wyndham | Proposed |\n|---|---|---|---|\n| `SWITZERLAND`
  | `[\"en\"]` | `[\"fr\",\"it\",\"en\"]` | Wyndham (all national languages) |\n|
  `BRAZIL` | `[\"en\"]` | `[\"en\",\"es\"]` | Wyndham |\n| `JAMAICA` | `[]` | `[\"fr\",\"es\"]`
  | Wyndham |\n| `CAYMAN_ISLANDS` | `[]` | `[\"es\"]` | Wyndham |\n| `BARBADOS` |
  `[]` | `[\"es\"]` | Wyndham |\n| `SAINT_KITTS_AND_NEVIS` | `[]` | `[\"es\"]` | Wyndham
  |\n| `ARGENTINA` | `[\"en\"]` | `[\"en\",\"pt\"]` | Wyndham |\n| `CHILE` | `[\"en\"]`
  | `[\"en\",\"pt\"]` | Wyndham |\n| `COSTA_RICA` | `[\"en\"]` | `[\"en\",\"pt\"]`
  | Wyndham |\n| `PARAGUAY` | `[\"en\"]` | `[\"en\",\"pt\"]` | Wyndham |\n| `DOMINICAN_REPUBLIC`
  | `[\"en\"]` | `[\"en\",\"pt\"]` | Wyndham |\n| `PUERTO_RICO` | `[\"en\"]` | `[\"es\"]`
  | follows the default decision above |\n\nProposed rule for the additional-languages
  column: **take the superset** — an extra supported\nlanguage is low-risk (guests
  opt in; `default_guest_language` is what drives outbound), so the\nunion is the
  safe default and needs no meeting. That collapses the CS decision to `PUERTO_RICO`'s\n*default*
  language alone.\n\nCite the Notion source in a module comment, as the Wyndham table
  does\n(https://www.notion.so/canarytechnologies/Supported-Languages-1d781468615180d29b17c998a0f5c47c).\n\n###
  Acceptance criteria\n\n- One module exporting both dicts, typed as the existing
  ones are\n  (`dict[Country, LANGUAGE_CODE]` / `dict[Country, list[LANGUAGE_CODE]]`).\n-
  Every country present in either source table is present in the union.\n- BW and
  Wyndham providers and tables are untouched.\n- A test asserting the union covers
  both source tables, so a future addition to either doesn't\n  silently diverge.\n\n###
  Open question\n\n**`PUERTO_RICO` default: `es` or `en`?** Ship `en` (Wyndham's,
  and the larger table) if no answer\nlands — it's a single entry, trivially changed
  later.\n\n---\n\n## 4. Configure supported languages on the DEFAULT onboarding path\n\n**Size:**
  M · **Blocked on:** #1 (guard convention) and #3 (the table)\n\n### Problem\n\n`ConfigureSupportedLanguagesPlan`
  runs for Best Western and Wyndham but is not in the DEFAULT\nstage, so an individual
  hotel gets none of it. Every per-country CS checklist prescribes exactly\nwhat this
  plan writes, by hand, per hotel:\n\n- `supported_languages` and `default_guest_language`
  per country\n- `supports_guest_language_preference = Yes` — unconditional in every
  checklist; model default is\n  `False` (`hotels/models/hotel.py:1211`)\n- `rollout_staff_language_selection`\n\nThe
  plan also ships three monitored checks (`SUPPORTED_LANGUAGES_CONFIGURED`,\n`DEFAULT_GUEST_LANGUAGE_CONFIGURED`,
  `STAFF_LANGUAGE_SELECTION_CONFIGURED`) that come along for\nfree once it's wired.\n\n###
  What to do\n\n- Add `DefaultSupportedLanguagesProvider` — a near-copy of `BestWesternSupportedLanguagesProvider`\n
  \ (~15 lines) reading the table from #3.\n- Add a `PlanFactory(plan=ConfigureSupportedLanguagesPlan,
  config_provider=DefaultSupportedLanguagesProvider)`\n  to `OnboardingType.DEFAULT`'s
  `BASE_CONFIGURATION_NEW` stage\n  (`models/property_configuration_processes.py:2582-2720`).\n-
  No `KNOWN_PLANS` change needed — `ConfigureSupportedLanguagesPlan` is already registered\n
  \ (`services/plan.py:87`).\n\n**Re-run guard (this is the part to get right).**
  The plan currently writes\n`hotel.supported_languages` outright (`plans/configure_supported_languages_plan.py:73-84`).
  On a\nlive hotel that discards languages CS added by hand. Apply the convention
  from #1:\n\n- Write the language *lists* only when `data.creating_new_hotel` is
  true, or the hotel is still at\n  the model default — `supported_languages` defaults
  to `SUPPORTED_LANGUAGE_CODES[\"EN\"]`\n  (`hotels/models/hotel.py:1119-1125`), so
  the check is \"empty, or exactly `{en}`\".\n- `supports_guest_language_preference
  = True` can stay unconditional — it's prescribed everywhere\n  and is monotonic.\n\nWhere
  the guard lives is a judgement call: the plan is shared with BW/Wyndham, so putting
  it in\nthe plan changes enterprise behaviour too. Prefer expressing it through the
  config/provider so\nDEFAULT opts in and the enterprise paths keep today's behaviour,
  unless the team wants it\neverywhere — worth a line in the PR description either
  way.\n\nUnknown countries already degrade sanely: the plan logs\n`configure_supported_languages.country_not_configured`
  and falls back to `[\"en\"]` / `en` with\n`rollout_staff_language_selection=False`.\n\n###
  Acceptance criteria\n\n- A new DEFAULT hotel in a country in the table gets the
  right `supported_languages`,\n  `default_guest_language`, `rollout_staff_language_selection`,
  and\n  `supports_guest_language_preference=True`.\n- A new DEFAULT hotel in a country
  *not* in the table gets `[\"en\"]`/`en`, no crash, and the warning\n  log fires.\n-
  Re-running the stage on a live hotel with hand-tuned languages does not change them.\n-
  BW and Wyndham onboarding behaviour is byte-for-byte unchanged.\n- Tests extend
  `onboarding/tests/plans/test_configure_supported_languages_plan.py`.\n\n### Open
  question\n\nShould `rollout_staff_language_selection` be gated the same way as the
  language lists? It's a\nboolean rollout flag, so the monotonic argument applies,
  but the plan currently sets it to `False`\nfor unrecognised countries — which on
  a re-run would turn it off for a hotel where CS had enabled\nit. Suggest: only ever
  set it to `True`, never back to `False`, on the DEFAULT path.\n\n---\n\n## Not in
  this batch\n\n- **Guest journey messages on DEFAULT** — the plan and seven enterprise
  providers exist, and\n  DEFAULT already monitors `GUEST_JOURNEY_MESSAGES_*` as critical
  without configuring them, but\n  what the default message set *is* for an individual
  hotel is CS content, not an eng decision.\n  Needs a spike with CS first.\n- **Twilio
  on DEFAULT** — DEFAULT has no `ConfigureTwilioPlan` at all while listing\n  `TWILIO_IS_CONFIGURED`
  as a critical check. The A2P form-fill is deterministic boilerplate, but\n  the
  US/CA-versus-international split and `ConfigureTwilioPlan`'s registration branching
  make this\n  its own project.\n- **Check-in / ID / GDPR settings** — TOOL-415. One
  note for that design: extend\n  `CheckInConfigurationUpdates` (`configuration_providers/configs/registration_card.py`)
  rather\n  than building a second mechanism; the plan-side apply loop is already
  generic over its fields.\n- **check-in/check-out times, silent hours** — `HotelInfoConfig`
  carries them and `HotelInfoPlan`\n  writes them, but no Salesforce field is mapped.
  Blocked on whether one exists.\n- **Portfolio defaults** — no matching boolean fields
  exist on `hotels.models.Portfolio`; needs a\n  field-level confirmation of what
  CS actually clicks.\n"
project: 2026-04-10T0840-ticket
source_id: null
tags: []
time_minutes: 5
title: Draft eng design for quick win default onboarding improvements that would impact
  customer success creating individual hotels (non-enterprise) and adding products
  to existing hotels via onboarding scripts
updated: 2026-08-06 17:52:00
waiting_on: null
waiting_since: null
working_on: true
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