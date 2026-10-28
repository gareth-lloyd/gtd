---
area: null
completed_at: 2026-10-28 14:40:05.597240
contexts:
- react
created: 2026-10-28 11:10:00.340315
defer_until: null
due: null
energy: medium
id: 2026-10-28T1110-answer-mike-hu-in-staff-ops-pilots-does-a-non-us-h
order: null
output: |-
  ## Agent run 2026-10-28

  Thread: https://canarytechnologies.slack.com/archives/C0BV0B9G8DS/p1793156397502809?thread_ts=1793111165.804069&cid=C0BV0B9G8DS
  (Marta asked Mike about Staff App messaging for the Aspire properties. Mike asked whether they are IHG/Wyndham SSO and whether Aspire is German, then asked Gareth the question.)

  ### Answer: yes, it matters
  - Each region has its own SSO orgs. Wyndham exists as separate rows: US `wyndham` is id 49, EU `wyndham` is id 36. A non-US hotel's users and hotel live only in the EU (or AP) database.
  - All Staff App OAuth endpoints in the global API are pinned to `region: us-west-2`. That covers /v1/oauth/lookup, the authorization challenge and tokens (backend/public-api/parser/global-api.yaml, around lines 4491-4719). The SSO `url` that the lookup returns is `settings.SITE_URL + /sso/login/<slug>`, which is the US host (backend/canary/api_gateway/views/oauth_lookup.py).
  - So a hard-coded link to the US IHG/Wyndham SSO login sends an EU hotel's staff through the US org. The SAML login can succeed, but the user ends up in a region where their hotel does not exist.
  - To work, the link has to point at the hotel's home-region host. That region's `SSO_LOGIN_ALLOW_LIST` must include the slug. The OAuth code and token exchange then have to happen in that same region, but today the global API sends them to US only.

  ### Not verified
  - What exactly the US SAML handler does for an EU-only hotel: no access, or a stray user provisioned in US. I did not trace this.
  - Whether an IHG SSO org exists in EU. The auto-mode classifier blocked that prod lookup. In US, `ihg` is id 347.
  - Which region the Aspire hotels are in. If they are UK/German they are probably EU, but that is unconfirmed.
  - Whether the Staff App has any way to choose a region.

  ### Draft Slack reply (NOT sent; needs your OK)
  To thread https://canarytechnologies.slack.com/archives/C0BV0B9G8DS/p1793156397502809?thread_ts=1793111165.804069&cid=C0BV0B9G8DS :

  > @Mike Hu yes, region matters. The SSO orgs are per region: EU has its own `wyndham` org, separate from the US one, and a non-US hotel's users and hotel only exist in the EU stack. The staff app OAuth endpoints on the global API (lookup / challenge / tokens) are all pinned to us-west-2, and the SSO link the lookup hands back is the US host. So a direct link to the US IHG/Wyndham SSO login would authenticate an EU hotel's staff against US, where their hotel doesn't exist.
  > For an EU property, the link has to point at the EU host, with the slug on the EU `SSO_LOGIN_ALLOW_LIST` and the OAuth exchange happening in EU too, which the global API doesn't route today. Worth confirming which region the Aspire hotels are in first. If they're US-hosted, the direct link is fine.

  ## Correction 2026-10-28 (after Gareth asked me to check the "all pinned to us-west-2" claim)
  That claim was overstated. Routing blocks in backend/public-api/parser/global-api.yaml:
  - /v1/oauth/lookup (line 4718) and /v1/oauth/authorize-challenge (line 4490): `region: us-west-2` on the monolith. Both call LoginLookupService.route, which reads the monolith's User table. So these really are US-only: an EU-only user gets the "password" answer, which is the same answer as an unknown account.
  - /v1/oauth/tokens (line 4570) and /v1/oauth/revoke (line 4638): `backend: identity-service`, `region: us-west-2`. identity-service "owns global identities" (backend/identity-service/README.md) in DynamoDB, and its /oauth/grants endpoint lets "the monolith's login page" issue a pending grant. So `us-west-2` here is where a global service is hosted. It is not a regional limit, and the token exchange is probably not a blocker for EU users.
  - /v1/login/oauth (line 4353): not pinned at all. It redirects to `https://{LOGIN_HOST}/login/oauth/`.

  Revised answer: region still matters, but more narrowly. The US-only parts are the identifier lookup / authorize-challenge, and the SSO URL they return, which is the US SITE_URL. A direct link that skips the lookup and opens the EU host's `/sso/login/<slug>/?next=/login/oauth/?application_sid=...` could work end to end, because the EU login page issues the grant through the global identity-service. Not verified:
  - whether EU's monolith points at the same global identity-service
  - whether the EU `SSO_LOGIN_ALLOW_LIST` includes the slugs
  - what the Staff App does after login with a hotel in another region

  ### Revised draft Slack reply (NOT sent)
  > @Mike Hu it does matter, but only for part of the flow. Staff users and the IHG/Wyndham SSO orgs are per region (EU has its own `wyndham` org). The identifier lookup / authorize-challenge on the global API run against the US monolith only, so for an EU-hosted hotel they won't find the user, and the SSO link they return is the US host. If you direct-link instead, the link needs to be the hotel's home-region host (e.g. the EU app's `/sso/login/wyndham/`) with the staff app's OAuth request as `next`. The token exchange goes through identity-service, which is global, so that leg should be fine, but nobody has tested an EU login end to end yet. First step: confirm which region the Aspire hotels are on. If they're US, the US link is fine.
project: null
source_id: https://canarytechnologies.slack.com/archives/C0BV0B9G8DS/p1793156397502809?thread_ts=1793111165.804069&cid=C0BV0B9G8DS
tags:
- morning-gtd
- slack
time_minutes: 15
title: 'Answer Mike Hu in #staff-ops-pilots: does a non-US hotel matter when the Staff
  App direct-links to IHG/Wyndham SSO?'
updated: 2026-10-28 14:40:05.597235
waiting_on: null
waiting_since: null
working_on: false
---

Aspire properties want Staff App messaging plus Ticketing. Mike asks: "if we direct link to the IHG and Wyndham SSO logins on staff app, does it matter if they're non-US?" Open 0 days, no reply from you.
https://canarytechnologies.slack.com/archives/C0BV0B9G8DS/p1793156397502809?thread_ts=1793111165.804069&cid=C0BV0B9G8DS