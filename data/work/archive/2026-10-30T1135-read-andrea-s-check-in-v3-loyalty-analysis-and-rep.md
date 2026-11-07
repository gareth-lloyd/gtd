---
area: null
completed_at: 2026-11-06 16:58:19.650053
contexts:
- react
created: 2026-10-30 11:35:30.688825
defer_until: null
due: 2026-11-04
energy: medium
id: 2026-10-30T1135-read-andrea-s-check-in-v3-loyalty-analysis-and-rep
order: null
output: |-
  ## Agent run 2026-10-30T13:11:18+0200

  Read Andrea's page and checked its claims against master (8bd2f4314f6, 2026-10-29) by reading the code. Nothing was run. No reply sent; the draft is below.

  Sources:
  - Andrea's message: https://canarytechnologies.slack.com/archives/C0B1Y5K9AMC/p1793304476674559
  - Notion page: https://app.notion.com/p/4088146861518127b6fbcdcab4a24f97
  - #ihg v3 thread: https://canarytechnologies.slack.com/archives/C03V5P4B48P/p1793019778323619?thread_ts=1792692313.584389&cid=C03V5P4B48P
  - #best-western v3 thread: https://canarytechnologies.slack.com/archives/C07BX379GQK/p1792692328083429
  - #epd-mobile test hotel thread: https://canarytechnologies.slack.com/archives/C09M5GRJPL2/p1793295767347989

  ### Verdict
  The page is broadly right and useful. The main thing to add is that the gift step does not depend on the catalog, so "v3 catalog with loyalty" is really three separate pieces of work:
  1. Scripts move to v3. Needs Connor's greenlight.
  2. Scripts set up the gift step. Blocked on the A/D work.
  3. Scripts move to the catalog. Can follow later.
  `membership_gift_step/handler.py` has no catalog reference. This also corrects Andrea's 10/26 #ihg message, which said the request requires writing directly to the catalog.
  Caveat: TOOL-871 says A&D do not want v3 hotels left on the card, so staying on v3 without the catalog needs their agreement.

  ### Confirmed
  - Gift write services are placeholders (`membership_gift_service.py`). AD-8260, AD-8257 and AD-10449 are In Progress under Laura.
  - The flow seeder has no gift step (`desired_check_in_flow.py`); it is added through the Django admin inline. Laura enabled it by hand on vibhors-test-hotel on 10/29, and no prod hotel uses it.
  - Additional-guest settings are locked on catalog hotels, and onboarding does not catch `AdditionalGuestFormManagedByCatalog`.
  - `COUNTRY_REGISTRATION_CARD_PROVIDERS` is empty. `add_catalog_fields` creates fields with no upsert; `ConfigureCheckInPlan` protects it by skipping hotels already on the catalog or live.
  - Extract, regenerate and move all refuse portfolio-managed hotels. The v3 compatibility blockers do not check portfolio, so BW can go to v3 but not the catalog.

  ### Corrections to the page
  - "A public write service is needed" is overstated. `CatalogFieldWriteService` (create/update/delete) and `StepFormElementService` already exist, and Internal Tools' country provider uses them. The real gap is idempotent writes, plus enterprise-style edits to a whole template.
  - The page does not mention `V3MigrationService.migrate_hotel_to_v3_and_catalog` (AD-10463, Done) or `ConfigureCheckInPlan` (TOOL-871, Done). Neither needs a card, but with none they produce only the default form (`load_schema_form_json` falls back to the default template), so they don't by themselves solve custom enterprise templates. The plan currently only appears in the general process, which still writes a default card first.
  - "Posts it to the PMS" means a note only. `special_request_code` and `package_code` on `MembershipGift` are not read by the online flow; only the kiosk's separate gift model uses its codes. A failed post is logged as a warning and not retried. So the codes the page lists under gift contents currently do nothing.
  - The enrollment bug is confirmed from code. v3's `EXTRACTED_FIELD_TO_CHECK_IN_FIELD` has no `membership_enrollment_status`, so REQUESTED / DECLINED / ALREADY_MEMBER are not written at submit. Enrollment itself still queues. In Python, only the kiosk reads the field, so the impact is probably reporting. I did not check Snowflake or dashboards.
  - Gift contents are not fully "not defined". `gms_core_ihg_upsells_provider.py` already has options by brand and tier (`WELCOME_AMENITY_BY_BRAND_US`), with translations. IHG's signed-off copy changes go on top. Caitlyn asked Taylor on 10/21 to own this with ENT: https://canarytechnologies.slack.com/archives/C03V5P4B48P/p1792552828421049

  ### Missing from the page
  - Mobile is bigger than "web only". AD-10552 is in Triage with no assignee. There is no V3 manifest minimum for iOS or Android, so SDK builds never receive the step. Caitlyn's in-app target for IHG is Dec 3, or about Dec 20 if testing overflows.
  - Skip behaviour is unresolved. The PRD allows skipping, but the handler rejects it and web disables Continue until a gift is picked (AD-10552 item 3).
  - Existing IHG hotels: the page only covers no longer creating the add-ons. Already-configured hotels need the add-ons removed, as Andrea said on 10/26. My inference on order: enable the step first and remove the add-ons after. Until the SDK supports the step, removing add-ons could leave app guests with no amenity, and leaving both on would offer web guests the amenity twice.
  - Step position: IHG's demo order was reg card -> gift -> upsell -> id -> cc. The seeder appears to use consecutive order numbers, so a script-inserted step may have no clean slot. I did not read the reg card's order value. This favours A/D owning the slot in the seeder.
  - Step copy: `MembershipGiftStepConfiguration` strings also need a script path, because IHG's copy changes are "handled by configs" per Caitlyn.
  - Timing of the upsert ask: AD-10449 pins the service signatures and its admin DC has no stable key, so the ask should reach Laura before those land.
  - Timeline conflict: Caitlyn expects all IHG on v3 by mid-November, while Taylor paused IHG migration until ENT is aligned. No date is attached to the A/D tickets.

  ### Not verified
  - What the current IHG add-on writes to the PMS, so I can't say whether a note is equivalent. Fulfilment of the 600 points option needs checking with Taylor or Laura.
  - Status of AD-8261, AD-8262 and AD-8263, which I did not open.
  - What "the ask" refers to exactly. I assumed IHG's separate Welcome Amenity step plus scripts targeting v3/catalog.

  ### Draft reply for the group DM (C0B1Y5K9AMC), not sent
  Thanks Andrea, this is useful. I checked it against master and my main takeaway is that the gift step doesn't depend on the catalog. I'd split this into three pieces:
  1. Scripts move to v3: small, just needs Connor's greenlight.
  2. Scripts set up the gift step: blocked on A/D, and this is what IHG is waiting for.
  3. Scripts move to the catalog: can follow. BW can go to v3 but stays on the card until portfolio hotels are supported.

  One catch: A/D have said they don't want v3 hotels left on the card, so we should agree (3) can trail (1) with them.

  A few things I'd change or add on the page:
  • A catalog write service already exists (`CatalogFieldWriteService`, used by Internal Tools' country provider), but it's a per-field API with no idempotent writes. `migrate_hotel_to_v3_and_catalog` doesn't need a card, but without one it only produces the default form. So our custom templates either still build a card first, or we delete and add fields against the default. Neither is good, so the ask to A/D is a way to declare a whole catalog template.
  • The gift only posts a PMS note today. The gift's special request and package codes aren't used online. @Connor do you know if a note is enough for IHG fulfilment, especially points?
  • The enrollment status bug looks real, though probably reporting only.
  • Mobile is the date risk: AD-10552 is in Triage with no owner, and IHG's in-app target is Dec 3.
  • Existing IHG hotels need a cutover: step on first, add-ons off after, with the SDK timing in mind.
  • IHG's demo order puts the gift before upsells, and the seeder doesn't own that slot yet.

  Next steps I'd suggest:
  • Andrea, can you ask Laura about the upsert now? AD-10449 is pinning the service signatures, and there's no stable gift key yet. Same conversation: A/D seeds the step when gifts are turned on, in the right position.
  • Connor, can you greenlight (1)? Caitlyn expects IHG on v3 by mid-November, so that's the date to test.
  • Taylor owns gift contents per Caitlyn's 10/21 ask, and the current add-on config is a good starting point.
project: 2026-08-31-ihg
source_id: https://canarytechnologies.slack.com/archives/C0B1Y5K9AMC/p1793304476674559
tags:
- morning-gtd
- slack
time_minutes: 20
title: Read Andrea's check-in v3 loyalty analysis and reply (with Connor)
updated: 2026-11-06 16:58:19.650041
waiting_on: null
waiting_since: null
working_on: false
---

Andrea shared a Notion analysis of what v3 catalog needs for loyalty items, to inform the conversations around the ask.
https://canarytechnologies.slack.com/archives/C0B1Y5K9AMC/p1793304476674559