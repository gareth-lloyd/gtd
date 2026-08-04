---
area: null
completed_at: 2026-08-04 15:13:13.786634
contexts:
- react
created: 2026-08-04 10:41:27.963925
defer_until: null
due: 2026-08-04
energy: medium
id: 2026-08-04T1041-reply-in-ent-group-dm-confirm-which-user-managemen
order: null
output: |
  ## Agent run 2026-08-04T12:12:31Z

  Researched Stephanie's thread (https://canarytechnologies.slack.com/archives/C0BLZ4Z9E67/p1785774630447929),
  the aggregated Notion doc (https://app.notion.com/p/canarytechnologies/User-Management-Triage-Efficiency-Aggregated-Overview-3b18146861518163a0d4cff07c3389e3),
  and ENT's Linear projects/issues. NOT posted to Slack — draft below awaits your approval.

  ### Verified ENT status

  - SCIM: eng design ENT-6491 "In Review" since 2026-06-23, assignee Lautaro, priority Low
    (https://linear.app/canary-technologies/issue/ENT-6491). Project "Support SCIM for SSO" is
    "Ready for Eng", target 2026-08-31, NO lead, implementation tickets not broken out
    (https://linear.app/canary-technologies/project/support-scim-for-sso-f27b59ecae9e).
  - CS portfolio editing in Django: ENT-7039 (add hotels) + ENT-7040 (add portfolio users), both
    Todo, assigned Andrés Figueira (https://linear.app/canary-technologies/issue/ENT-7039,
    https://linear.app/canary-technologies/issue/ENT-7040). ENT-6844 duped into them. The Notion
    doc calls this "In progress" — it is really scoped-and-assigned, not started. ENT-5290
    (Implementations-team Django portfolio perms) is Done.
  - Portfolio Typing: Implementation, lead Andrea, target 2026-08-31
    (https://linear.app/canary-technologies/project/portfolio-typing-60798dba32e0); ENT-6886
    (Django admin support for portfolio types) already Deployed. Prerequisite for safe CS edits.
  - Portfolio Reconciliation - Portfolio Membership: Product Definition, lead Gareth, target
    2026-08-31 (https://linear.app/canary-technologies/project/portfolio-reconciliation-portfolio-membership-4171e7fc6c55).
    Related: "Make Salesforce reliable as source of truth" in Implementation, lead Gareth
    (https://linear.app/canary-technologies/project/make-salesforce-reliable-as-source-of-truth-37efa69bf927).
  - Bulk edits: NOTHING in flight. ENT-5114 bulk user upload tool exists (Done); ENT-2651
    (Wyndham bulk portfolio users) Backlog; ENT-6982 (access to bulk upload tool) sitting in
    Triage. The 38%-bulk / 24%-bulk numbers in the doc are uncovered — genuine gap.
  - SSO adjacent: auto-delete SSO users removed client-side — Backlog (subsumed by SCIM);
    self-serve link email<->SSO account — Backlog; self-service SSO setup for clients — Paused
    (https://linear.app/canary-technologies/project/enable-self-service-sso-setup-and-management-for-clients-d9516660adc5).

  ### DRAFT REPLY (for the ENT group DM thread — needs your approval before posting)

  Confirming ENT status on the user-management pieces:

  *In flight:*
  - *SCIM / SSO auto-provisioning* — eng design done and in review (ENT-6491, Lautaro).
    Implementation tickets not yet broken out and it's currently low priority, so the ~50-ticket
    chain-SSO win needs a prioritization call plus real engagement with Marriott/Wyndham/IHG IdP teams.
  - *Portfolio typing* — in implementation (Andrea, target end of Aug). Django admin support for
    portfolio types is already deployed (ENT-6886). This is the foundation for opening portfolio
    editing beyond eng safely.
  - *Portfolio reconciliation + Salesforce as source of truth* — reconciliation is in product
    definition (me, target end of Aug); the SF source-of-truth project is in implementation.
    Together these target the wrong-SF-link / membership-drift ticket class.

  *Scoped & assigned, not started:*
  - *CS editing portfolios in Django* — ENT-7039 (CSMs add hotels to non-enterprise/sub-brand
    portfolios) and ENT-7040 (CSMs add portfolio users), both with Andrés, gated on portfolio
    typing. (Implementations team already has Django portfolio perms — ENT-5290.)

  *Backlog / paused (not committed):*
  - Auto-delete SSO users removed client-side (would be subsumed by SCIM deactivation);
    self-serve email<->SSO account linking; self-service SSO setup for clients (paused).

  *Not planned at all:*
  - *Bulk editing* — beyond the existing bulk user upload tool, there's nothing in flight for
    bulk portfolio edits or bulk role changes. The 38% bulk-shaped ticket volume in the doc isn't
    covered by anything ENT has planned, so that's a real gap for next step 2a.

  ### Suggested follow-up

  The Notion doc row 7 says portfolio-editing-for-CS is "In progress"; it's actually Todo.
  Worth flagging so Stephanie's doc stays accurate.
project: 2026-04-16T1210-unblock-team
source_id: https://canarytechnologies.slack.com/archives/C0BLZ4Z9E67/p1785774630447929
tags:
- morning-gtd
- slack
time_minutes: 15
title: 'Reply in ENT group DM: confirm which user-management pieces are in progress'
updated: 2026-08-04 15:13:13.786622
waiting_on: null
waiting_since: null
working_on: false
---

Stephanie Barry shared the aggregated User Management Triage Efficiency doc; next step 1 asks ENT to confirm exactly which pieces are in progress/planned (SCIM, editing portfolios, bulk edits, etc.).
https://canarytechnologies.slack.com/archives/C0BLZ4Z9E67/p1785774630447929