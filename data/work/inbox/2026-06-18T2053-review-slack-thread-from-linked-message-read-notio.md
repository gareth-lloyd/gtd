---
area: null
contexts: []
created: 2026-06-18 20:53:30.511699
defer_until: null
due: null
energy: low
id: 2026-06-18T2053-review-slack-thread-from-linked-message-read-notio
order: null
output: |
  ## Agent run 2026-06-18T21:10

  Reviewed the full recent DM history with Jordan Sterling (Slack DM D07HCMQU5FY,
  not just the linked message) and read the private Notion brief
  "Canary Identity & Auth — Landscape Brief"
  (https://www.notion.so/canarytechnologies/Canary-Identity-Auth-Landscape-Brief-Private-377814686151819fa8a7e17b373bf5c6).
  Grounded both against the codebase and the existing Linear ticket series.

  ### What Jordan is actually asking for (June 18 thread)
  Linked msg: "we need to take portfolios global. different uuids across regions sucks"
  (https://canarytechnologies.slack.com/archives/D07HCMQU5FY/p1781758493678979).
  Across the thread he lays out a 4-part ask and asks me/Enterprise to "make tickets":
  1. Move `Portfolio.Identifier` from a hardcoded Python enum -> a table (so identifiers
     aren't limited to the ~50 defined subset).
  2. Give ALL portfolios a global identifier ("you make them globally anyway. and add
     identifier to all").
  3. Put portfolios in the global DynamoDB registry + build APIs for them
     ("we need portfolios to live in the global dynamo and need apis for them").
  4. Fix the "bad tickets" that put portfolio *uuid* (region-local) on the application
     table — should reference portfolio *identifier* (global/stable) instead.

  ### The "bad tickets" he means (already shipped / in flight — not greenfield)
  Series under Linear projects "Api Authentication" + "Configure Pre-Prod for Wyndham":
  - ENT-6371 add portfolio_uuid attr + GSI to applications DynamoDB — DEPLOYED
    (https://linear.app/canary-technologies/issue/ENT-6371)
  - ENT-6372 ApplicationService.create accepts portfolio_uuid required — DEPLOYED
    (https://linear.app/canary-technologies/issue/ENT-6372)
  - ENT-6373 applications list endpoint w/ portfolio_uuid filter — IN REVIEW
    (https://linear.app/canary-technologies/issue/ENT-6373)
  - ENT-6374 backfill portfolio_uuid on existing rows — IN REVIEW
    (https://linear.app/canary-technologies/issue/ENT-6374)
  - ENT-6375 promote portfolio_uuid to required on ApplicationRecord — IN REVIEW
    (https://linear.app/canary-technologies/issue/ENT-6375)
  - ENT-6376 POST /v1/Applications (portfolio_uuid required) — IN REVIEW
    (https://linear.app/canary-technologies/issue/ENT-6376)
  Caveat: ENT-6177 (DEPLOYED) already scopes staging credentials off
  ApplicationRecord.portfolio_uuid (decision 2026-05-29). So portfolio_uuid is
  load-bearing in a live global table + GSI — a swap to identifier is a migration,
  not a rename.

  ### Current state in code (backend/canary)
  - `Portfolio.Identifier` enum: hotels/models/portfolio.py:21-78 — Django TextChoices,
    ~50 values (WYNDHAM, IHG, BEST_WESTERN, ...). Unique partial constraint on
    portfolio.identifier (portfolio.py:199). Most portfolios have identifier=None.
  - `Portfolio` model (hotels app): int PK `id` + unique `uuid`; nullable `identifier`;
    M2M to Hotel via PortfolioHotel; self-FK `parent`. NO region field — but the uuid is
    region-local because the row lives in region-local Postgres.
  - Lookup: PortfolioService.get_portfolio_by_identifier (portfolios/services/portfolio.py).
  - `ApplicationRecord.portfolio_uuid`: api_gateway/services/application_service.py;
    stored in GLOBAL DynamoDB (GLOBAL_PUBLIC_API_DYNAMODB_ENDPOINT_URL) — hence the
    region-local-uuid-in-a-global-table smell.
  - Cross-region precedent that already works: `hotel-slug-routing` global DynamoDB table
    (sync_hotel_slugs_to_dynamodb.py) maps slug -> owning region + hotel_uuid, with
    conflict-avoidance so two regions can't claim the same slug. A portfolio registry
    could follow this 1:1 (identifier -> one owning region) pattern.

  ### The real unresolved decision (routing)
  Jordan: "i think you make them globally anyway... portfolio references and membership
  probably has to be a global item to enforce access globally." Gareth flagged the catch:
  "Will it be possible for portfolios in multiple regions to point to the same identifier?
  ... Would not work for routing." Jordan: "yea why not. thats the whole point of this."
  -> This conflates two things:
    (a) identifier as a ROUTING key — must be 1:1 with a region for get/create/update-by-id
        (same constraint Jordan himself stated 2026-03-27: write ops must indicate region).
    (b) identifier as a global ACCESS-CONTROL / membership concept — legitimately spans
        regions.
  A single global identifier mapping to multiple region-local portfolio impls breaks (a).
  This is THE decision to lock before writing tickets: is a global portfolio identifier
  region-pinned (slug-style, routable) or a region-spanning grouping (needs a different
  routing story)? Also unresolved: single-region hotel groups (Gareth) — Jordan says give
  them a global ref anyway ("no harm in a global reference that only has an impl in one
  region").

  ### Notion brief connection
  The brief frames the whole Identity/Auth program: opaque IdentitySid spine, global
  DynamoDB, OAuth (shipped), and "applications are portfolio-owned." Internal
  service-to-service trust is the acknowledged soft spot (Securing Caller Identity
  proposal). Portfolio-global is the access-control substrate under "application owned by
  portfolio" — it's why the uuid-vs-identifier choice matters for enforcing access across
  regions. Owners: Jordan (Public API spine), Andrea Bradshaw (OAuth Global Login /
  cross-region login), Joshua Hart (audit/permission edges), Daga (identity gatekeeper).

  ### Status / next step
  Exploration done; no tickets created (external writes need explicit approval). Presented
  synthesis to user and asked for direction (draft ticket set locally vs. nail the routing
  decision vs. pull related design docs). Awaiting user steer.

  ## Agent run 2026-06-22T14:53:05

  Re-ran to advance toward ticket creation. Verified the moving facts, resolved the routing
  question against a live precedent, and drafted the full ticket set. No external writes —
  surfaced the gating decisions for sign-off.

  ### Verification (since 2026-06-19)
  - In-flight uuid series UNCHANGED, all still **In Review**: ENT-6373 (list endpoint, PR
    https://github.com/canary-technologies-corp/canary/pull/48214), ENT-6374 (backfill),
    ENT-6375 (promote-to-required, PR
    https://github.com/canary-technologies-corp/canary/pull/48220). ENT-6372 + ENT-6177
    Deployed. None merged yet -> part-4 ("bad tickets") is still catchable before
    portfolio_uuid fully cements.
  - **No existing "portfolio global dynamo / registry" ticket exists** — searched Linear;
    only hits are the region-local Above-Property portfolio API series (ENT-1820..1825, done
    2024) and the application-uuid series. This is greenfield.
  - Adjacent ticket: ENT-6398 "Canary admin pages for applications" (Backlog, OAuth Global
    Login project, https://linear.app/canary-technologies/issue/ENT-6398) — a consumer of
    the same APIs, not a dependency.

  ### Routing question — RESOLVED by precedent
  Prior run's open question (is a global identifier region-pinned/routable, or
  region-spanning?) is answered by the live `hotel-slug-routing` global DynamoDB table:
  - Keyed on a stable string (`slug`); attrs `region`, `hotel_uuid`, `is_current`,
    `updated_at`. post_save signal + `sync_hotel_slugs_to_dynamodb.py` upsert per-item,
    stamping the OWNING region, with a conflict guard that SKIPS the write if the key is
    already owned by another region (unless `--force-overwrite`). Reader resolves slug ->
    region + uuid; fail-open on dynamo error.
  - cites: hotels/management/commands/sync_hotel_slugs_to_dynamodb.py;
    hotels/services/hotel_slug_routing.py; api_gateway/selectors/
    api_gateway_dynamo_db_selector.py (hotel_slug_routing accessor); setting
    HOTEL_SLUG_ROUTING_TABLE; applications GSI portfolio_uuid-created_at-index in
    shared/aws/public_api_dynamo_db.py.
  => Model the global portfolio **identifier** as region-pinned-and-routable (slug-style:
  1 identifier -> exactly 1 owning region, conflict-avoided). The "spans regions for access
  control" need is met by the identifier being globally *resolvable*, not by one identifier
  having impls in many regions. The registry is a near 1:1 copy of hotel-slug-routing.

  ### Proposed ticket set (4 workstreams, ~12 tickets) — DRAFT, NOT created
  Mirrors Jordan's stacked-isolated-ticket style (cf. ENT-6371..6376). Suggest a new Linear
  project "Global Portfolio Registry" under the Identity/Auth initiative, or fold into the
  existing "Api Authentication" project (ab6b9cb6-9414-440a-a6d5-e4ba3232c586).

  A. Identifier becomes a real, universal field (Jordan asks 1+2)
  - A1 Decouple Portfolio.identifier from the hardcoded TextChoices enum -> free-form slug
    (keep format + unique-partial constraint). Migration. [hotels/models/portfolio.py:21-78,199]
  - A2 Identifier generation + backfill: every portfolio gets a stable global identifier
    (named ones keep their name; rest auto-gen a stable slug). Idempotent backfill command.
  - A3 Promote identifier to NOT NULL / required at create (PortfolioService.create
    generates it). Depends A1,A2. (pattern = ENT-6375)

  B. Global registry table + sync (Jordan ask 3 — storage)
  - B1 Create `portfolio-registry` global DynamoDB table + selector accessor. PK
    `identifier`; attrs region, portfolio_uuid, name, parent_identifier, status, updated_at.
    New setting PORTFOLIO_REGISTRY_TABLE; global endpoint. No data yet.
    (pattern = hotel-slug-routing table + ENT-6371)
  - B2 Sync portfolios -> registry: Portfolio post_save signal upsert w/ cross-region
    conflict guard + idempotent backfill command. Fail-open reads. Depends A3, B1.

  C. Portfolio APIs over the registry (Jordan ask 3 — APIs; the GTD task headline)
  - C1 Selector+service: resolve portfolio by identifier from registry (get + list),
    cross-region. PortfolioRegistryService. Depends B1.
  - C2 HTTP GET /v1/portfolios/{identifier} + GET /v1/portfolios (list, cursor pagination,
    InternalServiceAuthValidator). Depends C1. (pattern = ENT-6373)
  - C3 HTTP POST /v1/portfolios (create region-pinned + register globally; identifier
    required + globally unique, 409 on cross-region collision). Depends C1, A3.
    (pattern = ENT-6376 / OK-310)
  - C4 (DEFER) PATCH/update + membership endpoints — flag as follow-up, not in first slice.

  D. Repoint applications portfolio_uuid -> portfolio_identifier (Jordan ask 4 — "fix the
  bad tickets")
  - D1 Add portfolio_identifier attr + GSI to applications; dual-write w/ portfolio_uuid.
    (additive; pattern = ENT-6371)
  - D2 Backfill portfolio_identifier on existing application rows (resolve via uuid ->
    registry). (pattern = ENT-6374)
  - D3 Switch reads/filters to portfolio_identifier: repoint ENT-6373 list filter + ENT-6177
    staging-credential scoping; then retire portfolio_uuid. (pattern = ENT-6375)

  ### Open decisions (asked interactively this session)
  1. Routing model — recommend region-pinned slug (above).
  2. In-flight uuid tickets (ENT-6373/74/75, all In Review, NOT merged): let them land and
     do workstream D as a follow-on migration, vs redirect them now to identifier before
     merge. Time-sensitive.
  3. What to produce now: full ticket set in Linear / just a design+decision ticket for
     Jordan to ratify / hold as local draft.

  ### Status
  Verified + routing resolved + full ticket set drafted. No Linear writes performed (await
  explicit approval per rules). Awaiting answers to the 3 decisions; on approval I create
  the chosen scope.
project: null
source_id: null
tags: []
time_minutes: 5
title: REview slack thread from linked message. read notion doc. interactively explore
  this work
updated: 2026-06-22 14:53:05.000000
waiting_on: null
waiting_since: null
working_on: true
---

"Create Linear tickets: portfolios in the global dynamo + APIs for them"

https://canarytechnologies.slack.com/archives/D07HCMQU5FY/p1781758493678979

Read https://www.notion.so/canarytechnologies/Canary-Identity-Auth-Landscape-Brief-Private-377814686151819fa8a7e17b373bf5c6?source=copy_link