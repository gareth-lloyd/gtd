---
area: null
contexts: []
created: 2026-05-20 14:10:04.000318
defer_until: null
due: 2026-05-20
energy: low
id: 2026-05-20T1410-respond-asher
order: null
output: '## Agent run 2026-05-20T14:30:00


  **Thread**: Asher asked questions on TOOL-102 ("Surface SSO role permission management
  in Above Property Dashboard"). Stephanie looped me in because Lautaro (ticket author)
  is OOO.


  **Asher''s claim**: the ticket says SSO roles are filtered out of the Above Property
  Dashboard, but in reality they''re already returned and already editable/deletable.
  He asked: what''s the actual goal, should we visually distinguish SSO roles, should
  we lock down editing/deletion, and are his assumptions right.


  **Verified in code**:

  - `list_create_portfolio_roles.py:59` → `PortfolioRoleService.get_portfolio_roles_for_portfolio`
  — no SSO filter

  - `list_create_portfolio_property_role.py:70` → `RoleService.get_property_roles_for_portfolio`
  — no SSO filter

  - The selector named in the ticket (`get_portfolio_managed_roles_without_sso_organization_by_portfolio_ids`)
  is only called from `list_create_roles.py` (property-level dashboard, not above-property)
  and `hotel_staff/services/assignable_roles.py`. The ticket conflated those code
  paths.

  - Tests `test_update_portfolio_role__sso_organization_with_portfolio_allowed` and
  `test_delete_portfolio_role__sso_organization_with_portfolio_allowed` confirm Asher''s
  read — SSO portfolio roles can be updated and deleted today.


  **My read on intended scope** (per ticket: "Allow editing permissions on SSO roles.
  Out of scope: creating or deleting SSO roles, role mappings, assignments"):

  1. Goal isn''t to "unhide" SSO roles — they''re already visible. It''s to (a) tag
  them visually and (b) tighten the backend so name editing and deletion are blocked
  for SSO roles, only permissions are editable.

  2. Visual distinction: yes, inline badge/subtext is enough, matches the pattern
  Asher used for permissions selection.

  3. Name editing + delete: should be blocked for SSO roles. The two tests above will
  need to flip to assert the new constraint.

  4. Asher''s assumptions are all correct; not a test-data issue.


  **Open question for Lautaro on return**: whether the property-level dashboard (`list_create_roles`)
  should also surface SSO roles, or stay filtered. Default: leave it, ticket scope
  is Above Property only.


  ### Draft Slack reply (NOT POSTED — awaiting user approval)


  > Caught up on this — Asher''s investigation is right and the ticket description
  has a wrong premise about where the filter lives.

  >

  > The Above Property Dashboard endpoints don''t filter SSO roles today:

  > • `list_create_portfolio_roles` → `PortfolioRoleService.get_portfolio_roles_for_portfolio`
  (no filter)

  > • `list_create_portfolio_property_role` → `RoleService.get_property_roles_for_portfolio`
  (no filter)

  >

  > `get_portfolio_managed_roles_without_sso_organization_by_portfolio_ids` exists
  and does filter, but it''s only used in `list_create_roles` (the *property-level*
  dashboard) and `assignable_roles` (role-grant selection). So your test data isn''t
  wrong — that''s how it ships.

  >

  > Answering your Qs given the ticket''s "view + edit permissions only, no create/delete"
  framing:

  >

  > 1. *Expected end-result*: not "surface SSO roles" (they''re already surfaced)
  but "visually distinguish SSO roles and lock down what''s editable." Permissions
  editable, name read-only, delete disabled.

  > 2. *Visual distinction*: yes — inline badge/subtext is fine, same pattern as the
  permissions selector change. Separate section feels like overkill unless design
  wants it.

  > 3. *Edit name / delete*: no, per "Creating or deleting SSO roles — remains in
  Django Admin." Backend needs tightening too — the two tests you flagged (`test_update_portfolio_role__sso_organization_with_portfolio_allowed`,
  `test_delete_portfolio_role__sso_organization_with_portfolio_allowed`) should flip
  to assert the new constraint.

  > 4. *Assumptions*: all correct.

  >

  > One Q to park for Lautaro when she''s back: whether the property-level dashboard
  (`list_create_roles`) should also stop filtering SSO roles. Ticket is scoped to
  Above Property, so I''d leave that alone for now.

  '
project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 5
title: respond asher
updated: 2026-05-20 15:29:35.594135
waiting_on: null
waiting_since: null
working_on: false
---

https://canarytechnologies.slack.com/archives/C0AMJPBUH60/p1779216785548769?thread_ts=1779210047.749629&cid=C0AMJPBUH60