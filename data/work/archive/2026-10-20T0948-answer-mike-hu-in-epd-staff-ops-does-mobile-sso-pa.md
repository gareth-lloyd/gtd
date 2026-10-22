---
area: null
completed_at: 2026-10-20 14:39:11.829036
contexts:
- react
created: 2026-10-20 09:48:30.169812
defer_until: null
due: 2026-10-20
energy: medium
id: 2026-10-20T0948-answer-mike-hu-in-epd-staff-ops-does-mobile-sso-pa
order: 2
output: |
  ## Agent run 2026-10-20 10:08:56.348266

  ### Answer (short)
  Mostly yes. A picker that links straight to the SSO page works for IHG, Hyatt, Marriott and Wyndham
  with no backend change, because the per-org allow-list only gates the identifier lookup, not the SSO
  page. Two caveats: US-region-only still applies, and a direct link bypasses the allow-list that was
  our rollout control.

  ### How the two paths differ (verified in code, master as of 2026-10-20)
  - Identifier-first path (what the app does today): `LoginLookupService.route`
    (backend/canary/hotels/services/login_lookup.py:34) only returns SSO when the user's org slug is in
    `settings.SSO_LOGIN_ALLOW_LIST` (canary/settings/base.py:2082, env var, no code). Per James Lovatt
    2026-09-23 the prod list is bestwestern (BW Lab), best-western (BW Prod), canary-sso-test
    (https://canarytechnologies.slack.com/archives/C0AN8AQ49UG/p1790159717134059). That is the
    "config change" for Wyndham: add `wyndham` to the list. Same for any other brand.
  - Direct link path (Mike's picker design): the app opens
    `/sso/login/<slug>?next=/login/oauth/?client_id=...&code_challenge=...` (the same URL
    `_sso_login_url` builds in api_gateway/views/oauth_authorize_challenge.py:363). `sso_login`
    (sso/views/views.py:140) checks only is_enabled + IdP configured (issuer, sso_url, cert). After the
    SAML ACS, the RelayState lands on `/login/oauth/`, which auto-arms the grant for any application in
    `STAFF_APP_APPLICATION_SIDS` (hotels/views/views.py:410) with no org check. So no allow-list entry
    is needed on this path.

  ### Per-brand state in US prod
  - Wyndham: live SAML org `wyndham`, ~310 SSO logins in the last 3h on us-west-2 (plus ~60 on
    eu-central-1). Not on the allow-list.
  - IHG: live org `ihg` (admin id 347, 2,174 hotels), ~61 logins/3h US plus ~9 EU. Configured to allow
    SSO or password; Renan's lookup change returns SSO_OR_PASSWORD for that case. Sandbox org 346 also
    exists. Not on the allow-list.
  - Hyatt: org `hyatt` (Azure SAML, ENT-6185 done Sept 2026), plus `hyatt-sandbox`. 3-hotel pilot, no
    logins in the sampled 3h window, so quiet rather than broken.
  - Marriott: org `marriott`, 2 SSO logins in the last 3h on us-west-2, so the cert-expiry risk Lauta
    flagged on 2026-09-24 (cert expired Oct 10) did not take their login down.

  ### Caveats to state in the reply
  1. US-only still applies regardless of brand: token exchange is pinned to us-west-2 and
     `StaffOAuthTokenService.resolve` resolves the user "in this region" only
     (api_gateway/services/staff_oauth_token_service.py:18). Wyndham and IHG both have EU users signing
     in via SSO today; those accounts fail natively until APAC-144
     (https://linear.app/canary-technologies/issue/APAC-144/roll-out-staff-app-sso-globally).
  2. The allow-list was the rollout control. A direct link bypasses it. Fine if we open to all SSO orgs
     (Connor said yes in-thread), but then the picker is the de facto allow-list, so the backend should
     serve the org list (slug, display name, prod vs sandbox) rather than the app hardcoding slugs.
     Small backend piece; also choose prod vs sandbox per brand (IHG and Hyatt have both).
  3. Same hygiene as web: the profile needs sso_organization + sso_name_id, role/hotel mappings must
     resolve. Nothing mobile-specific.

  ### Draft Slack reply (NOT sent; thread
  https://canarytechnologies.slack.com/archives/C0AN8AQ49UG/p1792448760833769?thread_ts=1792018248.856969&cid=C0AN8AQ49UG)

  Mostly yes, with two caveats.

  Today the app sends the identifier to the lookup, and we only route to SSO if the user's org is on
  `SSO_LOGIN_ALLOW_LIST` (currently BW lab, BW prod, canary-sso-test). That's the per-brand config
  change: one env var entry per org slug, no code.

  If the picker links straight to the SSO page (`/sso/login/<slug>?next=<oauth authorize URL>`), the
  allow-list doesn't apply. The SSO page only checks the org is enabled with an IdP configured, and the
  return leg into the app is keyed on the app's client id, not the org. So IHG, Hyatt, Marriott and
  Wyndham would all work from the picker with no backend change. All four have live SAML orgs in US
  prod (Marriott and IHG logged SSO logins in the last few hours; Hyatt is a 3-hotel pilot, so quiet).

  Caveats:
  1. US region only still applies. Token exchange and user resolution are pinned to us-west-2, so an
     EU/AP account can't sign in natively whatever the brand. IHG and Wyndham both have EU users on SSO
     today; they'd fail on mobile until APAC-144.
  2. The allow-list was our rollout control, and a direct link bypasses it. Fine if we're opening to
     all SSO orgs (sounds like we are), but then the picker is the de facto allow-list, so the backend
     should serve the org list (slug, name, prod vs sandbox) rather than the app hardcoding slugs. Small
     backend piece. We'd also pick prod vs sandbox org per brand (IHG and Hyatt have both).
  3. Same account hygiene as web (SSO org and sso_name_id on the profile, role mappings). Nothing
     mobile-specific.

  Happy to hash out the backend side with Connor next week.

  ### Notes
  - Snowflake MCP hung (known issue, see memory); used the direct server-module bypass. sso_organization
    is not mirrored in CANARY_RAW, so org slugs came from Slack history and Groundcover
    CTX_sso_organization_slug, not the DB.
  - No external writes made.
project: 2026-09-08-mobile
source_id: https://canarytechnologies.slack.com/archives/C0AN8AQ49UG/p1792448760833769?thread_ts=1792018248.856969&cid=C0AN8AQ49UG
tags:
- morning-gtd
- slack
time_minutes: 15
title: 'Answer Mike Hu in #epd-staff-ops: does mobile SSO page work out of the box
  for IHG/Hyatt/Marriott?'
updated: 2026-10-20 14:39:11.829030
waiting_on: null
waiting_since: null
working_on: false
---

Follow-up to my 'Wyndham is a config change, native SSO is US-only' reply. Mike asks if linking to the SSO page on mobile needs extra config per brand. Open 0 days, no reply from me.
https://canarytechnologies.slack.com/archives/C0AN8AQ49UG/p1792448760833769?thread_ts=1792018248.856969&cid=C0AN8AQ49UG