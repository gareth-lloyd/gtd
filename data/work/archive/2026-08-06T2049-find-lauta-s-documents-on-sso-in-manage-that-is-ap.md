---
area: null
completed_at: 2026-08-07 13:42:21.929280
contexts: []
created: 2026-08-06 20:49:47.128643
defer_until: null
due: null
energy: low
id: 2026-08-06T2049-find-lauta-s-documents-on-sso-in-manage-that-is-ap
order: null
output: |
  ## Agent run 2026-08-07T09:05Z

  ### The document you're looking for

  **PRD: SSO management section in the Manage app** — Lautaro Mena, 2026-06-17, status
  Draft. https://app.notion.com/p/382814686151819ea24de669c6d33ea9
  (Notion path: Pod Homepages › Enterprise › PRDs)

  Framing: an internal-only "SSO" section in the existing `/manage/` app, Canary-staff
  gated. Origin stated as ENT-6440 (Create SSO for Highway West Vacations)
  https://linear.app/canary-technologies/issue/ENT-6440 — the manual work he had to do
  to complete that integration.

  Two features in scope:
  - **5.1 Create an SSO organization** from Manage instead of Django admin (entity ID,
    SSO URL, signing cert, NameID format, binding, provisioning flags, email domain
    list) + **prefill by pasting the customer's IdP metadata XML**.
  - **5.2 Add hotels (and optionally their users) to an org** — accepts hotels and/or
    portfolios, portfolios expand + dedupe, optional email-domain filter, idempotent
    skip-and-log, no dry-run/preview, results summary after apply.

  Explicit non-goals: customer-facing self-service, SLO, sso_hotel_id automation, SCIM,
  and "porting every Django-admin SSO field into Manage in one shot."

  Stated goal, verbatim: *"Internal teams should not need Django admin or manual data
  changes for routine SSO work."*

  ### The "blocking integrations" claim — exact source

  #epd-enterprise-engineers, 2026-06-18. He posts the PRD, then immediately:
  https://canarytechnologies.slack.com/archives/C0B1MN8F869/p1785274099197259 (thread
  root: https://canarytechnologies.slack.com/archives/C0B1MN8F869/p1781805314123839)

  > "Another missing piece for SSO [PRD link]"
  > "The current goal is to move SSO integration responsibilities to the implementation
  > team. I think this is a key feature that is needed to start that process.
  > @Andrea @Connor please review it when you have a minute."

  So the claim is his own, addressed to Andrea Bradshaw and Connor Swords, and it is
  softer than "blocking" — "a key feature that is needed to start that process." I found
  no message where anyone else asserts the handoff is blocked on this.

  ### Linear state (as of 2026-08-06)

  Project **Self service SSO org management** — lead Lautaro Mena, status **Planned**,
  Aug 1 – Sep 30, initiative "SSO Enhancements"
  https://linear.app/canary-technologies/project/self-service-sso-org-management-2df14b58fe5e

  Milestone "Manage app SSO section" — 7 tickets, **all in Backlog, none started**:
  - ENT-6962 Manage app: new SSO section with organization list https://linear.app/canary-technologies/issue/ENT-6962
  - ENT-6963 Backend: endpoint to create an SSO organization from Manage https://linear.app/canary-technologies/issue/ENT-6963
  - ENT-6964 Backend: parse IdP metadata XML to prefill org config https://linear.app/canary-technologies/issue/ENT-6964
  - ENT-6965 Backend: service to add hotels/portfolio to an SSO org (idempotent) https://linear.app/canary-technologies/issue/ENT-6965
  - ENT-6966 Manage app: create SSO organization flow (UI) https://linear.app/canary-technologies/issue/ENT-6966
  - ENT-6967 Manage app: org detail page with "Add hotels & users" https://linear.app/canary-technologies/issue/ENT-6967
  - ENT-6968 Manage app: configure org IdP from metadata XML (+ override warning) https://linear.app/canary-technologies/issue/ENT-6968
  - ENT-6969 "TODO" placeholder for the customer-facing phase https://linear.app/canary-technologies/issue/ENT-6969

  A second, older project **Enable self-service SSO setup and management for clients** is
  **Paused** https://linear.app/canary-technologies/project/9d657022-b75f-46c7-bfd1-42074df3a346

  ### On your "dumb version of Django admin" suspicion

  Partly right, partly not — worth separating:

  **Not a new app.** `/manage/` already exists as a first-class internal staff Vue app
  (`frontend/manage/`) with ~15 sections already shipped: payments, onboarding,
  properties, tips, kiosk configurator, access-requests, custom domains, cohorts,
  runbooks, issues, omni, check-in configurations. Adding an SSO section is extending an
  established surface, not standing up an admin clone.

  **But the scope is a Django-admin re-skin.** 5.1 is straightforwardly CRUD over
  `sso.Organization` fields that already exist in Django admin. The only genuinely new
  capability in the whole PRD is the metadata-XML parser (ENT-6964) and the
  hotel/user association service with its exclusivity rules (ENT-6965) — and that second
  one is real logic (external-footprint check across CompanyHotelUser /
  PropertyRoleGrant / AnalyticsRoleGrant / PortfolioRoleGrant / PortfolioWidePropertyRoleGrant)
  that has no Django-admin equivalent and is currently done by hand in shell. If you want
  to push back, the sharp version is: **ENT-6964 and ENT-6965 are the load-bearing
  tickets; ENT-6962/6963/6966/6967/6968 are UI over Django admin.** Ship the two, skip or
  defer the five, and the handoff argument mostly survives.

  **Counter-evidence on capability that supports your read.** #epd-enterprise, 2026-03-31
  https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1774987136766569 — Taylor
  Kirchwehm (implementation) had been self-serving SSO user/property assignment weekly for
  Marriott via User Data Import; it broke via PR #39963 and Lauta shipped a fix the same
  day (PR #42333). Taylor: *"this comes up at least once a week with Marriott hotels and
  being able to self-serve was a huge time save."* That's implementation staff already
  self-serving a comparable task through an existing tool — it argues the gap is narrower
  than the PRD implies.

  ### Wider pattern — this is one of four related docs he's circulating

  He's been running a broad "reduce eng-in-the-loop for user management" push since June:
  1. PRD: SSO management section in the Manage app (above) — 2026-06-17
  2. SCIM 2.0 Provisioning for SSO (design doc) https://www.notion.so/canarytechnologies/SCIM-2-0-Provisioning-for-SSO-38881468615181208ea5c996dffd3927 — posted 2026-06-24, ENT-6491 now closed
  3. Roles & Portfolios — Open Questions and Rework https://www.notion.so/canarytechnologies/Roles-Portfolios-Open-Questions-and-Rework-3ab81468615181729117c1610acd47c5 — posted 2026-07-28
  4. Proposal: Managed Support Access for CS https://www.notion.so/canarytechnologies/Proposal-Managed-Support-Access-for-CS-3ae81468615181abbf82ea4f92ef9794 — posted 2026-07-31; he himself flags it "goes in an opposite direction than Support Access Approval Flow", and defended it in the group DM by quoting Claude on internal-admin-tool-vs-impersonation. Laura DeWald agreed; noted Blake had said the opposite two days prior.

  Also his 2026-07-20 proposal for an org-level setting to make non-SSO grants inert at an
  org's hotels https://canarytechnologies.slack.com/archives/C0B1MN8F869/p1784571935197889
  and ENT-6973 (spike: central SSO role management with local login).

  ### Other docs worth a look
  - PRD: Self-Service SSO Management for Customers (the *customer*-facing one, earlier)
    https://app.notion.com/p/31e81468615181b9b365ce2d4daf5a33 — its top priority is
    "SSO Test Mode & Diagnostic Logs", flagged as "arguably the highest-value feature."
  - SSO Onboarding — Customer Success Playbook https://app.notion.com/p/37b814686151816fad1af44f8e67605c
  - Canary SSO Setup Guide (customer-facing) https://app.notion.com/p/329814686151811ba0e9c83835c89641
  - User Management & Triage Efficiency — Aggregated Overview https://app.notion.com/p/3b18146861518163a0d4cff07c3389e3 (702-ticket reclassification, updated 2026-08-05)

  ### What I did not do
  No comments, no status changes, no messages posted anywhere. Read-only throughout.

  ### Open question for you
  Nobody outside Lauta has stated that the Manage SSO section blocks the integrations
  handoff. If the handoff is actually blocked, the blocker is probably in the ENT-6965
  association logic (currently shell-only) rather than the org-CRUD UI — worth confirming
  with Connor/Andrea before the project leaves Planned on Sep 30.
project: null
source_id: null
tags: []
time_minutes: 5
title: Find Lauta's documents on SSO in /manage that is apparently blocking integrations.
updated: 2026-08-07 13:42:21.929268
waiting_on: null
waiting_since: null
working_on: false
---

I lowkey suspect he's underestimating their technical capability and wanting to build a dumb version of django admin. 

Start by finding eng designs or other documents created by lauta Mena in the last few months. This will concern passing SSO integrations to integrations team, or other aspects of self service sso setup. 

Also search slack particularly the enterprise channels for messages related to this from him.