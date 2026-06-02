---
area: null
contexts:
- react
created: 2026-06-02 07:17:51.414550
defer_until: null
due: null
energy: medium
id: 2026-06-02T0717-review-pr-46780-request-framework-v2-documentation
order: null
output: |
  ## Agent run 2026-06-02T14:19

  Reviewed PR #46780 (docs-only, +1190/-6, 12 files). Verified the docs' factual
  claims against shipped code on master rather than just reading for prose. The
  docs are genuinely high quality and mostly accurate — but there is one
  structural decision worth a conscious call before approving, plus two concrete
  inaccuracies. Did NOT post anything to GitHub. State: OPEN, already approved by
  dephiros (2026-06-02); 2 Copilot passes + several arihantdaga self-comments.

  ### Headline issue — the recommended import path only partially works today

  All docs tell readers to `from shared.request_framework import ...` (the rename
  target). Reality on master:
  - `shared/shared/request_framework/__init__.py` exports ONLY: validate_request,
    Gatekeeper, DataResponse/SimpleResponse/EmptyResponse/FileResponse/RedirectResponse.
  - It does NOT export: AuthContext, AuthorizeContext, Resource, AuthorizeByScope,
    NoAuthorize, or any Principal type. Those live ONLY in
    `shared.request_framework_v2` (its package dir lacks resource.py / authorize.py /
    identity.py / auth.py entirely).
  - 45 real modules import from `request_framework_v2`; exactly 1 imports from
    `shared.request_framework` (hotels/views/gatekeeper.py, just Gatekeeper).

  Concrete consequence: getting-started.md (the "read first" page) Step 3 has
  `from shared.request_framework import AuthorizeByScope`, which raises ImportError
  TODAY. Earlier imports on the same page (DataResponse, validate_request) succeed —
  so a newcomer copying verbatim gets a confusing half-working import block, not a
  clean "wrong module" failure.

  The author IS aware: README.md has a blockquote hedge ("rename in flight — if an
  import fails, the package is still request_framework_v2"). So this is a deliberate
  forward-looking-docs choice, not an oversight. My concern is severity/placement:
  - The hedge lives only in README. A reader who lands on getting-started.md (which
    the README itself sends them to "first") never sees it before hitting the broken
    import.
  - "If an import fails" undersells it — for the core auth/resource machinery the
    import ALWAYS fails today; it's not an edge case.

  Recommendation (Gareth's call — not a blocker): either
  (a) document `shared.request_framework_v2` (the path that works everywhere on
      master now) with a note that a rename to `shared.request_framework` is coming; or
  (b) keep the forward-looking target but (i) repeat the hedge at the top of
      getting-started.md, and (ii) confirm the rename PR is actually landing soon —
      otherwise these docs ship describing an import surface that doesn't fully exist.
  Worth a one-line question to arihantdaga on whether the rename is imminent.

  ### Concrete inaccuracies (should fix)

  1. migrating.md references a skill `migrate-validate-request-to-request-framework`
     "(in the ee plugin)" and tells readers to "run it on a view file." That skill
     does NOT exist anywhere in the repo. The ee plugin only ships
     `creating-rfv2-401-monitors` (which IS real — that reference is correct) and
     `creating-groundcover-monitors`. Either the skill is unmerged/renamed, or the
     reference is aspirational. Flag it — readers are told to run a non-existent tool.

  2. Example permission names are invented. Docs use `Permission.DASHBOARD_READ`,
     `RESERVATIONS_READ`, `RESERVATIONS_WRITE`, `CONTRACTS_READ` — none exist in
     `permissions.constants.Permission`. Real names follow a different scheme
     (ANALYTICS_HAS_DASHBOARD_ACCESS, CONTRACTS_HAS_PRODUCT_ACCESS, AUTHS_CAN_TAKE_PAYMENT,
     …). Low severity (clearly illustrative, inside example bodies), but the PR
     description claims things were "verified against real views," and these read like
     real members. Suggest either real names or obviously-placeholder ones
     (Permission.SOME_PERMISSION).

  ### Minor / verify

  - responses.md & reference.md state the 422 body is exactly
    `{"status": 422, "code": "unprocessable_entity", "data": {"fields": "<msg> @ <path>"}}`.
    UnprocessableEntity + the code/status are correct; the precise `data.fields`
    rendering is middleware-dependent and I did not trace it end-to-end. Descriptive
    only (nobody copy-pastes it), so low risk — worth a quick confirm by the author.
  - PR description says "not a migration guide," yet migrating.md exists and is linked.
    It's a thin pointer page, so fine — just a wording mismatch in the PR body.

  ### Verified CORRECT (the bulk of the PR — accurate against code)

  - validate_request, all 5 response types, Gatekeeper ABC (single abstract
    authenticate(); optional check_permissions default no-op) — accurate.
  - clone() lifecycle: confirmed core.py drops leading-underscore attrs
    (`if not k.startswith("_")`). The underscore-state-vs-config explanation is correct.
  - SimpleResponse is_list flag (uses safe=not is_list) — accurate (PR #46386).
  - Gatekeepers in canary/access_control/gatekeepers.py — HotelUserGatekeeper
    (optional hotel_permissions, MFA default, .user), GuestUserGatekeeper
    (.user -> User|None), PortfolioUserGatekeeper, StaffUserGatekeeper (real operator
    under impersonation) — all signatures accurate.
  - InternalServiceGatekeeper / InternalServiceOrApplicationGatekeeper in
    api_gateway/gatekeepers.py with documented params/accessors — accurate.
  - HotelPermissions(hotel_all/hotel_any), PortfolioPermissions(portfolio_all/
    parent_portfolio_all), AuthenticationLevel(MFA_REQUIRED/USER_PROFILE/IS_ACTIVE) —
    accurate.
  - AuthorizeHotel/AuthorizeHotelFromResource (hotels.request_framework.authorize),
    HotelResource (…resources), AuthorizePortfolio/PortfolioResource
    (portfolios.request_framework __init__), Resource base (model/identifier/resolve/
    get_wire_type; authorize= required; AuthorizeByScope requires scoped_by=) — accurate.
  - generate_openapi management command exists; fanout/schemas/dataclass_resource.py
    (DataclassResourceSchema) and guest/schemas/reservation_note_schema.py exist.

  ### Bottom line
  Strong, well-structured docs; the framework-mechanics descriptions are accurate and
  clearly the author DID verify against real code. The one thing I'd want resolved
  before merge is the import-path decision (headline issue) — it's the difference
  between docs that work today and docs that work after an unmerged rename. The
  missing migrate skill and fake permission names are quick fixes. None of it is a
  code-risk (docs only). No GitHub action taken — awaiting your decision on whether/how
  to raise these with arihantdaga.
project: null
source_id: https://github.com/canary-technologies-corp/canary/pull/46780
tags:
- morning-gtd
- github
time_minutes: 20
title: 'Review PR #46780: Request Framework v2 documentation'
updated: 2026-06-02 14:25:18.226654
waiting_on: null
waiting_since: null
working_on: false
---

Personally requested by arihantdaga; not yet reviewed.
https://github.com/canary-technologies-corp/canary/pull/46780