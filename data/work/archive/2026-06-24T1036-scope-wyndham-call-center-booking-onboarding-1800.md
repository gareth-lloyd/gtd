---
area: management
contexts:
- deep
created: 2026-06-24 10:36:50.883320
defer_until: null
due: 2026-06-24
energy: high
id: 2026-06-24T1036-scope-wyndham-call-center-booking-onboarding-1800
order: null
output: "## Agent run 2026-06-24T10:40Z\n\nReviewed the Notion reqs doc + Slack thread
  + inline Notion comments, and mapped\nthe onboarding-script feasibility against
  the codebase. Summary below.\n\nSources:\n- Slack thread (#epd-enterprise, Arjun
  + Andrea + Gareth + Stephen + Brad):\n  https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1782230014192569?thread_ts=1782230014.192569&cid=C047K6WSUJY\n-
  Reqs doc \"\U0001F3E8 Wyndham Call-Center Booking: Onboarding Requirements\":\n
  \ https://www.notion.so/canarytechnologies/Wyndham-Call-Center-Booking-Onboarding-Requirements-388814686151815c9d6fc408859b78b5\n
  \ (lives under Enterprise > PRDs)\n\n### END STATE the Voice pod is driving to\nVoice
  wants Call-Center agents to take bookings for ~1,800 US/CA Wyndham\nproperties that
  are NOT on Canary and have no Hotel model. The current booking\nflow needs a Hotel
  to build the branded payment auth form from the Hotel + its\nCRS config. Rather
  than decouple booking from the Hotel model in code, the plan\nis to **onboard each
  of the 1,800 as a minimal \"basic\" Hotel** — created but NOT\nlive, and with NO
  per-hotel Voice setup. Callers reach these hotels through the\nshared Wyndham Call-Center
  line, not a per-hotel number, so per-hotel Voice is\nunnecessary. When done, an
  agent on the Call-Center line can pull up any of these\nhotels and submit a correctly-branded
  auth form for payment.\n\nConcretely, for each property the onboarding script must
  produce:\n- A Hotel model (basic, is_live=False)\n- Hotel core fields: slug, currency,
  timezone, country (+ name/address/city/\n  country_code/company are also hard-required
  to create the row — see below)\n- Wyndham Site ID association (stored as MulesoftConfiguration.hotel_code
  on a\n  CRSAccount linked to the Hotel)\n- CRS / Mulesoft config: site code, channels,
  brand, environment\n- AuthorizationConfiguration — auto-created on first access,
  no explicit step\n- Hotel Branding (logo, theme) so the auth form is branded — likely
  via\n  SetBrandingPlan & ConfigureHotelImagePlan. (Branding was added to the reqs\n
  \ after a comment from a reviewer flagged it as THE reason the hotel must exist.)\n\n###
  Explicitly OUT of scope (Voice owns these at the Call-Center level)\n- Hotels do
  NOT have to be live.\n- Per-hotel Voice config — not needed; callers use the shared
  Wyndham line.\n- BookingGatewayConfig — Voice configures booking/availability routing
  to the\n  CRS (Mulesoft); these hotels have no PMS.\n- PaymentGatewayConfig — one
  shared above-property Wyndham payment gateway; Voice\n  points the auth form at
  it. Not per-hotel.\nSo the script's job is narrow: create the Hotel + identity +
  CRS site\nassociation + branding. Everything booking/payment/voice is Voice's setup.\n\n###
  Prerequisites / dependencies (the gating unknowns)\n- Each property must exist in
  Salesforce as an Account/Opportunity, OR be in the\n  Enterprise Wyndham CSV so
  SF records can be created. Andrea flagged that\n  onboarding flows need SF opportunities
  for all 1,800 and asked whether they\n  already exist — **UNANSWERED**. This is
  the biggest dependency. Gareth's\n  expectation: most are in SF already, and there's
  a comprehensive Wyndham CSV\n  to backfill the rest.\n- Each Account needs name,
  phone, address, timezone, room count. Gaps can be\n  pulled from Mulesoft. Required
  site IDs are in the attached CSV\n  (wyndham_us_ca_not_modeled.csv) on the reqs
  doc.\n\n### Open questions to settle at the Thu Jun 25 sync (Andrea set this up)\n1.
  Do SF Accounts/Opportunities already exist for all ~1,800? If not, the CSV→SF\n
  \  creation step is in scope and is the long pole. (Andrea — top priority.)\n2.
  CRS config scope (raised by Brad/reviewer in a Notion comment, still\n   unresolved):
  do we submit via the hotel's own CRS or the Call-Center's? Arjun:\n   there's no
  real hotel-vs-call-center CRS distinction — it's the same Mulesoft\n   endpoints
  called with the site id; the per-hotel CRS config is in the reqs\n   mainly so we
  can refactor less now (possible follow-up cleanup). Confirm\n   whether per-hotel
  MulesoftConfiguration is truly required by the auth-form/\n   booking path or whether
  the call-center-level config covers it.\n3. Branding source: where do logo/theme
  come from for 1,800 hotels? CSV almost\n   certainly lacks logos. Is per-property
  branding needed, or is Wyndham\n   sub-brand-level branding sufficient (one branding
  per brand)? Pin down the\n   data source for SetBrandingPlan/ConfigureHotelImagePlan.\n4.
  Minimal auth-form contract: confirm with Brad exactly which Hotel fields the\n   auth
  form renders so we don't over- or under-onboard.\n5. Timeline: Arjun needs this
  by end of next week (~Fri Jul 3), before holidays,\n   ahead of Call-Center booking
  go-live.\n\n### Script-approach assessment (feasibility: GOOD)\nThe existing onboarding
  Plan/ConfigProvider framework is well-suited; this is a\nthin use of it, not new
  infra. Key landmarks in backend/canary/:\n- Plan base: onboarding/plans/base.py
  (atomic, idempotent OnboardingPlan.execute(hotel))\n- Wiring: onboarding/models/property_configuration_processes.py\n
  \ (ONBOARDING_TYPE_CONFIG maps OnboardingType→ScriptType→plans). A WYNDHAM_MSA\n
  \ onboarding type already exists.\n- Batch runner: onboarding/management/commands/cron_run_onboarding_script_batches.py\n
  \ (+ Cohort / OnboardingScriptBatch models) can orchestrate a large cohort,\n  scheduled.
  limit_to_parent_brand can scope to Wyndham.\n- Hotel model: hotels/models/hotel.py
  — HARD-required to create a row:\n  name, slug_name, company, address1, city, country,
  country_code, currency.\n  Should also set hotels_timezone, phone, is_live=False.\n-
  Wyndham Site ID: crs_gateway/mulesoft/models/configuration.py\n  (MulesoftConfiguration.hotel_code
  = the site id; brand_code, primary/secondary\n  channel). Setup via crs_gateway/services/crs_set_up.py
  (CRSSetupService) — this\n  is decoupled from hotel creation, so CRS association
  is a clean second phase.\n- AuthorizationConfiguration: authorization/models/configuration.py
  — auto-created\n  on first access via ReadonlyAwareAutoOneToOneField; no explicit
  plan needed.\n- Salesforce: onboarding/services/onboarding.py — the SF-account path
  is the\n  normal entry, but a blank/demo hotel path exists (_create_blank_hotel,\n
  \ OnboardingType.DEMO) that bypasses SF. So SF can be bypassed technically, but\n
  \ Andrea wants SF records for the onboarding flow + downstream CS/account hygiene\n
  \ — that's a process decision, not a code blocker.\n- NO existing CSV bulk-importer
  found — the net-new work is a thin management\n  command / loop that reads the CSV
  (or SF), creates Hotels, runs the base-config\n  + CRS-setup + branding plans per
  hotel, batched via the cron runner.\n\nNet: low-risk, mostly assembly of existing
  plans. The real scoping risk is\nupstream data (SF records exist? branding source?)
  and the CRS-config question —\nnot the script mechanics. Recommend the Thu sync
  lock down Q1–Q3 above before\ncommitting to the build.\n\n## Agent run 2026-06-24T17:32Z
  — channel read + design sketch\n\nRead #wyndham-voiceai-internal (the Voice pod
  working channel, C0AJ1ENFSSU) and\nchased the key threads. This sharpens the END
  STATE materially.\n\n### The end-state driver is concrete: cross-property booking\nThe
  1,800-hotel onboarding is a PREREQUISITE for cross-property booking, not a\nstandalone
  task. Project: 'Gen Res · Booking without points across properties'\n(Linear, team
  VOX, lead Arjun, status Implementation, target 2026-07-14, under the\nEnhanced Voice
  AI initiative):\nhttps://linear.app/canary-technologies/project/gen-res-booking-without-points-across-properties-e69349e68cf4\n-
  It extends the booking flow from single-property to ACROSS properties (~4% of\n
  \ global automation rate). Once the GenRes line books at any Wyndham property, every\n
  \ property — including the ~1,800 not modeled — needs a Hotel to generate the branded\n
  \ auth form. Stephen confirmed cross-property is in this release and reflected in
  the\n  SOW doc (thread: https://canarytechnologies.slack.com/archives/C0AJ1ENFSSU/p1782237313759629).\n-
  Timeline lines up: project target Jul 14 ⇒ Arjun's onboarding-by-end-of-next-week\n
  \ (~Jul 3), before Call Center booking go-live. The onboarding script is on the\n
  \ critical path for this release.\n\n### Other relevant signals from the channel\n-
  Card-over-the-Phone is in ACTIVE UAT (started Jun 23) — the card-capture/auth-form\n
  \ workstream the onboarding feeds. The branded-auth-form requirement is being tested\n
  \ now, not hypothetical.\n- Booking pilots are scaling — Arjun 'Enabling the next
  wave of booking pilots now!'\n  (Jun 17) via VOX-3332 (vetted property list). The
  1,800 is the bulk follow-on after\n  the vetted pilots.\n- Shared Wyndham payment
  gateway confirmed live (Shiji-tokenization thread references\n  gateway config 1225)
  — consistent with the single above-property gateway Voice points\n  at, not per-hotel.
  Reinforces leaving ConfigurePaymentGatewayIntegrationPlan OUT of\n  the onboarding
  subset.\n- 'above-property call search' GrowthBook flag is owned by the enterprise
  team — related\n  to the above-property/call-center model these hotels plug into.\n-
  NOT in scope of the 1,800: VOX-3463 (cross-property suggestion for single-property\n
  \ bookings) is a flagged follow-up, not this release; Wyndham Connect Plus International\n
  \ (LATAM/EMEA/SEAPR) is a separate track — the 1,800 is US/CA only.\n\n### Design
  sketch — minimal subset of the Wyndham onboarding flow\nFull sketch written to plan
  file: ~/.claude/plans/functional-swinging-falcon.md\nThe full WYNDHAM_MSA flow runs
  ~18 plans in BASE_CONFIGURATION_NEW + Twilio + PMS\ncreate/validate + membership
  gateway + room upgrades + GOLIVE. The minimal subset is a\nNEW OnboardingType (e.g.
  WYNDHAM_CALL_CENTER_BOOKING) with can_create_new_hotels=True,\na SINGLE BASE_CONFIGURATION_NEW
  stage, and NO go-live (terminal_stage = initial_stage,\nmirroring the WYNDHAM_AI_VOICE
  single-stage pattern). Maps each Notion requirement to one\nexisting plan (no new
  plans needed — pure config assembly):\n- HotelInfoPlan + WyndhamHotelInfoProvider
  → core fields; slug wyndham-{site_id}, currency, timezone, country (required)\n-
  SetBrandingPlan + DefaultBrandingConfigProvider → branding is brand-level by BrandId,
  not per-property (required)\n- CreateHotelAssociationIdsPlan + WyndhamHotelAssociationIdConfigProvider
  → Wyndham Site ID association (required)\n- CRSGatewayPlan + WyndhamCRSGatewayConfigProvider
  → CRSAccount + Mulesoft config (required*; * = the open CRS-scope question Q2)\n-
  AddToPortfolioPlan + WyndhamPortfolioConfigProvider → WYNDHAM portfolio membership
  (REQUIRED, not just tagging)\n- ConfigureHotelImagePlan + WyndhamHotelImageProvider
  → header image (optional)\n- AuthorizationConfiguration → auto-created on first
  access, no plan\nKey find: the per-hotel Voice path we are AVOIDING is voice/management/commands/\nsetup_voice_booking_authform.py
  — it requires voice_configuration (livekit) + a\nBookingGatewayConfig + Wyndham
  portfolio membership, then points the shared\nWYNDHAM_PAYMENT_GATEWAY_UUID. Voice
  runs that at the call-center level; the onboarding\nscript does not. But it checks
  WYNDHAM portfolio membership to route to the shared\ngateway — which is why AddToPortfolioPlan
  must stay in the subset.\nWiring a new type also touches: onboarding_type.py (enum),
  services/types.py (SF\nopportunity→deployment→type mapping, if driven via SF), KNOWN_PLANS
  (all six already\nregistered), and a migration for the OnboardingScriptBatch/Cohort
  choices.\n"
project: 2026-04-16T1210-unblock-team
source_id: https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1782230014192569?thread_ts=1782230014.192569&cid=C047K6WSUJY
tags:
- morning-gtd
- slack
time_minutes: 15
title: Scope Wyndham Call Center booking onboarding (~1800 non-onboarded Wyndhams)
updated: 2026-06-25 14:39:05.302526
waiting_on: null
waiting_since: null
working_on: false
---

original request: https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1782230014192569

Arjun (@me + Andrea) in #epd-enterprise: Voice wants to book ~1800 non-onboarded US/CA Wyndhams via Call Center; plan is a minimal onboarding script (not live, no Voice). Reqs doc: https://www.notion.so/canarytechnologies/Wyndham-Call-Center-Booking-Onboarding-Requirements-388814686151815c9d6fc408859b78b5 — needed by end of next week. Andrea set a Thu Jun 25 sync. Review reqs + assess script approach. https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1782230014192569?thread_ts=1782230014.192569&cid=C047K6WSUJY


Aim: document the end state Voice pod are trying to get to.