---
area: null
completed_at: 2026-09-11 15:00:59.451409
contexts:
- react
created: 2026-09-10 09:26:03.018049
defer_until: null
due: null
energy: high
id: 2026-09-10T0926-review-epd-enterprise-jordan-sterling-pr-55537-gen
order: null
output: |
  ## Agent run 2026-09-11T11:44:41Z

  **PR:** #55537 (https://github.com/canary-technologies-corp/canary/pull/55537), "ID-79: GET /api/private/v1/portfolios — list portfolios from the regional table". Linear ID-79 (https://linear.app/canary-technologies/issue/ID-79).
  **Slack thread:** https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1788992960326799

  **State:** open. Lauta (lmenaolivares) approved at 3fcaf40. Head is now 308f75e, which adds case-insensitive identifier matching after that approval. CI is green apart from the non-blocking E2E shard 4/4 (mergeState UNSTABLE). Andrea (abrad) left 2 comments and has not approved.

  **Jordan's questions.** He removed them from the PR body on 09-10 16:17, so they are recovered from the edit history:
  1. Is the API contract good?
  2. Is the shape of the portfolio object good?
  3. Should this read the Postgres portfolio table, or only the in-code identifier enum?

  **Already discussed in the review threads and Slack:**
  - Andrea asked about `primary_sso_organization_uuid`. Lauta said it's fine to leave it out.
  - Andrea asked about normalizing identifiers to lowercase. Jordan now matches them case-insensitively on input.
  - Lauta asked to add portfolio `types`. Jordan asked whether the number of types is bounded; Lauta thinks it will grow. Still open.
  - Lauta pushed back on one endpoint for every principal. Jordan cited the one-API-per-resource direction (this is now written into `.claude/rules/backend/api-endpoints.md`) and "don't change the actor mid-request" (Daga's idea). Lauta approved anyway.

  ### My answers

  **Q1: Contract.** Good. It follows the repo's API rules: one resource for all principals, repeated `?identifier=` params, `uuid` / `parent_uuid` instead of integer PKs, no embedded objects, and the standard `CursorPagination` envelope. It has the same Policy→Selector shape as `HotelAccessPolicy`. Nits:
  - `Portfolio.identifier` has no unique constraint in the DB. A filter on one identifier can return more than one row, so the application-create consumer must treat "more than one" as a real outcome, not only 0 or 1.
  - The `identifier` filter is case-insensitive, but the `ApplicationPrincipal` scope matches exactly (`identifier=portfolio_identifier`). An application whose record says `Demo` sees nothing. Pick one rule.
  - If the boundary portfolio is deleted mid-pagination, the next page is a 400 and the client must restart. That's acceptable, but document it.

  **Q2: Object shape.** Fine as is. On `types`: `PortfolioType` is a closed `TextChoices` with 7 members (parent_brand, brand, msa, management_company, above_property_dashboard, sso_organization, ad_hoc), and `(portfolio, type)` has a unique constraint. So there are at most 7 per portfolio, which is well inside Jordan's own "< 50 → array on the object" rule. Recommend adding `types: list[str]` now or as a quick follow-up. It needs a `prefetch_related("type_assignments")`, which makes the "page after a cursor is one query" test into 2.

  **Q3: Table vs enum. This is the most important question and it isn't settled.**
  - The ID-79 ticket explicitly rejected a region-local Postgres lookup as "regionally wrong", because applications are global Dynamo rows. The PR now reads exactly that regional table, and the ticket text still says "enum-backed / InternalServiceGatekeeper only / no uuid". The ticket and the PR contradict each other.
  - `ApplicationService.create` (`api_gateway/services/application_service.py:117-135`) documents `portfolio_identifier` as "cross-region-stable". For staging applications it requires a `Portfolio.Identifier` enum member so the authz check can resolve the portfolio in every region (ENT-6687).
  - Consequences if identity-service validates against one region's table:
    - A free-form identifier that exists only in the region called is accepted, even when the application's authz must resolve elsewhere.
    - A portfolio onboarded in another region is rejected.
  - My view: the table is the right answer to "does this exist in region X", and the enum alone is incomplete (it misses the `internal_*` portfolios and regional above-property portfolios). But the consumer must keep the staging enum guard, and must say which region it validates against. And ID-79 should be updated so the rejected option doesn't come back unannounced.

  ### Main concern: the UserPrincipal scope (not raised on the PR yet)
  The user scope is "portfolios of hotels they belong to", and the PR "Why" says this user-scoped read "doubles as the authorization check". Three problems:
  1. **Visibility.** The scope ignores the existing rule `Portfolio.PUBLIC_PORTFOLIO_IDENTIFIERS`: "membership should be visible to end users" only for public portfolios. That rule is used by `PortfolioService.get_public_portfolio_identifiers` and `hotel_staff/services/user_assignment_operation.py:42`. With this PR, a hotel user would also see `BW_DEACTIVATED`, `wyndham_deactivated`, `crestline_payroll`, `epd_test_portfolio`, `user_created_demos`, `internal_*`, and ad-hoc / above-property portfolios. This is concrete evidence for Lauta's "some may not be meant for customer eyes".
  2. **Being able to see a portfolio doesn't mean you have authority over it.** A user at one Wyndham hotel can see the `wyndham` portfolio. If "create application" treats "visible" as "allowed", that user can create an application owning the whole portfolio, and `HotelAccessPolicy` would then give it every hotel in the portfolio. The create flow needs its own permission check; this read must not stand in for one.
  3. **Wrong users rejected.** If the person who clicks "create application" is a Canary employee, they usually have no `CompanyHotelUser` rows for the customer's hotels. The actor-preserving call returns an empty list, so a real identifier looks invalid.

  Other code details look fine: cursor subquery scoped to the caller, `ServerError` fallthrough, `.distinct()` on the membership join, and `PortfolioHotel` / `CompanyHotelUser` have no soft-delete, so no stale rows leak. I didn't run the tests locally; CI passed them.

  ### Draft PR comment (NOT posted; needs your OK)
  > Nice, clean building block — contract/shape LGTM. Answers to the questions you had at the top:
  > **Shape / types:** `PortfolioType` is a closed 7-value enum with a (portfolio, type) unique constraint, so bounded — an array on the object fits your <50 rule. Happy for it to be a follow-up (it'll need a prefetch).
  > **Table vs enum:** table is right for "does it exist in this region", but ID-79 still says region-local was rejected, and `ApplicationService.create` keeps staging `portfolio_identifier` enum-only for cross-region authz (ENT-6687). Can the consumer PR keep that guard and say which region it validates against? Worth updating ID-79 so the ticket matches the PR.
  > **UserPrincipal scope — two things before this becomes the create-application check:**
  > 1. Users currently see every portfolio their hotels are in, including deactivated/internal/payroll/test ones. We already codify end-user visibility as `Portfolio.PUBLIC_PORTFOLIO_IDENTIFIERS` (`PortfolioService.get_public_portfolio_identifiers`) — should the user branch filter on that (or on types)?
  > 2. Seeing a portfolio isn't authority over it: a user at one Wyndham hotel sees `wyndham`. Please make sure application-create does its own permission check rather than relying on this read — and if the clicker is a Canary employee with no CompanyHotelUser rows, this scope returns nothing.
  > Nit: identifier filter is case-insensitive but the ApplicationPrincipal scope is exact-match; and `identifier` isn't unique in the DB, so a filter can return >1 row.

  **Suggested next step:** decide whether to post the comment above (or send a shorter version in the Slack thread). The only point I'd call important is the UserPrincipal visibility/authority concern, and the PR is already approved, so it's worth raising before merge.

  ## Agent run 2026-09-11 (follow-up): what one Wyndham hotel's staff could see, from Snowflake
  Source: Snowflake `CANARY_RAW.CANARY.HOTELS_PORTFOLIO` and `HOTELS_PORTFOLIOHOTEL`, read-only. The CDC mirror has duplicate rows, so each table is deduped to the latest row per id, with CDC-deleted rows dropped. This models the PR's user scope: the portfolios of every hotel the user is a member of, with no role or public/private check. The user is a member of one hotel in `wyndham`.

  **US: 6,609 hotels in `wyndham`.** Number of portfolios such a user would see:
  - 1,293 hotels: 1 portfolio
  - 389 hotels: 2
  - 3,050 hotels: 3
  - 1,810 hotels: 4
  - 67 hotels: 5–10. The worst case is hotel 5495 with 10.
  - 113 hotels would also show portfolios with no identifier.

  The typical set is `wyndham`, `wyndham_connect_gms`, `wyndham_connect_international` and sometimes `wyndham_connect_plus`. These are all in `PUBLIC_PORTFOLIO_IDENTIFIERS`, so seeing them is OK. The problem is authority: `wyndham` covers 6,609 hotels.

  Reachable portfolios that aren't public, or belong to other brands. Counts are the number of Wyndham hotels that reach it, then the portfolio's total hotels:
  - `BW`: 1 Wyndham hotel reaches it; 1,644 hotels, 1,643 of them not Wyndham
  - `marriott`: 3; 1,032 total
  - `marriott_upsells`: 3; 1,022 total
  - `drury`: 8; 153 total
  - `aimbridge`: 1; 117 total
  - `pyramid`: 1; 105 total
  - `IMM`: 2; 96 total
  - `wyndham_deactivated`: 367; 379 total
  - `wyndham_latam` (132), "Wyndham UAT properties", "Wyndham Compendium (Temporary)", "Corp Portal Portfolio", "Integrations view portfolio"
  - About 40 personal "<Full Name>'s Portfolio" portfolios (up to 179 hotels each) and several management-company portfolios with no identifier. Their names expose staff names to any front-line user at a member hotel.

  **EU:** 1,661 hotels in any `wyndham*` portfolio, of which 1,439 are in `wyndham_deactivated`; at most 5 portfolios per hotel. Also reachable: "Wyndham EMEA (DO NOT USE)" and "UAT Properties", both with no identifier. **AP:** no Wyndham portfolios.

  **What this means:** for listing, most Wyndham users see only public Wyndham portfolios. The outliers expose deactivated, internal and personal portfolios, plus other brands' portfolios. Suppose application-create treats "visible" as "allowed". Then a clerk at an ordinary Wyndham hotel could create an application covering 6,609 hotels. A clerk at the one Wyndham hotel that is also in BW could get 1,643 Best Western hotels, and at one of the 3 Marriott-overlap hotels, about 1,030 Marriott hotels.
project: 2026-04-16T1210-unblock-team
source_id: https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1788992960326799
tags:
- morning-gtd
- slack
- from-awareness
time_minutes: 5
title: 'Review #epd-enterprise: Jordan Sterling: PR #55537 general-purpose list-portfolios
  API, questions to the pod at the top of the PR'
updated: 2026-09-11 15:00:59.451393
waiting_on: null
waiting_since: null
working_on: false
---

Promoted from the 2026-09-10 awareness report (Slack highlights).
https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1788992960326799