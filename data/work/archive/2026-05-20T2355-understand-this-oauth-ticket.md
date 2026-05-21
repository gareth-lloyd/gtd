---
area: null
contexts: []
created: 2026-05-20 23:55:52.791126
defer_until: null
due: null
energy: low
id: 2026-05-20T2355-understand-this-oauth-ticket
order: null
output: '## Agent run 2026-05-21T13:00:00


  **ENT-6281 — Status: Deployed (PR #45931 merged, completed 2026-05-20)**

  Author: Jordan Sterling. Project: Api Authentication. Team: Enterprise.

  Related: ENT-6207 (added `StaffUser` enum value), ENT-6204 (OAuth login page — your
  branch).


  ### What the ticket did

  Wired `IdentityType.STAFF_USER` into `IdentityService.create()` validation so it
  can actually be used. Before this, the enum value existed (added in ENT-6207) but
  `IdentityService.create()` rejected it with `IdentityReferenceMismatchError` because
  the type was missing from both the `IdentityReference` union and the `_REFERENCE_TYPES_BY_IDENTITY_TYPE`
  runtime validation dict.


  ### What actually shipped (vs. the ticket spec)

  The ticket suggested a `StaffUserReference` dataclass wrapping `username:email`.
  The merged implementation in `backend/canary/api_gateway/services/identity_service.py:30-48`
  differs:


  - Uses `NewType("StaffUserReference", str)` instead of a dataclass — lighter weight,
  but the static type system still distinguishes it from bare `str` so SID-typed identities
  reject it.

  - **Reference is a stable immutable id (profile UUID), NOT `username:email`** —
  explicit code comment says mutable username/email would break the `(type, reference)`
  dedup contract. This is a notable departure from ENT-6207''s spec.

  - Runtime dict entry: `IdentityType.STAFF_USER: (str,)` (Sid is an ABC, not a str
  subclass, so str and SID types don''t cross-accept at runtime).


  ### Why it matters for your work (ENT-6204 OAuth login page)

  This unblocks the login-page flow you''re on: somewhere between login submit and
  `OAuthGrantService.create()`, your code needs to call `IdentityService.create(IdentityType.STAFF_USER,
  StaffUserReference(<profile_uuid>), label=...)` to materialize the staff identity.
  The ticket explicitly calls out that wiring this into the ENT-6204 flow is OUT OF
  SCOPE for ENT-6281 — that''s your job. Permission grants based on StaffUser identity
  are also out of scope.


  ### Action implication

  Heads-up: if your branch (`glloyd/ent-6204-oauth-login-page`) currently constructs
  a `username:email` reference based on the ENT-6207 spec, you''ll need to swap it
  to the profile UUID per the shipped ENT-6281 contract.


  No external writes performed. Read-only research.

  '
project: null
source_id: null
tags: []
time_minutes: 5
title: understand this oauth ticket
updated: 2026-05-21 12:49:07.969001
waiting_on: null
waiting_since: null
working_on: false
---

https://linear.app/canary-technologies/issue/ENT-6281/wire-identitytypestaff-user-into-identityservicecreate-validation