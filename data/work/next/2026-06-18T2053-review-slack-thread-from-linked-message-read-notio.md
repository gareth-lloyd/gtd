---
area: null
contexts: []
created: 2026-06-18 20:53:30.511699
defer_until: null
due: 2026-06-23
energy: medium
id: 2026-06-18T2053-review-slack-thread-from-linked-message-read-notio
order: null
output: |
  # Portfolios -> global: review, domain map, and proposed ticket plan
  Last updated 2026-06-22. Sources: Jordan Sterling DM (Slack D07HCMQU5FY) — linked msg +
  full thread; the private Notion "Canary Identity & Auth — Landscape Brief"
  (https://www.notion.so/canarytechnologies/Canary-Identity-Auth-Landscape-Brief-Private-377814686151819fa8a7e17b373bf5c6).
  Grounded against backend/canary and the existing Linear ticket series. No external writes
  performed in any run.

  ## What Jordan asked for (June 18 DM thread)
  Linked msg: "we need to take portfolios global. different uuids across regions sucks"
  (https://canarytechnologies.slack.com/archives/D07HCMQU5FY/p1781758493678979). Across the
  thread he lays out a 4-part ask and wants tickets made:
  1. Move `Portfolio.Identifier` from a hardcoded Python enum -> open / table-backed (so
     identifiers aren't capped at the ~50 defined values).
  2. Give ALL portfolios a global identifier ("you make them globally anyway. and add
     identifier to all").
  3. Put portfolios in the global DynamoDB registry + build APIs for them. <- the task headline.
  4. Fix the "bad tickets" that put portfolio *uuid* (region-local) on the global applications
     table — should reference the portfolio *identifier* (global/stable) instead.

  ## The domain in plain terms (the why)
  - Canary runs as separate regional deployments, each with its OWN Postgres. A brand like
    Wyndham exists as a different row, with a different `uuid`, in each region. Nothing is
    shared between regions at the Postgres layer.
  - `uuid` = a region-local handle: unique, but meaningless in another region ("update folder
    #8472" makes no sense to a region that doesn't have #8472). `identifier` = a stable shared
    name (`WYNDHAM`) that means the same thing everywhere. Today only ~50 named portfolios
    have an identifier; the rest are null.
  - To share state across regions, Canary uses global DynamoDB tables (AWS-replicated). The
    pattern: store a stable key + the owning region + the region-local uuid. Two such tables
    already exist — `hotel-slug-routing` (slug -> region + hotel_uuid) and `applications`
    (keyed by sid; currently carries portfolio_uuid).
  - "Take portfolios global" therefore means: give every portfolio a stable identifier,
    publish portfolios into a global registry table keyed by identifier, expose APIs over it,
    and make applications reference the identifier instead of the region-local uuid.

  ## The routing tension and how it resolves
  - To ACT on a portfolio by identifier (get / create / update-by-id), the system must know
    which region owns it — so one identifier must map to exactly one owning region. This was
    Gareth's concern in the thread ("would not work for routing").
  - Jordan wants the identifier to be a global ACCESS concept — enforce "this user can see all
    of Wyndham" across regions ("yea why not. thats the whole point of this").
  - These reconcile, and the live `hotel-slug-routing` table already proves it: a slug is BOTH
    globally resolvable (anyone, any region, can look it up) AND region-pinned (it resolves to
    exactly one owning region, with a conflict guard preventing two regions claiming the same
    key). Global visibility != multi-region implementations.
  - => Recommendation: model the portfolio identifier as a region-pinned, globally-resolvable
    slug — a near 1:1 copy of `hotel-slug-routing` (proven in production).
  - The one genuine open question: a brand like Wyndham really does operate in several regions.
    Region-pinning means the global record names ONE home region as owner, with the other
    regions' hotels rolling up under it. That "pick a home region" simplification is the real
    decision under the whole thing and needs Jordan's blessing.

  ## Verified current state (as of 2026-06-22)
  - NO existing "portfolio global dynamo / registry" ticket — searched Linear. Only hits are
    the region-local Above-Property portfolio API series (ENT-1820..1825, done 2024) and the
    application-uuid series. This is greenfield.
  - In-flight application-uuid series — all still In Review, none merged:
    - ENT-6373 applications list endpoint w/ portfolio_uuid filter — PR
      https://github.com/canary-technologies-corp/canary/pull/48214
    - ENT-6374 backfill portfolio_uuid on existing rows
    - ENT-6375 promote portfolio_uuid to required — PR
      https://github.com/canary-technologies-corp/canary/pull/48220
  - Deployed: ENT-6372 (create accepts portfolio_uuid), ENT-6177 (staging credentials scoped
    off ApplicationRecord.portfolio_uuid; decision 2026-05-29). So portfolio_uuid is live +
    load-bearing — part-4 is a migration, not a rename, but it's still catchable because the
    In-Review PRs have not merged.
  - Adjacent: ENT-6398 "Canary admin pages for applications" (Backlog,
    https://linear.app/canary-technologies/issue/ENT-6398) — a consumer of these APIs, not a
    dependency.

  ## Key code references (backend/canary)
  - Portfolio model + `Identifier` enum (~50 TextChoices) + unique-partial constraint:
    hotels/models/portfolio.py (enum ~21-78; constraint ~199).
  - Identifier lookup: portfolios/services/portfolio.py `get_portfolio_by_identifier`.
  - The precedent that templates the entire registry:
    - hotels/management/commands/sync_hotel_slugs_to_dynamodb.py — batch backfill + region
      conflict guard (skip-if-owned-elsewhere unless --force-overwrite).
    - hotels/services/hotel_slug_routing.py — post_save signal upsert; fail-open reads.
    - api_gateway/selectors/api_gateway_dynamo_db_selector.py — hotel_slug_routing accessor;
      applications GSI `portfolio_uuid-created_at-index`.
    - settings: HOTEL_SLUG_ROUTING_TABLE, GLOBAL_PUBLIC_API_DYNAMODB_ENDPOINT_URL.
  - Applications record + GSI: shared/aws/public_api_dynamo_db.py (ApplicationRecord carries
    portfolio_uuid); api_gateway/services/application_service.py.

  ## Notion brief connection
  The "Canary Identity & Auth — Landscape Brief" frames the wider program: opaque IdentitySid
  spine, global DynamoDB, OAuth (shipped), and "applications are portfolio-owned." Portfolio-
  global is the access-control substrate beneath "application owned by portfolio" — which is
  exactly why the uuid-vs-identifier choice matters for enforcing access across regions.
  Owners: Jordan (Public API spine), Andrea Bradshaw (OAuth global login / cross-region login),
  Joshua Hart (audit / permission edges), Daga (identity gatekeeper).

  ## Proposed ticket plan (~12 tickets, 4 stacked phases)
  Mirrors Jordan's stacked-isolated style (cf. ENT-6371..6376). Suggested home: a new "Global
  Portfolio Registry" project under the Identity/Auth initiative, or fold into the existing
  "Api Authentication" project (ab6b9cb6-9414-440a-a6d5-e4ba3232c586).

  Phase A — make the identifier a real, universal field (Jordan asks 1+2)
  - A1 Decouple Portfolio.identifier from the hardcoded enum -> open validated slug (keep
    format + unique-partial constraint). Migration. [hotels/models/portfolio.py:21-78,199]
  - A2 Identifier generation + idempotent backfill: every portfolio gets a stable identifier
    (named ones keep their name; the rest auto-generate one).
  - A3 Promote identifier to NOT NULL / required at create. Depends A1,A2. (pattern = ENT-6375)

  Phase B — global registry table + sync (Jordan ask 3, storage)
  - B1 Create `portfolio-registry` global DynamoDB table + selector accessor. PK identifier;
    attrs region, portfolio_uuid, name, parent_identifier, status, updated_at. New setting
    PORTFOLIO_REGISTRY_TABLE. (pattern = hotel-slug-routing table + ENT-6371)
  - B2 Sync portfolios -> registry: post_save signal upsert w/ cross-region conflict guard +
    idempotent backfill command; fail-open reads. Depends A3, B1.

  Phase C — portfolio APIs over the registry (Jordan ask 3, APIs; the task headline)
  - C1 Selector + service: resolve portfolio by identifier (get + list), cross-region. Dep B1.
  - C2 GET /v1/portfolios/{identifier} + GET /v1/portfolios (list, cursor pagination,
    InternalServiceAuthValidator). Depends C1. (pattern = ENT-6373)
  - C3 POST /v1/portfolios (create region-pinned + register globally; identifier required +
    globally unique, 409 on cross-region collision). Depends C1, A3. (pattern = ENT-6376/OK-310)
  - C4 (DEFER) update + membership endpoints — follow-up, not in the first slice.

  Phase D — repoint applications portfolio_uuid -> portfolio_identifier (Jordan ask 4, the
  "bad tickets")
  - D1 Add portfolio_identifier attr + GSI to applications; dual-write w/ portfolio_uuid.
    (additive; pattern = ENT-6371)
  - D2 Backfill portfolio_identifier on existing application rows. (pattern = ENT-6374)
  - D3 Switch reads/filters to identifier (repoint ENT-6373 list filter + ENT-6177 staging-
    credential scoping); retire portfolio_uuid. (pattern = ENT-6375)

  Sequencing: A -> B -> C -> D. A + B are the foundation, C is the headline deliverable, D is
  a separate migration epic that collides with in-review work.

  ## Open decisions (raised interactively; unresolved)
  1. Routing model — recommend region-pinned slug; needs the "pick a home region"
     simplification blessed (Jordan's call).
  2. In-flight uuid PRs (ENT-6373/74/75, In Review): let them land + do Phase D as a follow-on
     migration (recommended) vs redirect them to identifier before merge. Time-sensitive.
  3. What to create now: full ticket set / a single design+decision ticket for Jordan to
     ratify / hold as local draft.

  ## Status
  Reviewed (Slack + Notion), domain mapped, routing tension resolved against the live
  hotel-slug-routing precedent, full ticket plan drafted, current state re-verified. No Linear
  writes performed — awaiting the decisions above before creating anything.

  ## Agent run 2026-06-23T09:50

  Read the newer DMs + the team thread; the picture firmed up and I wrote the design note.

  ### New since last run
  - Team thread 2026-06-22 22:20 (Jordan + Andrea + Ryan + Gareth):
    https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1782156026162049
    Consensus on the apps fix (add portfolio_identifier, remove portfolio_uuid, backfill).
    Ryan wants to execute it ("start using pre-production functionality pretty soon").
    Andrea: "identifier is the only thing currently guaranteed to be consistent across
    regions." Jordan: the global portfolio table "might just be a list of portfolio
    identifiers and some basic metadata." Gareth committed publicly to writing the eng
    design + tickets.
  - Membership: Jordan + Gareth aligned it stays REGIONAL (Postgres). Jordan: "i haven't
    found a use case for global portfolio membership." Enforcement is hotel-anchored ->
    regional; the EU-cannot-call-US constraint kills the call-home alternative. The one
    named boundary is cross-region AGGREGATION (out of scope).
  - Backfill sheet read (https://docs.google.com/spreadsheets/d/1XAkZRz5Oqqw-_0HtuZChjf5hNRjE7XEHJSpcG0wB2IM):
    ~42 apps, ONLY 2 have a portfolio_uuid -> the backfill is ownership-assignment, not
    uuid->identifier translation. Real customer apps are the multi-region brands
    (IHG x4, Wyndham x2, Best Western x1) + 2 partners (Zendesk, HotelEngine); ~31 are
    internal Canary test/infra apps (-> one CANARY_INTERNAL owner); several are deletable
    junk. Confirms "the cross-region problem is a few brands, not all portfolios."

  ### Deliverable written
  Design note: backend/canary/tmp/investigations/portfolios-global-identifier-design.md
  Contains: tight problem/solution, why-identifier-not-uuid, the few-brands grounding,
  membership-regional decision, current-state + ENT-637x table, and the sequenced ticket
  plan T1-T8 + deferred, plus a proposed backfill owner-mapping table and the 4 decisions
  needed from Jordan.

  ### Final ticket sequence (in the doc)
  - T1 (coord) stop extending portfolio_uuid; cancel ENT-6374/6375, repoint ENT-6373.
  - T2 ensure app-owning portfolios have identifiers (+ create CANARY_INTERNAL).
  - T3 (parallel, non-blocking) decouple identifier from the enum.
  - T4 add portfolio_identifier attr+GSI to applications (dual-write).
  - T5 backfill from curated owner map; delete junk. [URGENT path: T2+T4+T5 unblocks pre-prod]
  - T6 switch reads/filters to identifier; drop portfolio_uuid.
  - T7 create portfolio-registry global dynamo table.
  - T8 sync portfolios -> registry (signal + backfill, region conflict guard).
  - Deferred: registry CRUD APIs; global membership; universal identifier backfill.

  ### Status
  Design note written locally. No Linear writes, no Slack messages sent. Next: on the go-
  ahead, draft full Linear-ready bodies for T1-T8 and/or share the note with Jordan. The
  4 open decisions (membership regional; cancel 6374/6375; partner-app ownership; registry
  now-vs-later) are Jordan/team calls.
project: 2026-04-10T0840-ticket
source_id: null
tags: []
time_minutes: 30
title: REview slack thread from linked message. read notion doc. interactively explore
  this work
updated: 2026-06-23 13:34:34.706736
waiting_on: null
waiting_since: null
working_on: true
---

"Create Linear tickets: portfolios in the global dynamo + APIs for them"

https://canarytechnologies.slack.com/archives/D07HCMQU5FY/p1781758493678979

Read https://www.notion.so/canarytechnologies/Canary-Identity-Auth-Landscape-Brief-Private-377814686151819fa8a7e17b373bf5c6?source=copy_link