---
area: null
contexts:
- react
created: 2026-05-25 04:15:51.650085
defer_until: null
due: null
energy: low
id: 2026-05-25T0415-send-andrea-links-to-global-dynamo-prs-oauth-groun
order: null
output: |
  ## Agent run 2026-05-25T11:45Z

  Andrea's ask (group DM with Andrea + Jordan, C0B5597H1FC):
  > Do you mind pointing me to your global dynamo PRs so I can get a little oriented before hand?

  "Global dynamo" = Jordan's api_gateway Dynamo-backed groundwork that the OAuth login page (ENT-6204, my PR #45580) sits on top of. Below is a grouped list of Jordan's merged PRs in that series, in the order it makes sense to orient through them.

  ### Draft Slack reply (NOT SENT — awaiting approval)
  ```
  All Jordan's, in roughly the order they stack:

  Application + Identity foundations (api_gateway Dynamo schema)
  • ENT-6191: Remove duplicate Django Application/AuthToken models — https://github.com/canary-technologies-corp/canary/pull/45339
  • ENT-6191 (2/2, open): Delete Application + AuthToken Django models — https://github.com/canary-technologies-corp/canary/pull/45377
  • ENT-6209: Rename ApplicationCredentialService → Application dataclass + split create — https://github.com/canary-technologies-corp/canary/pull/45448
  • ENT-6210: ApplicationService.get(sid) — https://github.com/canary-technologies-corp/canary/pull/45449
  • ENT-6211: ApplicationService.update() for name + status — https://github.com/canary-technologies-corp/canary/pull/45450
  • ENT-6212: oauth_redirect_url field + ApplicationService.update() — https://github.com/canary-technologies-corp/canary/pull/45486
  • ENT-6207: Add StaffUser to IdentityType enum — https://github.com/canary-technologies-corp/canary/pull/45525
  • ENT-6281: wire IdentityType.STAFF_USER into IdentityService.create() validation — https://github.com/canary-technologies-corp/canary/pull/45931

  Application secrets + OAuth grant/token endpoints
  • ENT-6202: application_secrets table + service + CRUD — https://github.com/canary-technologies-corp/canary/pull/45478
  • ENT-6203: oauth_grants table + OAuthGrantService — https://github.com/canary-technologies-corp/canary/pull/45483
  • ENT-6205: POST /oauth/tokens (authorization_code grant) — https://github.com/canary-technologies-corp/canary/pull/45540
  • ENT-6206: POST /oauth/tokens (refresh_token grant) — https://github.com/canary-technologies-corp/canary/pull/45553
  • ENT-6208: Application Update API for oauth_redirect_url — https://github.com/canary-technologies-corp/canary/pull/45552
  • ENT-6265: HMAC the OAuth refresh token at rest — https://github.com/canary-technologies-corp/canary/pull/45794
  • ENT-6266: HMAC the authorization code at rest — https://github.com/canary-technologies-corp/canary/pull/45798

  Routing / wiring
  • ENT-6282: Istio routes for OAuth (/v1/oauth/tokens + /v1/oauth/login) — https://github.com/canary-technologies-corp/canary/pull/45973
  • ENT-6282 follow-up (open): Flip OAuth login GAD path to match Django — https://github.com/canary-technologies-corp/canary/pull/46199

  For context, my ENT-6204 login page sits on top of this: https://github.com/canary-technologies-corp/canary/pull/45580
  ```

  ### Status
  - Draft prepared, NOT posted to Slack. Channel C0B5597H1FC, replying to thread 1779465810.807809.
  - Awaiting Gareth's go/no-go before sending.
project: null
source_id: https://canarytechnologies.slack.com/archives/C0B5597H1FC/p1779465810807809
tags:
- morning-gtd
- slack
time_minutes: 10
title: Send Andrea links to global dynamo PRs (oauth groundwork)
updated: 2026-05-25 11:57:09.625075
waiting_on: null
waiting_since: null
working_on: false
---

Group DM with Andrea/Jordan: orientation before a meeting. https://canarytechnologies.slack.com/archives/C0B5597H1FC/p1779465810807809