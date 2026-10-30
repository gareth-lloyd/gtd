---
area: null
completed_at: 2026-10-29 14:26:59.998228
contexts:
- react
created: 2026-10-29 09:54:56.614065
defer_until: null
due: null
energy: medium
id: 2026-10-29T0954-answer-marta-in-staff-ops-pilots-estimate-for-wynd
order: null
output: |-
  ## Agent run 2026-10-29T14:20

  **Status: Renan has not replied.** Thread (https://canarytechnologies.slack.com/archives/C0BV0B9G8DS/p1793206186947919?thread_ts=1793111165.804069&cid=C0BV0B9G8DS) ends at Mike's 19:13 reply on 10-28; your question to Renan (https://canarytechnologies.slack.com/archives/C0BV0B9G8DS/p1793191188912169?thread_ts=1793111165.804069&cid=C0BV0B9G8DS) is unanswered. No other Renan messages on this since 10-20.

  **Is a solution lined up? No.** Renan's Global User Profile / Global SSO design doc (https://app.notion.com/p/3f381468615180939704fd689cd53eb0, status REVIEW ME!, Identity team) is the nearest thing, but it does not unlock this:
  - It states "Staff App SSO is US-only by decision" and lists the Staff App flow's boundaries as "US only, one allow-listed organization, no region picker, no cross-region session".
  - Its scope is one immutable global sid per person (renames, cross-region duplicates). The doc says property switching across regions is "Global Web's to build". It does not add EU routing to lookup/challenge/tokens.
  - Its rollout (2 migration PRs, 2 identity-service deploys, 3 monolith PRs, per-org rollout with BW last) would be a multi-week dependency anyway. Waiting for it would mean months, not weeks.

  **What the minimal non-US change looks like (from code):**
  1. `backend/canary/hotels/services/login_lookup.py` decides SSO from the regional DB plus `settings.SSO_LOGIN_ALLOW_LIST`. On the us-west-2 global host it cannot see EU users or the EU `wyndham` org. The lookup needs to resolve the region (fan out to EU, or have the app pass or choose a region) and return the EU SSO host.
  2. Add the EU wyndham org slug to the EU allow-list.
  3. The challenge and token exchange must hit the EU monolith (today they are pinned to us-west-2 on the global API). The bearer then resolves against EU Postgres.
  4. The Staff App probably needs a change to honour a region or host from the lookup. That means a mobile release plus store review, unless the app already follows the returned host.
  5. Test with a real EU Wyndham login (Mike asked for test logins).

  My rough sizing (my estimate, not confirmed with Renan or Mike): about 1–2 weeks of backend work, plus the mobile release cycle and testing with a Wyndham EU login. Realistically **3–5 weeks from when someone starts**, and it is not on anyone's queue today. I did not verify whether the app already follows a returned host. That one fact moves the estimate most.

  **Draft reply for Marta (NOT posted; needs your OK and your call on owner and timeline):**

  > <@U0A7PLXAU8N|Marta> No reply from Renan yet, but I checked: nothing is queued that covers this. The Global SSO project Identity is designing fixes cross-region identity, but it explicitly keeps Staff App SSO US-only, so it won't unblock Aspire on its own.
  > The targeted fix is smaller: make the Staff App login lookup and token exchange EU-aware and allow-list the EU Wyndham org. Rough size is 1–2 weeks of backend work plus a Staff App release and testing with a real EU Wyndham login. So realistically 3–5 weeks from when someone picks it up, and it isn't staffed yet. <@U0BJWDFE272|Mike> / <@U09KJASPRPZ|Renan>, can we agree an owner? I'd tell Wyndham "not before mid-December" for now, and we'll firm it up once it's scheduled.

  Decisions for you before sending: (a) whether to commit a date ("mid-December") at all, (b) who owns it (Identity/Renan vs Mike's Staff team vs you), (c) whether to DM Renan first instead of answering for him.

  ## Agent run 2026-10-29T15:05 (assumptions tested; SUPERSEDES the estimate and draft above)

  The first run's estimate was wrong. The app does not use the us-west-2-pinned global routes for login, so no routing or app change is needed for EU login. Two other gaps decide the timeline instead.

  **Assumptions tested**
  1. "Lookup, challenge and tokens are pinned to us-west-2, so EU needs routing work": FALSE for the app. The routes are pinned in `backend/public-api/parser/global-api.yaml`. The Staff App (staff-app-react-native, `src/api/authService.ts`) sends lookup, token exchange and refresh to the picked region's own host (`eu.canarytechnologies.com/api-gateway/v1/oauth/...`), and the EU monolith answers. My Slack reply in the thread said otherwise and needs a correction.
  2. "Lookup hands back the US SSO host": FALSE on the EU host. `api_gateway/views/oauth_lookup.py` builds the URL from `settings.SITE_URL`, so the EU monolith returns the EU SSO URL.
  3. "App needs a region picker and a release": FALSE. The login screen already has a US/EU/APAC picker (`src/config/region.ts`). The brand-tile SSO screen (Wyndham slug `wyndham`, built on the picked region's host) merged 2026-10-21 in STAFF-304 (staff-app-react-native #138). NOT verified: whether a store build with that screen has shipped.
  4. "Grant replication race between regions": not an issue. The EU host mints and redeems the code, against the global `oauth-grants` table.
  5. NEW, config blocker: EU production (canary-kubernetes `apps/canary/canary/values/production/eu-central-1.yaml`) sets neither `STAFF_APP_APPLICATION_SIDS` nor `SSO_LOGIN_ALLOW_LIST`. US sets `STAFF_APP_APPLICATION_SIDS: ["app_d4pygdgmfyfhqqjqwyfwv8kkf6yy6f"]`. Without it the EU monolith:
     - refuses every Staff App OAuth bearer (`StaffOAuthTokenService.resolve` returns None, so every call is anonymous);
     - shows the consent page instead of skipping it (`hotels/views/views.py:410`).
     Without the allow-list, typing an email goes to the password step, though the Wyndham brand tile still works.
     Side note: the US allow-list is `["bestwestern","best-western","canary-sso-test"]`, with no wyndham or ihg. Email lookup does not route Wyndham to SSO in the US either; only the brand tile does.
  6. NEW, big blocker for Ticketing: task-management is deployed only in us-west-2. canary-kubernetes `apps/task-management/` has only us-west-2 environments and values, and EU canary config has no `TASK_MANAGEMENT_BASE_URL`. The app calls `/api/task-management/v1/{hotel_slug}/...` on the regional host, so EU ticket calls have no backend. Mike's "Ticketing they can use now" holds for the US only.

  **Not verified**
  - EU `wyndham` org slug and SAML readiness. The auto-mode classifier denied the EU prod Sallyport read. Run `search_sso_organizations("wyndham")` on canary-mcp-eu yourself.
  - That `eu.` routes `/api-gateway/` to the monolith. I made no prod HTTP calls.
  - That staff messaging endpoints have no other EU-specific gaps. This path has never run in EU.

  **Estimate**
  - Messaging only: a config change. One canary-kubernetes PR adds `STAFF_APP_APPLICATION_SIDS` and `SSO_LOGIN_ALLOW_LIST` (with the EU wyndham slug) to eu-central-1. Then confirm the EU org and the store build, and run an end-to-end test with a real EU Wyndham login. About 1 to 3 working days, gated on getting a test login. The residual risk is bugs on a first-ever EU run.
  - Ticketing in EU: an infra project. task-management needs an eu-central-1 deployment (DB, SQS, secrets, helm values, edge routing for `/api/task-management` on `eu.`, monolith `TASK_MANAGEMENT_BASE_URL`, identity callers). Rough guess 2 to 4 weeks once Infra or the Ticketing team owns it. Lowest confidence of all the numbers here.

  **Revised draft for Marta (NOT posted)**

  > <@U0A7PLXAU8N|Marta> Correction to my earlier message: I dug in, and the Staff App already logs in against the EU stack directly. EU SSO login doesn't need new code, only a config change in our EU deployment plus a test with a real EU Wyndham login. If we can get a test login, messaging for the 2 Aspire properties could be ready within about a week.
  > The bigger gap is Ticketing: the ticketing service only runs in our US region today, so it isn't available to EU hotels yet. That's an infra project, probably a few weeks once someone owns it. <@U0BJWDFE272|Mike>, can you check whether ticketing in EU is planned? Would a messaging-only pilot work for Aspire to start?

  Decisions for you: (a) whether to do the EU config PR yourself; (b) whether to commit "about a week" for messaging before the EU org is checked; (c) who to ask about EU task-management (Mike or Infra).
project: null
source_id: https://canarytechnologies.slack.com/archives/C0BV0B9G8DS/p1793206186947919?thread_ts=1793111165.804069&cid=C0BV0B9G8DS
tags:
- morning-gtd
- slack
time_minutes: 15
title: 'Answer Marta in #staff-ops-pilots: estimate for Wyndham non-US Staff pilot
  code changes'
updated: 2026-10-29 14:26:59.998219
waiting_on: null
waiting_since: null
working_on: false
---

Marta needs an ETA on the SSO-related code changes so she can tell Wyndham when Staff can pilot outside the US (Aspire, 2 properties ready, ~60 EU sites). Waiting on Renan's reply first.
https://canarytechnologies.slack.com/archives/C0BV0B9G8DS/p1793206186947919?thread_ts=1793111165.804069&cid=C0BV0B9G8DS