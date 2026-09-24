---
area: null
completed_at: 2026-09-24 10:51:09.680501
contexts:
- react
created: 2026-09-24 09:07:24.295008
defer_until: null
due: null
energy: low
id: 2026-09-24T0907-reply-to-jordan-sterling-re-global-single-login-ro
order: null
output: |
  ## Agent run 2026-09-24T10:24

  Thread: https://canarytechnologies.slack.com/archives/D07HCMQU5FY/p1790176104382869
  Nothing sent. Draft below for you to post in the DM.

  ### What Jordan said (unanswered, 2026-09-23)
  1. Slug is fine as a workaround if nobody uses it today, but it is NOT a globally unique linking id: BW's different IdPs share the same slug.
  2. Proposed roadmap for "login once, all Canary regions": v1 SSO only (except BW/Wyndham), v2 email-only users, v3/maybe-never username users.

  ### Codebase facts I checked (backend/canary)
  - `sso/models/organization.py`: `Organization.slug` is `SlugField(unique=True)`, so unique per regional DB only. It is baked into the SP-side URLs the IdP is configured with: `saml-acs`, `saml-metadata`, `sso-login` (`sso/views/sso_overview.py:79-80`). Changing a slug is therefore a customer-side change, which is an argument against overloading it as a linking key.
  - `issuer_id` (IdP entity id) and `certificate` are the fields that actually identify "which IdP". Two regional orgs with the same slug but different `issuer_id` are different IdPs.
  - BW and Wyndham use fixed slugs in every region: `BEST_WESTERN_SSO_ORG_SLUG = "best-western"` (`onboarding/configuration_providers/best_western/best_western_sso_provider.py:9`) and `WYNDHAM_SSO_ORG_SLUG = "wyndham"` (`onboarding/services/vendor/wyndham_definitions.py:28`). Each region has its own IdP app because we asked them to split. So Jordan's point is exactly right for these two: same slug, different IdP, no shared IdP session to ride.
  - `Organization.uuid` exists (unique, nullable) but is generated per row, so it is also not a cross-region link.

  ### Draft reply (Slack DM, two messages)

  **Message 1**
  > Agree on slug. It's unique per region only, and it's baked into the ACS / metadata / login URLs the IdP is configured with, so it's really a customer-facing contract rather than a linking id. Overloading it would mean any rename is a customer change.
  >
  > I think there are two different "same" relationships and the slug only gets one of them:
  > 1. same customer org across regions -> slug (or a Portfolio.identifier-style column) can link that
  > 2. same IdP across regions -> that's issuer_id + cert matching, and it's the one "login once" actually needs
  >
  > For BW and Wyndham, 1 is true and 2 is false, which is why they fall out of v1. For most other customers 2 is true today without them doing anything, which is your "it would just work" point.
  >
  > If we want an explicit link rather than inferring from issuer_id, I'd add a dedicated nullable `global_identifier` on sso Organization, same pattern as Portfolio.identifier, and leave slug alone.

  **Message 2**
  > Roadmap: +1 to the ordering.
  > - v1 SSO-only: agree. Suggest we define "same IdP" as issuer_id match rather than slug match so it's safe by construction.
  > - BW/Wyndham: they're the ones who most want this, and the split IdPs exist because we asked for them. I'd treat "consolidate to one IdP app" as a customer-coordination track that runs alongside v1 rather than an eng blocker. Happy to raise it with the BW and Wyndham contacts once v1 has a shape.
  > - v2 email-only users: fine as the next step, needs a global user identity story, which is a bigger change.
  > - v3 username users: agree maybe-never. Mostly legacy / shared logins.
  >
  > This spans pods, same as the API pattern discussion. Want to write it up as a short doc and take it to eng-general?

  ### Things you may want to adjust before sending
  - Whether you actually want to volunteer the BW/Wyndham customer conversation.
  - Whether `global_identifier` is worth proposing now or is premature; Jordan may prefer issuer_id inference only.
project: null
source_id: https://canarytechnologies.slack.com/archives/D07HCMQU5FY/p1790176104382869
tags:
- morning-gtd
- slack
time_minutes: 10
title: 'Reply to Jordan Sterling re: global single-login roadmap and BW IdP slug linking'
updated: 2026-09-24 10:51:09.680496
waiting_on: null
waiting_since: null
working_on: false
---

Jordan's last two messages are unanswered: org slug is fine if unused but is not a globally unique linking id (different BW IdPs share a slug), and a proposed roadmap: v1 SSO only (except BW/Wyndham), v2 email-only users, v3/maybe-never username users. Key-account (BW, Wyndham) SSO.
https://canarytechnologies.slack.com/archives/D07HCMQU5FY/p1790176104382869