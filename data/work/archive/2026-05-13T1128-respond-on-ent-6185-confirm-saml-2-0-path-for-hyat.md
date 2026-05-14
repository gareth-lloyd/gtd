---
area: engineering
contexts:
- react
created: 2026-05-13 11:28:24.356904
defer_until: null
due: 2026-05-13
energy: low
id: 2026-05-13T1128-respond-on-ent-6185-confirm-saml-2-0-path-for-hyat
order: null
output: '## Agent run 2026-05-13T14:20Z


  **Verified Canary''s SAML 2.0 support before drafting:**

  - `backend/canary/sso/` is a SAML 2.0 SP built on python3-saml — bindings, NameID
  formats, ACS, metadata endpoints all SAML 2.0.

  - Azure AD is an explicitly handled IdP (`organization.py:336` — option to disable
  `RequestedAuthnContext` for Azure).

  - SP endpoints are slug-scoped per org: `/sso/saml/acs/<slug>` and `/sso/saml/metadata/<slug>`.

  - Attribute model the IdP needs to assert: `email` (NameID emailAddress), `roles`,
  `hotels` (list of `sso_hotel_id`), optionally `hotel_roles`, plus first/last name.


  **Draft Linear comment for Andres (NOT POSTED — awaiting approval):**


  ---

  Confirmed — **SAML 2.0 is the correct path** for Hyatt. Canary''s SSO is a SAML
  2.0 SP (python3-saml under the hood) and Azure AD / Entra ID is already a supported
  IdP for other enterprise customers. We do not currently expose an OIDC SP, so SAML
  is also the only path.


  Olympia can tell Tilynn to proceed with the Azure AD SAML 2.0 enterprise-app setup.
  Once their Identity Management team is engaged, we''ll need from them:


  1. **IdP metadata XML** (or, equivalently: Entity ID / Issuer, SSO URL, and signing
  X.509 cert).

  2. **NameID format** — `emailAddress` (`urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress`).

  3. **Attribute assertions** — at minimum `email`, `firstName`, `lastName`; plus
  `roles` and `hotels` (list of Canary `sso_hotel_id`s the user can access). `hotel_roles`
  is supported if they want per-hotel role granularity.

  4. **Confirmation** of whether they want JIT provisioning, password-login fallback,
  and how hotel access is managed (IdP-driven via `hotels` attribute vs. Canary-side).


  We''ll send them our **SP metadata URL** (one per SSO org slug — `https://<site>/sso/saml/metadata/<slug>`)
  and Entity ID once we create the SSO organization in canary-admin. Standard runbook:
  [Hotel SSO Onboarding](https://www.notion.so/a40a4042b4504183a51a3785ac9e612f).


  Happy to join the kickoff call with Hyatt IdM when it''s scheduled.

  ---


  **Next:** Gareth to review/edit the draft, then post to ENT-6185 manually (or approve
  me to post via Linear MCP).

  '
project: 2026-04-16T1210-unblock-team
source_id: https://linear.app/canary-technologies/issue/ENT-6185/hyatt-create-sso-azure-saml
tags:
- morning-gtd
- linear
time_minutes: 5
title: 'Respond on ENT-6185: confirm SAML 2.0 path for Hyatt SSO'
updated: 2026-05-13 14:37:39.635709
waiting_on: null
waiting_since: null
working_on: false
---

Andres asked: 'no SLA but High-Priority ASAP — confirm SAML 2.0 is the correct path.' https://linear.app/canary-technologies/issue/ENT-6185/hyatt-create-sso-azure-saml