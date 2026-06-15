---
area: null
contexts: []
created: 2026-06-10 16:59:57.293608
defer_until: null
due: null
energy: low
id: 2026-06-10T1659-i-really-need-to-do-that-above-property-templates
order: null
output: |
  ## Agent run 2026-06-15T13:05Z — Review of "Rules Browser: Above-Property UI for Rules-Based Configuration"

  Doc: https://app.notion.com/p/canarytechnologies/Rules-Browser-Above-Property-UI-for-Rules-Based-Configuration-37c81468615181be923cec1df122e5fd
  (Design Doc DB → Projects; Status WIP; Team Enterprise; Product: Above Property Dashboard + Portfolios)

  Verified the load-bearing technical claims against the codebase on the current branch (two Explore sub-agents). Verdict: **solid design, ready to ticket with two corrections and a handful of nits.** The architecture is right — server-side resolution via the single engine, read-only, curated allowlist, what-if-only. The provenance and 422-ambiguity reasoning is genuinely well-grounded, not hand-wavy.

  ### Two things that are wrong in the doc (fix before handing to an implementer)
  1. **"Request Framework v2" vs the cited example contradict each other.** The doc says to build the endpoints in "Request Framework v2 ... following patterns in `portfolios/views/portfolio.py`." But `portfolios/views/portfolio.py` actually uses the OLDER `@load_schema` / `RequestSchema` pattern, not RF v2 (`@validate_request`). An implementer who copies portfolio.py will NOT be writing RF v2. Decide which you actually want — if RF v2, point to a real RF v2 view as the reference (the `backend:write-api-view` skill is RF v2) and don't cite portfolio.py; if you want consistency with the rest of `portfolios/`, drop the "v2" claim. Right now they conflict.
  2. **Two named frontend anchors don't exist on the current branch.** The doc references `AbovePropertySidebar.vue` and the `useCurrentUserPortfolioPermissions()` composable by name as if they're established. Neither was found on the current branch (the `AboveProperty/` dir does exist). They may live only on the spike branch or the names may be approximate. Before ticketing the frontend milestone, confirm the real sidebar component + the real portfolio-permission composable name so the tickets point at files that exist.

  ### Verified TRUE (the design rests on these and they hold)
  - Engine shape is exactly as described: `GroupAttributes` (frozen, all 8 fields), `ConfigSpec` (key/OverridePolicy FINAL|FREE/value + ANY_NON_NULL sentinel), `ConformityDiamondTree` (networkx DAG, edges carry default_weight + per-setting settings_weights), `ConformityService` with `get_all_setting_values_for_hotel_attributes`, `finalize()`, `_ROOTS`. (`services/conformity.py`)
  - **Provenance is a genuinely cheap pure addition.** Confirmed: resolution already computes a per-key `winner` and then *discards* it (conformity.py ~line 371/400). `explain_resolution` just surfaces what's already computed — low risk, no behaviour change. Good call.
  - `GroupAttributes.matches_hotel` exists and checks each non-null attribute independently → the per-criterion `match_breakdown` is directly derivable. (conformity.py:136-164)
  - `admin._format_value` helper and `tree_viewer.html` exist and are reusable; `checks.py` exists with a registered system check that can be extended. `generate_setting_types` management command exists. All three tree configs (wyndham/best_western/ihg_pilot) exist and are loaded via explicit import + `autodiscover_modules`.
  - Portfolio permission system is real and distinct from the hotel-level `Permission` enum. Most-recent precedent to copy: `PORTFOLIO_HAS_VOICE_TRANSCRIPT_ACCESS` / `PORTFOLIO_HAS_VOICE_RECORDING_ACCESS` (PortfolioPermissionGrant + PortfolioRole; frontend mirror exists and is kept in sync). Frontend `ResourceBuilder + createQuery()` API-module pattern confirmed.

  ### The 422 / ambiguity argument is the strongest part — and confirms a real gap
  Confirmed: `break_tie` raises `InvalidConformityTreeError` on equal sibling weights, and `finalize()` does NOT exhaustively prove tie-breakability for every attribute combination (it validates DAG structure, single root, sibling non-override, FINAL chains — but ties are only resolved at query time). So the simulator genuinely can construct combinations no real hotel has and trip an ambiguity. The "return structured 422, never 500, log at warning as a latent tree bug" handling is correct and important. **Strongly endorse the suggested CI sweep** (resolve every combination in the simulator-dimension space per release) — that turns the simulator into a tree-correctness fuzzer, which is arguably more valuable than the customer feature itself. Consider pulling that from "Testing" up into a Milestone-1 deliverable.

  ### Smaller concerns / suggestions
  - **Migration step is unstated.** Adding a `PortfolioPermission` value means a migration on the `granted_permission` CharField choices (that's how the voice perms shipped). Milestone 2 should call this out explicitly so it isn't missed.
  - **Allowlist is the real risk surface, not the engine.** The whole "safe for customer eyes" guarantee rests on the `SettingDisplay` registry being correct. The system check enforces *that registered keys exist*, but nothing enforces *that a sensitive key wasn't registered*. The key-by-key PM sign-off (Open Decision #1) is therefore load-bearing, and the test "assert a known non-allowlisted key never appears in any response" is good but only catches one key. Suggest: maintain an explicit *denylist* of known-sensitive prefixes (`integration_secret_*`, `payment_gateway_*`, `rollout_*`) that the system check hard-fails on if ever registered — defence in depth beyond reviewer diligence.
  - **Caching nuance.** "Static per deploy → cacheable" is right for the `tree` endpoint. But `Cache-Control: private, max-age=3600` keyed by portfolio while the underlying tree is keyed by *brand* means N cache entries for identical content and a 1h window where a hotfix-deployed tree change is stale. Minor; client query cache is probably enough — consider just dropping the explicit max-age and relying on the query cache as the doc already hedges.
  - **`simulator_dimensions` "other country" option** is a nice touch (country-in-no-group must still resolve). Make sure the resolve endpoint's enum validation actually permits a country value that appears in no group — easy to accidentally reject it if validating against "countries present in the tree."
  - **Compare-on-client** (two resolve calls, diff client-side) is fine since it's presentation, not resolution — consistent with the "frontend never resolves" principle. No objection.
  - **Naming → "Locked/Adjustable" and "takes precedence over"** mapping for FINAL/FREE and weights is the right hotelier-facing call; keeping raw FINAL/FREE in the API contract and mapping in one frontend helper is clean.

  ### Open decisions — my recommendations
  - #1 (allowlist ownership): agree with eng-proposes / PM-approves, plus the denylist guard above.
  - #2 (default grant): agree — manual per-portfolio, Wyndham pilot first. Don't backfill into existing enterprise-admin roles for v1.
  - #3 (DAG in v1): keep in v1; it's the highest-signal part of the UX and the spike adapts cheaply. Reasonable to cut to fast-follow only if Milestone 3 slips.

  ### Bottom line
  Approve the direction. Before ticketing: (1) resolve the RF-v2-vs-portfolio.py contradiction, (2) confirm the real frontend sidebar component + permission composable names, (3) add the migration step to Milestone 2 and consider promoting the CI combination-sweep to Milestone 1. No architectural objections.

  Not done (out of scope for a 5-min review, flag if you want it): I did not read the spike branch `gareth-lloyd/rules-browse-proto-v1` diff or the related PRD/engine design docs in depth — happy to if you want the allowlist corpus (`SETTING_LABELS`) reviewed key-by-key for customer-suitability, which is the one piece of real homework this design defers.
project: null
source_id: null
tags: []
time_minutes: 5
title: Review this above property dashboard rules based configuration proposal
updated: 2026-06-15 13:05:00.000000
waiting_on: null
waiting_since: null
working_on: false
---

https://app.notion.com/p/canarytechnologies/Rules-Browser-Above-Property-UI-for-Rules-Based-Configuration-37c81468615181be923cec1df122e5fd

Review