---
area: null
completed_at: null
contexts:
- react
created: 2026-10-21 09:50:10.042616
defer_until: null
due: null
energy: medium
id: 2026-10-21T0950-reply-to-sam-kariu-re-eng-design-automate-check-in
order: null
output: "## Agent run 2026-10-21T10:20\n\nRead the design doc (https://app.notion.com/p/canarytechnologies/Eng-Design-Automate-Check-in-V3-Onboarding-3df8146861518182b3b7ee941e476814),
  all 9 comment threads, and Sam's DM (https://canarytechnologies.slack.com/archives/D04UH06R738/p1792499787232569).
  Spot-checked the doc's code claims against master (as of 2026-10-20). Nothing sent;
  reply below is a draft.\n\n### Context\n- Sam's DM is just the link, no question.
  Doc status is \"REVIEW ME!\", last edited 2026-10-19. The Reviewers property lists
  Laura DeWald plus one other person; you are not on it. The inline Reviewers table
  returned no rows.\n- Both of your earlier comments (24 Sep) got replies: the V3
  rebuild paragraph was made more specific, and Sam acknowledged the billing-country
  point. Laura's comments (US OCR, GDPR retention, risk handling, backwards-compat
  list) all look addressed in the current text. The threads are still open, so Sam
  could resolve them.\n- The design has changed a lot since you last read it. It no
  longer writes a country registration card. Onboarding now ends with: write check-in
  settings (OCR on when bought) -> `migrate_hotel_to_v3` -> `move_to_catalog` -> add
  the country's catalog fields. Phase 1 (tickets 1-6, TOOL-866..871) needs no country
  content. A hotel already on the catalog or already live is skipped.\n\n### What
  I checked in code\n- OK: `GuestFieldsSourceService.move_to_catalog` (guest_experience/services/guest_fields_source.py:44),
  `V3MigrationService.migrate_hotel_to_v3` (guest_experience/services/v3_migration.py:117)
  and `enforce_v3_blockers_on_config_save` (guest_experience/signals.py:56) all exist.\n-
  OK: `MissingSalesforceOpportunityError` is caught in `DefaultHotelProductsProvider`
  (onboarding/plans/hotel_products_plan.py:168).\n- Overstated: the doc says \"the
  onboarding script never applies IGNORED_PRODUCT_TYPES\". It is applied in `OpportunityHotelProductsProvider._parse_products`
  (onboarding/configuration_providers/opportunity_hotel_products_provider.py:63) and
  in `get_salesforce_product_types_to_activate_from_salesforce_data` (onboarding/services/onboarding.py:1020).
  Both are product-activation paths. The design's OCR check reads raw strings from
  `get_salesforce_products`, so the conclusion (no change to the ignore list) still
  holds. The sentence just needs narrowing.\n- Real gap: `move_to_catalog` does not
  raise. It returns a `SourceChangeOutcome`: MOVED_TO_CATALOG / ALREADY_ON_CATALOG
  / REFUSED / NO_STEP / PORTFOLIO_MANAGED. Its `_move` docstring says a refusal deliberately
  leaves already-extracted catalog rows in place. So two doc claims only hold if ticket
  6 (TOOL-871) does the work:\n  - \"A refused move fails the run\". The plan must
  raise on any outcome other than MOVED_TO_CATALOG, including NO_STEP if the v3 seed
  has not produced steps.\n  - \"A retry starts clean\". The raise must happen inside
  the transaction so the partial rows roll back.\n  Worth spelling out in ticket 6.\n\n###
  Other points worth raising (judgement, not verified)\n- \"Already live\" is the
  skip condition but is not defined: which field or state? It decides whether a re-run
  touches a hotel, so it should be named in ticket 6.\n- Risk 5 says every v3 hotel
  moves onto the catalog by end of October 2026, which is this month. Phase 1 depends
  on the catalog being stable for brand-new hotels. Does A&D have a date for when
  `move_to_catalog` is considered GA?\n- Minor: \"In short\" says onboarding ends
  in three steps, while Proposed solution says four (the fourth is the phase-2 country
  fields). Fine, but a reader could trip on it.\n\n### Draft Slack reply to Sam (DM
  D04UH06R738). NOT SENT\n> Hey Sam, read through the latest version. It's much cleaner
  now that it goes straight to v3 + the catalog instead of building a country card,
  and splitting phase 1 so it needs no country content is a good call. Overall \U0001F44D
  from me, just a few things:\n> 1. `move_to_catalog` doesn't raise. It returns a
  `SourceChangeOutcome` (REFUSED / NO_STEP / PORTFOLIO_MANAGED…), and on refusal it
  intentionally leaves already-extracted rows behind. So \"a refused move fails the
  run\" and \"a retry starts clean\" only hold if TOOL-871 raises on anything but
  MOVED_TO_CATALOG *inside* the transaction. Might be worth stating that in the ticket.\n>
  2. What does \"already live\" mean for the skip check? Worth naming the exact field,
  since it decides whether a re-run touches a hotel.\n> 3. Small one: \"the onboarding
  script never applies IGNORED_PRODUCT_TYPES\" isn't quite right. `OpportunityHotelProductsProvider`
  and the activation path both subtract it. Your OCR check reads raw products via
  `get_salesforce_products` so the conclusion stands, the sentence just needs narrowing.\n>
  4. Risk 5: catalog for every v3 hotel by end of Oct is basically now. Do A&D consider
  it ready for brand-new hotels?\n> Also, my and Laura's older comment threads look
  addressed, so feel free to resolve them.\n\nAlternatively, post points 1-3 as inline
  Notion comments on the doc (on \"A refused move fails the run\", \"A hotel already
  set up is skipped\", and the IGNORED_PRODUCT_TYPES bullet) and send Sam a one-liner
  in Slack. Your call; nothing has been posted.\n\n## Agent run 2026-10-21T10:11\n\n>
  Follow-up asked: \"Summarize Sam's design at high level\"\n\nSource: the design
  doc (https://app.notion.com/p/canarytechnologies/Eng-Design-Automate-Check-in-V3-Onboarding-3df8146861518182b3b7ee941e476814),
  re-fetched. It is unchanged since the last run (last edited 2026-10-19). Linear
  project: https://linear.app/canary-technologies/project/automate-check-in-v3-onboarding-617b22ca4b48\n\n###
  Problem\nNon-enterprise (DEFAULT) onboarding gives every hotel the same hardcoded,
  US-shaped registration card, whatever its country. `DefaultRegistrationCardProvider`
  ignores its input. So after every EMEA go-live a CSM rebuilds the card by hand to
  meet local law. Onboarding also leaves hotels on v2 and the registration card, and
  both are being retired.\n\n### What the design does\nAt the end of DEFAULT onboarding,
  for a new hotel only (a hotel already on the catalog or already live is skipped):\n1.
  Write the check-in settings. If the hotel bought OCR (per Salesforce `Active_Products__c`
  across its active opportunities), switch the ID step on: `*_WITH_OCR`, or `OPTIONAL_WITH_OCR`
  when its country has no definition. The script never switches OCR off.\n2. Route
  the hotel to v3 (`migrate_hotel_to_v3`).\n3. Move the hotel onto the field catalog
  (`move_to_catalog`). The standard catalog comes from the default template, and nothing
  is written to the registration card.\n4. Phase 2 only: if the hotel's country (taken
  from the Salesforce billing address) has a definition in code, add that country's
  fields to the catalog and its registration form. The country also supplies the ID
  editability, additional-guest and retention/purge settings, which are written in
  step 1 because the move locks them.\nSteps 3 and 4 commit in one transaction. If
  `move_to_catalog` refuses the hotel, the run fails loudly.\n\nA country with no
  definition gets the standard catalog and no error. DEFAULT serves every independent
  hotel worldwide, US included, so erroring there would block almost all onboarding.\n\n###
  Structure\n- Providers: a base `CountryRegistrationCardProvider` plus one thin subclass
  per country under `onboarding/configuration_providers/country/`, chosen on `HOTEL_COUNTRY`.
  `DefaultRegistrationCardProvider` stays the fallback. The OCR check is shared code,
  so OCR works whether or not a country is defined.\n- Monitoring: `check_hotel_configuration`
  reports where a live hotel has drifted from its country definition and changes nothing.
  It covers OCR vs purchase, `id_document_*`, additional-guest settings, retention,
  and whether the country fields are present. A separate check flags hotels in undefined
  countries. It reads the local `SalesforceOpportunity` mirror through the same purchased-products
  rule that onboarding uses.\n- No feature flag. The list of defined countries is
  the rollout control.\n\n### Phases and tickets\n- Phase 1 (needs no country content):
  TOOL-866 handle `V3MigrationBlocked`; TOOL-867 compute `has_id_document_ocr` from
  `is_ocr_enabled`; TOOL-868 alias the product name \"Contactless Check-in - ID OCR\";
  TOOL-869 one purchased-products rule shared by onboarding and monitoring; TOOL-870
  OCR on the default path; TOOL-871 route new hotels to v3 and the catalog.\n- Phase
  2 (gated on legally approved content, none of which exists yet): TOOL-872 country
  provider base; TOOL-873 monitoring; TOOL-874 Italy, then TOOL-875 Spain and TOOL-876
  UK.\n\n### Out of scope\nEnterprise paths (Wyndham, BW, IHG), Incode ID verification,
  translated labels, a CS editing UI, existing hotels (A&D's migration), fields that
  depend on guest nationality, and kiosk.\n\n### Main accepted risks\n- No approved
  country content yet.\n- The billing country may differ from the physical country.\n-
  The field catalog is new; every v3 hotel is due on it by the end of Oct 2026.\n-
  Definitions live in code, so every legal change needs engineering.\n- This is the
  first thing that switches OCR on automatically, which brings GDPR into play; each
  definition carries retention settings for that reason.\n\nOpen product questions
  (which countries ship first, who signs off on legal content, the ID step for undefined
  countries, kiosk) are in the doc's appendix and do not block the build.\n\nMy review
  points and the draft Slack reply from the previous run still apply. Nothing was
  sent.\n"
project: 2026-08-31-ihg
source_id: https://canarytechnologies.slack.com/archives/D04UH06R738/p1792499787232569
tags:
- morning-gtd
- slack
time_minutes: 30
title: 'Reply to Sam Kariu re: Eng Design: Automate Check-in V3 Onboarding'
updated: 2026-10-21 14:47:08.929442
waiting_on: null
waiting_since: null
working_on: false
---

Sam DM'd the design doc (Oct 20) and is waiting on my read.
https://app.notion.com/p/canarytechnologies/Eng-Design-Automate-Check-in-V3-Onboarding-3df8146861518182b3b7ee941e476814
https://canarytechnologies.slack.com/archives/D04UH06R738/p1792499787232569