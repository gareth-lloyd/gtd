---
area: null
contexts: []
created: 2026-06-10 14:53:20.209903
defer_until: null
due: null
energy: low
id: 2026-06-10T1453-investigation-what-would-it-look-like-to-swap-our
order: null
output: |
  ## Agent run 2026-06-10T14:59 (local)

  Investigated swapping Canary's in-house SSO and Events (audit logging) for WorkOS,
  per Blake's question in #eng-leadership Slack thread. Three research tracks: codebase
  map of sso/, codebase map of event/, and WorkOS product/pricing research (verified
  against workos.com/pricing and docs, June 2026).

  ### TL;DR

  - **SSO: plausible swap, moderate effort (~2-4 wks), but weak ROI at our current
    scale (~5-10 active connections).** The win is operational (self-serve IdP setup
    via WorkOS Admin Portal, no more python3-saml/xmlsec/cert maintenance), not cost.
    Worth it only if we expect a wave of new enterprise SSO deals.
  - **Audit logging: do NOT swap.** Our Events system is not just an audit log — it's
    an internal event bus feeding product features. WorkOS Audit Logs is an append-only
    sink and cannot replace it. At most, WorkOS could be an *additive* enterprise
    SIEM-export feature.

  ### What we have today

  **SSO** (`backend/canary/sso/`, ~16K LOC incl. migrations, 111 files, 26 test files):
  - SAML 2.0 only, SP-initiated only, via python3-saml. No OIDC, no IdP-initiated, no SCIM.
  - `Organization` model (45+ fields) per brand IdP; provisioned manually via Django admin
    by engineers — no self-serve.
  - The bulk of the code is NOT protocol plumbing: it's JIT user/hotel provisioning,
    role mapping (property/portfolio), account merging, BW-style multi-region portfolio
    scoping, email-domain limits, blocked users, diagnostic logging. All of that is
    protocol-agnostic and survives any swap.
  - MFA is bypassed for SSO sessions; Zendesk one-way user sync hooks login.

  **Events** (`backend/canary/event/` + ~510 spec files across 29+ apps):
  - ~499 event types; actor + impersonator chain + target + ancestor chain + payload;
    separate event database; SQS FIFO async pipeline; no retention/purge (append-only).
  - 14 synchronous `register_event_created` handlers drive real product behavior:
    segmentation re-evaluation, auto check-in, message scheduler, chat room queue,
    authorization sync, contracts notifications.
  - Customer-facing audit views (reservations, payment links, registration cards, F&B,
    compendium...) rely on per-spec `hydrate()` that batch-loads related objects from
    our DB for display, with i18n event text templates.

  ### What WorkOS offers (verified June 2026)

  - **Standalone SSO API** (separate from AuthKit): OAuth-style redirect → callback code
    → normalized profile. We keep our own user model/sessions. Organization = tenant
    primitive (one per brand IdP — NOT per hotel, so economics scale fine). Handles
    SAML+OIDC, IdP-initiated, cert rotation. Admin Portal lets the customer's IT team
    self-configure their IdP with guided walkthroughs.
  - **Pricing**: NO free SSO tier ("1M users free" is AuthKit user management only).
    SSO per active connection/mo, tiered $125 (1-15) down to $50 (101-200), 201+ custom.
    At our ~5-10 connections: ~$7.5-15k/yr — trivial. At 50 connections ~$60k/yr list.
  - **Audit Logs**: org-scoped events (action/actor/targets/context/metadata), schemas
    must be pre-registered in their dashboard, retention 30d default / up to 365d,
    $99/mo per 1M events retained + $125/mo per SIEM log-stream connection. Embeddable
    per-customer audit viewer via Admin Portal; Log Streams to customer's own
    Splunk/Datadog/S3/Sentinel.
  - **Migration support**: documented homegrown→WorkOS playbook, proxy approach (our ACS
    URL forwards to WorkOS so customer IdPs never need reconfiguring), CSV bulk import
    of existing connections/certs.
  - **Risks/gaps**: US-only data residency (no EU region — DPA confirms; we run EU
    deployments, so this needs legal/customer review). SOC 2 Type II yes; ISO 27001
    unconfirmed. ~3 incidents/mo on status trackers; 99.99% SLA only on enterprise
    contracts. An SSO vendor outage = enterprise login outage.

  ### SSO swap assessment

  What changes: `sso_login`/`saml_acs`/`saml_metadata` views → WorkOS SDK redirect +
  callback; drop python3-saml/xmlsec; deprecate cert/binding/NameID fields on
  Organization. What stays: ~all of SSOOrganizationService (provisioning, role/hotel
  mapping, merge, portfolio logic) — just fed from a WorkOS profile instead of parsed
  SAML. Effort ~2-4 weeks + per-customer config validation.

  Honest take: the system is built, working, and serves ~5-10 connections. Swapping
  buys self-serve onboarding for FUTURE brands, OIDC support, and removal of crypto
  maintenance surface — at the cost of a migration project, a new vendor dependency in
  the login path, and a US-residency question for EU customers. Recommend: not now,
  unless sales pipeline shows many SSO-requiring deals; revisit as "adopt WorkOS for
  new connections only" if onboarding friction becomes a bottleneck.

  ### Audit logging swap assessment

  Not a fit as a replacement:
  1. Events is a product event bus, not just audit — WorkOS has no callbacks/handlers,
     so segmentation, auto check-in, message scheduling etc. would all need a new bus.
  2. Customer audit views depend on hydration of related objects from our DB + i18n
     templating; WorkOS's viewer can't do either.
  3. Impersonation chains and ancestor chains don't map to WorkOS's flat actor/target
     schema; 499 event types would need schema registration in their dashboard.
  4. Volume cost ($99/mo per 1M events retained) on a high-volume append-only table
     (it has its own database) likely exceeds what we pay to store it ourselves, for
     strictly less capability.

  Where WorkOS *could* add value: their per-org Log Streams (customer's IT streams
  their own audit events to their own Splunk/Sentinel) is an enterprise feature we
  don't have. If Wyndham/BW/IHG security teams ever ask for SIEM export, options are
  (a) dual-emit a curated security-relevant subset of events to WorkOS Audit Logs as
  an add-on, or (b) build export ourselves. Neither is urgent.

  ### Open items / unverified

  - WorkOS tier pricing marginal vs whole-count not stated officially; 201+ is
    sales-only. EU residency gap confirmed as of June 2026 but roadmap may change.
  - Drafted no Slack reply; happy to draft a response to Blake's thread on request.
  Sources: workos.com/pricing, /docs/sso, /docs/audit-logs, /docs/admin-portal,
  /docs/migrate, /security, status.workos.com.
project: null
source_id: null
tags: []
time_minutes: 5
title: 'investigation: what would it look like to swap our SSO and audit logging (Events)
  for work os'
updated: 2026-06-10 16:47:01.143289
waiting_on: null
waiting_since: null
working_on: true
---

https://canarytechnologies.slack.com/archives/C02MVAEJD0Q/p1781092277820879