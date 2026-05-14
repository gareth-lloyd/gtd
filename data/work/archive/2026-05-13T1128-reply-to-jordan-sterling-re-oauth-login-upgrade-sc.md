---
area: null
contexts:
- react
created: 2026-05-13 11:28:24.559300
defer_until: null
due: 2026-05-13
energy: medium
id: 2026-05-13T1128-reply-to-jordan-sterling-re-oauth-login-upgrade-sc
order: null
output: '## Agent run 2026-05-13T16:00:00Z


  ### Context gathered


  Full conversation in #eng-directors + Jordan''s DM. Read the Notion design doc (Canary
  Public API, V2 OAuth section).


  **Ownership:** Agreed this rolls to Gareth first, delegate where appropriate. Enterprise
  owns auth/login/2FA/SSO.


  **Technical scope (from Notion doc):**

  - OAuth 2.0 Authorization Code flow for hotel staff login

  - Reuses api_gateway app + existing DynamoDB tables (applications, auth-tokens,
  identities) + existing login page

  - New: client_secret + oauth_redirect_url fields on ApplicationRecord

  - New: oauth_grants DynamoDB table (short-lived, 5-min TTL)

  - New endpoints: POST /v1/oauth/login_attempts, POST /v1/oauth/tokens

  - Login page upgrade: detect ?oauth_code= param, support normal + OAuth login paths,
  MFA stays on Canary

  - Refresh token support

  - Mobile app is the immediate consumer (unblocks hacky auth workaround)


  **Bigger picture Jordan flagged:** Once staff users authenticate via OAuth, portfolio-scoped
  applications and moving portfolios to global DB become important — and that''s "not
  a simple project."


  ### Draft reply to Jordan (DM)


  > Yeah, I reviewed the doc — agree this is tractable. The core OAuth flow (login_attempts
  + token exchange endpoints, oauth_grants table, login page upgrade) is well-scoped
  and reuses most of what''s already there.

  >

  > I''ll own it on the Enterprise side. Need to figure out who picks it up — probably
  makes sense to look at that once we''re firmer on block 2 assignments.

  >

  > The bigger piece you flagged — portfolios as application owners, scoping requests,
  global DB — agree that''s separate and substantially larger. Worth keeping that
  off the critical path for the mobile app unblock.


  **Action:** Review draft, adjust tone/content, send via Slack DM to Jordan (D07HCMQU5FY).

  '
project: 2026-04-16T1210-unblock-team
source_id: https://canarytechnologies.slack.com/archives/D07HCMQU5FY/p1778534425346539
tags:
- morning-gtd
- slack
time_minutes: 15
title: 'Reply to Jordan Sterling re: OAuth login upgrade scope'
updated: 2026-05-13 17:13:43.898690
waiting_on: null
waiting_since: null
working_on: false
---

Jordan thinks not a huge project — upgrade login page to handle normal + OAuth so mobile app can use it. Doc in #eng-directors. https://canarytechnologies.slack.com/archives/D07HCMQU5FY/p1778534425346539