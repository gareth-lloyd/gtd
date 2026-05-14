---
area: null
contexts:
- deep
created: 2026-05-13 11:28:24.290802
defer_until: null
due: null
energy: high
id: 2026-05-13T1128-review-pr-45149-request-framework-v2-part-4-resour
order: null
output: "## Agent run 2026-05-13T12:00Z\n\nReviewed locally via `gh pr diff 45149`
  + checkout. 1370/-203 across 16 files, draft, stacked on the (now-closed) #45146/#45147
  — this PR absorbs both of them since the gatekeeper and authorize layers ended up
  too coupled to split.\n\n### Design — what it is\nv2 splits the v1 Gatekeeper into
  two pieces:\n- `Gatekeeper.authenticate(request) -> AuthContext` (ABC, one abstract
  method) runs first, validates credentials, returns immutable `AuthContext(request,
  user)`.\n- Each `Resource`'s `authorize(auth_context, instance) -> AuthorizeContext
  | None` callback runs per-resource after resolution; contributions are merged into
  a single `AuthorizeContext(hotel_id, portfolio_id)`.\n- `Gatekeeper.check_permissions(auth,
  authorize_ctx)` runs last and enforces view-declared role permissions against the
  established scope. No-op on the base; `HotelUserGatekeeper` overrides it.\n- Gatekeepers
  are now pure config — no per-request state, no `clone()`, no `inject_request_data`,
  no convention checks. v1's `<AppName>AppGatekeeper` naming/file-location rule is
  gone.\n- Provides `HotelUserGatekeeper`, `GuestUserGatekeeper`, `HotelResource`,
  `AuthorizeHotel`, `AuthorizeByScope`, `NoAuthorize`. Portfolio/Staff/Internal/PublicAPI
  gatekeepers are flagged \"planned\".\n\nArchitecturally this is clean and a genuine
  improvement over v1's implicit auth and per-app gatekeeper sprawl. Ready to be plumbed
  into real routes in later parts of the stack.\n\n### Concerns to raise on the PR
  (in priority order)\n\n**1. Doc/code contradiction on AuthorizeContext conflict
  resolution.** This is the biggest item.\n- `_resolve.py::_merge_authorize_context`
  **raises RuntimeError** on a hotel_id/portfolio_id mismatch between two callbacks
  (and its docstring agrees).\n- The README (intro flow diagram blurb + FAQ \"Why
  does the authorize callback return…\") says \"last-non-None wins per slot; on a
  mismatch the slot is dropped and logged.\"\n- `auth.py::AuthorizeContext` docstring
  also says \"log and drop the slot.\"\n- Pick one. Raising is probably correct (it's
  a programming error — you can't be scoped to two hotels at once), in which case
  update the README + `AuthorizeContext` docstring. Add a test for the raise.\n\n**2.
  AuthorizeHotel returns `Unauthorized` for non-membership — exposes hotel-slug enumeration.**\n`AuthorizeHotel.__call__`
  raises `Unauthorized` when the authenticated user isn't a `CompanyHotelUser` of
  the resolved hotel. That confirms the slug exists for anyone with valid credentials,
  which v1 typically obscured with 404. The commit `6c4e9f31d19 AuthorizeHotel: raise
  Unauthorized for the non-membership case too` shows this was a deliberate tightening
  — worth confirming it's an intentional product decision (rather than a slip) and
  aligning with the v1 behavior people are used to.\n\n**3. Test gap on the canary-side
  security-sensitive bits.**\nShared/framework code is well-tested (`_resolve_test`,
  `authorize_test`, `core_test`, `resource_test` — solid coverage). But `backend/canary/canary/access_control/gatekeepers.py`
  and `backend/canary/hotels/request_framework/*.py` have **zero tests**. Specifically
  missing:\n- `AuthorizeHotel.__call__`: anonymous user; authenticated user not in
  CompanyHotelUser; IP blocked; happy path returning correct `AuthorizeContext(hotel_id=…)`.\n-
  `HotelUserGatekeeper.authenticate`: each AuthenticationLevel branch (active/profile/MFA),
  with corresponding exception types.\n- `HotelUserGatekeeper.check_permissions`:
  no resource established hotel context → the `RuntimeError`; declared permissions
  enforced; declared permissions empty → early return.\n- `HotelResource.resolve`:
  HotelSelector miss → NotFound; happy path binds structlog context.\n- `GuestUserGatekeeper.authenticate`:
  anonymous user → `user=None`; authenticated session user → `user=<User>`.\n\nThese
  are the closest things to production-affecting auth code in this PR; they shouldn't
  ship without unit tests.\n\n**4. README claim about `AnonymousUser` is wrong for
  the current implementation.**\nREADME says `GuestUserGatekeeper`'s `auth.user` is
  `User | AnonymousUser | None`. The code only ever produces `User | None` (anonymous
  → returns `AuthContext(request=request)` with default `user=None`). Either:\n- return
  `AuthContext(request=request, user=user)` when anonymous (preserving Django's `request.user`
  as an AnonymousUser), or\n- update the README and tighten `AuthContext.user` to
  `User | None`.\nThe Django convention is to keep AnonymousUser; v1's `get_authenticated_user`
  returns `None`, so this matches v1, but the docs should reflect that.\n\n**5. JSON
  body is parsed twice.** `_resolve.collect_raw_values` parses `request.body` to extract
  resource fields; then `_build_param_dataclasses` re-parses it via `json.loads(request.body)`
  for the body dataclass. Cache the parse (e.g., compute once in `prepare_request`
  and pass through). Minor perf, but per-request hot path.\n\n**6. `auth` param injection
  is structurally typed by name only.**\n```python\nif \"auth\" in get_type_hints(request_handler):\n
  \   params[\"auth\"] = auth_context\n```\nIf a handler accidentally declares `auth:
  SomeOtherType` it'll receive an `AuthContext` and a misleading type error happens
  deep in the handler. Verify the hint resolves to `AuthContext` (consistent with
  how `gatekeeper`/`body`/etc. are typed-checked in `_run_convention_checks`).\n\n**7.
  `GuestUserGatekeeper.authenticate` redundant check.**\n```python\nif user.is_anonymous
  or user.is_authenticated is False:\n```\nEquivalent to `if not user.is_authenticated:`
  — one check suffices. Comment already notes the Django-way intent; just pick one
  form. (Commit `35c1519bc1a` shows this was already addressed once; the leftover
  redundancy is minor.)\n\n**8. Global cattrs `converter` is mutated at decoration
  time.** `register_resource_field_hooks_for_request_handler` calls `converter.register_structure_hook(dc_class,
  …)` on the module-level converter. If two views share a param dataclass with different
  Resource fields, the second registration overwrites the first. In practice param
  dataclasses are per-view, so this is fine — but worth a comment noting the assumption,
  or scoping to a per-handler converter.\n\n**9. `_merge_authorize_context` raises
  `RuntimeError`.** If the policy stays \"raise on mismatch,\" consider a more specific
  exception type (a framework-level `AuthorizeContextConflict` or similar) — `RuntimeError`
  will be hard to grep for and harder to handle/observe in middleware.\n\n**10. Two
  `MalformedBody`-class hierarchies briefly coexist.** `exceptions.py` defines the
  canonical ones; `core.py` previously had its own. The `__init__.py` re-exports from
  `exceptions.py` now and `core.py` imports `MalformedBody` from there — good. Just
  verify no in-tree code still imports `MalformedBody` from `shared.request_framework_v2.core`
  directly (a quick `rg \"request_framework_v2.core import .*Malformed\"` would confirm).\n\n###
  Things that look good\n- Topological sort with cycle detection + unit tests is the
  right shape.\n- `AuthorizeByScope` requires `scoped_by` at import time via the `requires_scoped_by`
  class marker — clean foot-gun prevention.\n- `AuthContext` and `AuthorizeContext`
  are frozen dataclasses; immutability is enforced where it matters (the wire-level
  scope contributions). The shallow-immutable nature of `request: HttpRequest` is
  fine but maybe worth a one-line acknowledgment in `AuthContext`'s docstring.\n-
  `Resource.get_wire_type` falls back to `str` for unknown field types — sensible
  for OpenAPI generation.\n- `HotelResource` correctly routes through `HotelSelector`
  to preserve old-slug ownership.\n- Resource-field cattrs passthrough is a neat trick
  to keep cattrs out of the model-loading path while preserving structured validation
  for the rest.\n\n### Recommendation\nNot blocking, but I'd want (1), (2), (3), and
  (4) addressed before this gets out of draft. (1) and (4) are doc bugs that mislead
  future readers; (2) is a security/policy question that needs a sign-off; (3) is
  a test-coverage gap on the most security-sensitive new code. The rest (5–10) are
  nits.\n\nNo comment posted to the PR — drafted locally; awaiting user direction
  before posting anything to GitHub.\n"
project: 2026-04-16T1210-unblock-team
source_id: https://github.com/canary-technologies-corp/canary/pull/45149
tags:
- morning-gtd
- github
time_minutes: 45
title: 'Review PR #45149: Request Framework v2 Part 4 — Resource resolution + Hotel
  Authorization'
updated: 2026-05-13 23:07:14.372796
waiting_on: null
waiting_since: null
working_on: false
---

Arihant requested review. Part 4/7 in RF v2 stack; stacked on #45147. Significant framework change. https://github.com/canary-technologies-corp/canary/pull/45149