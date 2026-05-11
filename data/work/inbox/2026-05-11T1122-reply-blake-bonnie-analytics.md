---
area: null
contexts: []
created: 2026-05-11 11:22:17.226474
defer_until: null
due: null
energy: low
id: 2026-05-11T1122-reply-blake-bonnie-analytics
order: null
output: |
  ## Agent run 2026-05-11T11:35

  Thread is Crown Resorts asking Canary to embed their Google Tag Manager
  container (GTM-WJTX3ZWW) on the digital compendium pages hosted on
  checkin.crownresorts.com.au, so they can do cross-domain attribution from
  the in-room QR code into Crown websites + Seven Rooms. Pilot launches at
  Crown Promenade Melbourne 18 May 2026. Blake is asking whether to scope
  this narrowly (just GTM) or build a generic "embed analytics scripts"
  capability. Connor flagged that we already did this for Wyndham
  ("Quantum Metric"). Bonnie wants to commit to Crown by Fri 15 May.

  ### What we did for Wyndham Quantum Metric

  Frontend-only, ~15 lines, all in `frontend/guest/src/views/HotelRoot.vue`
  (lines 113–130). It hard-codes a single script URL and gates it on
  portfolio + feature flag:

  - `QUANTUM_METRICS_SRC = "https://cdn.quantummetric.com/qscripts/quantum-wyndham.js"`
  - Loaded once, when both:
    - `getFeatureValue(Features.ROLLOUT_QUANTUM_METRICS_WYNDHAM)` is true, **and**
    - `isWyndham(hotel)` (i.e. `hotel.portfolio_identifiers` includes `WYNDHAM`).
  - Uses the existing `shared/helpers/loadScript` helper, which appends a
    `<script src=…>` tag to `<head>` once and caches the promise globally.
  - Scope is the guest-facing Compendium SPA only (not check-in,
    authorizations, hotels app, etc.) — exactly the limit Connor described.

  So: portfolio-scoped feature flag + hard-coded URL + portfolio predicate.
  No backend, no admin UI, no config, no per-hotel anything. Wyndham gets
  their own Quantum-Metric tenant bundled into one script and we just inject
  it.

  ### Is it easy to make generic?

  Two answers depending on what "generic" means:

  **(a) Same shape for Crown (one-off, ships fastest, ~half a day):** copy
  the Wyndham block with `ROLLOUT_CROWN_GTM_TRACKING` + `isCrown(hotel)`
  (the helper already exists in `shared/helpers/hotel.ts`) + Crown's GTM
  loader URL. **Caveat:** Google Tag Manager normally ships in two pieces —
  an inline `<head>` bootstrap script and a `<noscript><iframe>` after
  `<body>`. Our `loadScript` helper only does the first. For an SPA like the
  compendium, the `<noscript>` fallback is largely cosmetic (no JS means the
  app never renders anyway), so we can probably skip it, but Crown should
  confirm. If they insist on the iframe we'd need a tiny helper to inject
  it.

  **(b) Properly generic "embed analytics scripts" feature (~2–4 days):**
  table-driven config (per hotel or per portfolio) of script URLs to embed,
  with optional support for inline GTM bootstrap + noscript iframe, and an
  allow-list of trusted CDNs so we don't sign up to debug every customer's
  broken tracking pixel. Probably worth doing once if Blake is right that
  more Enterprise customers will ask — which feels likely, GTM/analytics
  embedding is a stock Enterprise digital-team ask.

  ### My recommendation to Blake

  - This belongs in **Enterprise**, not In-Stay. It's a request from a
    corporate digital-marketing team for cross-domain attribution; same
    shape and stakeholder profile as the Wyndham Quantum work. In-Stay is
    about the in-stay guest experience, not Crown's marketing pipeline.
  - For the **15 May commitment**: confidently yes, we can ship the
    Wyndham-shaped one-off (`isCrown` + flag + GTM bootstrap) within the
    pilot window. The cheap path is well-trodden.
  - But flag two things to Crown:
    1. The `<noscript>` iframe piece — confirm they're okay without it on
       an SPA.
    2. Their Step-1 snippet uses an **inline** `<script>` block that
       defines a function and references `window.dataLayer`. We don't
       currently allow inline analytics scripts (our `loadScript` only
       handles `<script src=…>`). Either we adapt to inject it inline, or
       we host the equivalent bootstrap ourselves and just load it via
       URL. Worth a 10-min call between our dev and Meeno to settle.
  - Decide separately whether to commit to (b) — the generic version — as
    a follow-up. If Blake wants to position this as a repeatable
    Enterprise capability ("Embedded customer analytics"), it's worth
    the extra few days. If Crown is one-of-one for now, mirror Wyndham.

  ### Risks worth naming in the reply

  - **Security**: 3rd-party scripts get full DOM/cookie access to a page
    that may include reservation context (guest surname, conf #). Same
    risk we already accepted for Wyndham. Bernard already cleared the
    pattern; the EMEA cookie-consent caveat he raised doesn't apply to
    Crown (AU only).
  - **CSP**: if/when we tighten CSP, embedded GTM needs `script-src
    https://www.googletagmanager.com` and `frame-src https://www.googletagmanager.com`.
    Worth filing as a follow-up.
  - **PII through the dataLayer**: GTM will see whatever's in the page
    URL / dataLayer pushes. We should not be pushing guest PII to the
    dataLayer — verify the compendium routes don't expose names in URL
    params before we ship. (The `confirmation` query param is consumed
    and cleared in HotelRoot.vue, but `r` reservation param is also
    handled — check what stays in the URL after init.)
  - **Performance**: extra ~50–100 KB of 3rd-party JS on every compendium
    page load. Acceptable; Wyndham already pays this.

  ### Suggested next action

  Reply to Blake's email with the summary above. Hand back to user — I
  have not sent anything externally.
project: null
source_id: null
tags: []
time_minutes: 5
title: Reply Blake/bonnie/ analytics
updated: 2026-05-11 11:35:00
waiting_on: null
waiting_since: null
working_on: false
---

https://mail.google.com/mail/u/0/#inbox/FMfcgzQgLjWRwnLlgDqrFNgFntdLHrQW

What did we do for Wyndham quantum?

Is it easy to make that generic?