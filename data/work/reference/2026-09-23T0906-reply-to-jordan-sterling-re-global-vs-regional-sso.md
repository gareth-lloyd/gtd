---
area: null
completed_at: 2026-09-23 16:14:14.144681
contexts:
- react
created: 2026-09-23 09:06:58.477237
defer_until: null
due: 2026-09-23
energy: low
id: 2026-09-23T0906-reply-to-jordan-sterling-re-global-vs-regional-sso
order: null
output: |
  ## Agent run 2026-09-23 13:23:35

  ### PR 55537 (Sep 14 ask) — already closed, nothing to do
  Jordan asked on Sep 14 (https://canarytechnologies.slack.com/archives/D07HCMQU5FY/p1789401141742879) whether you had concerns on PR 55537. You replied Sep 15 12:59 "I'm OK with it. I've resolved my comment thread." PR merged Sep 15 17:10 UTC and deployed to prod: https://github.com/canary-technologies-corp/canary/pull/55537 (ID-79, GET /api/private/v1/portfolios). No reply owed.

  ### Sep 22 idea: global vs regional SSO configs — reply owed
  Thread: https://canarytechnologies.slack.com/archives/D07HCMQU5FY/p1790097422396279
  Jordan (Sep 22 20:15-20:17): "we should have global SSO config" / "this is complex because sso is regional right now and extracting it would be hard" / "one workaround is linking regional sso configs with a common identifier, same idea as portfolio_identifier but for sso. maybe there's already a column on the sso config table that does this" / "people don't want regional sso configs, they want global sso configs".
  Likely trigger: Rodrigo's PR 55813 (https://github.com/canary-technologies-corp/canary/pull/55813), staff-app SSO lookup on the global API gated by SSO_LOGIN_ALLOW_LIST, a settings list of sso.Organization slugs (chosen to avoid a migration). Also #epd-staff-app Sep 23: Belinda asked whether SSO goes beyond BW; Mike Hu said "starting with BW, intend to expand".
  Prior context: Notion design doc "Global Identities & SSO — Immutable Identity, Cross-Region Linking" (https://app.notion.com/p/3ca81468615181fcbc5af1d1a671fc2a) already states "SSO is regional end to end" and sketches a global_identity_sid; Aug 31 Global SSO meeting notes (https://docs.google.com/document/d/1HcCYu7rdm2JEc1D1yJNzmjh9eij4xryPettHBNxycRY).

  What the code says (backend/canary/sso/models/organization.py):
  - `slug`: SlugField, unique per region. Already the de-facto cross-region identifier: PR 55813's allow-list keys on it from the global API, and the ACS URL is reverse("saml-acs", slug). Nothing enforces the same slug in every region.
  - `uuid`: per-row default uuid4, so it differs per region. Not a global key.
  - `join_users_to_portfolio`: nullable FK to hotels.Portfolio, whose `identifier` IS the global in-code enum (Portfolio.Identifier). So there is an indirect global link org -> portfolio -> identifier, but it's nullable and means "auto-join users to this portfolio", not "this org's global identity".
  - No dedicated global-identifier column exists.
  - The genuinely regional part isn't just the config row: SP entity id / ACS URL are built from settings.SITE_URL + slug per region, and there are per-org SP cert overrides. Every IdP is configured against a regional ACS, so a "global config" still needs per-region SP metadata or a global ACS that routes.

  Could NOT verify: whether BW/Wyndham/IHG orgs actually share a slug across us/eu/ap. sso_organization is not in the CANARY_RAW Snowflake mirror and the Teleport MCP sessions were expired this run. If you want to state it as fact, run in each region: Organization.objects.values_list('slug', 'join_users_to_portfolio__identifier').

  ### Draft reply (NOT sent; paste into the DM if you're happy)

  Agree on the destination: customers think of "our IdP" as one thing, so one config that spans regions is the right end state. On the workaround: there's no dedicated column today, but two things get most of the way there.

  1. `Organization.slug` is already the cross-region key by convention. 55813's allow-list is keyed on it from the global API, and the ACS URL is derived from it. It's just not enforced, so the cheap first step is making "same slug in every region" a rule (a check on create in admin plus a one-off audit) rather than a new column.
  2. `join_users_to_portfolio` -> `Portfolio.identifier` gives an indirect global link for orgs that set it. Nullable and means something else, so I wouldn't lean on it.

  If we want the portfolio_identifier pattern properly, I'd copy the ID-79 shape: nullable `identifier` on `sso.Organization` backed by an in-code enum, then `GET /api/private/v1/sso-organizations?identifier=` for identity-service / the global API. Same contract survives the eventual move to a global table, same as portfolios.

  The part that stays hard regardless: the SP side is per region (SITE_URL + slug ACS, per-org SP cert overrides) and every IdP is configured against a regional ACS. A global config record is easy; a global ACS that routes to the right region is the real extraction work, and it's the same problem the Global Identities doc calls out. Happy to sketch it if staff-app SSO beyond BW makes it urgent.

  Quick check before we decide anything: do BW/Wyndham/IHG actually share a slug across us/eu/ap today? I couldn't verify from here.

  ## Agent run 2026-09-23 16:09:37

  Follow-up asked: "Describe the routing problem that remains after we have a global SSO config record"

  ### Short version
  A global SSO config record fixes *where the IdP settings live*. It does not fix *where the browser lands after the IdP redirects*, *which region's user row and session get logged in*, or *how anyone finds that region from an email address*. Those three are the routing problem, and each one is a separate piece of work. None of them is a schema change.

  ### What the global record would actually cover
  The IdP half of `sso.Organization`: issuer_id, sso_url, slo_url, certificates, force_authn, name-id/attribute config, role mappings, allowed email domains, the staff-app allow-list (today `SSO_LOGIN_ALLOW_LIST` in settings), and the per-org SP cert overrides. That is the part customers mean by "our SSO config" and it is the same in every region. The other half of the model is inherently regional: `SSOOrganizationHotel` rows point at regional hotels, `join_users_to_portfolio` points at a regional Portfolio row, diagnostic logs are per region. So "global config" is really a split (global IdP record + regional mapping rows), not a lift of the whole table.

  ### The four things that stay regional after the split

  **1. The SAML endpoint (ACS) is a regional URL.** `Organization.settings` builds the SP side as `entityId = settings.SSO_ENTITY_ID` and `assertionConsumerService.url = settings.SITE_URL + /sso/saml/acs/<slug>` (backend/canary/sso/models/organization.py:301-303). SITE_URL is per deployment (www / eu / ap). So every customer IdP is registered against one region's ACS. A global record can hold one canonical SP identity, but then something has to answer at that URL. Options:
  - Keep N regional ACS URLs and have the customer register all of them in their IdP (Okta, Entra and ADFS all allow multiple reply URLs; IdP-initiated logins go to the default one). Zero code, but the customer does the work per region, which is exactly the complaint.
  - One global ACS host (app. or api.) that validates the assertion and forwards. This moves the whole SP to the global host, see 4.

  **2. Login and session are regional.** After validation `saml_acs` does `SSOOrganizationService.get_user(sso_org, name_id, attributes)` against the regional DB, then `django.contrib.auth.login` on the regional session, marks MFA passed on that session, and redirects to `RelayState` (regional SITE_URL + next) (backend/canary/sso/views/views.py:486-521). A global ACS therefore ends up holding a validated identity on a host that has no user rows and cannot set the regional session cookie. To finish, it would need a one-time signed handoff to the regional host that logs the user in. We have two half-precedents (the `merge_user_jwt` in manual_user_merge.py:518 and the api-gateway `identity_token`), but neither is "log this browser in on region X". That is a new auth primitive with expiry, single-use and audience binding, and it is the security-review-heavy part.

  **3. There is no person-to-region lookup.** routing-service routes by hotel slug (DynamoDB `hotel-slug-routing`) or by a pinned region per route (backend/routing-service/routing-config.production.yaml); there is no user, org or email key. The staff-app lookup Rodrigo shipped (`POST /v1/oauth/lookup`, PR 55813 https://github.com/canary-technologies-corp/canary/pull/55813) is pinned to us-west-2, reads the US DB only, and returns `https://www.canarytechnologies.com/sso/login/<slug>`; the PR says "Multi-region lookup is out of scope: US only, one region, no fan-out." So today an EU BW user typing their email into the staff app gets a US URL. To route, we need one of: a global user/identity index (identity-service's identities plus the `global_identity_sid` from the Global Identities doc https://app.notion.com/p/3ca81468615181fcbc5af1d1a671fc2a), or fan-out to every region on lookup (Rodrigo's superseded PoC PR 54998 https://github.com/canary-technologies-corp/canary/pull/54998 did that with a chooser page). Either way there is an ambiguity case to decide: one email with accounts in two regions.

  **4. SP-initiated request state lives in the regional session.** `sso_login` stores `AuthNRequestID` in the Django session and `saml_acs` reads it back to verify `InResponseTo` (views.py:187-190). If login starts on a regional host and the ACS answers on a global host, the session cookie is not there, so the check silently degrades to "unsolicited". Practically: whoever owns the ACS must also own `/sso/login/<slug>` and the session that ties them. Half-moving the SP is not an option.

  ### What this means for the "common identifier" workaround
  A shared identifier across regional configs (slug enforced, or an `identifier` enum like Portfolio) solves the admin-side problem: one name that means the same customer in every region, so tooling and the global API can address it. It leaves 1-4 untouched: the customer still registers three ACS URLs, and the login flow still needs a person-to-region resolver before it can pick a `/sso/login/<slug>` host. Which is fine, as long as we say so: the identifier is the cheap step, the resolver (3) is the next real one, and the global ACS with handoff (1, 2, 4 together) is the expensive one that only becomes necessary if we want customers to register a single URL.

  ### Recommended order, for the reply
  1. Common identifier on regional configs (cheap, no migration if slug is enforced by convention plus an audit).
  2. Person-to-region resolver on the global API: identity-service index preferred, fan-out as the stopgap. Fixes the staff-app lookup returning US for everyone.
  3. Global ACS + regional session handoff only if "one URL to register" becomes a customer requirement. It is a new auth primitive, not a config change.

  ### Draft reply (NOT sent; paste into the DM if you're happy)

  On the routing side, I want to separate what a global config record would fix from what it wouldn't, because I think the second list is where the actual work is.

  A global record fixes where the IdP settings live: issuer, SSO URL, certs, role mappings, allowed domains, the staff-app allow-list. That's what customers mean by "our SSO config" and it's legitimately the same in every region. The hotel mappings and join-to-portfolio stay regional by nature, so it's a split rather than a lift.

  What it doesn't fix:
  1. The ACS URL is per region (SITE_URL + /sso/saml/acs/slug). Every customer IdP is registered against one region's ACS. Either the customer registers all three, or we stand up a global ACS.
  2. Login and session are regional. The ACS logs the user in on the regional Django session and redirects to a regional RelayState. A global ACS would validate the assertion and then have nowhere to put it. Finishing needs a signed one-time handoff to the regional host, which is a new auth primitive we don't have.
  3. Nothing maps a person to a region. routing-service keys on hotel slug or a pinned region. The staff-app lookup in 55813 is pinned to US and returns a www URL for everyone, by design for launch. We'd need a global identity index (identity-service plus the global_identity_sid idea) or fan-out on lookup.
  4. The SP-initiated request id lives in the regional session, so whoever owns the ACS also has to own /sso/login. Can't half-move it.

  So the common-identifier idea is the right cheap step and I'd do it. The next real step is the person-to-region resolver, because that's what makes the staff-app lookup correct outside the US. The global ACS + handoff is the expensive one and I'd only do it if "register one URL" becomes a customer requirement.

  ### Not verified this run
  - Whether BW/Wyndham/IHG orgs share a slug across regions (Teleport sessions still expired; sso_organization not in Snowflake). Same query as last run.
  - Whether each customer IdP currently has all three regional ACS URLs registered, or only one. ENT would know.
  - How python3-saml treats a missing request_id in our config (`rejectUnsolicitedResponsesWithInResponseTo` is not set in Organization.settings, so the check is skipped, but I did not run it).
project: 2026-04-16T1210-unblock-team
source_id: https://canarytechnologies.slack.com/archives/D07HCMQU5FY/p1790097422396279
tags:
- morning-gtd
- slack
time_minutes: 10
title: 'Reply to Jordan Sterling re: global vs regional SSO configs idea'
updated: 2026-09-23 16:14:14.144673
waiting_on: null
waiting_since: null
working_on: false
---

Jordan: 'people dont want regional sso configs. they want global sso configs' then 'i have this idea:' (saved). Also check his Sep 14 ask whether I had concerns on PR 55537 before merge.
https://canarytechnologies.slack.com/archives/D07HCMQU5FY/p1790097422396279
https://canarytechnologies.slack.com/archives/D07HCMQU5FY/p1789401141742879