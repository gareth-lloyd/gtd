---
area: null
contexts:
- react
created: 2026-05-14 10:01:39.210950
defer_until: null
due: 2026-05-14
energy: medium
id: 2026-05-14T1001-skim-jordan-s-oauth-applicationservice-refactor-ti
order: null
output: '## Agent run 2026-05-14T13:05:00


  ### TL;DR for the DM

  These are Jordan''s "second part" — pure service-layer plumbing in `backend/canary/api_gateway/`
  that the OAuth work will sit on top of. Three are In Review (6209/6210/6211), one
  is still Todo (6212). All are small, well-scoped, single-author. None of this is
  on the login-page critical path — it''s the foundation for the portfolio-owned Application
  Update API (ENT-6208), which is itself in the looser-deadline OAuth Global Login
  project.


  ### Project split

  - **Api Authentication** project (these four tickets): the CRUD layer refactor on
  `ApplicationService`. Backed by DynamoDB (`ApplicationRecord` is a `msgspec.Struct`,
  not a Django model).

  - **OAuth Global Login** project: ENT-6204 login page (your team''s part), ENT-6205
  code exchange, ENT-6208 Application Update API endpoint. ENT-6212 is the bridge
  — it lives in Api Authentication but is the prerequisite for ENT-6208.


  ### Ticket-by-ticket


  - **ENT-6209** — In Review, PR #45448. Rename `ApplicationCredentialService` → `ApplicationService`
  (file + class). Introduces an `Application` domain dataclass (typed sid, `ApplicationStatus`
  enum, `datetime`, `UUID`) layered above the flat-string DAL `ApplicationRecord`;
  service owns the converter both ways. Splits today''s all-in-one `create_application()`
  into three composable calls — `ApplicationService.create()` writes only the row,
  with `IdentityService.create()` and `AuthTokenService.create_token()` composed at
  the caller. Only one existing caller (a management command). Pure refactor, end
  state identical.


  - **ENT-6210** — In Review, PR #45449. `ApplicationService.get(sid) -> Application
  | None`. Coalesces Dynamo "not found" into `None`. Deliberately does **not** filter
  soft-deleted — `deleted_at` is returned populated; caller filters.


  - **ENT-6211** — In Review, PR #45450. `ApplicationService.update()` for `name`
  and `status` only. Partial-update style (`None` = don''t touch). Validates `len(new_name)
  ≤ 200` (empty string allowed). No-op detection: if diff is empty, skip the PutItem
  and don''t bump `updated_at`. Out of scope: `is_staging` (immutable), `portfolio_uuid`,
  `deleted_at`, `oauth_redirect_url`.


  - **ENT-6212** — Todo, no PR yet. Adds `oauth_redirect_url: list[str]` to the DAL
  `ApplicationRecord` (stored as Dynamo `L` of `S`, missing attribute decodes as `[]`)
  and to the `Application` dataclass, and extends `update()` with `new_oauth_redirect_url`.
  Validation rules (https-only / localhost-http, max 10, max 2048 chars, no fragment,
  no query) are defined in ENT-6208 and enforced in the service layer here. `[]` is
  a valid clear; `None` means don''t touch.


  ### Things worth flagging in the DM

  - 6209–6211 are tight self-contained PRs and should be quick reviews; nothing in
  them touches the OAuth login page surface.

  - The actual coupling point to your team''s work is **ENT-6208** (Application Update
  API endpoint) — it depends on 6212 landing first so the `oauth_redirect_url` field
  exists on the model. Worth confirming with Jordan whether ENT-6208 is also in his
  "second part" bucket or whether you need to coordinate on the endpoint shape that
  the login page (ENT-6204) will read against.

  - The validation rules for `oauth_redirect_url` live in ENT-6208''s spec and the
  service layer (ENT-6212) raises on failure — if the login page does its own redirect_uri
  matching at `/login/oauth` time, it should match exactly the same normalization
  (no fragment, no query, scheme/host comparison) to avoid drift.

  - DynamoDB last-write-wins on update — no optimistic concurrency. Fine for these
  fields but worth knowing.


  ## Agent run 2026-05-15T11:30:00


  ### What changed since last run

  Jordan sent a new DM (2026-05-15 07:35 EEST). The ask is now specific: **ENT-6204
  (OAuth Login Page) is the only ticket left** and the only one for our team. He wants
  it either (a) assigned and worked tomorrow, or (b) at minimum reviewed and put into
  a "claude-ready" state so he can just say "claude go". He explicitly does not know
  the Canary login part — that is exactly the domain knowledge gap the Enterprise
  team is being asked to cover. Everything else is in review and expected to land
  soon.


  ### OAuth Global Login project state (2026-05-15)

  Project status: Eng Design, started 2026-05-14, no target date. Flagged "Phase Future"
  in the design doc — NOT on the Feb/Mar IHG rollout, no committed date.

  - ENT-6201 — implementation tracker — **Canceled** (2026-05-14).

  - ENT-6207 — Add StaffUser to IdentityType enum — **Deployed / done**.

  - ENT-6202 — application_secrets table + service + CRUD — **In Review** (Jordan).

  - ENT-6203 — oauth_grants table + OAuthGrantService — **In Review** (Jordan). Dependency
  of 6204.

  - ENT-6205 — OAuth Authorization Code Exchange API — **In Review** (Jordan).

  - ENT-6206 — Refresh Token API — **In Review** (Jordan).

  - ENT-6208 — Application Update API (registers oauth_redirect_url) — **In Review**
  (Jordan). Dependency of 6204''s redirect_uri exact-match check.

  - ENT-6204 — OAuth Login Page — **Backlog, UNASSIGNED** ← the one for our team.

  Sibling Api Authentication project: ENT-6209/6210/6211 In Review, ENT-6212 Todo
  (the ApplicationService plumbing reviewed in the previous run).

  Net: Jordan''s entire side is in review. The only outstanding build is ENT-6204.


  ### Review of ENT-6204 — is it "claude-ready"? Mostly, but NOT yet.

  Well-written parts: clear validation order, explicit failure paths (no redirect
  / no info leak on bad app or redirect_uri), RFC references, concrete test list,
  good scope fencing (PKCE and scopes explicitly deferred).

  Blockers to resolve before "claude go" — all in the login domain Jordan flagged
  as unknown to him, i.e. our value-add:

  1. **Hostname is wrong/ambiguous.** Goal says "dashboard hostname" but the URL example
  uses `https://www.canarytechnologies.com/login/oauth` — that is the marketing site,
  not the staff dashboard host. Needs the real host pinned before anyone codes routing.

  2. **Build-vs-reuse decision is unmade and is OURS to make.** Jordan explicitly
  punts: "i know nothing about the Canary login page and it scares me... if you are
  an expert, up to you if you want to reuse it." The ticket assumes "same Django/template
  stack as existing staff login, leverage existing MFA components" — but if the staff
  login is actually the Vue SPA, that assumption is wrong and the whole approach changes.
  Someone who knows canary auth must verify the staff login stack and identify the
  reusable MFA (TOTP/SMS/email) components before this is claude-ready.

  3. **MFA enrollment vs verification unspecified.** If an authenticating staff user
  has no MFA configured, does the page force enrollment or let them through? Should
  mirror existing staff-login behavior — needs a domain answer.

  Minor: IdentityRecord reference `f"{username}:{email}"` is mutable on both halves
  (fine for v1, worth a note); "standalone error page" location/look undefined; 6204
  can be built in parallel against 6203/6208 interfaces but cannot be end-to-end tested
  until both land.


  ### Recommendation (for your decision — nothing actioned)

  ENT-6204 is close but needs ~30 min from someone with canary staff-login/auth knowledge
  to (a) make the reuse-vs-new-page call, (b) pin the real host, (c) answer the MFA-enrollment
  question. After that it is genuinely "claude go". I have NOT changed the Linear
  assignee/status or replied to Jordan — assignment and the DM reply are your calls.
  Say the word and I''ll draft the Slack reply and/or a Linear comment with these
  three questions for you to review before anything is sent.


  ## Agent run 2026-05-15T12:15:00 — ENT-6204 open-question investigation


  Investigated the canary codebase. Three of the earlier "blockers" resolve; one new,
  more important one surfaced.


  ### Q1 — Stack: reuse is VIABLE; ticket''s assumption is correct

  Staff/hotel login is a server-rendered Django template flow, NOT a Vue SPA: `login_view`
  at backend/canary/hotels/views/views.py:248; route `^login/$` at hotels/urls.py:44;
  template hotels/templates/login.html; `LoginForm` + `authenticate()`; post-auth
  orchestration `redirect_after_login` (views.py:426) → `verify_2fa_code` (views.py:356).
  A new Django-template page at `/login/oauth` can reuse all of this directly. ENT-6204''s
  "same Django/template stack, leverage existing MFA components" is CORRECT.


  ### NEW critical wrinkle — is_staff users bypass password auth entirely

  views.py:297-302: if the resolved user has Django `is_staff=True`, login_view force-redirects
  to **Google OAuth** (`GoogleUserService.get_google_oauth_url`), never password+MFA.
  Terminology collision in the OAuth tickets: ENT-6207/6204 call the principal a "StaffUser"
  / "Canary hotel staff user", but a *hotel* employee is a `CompanyHotelUser`, NOT
  Django `is_staff`. Django `is_staff` = Canary internal/support employees.

  - If the OAuth login page targets hotel employees → password+MFA reuse is clean,
  no problem.

  - If it must also cover Canary internal (`is_staff`) users → those go through Google
  OAuth only; the password+MFA path and the `reference=f"{username}:{email}"` IdentityRecord
  construction in the ticket do not apply to them and need rethinking.

  This is THE open question to put to Jordan before "claude go" — it determines whether
  the page is a straight reuse or needs a Google-OAuth branch.


  ### Q2 — MFA components (reusable as-is)

  Methods: EMAIL (default fallback), SMS, TOTP (user_profile.py:26-29). Verification
  is a separate authenticated step: `verify_2fa_code` (views.py:356), GET sends code
  / POST checks. Service: `MultiFactorAuthenticationService.send_mfa_code` / `check_mfa_verification`
  (multi_factor_authentication.py:141 / 184). Gating: `request_has_mfa_if_required`
  (line 42) + `redirect_after_login`. "Remember this device" 30-day `KnownDeviceToken`
  cookie can skip MFA; 30-min lockout after repeated failures.


  ### Q3 — MFA enrollment: NOT a blocker

  MFA is conditional, never a hard enrollment wall. `user_requires_mfa` (multi_factor_authentication.py:81)
  is True only if one of the user''s hotels has `require_mfa=True` (default False)
  OR the user holds a `REQUIRES_MFA_PERMISSIONS` permission. When required but nothing
  is set up, `check_mfa_verification` falls through to the SMS/email code path and
  `preferred_2fa_method` defaults to EMAIL — every user has an email, so a code is
  always deliverable. TOTP only applies if the user explicitly verified a device.
  No separate "enroll MFA" UI to design.


  ### Q4 — Hostname: ticket is CORRECT (my earlier concern was wrong)

  Production `SITE_URL = https://www.canarytechnologies.com` (settings/production_base.py:16,
  env-overridable); `ALLOWED_HOSTS=["*"]`. The Django app including `/login/` is served
  from www.canarytechnologies.com — there is no separate dashboard subdomain for staff
  login. So `https://www.canarytechnologies.com/login/oauth` is the right host. Resolves
  my prior "hostname looks wrong" flag.


  ### Net for ENT-6204

  Resolved: hostname correct, stack reuse viable, MFA enrollment a non-issue. Remaining
  real open question: the **is_staff / Google-OAuth divergence + the "StaffUser" terminology**
  — confirm intended audience (hotel employees only vs. also Canary internal staff)
  with Jordan; that single answer makes the ticket genuinely "claude go" or expands
  its scope. Minor implementer notes: reuse-vs-fork the login template, IdentityRecord
  reference stability, standalone error page look/location.


  ## Agent run 2026-05-15T12:55:00 — posted context to Linear


  Posted the investigation findings + the three open mobile/webview questions as a
  COMMENT on ENT-6204 (comment id 5de059ef-ccfe-4209-8237-3cfaecc73b62, authored as
  Gareth Lloyd). Original ticket description left untouched per instruction. Webview
  check added: page renders fine in a webview (server- rendered forms, no JS; SESSION_COOKIE_SAMESITE="None"+Secure
  already set in production_web.py:9-10) — real concerns are redirect_uri scheme vs
  ENT-6208 validation, PKCE deferral for a mobile public client, and embedded-webview
  vs system-browser (RFC 8252). is_staff question resolved by user: is_staff = Canary
  employee, hotel staff never is_staff, so password+MFA reuse is clean. No Slack reply
  sent to Jordan.

  '
project: 2026-04-10T0840-ticket
source_id: https://linear.app/canary-technologies/issue/ENT-6211/applicationserviceupdate-for-name-status
tags:
- morning-gtd
- linear
- from-awareness
time_minutes: 20
title: REview Oauth project and assign outstanding work
updated: 2026-05-15 15:58:07.227345
waiting_on: null
waiting_since: null
working_on: false
---

Jordan: oauth work is 2 sides — one ticket (login page) for my team, second part (portfolio-owned APIs) on his side, looser deadline. https://canarytechnologies.slack.com/archives/D07HCMQU5FY/p1778710486268839