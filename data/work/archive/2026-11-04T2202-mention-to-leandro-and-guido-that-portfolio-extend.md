---
area: null
completed_at: 2026-11-06 16:57:08.745707
contexts: []
created: 2026-11-04 22:02:17.533435
defer_until: null
due: null
energy: low
id: 2026-11-04T2202-mention-to-leandro-and-guido-that-portfolio-extend
order: null
output: |
  ## Agent run 2026-11-06T16:45 (research + draft message; nothing sent)

  ### Where the guard lives (all on master)
  - `RegistrationCardService.is_portfolio_managed(hotel)` — backend/canary/check_in/services/registration_card.py:328. True when the hotel has a `RegistrationCardExtension` in state CURRENT. Docstring: "A portfolio push rewrites every member hotel's schema server-side ... so local edits do not survive."
  - Callers that stop on it:
    - `GuestFieldsSourceService.move_to_catalog` — guest_experience/services/guest_fields_source.py:50 → returns `SourceChangeOutcome.PORTFOLIO_MANAGED`
    - `CatalogExtractionService.extract_for_hotel` / `regenerate_for_hotel` — guest_experience/services/catalog_extraction.py:74 and :122 → `ExtractionOutcome.PORTFOLIO_MANAGED`
    - `V3MigrationService.migrate_hotel_to_v3_and_catalog` maps it to `V3CatalogMigrationOutcome.PORTFOLIO_MANAGED` — guest_experience/services/v3_migration.py:65
    - Onboarding: `ConfigureCheckInPlan._move_to_catalog` raises `ERROR_REGISTRATION_CARD_PORTFOLIO_MANAGED` — onboarding/plans/configure_check_in_plan.py:24 (Ramiro, TOOL-871, PR #60865). Message to operators: "Send the hotel to the team that owns check-in v3, who handle portfolio cards." (onboarding/exceptions.py:322, :683)
    - Leandro's just-merged ENT-8140 PR #62935 (https://github.com/canary-technologies-corp/canary/pull/62935, merged 2026-11-06) keeps the same `PORTFOLIO_MANAGED` early return.
  - Introduced by Rafael Nunes in AD-8176 (PR #56116, https://github.com/canary-technologies-corp/canary/pull/56116) and AD-8179 (PR #56118); regenerate path in AD-10273 (PR #59861).

  ### Existing ticket for this exact gap
  - AD-8448 "[FieldsCatalog] Make portfolio card pushes write the field catalog" — https://linear.app/canary-technologies/issue/AD-8448/fieldscatalog-make-portfolio-card-pushes-write-the-field-catalog — created by Leandro 2026-09-22, assigned Rafael, In Progress since 2026-10-23, no comments, no PR yet. Its branch name is `glloyd/ad-8448-...` (you may have been attached to it at some point). Acceptance criterion 3 is "move_to_catalog accepts a portfolio-managed hotel", but it is gated on criterion 1 (push must write catalog rows first). Related: AD-8180 (drop schema_form_json) is blocked by these hotels staying on the card.

  ### Assessment of your point
  - Correct for the migration itself. The portfolio push (`PortfolioExtendableRegistrationCardService.update_portfolio_extendable_registration_card`, check_in/services/extendable_registration_card.py:81) synchronously rewrites each member hotel's `RegistrationCard.schema` in the same transaction. So at migration time the hotel's current card IS the portfolio card plus its extension; extracting the catalog from it is as valid as for any other hotel. Refusing is not protecting anything on the way in.
  - One residual question they will raise: after the hotel is on the catalog, a later portfolio push still writes `RegistrationCard.schema`, which a catalog hotel no longer reads, and `regenerate_for_hotel` also refuses portfolio-managed hotels, so the push would be silently ignored. That is what AD-8448 is about. Your "we're replacing reg cards" framing answers it if portfolio-level config is moving to the catalog/onboarding plans anyway; worth saying explicitly so they do not read the ask as "drop the ticket".
  - Not verified: how many v3 hotels are currently portfolio-managed (BW is the only known PortfolioExtendableRegistrationCard user per ENT-4303/ENT-5437/ENT-6321). Would need a prod read.

  ### Draft Slack message (NOT sent — needs your go-ahead; send to Leandro Alvarez and Guido Percu)
  > Quick one on the v3/catalog migration: `is_portfolio_managed` makes `move_to_catalog`, `extract_for_hotel` and `ConfigureCheckInPlan` stop and return `portfolio_managed` whenever a hotel has a CURRENT `RegistrationCardExtension`. I don't think that guard should block the migration. The portfolio push writes the member hotel's `RegistrationCard.schema` synchronously, so the hotel's current card is always up to date and can be relied on as the extraction source, same as any other hotel. The only real gap is post-migration drift (a later push updates a card the catalog hotel no longer reads), which is AD-8448, and that matters less and less as we replace reg cards with catalog/onboarding config. Suggest: let the migration through today and treat AD-8448 as "make the push write catalog rows" rather than a precondition. Happy to pair on it. Context: check_in/services/registration_card.py:328, guest_experience/services/guest_fields_source.py:50, onboarding/plans/configure_check_in_plan.py:24, https://linear.app/canary-technologies/issue/AD-8448

  ### Possible follow-ups (your call)
  - Send the message above (Slack DM/group to Leandro + Guido, or comment on AD-8448).
  - If they agree: small PR removing the three `is_portfolio_managed` early returns and the onboarding error mapping, plus a test that a portfolio-managed hotel extracts from its current card. Rafael owns AD-8448, so loop him in.

  ## Agent run 2026-11-06T17:00 (audience + Linear comment draft; nothing posted)

  Audience: Rafael Nunes owns the guard and AD-8448, so he is the decider; Leandro created the ticket; Guido is secondary. Recommended: comment on AD-8448 so all three see it next to the acceptance criteria.

  ### Draft comment for AD-8448 (https://linear.app/canary-technologies/issue/AD-8448) — NOT posted
  Proposing we split this ticket's acceptance criteria. Criterion 3 ("move_to_catalog accepts a portfolio-managed hotel") does not need to wait for criterion 1 ("a push writes catalog rows").

  Why the guard is not protecting the migration: is_portfolio_managed (check_in/services/registration_card.py:328) stops move_to_catalog, extract_for_hotel, regenerate_for_hotel and the onboarding ConfigureCheckInPlan. But the portfolio push (extendable_registration_card.py:81) rewrites each member hotel's RegistrationCard.schema synchronously, in the same transaction. At migration time the hotel's current card IS the portfolio card plus its extension, so extracting from it is as valid as for any other hotel.

  What the guard was actually guarding: post-migration drift (a later push writes a card the catalog hotel no longer reads). Real, but that is criterion 1, not a reason to keep the hotel off the catalog today, and it shrinks as reg cards are replaced by catalog/onboarding-plan config (ENT-8140, TOOL-871/872).

  Proposal: (1) now, drop the is_portfolio_managed early returns in guest_fields_source.py, catalog_extraction.py and the ERROR_REGISTRATION_CARD_PORTFOLIO_MANAGED mapping in configure_check_in_plan.py; add a test that a hotel with a CURRENT RegistrationCardExtension extracts from its current card. (2) This ticket keeps criteria 1, 2, 4. Also unblocks AD-8180 for portfolio-managed v3 hotels. Not yet checked: count of portfolio-managed v3 hotels (BW only known user).

  Before posting: verify @mention handles for Rafael/Leandro/Guido; decide whether to keep the "I can take it or pair" offer.

  ## Agent run 2026-11-06T17:20 ("are they actually blocked?")

  Short answer: nobody is blocked from check-in v3 today. The guard only blocks the *catalog* move, and only Best Western has portfolio-managed cards. It bites in three places, none urgent yet:
  - BW v3 hotels stay on the registration card inside v3 (migrate_hotel_to_v3 works; move_to_catalog refuses). Guido's BW v3 migration is proceeding anyway: https://canarytechnologies.slack.com/archives/C07BX379GQK/p1792692328083429 (2026-10-22).
  - AD-8180 (drop schema_form_json) needs every v3 hotel on the catalog, so BW blocks it. That is the AD team's own cost, not an ENT one.
  - Onboarding: ConfigureCheckInPlan (v3 + catalog + country fields) runs only in the OnboardingType.DEFAULT process (property_configuration_processes.py:3314). Enterprise BW/IHG/Wyndham scripts still set v2 (Andrea, same thread; Connor asked about moving them to v3). The BW registration card provider creates a RegistrationCardExtension per hotel (best_western/registration_card_provider.py:115), so the day ENT scripts adopt ConfigureCheckInPlan, every BW onboarding hits ERROR_REGISTRATION_CARD_PORTFOLIO_MANAGED. That is the forward-looking reason to lift it before the ENT script change, not after.

  How the AD team is handling it: AD-8448 exists (Leandro, 2026-09-22). On 2026-10-22 Leandro asked Rafael whether he had started; Rafael had not, Leandro said he would take it (https://canarytechnologies.slack.com/archives/C029BPP02H0/p1792684260328789?thread_ts=1792684188.914489&cid=C029BPP02H0). Linear still shows Rafael as assignee, In Progress since 2026-10-23, no PR. Leandro shipped ENT-8140 (#62935, merged today) first and kept the early return. So: acknowledged, parked behind the "push must write catalog rows" precondition. "Effectively dealt with" only in the sense that nothing needs it yet.

  You already made this point to Andrea and Connor on 2026-10-29 ("self-imposed limitation ... doesn't block in practice"): https://canarytechnologies.slack.com/archives/C0B1Y5K9AMC/p1793282223358729

  Not obtained: prod count of portfolio-managed hotels by check-in version. The auto-mode classifier denied the read-only Sallyport query. Query to run yourself on the canary DB (us-west-2 and eu-central-1):
    SELECT c.checkin_version, c.uses_field_catalog, p.slug, count(DISTINCT e.hotel_id)
    FROM check_in_registrationcardextension e
    JOIN check_in_portfolioextendableregistrationcard p ON p.id = e.extendable_registration_card_id
    JOIN check_in_configuration c ON c.hotel_id = e.hotel_id
    WHERE e.state = 'current' GROUP BY 1,2,3 ORDER BY 4 DESC;

  Implication for the draft comment: reframe from "you are blocking hotels" to "lift it now so the ENT script move to v3+catalog does not trip on BW". Add Rafael and Leandro; Guido is cc.
project: null
source_id: null
tags: []
time_minutes: 5
title: mention to leandro and guido that portfolio extendable should not limit
updated: 2026-11-06 16:57:08.745687
waiting_on: null
waiting_since: null
working_on: false
---

Check the AD team's check-in v3 catalog migration code
It explicitly stops fand raises for portfolioextendableRegistrationcard prsence. 

not an issue in practice if we're replacing reg cards. The current reg card will always be up-to-date and can be relied on.