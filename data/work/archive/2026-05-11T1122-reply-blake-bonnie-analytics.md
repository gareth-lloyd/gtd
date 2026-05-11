---
area: null
contexts: []
created: 2026-05-11 11:22:17.226474
defer_until: null
due: null
energy: low
id: 2026-05-11T1122-reply-blake-bonnie-analytics
order: null
output: "## Agent run 2026-05-11T11:35\n\nThread is Crown Resorts asking Canary to
  embed their Google Tag Manager\ncontainer (GTM-WJTX3ZWW) on the digital compendium
  pages hosted on\ncheckin.crownresorts.com.au, so they can do cross-domain attribution
  from\nthe in-room QR code into Crown websites + Seven Rooms. Pilot launches at\nCrown
  Promenade Melbourne 18 May 2026. Blake is asking whether to scope\nthis narrowly
  (just GTM) or build a generic \"embed analytics scripts\"\ncapability. Connor flagged
  that we already did this for Wyndham\n(\"Quantum Metric\"). Bonnie wants to commit
  to Crown by Fri 15 May.\n\n### What we did for Wyndham Quantum Metric\n\nFrontend-only,
  ~15 lines, all in `frontend/guest/src/views/HotelRoot.vue`\n(lines 113–130). It
  hard-codes a single script URL and gates it on\nportfolio + feature flag:\n\n- `QUANTUM_METRICS_SRC
  = \"https://cdn.quantummetric.com/qscripts/quantum-wyndham.js\"`\n- Loaded once,
  when both:\n  - `getFeatureValue(Features.ROLLOUT_QUANTUM_METRICS_WYNDHAM)` is true,
  **and**\n  - `isWyndham(hotel)` (i.e. `hotel.portfolio_identifiers` includes `WYNDHAM`).\n-
  Uses the existing `shared/helpers/loadScript` helper, which appends a\n  `<script
  src=…>` tag to `<head>` once and caches the promise globally.\n- Scope is the guest-facing
  Compendium SPA only (not check-in,\n  authorizations, hotels app, etc.) — exactly
  the limit Connor described.\n\nSo: portfolio-scoped feature flag + hard-coded URL
  + portfolio predicate.\nNo backend, no admin UI, no config, no per-hotel anything.
  Wyndham gets\ntheir own Quantum-Metric tenant bundled into one script and we just
  inject\nit.\n\n### Is it easy to make generic?\n\nTwo answers depending on what
  \"generic\" means:\n\n**(a) Same shape for Crown (one-off, ships fastest, ~half
  a day):** copy\nthe Wyndham block with `ROLLOUT_CROWN_GTM_TRACKING` + `isCrown(hotel)`\n(the
  helper already exists in `shared/helpers/hotel.ts`) + Crown's GTM\nloader URL. **Caveat:**
  Google Tag Manager normally ships in two pieces —\nan inline `<head>` bootstrap
  script and a `<noscript><iframe>` after\n`<body>`. Our `loadScript` helper only
  does the first. For an SPA like the\ncompendium, the `<noscript>` fallback is largely
  cosmetic (no JS means the\napp never renders anyway), so we can probably skip it,
  but Crown should\nconfirm. If they insist on the iframe we'd need a tiny helper
  to inject\nit.\n\n**(b) Properly generic \"embed analytics scripts\" feature (~2–4
  days):**\ntable-driven config (per hotel or per portfolio) of script URLs to embed,\nwith
  optional support for inline GTM bootstrap + noscript iframe, and an\nallow-list
  of trusted CDNs so we don't sign up to debug every customer's\nbroken tracking pixel.
  Probably worth doing once if Blake is right that\nmore Enterprise customers will
  ask — which feels likely, GTM/analytics\nembedding is a stock Enterprise digital-team
  ask.\n\n### My recommendation to Blake\n\n- This belongs in **Enterprise**, not
  In-Stay. It's a request from a\n  corporate digital-marketing team for cross-domain
  attribution; same\n  shape and stakeholder profile as the Wyndham Quantum work.
  In-Stay is\n  about the in-stay guest experience, not Crown's marketing pipeline.\n-
  For the **15 May commitment**: confidently yes, we can ship the\n  Wyndham-shaped
  one-off (`isCrown` + flag + GTM bootstrap) within the\n  pilot window. The cheap
  path is well-trodden.\n- But flag two things to Crown:\n  1. The `<noscript>` iframe
  piece — confirm they're okay without it on\n     an SPA.\n  2. Their Step-1 snippet
  uses an **inline** `<script>` block that\n     defines a function and references
  `window.dataLayer`. We don't\n     currently allow inline analytics scripts (our
  `loadScript` only\n     handles `<script src=…>`). Either we adapt to inject it
  inline, or\n     we host the equivalent bootstrap ourselves and just load it via\n
  \    URL. Worth a 10-min call between our dev and Meeno to settle.\n- Decide separately
  whether to commit to (b) — the generic version — as\n  a follow-up. If Blake wants
  to position this as a repeatable\n  Enterprise capability (\"Embedded customer analytics\"),
  it's worth\n  the extra few days. If Crown is one-of-one for now, mirror Wyndham.\n\n###
  Risks worth naming in the reply\n\n- **Security**: 3rd-party scripts get full DOM/cookie
  access to a page\n  that may include reservation context (guest surname, conf #).
  Same\n  risk we already accepted for Wyndham. Bernard already cleared the\n  pattern;
  the EMEA cookie-consent caveat he raised doesn't apply to\n  Crown (AU only).\n-
  **CSP**: if/when we tighten CSP, embedded GTM needs `script-src\n  https://www.googletagmanager.com`
  and `frame-src https://www.googletagmanager.com`.\n  Worth filing as a follow-up.\n-
  **PII through the dataLayer**: GTM will see whatever's in the page\n  URL / dataLayer
  pushes. We should not be pushing guest PII to the\n  dataLayer — verify the compendium
  routes don't expose names in URL\n  params before we ship. (The `confirmation` query
  param is consumed\n  and cleared in HotelRoot.vue, but `r` reservation param is
  also\n  handled — check what stays in the URL after init.)\n- **Performance**: extra
  ~50–100 KB of 3rd-party JS on every compendium\n  page load. Acceptable; Wyndham
  already pays this.\n\n### Suggested next action\n\nReply to Blake's email with the
  summary above. Hand back to user — I\nhave not sent anything externally.\n"
project: null
source_id: null
tags: []
time_minutes: 5
title: Reply Blake/bonnie/ analytics
updated: 2026-05-11 14:17:51.512856
waiting_on: null
waiting_since: null
working_on: false
---

https://mail.google.com/mail/u/0/#inbox/FMfcgzQgLjWRwnLlgDqrFNgFntdLHrQW

What did we do for Wyndham quantum?

Is it easy to make that generic?