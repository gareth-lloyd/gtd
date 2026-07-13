---
area: null
contexts:
- react
created: 2026-07-13 09:16:05.792000
defer_until: null
due: null
energy: low
id: 2026-07-13T0916-reply-to-connor-re-ent-6844-csms-adding-removing-p
order: null
output: |
  ## Agent run 2026-07-13T11:42
  Researched ENT-6844 (https://linear.app/canary-technologies/issue/ENT-6844/enable-csms-to-add-and-remove-properties-from-portfolios)
  and the codebase, drafted a Slack reply to Connor (below). NOT sent — needs your approval.
  Thread to reply in: https://canarytechnologies.slack.com/archives/C0B1Y5K9AMC/p1783704692196209

  ### What I found in the code (backend/canary)
  - `PortfolioHotelAdmin` (portfolios/admin.py) already routes every add through
    `PortfolioService.add_hotels` and every delete through `PortfolioService.remove_hotel` —
    so admin access is NOT raw table editing; it enforces parent containment, SSO-org
    compatibility, CompanyHotelUser propagation, and role-grant cleanup, and is registered
    with `enrich_history=True` (audit trail).
  - Team grants in `canary_staff/services/canary_staff_service.py`:
    Implementation ALREADY has view/add/delete on `hotels.portfoliohotel` (line ~1007);
    CS is view-only (line ~334); Support has none. So option 1 is mostly a permissions
    change (file says notify Blake before changing any team permissions).
  - Guardrail gap: `USE_ONBOARDING_SCRIPTS_DEACTIVATE` only covers WYNDHAM + IHG_PILOT,
    and only blocks DELETES — adds to automated brand portfolios (BW, IHG, MSA, etc.)
    are unguarded, and the set has already drifted vs. the real automated list.
  - No "portfolio type" field exists — only `Portfolio.identifier` (free-form since
    ENT-6604). Connor's "portfolio types" control would need either an expanded
    identifier denylist or (better) an explicit manual/automated membership flag.

  ### Recommendation
  Option 1 with tightened guardrails. Option 2 (guided flow) defer until bulk need is
  proven. Option 3 (Manage page) is a big lift and moves membership editing toward
  customer hands — not for this.

  ### Draft Slack reply (paste into thread or approve for send)
  Hey Connor — had a look, my take: option 1, and it's ~90% built already.

  Context on where this stands today:
  • The PortfolioHotel admin page already routes every add/remove through PortfolioService, which enforces the invariants (parent-portfolio containment, SSO org checks, dashboard-user propagation, role-grant cleanup) and writes audit history. So opening that page up isn't raw table editing — it's the safe path.
  • Implementation already has add/delete on it; CS is view-only. So "enable CSMs" is a couple of lines in canary_staff_service.py (with Blake's sign-off per the rules in that file).
  • Your "portfolio types" instinct is right, and partially exists: there's a guard today that blocks deletes on automated portfolios and points at the onboarding scripts — but it only covers Wyndham + IHG Pilot, and only blocks deletes, not adds. Before widening access I'd want to (a) cover the full brand-automated set (BW, the IHG/Wyndham variants, MSA portfolios) and (b) block adds too, otherwise someone can add a hotel to the Wyndham portfolio and the automation will fight it.

  On the mechanism: there's no type field on Portfolio, just `identifier` (free-form now for region-local portfolios). Rather than a hardcoded denylist that drifts every time we add a brand (the current one already has), I'd add an explicit "membership managed by: manual / automated" flag on Portfolio and have the admin check that. Small migration + small admin change.

  Option 2 I'd hold off on — the raw admin is one-row-at-a-time but that matches the CSM use case; if bulk becomes a real need we can add a "manage hotels" view on the Portfolio page later. Option 3 is a much bigger lift (API endpoints, permission model, frontend) and puts membership editing one step from customer hands — only worth it if we want customer self-serve someday.

  So concretely: 1) add the manual/automated flag and make the guard symmetric (adds + deletes), 2) grant CS add/delete on hotels.portfoliohotel with Blake's sign-off. Happy to pick it up — it's a small pair of PRs.
project: null
source_id: https://canarytechnologies.slack.com/archives/C0B1Y5K9AMC/p1783704692196209
tags:
- morning-gtd
- slack
time_minutes: 10
title: 'Reply to Connor re: ENT-6844 — CSMs adding/removing properties from portfolios'
updated: 2026-07-13 14:23:36.449131
waiting_on: null
waiting_since: null
working_on: false
---

Group DM (Jul 10, saved): "not urgent at all but would love your thoughts here" → https://linear.app/canary-technologies/issue/ENT-6844/enable-csms-to-add-and-remove-properties-from-portfolios
https://canarytechnologies.slack.com/archives/C0B1Y5K9AMC/p1783704692196209