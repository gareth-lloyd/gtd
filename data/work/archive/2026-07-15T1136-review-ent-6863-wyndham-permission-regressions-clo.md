---
area: null
contexts:
- react
created: 2026-07-15 11:36:23.425516
defer_until: null
due: null
energy: low
id: 2026-07-15T1136-review-ent-6863-wyndham-permission-regressions-clo
order: null
output: |
  ## Agent run 2026-07-15T14:07

  Reviewed ENT-6863 (https://linear.app/canary-technologies/issue/ENT-6863/investigate-wyndham-portfolio-and-recordings-permission-regressions) thread + sanity-checked the permission code. Verdict: closure rationale is PLAUSIBLE BUT INCOMPLETE — the "user error" label is asserted, not demonstrated, and one question in the thread was never answered.

  ### Corrections to the summary
  - The ticket is NOT closed — it's still **Todo**, assigned to Andrés Figueira, priority Low. Connor said "No regressions - chalk it up to Wyndham user error" and deferred investigation to next cycle; nobody canceled it.
  - Origin: Slack thread synced to the ticket (https://canarytechnologies.slack.com/archives/C04STT7UPRQ/p1784042142911569?thread_ts=1784042142.911569&cid=C04STT7UPRQ), context is the new Above Property Call Dashboard rollout.

  ### What actually happened
  - **Issue #1 (portfolio not visible)**: Connor called it a red herring — the Wyndham role was missing the "View Portfolio" permission; he added two permissions to PortfolioRole id=1 ("Portfolio manager", canary-admin/permissions/portfoliorole/1/change/). Users (Justin, Jen) confirmed fixed. Since the dashboard is new, "never configured" is more likely than "regressed" — reasonable, but nobody verified it ever worked before, so "no regression" is unproven.
  - **Issue #2 (recordings tab)**: the day BEFORE, the same permissions were added to two "WHR" roles that Justin already holds — and it did NOT work. It only worked after adding them to the third role. Andrea asked exactly the right question ("why wasn't it working previously since Justin has the roles we added the permissions to") — never answered. Connor's follow-up assumption ("we take the union of permissions across roles?") was also left hanging.
  - **Side issue (fwd categories filter, 0 calls for Reservations+Handled)**: resolved as by-design — a forwarded call is by definition not handled; Justin should filter by intent. Fine.

  ### Code sanity-check (canary backend)
  - Union across roles IS how it works: `PortfolioPermissionService.get_all_user_permissions_for_portfolios` (backend/canary/permissions/services/portfolio_permission.py:66) unions permission grants from ALL of the user's PortfolioRoleGrants (custom + default). So Connor's assumption is correct — which makes Justin's failure with the two WHR roles genuinely unexplained, not user error.
  - Best candidate explanation: **permissions are portfolio-scoped**. PortfolioRole and PortfolioRoleGrant both carry a portfolio FK, and every check runs against the specific portfolio_id being viewed. If Justin's WHR role grants sit on a different (e.g. child) portfolio than the one the Above Property dashboard checks, adding perms to those roles does nothing for that view — while "Portfolio manager" (role id 1, presumably on the top-level Wyndham portfolio) fixes it. Checkable in ~2 min in admin: compare portfolio_id on Justin's grants vs. role 1's portfolio.
  - Second candidate: **wipe-and-regrant of non-SSO roles**. `PortfolioUserManagementService.__set_user_portfolio_roles` (backend/canary/portfolios/services/portfolio_user_management.py:389) deletes ALL non-SSO PortfolioRoleGrants for a portfolio before re-adding the selected ones — any UI edit of Justin's assignments between the perm-add and his test could have dropped the WHR grants (Andrea noted they "aren't SSO roles"). Also called from canary_staff_service.py:1420. Audit trail: PermissionsEventService events + PortfolioRoleGrant timestamps would confirm/refute.
  - Residual risk flagged in-thread: Andrea said "those roles will be cleaned up eventually :)" — the fix added perms to ad-hoc roles; a later role cleanup (there are precedent onetime_remove_wyndham_* commands) could silently re-break this.

  ### Recommendation
  Closure-as-user-error is premature for issue #2. Keep the deferred next-cycle investigation but make it concrete on the ticket: (1) check which portfolio Justin's WHR role grants are scoped to vs. the dashboard's portfolio; (2) check PermissionsEvent/grant timestamps for a wipe-regrant between the two fix attempts; (3) document which role/portfolio is the canonical place for Above Property Call Dashboard perms so role cleanup doesn't regress it. Happy to draft a Linear comment with these leads if you want (not posted — needs your approval).
project: null
source_id: https://linear.app/canary-technologies/issue/ENT-6863/investigate-wyndham-portfolio-and-recordings-permission-regressions
tags:
- morning-gtd
- linear
- from-awareness
time_minutes: 10
title: 'Review ENT-6863: Wyndham permission ''regressions'' closed as user error —
  sanity-check before next cycle'
updated: 2026-07-15 16:20:41.258835
waiting_on: null
waiting_since: null
working_on: false
---

Both issues (portfolio not visible, recordings tab) fixed by adding role permissions; no regressions found, investigation deferred to next cycle.
https://linear.app/canary-technologies/issue/ENT-6863/investigate-wyndham-portfolio-and-recordings-permission-regressions