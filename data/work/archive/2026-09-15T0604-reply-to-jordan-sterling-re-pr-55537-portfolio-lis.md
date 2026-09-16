---
area: null
completed_at: 2026-09-15 15:28:03.166590
contexts:
- react
created: 2026-09-15 06:04:55.423740
defer_until: null
due: null
energy: medium
id: 2026-09-15T0604-reply-to-jordan-sterling-re-pr-55537-portfolio-lis
order: null
output: |
  ## Agent run 2026-09-15T11:53:30.215716

  **Verdict: GO — my comment does not block. Reply to Jordan and resolve the thread.**

  Context checked:
  - PR #55537 (https://github.com/canary-technologies-corp/canary/pull/55537): OPEN, MERGEABLE, already APPROVED by lmenaolivares 9/10. Latest commit 308f75ed50b (case-insensitive identifier filter).
  - My comment thread (https://github.com/canary-technologies-corp/canary/pull/55537#discussion_r3988908740) — Jordan's 9/11 reply: application-create has no permission checks yet, nothing is wired to a page, and this list does not feed any other API's auth. Lauta asked what the driver is; Jordan: validating portfolio_identifier before writing the application row.
  - Jordan's DM 9/14 (https://canarytechnologies.slack.com/archives/D07HCMQU5FY/p1789401141742879): "did you have any concerns on this pr ... just wanted to double check with you before merging". No thread replies yet.

  Why it is not blocking:
  1. Exposure is only reachable by bearer identities via MultiPrincipalGatekeeper — session cookie / anonymous are 401. Today only identity-service mints a user bearer, so no browser-reachable surface for a front-desk user.
  2. Payload is low sensitivity: uuid, identifier, name, parent_uuid, reporting_currency, timestamps. Leaking that an internal_* / regional portfolio exists is informational, not privileged.
  3. PUBLIC_PORTFOLIO_IDENTIFIERS is used on master for hotel-dashboard visibility and Growthbook targeting (hotels/models/portfolio.py:104, portfolios/services/portfolio.py:329,351, hotel_staff/services/user_assignment_operation.py:42). Applying it here would hide exactly the internal_* / above-property rows the application-create flow needs to validate, so it defeats the endpoint's purpose — as I already said in the comment.
  4. The real risk (a low-privilege user creating an application) belongs to the application-create endpoint, which Jordan confirmed still needs a permission check. That is a follow-up, not a condition on this PR.

  Draft Slack reply to Jordan (NOT sent — paste into the DM thread):

  > No blocker from me — go ahead and merge. Reasoning: the only surface is bearer identities (session cookie is 401), the payload is just uuid/identifier/name/parent/currency, and applying PUBLIC_PORTFOLIO_IDENTIFIERS would hide the internal_* rows the app-create flow needs to validate. Two asks so the concern doesn't get lost: (1) a ticket for the permission check on application create (any staff user in a Wyndham hotel must not be able to create an app against `wyndham`), and (2) when this list lands on an actual page, revisit the user scope — probably "portfolios where the user holds a management role" rather than plain membership. I'll resolve my comment.

  Manual follow-ups for Gareth:
  - Send the Slack reply above.
  - Resolve the GitHub thread on portfolio_access.py (optionally paste the same reasoning there).
  - Optionally ask Jordan to create the follow-up Linear ticket for app-create authz (ID team), or create it yourself.

  ## Agent run 2026-09-15T11:55:05.988853 (addendum: portfolio types)

  Question: suggest using portfolio types to filter?
  Answer: yes as a `?type=` query filter, no as a visibility gate.
  - PortfolioType (hotels/models/portfolio_type_assignment.py) is a 7-value enum on a join table: parent_brand, brand, msa, management_company, above_property_dashboard, sso_organization, ad_hoc.
  - The internal_* owner portfolios and regional above-property portfolios are typed ad_hoc / above_property_dashboard (backfill in portfolios/management/commands/onetime_backfill_portfolio_type_assignments.py falls back to ad_hoc). Hiding those types would hide exactly the rows app-create must validate, so types cannot replace the scope check.
  - A repeatable `?type=` filter alongside `?identifier=` is cheap (selector-only) and serves the next consumer (SSO org / dashboard picker). Lauta raised types on the response shape 9/10; Andre closed it as "leave off until external use case". A filter param is a smaller ask and does not need to block the PR.

  Optional line for the Slack reply:
  > One idea for a follow-up, not a blocker: a repeatable ?type= filter (PortfolioType values) alongside ?identifier=. It doesn't solve the visibility question — internal_* and above-property rows are ad_hoc / above_property_dashboard and are exactly what app-create needs to see — but the next caller after app-create will almost certainly want "portfolios of type X I belong to" (SSO org picker, dashboard picker), and it's cheap to add in the selector now.
project: null
source_id: https://canarytechnologies.slack.com/archives/D07HCMQU5FY/p1789401141742879
tags:
- morning-gtd
- slack
time_minutes: 15
title: 'Reply to Jordan Sterling re: PR #55537 portfolio listing scope'
updated: 2026-09-15 15:28:03.166584
waiting_on: null
waiting_since: null
working_on: false
---

Jordan wants to merge ID-79 (GET /api/private/v1/portfolios) and asked whether my open comment blocks. My 9/11 comment on portfolio_access.py: listing is too permissive (a single-hotel Wyndham front-desk user can list regional/internal portfolios); suggested PUBLIC_PORTFOLIO_IDENTIFIERS. Jordan replied 9/11; give a go/no-go.
https://canarytechnologies.slack.com/archives/D07HCMQU5FY/p1789401141742879
https://github.com/canary-technologies-corp/canary/pull/55537