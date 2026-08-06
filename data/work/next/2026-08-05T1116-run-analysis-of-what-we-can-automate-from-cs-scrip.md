---
area: null
completed_at: null
contexts: []
created: 2026-08-05 11:16:47.333000
defer_until: null
due: null
energy: low
id: 2026-08-05T1116-run-analysis-of-what-we-can-automate-from-cs-scrip
order: null
output: |
  ## Agent run 2026-08-05T14:04

  Method: read the two example docs from James's Slack DMs, then fanned out 4 research agents — (1) core CS config docs, (2) comms-channel docs, (3) country/language deep-dive incl. Drive, (4) codebase map of what the DEFAULT onboarding script already stamps.

  ### Job 1 — The doc store

  The general store is **"CustOps Process Documentation"** (https://app.notion.com/p/13f8146861518045bf68e89e252adf6e), under Customer Operations Homebase → it's the CSA runbook index (~25 docs): Account Configuration & Onboarding App, Hotel Configuration/Setup, Branding (+ Enterprise Branding Rulebook DB), Form Builder Guide, Webchat, Voice, Twilio, WhatsApp, LINE/UIB, CSA Integrations, User Access, Demo Hotel, etc. James's two examples both hang off this tree.

  A second, newer store matters even more for scripting: **"Check in setup guide by country"** (https://app.notion.com/p/32e81468615180dcb772eed63ff1fab5) — per-country checklists: Spain no-OCR (https://app.notion.com/p/2ce8146861518007a517d12f45e11e54), Greece no-OCR (https://app.notion.com/p/32e8146861518086a492c720528c827f), Greece OCR (https://app.notion.com/p/3498146861518097a0e7d74f55ccc7bc), UK OCR (https://app.notion.com/p/3b381468615180a6af53eddb4c9e9bf4), Australia no-OCR (https://app.notion.com/p/3b381468615180d68fd3fea10343f337). Also: EMEA reg-card meeting notes (https://app.notion.com/p/36681468615180928025c8db62f6e06a), "Registration card configuration" (https://app.notion.com/p/1d78146861518095830ad6923bda9163), and Isaac's Drive SOPs (Italy: https://docs.google.com/document/d/1xWBfa_Lu0nTPcFQXYCt146Y1QWsd0uQNQthZ-SgZKHo — note the referenced folder 1KMaVCOohiHPaicvUbuMmU6QIREYL2jSZ wasn't accessible to my Drive connector).

  ### Job 2 — Country & language conditionals

  What CS sets conditional on country today (all manual on the DEFAULT path):
  - **Registration card fields** — each country checklist prescribes exact fields+tags (Spain: second last name, ID support number for DNI, gender, DOB, nationality, ID details, additional-guest counts; UK: much lighter, Next Destination for non-UK guests; Italy per Drive SOP). Already scoped for automation by the "Automate Check-in Onboarding" project (https://app.notion.com/p/39e8146861518112abedc03bf47b0dc8, Linear: https://linear.app/canary-technologies/project/automate-registration-card-setup-by-country-in-the-onboarding-script-617b22ca4b48).
  - **ID / OCR / accompanying-guest Django settings** — the checklists also prescribe `id_step_with_ocr` (Optional vs Optional-with-OCR), `id_options` (Spain: 4 types; UK: passport only), `require_id_card_back`, `purge_id_on_reservation_status_change=Yes` (GDPR), per-country `id_consent_text_i18n`, and full accompanying-guest field requiredness matrices (Spain requires ~15 fields; UK 4). The check-in project covers the card + ID step; the accompanying-guest matrix is in-scope content it should also consume.
  - **Languages** — checklists set `Language Settings` per country (Spain: en+es; UK: en) and `supports_guest_language_preference=Yes` always. Crucially, **`ConfigureSupportedLanguagesPlan` already exists in code** (backend/canary/onboarding/plans/configure_supported_languages_plan.py) and does exactly this from country→language tables — but it only runs for Best Western and Wyndham; it is NOT in the DEFAULT stage. Standardizing = write a generic country→language table and add the plan to DEFAULT. Probably the single cheapest country-conditional win.
  - **Twilio/SMS** — US/CA: A2P registration (W9/CBN) with automated interim provisioning + auto-migration; everywhere else: per-country regulatory bundles, number type must match country. Channel selection is itself country-driven: SMS US/CA, WhatsApp international, LINE/WeChat for JP/CN-adjacent markets.
  - Region (US/EU/APAC hosting) drives webhook prefixes (LINE), test URLs, admin URLs. The script already does one country branch on DEFAULT: `has_fallback_to_sms` for EU/APAC (hotel_products_plan.py:81-83).
  - Infra note: `DeciderAttribute.HOTEL_COUNTRY` already exists and `hotel_country` is populated for every onboarding type — country-conditional providers are architecturally free.

  ### Job 3 — Low-hanging "always set this" candidates

  1. **Add `ConfigureSupportedLanguagesPlan` to DEFAULT** (see above). Sets supported_languages, default_guest_language, supports_guest_language_preference, staff language rollout.
  2. **`supports_guest_language_preference = Yes`** — unconditional in every country checklist; currently untouched by DEFAULT.
  3. **GDPR ID purge** (`purge_id_on_reservation_status_change=Yes`) — prescribed in both Spain and UK templates; a candidate default for EU/UK countries (trade-off documented: no ID on chargeback reports).
  4. **Voice defaults** — CS docs say: multilingual OFF unless requested, and forwarding number defaults to the hotel's own phone as placeholder. The `VOICE_AI_FORWARD_CALL_TO` OnboardingValue is hard-required by DefaultVoiceConfigProvider; defaulting it to hotel phone would remove a manual step (CustOps Voice doc: https://app.notion.com/p/33481468615180f59f01f6a76f99f540).
  5. **Twilio A2P form fill** — every field CS enters is deterministic boilerplate: use case always "Low Volume Mixed", Messaging Service always "Canary Messages", standard campaign description/sample messages, fallback contact Canary Support. The "Configure Twilio Interim Messaging" admin button already automates provisioning; the remaining form-fill is scriptable. Note DEFAULT stage has NO ConfigureTwilioPlan at all (Wyndham/BW do).
  6. **Portfolio creation defaults** — "Set up Dashboard=True", "Grant User Management=True" always.
  7. **Webchat defaults** — welcome/error message templates, default booking-link params string (`adults={adults}&children={children}&checkin_date=...`) are documented constants.
  8. **Branding presets pipeline exists** — "Canary Hotel Branding Repository" DB (under https://app.notion.com/p/161814686151805780e2f8055ca4851f) has an "Added to Canary Onboarding App" checkbox per brand — the automation frontier is literally tracked in Notion; keep moving rows in.
  9. Check-in/check-out times: HotelInfoPlan supports them but the default provider never sets them.

  ### Job 4 — The full conditional map guiding CS actions

  What the DEFAULT script stamps today: hotel info, branding (known brands), product flags from SF opportunity, auth form template, default (US-shaped, English-only) reg card, training user, departments. What CS then does manually — and the conditional that drives each:
  - **Product purchased** (SF opportunity): drives which manual runbook fires — AI Webchat → booking-link config; Voice → number+forwarding+booking agent; OCR → different card (product currently in IGNORED_PRODUCT_TYPES); Tipping → collateral. Products are NOT plumbed into OnboardingPlanData (providers fetch ad hoc) — plumbing them in is the enabler for product-conditional plans (already argued in the check-in project's REQ-010).
  - **PMS integration**: form-builder tags must map to PMS fields; booking-link param templates differ per booking engine (Synxis vs Direct-book vs WindsurferCRS, each with currency/locale/date-format quirks); CSA Integrations routes by PMS (Opera on-prem vs hosted vs HotelKey vs Mews). Precedent in code: BW `VENDOR_CONFIG` maps 6 PMS vendors → distinct reg-card templates. PMS vendor is not on OnboardingPlanData; BW reads it from OnboardingValue Kind PMS_TYPE.
  - **Payment gateway**: DEFAULT has no payment-gateway plan at all; only enterprise providers exist (Wyndham Elavon US/CA-only; IHG FreedomPay via OnboardingValue credentials).
  - **Brand / management company**: tipping collateral rules (Marriott franchised yes / Marriott-managed+IHG+Wyndham no), IHG theme palette, brand boilerplate in A2P campaigns (Wyndham, Choice), brand-level vs hotel-level webchat (Mitsis), mgmt-co-specific tipping/roles/departments providers already in DEFAULT's config.
  - **New vs Expansion business**: different Onboarding App flow; expansion (Add Products) path ignores products like OCR — known gap.
  - **Country/region**: everything in Job 2, plus enterprise precedents to generalize from (Wyndham ADDITIONAL_GUEST_STEPS_BY_COUNTRY, per-region upsells/guest-journey/go-live; IHG get_ihg_region branching).

  The big-picture gap: for a DEFAULT hotel the script's single stage omits Twilio, guest-journey messages, chat settings, upsells, payment gateway, languages, PMS, and go-live plans — that list IS the manual CS workload. The plans all exist (enterprise paths use them); the work is authoring default/country-generic providers for them, in roughly this value order: languages → Twilio/messaging registration → reg card by country (in flight) → voice defaults → guest-journey defaults.

  Full agent reports available in session transcripts; codebase refs are in backend/canary/onboarding (property_configuration_processes.py:2576-2744 for the DEFAULT stage).

  ## Agent run 2026-08-05T20:35

  Follow-on task: quick, low-risk changes we can specify today. I re-verified the key codebase claims from the prior run against the repo (configure_supported_languages_plan.py, the DEFAULT stage in property_configuration_processes.py:2576-2744, SupportedLanguagesConfig, the BW provider, hotel_products_plan.py:80-83) — all hold. Specs below are concrete enough to hand to an engineer or turn into Linear tickets.

  ### Why these are low-risk by construction

  Everything below only changes what the onboarding script stamps on NEW hotels at onboarding time — zero effect on existing hotels. Plans are idempotent, run in a transaction, and (for #1) come with built-in post-run monitoring checks. CS retains the Onboarding App to override anything after the script runs.

  ### Tier 1 — spec is complete, buildable immediately

  **1. Wire ConfigureSupportedLanguagesPlan into the DEFAULT stage** (the single cheapest country-conditional win; delivers checklist items "Language Settings" + "supports_guest_language_preference=Yes" in one PR)
  - The plan (plans/configure_supported_languages_plan.py) is already fully generic: it consumes a `SupportedLanguagesConfig` dataclass = {hotel_country, default_guest_communication_language_by_country, additional_language_by_country} and sets hotel.supported_languages, default_guest_language, supports_guest_language_preference=True, rollout_staff_language_selection. It also registers three MonitoredCheckTypes (SUPPORTED_LANGUAGES_CONFIGURED, DEFAULT_GUEST_LANGUAGE_CONFIGURED, STAFF_LANGUAGE_SELECTION_CONFIGURED) — monitoring for free.
  - Build: (a) a `DefaultSupportedLanguagesProvider` — a ~20-line copy of `BestWesternSupportedLanguagesProvider` (configuration_providers/best_western/best_western_supported_languages_provider.py) pointing at a new generic country→language table; (b) one `PlanFactory(plan=ConfigureSupportedLanguagesPlan, config_provider=DefaultSupportedLanguagesProvider)` entry appended to the DEFAULT BASE_CONFIGURATION_NEW plans list (property_configuration_processes.py:2585-2718). The plan is already in KNOWN_PLANS and the batch choices migration (0088).
  - Seed the table only with countries CS has documented: ES (en+es, default es), GR (en+el, default el), GB (en), AU (en), IT (en+it, default it) — cross-check against BW's existing `language_definitions.py` table, which already encodes the same mapping for ~dozens of countries and could simply be promoted to shared/default.
  - Failure mode for unlisted countries is exactly today's behavior (English-only) plus a structured warning log ("configure_supported_languages.country_not_configured") that tells us which country table entries to add next. Behavior change is opt-in per table row.

  **2. supports_guest_language_preference = True for all new hotels** — comes free with #1; the plan sets it unconditionally whenever a provider is present, matching the "always Yes" line in every country checklist. No separate work needed.

  ### Tier 2 — small builds, each needs one product decision first

  **3. Voice forwarding-number default.** DefaultVoiceConfigProvider hard-requires the `VOICE_AI_FORWARD_CALL_TO` OnboardingValue; CS's own runbook (https://app.notion.com/p/33481468615180f59f01f6a76f99f540) says the placeholder is always the hotel's own phone. Change: fall back to hotel phone when the OnboardingValue is absent. Scope is tiny (one provider, ad-hoc CONFIGURE_VOICE stage that CS triggers deliberately). Decision needed: confirm hotel-phone fallback can't create a forwarding loop on any telephony path.
  - **4. GDPR ID purge for EU/UK** — set `purge_id_on_reservation_status_change=True` when hotel_country is in an EU/UK list. Prescribed in both the Spain and UK checklists. Decision needed: sign-off on the documented trade-off (purged IDs unavailable for chargeback evidence). Mechanically trivial once approved — a country-conditional field-set in an existing or new small plan.
  - **5. Check-in/check-out times** — HotelInfoPlan already supports them; DefaultSalesforceHotelInfoProvider never sets them. Decision needed: confirm the Salesforce account/opportunity actually carries these fields for non-enterprise deals; if yes, it's a 5-line provider change.

  ### Specify now, build next (not "today", but the spec can be written this week)

  - **6. DEFAULT Twilio stage** — DEFAULT has no ConfigureTwilioPlan wiring at all (BW/Wyndham do), yet every A2P form field CS fills is deterministic boilerplate ("Low Volume Mixed", "Canary Messages", standard samples, Canary Support fallback) and interim provisioning is already an admin button. This is the biggest CS-hours item after languages; spec = add CONFIGURE_TWILIO as an ad-hoc stage for DEFAULT reusing the existing plan + a default provider carrying the boilerplate.
  - **7. Webchat + portfolio constants** — welcome/error templates, booking-link param string, "Set up Dashboard=True"/"Grant User Management=True" are documented constants; fold into existing plans when chat settings get a DEFAULT plan.

  Suggested sequencing: ship #1/#2 as one PR pair (table+provider PR, wiring PR) this sprint; open decisions for #3-#5 in parallel; write the Twilio spec while those land. If useful next step: I can draft the Linear tickets (as local drafts for your review — I won't post anything).

  ## Agent run 2026-08-05T20:50 — expansion of item #7 (webchat + portfolio constants)

  **Webchat constants.** After the DEFAULT script runs, the Webchat runbook has a CSA hand-configure settings that are documented constants: welcome/off-hours/error message templates, and the booking-link parameter string (`adults={adults}&children={children}&checkin_date=...`) appended to the hotel's booking engine URL. `ChatSettingsPlan` (backend/canary/onboarding/plans/chat_settings_plan.py) already handles all of it — auto-respond hours + off-hours message, AI flags (has_ai, is_ai_responding_enabled, has_managed_ai_answers), booking_url_prefix via BookingLinkConfigurationService, staff signatures, notification sound, escalation scope, preset message templates. Every ChatConfig field is nullable and the plan stamps only what the provider supplies, so a default provider can start minimal (boilerplate messages + preset templates only). Gap: the plan is wired only into enterprise paths (ChatConfigProviders exist for IHG and Best Western only); DEFAULT doesn't include it. Spec: a `DefaultChatConfigProvider` carrying the runbook constants, wired into DEFAULT, ideally gated on a messaging product being purchased. Caveat: the booking-link params string is per-booking-engine (Synxis vs Direct-book vs WindsurferCRS: currency/locale/date-format differ), so the default provider should stamp only engine-agnostic constants and leave the params template manual until PMS/booking-engine identity is plumbed into OnboardingPlanData (the Job 4 dependency).

  **Portfolio constants.** Probably NOT an onboarding-script change. The CS User Access runbook's "Set up Dashboard=True" / "Grant User Management=True" are defaults on the portfolio *creation* flow (admin/Onboarding App form), not per-hotel config — the quick win is pre-ticking those two boxes on the creation form, a tiny frontend/admin change. The script-side counterpart, `AddToPortfolioPlan` (plans/add_to_portfolio_plan.py), does a different job — attaching a hotel to an *existing* portfolio with exclusivity rules — and is wired only for enterprise/management-company paths (IHG, BW, MVW, Pyramid, Aimbridge, Crestline providers). DEFAULT hotels mostly lack a portfolio at script time, so scripted attachment would require resolving/auto-creating portfolios from the Salesforce account — a bigger decision, deliberately excluded from the "today" tiers.
project: 2026-08-05-strategy
source_id: null
tags: []
time_minutes: 5
title: Run analysis of CS onboarding activities after the basic, non-enterprise onboarding
  scripts run
updated: 2026-08-05 20:52:00.000000
waiting_on: null
waiting_since: null
working_on: false
---

https://canarytechnologies.slack.com/archives/D0B3K8BU0F3/p1785917736028909
https://canarytechnologies.slack.com/archives/D0B3K8BU0F3/p1785917765596929

Goal: Analyze Customer Success team's activities while onboarding hotels, by looking at their notion docs. 

Job 1: following the two examples above, find the general store of CS-aimed docs in Notion describing hotel configuration processes. 

Job 2: Narrow focus on country and language settings. What is set conditional on Hotel's country? Can we standardize and build into scripts?

Job 3: Look at the settings they're commonly changing. Are there any low-hanging fruit "always set this" type changes we can just build into default onboarding scripts?

Job 4: A more sophisticated analysis that's not limited by the current onboarding scripts. What conditionals (which product, which PMS integration, which payment gateway, etc) guide their actions?


Follow on agent task:
* Summarize quick, low-risk changes that we can specify today