---
area: null
contexts:
- craft
created: 2026-05-27 15:49:39.043474
defer_until: null
due: 2026-05-28
energy: medium
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

  ## Agent run 2026-06-03T12:04Z

  Re-ran to verify the prior sketch against *current* code (the task notes the Notion doc is stale vs. code). Every structural claim in the prior run still holds. Two corrections + one substantial strengthening of the evidence base below. The sketch is sound and ready to promote; the change is that the "Why now" argument is now backed by a concrete inventory rather than a hand-wave.

  ### Corrections / drift since the prior run

  - **Portfolio has moved to its own app.** The *model* is still `hotels/models/portfolio.py` (unchanged — confirmed the 50-value `Identifier` enum, `parent` self-FK, `PUBLIC_/DISCOVERABLE_PORTFOLIO_IDENTIFIERS` frozensets, and the `identifier`-unique constraint). But `PortfolioService` now lives at `backend/canary/portfolios/services/portfolio.py`, not under `hotels/`. Any migration plan should target the `portfolios` app.
  - **The one-level parent cap is real and explicit** — `PortfolioService.add_hotels()` (`portfolios/services/portfolio.py:387-394`) raises `BadRequest("Cannot auto-add hotels: multi-level portfolio hierarchies are not supported.")` when `portfolio.parent.parent_id is not None`. This is the hard ceiling the sketch claims: you cannot model "Aimbridge manages Super 8s which are a sub-brand of Wyndham" in the tree today. `create_portfolio()` (`:184-239`) validates `identifier` via `full_clean()` but does **no** validation on `parent` kind/shape — exactly the gap the type-driven invariants would fill.
  - **GrowthBook attribute name confirmed**: `_get_portfolio_attributes()` (`feature_flags/utils/base_features.py:144-147`) emits `{"portfolio_identifier": portfolio.identifier}` and only for non-null identifiers. So targeting is keyed on the raw string, and NULL-identifier portfolios (internal/demo) are silently untargetable — another argument for a `kind` that distinguishes `INTERNAL` explicitly rather than leaning on a NULL identifier.
  - **Brand model is unrelated to Portfolio** (`hotels/models/brand.py`): `Hotel.brand` is a direct FK; Brand holds theming/collateral (`image`, `parent_name`, `external_brand_code`, `features_config_uuid`, `default_collateral_config_uuid`). There is **no** FK between Brand and Portfolio. This confirms open-question recommendation (a): keep Brand for theming, `Portfolio(kind=BRAND)` is the org/rules concept, reconcile later. They're genuinely orthogonal today.

  ### The strongest evidence for typing: the identifier-string grouping sprawl

  The prior run asserted "MSA / onboarding code hard-codes identifier-string lookups every time." That's now quantified. There are **at least 8 separate in-code structures** that re-derive a *type* from `identifier`, plus **~20+ call sites** that string-match identifiers. Each one is a `kind` field waiting to be born:

  | In-code structure | Location | What "type" it's faking |
  | --- | --- | --- |
  | `PUBLIC_PORTFOLIO_IDENTIFIERS` | `portfolio.py:77` | visibility + GrowthBook-targetable |
  | `DISCOVERABLE_PORTFOLIO_IDENTIFIERS` | `portfolio.py:100` | guest-API discoverability |
  | `MSA_PORTFOLIO_IDENTIFIERS` | `onboarding/.../master_service_agreement.py:8` | MSA membership — **but contains `BW`/`WYNDHAM` (parent brands), not the `wyndham_connect_*` MSA rows**, which is itself the conceptual muddle this proposal fixes |
  | `ENTERPRISE_PORTFOLIO_IDENTIFIERS` | `_variant_migration_helpers.py:25` | "is an enterprise parent" (8 IHG/Wyndham/BW entries) |
  | `GROUP_USE_CASES_BY_PORTFOLIO_IDENTIFIER` | `use_case.py:107` | parent-brand → guest-journey use-cases (BW/WYNDHAM/IHG) |
  | `ADDON_USE_CASES_BY_PORTFOLIO_IDENTIFIER` | `use_case.py:163` | parent-brand → addon use-cases (same three) |
  | `ENTERPRISE_DEPLOYMENTS_TO_PORTFOLIO_IDENTIFIER` | `salesforce_onboarding_fields.py:60` | Salesforce deployment enum → MSA identifier |
  | `PORTFOLIO_TO_LOYALTY_PROGRAM_IDENTIFIER_MAP` | `membership_level_new.py:371` | portfolio → loyalty program priority |

  ~20+ `hotel_belongs_to_portfolio_by_identifier(...)` / dict-lookup call sites span onboarding (deactivate-hotel providers for Wyndham, BW, IHG, Wyndham Connect Plus; SSO user merge; onboarding batch) and guest-journey (`group_use_case_service.py`). Every new commercial agreement or brand today means editing several of these by hand.

  **This is the headline finding.** The proposal isn't speculative architecture — it's *consolidating eight ad-hoc reinventions of `Portfolio.kind` that already exist in the codebase* into one typed field. That reframes the pitch from "add a nice abstraction" to "stop maintaining eight parallel hard-coded taxonomies." Note also that `MSA_PORTFOLIO_IDENTIFIERS` lumping parent-brand identifiers in with "MSA" is concrete proof the current flat enum can't tell a parent brand from a commercial agreement — the exact distinction `kind` introduces.

  ### One refinement to the taxonomy

  Given `PUBLIC_PORTFOLIO_IDENTIFIERS` mixes parent brands (`WYNDHAM`, `IHG`, `BEST_WESTERN`) with MSAs (`wyndham_connect_*`, `best_western_*`gms) and a messaging-only variant, **visibility is orthogonal to kind** and should be its own field, not derived from kind. Recommend `Portfolio.kind` (enum) **and** `Portfolio.visibility` (enum: `INTERNAL` / `PUBLIC` / `DISCOVERABLE`) as two independent columns — the prior sketch implied `INTERNAL` was a kind, but the data shows a public MSA and an internal MSA are both conceivable. Keep `kind` for the org-tree role; keep `visibility` for who-can-see. This also lets `PUBLIC_/DISCOVERABLE_PORTFOLIO_IDENTIFIERS` frozensets retire cleanly into a column rather than being folded into `kind`.

  ### Updated migration note

  Step 4 of the prior migration (invariant checks) should land in `portfolios/services/portfolio.py` (`create_portfolio` + `add_hotels`), and is the natural home to *also* relax the one-level cap once `kind` lets us express legitimate multi-level shapes (brand-under-parent + management-company cross-cut). The cap exists today precisely because untyped multi-level trees are unsafe; typing them is what makes lifting the cap safe.

  ### Suggested next steps (unchanged + one)
  1. Promote to a Notion design doc or Linear ticket (still open — user's call).
  2. 30-min sync with the rules-config doc owner on the coupling question (still the key unresolved tension).
  3. **New:** lead the pitch with the 8-structure inventory above — it's the most persuasive, least-speculative framing and it's now verified against live code.

  Set `working_on: false`. Did not move the file or change body / title.

  ## Agent run 2026-06-03T12:13Z

  User gave direction that changes the shape of the design. Two of the earlier runs' assumptions were wrong and are corrected here. This section is the current best version of the sketch and **supersedes the single-`kind` enum** proposed in the 2026-05-27 and 2026-06-03T12:04 runs (those stay above for history). Key changes:

  - **Identifiers are explicitly out of scope.** They are orthogonal to types and we are NOT redesigning them. An identifier is a deliberate (if clunky) device: a stable logical handle that lets code refer to e.g. "the Wyndham portfolio" consistently even though that portfolio is physically a different row across separate regional servers/databases. It maps a logical business unit to code. That's a useful property worth keeping. The earlier runs over-indexed on identifier mechanics; drop that framing.
  - **Types must be multi-valued.** Hard requirement from the user: a single portfolio can serve *several* purposes at once — e.g. it is the Wyndham parent-brand portfolio *and* an SSO organization's enrollment target. A single-valued `kind` column cannot express this. The model must let a portfolio hold a *set* of types.

  ---

  # Typed Portfolios — sketch (v2)

  ## The concept today: useful but amorphous

  A `Portfolio` is "a named group of hotels (and, via roles, users)." In practice that one concept is overloaded to do many unrelated jobs at once:

  - **Brand / parent-brand grouping** — collect all Wyndham, or all Super 8, properties.
  - **MSA membership** — mark which hotels fall under a commercial agreement (Wyndham Connect GMS, BW GMS, …).
  - **Above-Property Dashboard (APD) backing** — a portfolio is the unit an Explo customer + dashboards hang off (`Portfolio.explo_customer_token`, `override_explo_*_dashboard_id`; above-property view at `hotels/views/views.py:785`; `AbovePropertyDashboardService`). APD collects many hotels *and* users into one reporting surface.
  - **SSO organization enrollment** — `sso.Organization.join_users_to_portfolio` (FK → Portfolio, `sso/models/organization.py:238`) auto-enrolls every user who SSO-logs-into that org as a `PortfolioManagedUser`.
  - **Arbitrary / ad-hoc grouping** — internal demos, regional slices, one-off customer cuts, feature-flag targeting cohorts.

  Nothing in the schema says which of these a given portfolio *is*. The purpose is inferred — from the name, from the identifier, from membership in a hard-coded frozenset, or from an analyst's memory. That's the amorphousness we want to discipline.

  ## Proposal: give portfolios explicit, multi-valued types

  Add a typed, **multi-valued** classification to `Portfolio`. A portfolio carries a *set* of types, each naming a purpose it serves. Types are first-class and drive business logic, instead of business logic guessing the purpose from string-matching.

  Candidate type set (names TBD, this is the shape not the final list):

  | type | what it means |
  | --- | --- |
  | `PARENT_BRAND` | top-level brand grouping (Wyndham, IHG, BW) |
  | `BRAND` | sub-brand grouping (Super 8, Holiday Inn Express) |
  | `MSA` | hotels under a commercial agreement |
  | `MANAGEMENT_COMPANY` | operator grouping that crosses brands |
  | `ABOVE_PROPERTY_DASHBOARD` | backs an Explo APD (cross-hotel reporting + users) |
  | `SSO_ORGANIZATION` | enrollment target for an SSO org |
  | `AD_HOC` | arbitrary customer/internal grouping with no special semantics |
  | `INTERNAL` | demo / QA / dev — excluded from production behavior |

  A real portfolio holds several of these simultaneously. The Wyndham portfolio might be `{PARENT_BRAND, ABOVE_PROPERTY_DASHBOARD, SSO_ORGANIZATION}`. A throwaway demo is just `{INTERNAL}`.

  ### Types drive business logic

  The point of typing is that each type can carry **behavioral rules** the flat concept can't express. Purely illustrative — exact rules are a design decision, not settled here:

  - **Hierarchy capability** — some types may participate in parent/child relationships, others may not. (Hypothetically: `BRAND` may have a `PARENT_BRAND` parent; an `SSO_ORGANIZATION` type confers no hierarchy at all; an `AD_HOC` portfolio cannot be a parent of a brand portfolio.) The single one-level cap in `PortfolioService.add_hotels()` (`portfolios/services/portfolio.py:387-394`) is currently a blunt global rule *because* we can't reason per-type; typing is what lets the hierarchy rule become type-aware.
  - **Membership rules** — e.g. a hotel may belong to at most one `PARENT_BRAND` portfolio, but to many `AD_HOC` ones.
  - **Composition rules** — which types may co-exist on one portfolio and which are mutually exclusive (e.g. `PARENT_BRAND` and `BRAND` probably can't both apply to the same portfolio; `SSO_ORGANIZATION` composes with anything).
  - **Lifecycle / safety** — `INTERNAL` is invisible to production rollouts, rules evaluation, and customer surfaces, regardless of what else it's tagged.

  ### Why multi-valued is non-negotiable

  Because the purposes genuinely overlap on the same row. SSO enrollment, APD backing, and brand grouping are independent reasons a portfolio exists, and one portfolio routinely satisfies more than one. Force a single type and we either duplicate portfolios (one "brand" copy, one "SSO" copy, membership drifts between them) or we're back to inferring the other purposes from somewhere else — the exact problem we're removing.

  ## Modeling options (for the design doc to decide)

  1. **Type set as a through-model** — `Portfolio` ↔ `PortfolioTypeAssignment` ↔ type. Lets a type carry type-specific attributes later (e.g. the `SSO_ORGANIZATION` assignment could reference the org; an `MSA` assignment could hold agreement metadata). Most flexible; recommended starting point.
  2. **Array/enum-set column** on `Portfolio` — simplest; fine if types stay pure tags with no per-type data. Risk: we later need per-type attributes and have to migrate to a through-model anyway.
  3. **One-axis vs two-axis** — open question below. A flat set is simplest; a two-axis split (structural role + functional purpose) is cleaner if the two never interact. Lean flat until a real rule forces the split.

  Whichever we pick, the type registry (the table of per-type rules: hierarchy-capable?, exclusive-with?, membership-cardinality, production-visible?) lives in code as the single source of business behavior, and the assignments live in the DB.

  ## What this replaces

  Today the "type" of a portfolio is already being reconstructed ad hoc, in at least eight places — hard-coded frozensets and dicts plus ~20+ `hotel_belongs_to_portfolio_by_identifier(...)` call sites across onboarding and guest-journey (inventory in the 12:04 run above). Each is a hand-maintained, single-purpose guess at a type. Typed portfolios consolidate those into one declared classification the code can query. (This is supporting evidence, not the headline — the headline is the multi-purpose discipline.)

  ## Explicitly out of scope

  - **Identifiers.** Keep as-is. Orthogonal to types; still the stable cross-region logical handle. Do not fold types into identifiers or vice versa.
  - **RBAC / PortfolioRole.** Roles keep attaching to portfolios regardless of type.
  - **The rules engine.** Typed portfolios are substrate it can read; this doc doesn't design the engine. (Coupling-vs-decoupling tension with the Notion "Rules-based hotel configuration" doc still needs settling — see prior runs.)
  - **Brand model.** `hotels/models/brand.py` stays the theming/collateral concept, FK'd from `Hotel`; unrelated to `Portfolio`. `Portfolio(type=BRAND)` is the org concept.

  ## Open questions

  - **One axis or two?** Is a flat multi-set enough, or do we want a structural axis (parent-brand/brand/MSA/management-co) distinct from a functional axis (APD/SSO/ad-hoc)? Decide based on whether any rule needs to treat them differently.
  - **Per-type attributes now or later?** If `SSO_ORGANIZATION` / `MSA` assignments will carry data, start with the through-model (option 1).
  - **Composition matrix.** Enumerate which type pairs are legal vs mutually exclusive — needs a short workshop with examples.
  - **Membership cardinality per type.** "At most one parent brand per hotel" etc. — confirm with real data before enforcing.
  - **Backfill.** How do we classify the existing ~50 portfolios into type-sets? Some are obvious (the MSA rows, the brand rows); APD/SSO membership can be derived from `explo_customer_token` presence and inbound `Organization.join_users_to_portfolio` FKs respectively — that backfill is mechanical, which is a nice argument for feasibility.

  ## Suggested next steps
  1. Promote to a Notion design doc / Linear ticket (user's call — not done).
  2. Workshop the composition matrix + per-type rules with 4-5 concrete real portfolios (Wyndham, a BW MSA, an APD-only customer cut, a pure SSO org, a demo).
  3. Resolve coupling-vs-decoupling with the rules-config doc owner.

  Set `working_on: false`. Did not move the file or change body / title.

  ## Agent run 2026-06-03T12:19Z

  Critiqued v2, then wrote the final version as a **private Notion design doc** (created with no parent → workspace-level page private to Gareth): https://app.notion.com/p/37481468615181b6b94bd569ba782491 — "Typed Portfolios — Design Doc".

  Self-critique of v2 (all fixed in the Notion doc):
  1. Deferred instead of deciding — now takes positions (flat set + two documented axes; through-model over enum-array).
  2. Conflated structural vs functional axes without resolving — resolved: one flat multi-valued set, axes are a doc/rule-authoring aid not a schema boundary.
  3. `INTERNAL` smuggled back in as a type, contradicting the earlier visibility-is-orthogonal point — removed; INTERNAL is now a separate `visibility` concern, out of scope.
  4. Never engaged the strongest objection (several purposes already derivable from inbound FKs: SSO via `join_users_to_portfolio`, APD via `explo_customer_token`) — now has a dedicated "declared types vs derived-from-relationships" section with a clear position and per-type verdict.
  5. No concrete schema — now includes `PortfolioType` + `PortfolioTypeAssignment` Django sketch with constraints + worked example (`Wyndham = {PARENT_BRAND, ABOVE_PROPERTY_DASHBOARD, SSO_ORGANIZATION}`).
  6. Composition/membership rules all hypothetical — now a draft composition+cardinality matrix to react to.
  7. Naming unsettled — recommends keeping "type" (team continuity) but stresses it's a *set*, never single-valued.

  Doc structure: TL;DR · Problem · Goals/Non-goals · Background (real uses table) · Proposal (schema, catalog, rules matrix, business-logic payoff) · the declared-vs-derived design question · Out-of-scope · Migration/rollout · Open questions · Appendix (code evidence, all file-cited).

  External write: creating the Notion page was the one outbound action — explicitly requested by the user this session ("write your final version as a private-to-me notion design doc"). Placed with no parent so it is private to the creator, not in any shared teamspace. No other external writes; not promoted to Linear, not shared with anyone.

  Set `working_on: false`. Did not move the file or change body / title.

  ## Agent run 2026-06-03T12:23Z

  Added (per user request) a callout to the Notion doc defending the **max one-level hierarchy** cap: it's a deliberate trade — "group of groups" covers the real two-tier shapes (parent brand → brands/MSAs) while avoiding the unbounded cost of arbitrary depth (recursive traversal, ambiguous ancestor resolution, cycle risk, unstatable invariants). Key argument: when more structure is needed, add *breadth not depth* — multiple types per portfolio + multiple portfolio memberships per hotel let independent dimensions compose as parallel memberships rather than deeper nesting. Placed at the end of §4 (Types drive business logic), blue callout.

  Also reconciled two lines that previously argued for *relaxing* the cap (the §4 Hierarchy bullet and migration step 6) so the doc no longer contradicts the callout: the cap **stays**; typing makes it type-*aware* (which type-pairs may nest within the single level), not deeper.

  External write: edited the existing private Notion page (same one created in the 12:19 run) — explicitly requested this session. No other external writes.

  Set `working_on: false`. Did not move the file or change body / title.
project: 2026-04-10T0840-ticket
source_id: null
tags: []
time_minutes: 15
title: Sketch the product document proposing modeling "types" of Portfolios
updated: 2026-06-03 15:23:51.335669
waiting_on: null
waiting_since: null
working_on: false
---

https://www.notion.so/canarytechnologies/Rules-based-hotel-configuration-269814686151800f8812f8373d3f90e3?source=copy_link has useful context around adding type metadata to portfolios

However, not completely up to date with code