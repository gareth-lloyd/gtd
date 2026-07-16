---
area: null
contexts: []
created: 2026-07-16 12:09:16.367329
defer_until: null
due: null
energy: low
id: 2026-07-16T1209-answer-ani-s-question
order: null
output: |-
  ## Agent run 2026-07-16T12:16:01

  Ani's question (Slack: https://canarytechnologies.slack.com/archives/C04STT7UPRQ/p1784147743714569):
  why was the Wyndham Manager role not configured to be visible on the EMEA portfolio?
  Refers to ONC-24684 (https://linear.app/canary-technologies/issue/ONC-24684/jenniferwilliams-does-not-see-wyndham-manager-role-for-emea-portfolio),
  already fixed by Kevin Cormier by editing PropertyRole 109 in EU admin
  (https://eu.canarytechnologies.com/canary-admin/permissions/propertyrole/109/change/).

  ### Answer (from code investigation, canary repo)

  - A role only appears in a portfolio's Users page if its `PropertyRole.portfolio`
    FK points at that portfolio: the picker is served by
    `ListCreatePortfolioPropertyRolesView` -> `RoleService.get_property_roles_for_portfolio`
    (backend/canary/permissions/services/role.py:1705), which filters
    `portfolio_id=<portfolio>, permission_context=PROPERTY`. The `portfolio` FK
    *is* the "visible in portfolio view" switch Kevin flipped.
  - Wyndham roles are not created by onboarding: `WyndhamRolesAndPermissionsProvider`
    deliberately creates zero roles (roles=[]) because Wyndham roles are granted via
    Okta SSO (`OrganizationRoleMapping` maps SAML attribute values -> PropertyRole).
    A PropertyRole may be scoped to the SSO organization only (portfolio NULL) —
    valid for SSO auto-granting, but invisible to manual portfolio user management.
  - So: the EU-datacenter "Wyndham Manager" role (PropertyRole 109) was hand-configured
    (admin) as SSO-org-scoped without the EMEA portfolio link, while the US-datacenter
    equivalent got the portfolio link for NAMER. There is no automated step that links
    Wyndham SSO roles to portfolios — it's a per-datacenter manual admin step, and it
    was simply missed when the EMEA side was set up. Manual-config gap, not a code bug.
  - Caveat: I had no prod EU read access from this session, so the "SSO-only scope"
    pre-fix state is inferred from code paths. To confirm who/when: open the role's
    admin page and click "Events for object" (PropertyRole is eventable), which shows
    the creation + Kevin's change history.

  ### Suggested follow-ups (not done)

  - Sweep EU (and other DCs) for other Wyndham roles with the same gap:
    `PropertyRole.objects.filter(sso_organization__name__icontains="wyndham", portfolio__isnull=True)`
    — read-only, via /debug_in_shell if desired.
  - Draft Slack reply for #C04STT7UPRQ thread (NOT sent, needs your approval):
    "The Manager role only shows on a portfolio's Users page if the role record is
    explicitly linked to that portfolio. On the EU datacenter the Wyndham Manager role
    was set up scoped to the Wyndham SSO organization only — granted automatically via
    the Okta role mappings but never linked to the EMEA portfolio, so the portfolio UI
    didn't list it. The NAMER copy (US datacenter) did have the portfolio link, which is
    why Jennifer saw it there. These roles are configured manually per datacenter
    (Wyndham onboarding intentionally creates no roles since they come from SSO), so this
    was a missed manual config step when EMEA was set up rather than a code bug. Kevin
    added the missing link (ONC-24684), so it's visible now; we'll check the other
    Wyndham SSO roles on EU for the same gap."

  ## Agent run 2026-07-16T12:36:44

  Reply POSTED to Ani's thread with user approval:
  https://canarytechnologies.slack.com/archives/C04STT7UPRQ/p1784194585038289?thread_ts=1784147743.714569&cid=C04STT7UPRQ
  Remaining follow-up (not done): sweep EU for other Wyndham SSO roles missing the
  portfolio link (PropertyRole.objects.filter(sso_organization__name__icontains="wyndham",
  portfolio__isnull=True)).

  ## Agent run 2026-07-16T12:41:32

  Follow-up sweep DONE — user ran read-only /debug_in_shell script on US + EU prod:
  - US prod Wyndham org (49): all 7 SSO roles linked to portfolio 166. Clean.
  - EU prod Wyndham org (36): all 6 roles linked to portfolio 34 (incl. 109
    'Wyndham manager' from Kevin's ONC-24684 fix, plus 110/111). Clean.
  - Only gaps are sandbox orgs (EU roles 143-145, US roles 167-168); neither
    sandbox org has any portfolio to link to — no action recommended.
  - Side finding: on BOTH prod orgs the SAML values whrlevel1 / whrlevel2 /
    whropsrms map to nothing, while the matching 'WHR Level 1/2' / 'WHR OPS & RMS'
    roles exist and are portfolio-linked. Users arriving with those SAML attrs get
    no role. Possibly deprecated mappings — worth checking with Wyndham SSO config
    owner. Not actioned.
project: null
source_id: null
tags: []
time_minutes: 5
title: answer Ani's question
updated: 2026-07-16 12:41:32.408215
waiting_on: null
waiting_since: null
working_on: false
---

https://canarytechnologies.slack.com/archives/C04STT7UPRQ/p1784147743714569

May require /debug_in_shell