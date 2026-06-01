---
area: null
contexts:
- react
created: 2026-05-31 07:53:13.121866
defer_until: null
due: null
energy: medium
id: 2026-05-31T0753-review-api-gateway-identity-verification-pr-46645
order: null
output: |
  ## Agent run 2026-06-01T16:55 — Review of PR #46645 (identity verification w/ API Gateway)

  Reviewed the full diff (14 files, +961). NOT posted to GitHub — this is for you to weigh in / relay to Arihant.
  Status on GitHub: already APPROVED by jsflax + jordan-canary; CI green; Tusk/Copilot bots ran.

  ### Verdict
  Solid, well-architected PR. The middleware-establishes / gatekeeper-requires split is clean,
  service-agnostic (policy in shared, credential resolution in canary), thoroughly tested
  (100% of new statements covered), and the docstrings are unusually good. I'd approve too.
  No blocking correctness bugs found. The substantive concerns are all SECURITY/design, and the
  author has already flagged the biggest one in-code with a Linear ticket.

  ### Things I verified
  - Thread-safety of `self._principal` stash in gatekeepers: SAFE. `Gatekeeper.clone()`
    (core.py:104) copies only non-underscore config attrs per request and runs authenticate()
    on the clone, so request-scoped `_principal` can't leak across requests. Docstrings'
    "per-request clone" claims are accurate.
  - All cross-app symbols canary now imports from api_gateway exist
    (IdentityService.get, testing.stub_identity) and IdentityType/IdentityRecord fields line up.
  - `identity.type == IdentityType.INTERNAL_SERVICE` works (StrEnum vs str field) — fine.
  - Lazy `request.principal` (SimpleLazyObject) + `isinstance` forcing resolution — correct, tested.

  ### #1 thing to surface (security, author already knows)
  `resolve_bearer` trusts ANY well-formed identity_sid that resolves in the Identity table as
  that principal type. identity_sids are NOT high-entropy secrets — they're guessable/enumerable
  handles. Auth therefore rests ENTIRELY on the Istio WASM edge validating the public
  `app:secret` token and rewriting it to `Bearer <identity_sid>` before it reaches Django.
  Any path that reaches Django with a raw `Bearer <sid>` bypassing Istio (direct internal
  network, SSRF, a misrouted public route) authenticates an attacker as that service/app.
  - Author has acknowledged this in-code (principal.py:674-677) and filed **EE-1495**. jsflax
    left a matching non-blocking trust-boundary note.
  - My take: fine to merge as the framework skeleton, but EE-1495 must land before any real
    internal-service route goes live behind this on a network-reachable path. Worth confirming
    with Arihant that EE-1495 is a hard gate on the task-management routes that stack on top,
    not a someday-maybe.

  ### #2 (minor, still OPEN on PR) — case-sensitive Bearer prefix
  principal_middleware.py: `_BEARER_PREFIX = "Bearer "` + `.startswith()`. RFC 7235 auth-scheme
  is case-insensitive; `bearer `/`BEARER ` silently downgrade to session→anonymous. use-tusk
  flagged this as P2 and the thread is still open. Low severity (fails safe to a clean 401, no
  escalation), but a one-line `.lower().startswith()` / case-insensitive split is a cheap fix.
  Worth nudging Arihant to either fix or explicitly wontfix-close the thread.

  ### #3 (design note, non-blocking) — canary <-> api_gateway now mutually dependent
  opinionated_state.py now lists API_GATEWAY in CANARY.dependencies AND CANARY in
  API_GATEWAY.depended_on_by (api_gateway already depended on canary). That's a deliberate
  bidirectional edge so canary's PrincipalMiddleware can import IdentityService. The dep
  framework permits it (explicitly encoded), but it's a coupling smell worth a sentence of
  justification — long term IdentityService arguably wants to live in shared so neither app
  has to reach into the other.

  ### Good calls worth acknowledging
  - HotelUserGatekeeper deliberately does NOT yet accept OAuthUserPrincipal, with a precise
    comment on why (scope + install-grant + MFA reconciliation must land first, else an app
    bypasses scope enforcement via a hotel-user route). That's exactly the right defensive
    default — flag it to Arihant as a highlight.
  - "failed Bearer never falls back to session cookie" is correctly implemented and tested —
    avoids a bad token silently borrowing an ambient cookie identity.
  - OAuthUserPrincipal / GuestPrincipal defined-but-reserved so reviewers see the full model.

  ### Already-resolved / non-issues
  - Copilot's `service_name` naming nit and its `_internal_principal` fixture-type nit appear to
    be against an earlier revision — current code uses `service_sid` and the test helper passes
    `IdentityType.INTERNAL_SERVICE` explicitly. Safe to dismiss.

  ### Suggested reply to Arihant (Slack) — DRAFT, not sent
  "Looked it over — clean design, the middleware/gatekeeper split and the soft-fail/no-cookie-
  fallback policy are right, and test coverage is great. No blockers from me. Two things:
  (1) the identity_sid-as-bearer trust model (EE-1495) — agree it's fine as the skeleton, but
  let's treat EE-1495 as a hard gate before the task-mgmt routes ride on it on any network-
  reachable path; (2) tiny one: the Bearer prefix check is case-sensitive (use-tusk's open P2),
  worth a one-liner or a wontfix. Nice call deferring OAuthUserPrincipal out of HotelUserGatekeeper."

  NOTE: I did not run the test suite locally (review only); CI is green and new-code coverage is 100%.
project: null
source_id: https://canarytechnologies.slack.com/archives/C0ACQT82JLA/p1780068040459209
tags:
- morning-gtd
- slack
- from-awareness
time_minutes: 20
title: 'Review API Gateway identity-verification PR #46645 (Arihant)'
updated: 2026-06-01 16:55:00.000000
waiting_on: null
waiting_since: null
working_on: false
---

Arihant asked for eyes on the identity-verification w/ API Gateway work. Notion design + PR #46645.
https://canarytechnologies.slack.com/archives/C0ACQT82JLA/p1780068040459209