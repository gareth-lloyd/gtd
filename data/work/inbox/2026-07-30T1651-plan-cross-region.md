---
area: null
contexts: []
created: 2026-07-30 16:51:23.289273
defer_until: null
due: null
energy: low
id: 2026-07-30T1651-plan-cross-region
order: null
output: |
  ## Agent run 2026-07-31T13:15:00+01:00

  Plan for the Cross-Region property selector: an admin logged into one region sees
  their hotels from the other regions in the main hotel dropdown on /hotels, with
  links out to those regions. Data source: Trino federating the three regional
  Snowflake accounts (per the task note). Research: Bear notes had nothing on this;
  context below comes from the codebase, Snowflake, Linear, and Notion.

  ### What already exists (leverage, don't build)

  - Trino IS deployed (Data Platform, on Kubernetes) and already connected across
    the three regional Snowflake accounts — confirmed in "Snowflake & DBT Access
    Request" (https://app.notion.com/p/3968146861518048b060c22ad4a7d0ed) and the
    completed PoC DATA-695 (https://linear.app/canary-technologies/issue/968769b7-bde4-40e6-9b43-f0222a9493a0).
    Nothing in the canary repo talks to it yet — client + creds + network path are new work.
  - Each regional Snowflake account has CANARY_RAW.CANARY, an Airbyte CDC mirror of
    that region's canary Postgres with everything the query needs: AUTH_USER,
    HOTELS_COMPANYHOTELUSER, HOTELS_HOTEL, HOTELS_USERPROFILE, portfolio +
    permission tables (verified live in us and eu; CDC lag is minutes).
  - Frontend already ships all three regions' base URLs in every build:
    VUE_APP_SITE_URL_{US,EU,AP} in frontend/packages/shared/constants/getRegionalConfigVar.ts
    (getRegion() at :232). Links out need zero new config.
  - The dropdown is frontend/packages/shared/components/HeaderDropdownHotel.vue,
    fed by GET /api/users/me (backend/canary/hotels/views/api/user/own_user.py:83,
    hotels list built in hotels/utils/api/serialize_user.py:216). Its portfolio
    branch (:225-234) already demonstrates plain <a href> entries — the exact
    pattern cross-region rows need (router-link won't cross origins).
  - Hotel slugs are already globally unique across regions, enforced via the
    hotel-slug-routing DynamoDB Global Table
    (backend/canary/hotels/services/hotel_slug_routing.py) — so a link target of
    ${SITE_URL_EU}/hotels/<slug>/ is unambiguous.
  - Region enum: backend/canary/canary/region.py (US/EU/APAC from AWS_REGION_NAME).

  ### Proposed design

  1. Backend: small TrinoConnectionService in backend/canary/data_warehouse
     (python `trino` client, read-only creds via settings, mirroring the existing
     SnowflakeConnectionService shape). One federated query keyed on the logged-in
     user's normalized email, UNION over the two remote regions' catalogs:
     AUTH_USER (lower(email) match) -> HOTELS_COMPANYHOTELUSER -> HOTELS_HOTEL
     (name, slug, uuid, is_active, is_customer), filtering _ab_cdc_deleted_at IS NULL.
  2. New endpoint /api/users/me/cross_region_hotels (Request Framework v2 via
     backend:write-api-view skill) — do NOT widen /api/users/me: Trino+Snowflake
     latency (seconds, warehouse cold starts) can't sit in the login-critical path,
     and serialize_user already has a flagged 6000-hotel Wyndham perf problem
     (serialize_user.py:141). Cache result per-user (Redis, ~24h TTL,
     stale-while-revalidate; fail silent to empty list). Dropdown fetches lazily
     on open.
  3. Frontend: an "Other regions" section at the bottom of HeaderDropdownHotel.vue
     — grouped by region, plain <a href> to ${SITE_URL_<REGION>}/hotels/<slug>/,
     capped at ~10 rows per region with a "+N more in EU" summary row (Wyndham-scale
     users). New analytics events alongside Header.HotelSelector.* in
     frontend/packages/shared/utilities/analytics/events/hotels.ts.
  4. Gating: feature flag, start with internal users + one pilot enterprise
     portfolio. Clicking a link lands on the other region's login (sessions are
     cookie-scoped per region-domain; no SSO handoff exists yet) — acceptable v1,
     and exactly what the Identity/Enterprise cross-region auth work will fix later.
  5. Identity matching v1 = case-insensitive email. Caveats: email isn't
     unique-constrained per region, and ID-2 "Audit: Duplicate users across
     regions" (https://linear.app/canary-technologies/issue/ID-2/audit-duplicate-users-across-regions)
     is still open — the Trino query is incidentally the perfect tool to run that
     audit during the spike. For SSO users, (sso_organization, sso_name_id) is the
     stronger key (unique-constrained, migration 0727) — v2.

  ### Phasing

  - Phase 0 (spike, 1-2d): get Trino endpoint/creds + network path from Data
    Platform (their k8s deployment; likely needs a DATA ticket); run the membership
    query for known cross-region users; measure latency; run the ID-2 dup audit as
    a by-product.
  - Phase 1: TrinoConnectionService + service + cached endpoint + flag.
  - Phase 2: dropdown section + links + analytics + empty/error states.
  - Phase 3: pilot rollout; follow-ups: SSO handoff, (sso_org, sso_name_id)
    matching, possibly replace the Trino lookup with a user-region DynamoDB global
    table if freshness/latency demands it.

  ### Tensions to resolve (flagged, not blockers)

  - The codebase's established pattern for exactly this shape of problem is a
    DynamoDB Global Table (used 3x: hotel-slug-routing, OTA routing, and the
    Identity team's in-flight global auth_user table — ID-11
    https://linear.app/canary-technologies/issue/ID-11/create-global-auth-user-table,
    backfill already done). Trino-over-Snowflake is fine for v1 given caching
    (minutes of CDC lag is acceptable for a selector), but the global auth_user
    table is the natural long-term home for "which regions does this user exist
    in" — design the service interface so the data source can be swapped.
  - This feature is a slice of Andrea Bradshaw's Enterprise project "Support
    cross-region Auth and Above Property Dashboards" (status: Product Definition,
    https://linear.app/canary-technologies/project/support-cross-region-auth-and-above-property-dashboards-da48fe9e2663)
    — sync with Andrea before building so the selector and the auth work don't
    diverge (their summary explicitly includes "corporate users can access
    property-level dashboards across regions from single URL").
  - GDPR: response data is hotel/company data (not personal), and the lookup key
    is the requesting user's own email — low risk, matches the metadata-only
    recommendation in the old "Cross-Region Federation Service" notes
    (https://app.notion.com/p/2f4814686151808fbfbbc561d918ebfd), but the
    EU-Snowflake-queried-from-US path should get a security-review nod.
  - Latent bug found en route: internal_support/services/zendesk_remote.py:3 maps
    EU to "eu-west-1" but the real EU region is eu-central-1 (region.py:21).
    Worth a drive-by ticket.

  Next actions if proceeding: (1) message Andrea re: project overlap, (2) DATA
  ticket for Trino access/creds from canary pods, (3) spike branch for the
  federated query. Drafted nothing external; no writes made anywhere.

  ## Agent run 2026-07-31T13:40:00+01:00

  On explicit request, published the PRD & feasibility piece as a private Notion
  page: "Cross-Region Property Selector — PRD & Feasibility"
  (https://app.notion.com/p/3ae81468615181a9a330df1533570c15). Brief/high-level:
  product goals, justification, UI thoughts (incl. external-site ↗ indicator),
  Trino-federated query strategy, feasibility table, open questions.
project: null
source_id: null
tags: []
time_minutes: 5
title: plan cross-region
updated: 2026-07-31 13:40:00.000000
waiting_on: null
waiting_since: null
working_on: false
---

- Cross-Region property selector
    - See my properties across regions
    - Link to other regions


Build against trino cross region snowflake