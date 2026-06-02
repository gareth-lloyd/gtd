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
  ## PR #46645 — identity verification w/ API Gateway (EE-1490, Arihant)

  **Bottom line:** Solid, well-architected foundation. Ship it. No blocking bugs. The real
  watch-item is a security follow-up (EE-1495) the author already filed. Review NOT posted to
  GitHub — for you to relay. (Status: merged 2026-06-02; was approved by jsflax + jordan-canary.)

  **What it is:** one typed `Principal` per request. Middleware *establishes* "who is calling"
  (soft-fail → anonymous, never rejects); view-level gatekeepers *require* a type (hard 401/403).
  Policy in `shared`, credential resolution in `canary`. Clean, tested (100% new-stmt coverage),
  unusually good docstrings.

  ### Verified
  - `self._principal` stash is thread-safe — `Gatekeeper.clone()` drops `_`-attrs per request.
  - Cross-app imports (IdentityService, stub_identity), enum/field alignment, lazy
    `SimpleLazyObject` principal + `isinstance` resolution — all correct.

  ### Findings (ranked)
  1. **[SECURITY — the one that matters] identity_sid-as-bearer is unauthenticated at Django.**
     sids are derivable (unsalted hash of a non-secret ServiceSid), not secrets. Security rests
     ENTIRELY on the Istio edge stamping `Bearer <sid>` and nothing else reaching Django with one.
     Any non-Istio path in (SSRF, internal network, misrouted route) = impersonate any service/app.
     Author flagged it in-code + filed **EE-1495** (Urgent, still Todo). → Confirm with Arihant
     that EE-1495 is a HARD GATE before any real route rides this on a network-reachable path.
  2. **[minor, OPEN thread] Bearer prefix is case-sensitive** (`"Bearer "` + startswith). RFC 7235
     says case-insensitive; `bearer`/`BEARER` silently downgrade to anonymous. Fails safe (clean
     401), one-line fix. use-tusk's P2 thread still open — nudge to fix or wontfix-close.
  3. **[design nit] canary ↔ api_gateway now mutually dependent** (so PrincipalMiddleware can
     import IdentityService). Framework permits it; long-term IdentityService probably belongs in
     `shared`.

  ### Good calls
  - `HotelUserGatekeeper` deliberately refuses `OAuthUserPrincipal` until scope+install-grant+MFA
    enforcement lands — right defensive default.
  - Failed Bearer never falls back to the session cookie (tested) — no silent cookie-borrowing.
  - Copilot's `service_name`/fixture nits are stale (code already uses `service_sid`) — dismiss.

  ### How this fits OAuth / global APIs / mobile (the bigger picture)
  This PR is the **framework rail** (Arihant / Eng Enablement, "Canary Services Framework"); the
  **OAuth Global Login** + Global API work (Jordan/Andrea, Enterprise, ENT-62xx) is the **product
  train** that rides it. They meet at the Istio edge contract: OAuth mints public credentials and
  teaches the edge to validate them → edge rewrites to `Bearer <identity_sid>` → THIS PR's
  middleware resolves it to a Principal. Concrete seams:
  - `IdentityType` enum is the literal handoff (OAuth's ENT-6207 adds types; this PR branches on them).
  - `ApplicationPrincipal.scopes` + gatekeeper `required_scopes` = the (currently no-op) enforcement
    point waiting for OAuth scopes to ship.
  - `OAuthUserPrincipal` = the mobile / app-on-behalf-of-user case — shape carved here, filled by OAuth.
  - `UserPrincipal.sid = None` = the hook for the global auth_user / global-login table (ENT-6300).
  - **EE-1495 is a shared prerequisite** — OAuth tokens resolve to identities, so its trust model is
    only as strong as this edge gate.
  - Timing: OAuth is "Phase Future" (NOT on the IHG rollout, no committed date). The rail is being
    laid ahead of it; the immediate consumer is internal-service auth + the RFv2 route migration.

  ### Draft Slack reply to Arihant (NOT sent)
  "Looked it over — clean design, the middleware/gatekeeper split and soft-fail/no-cookie-fallback
  policy are right, coverage is great, no blockers. Two things: (1) treat EE-1495 as a hard gate
  before any route rides this on a network-reachable path; (2) tiny — the Bearer prefix check is
  case-sensitive (use-tusk's open P2), worth a one-liner or wontfix. Nice call deferring
  OAuthUserPrincipal out of HotelUserGatekeeper."

  NOTE: review only — did not run tests locally; CI green, new-code coverage 100%.
project: null
source_id: https://canarytechnologies.slack.com/archives/C0ACQT82JLA/p1780068040459209
tags:
- morning-gtd
- slack
- from-awareness
time_minutes: 20
title: 'Review API Gateway identity-verification PR #46645 (Arihant)'
updated: 2026-06-02 14:05:58.603410
waiting_on: null
waiting_since: null
working_on: false
---

Arihant asked for eyes on the identity-verification w/ API Gateway work. Notion design + PR #46645.
https://canarytechnologies.slack.com/archives/C0ACQT82JLA/p1780068040459209