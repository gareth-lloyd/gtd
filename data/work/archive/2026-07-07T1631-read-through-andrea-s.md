---
area: management
contexts: []
created: 2026-07-07 16:31:37.431367
defer_until: null
due: 2026-07-14
energy: medium
id: 2026-07-07T1631-read-through-andrea-s
order: 4
output: |
  ## Agent run 2026-07-08T06:59:34Z

  Read the three design docs surfaced in the 2026-07-07 1-1 note. Two are the
  new "portfolio membership" pair Andrea worked on with Fable (created 2026-07-06,
  status WIP, owner tagged); the third ("portfolio typing") is older (last edited
  ~2026-06-03) and re-surfaced as related context.

  ### 1. Hotel Portfolio Membership Validation  (Design Doc, WIP)
  https://app.notion.com/p/39581468615181c1baa1cd06a64841a1
  - **Problem:** enterprise portfolio membership goes stale fast — hotels linger in
    portfolios they left, portfolios miss hotels SF says are live. Membership gates
    real behavior (enterprise features, APD, reporting, flag targeting), so bad data
    silently mis-configures customers. Today only 6 MSA/deployment portfolios are
    validated (`sync_enterprise_deployment_portfolio`); everything else — main brand
    portfolios (WYNDHAM/BEST_WESTERN/IHG + children), Marriott Managed, smaller
    enterprises, and structural invariants — has **no validation at all**.
  - **Solution:** a declarative validation-spec registry in a new
    `backend/canary/portfolios/validation/` package. Each spec = portfolio +
    expected-membership resolver + policy (REPORT_ONLY / AUTO_SYNC) + severity + regions.
    Daily cron per region, one Slack digest to the existing drift channel + structured
    logs for Groundcover.
  - **Key design choices worth your eye:**
    - `ExpectedMembership.authoritative: bool` — non-authoritative resolvers (cached SF
      brand fields) only emit `missing` findings, never removals. Prevents a stale-cache
      false-positive avalanche.
    - **Report-only first**, per-portfolio graduation to auto-sync via a reviewed one-line
      change after ≥2 weeks zero false positives. Removals from main brand portfolios are
      explicitly OUT of auto-sync scope.
    - Zero new Salesforce API load in phases 1–2 (reads local `SalesforceHotelAccount.account_data`).
    - Deliberate import-direction discipline: `portfolios` must never import `onboarding`;
      SF-reading resolvers register *into* the registry from the onboarding side.
    - Multi-region model: region-local validation only; residency-vs-geography treated as its
      own permanently-report-only `region_mismatch` finding; a Phase-2 cross-region orphan /
      double-homed report closes the single-region blind spot via Groundcover reconciliation.
  - **4 decisions the doc asks the team for** (relevant to your 1-1):
    1. Auto-sync appetite per portfolio + who signs off on each graduation.
    2. Source of truth for Drury / TUI Blue / Four Seasons — adopt `Associated_Enterprise_Deployments__c`
       SF label (needs SF ops tagging) or accept as registered gaps.
    3. Channel ownership — drift default is **#epd-enterprise** (`C047K6WSUJY`), already busy;
       dedicated channel? who owns triage rotation? NB doc flags that Canary Bot posted drift
       there Feb 27–Mar 2 2026 then went silent — needs investigating whether the flag was
       disabled or the path broke.
    4. Should the Wyndham regional-children spec (derivational, deterministic) skip straight to
       auto-sync after one bake cycle.
  - **Dependency on your PR #45154** (https://github.com/canary-technologies-corp/canary/pull/45154):
    Phases 1–2 have zero file overlap with it; Phase 3 (unifying the deployment sync as a
    resolver, retiring `REPORT_ONLY_PORTFOLIOS`) waits until #45154 merges and settles.

  ### 2. Code Execution Plan  (child of doc #1)
  https://app.notion.com/p/3958146861518103a557d15cd87396b4
  - PR-by-PR breakdown, each independently shippable + report-only until an explicit graduation step:
    - **PR1** validation core + structural invariants (move `EXCLUSIVE_/REPLACEABLE_PORTFOLIOS`
      out of `add_to_portfolio_plan.py` into `hotels/models/portfolio.py`).
    - **PR2** brand + country + brand-partition resolvers, big-3 specs (in `onboarding/validation_specs.py`).
    - **PR3** cron command, Slack digest, observability (GrowthBook kill-switch
      `portfolio_membership_validation_enabled`, structlog events, k8s CronJob + Groundcover monitors as
      out-of-repo follow-ups).
    - **PR4** Marriott/MVW/Aimbridge specs; **PR5** drift-exception + finding models + admin workbench;
      **PR5b** cross-region orphan report.
    - **PR6** (after #45154) wrap deployment sync as `enterprise_deployment_resolver` — highest-risk,
      behavior-preserving refactor; **PR7** auto-sync path + first graduations.
  - Sequencing: 1→2→3 sequential; 4/5/5b parallel after 3; 6→7 after #45154.
  - Names sharp edges verified in `portfolios/services/portfolio.py`: `add_hotels` is atomic-per-batch,
    auto-adds parent, raises on multi-level hierarchy + SSO-org mismatch → apply per-hotel with isolation;
    `remove_hotel` needs `remove_from_children=True`. (Matches your saved rule to route membership
    changes through PortfolioService, not PortfolioHotel directly.)

  ### 3. Typed Portfolios — Design Doc  (older, ~2026-06-03)
  https://app.notion.com/p/37481468615181b6b94bd569ba782491
  - **Thesis:** `Portfolio` is one overloaded concept doing many jobs (brand grouping, MSA membership,
    APD backing, SSO enrollment, ad-hoc grouping); nothing in the schema says which, so ≥8 in-code
    structures and ~20+ call sites re-derive "type" from the identifier string. Proposes an explicit
    multi-valued `PortfolioType` via a `PortfolioTypeAssignment` through-model (PARENT_BRAND, BRAND,
    MSA, MANAGEMENT_COMPANY, ABOVE_PROPERTY_DASHBOARD, SSO_ORGANIZATION, AD_HOC), with behavioral rules
    in a code-side registry.
  - Keeps the one-level hierarchy cap deliberately ("add breadth, not depth"); `identifier` and
    `visibility` stay out of scope; INTERNAL is deliberately NOT a type.
  - Main review debate: which of SSO_ORGANIZATION / ABOVE_PROPERTY_DASHBOARD are better left *derived*
    from existing FKs vs. declared as types.

  ### Cross-doc note for your 1-1
  The two docs are in tension in a useful way. The Validation doc leans heavily on identifier-string
  matching / hard-coded frozensets (`MSA_PORTFOLIO_IDENTIFIERS`, brand-ID sets, country partitions) —
  exactly the fragility the Typed Portfolios doc wants to eliminate by making purpose queryable.
  Typed Portfolios' own open questions explicitly flag a coupling-vs-decoupling tension with the
  rules-engine `GroupAttributes` doc that "needs settling with that doc's owner before either ships."
  Worth deciding whether Validation should be built to read typed portfolios (once they exist) or
  ship first on identifier matching and migrate later — the execution plan currently assumes the latter.

  No edits or comments made to any Notion doc (read-only).
project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 15
title: Read through Andrea's new design docs mentioned in latest 1-1 notes. plan work
updated: 2026-07-14 16:15:53.787642
waiting_on: null
waiting_since: null
working_on: false
---

https://app.notion.com/p/canarytechnologies/Andrea-Gareth-1-1-journal-3568146861518006b9daf302fb27807c?source=copy_link#3968146861518065a2e8fbb075aa3722