---
area: null
contexts: []
created: 2026-05-27 15:49:39.043474
defer_until: null
due: null
energy: low
id: 2026-05-27T1549-portfolio-typing-needs-to-be-pushed
order: null
output: |
  ## Agent run 2026-05-27T21:05Z

  Sketched a product doc proposing typed Portfolios. The Notion "Rules-based hotel configuration" doc proposes a `GroupAttributes` abstraction that is *intentionally* decoupled from the Portfolio table ("Groups might correspond 1-1 with portfolios, but they are *logical* groups which are valid whether or not they have a corresponding database object"). This sketch argues the *opposite*: until we type the Portfolios we already have, the rules engine has no trustworthy substrate.

  ---

  # Typed Portfolios — sketch

  ## Problem

  Today `Portfolio` is a single bag for semantically distinct groupings:
  - **Parent brand**: WYNDHAM, IHG, BEST_WESTERN
  - **Sub-brand**: implicit / mostly absent
  - **MSA / commercial agreement**: MSA_WYNDHAM_CONNECT_GMS, MSA_BEST_WESTERN_GMS
  - **Management company**: ad-hoc, no schema
  - **Region / market**: ad-hoc, encoded in name
  - **Customer-owned grouping**: portfolios that map to a regional manager's view
  - **Internal / demo / dev**: NULL identifier

  Evidence:
  - `Portfolio.identifier` is a 40+ value flat enum mixing all the above (`backend/canary/hotels/models/portfolio.py`)
  - `parent` is a single self-FK with a one-level cap enforced in `PortfolioService.add_hotels()` — no way to express "Super 8 is a sub-brand of Wyndham" *and* "Aimbridge manages these Super 8s"
  - `PUBLIC_PORTFOLIO_IDENTIFIERS` / `DISCOVERABLE_PORTFOLIO_IDENTIFIERS` are frozen sets in code, which is what we'd do if we had a `type` and a `visibility` field
  - Feature-flag targeting passes `portfolio.identifier` to GrowthBook as a string (`feature_flags/utils/base_features.py`) — the rollout doc explicitly flags this as a reliability risk if portfolio membership is wrong

  The rules-engine proposal will fail on this foundation. `GroupAttributes(parent_brand_id=…, brand_id=…, msa=…, management_company_id=…)` requires those four things to be *retrievable per hotel*. Today they live as overlapping membership in untyped portfolios. We will reverse-engineer them from identifier-string parsing and the analyst's memory — exactly the drift problem the rules engine is supposed to fix.

  ## Proposal

  Add `Portfolio.kind` (or `type` — naming TBD) as a non-null enum:

  | kind | example | semantics |
  | --- | --- | --- |
  | `PARENT_BRAND` | Wyndham, IHG, BW | top of brand tree; mutually exclusive per hotel |
  | `BRAND` | Super 8, Days Inn, Holiday Inn Express | sub-brand; parent must be `PARENT_BRAND` |
  | `MSA` | Wyndham Connect GMS, Wyndham Connect Plus | commercial agreement scoped under a parent brand |
  | `MANAGEMENT_COMPANY` | Aimbridge, Highgate | cross-brand operator |
  | `CUSTOMER_GROUPING` | "Aimbridge East Coast Wyndhams" | customer-defined slice for reporting / RBAC |
  | `REGION` | Wyndham EU | geographic override layer |
  | `INTERNAL` | Canary demo, QA | excluded from production rules and rollouts |

  ### Type-driven invariants

  Each kind comes with rules the flat model can't express:
  - `PARENT_BRAND` has no `parent`; a hotel can belong to at most one
  - `BRAND.parent.kind == PARENT_BRAND`
  - `MSA.parent.kind == PARENT_BRAND` (the MSA sits under the parent brand, not the sub-brand)
  - `MANAGEMENT_COMPANY` has no `parent` and crosses brands
  - `REGION` has no `parent` but carries a country / region attribute set
  - `CUSTOMER_GROUPING` is the only kind end-customers can create; the rest are Canary-controlled
  - `INTERNAL` is invisible to GrowthBook targeting, the rules engine, and customer-facing surfaces

  ### Relationship to the rules-engine `GroupAttributes`

  The Notion `GroupAttributes(parent_brand_id, brand_id, msa, management_company_id, countries, canary_region)` becomes a typed projection of real DB rows:

  ```
  HotelAttributes(hotel) = {
    parent_brand_id:       hotel.portfolios.filter(kind=PARENT_BRAND).single(),
    brand_id:              hotel.portfolios.filter(kind=BRAND).single(),
    msas:                  hotel.portfolios.filter(kind=MSA),
    management_company_id: hotel.portfolios.filter(kind=MANAGEMENT_COMPANY).single(),
    region:                hotel.portfolios.filter(kind=REGION).single_or_none(),
    ...
  }
  ```

  Two consequences:
  1. `GroupAttributes` stops being an in-code logical construct disconnected from data — it's a typed projection of real rows. Drift becomes detectable.
  2. The "mutual exclusivity of roots" rule the Notion doc relies on becomes a DB-enforceable constraint on `PARENT_BRAND` membership rather than a runtime assertion.

  ### What this is *not*

  - Not a redesign of permissions / RBAC. PortfolioRole, PortfolioRoleGrant etc. continue to attach to a Portfolio regardless of kind.
  - Not a replacement for the rules engine — it's the substrate the rules engine reads from.
  - Not a renaming. Existing `identifier` strings stay as stable external keys; `kind` is added alongside.

  ## Migration shape

  1. Add nullable `kind` field + enum. Ship.
  2. Backfill the 40+ identifier-based portfolios — parent brands, MSAs, BW / Wyndham / IHG variants. PR-reviewed.
  3. Make `kind` non-null. Default the rest to `CUSTOMER_GROUPING` or `INTERNAL`.
  4. Add invariant checks in `PortfolioService.create_portfolio` / `add_hotels` (uniqueness of `PARENT_BRAND` per hotel, parent-kind FK rules).
  5. Audit existing `parent` relationships against the new rules; fix or grandfather with a flag.
  6. Rules engine can now use kind-typed queries instead of identifier-string regex.

  ## Open questions

  - Does a hotel belong to *one* `BRAND` or many? Suspect one in practice — worth confirming with examples (does a property ever flag-flip mid-management between two sub-brands?).
  - Where do `BRAND` and `MSA` interact for the override-weights problem? The Notion doc shows MSA + sub-brand siblings under parent brand. Do we ever need diamond-style inheritance between *brand* and *MSA*, or are those parallel dimensions that should compose at the `GroupAttributes` level rather than the tree level?
  - `Brand` model already exists for visual / collateral config — relate to `Portfolio(kind=BRAND)` how? Options: (a) keep separate, FK Portfolio→Brand; (b) merge; (c) leave parallel and reconcile later. Recommendation: (a) — Brand stays for theming, Portfolio(kind=BRAND) is the org / rules concept.
  - Customer-facing UX: do customers see "Wyndham — parent brand" / "Aimbridge — management company" as separate filters in the portfolio picker, or is it transparent? Probably transparent for now, opt-in surfacing later.

  ## Why now

  Three converging forces:
  - Rules-engine doc is APPROVED but practically blocked on this
  - GrowthBook targeting is increasingly load-bearing on portfolio identifiers (`base_features.py`)
  - MSA / onboarding code hard-codes identifier-string lookups every time we add a new commercial agreement — each one is a small migration we'd rather not keep writing

  ---

  ### Suggested next steps
  1. Decide: Linear ticket for this proposal, or a Notion design doc draft alongside the Rules-based config one?
  2. 30-min sync with Project Owner of the rules-config doc to resolve a real tension — I'm taking the position that typed Portfolios and `GroupAttributes` should be coupled; the Notion doc explicitly decouples them. That needs settling before either ships.

  Set `working_on: false`. Did not move the file or change body / title.
project: null
source_id: null
tags: []
time_minutes: 5
title: Sketch the product document proposing modeling "types" of Portfolios
updated: 2026-05-27 21:05:00.000000
waiting_on: null
waiting_since: null
working_on: false
---

https://www.notion.so/canarytechnologies/Rules-based-hotel-configuration-269814686151800f8812f8373d3f90e3?source=copy_link has useful context around adding type metadata to portfolios

However, not completely up to date with code