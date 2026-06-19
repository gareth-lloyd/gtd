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
project: null
source_id: null
tags: []
time_minutes: 5
title: REview slack thread from linked message. read notion doc. interactively explore
  this work
updated: 2026-06-18 21:10:00.000000
waiting_on: null
waiting_since: null
working_on: true
---

https://canarytechnologies.slack.com/archives/D07HCMQU5FY/p1781758493678979

Read https://www.notion.so/canarytechnologies/Canary-Identity-Auth-Landscape-Brief-Private-377814686151819fa8a7e17b373bf5c6?source=copy_link