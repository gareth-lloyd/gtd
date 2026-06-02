---
area: null
contexts:
- react
created: 2026-05-31 07:45:57.217937
defer_until: null
due: null
energy: low
id: 2026-05-31T0745-triage-ent-6365-support-creating-auth-credential-p
order: null
output: |
  ## Agent run 2026-06-01T13:48:39Z — Triage of ENT-6365

  **Ticket:** Support creating Auth Credential Pairs for mobile apps (Enterprise,
  Medium, still in Triage). Created by Andrea (from Luiza's report). Comment thread:
  Andrea cc'd @glloyd @laura → Laura cc'd @sbarry. No other discussion yet.

  ### What's actually being asked
  Luiza (api-gateway) has to hand-mint a new Application + auth-token credential pair
  every time the mobile team onboards a new hotel. Today she does this via `shell-plus`
  calling the services directly. The two "easy" paths are both broken for prod use:
  - The normal HTTP/API path errors with a **DynamoDB no-permission** error.
  - The `create_application` management command is **staging-only** AND **leaks the
    secret to Datadog**.

  AC framed as two questions: (1) should mobile own this? (2) build a Django-admin flow?

  ### Codebase grounding (so the scoping is concrete)
  - Credentials live in **DynamoDB, not the Django ORM**. App `backend/canary/api_gateway/`.
    Records defined in `backend/shared/shared/aws/public_api_dynamo_db.py`
    (`ApplicationRecord`, `AuthTokenRecord`, `IdentityRecord`). Token secret is stored
    SHA3-512 hashed — the plaintext secret only exists at creation time, so it must be
    surfaced to the caller exactly once and never persisted/logged.
  - Creation sequence already exists and is small — see
    `api_gateway/management/commands/create_application.py:20-48`:
    `ApplicationService.create(is_staging=...)` → `IdentityService.create(...)` →
    `AuthTokenService.create_token(...)`, then assemble `f"{application_sid}:{secret}"`.
  - **The Datadog leak is right there**: `create_application.py:43-48` logs
    `credential_pair=...` (full plaintext secret) via structlog → Datadog. Bug regardless
    of how this ticket lands.
  - **Staging is a hardcoded flag**, not a separate path: command passes `is_staging=True`,
    which yields a `StagingApplicationSid` (`app_staging_` prefix vs prod `app_`).
    Prod only needs `is_staging=False`.
  - **DynamoDB permission error explained**: writes go through
    `ApiGatewayDynamoDbSelector.save_auth_token` →
    `api_gateway_dynamo_db_selector.py:185-186`. The backend service has the IAM role to
    write the DynamoDB tables (applications / auth-tokens / identities); ad-hoc/local
    shells and the API caller don't. **An in-service Django-admin flow runs with the
    service's IAM creds, so it sidesteps the permission error cleanly** — this is the
    strongest argument for the admin approach.
  - **Admin scaffold already exists** for the sibling entity: `api_gateway/admin_views.py`
    has `identity_lookup_view` / `identity_create_view` / `identity_change_view` with
    forms + templates. An "Application + credential pair" creator follows the exact same
    pattern — low lift.

  ### Recommendation (for triage out of Triage)
  Build it as a **Django-admin flow in `api_gateway`**, not mobile-owned tooling, and
  NOT a CLI command for prod secrets. Rationale:
  - Solves the DynamoDB permission problem for free (runs as the service).
  - Reuses the existing identity-admin scaffold + the 3-call service sequence already
    proven in `create_application.py`.
  - Lets the secret be displayed **once in the UI response** and never logged — fixes the
    Datadog-exposure concern by construction.
  - Ownership: creation lives in **canary backend / api-gateway (Enterprise's area)**, not
    mobile — mobile *consumes* credentials. An admin UI lets Luiza/support self-serve
    without engineer shell access, which is the real pain point.

  Concrete scope if it's greenlit:
  1. Add `application_create_view` (form: name, `is_staging` toggle) that runs the
     create_application sequence and renders the credential pair once in the template.
  2. Fix `create_application.py:43-48` to stop logging `credential_pair` (drop the field
     or print to stdout only) — do this even if the admin flow slips.
  3. Decide who can see the admin page (staff perm gating).

  ### ⚠️ Open question to flag before estimating
  The ticket says "new credentials every time they integrate with a **new hotel**," but
  Applications/credentials are currently **global — not hotel-scoped** (any `app_` SID can
  hit any hotel; staging keys are restricted to `staging-` hotels by a separate
  enforcement). So "per-hotel credential" may be a *new requirement*, not just an
  ergonomics fix. Worth confirming with Luiza/mobile whether they want (a) just an easier
  way to mint global app credentials, or (b) genuinely hotel-scoped credentials — (b) is a
  meaningfully larger change to the data model/enforcement.

  ### Suggested next step
  Low-effort feature; existing scaffold + services make the admin flow small. Confirm the
  hotel-scoping question above, then move out of Triage into the Enterprise backlog (not
  mobile). I did NOT post anything to Linear — drafting a comment is available on request.
project: null
source_id: https://linear.app/canary-technologies/issue/ENT-6365/support-creating-auth-credential-pairs-for-mobile-apps
tags:
- morning-gtd
- linear
time_minutes: 10
title: 'Triage ENT-6365: Support creating Auth Credential Pairs for mobile apps'
updated: 2026-06-02 13:28:58.812062
waiting_on: null
waiting_since: null
working_on: false
---

Andrea cc'd @glloyd @laura; still in Triage.
https://linear.app/canary-technologies/issue/ENT-6365/support-creating-auth-credential-pairs-for-mobile-apps