---
area: null
contexts:
- react
created: 2026-05-14 10:01:39.210950
defer_until: null
due: 2026-05-14
energy: medium
id: 2026-05-14T1001-skim-jordan-s-oauth-applicationservice-refactor-ti
order: null
output: '## Agent run 2026-05-14T13:05:00


  ### TL;DR for the DM

  These are Jordan''s "second part" — pure service-layer plumbing in `backend/canary/api_gateway/`
  that the OAuth work will sit on top of. Three are In Review (6209/6210/6211), one
  is still Todo (6212). All are small, well-scoped, single-author. None of this is
  on the login-page critical path — it''s the foundation for the portfolio-owned Application
  Update API (ENT-6208), which is itself in the looser-deadline OAuth Global Login
  project.


  ### Project split

  - **Api Authentication** project (these four tickets): the CRUD layer refactor on
  `ApplicationService`. Backed by DynamoDB (`ApplicationRecord` is a `msgspec.Struct`,
  not a Django model).

  - **OAuth Global Login** project: ENT-6204 login page (your team''s part), ENT-6205
  code exchange, ENT-6208 Application Update API endpoint. ENT-6212 is the bridge
  — it lives in Api Authentication but is the prerequisite for ENT-6208.


  ### Ticket-by-ticket


  - **ENT-6209** — In Review, PR #45448. Rename `ApplicationCredentialService` → `ApplicationService`
  (file + class). Introduces an `Application` domain dataclass (typed sid, `ApplicationStatus`
  enum, `datetime`, `UUID`) layered above the flat-string DAL `ApplicationRecord`;
  service owns the converter both ways. Splits today''s all-in-one `create_application()`
  into three composable calls — `ApplicationService.create()` writes only the row,
  with `IdentityService.create()` and `AuthTokenService.create_token()` composed at
  the caller. Only one existing caller (a management command). Pure refactor, end
  state identical.


  - **ENT-6210** — In Review, PR #45449. `ApplicationService.get(sid) -> Application
  | None`. Coalesces Dynamo "not found" into `None`. Deliberately does **not** filter
  soft-deleted — `deleted_at` is returned populated; caller filters.


  - **ENT-6211** — In Review, PR #45450. `ApplicationService.update()` for `name`
  and `status` only. Partial-update style (`None` = don''t touch). Validates `len(new_name)
  ≤ 200` (empty string allowed). No-op detection: if diff is empty, skip the PutItem
  and don''t bump `updated_at`. Out of scope: `is_staging` (immutable), `portfolio_uuid`,
  `deleted_at`, `oauth_redirect_url`.


  - **ENT-6212** — Todo, no PR yet. Adds `oauth_redirect_url: list[str]` to the DAL
  `ApplicationRecord` (stored as Dynamo `L` of `S`, missing attribute decodes as `[]`)
  and to the `Application` dataclass, and extends `update()` with `new_oauth_redirect_url`.
  Validation rules (https-only / localhost-http, max 10, max 2048 chars, no fragment,
  no query) are defined in ENT-6208 and enforced in the service layer here. `[]` is
  a valid clear; `None` means don''t touch.


  ### Things worth flagging in the DM

  - 6209–6211 are tight self-contained PRs and should be quick reviews; nothing in
  them touches the OAuth login page surface.

  - The actual coupling point to your team''s work is **ENT-6208** (Application Update
  API endpoint) — it depends on 6212 landing first so the `oauth_redirect_url` field
  exists on the model. Worth confirming with Jordan whether ENT-6208 is also in his
  "second part" bucket or whether you need to coordinate on the endpoint shape that
  the login page (ENT-6204) will read against.

  - The validation rules for `oauth_redirect_url` live in ENT-6208''s spec and the
  service layer (ENT-6212) raises on failure — if the login page does its own redirect_uri
  matching at `/login/oauth` time, it should match exactly the same normalization
  (no fragment, no query, scheme/host comparison) to avoid drift.

  - DynamoDB last-write-wins on update — no optimistic concurrency. Fine for these
  fields but worth knowing.

  '
project: 2026-04-10T0840-ticket
source_id: https://linear.app/canary-technologies/issue/ENT-6211/applicationserviceupdate-for-name-status
tags:
- morning-gtd
- linear
- from-awareness
time_minutes: 20
title: 'Skim: Jordan''s OAuth/ApplicationService refactor tickets (ENT-6209/6210/6211/6212)
  in review'
updated: 2026-05-14 13:32:54.801239
waiting_on: null
waiting_since: null
working_on: true
---

Related to Jordan's DM on oauth split. Skim the In Review tickets so I can respond to the DM with context. https://linear.app/canary-technologies/issue/ENT-6211/applicationserviceupdate-for-name-status

Jordan: oauth work is 2 sides — one ticket (login page) for my team, second part (portfolio-owned APIs) on his side, looser deadline. https://canarytechnologies.slack.com/archives/D07HCMQU5FY/p1778710486268839