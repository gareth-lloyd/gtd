---
area: null
contexts: []
created: 2026-05-14 11:20:32.681178
defer_until: null
due: null
energy: medium
id: 2026-05-14T1120-marriott-managed-situation
order: 8
output: '## Agent run 2026-05-14T13:05Z


  ### What the task is

  ENT-6117 — Courtyard by Marriott Los Angeles Monterey Park transitioned from Marriott-managed
  to Aimbridge-franchised. GM Cindy Dang (cindy.dang@aimbridge.com) can''t log in
  via canarytechnologies.com because the hotel is still wired to Marriott PingFederate
  SSO. The ticket also codifies the manual runbook into a `MarriottRemoveHotelFromParentBrandProvider`
  driving `DeactivateHotelPlan`.


  ### Pinned comment from Ashley Kleczek (2026-05-13)

  > "this property was never live with Marriott Digital Tips, they were just under
  the Enterprise umbrella. Can they keep this dashboard or can you let me know if
  I need to make a new one? They already received their tip collateral and are very
  eager to get started"

  > "where can our CSA team see this on SFDC so when they go to create a new dashboard,
  they know if needs to be newly created. cc @dguzman"


  Two questions: (1) can the existing Canary hotel be reused since it was never live
  on Tips? (2) where in SFDC can CSA see this signal so they don''t have to ask each
  time?


  ### My take — Q1: New dashboard required even though never live on Tips

  Precedent: **ENT-5949 (Dearborn Inn, Autograph Collection)**, Done 2026-04-17. Identical
  scenario — Dan Logan: *"this property was previously managed by a separate 3rd Party
  and needs a new Admin & Dashboard configured for a fresh start. **It is not live
  on any products.**"* Resolution was the fresh-hotel path (dissociate old, CS creates
  new via SFDC Onboarding App). "Never live on products" doesn''t change the recipe.


  Why reuse doesn''t work in-place for LAXMP regardless of Tips status:

  - `sso_organization.slug = marriott` → PingFederate SSO claim is `hotels: ["LAXMP"]`.
  Cindy''s @aimbridge.com identity can never satisfy that claim. SSO detach is required.

  - `SalesforceHotelMetadata.parent_brand_name = "Marriott International"` and the
  `SalesforceHotelAccount` rows point at the old Marriott-managed SF Account. If CS
  reuses the hotel, every `IncidentService.update_salesforce*` writeback path keeps
  pointing at the wrong SF Account.

  - `HotelAssociationId` rows (MARSHA code, segment id, property id) are Marriott-specific.

  - The `marriott` parent brand also gates tipping config (RRD/Prisma payroll) — even
  though never live, the config plumbing on the record assumes Marriott corporate
  ownership.


  Doing the in-place flip is exactly the work `DeactivateHotelPlan` + the new `MarriottRemoveHotelFromParentBrandProvider`
  would do. Once that runs, the SF Account is free and CS creates a clean hotel via
  the SFDC Onboarding App. So the answer to Ashley is the same as ENT-5949: **new
  dashboard required; old hotel gets archived in place.**


  Important nuance for Ashley: she''s worried about the tip-collateral handoff. The
  new (Aimbridge-franchisee) hotel is *not* on Marriott Digital Tips — it will be
  onboarded as a regular franchisee Tips dashboard if Aimbridge wants Tips. Collateral
  that referenced the property URL/slug will continue to work because the runbook
  archives the old slug with a `-marriott-managed` suffix and frees the original slug
  for the new hotel to claim. Confirm with Taylor whether the collateral was Marriott-program-specific
  (in which case it needs to be regenerated under the franchisee program).


  ### My take — Q2: SFDC visibility for CSA team

  I don''t have direct SFDC schema access from here. The signal in Canary is: `Hotel.sso_organization.slug
  == "marriott"` OR `SalesforceHotelMetadata.parent_brand_name == "Marriott International"`
  (the canonical fields `MarriottRemoveHotelFromParentBrandProvider` checks). The
  SFDC mirror of this should be queryable on the Account record — likely an Account-level
  field like *Parent Brand* or *Account Type*. **Action: ask Daniel Guzman / SFDC
  admin which Account field reflects Marriott-managed vs. franchisee** so CSA can
  self-serve the decision before opening an Enterprise ticket.


  A second-order improvement: once ENT-6117 ships, we could surface in the SFDC Onboarding
  App''s preflight check whether the SF Account already has a Canary Hotel with `parent_brand
  = Marriott`, and if so block creation until the archive runbook has run. That would
  make Q2 mostly moot — the tool would tell CSA directly.


  ### Recommended reply (draft only — NOT sent)

  ```

  @Ashley — new dashboard. Same as ENT-5949 (Dearborn Inn) even though that one

  was also never live: the hotel record is wired to Marriott SSO + the

  Marriott SF Account + Marriott parent brand, so the existing dashboard can''t

  be handed to an Aimbridge-managed GM as-is. ENT-6117 codifies the archive

  runbook; once it runs against LAXMP, CS can create the new dashboard via

  the SFDC Onboarding App (the old slug is freed for the new hotel to claim).


  On the tip collateral — if the collateral was generated under Marriott

  Digital Tips specifically (Marriott payroll integration, Marriott-branded

  materials), it''ll need to be regenerated for the Aimbridge franchisee

  program. If it''s generic property-branded collateral keyed off slug/name,

  the slug-freeing step means it should still work post-archive. Best to

  loop Taylor on which flavor it is.


  @Daniel — for SFDC visibility: in Canary the signal is

  `parent_brand_name == "Marriott International"` on SalesforceHotelMetadata,

  or `sso_organization.slug == "marriott"` on the Hotel. Which Account-level

  field on SFDC mirrors this? If we can point CSA at one column, they can

  decide "new dashboard vs. reuse" without filing an Enterprise ticket.

  ```


  ### Status of ENT-6117 implementation itself

  - Description ratified, scope locked (per Taylor''s Slack answers logged in the
  2026-05-11 comment).

  - Branch `glloyd/ent-6117-change-from-marriott-managed-to-non-managed` exists; ticket
  moved to In Progress 2026-05-14T08:19Z.

  - No PR yet. Next implementation steps are well-specified in the description (4
  fields on `DeactivateConfig`, new provider, error code, wire into `MARRIOTT_TIPPING`
  process, tests). Estimated ≤1 day once started.

  - LAXMP itself is a candidate first-customer once the code is merged — Ashley''s
  comment is effectively asking for an ETA.


  ### Suggested next actions for Gareth

  1. Post the reply to Ashley + Daniel on ENT-6117 (text above; needs your final sign-off
  before sending — agent did NOT post).

  2. Ping Taylor in the existing Slack thread to clarify the tip-collateral flavor
  (Marriott program vs. generic).

  3. Decide: ship ENT-6117 first and use LAXMP as the smoke-test case, or do LAXMP
  via the existing manual runbook now and ship ENT-6117 after. The Aimbridge GM is
  blocked on login, so the manual runbook is probably the faster path for this single
  property; ENT-6117 then prevents the next one from being manual.

  4. Followup ticket idea: SFDC Onboarding App preflight ("Account already has a Marriott-branded
  Canary hotel — archive it first?") — defers Q2 by tooling it away.


  ### Source pointers

  - ENT-6117 description + comments (this ticket).

  - ENT-5949 (Dearborn Inn) — direct precedent for "never live, still needs new dashboard".

  - ENT-5071 (Fairfield/SpringHill SeaWorld) — earlier precedent, slug-preservation
  concern.

  - Notion KBs linked in description: "Marriott Owned-to-Franchised Hotel Transition"
  and "Soft-Deleting a Hotel".

  - Slack thread referenced in description: canarytechnologies.slack.com/archives/C05E196GGD8/p1778267806249239
  (Taylor''s portfolios/is_active/user-access answers — not re-read this session).

  '
project: 2026-04-16T1351-ship
source_id: null
tags: []
time_minutes: 15
title: Marriott managed situation
updated: 2026-05-18 14:38:47.111724
waiting_on: null
waiting_since: null
working_on: true
---

https://linear.app/canary-technologies/issue/ENT-6117/change-from-marriott-managed-to-non-managed#comment-011051ff