---
area: null
contexts:
- consume
created: 2026-06-08 11:24:12.894573
defer_until: null
due: 2026-06-09
energy: medium
id: 2026-06-08T1124-review-design-doc-securing-caller-identity-recomme
order: null
output: |
  ## Agent run 2026-06-08T12:11

  Reviewed the Notion doc "Securing Caller Identity with Istio Infra" (titled in the
  email "Securing Caller Identity - Recommendation & Industry Context") by Arihant Daga.
  https://app.notion.com/p/37481468615180c4994cdff60ed5b878
  Reviewers: Aditya Menon, Johannes Schmidt, Jordan Sterling, Gareth Lloyd. Status: IN REVIEW.
  No existing comments on the doc. NOTHING was posted to Notion — review drafted here only.

  ### Verdict
  Endorse the direction. The core diagnosis is correct and the proof-vs-presence framing
  is exactly right. It is not a redesign — it finishes the phantom-token pattern Canary
  already runs. I'd approve Phase 0 conditional on the rollout/enumeration gaps below
  being closed first; the riskier-than-stated items are the Phase 0 hard-cutover and the
  aud-vs-forwarding tension.

  ### Both load-bearing claims VERIFIED in code (not just asserted)
  - IdentitySid = UNSALTED SHA-256 of (type, reference), derivable offline:
    backend/shared/shared/sids/sid.py:92-117 (plain hashlib.sha256, no salt/pepper/key);
    generated at backend/canary/api_gateway/services/identity_service.py:95.
  - Internal `Bearer id_xxx` trusted by presence, zero signature check:
    backend/canary/canary/middlewares/principal.py:33-55 — resolve_bearer parses the sid,
    does IdentityService.get() (plain DynamoDB lookup), grants principal. An inline comment
    there ALREADY flags this as unsafe and links Linear EE-1495 + PR #46645
    (discussion r3325021033). So the gap is known and tracked, not novel.
  - Contrast confirmed: the external app_xxx:as_xxx path DOES verify cryptographically
    (auth_token_service.py:42-43,86-91, sha3_512 hash-lookup of the secret). The defect is
    specifically the internal token, as the doc says.

  ### Strengths
  - Right altitude: keeps the phantom-token shape, fixes the one defect (sign the internal
    token). Doesn't boil the ocean.
  - Phasing is sensible: HMAC single-verifier (Phase 0) -> generalize/east-west (Phase 1)
    -> asymmetric+JWKS+waypoint+STRICT mTLS (Phase 2).
  - Rotation section is unusually good — make-before-break with a key SET + `kid`, and the
    insight that asymmetric+JWKS turns rotation from "synchronized multi-fleet redeploy"
    into "publish a key + flip the signer." Shipping `kid` from Phase 0 is free and correct.
  - Industry grounding (BeyondProd two-signal model, Netflix Passport, RFC 8693, Istio
    jwt_authn, SPIFFE) is accurate and load-bearing, not decoration.

  ### Key risks to resolve BEFORE Phase 0 merge (the dangerous parts)
  1. Phase 0 is a HARD CUTOVER and the doc under-plays it. "Verify signature + take
     identity_sid from the claim, no valid token -> 401" means the instant it ships, EVERY
     caller that today sends a raw `Bearer id_xxx` and does NOT pass through the
     token-minting api.* edge branch gets a clean 401. The doc proposes "measure east-west
     volume in Datadog and assume ~0." Volume is the wrong instrument — it misses
     low-frequency-but-critical callers (nightly/cron jobs, async/celery workers, one-off
     internal scripts, health/probe paths). Ask for an ENUMERATION of callers + ingress
     paths to the monolith, not a volume estimate, and a dual-accept window (accept BOTH
     opaque id_xxx and signed token behind a flag, watch 401s-by-route, then flip to
     signed-only) rather than a flag day. This is where 401 storms live.
  2. Non-edge ingress to the monolith. The whole fail-closed argument assumes every request
     that reaches the monolith first traversed the token-minting edge. Need explicit
     confirmation there is NO path to the monolith that bypasses the edge (direct ALB/LB,
     legacy ingress, in-cluster DNS, the ~web hostname). Any such path mints no token =>
     fails closed => breakage. This is the same enumeration as (1) from the ingress side.
  3. `aud` vs "forward-the-token-while-valid" (east-west) are in tension. If the edge mints
     aud=monolith and Phase 1 forwards that same token on fan-out to service B, B's aud
     check must fail or B must accept a token not addressed to it (re-opening the replay
     surface). Decide the aud model now: per-service aud (then forwarding needs re-mint /
     token-exchange, not raw forward) vs a generic internal audience (weaker). The doc
     lists "forward vs mint-per-service vs mTLS-only" as the genuinely-open decision —
     agree, and aud semantics are the crux of it.

  ### Technical questions / pushes
  4. Does the sid-hardening (keyed/random instead of unsalted SHA-256) even stay necessary?
     Once trust = signature verification, a derivable sid INSIDE a signed token is harmless
     — guessability only mattered while presence == trust. Making the sid non-derivable is
     a broad, costly migration (it's the spine, referenced everywhere, and the Public API
     doc explicitly decided "Identity sids are not secrets" — this reverses that). I'd pull
     it OUT of Phase 0's critical path: ship the signature first (that closes the hole),
     then decide whether sid-hardening is worth it as true defense-in-depth or is redundant.
     The doc bundles it into Phase 0; I'd de-bundle.
  5. Cross-region short-circuit + signer location. The doc flags (correctly) that moving the
     signer into /api-gateway/authenticate is cleaner for rotation BUT the cross-region
     short-circuit skips authenticate, so that path must re-mint/forward at the destination
     edge. This is described as "a tradeoff to weigh" — it's actually a concrete design item
     that should be specified before committing the signer location, because it determines
     whether Phase 0's monolith-scoped story even holds for cross-region traffic.
  6. Replay within TTL. A signed short-lived token is still replayable until exp if it leaks
     (logs, SSRF, a chatty proxy). Short TTL bounds it — fine given the threat model is
     forgery/smuggling, not in-mesh interception — but the doc should state the residual
     replay window explicitly rather than leave it implicit. (Token-binding/DPoP is overkill
     here; just name the tradeoff.)
  7. Phase 0 "days" estimate is optimistic. Verification in resolve_bearer is one file, yes,
     but minting in the Rust WASM plugin + new ExternalSecret across regions + the
     enumerate/dual-accept rollout (items 1-2) is more than days. The one-file framing hides
     the operational work.
  8. Defense-in-depth strip across ~40 white-label domains + two gateways: is there a single
     chokepoint to strip the identity header, or is it per-domain config? If per-domain, the
     strip has the SAME "new path = forgotten" failure mode the doc rightly warns about — so
     it stays correctly classified as DiD-not-correctness, but worth confirming the strip
     itself isn't presence-shaped.

  ### Wyndham MCP relevance (why this landed on my plate)
  The Wyndham MCP integration calls into the monolith on a caller's behalf, so it is exactly
  the kind of caller Phase 0's fail-closed flip can break. Concrete ask for the author:
  confirm where Wyndham MCP traffic enters. If it arrives on the authenticated api.* edge
  branch, it gets a minted signed token and is fine by construction. If it enters on another
  hostname, or any MCP/agent path reaches the monolith east-west with a raw
  `Bearer id_xxx`, it MUST be in the item-1 enumeration and migrated before signed-only
  enforcement, or MCP auth 401s on cutover. I did not trace the MCP ingress path in this
  pass — flagging it as the specific thing to verify, not asserting it breaks.

  ### Nits
  - Page title ("...with Istio Infra") and the email/DB title ("...Recommendation & Industry
    Context") differ — harmless, but align them so it's findable.
  - Monitoring: doc already calls for verify-failures-by-`kid` (good); add 401s-by-route and
    mint-rate-vs-verify-rate dashboards for the rollout window specifically.

  ### Suggested next step
  These are review comments, not blockers to the idea. If you want, I can post a condensed
  version (verdict + items 1-3 + the Wyndham MCP question) as a Notion comment on the doc —
  needs your explicit go-ahead before I post anything externally.

  ## Agent run 2026-06-09T15:20

  Two follow-ups this pass: (A) traced the MCP ingress path the prior run flagged as
  unverified; (B) reviewed the 1-1 transcript with the author (Daga, Jun 9). Nothing
  posted anywhere — all drafted here.

  ### A. MCP ingress trace — RESOLVED. The good news: MCP does NOT use the broken path.
  The prior run flagged "I did not trace the MCP ingress path." I have now. Conclusion:
  the in-repo MCP surface is auth-INDEPENDENT of the internal `Bearer id_xxx` phantom
  token, so the Phase 0 cutover does NOT break it by construction.

  - The MCP app (`backend/canary/canary_mcp/`) authenticates via its OWN DRF backends, not
    the principal middleware's `resolve_bearer`:
    - `TeleportJwtAuthentication` (canary_mcp/auth.py:24-136): requires `X-Teleport-Jwt` +
      `X-MCP-Internal-Secret` matching `MCP_INTERNAL_SECRET`. The JWT itself is decoded
      WITHOUT signature verification (auth.py:125-136) — trust comes entirely from the
      shared `MCP_INTERNAL_SECRET` proving the request came from the MCP server. So this
      path has its own "trust by shared secret" model, separate from id_xxx.
    - `AgentTokenAuthentication` (auth.py:139-209): static per-agent bearer tokens
      (`MCP_AGENT_TOKEN_{AGENT}`, e.g. devin), constant-time compared. Also not id_xxx.
  - `McpBaseView` (views.py:46-57) pins `authentication_classes = [TeleportJwtAuthentication,
    AgentTokenAuthentication]` and is read-only (http_method_names = get/head/options;
    read-only also enforced in the auth backends and by a CI test per the docstring).
  - There is NO Wyndham-specific MCP code path. `grep wyndham + mcp` only hits settings
    files (deployment domain lists), not a distinct auth/ingress route. The MCP URL set
    (canary_mcp/urls.py) is hotel-analytics / voice / KB / portfolio-analytics endpoints,
    all behind McpBaseView.

  Net: whatever "Wyndham MCP" denotes operationally, if it reaches Canary through the MCP
  server it arrives with a Teleport JWT + internal secret (or an agent token), NOT a raw
  `Bearer id_xxx`. Phase 0's signed-only flip changes the id_xxx path; it leaves the MCP
  backends untouched. So the prior run's worst-case ("MCP auth 401s on cutover") does NOT
  materialise for the canary_mcp surface. This downgrades the Wyndham-MCP concern from
  "verify before cutover" to "confirmed not on the affected path."

  CAVEAT — one residual question worth a sentence to the author: the MCP endpoints call
  into monolith services/selectors IN-PROCESS (they're Django views in the monolith, e.g.
  HotelAnalyticsService, HotelSelector), so there's no second internal hop using id_xxx
  from within an MCP request. IF any MCP view is ever changed to make an east-west HTTP
  call to another internal service on the user's behalf, THAT hop would mint/forward a
  token and re-enter the id_xxx story. Not the case today; flag it as a "keep MCP in-process
  or use token-exchange when you don't" note, not a current break.

  ### B. Review of the 1-1 transcript (Daga, Jun 9)
  The call confirms the prior code review and adds org + design facts that change two of my
  recommendations. Verbatim-grounded takeaways:

  CONFIRMS (matches what I verified in code):
  - Author states the exact defect: "unsalted hash of type and reference… you can frame
    this thing as long as you know the ID number and the mechanism," and the endpoint
    "only checking that identity_sid is present, we trust that." This is precisely
    sid.py:92-117 + principal.py:33-55. Diagnosis is sound and self-consistent.
  - Author confirms it's theory-now-not-yet-exploited: id_sid "is only traveling within our
    VPC, never sent to the client" but "someday it may be leaked… we're not treating this
    as a secret." Matches my item-6 (residual replay) and the "becomes real when the API
    goes public" framing. Good — he's not overselling current exposure.
  - Author confirms the Phase 0 mechanism is exactly "identity_sid as a JWT claim"
    ("it's still going to be identity_sid, but in JWT form… identity_sid as claim"). Aligns
    with the doc and my read.

  NEW — changes my recommendations:
  - On my item-4 (de-bundle sid-hardening): the transcript VALIDATES de-bundling. The author
    frames the fix as purely "send a JWT of the same thing" — the sid stays derivable inside
    the signed token and that's fine. He does NOT propose making the sid non-derivable as
    part of this work. So Phase 0 = signature only; sid-hardening is not even on his path.
    My "pull it out of Phase 0" recommendation is consistent with the author's own framing —
    I'd now state it as "confirm sid-hardening is explicitly OUT of scope" rather than "argue
    to remove it."
  - DEV ESCAPE HATCH = new security item, not in my prior review. Author: "if DEBUG is true,
    we do expect that it can be without JWT as well" + "a make command wrapper." This is a
    classic footgun: a debug-only auth bypass that must be PROVABLY unreachable in prod
    (not just `if settings.DEBUG`, which has bitten teams when DEBUG leaks true, or when the
    bypass keys off an env var an attacker can influence). Concrete ask for the doc: specify
    the escape hatch as fail-CLOSED (default deny; bypass requires an explicit dev-only
    signal that cannot exist in prod images), and add a CI/startup assertion that the bypass
    is disabled when not DEBUG. Add this to the "risks to resolve before Phase 0" list.
  - JWT SECRET ROTATION is the actual blocking dependency. Author: "right now I'm just
    waiting for approval from platform… specifically the JWT secret rotation piece. Once
    we're aligned on that, my next move is creating a project." So the doc's rotation section
    (which I praised) is also the critical-path gate — the thing platform must sign off. If
    Gareth wants this to move, the lever is getting platform alignment on rotation, not more
    review of the core idea.

  ORG / OWNERSHIP signal (relevant to the possible identity pod):
  - Author is PIVOTING OFF this in June. Request-framework pod is redirecting to AI tooling
    ("now that Tyler is also not there"). He explicitly will NOT implement: "I would not be
    able to do all of the implementation… create a project for that and then maybe hand over
    to some other person." He wants the IDEA + design doc approved, then a project created
    and handed off.
  - This is the load-bearing org fact: if a dedicated identity pod is real and lands with
    Gareth, this work arrives as an APPROVED-DESIGN-BUT-UNOWNED implementation project. The
    risk is not the design (it's sound) — it's the handoff gap: the person who holds the
    context is leaving the work. Recommend capturing Daga's context NOW (he offered: "ping
    me if you have follow-ups") and treating the enumeration (items 1-2) + escape-hatch
    hardening + platform rotation sign-off as the concrete project scope to inherit.
  - Genesis of the defect (for the record): author says it was a deliberate DX tradeoff
    called out in the services doc and discussed with Jordan — "to keep it simple… we can
    simply curl it, need not generate a new token." So it was a known, signed-off simplicity
    choice, not an accident. Reversing it has a DX cost the author plans to absorb with a
    make-command wrapper — which is why the escape hatch exists, which is why the escape
    hatch needs the hardening above.

  ### Updated bottom line
  Endorse unchanged. The transcript strengthens the case (author's framing matches the code
  and my review) and resolves the Wyndham-MCP worry (not on the affected path). Two additions
  to the "before Phase 0" list: (a) the DEBUG escape hatch must be provably-prod-unreachable
  and fail-closed; (b) platform sign-off on JWT secret rotation is the real gate. One org
  flag for the pod question: the design is owned by someone leaving the work — plan the
  handoff, capture context before June.

  ### Suggested next step (unchanged, still needs your go-ahead)
  I can post a condensed Notion comment (verdict + enumeration ask + escape-hatch hardening
  + Wyndham-MCP "confirmed not affected"). I have NOT posted anything. Say the word and I'll
  draft the exact comment text for your approval before sending.
project: 2026-04-10T0840-ticket
source_id: https://mail.google.com/mail/u/0/#inbox/19e98426b872f374
tags:
- morning-gtd
- gmail
time_minutes: 15
title: 'Review design doc: Securing Caller Identity — Recommendation & Industry Context'
updated: 2026-06-16 15:53:10.706307
waiting_on: null
waiting_since: null
working_on: false
---

Arihant Daga added you as a reviewer (Notion design doc). Relevant to Wyndham MCP auth.
https://mail.google.com/mail/u/0/#inbox/19e98426b872f374