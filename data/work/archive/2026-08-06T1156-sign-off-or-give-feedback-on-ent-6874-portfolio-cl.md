---
area: null
completed_at: 2026-08-06 15:00:14.098298
contexts:
- react
created: 2026-08-06 11:56:55.285600
defer_until: null
due: null
energy: medium
id: 2026-08-06T1156-sign-off-or-give-feedback-on-ent-6874-portfolio-cl
order: null
output: |
  ## Agent run 2026-08-06T10:49:38Z

  **Bottom line: don't sign off yet — give feedback.** The *command* is good (additive,
  dry-run default, 12 tests, enum-coverage test). The *classification* has one decision
  that will produce 400 invariant violations in US prod alone, and two semantic problems
  worth settling before ENT-6875/6878 build on top of it. None of it blocks running the
  backfill (it's additive and reversible via admin), but it should be answered before
  Andrea treats the current mapping as signed off.

  ### What I actually reviewed

  I could **not** open Andrea's spreadsheet — Google Drive isn't authenticated in this
  session (`/mcp` → "claude.ai Google Drive" would fix it). So instead I reviewed the
  source of the results:

  - The `TYPES_BY_IDENTIFIER` mapping in PR #52058
    (https://github.com/canary-technologies-corp/canary/pull/52058) — all 58 identifiers.
  - The rule matrix in the design doc
    (https://app.notion.com/p/canarytechnologies/Typed-Portfolios-Design-Doc-37481468615181b6b94bd569ba782491).
  - **Re-derived the classification against live US prod** via Snowflake
    (`CANARY_RAW.CANARY.HOTELS_PORTFOLIO` / `HOTELS_PORTFOLIOHOTEL`, CDC-deduped).
    **US only** — EU/AP not checked, and the `sso.Organization` tables aren't in the
    Snowflake mirror so I could not verify the `SSO_ORGANIZATION` derivation leg.

  US prod shape: 347 live portfolios. Only **64 have an identifier** — the hand-classified
  mapping is doing real work on 18% of rows. 283 (82%) have no identifier at all: 237 of
  those have an Explo token (→ `ABOVE_PROPERTY_DASHBOARD`) and 46 have neither (→ `AD_HOC`
  by fallback).

  ### 1. BLOCKER FOR ENFORCEMENT — 400 US hotels get two PARENT_BRANDs; 95% of that is one decision

  The doc's only per-hotel cardinality rule is `≤ 1 PARENT_BRAND per hotel`
  (ENT-6875 audit → ENT-6878 enforcement). Applying the mapping to US prod today:

  | PARENT_BRAND pairs on one hotel | hotels |
  | --- | --- |
  | wyndham + wyndham_deactivated | 380 |
  | drury + wyndham | 8 |
  | marriott + wyndham | 3 |
  | marriott + marriott_demo | 2 |
  | IHG + ihg_demo, BW + IHG, IHG + marriott, BW + wyndham, ESA + wyndham, IHG + drury, marriott + proper | 1 each |
  | **total** | **400** |

  **383 of the 400 are lifecycle artefacts** (`*_deactivated`, `*_demo`) — created directly
  by the PR's policy that "staging/deactivated/demo variants keep their production
  counterpart's structural type." I think that policy is *right in principle* (lifecycle
  belongs on the future `visibility` axis, as the doc says), but it means the cardinality
  invariant is unenforceable until `visibility` lands. Pick one and write it down now:
  either (a) the audit/enforcement excludes lifecycle variants, or (b) lifecycle variants
  get `AD_HOC` instead of the structural type until `visibility` exists.

  The remaining ~17 (drury+wyndham, marriott+wyndham, BW+IHG…) are **genuine cross-brand
  data problems** that predate typing. That's exactly what ENT-6875 is for — good news, the
  typing found them. Worth calling out separately so they don't get lost in the 380.

  ### 2. Structural parentage: the mapping creates rows the rule matrix says are illegal

  Matrix says `BRAND`: parent must be `PARENT_BRAND`; `MSA`: parent must be `PARENT_BRAND`.
  In US prod:

  - **MSA-typed with no parent (7):** `wyndham_connect_gms` (4,880 hotels),
    `wyndham_connect_international` (4,880), `wyndham_connect_plus` (1,622),
    `wyndham_connect_digital_tipping` (0), `best_western_gms` (1,311),
    `best_western_international_gms` (1,311), `wyndham_seapr` (0).
    Only `wyndham_emea`, `wyndham_latam`, `ihg_poc` actually have parents.
  - **BRAND-typed with no parent (2):** `MVW` (56 hotels), `crown` (1 hotel).
    The three IHG sub-brands correctly parent to `IHG`.
  - **`PARENT_BRAND` + `MSA` on the same row is self-contradictory** as the matrix is
    currently worded: `PARENT_BRAND` = "no parent (is a root)", `MSA` = "parent must be
    `PARENT_BRAND`". The mapping puts both on `wyndham`, `BW` and their four
    staging/deactivated variants. Needs the matrix to state parentage rules
    **conditionally** ("*if* a parent is set, it must be…"), or enforcement breaks the two
    largest brands.

  Ask: is the fix to relax the matrix wording, or to actually set `parent` on the six
  Connect/GMS portfolios? The latter is a real data change and out of scope for an
  additive backfill — so it needs its own ticket.

  ### 3. `MSA` the type ≠ `MSA_PORTFOLIO_IDENTIFIERS` the frozenset

  `backend/canary/onboarding/services/master_service_agreement.py:8` — today
  `MSA_PORTFOLIO_IDENTIFIERS` is **only `{BEST_WESTERN, WYNDHAM}`**, and it is paired with
  `MSA_PRODUCTS` (a per-identifier product-exclusion list), guarded by an assert that every
  MSA identifier has a products entry.

  The new `MSA` type covers 16 identifiers. So `has_type(MSA)` is **not a drop-in
  replacement** for that frozenset — swapping it in during the call-site migration would
  make `exclude_msa_products_for_hotel` match hotels in `wyndham_connect_plus`,
  `wyndham_seapr`, `ihg_poc` etc., which have no `MSA_PRODUCTS` entry, and silently exclude
  nothing. Two different concepts share the word "MSA": *"is under a commercial agreement"*
  vs *"is under an agreement whose bundle changes what we activate"*. The doc already
  anticipates the answer (per-assignment `MSA` metadata) — worth noting on ENT-6874 so the
  migration ticket doesn't treat it as mechanical.

  ### 4. The `AD_HOC` fallback is asymmetric

  `is_fallback = not derived and not existing`, so `AD_HOC` only applies when *nothing at
  all* was derived. Consequence in US prod: 237 identifier-less portfolios get
  `{ABOVE_PROPERTY_DASHBOARD}` and 46 otherwise-identical ones get `{AD_HOC}` — the same
  kind of real-world object labelled differently based on whether an Explo token happened
  to be provisioned. Suggest applying `AD_HOC` whenever no **structural** type is derived,
  not when nothing is derived. Then `AD_HOC` consistently means "no structural role" and
  those 283 rows are uniform.

  ### 5. Free-form identifiers are already in prod and the enum-keyed dict can't see them

  ENT-6604 made `identifier` free-form; US prod already has 6 values outside the enum:
  `Noble House Portfolio` (16 hotels), `Radius Hospitality Portfolio` (12),
  `FriendWell Portfolio` (5), `dnc-uat` (2), `palette_hotels` (1),
  `Hotel Natalya Portfolio` (1).

  Noble House and Radius are real management companies — they'll come out as
  `ABOVE_PROPERTY_DASHBOARD` or `AD_HOC`, never `MANAGEMENT_COMPANY`. Not a bug in the
  command, but it means the dict has a permanent blind spot. Suggest an explicit
  `unmapped_identifier` CSV column / warning so these stay visible rather than blending
  into the identifier-less rows. (Aside: those first four contain spaces, which
  `Portfolio.clean()`'s `_IDENTIFIER_PATTERN` now rejects — pre-existing rows that would
  fail validation today.)

  ### 6. Two classifications I'd push back on individually

  - **`MVW` → `BRAND`.** Marriott Vacations Worldwide is a separate listed company that
    licenses the brand, and its portfolio has no parent link to `marriott`. Standalone
    company → `PARENT_BRAND` by the PR's own stated policy.
  - **`crown` → `BRAND`.** The row is literally named "Crown Resorts Portfolio (UAT)" with
    1 hotel. Typing a UAT portfolio as a Canary-controlled structural `BRAND` looks wrong;
    `AD_HOC` fits better.

  ### 7. Question, not an objection

  `Portfolio.primary_sso_organization` (`hotels/models/portfolio.py:210`) is a second
  SSO-shaped relationship the derivation doesn't consider — only
  `Organization.join_users_to_portfolio` is used. Different semantics (it assigns an SSO org
  to *newly created* APD users), so excluding it is probably right, but ENT-6884's drift
  detection will need to know it exists. 3 US portfolios have it set.

  ### Suggested reply to Andrea (NOT SENT — needs Gareth to write/approve)

  Per the repo's human-authored-communication rule I have not posted anything to Linear or
  GitHub. The above is raw material; the Linear comment needs to be in Gareth's own words.

  Highest-value things to raise, in order: (1) the 400-hotel `PARENT_BRAND` collision and
  what to do about lifecycle variants; (2) conditional wording for the parentage rules;
  (3) the `MSA` frozenset semantic collision.

  ### Not done / not verified

  - Spreadsheet not opened (no Google auth) — my numbers are re-derived, not reconciled
    against Andrea's output. Worth a diff once the sheet is readable.
  - **EU and AP regions not checked at all.** Both need the same three queries before the
    `--commit` run.
  - `SSO_ORGANIZATION` derivation unverified (sso tables absent from the Snowflake mirror).
  - Did not run the PR's tests locally.

  ## Agent run 2026-08-06T11:33:00Z — the four derivation rules checked against the code

  Gareth's steer: *"explo token presence is not a good conditional. Creating a portfolio via
  portfolio service always creates an explo token."* Confirmed in code, and it's worse than
  a weak signal — it's a creation side-effect. Rule by rule:

  ### Rule 1 — `TYPES_BY_IDENTIFIER` via `parse_identifier` — SOUND

  `Portfolio.parse_identifier` (`hotels/models/portfolio.py:241`) coerces to an enum member
  and returns `None` for null/unrecognised values, failing safe as intended. The dict covers
  all 58 members and a test asserts it. The MSA_* block is uniformly `MSA`; the ten
  management companies (Aimbridge, Crestline, Crestline Payroll, Pyramid, Stonebridge,
  Buffalo, Raymond, Northland, IMM, PHG) are uniformly `MANAGEMENT_COMPANY`. As advertised.

  Two small things: `derive_types` does `TYPES_BY_IDENTIFIER[identifier]` (direct subscript),
  so adding an `Identifier` member without updating the dict is a runtime `KeyError` — CI
  catches it, but `.get(identifier, frozenset())` is free insurance. And the free-form
  blind spot from run 1 stands (6 unmapped identifiers in US prod).

  ### Rule 2 — `explo_customer_token` → `ABOVE_PROPERTY_DASHBOARD` — BROKEN, drop it

  Three writers of `Portfolio.explo_customer_token`; only one carries intent:

  1. **`PortfolioService.create_portfolio`** (`portfolios/services/portfolio.py:243-246`):
     `if is_production(): ... portfolio.explo_customer_token = response.token` — unconditional.
     **Every portfolio created through the service in prod gets a token**, whatever it's for.
  2. **`backfill_explo_customer_tokens --all --commit`**
     (`portfolios/management/commands/backfill_explo_customer_tokens.py`) iterates
     `Portfolio.objects.all()` and mints a token for every portfolio in the DB.
  3. `AbovePropertyDashboardService._setup_explo_token_for_portfolio`
     (`portfolios/services/above_property_dashboard.py:84`) — the only intent-bearing writer,
     and the one the ticket cites as "the load-bearing APD predicate". It is load-bearing for
     *reading* a dashboard; it is not the only thing that *sets* the field.

  So the predicate actually reads "was created via `PortfolioService` in prod, or swept by
  the backfill" — not "is an above-property dashboard". US prod bears this out:

  | | US prod |
  | --- | --- |
  | live portfolios | 347 |
  | has `explo_customer_token` | 277 (80%) |
  | created since 2025-01-01 | 329 |
  | has any `override_explo_*_dashboard_id` | **15** |
  | token but **zero** PortfolioUsers and **zero** role grants | **19** (provable false positives) |

  The converse matters too: 299 portfolios have a portfolio user or a role grant, so "has
  users who could reach the dashboard" isn't discriminating either — most US portfolios
  genuinely *are* above-property dashboards. So the label isn't mostly wrong; the problem is
  that **the rule isn't measuring anything**. It returns ~80% true regardless of the facts.

  The design doc's own justification for *declaring* `ABOVE_PROPERTY_DASHBOARD` rather than
  deriving it is *"intent before wiring — you can mark a portfolio `ABOVE_PROPERTY_DASHBOARD`
  at setup time, before the Explo token is provisioned."* Deriving it from a token minted
  automatically at creation inverts exactly that argument.

  Also: the `is_production()` gate means **staging portfolios never get a token on
  creation**, so a dry run reviewed against staging shows a completely different APD
  distribution than prod. That undercuts "review the dry-run output per region" as a check
  on this rule specifically.

  **Recommendation:** drop rule 2 from the backfill. `ABOVE_PROPERTY_DASHBOARD` should be
  declared, not inferred — ENT-6880 auto-assigns it at the Explo provisioning wiring point
  going forward, and admin (ENT-6886) covers the rest. If a seed label is wanted, use
  `override_explo_*_dashboard_id IS NOT NULL` (15 US rows — genuinely configured dashboards)
  as a conservative starting point rather than the token.

  ### Rule 3 — inbound `Organization.join_users_to_portfolio` → `SSO_ORGANIZATION` — SOUND

  `sso/models/organization.py:242` — nullable FK, help text "If set, all users will be joined
  to this portfolio by creating PortfolioManagedUser instances". That is precisely the doc's
  `SSO_ORGANIZATION` meaning, and `Organization` has no soft-delete or `is_active` field, so
  the bare `Exists(...)` annotation needs no extra filter. Correct as written. (Still
  unverified against prod data — the sso tables aren't in the Snowflake mirror.)

  ### Rule 4 — `AD_HOC` when nothing derived — collateral damage from rule 2

  `is_fallback = not derived and not existing`. Because rule 2 fires for ~80% of portfolios,
  the `AD_HOC` fallback is suppressed almost everywhere it should apply: only **46** US
  portfolios get it, when ~283 have no identifier and no structural role at all. The
  portfolios most deserving of `AD_HOC` are exactly the ones a stray creation-time token
  disqualifies.

  This sharpens finding 4 from the first run — the asymmetry was real, and now the mechanism
  is known. Fix both together: drop rule 2, and make the fallback fire when **no structural
  type** is derived rather than when nothing at all is derived. Then `AD_HOC` consistently
  means "no structural role", and it lands on the ~283 rows that actually have none.

  ### Net effect on the sign-off

  Rules 1 and 3 are fine. Rule 2 should come out; rule 4 should be rewritten in terms of
  structural types. That changes the classification materially — the spreadsheet Andrea
  circulated would need regenerating before it means much, which is a second independent
  reason not to sign off on the current output.
project: 2026-04-16T1210-unblock-team
source_id: https://linear.app/canary-technologies/issue/ENT-6874/classify-existing-portfolios-and-backfill-type-assignments-additive
tags:
- morning-gtd
- linear
time_minutes: 30
title: Sign off or give feedback on ENT-6874 portfolio classification results
updated: 2026-08-06 15:00:14.098287
waiting_on: null
waiting_since: null
working_on: false
---

Andrea @mentioned me and Connor: "current logic results ... Please provide feedback or sign off." Spreadsheet of classified portfolios from the additive-only backfill command.
https://linear.app/canary-technologies/issue/ENT-6874/classify-existing-portfolios-and-backfill-type-assignments-additive