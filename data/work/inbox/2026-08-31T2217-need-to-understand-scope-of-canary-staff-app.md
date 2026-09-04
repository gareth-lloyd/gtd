---
area: null
completed_at: null
contexts: []
created: 2026-08-31 22:17:52.803054
defer_until: null
due: null
energy: low
id: 2026-08-31T2217-need-to-understand-scope-of-canary-staff-app
order: null
output: |
  ## Agent run 2026-09-03T14:05:00

  **Heads-up on the two links in this item:** neither is the staff app. `C0A4EN8SJLA` is
  #wyndham-mobile-app-project (the *guest*-facing Canary SDK embedded in the Wyndham Rewards
  app) and `C09M5GRJPL2` is #epd-mobile (the broader mobile team). The staff app has its own
  channel: **#epd-staff-app** — https://canarytechnologies.slack.com/archives/C0AN8AQ49UG

  ---

  ### 1. Where's the code?

  **`canary-technologies-corp/staff-app-react-native`** — https://github.com/canary-technologies-corp/staff-app-react-native
  (internal repo, *not* in the canary monorepo). React Native on Expo, single codebase for
  iOS + Android. Pushed by James Lovatt on 2026-08-20 as an agentic conversion of the earlier
  native iOS app: "this is far from a finished version, a decent pass of tidy up is needed as
  this was all driven by the agentic conversion"
  (https://canarytechnologies.slack.com/archives/C0AN8AQ49UG/p1787935367405959 area).

  Repo docs are unusually good — read `README.md`, `docs/ARCHITECTURE.md`, `docs/DECISIONS.md`,
  `CLAUDE.md`.

  Shipped artifacts:
  - iOS: "Canary Staff App" — https://apps.apple.com/us/app/canary-staff-app/id6787887995 (released 2026-08-20)
  - Android: `com.canarytechnologies.staff` — https://play.google.com/store/apps/details?id=com.canarytechnologies.staff (passed Google review first shot, live 2026-09-02)
  - Figma: https://www.figma.com/design/hh3BgBESFLGp0ilIR8w9D9/Staff-App

  Backend lives in the monorepo: **`backend/canary/api_gateway/`** (auth + device attestation),
  `backend/canary/chat/views/api_external_mobile_chat/` (messaging), and
  `backend/canary/task_management/` (ticketing + shifts).

  **Don't confuse with:** `frontend/openkey/staff-portal`, `backend/canary/canary_staff`,
  `backend/canary/hotel_staff` — unrelated, all pre-existing.

  ### 2. What does it do?

  Repo one-liner: *"Hotel staff app: guest messaging, service ticketing, and shift management."*
  It's the staff-side counterpart to the guest experience — a phone in a housekeeper's or front
  desk agent's hand instead of the web dashboard.

  Shipped / in-flight feature surface (from `src/app/` route tree):
  - **Guest messaging** — threads, broadcasts (arrivals / departures / in-house), templates,
    search, translation, attachments, guest info. *Live on iOS and Android as of 2026-09-02.*
  - **Service ticketing** — list, detail, create (incl. AI draft + voice), assign, escalate,
    notes, photo attachments. *Next up; QA in progress.*
  - **Shift management** — clock-in / clock-out.
  - Multi-property (`select-property`), settings, 7 languages, dark mode (being disabled per STAFF-95).

  Roadmap sequencing per Mike Hu (PM): **1. Guest messaging Android → 2. Ticketing iOS/Android
  → 3. Housekeeping.** Linear team is **STAFF** (Staff Ops), projects:
  - Service Tickets (Implementation, James Lovatt) — https://linear.app/canary-technologies/project/service-tickets-6f5344a4ea16
  - Housekeeping MVP (Backlog, target 2026-10-30) — https://linear.app/canary-technologies/project/housekeeping-mvp-9a86640f7a7c
  - Internal team messaging (Backlog) — https://linear.app/canary-technologies/project/internal-team-messaging-9f3b44af56d7

  **Commercial driver:** Best Western. Their COO is meant to demo the staff app onstage at the
  BWH convention **26 Oct in Phoenix**, target 500+ properties signing up. That needs ~2 weeks of
  real property testing first, so demo-ready by **~10 Oct**. It's BW's most-requested feature and
  it's a race against HotelKey. Also being pitched to North American indies (Charlie Christou is
  waiting on Caitlyn for the first outbound comms tranche).

  **People:** Mike Hu (PM), James Lovatt (eng lead), Diana Perez Afanador (eng/build/CI),
  Sofya Votchal (QA), Caitlyn Levine (mobile program), Wenjun (design), Marshall (housekeeping
  device strategy), Jake W / Rachel Kim (PMs).

  ### 3. How does it authenticate and make calls?

  **Auth — email/password → HS256 JWT pair, today. No SSO yet.**

  - `POST /api-gateway/v1/auth/login` (`backend/canary/api_gateway/views/staff_login.py`)
    → `{access_token, refresh_token, access_expires_at, refresh_expires_at, user}`.
    Access token 24h, refresh 30d (`api_gateway/services/staff_jwt.py`).
  - JWT is `HS256` signed with Django's `SECRET_KEY`; claims `sub`, `iss`, `iat`, `exp`,
    `username`, `type`. **`iss` is region-suffixed** (`canary-us` / `canary-eu` / `canary-ap`)
    to stop cross-region token replay — which is exactly why the app has a region concept.
  - Tokens stored in the Keychain via `expo-secure-store` (`tokenStore`), never in SQLite.
  - Every call goes through **one** client, `src/api/httpClient.ts`, which adds
    `Authorization: Bearer <access>`, converts snake_case↔camelCase at the boundary, applies a
    30s timeout, and on a 401 does a single coalesced refresh against
    `/api-gateway/v1/auth/refresh` then replays. A token within 30s of expiry refreshes
    pre-emptively.
  - Server side, `StaffJWTGatekeeper` (`backend/canary/api_gateway/gatekeepers.py`) validates it.
    **Deliberately not hotel-scoped** — the token identifies the *user*, who may work across
    several hotels; hotel scoping happens per-endpoint via the slug in the path. Chat has its own
    `MobileChatAuthValidator` that decodes the same `StaffJWT`.

  **Device attestation — a second, separate credential layer.**
  Before login, the app registers the device with the gateway:
  `POST /v1/devices/challenge` → `/v1/devices/register` → `/v1/devices/attest`, on the `api.` host.
  Bootstrap auth is `Bearer <appId>` (a hardcoded per-environment app id in
  `src/config/environments.ts`); after registration it's `Bearer <applicationSid>:<secretKey>`.
  Backed by Apple App Attest through the in-tree `canary-attestation` Expo module — **iOS only**,
  Android gets a no-op stub. A device with a Secure Enclave gets a hardware key; simulator/older
  hardware falls back to software and *the backend sees a lower trust level*.

  **Host / region routing** (`src/config/region.ts`) is the fiddly bit. Host is composed at
  request time from environment + session region under four conventions (`default`/`site`/`api`/
  `secure`), e.g. `eu.canarytechnologies.com`, `api.eu.…`, `secure.api.eu.…`. Note
  `apac` → `ap` in the slug, and `staffEffectiveRegion()` maps **US → null (global host)**,
  because `us.` doesn't route the ticketing prefix and every ticket call against it lands in the
  monolith's HTML 404.

  **The endpoints it actually calls:**
  | Surface | Path |
  |---|---|
  | Auth | `/api-gateway/v1/auth/{login,refresh,me,request-reset}`, `/api-gateway/v1/app/version-status` |
  | Device attestation | `/v1/devices/{challenge,register,attest}` (api. host) |
  | Messaging | `/api/v1/chat/{threads,messages,broadcasts,broadcast_groups,broadcast_guests,message_templates,search,messages/translate}` |
  | Ticketing + shifts | `/api/task-management/v1/<hotel_slug>/{tickets,assignable-staff,escalation-settings,clock-in,clock-out}` |
  | Push | `/v1/push_notifications/staff_device_token` |
  | Real time | Socket.IO at `/ws/fanout/`, token passed in the handshake auth — **chat only** |

  **Architecture worth knowing:** the store *is* the cache. Components never `fetch`. A service
  requests → parses with a zod schema → writes rows into SQLite via Lattice (`@jsflax/lattice`),
  one `.sqlite` file per hotel plus a cross-hotel `app.sqlite`; hooks read back through live
  queries. Reads work offline for free. Only ticket creation queues for offline replay. At rest
  it relies on OS file protection, not app-layer encryption (decision `D40`).

  ### 4. The bit that's actually on your plate: SSO

  **The staff app cannot go GA without SSO** — it's a hard blocker for any Best Western property,
  and Enterprise owns SSO. Caitlyn escalated this to you and Andrea on 2026-08-28:
  https://canarytechnologies.slack.com/archives/C0AN8AQ49UG/p1787935367405959

  Where the thread landed (your own notes in it):
  - **Decided: US-only SSO** — no region picker, no cross-region session. Connor confirmed BW made
    no such ask; the regional-IdP split was Canary's decision, not theirs, and there are no
    property users spanning regions. This descoped the ask significantly.
  - **Decided: two-stage identifier-first login** — identifier screen, then fork to SSO or
    password. Ambiguous email falls back to username. Allow-list of SSO orgs with exactly one
    entry (Best Western); password login stays global and unchanged.
  - **Open: the backend shape of the fork, and who builds it.** Requires globalizing the user
    profile table and the SSO settings table (regional today).
  - Renan Moreira posted a full proposed flow diagram in #eng-identity on 2026-08-31:
    https://canarytechnologies.slack.com/archives/C0BET8YEKB4/p1788203721883719 — global
    `api./v1/login/oauth` → identifier-first page in us-west-2 → parallel server-side fan-out to
    `/internal/login/lookup` in eu-central-1 and ap-southeast-1 → fork to SAML or a regional
    password hop → consent → OAuth code → token exchange, with grants in a global DynamoDB and
    `PrincipalMiddleware` resolving `auth_user_sid` → `global_identity_sid` per region.
  - Deadline: **SSO live by ~10 Oct**. Connor: "we can likely loan an ENT engineer towards this."
  - Connor flagged this to you in DM as "a gap for GA release of staff app".
  - Related scoping project: https://linear.app/canary-technologies/project/phase-2-foundational-services-guest-app-staff-app-white-label-aa26ca2aaa32/overview

  ### Suggested next actions (not taken)
  - Confirm whether ENT is loaning an engineer for staff-app SSO, and who.
  - Close out the open item: backend shape of the identifier-first fork + ownership (you owe
    follow-up notes from the backend design discussion — you said "I have more notes on the
    backend build discussion which I'll share before EOD").
  - Note the attestation asymmetry: App Attest is iOS-only, Android is a no-op stub. Worth
    checking whether that's acceptable for a BW GA where Android is likely the majority of
    property devices.
project: null
source_id: null
tags: []
time_minutes: 5
title: I Need to understand purpose and scope of Canary staff mobile app
updated: 2026-09-03 15:09:36.065562
waiting_on: null
waiting_since: null
working_on: false
---

https://canarytechnologies.slack.com/archives/C0A4EN8SJLA
https://canarytechnologies.slack.com/archives/C09M5GRJPL2

Where's hte code?
What does it do?
How does it authenticate and make calls?