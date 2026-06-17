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

  ## Agent run 2026-06-15T12:07Z — Closed the two open items from the first run

  Re-launched to finish the homework the first run deferred. Resolved both flagged uncertainties against the current branch (two Explore sub-agents). Net: **correction #2 was a false alarm — retract it; the allowlist concern is now backed by concrete numbers and is the real work.**

  ### RETRACT correction #2 — both frontend anchors DO exist on the current branch
  The first run said `AbovePropertySidebar.vue` and `useCurrentUserPortfolioPermissions()` weren't found. They are both present (the first run's sub-agent just missed them):
  - `AbovePropertySidebar.vue` → `frontend/hotels/src/components/AbovePropertySidebar.vue` (fixed 175px left sidebar, theme `#375492`; already renders Integrations / Analytics / Calls / Users & Portfolios sections, gated by portfolio perms). Last modified Jun 3–5 2026.
  - `useCurrentUserPortfolioPermissions()` → `frontend/packages/shared/api/permissions/Portfolio.ts:16` (a `createQueryList`, scoped/param'd by `portfolioUuid`, returns `PortfolioPermission[]`). The sidebar already consumes it (lines 51–62).
  - So the doc's named anchors are accurate. The frontend milestone can ticket against real files. **Only correction #1 (RF-v2 vs portfolio.py contradiction) still stands.**
  - Bonus: the `PortfolioPermission` enum already has 13 values incl. `PORTFOLIO_HAS_ANALYTICS_ACCESS`, `PORTFOLIO_HAS_PROPERTY_MANAGEMENT_SYSTEM_INTEGRATION_ACCESS`, `PORTFOLIO_HAS_PAYMENT_GATEWAY_INTEGRATION_ACCESS`, `PORTFOLIO_HAS_SSO_DIAGNOSTIC_ACCESS` etc. (`frontend/packages/shared/schemas/permissions/PortfolioPermission.ts`). A new `PORTFOLIO_HAS_RULES_BROWSER_ACCESS`-style value slots straight into this established pattern.

  ### The allowlist homework — done, and it confirms this is the #1 risk surface
  `SettingDisplay` / `SETTING_LABELS` **does not exist yet** — entirely net-new, as the doc implies. The sizing matters a lot for the safety story:
  - The engine manages **~391 setting keys**, auto-generated by the `generate_setting_types` command introspecting 5 models (Hotel, check_in/check_out Configuration, AuthorizationConfiguration, MembershipGatewayConfiguration). Full enumerated list lives in `rules_based_configuration/services/conformity.pyi` (Literal aliases, lines ~20–479).
  - **A first pass flags ~45 of those 391 as clearly NOT customer-safe.** Concrete examples (this is the corpus the PM sign-off in Open Decision #1 must catch):
    - Secrets/API keys: `hotel.integration_secret_key`, `hotel.guest_insights_secret_key`, `hotel.stb_eva_api_key`/`_api_secret`/`_private_key`, `hotel.twilio_sub_account_token`, `hotel.zingle_password`, `hotel.explo_customer_token`, `hotel.pacs_gateway_account_sid`.
    - Payment/PCI: `hotel.payment_gateway_name`, `*.payment_gateway_config_id` (auth + check_in), `hotel.check_in_configuration.is_tokenizing_with_hotel_payment_gateway`, `...override_payment_gateway_to_post_raw_credit_card_to_pms`, `hotel.can_view_card_tokens_only`.
    - Webhook creds: `hotel.check_in_configuration.notification_webhook_auth_credentials`.
    - ~17 internal `rollout_*` flags (e.g. `rollout_new_messaging_ui`, `rollout_whatsapp_integration`, `rollout_hardcoded_gj_segments_*`) + demo/mock flags (`has_mobile_key_demo`, `has_mock_pms_gateway`) — operational/competitive leakage, not secrets, but still not for customer eyes.
  - **This is exactly why my first-run denylist suggestion is load-bearing, not optional.** A ~391-key surface where ~45 are dangerous and the registry is hand-maintained is precisely the case where "reviewer diligence + one negative test" is too thin. Recommend: (a) explicit allowlist, never auto-derived from all keys; (b) a hard-failing system check on a denylist of sensitive prefixes (`integration_secret*`, `*payment_gateway*`, `*_token`, `*_secret*`, `*password*`, `*webhook_auth*`, `rollout_*`, `has_mock_*`, `*_demo`) so a future engineer can't register one by accident; (c) the system check should fire at startup like the existing `checks.py` checks.

  ### Updated bottom line
  Approve the direction (unchanged). Pre-ticketing list shrinks to: **(1) resolve the RF-v2-vs-portfolio.py contradiction** (still real); (2) ~~confirm frontend anchors~~ — done, they exist, ticket freely; (3) add the `PortfolioPermission` choices migration to Milestone 2; (4) promote the CI combination-sweep to Milestone 1; **(5) NEW — treat the allowlist as the primary safety deliverable: explicit registry + denylist system check, with the ~45-key sensitive set above as the known-bad baseline for PM sign-off.** Spike-branch diff (`gareth-lloyd/rules-browse-proto-v1`) still not read — say the word if you want it.

  ## Agent run 2026-06-16 — Applied allowlist-section rewrite to the Notion doc (user-approved)

  User agreed the allowlist section needed significant alteration given the ~45-unsafe-key finding. With explicit approval, edited the Notion doc in four places:
  1. **§1 `SettingDisplay` bullet** rewritten — now states the allowlist is the single safety boundary, cites ~391 total keys / ~45 categorically unsafe (secrets, payment/PCI, webhook creds, rollout/mock/demo flags), and requires key-by-key review against that known-bad set.
  2. **New `DENYLISTED_SETTING_PREFIXES` bullet** added — defence-in-depth guard independent of the allowlist; explicit sensitive-prefix denylist that hard-fails the system check if any allowlisted key matches, so the allow-only model can't fail open.
  3. **System-checks bullet** augmented — added the denylist-match hard-fail.
  4. **Testing API bullet** + **Open Decision #1 default** updated to reference the denylist backstop.

  Core argument that drove it: the original system check only enforced that registered keys *exist*, not that sensitive keys *weren't* registered — an allow-only model one careless `SettingDisplay(...)` away from leaking a secret. The denylist closes that.

  ## Agent run 2026-06-16 (round 2) — Second adversarial pass against the codebase

  Re-reviewed the *current* doc top-to-bottom and hard-verified its load-bearing claims against `master`/branch code (read `conformity.py` resolution walk + `break_tie`/`get_override_weight`, `hotel_attributes.py`, `generate_setting_types.py` + `setting_type_generator.py`; two Explore sub-agents on the portfolio view pattern and `_ROOTS`/portfolio-brand relationship). Net: **the engine-facing claims hold up, including the provenance algorithm. But one prior correction is still unfixed in the doc, and there are two real design gaps and three precision traps an implementer would hit.** Ordered by severity.

  ### A. STILL UNFIXED — RF-v2 vs `portfolio.py` contradiction (this is original correction #1, never resolved)
  §3 still reads: "Request Framework v2 — follow the `backend:write-api-view` conventions and the patterns in `portfolios/views/portfolio.py`." Confirmed `portfolios/views/portfolio.py` uses the **legacy** `@load_schema` / `RequestSchema` pattern (`from canary.schema import RequestSchema, load_schema`; `shared.request_validation`). `backend/canary/CLAUDE.md` is explicit: new views MUST use Request Framework (`shared.request_framework`, `@validate_request` + class gatekeeper), the two decorators "are different functions and can't be mixed in one file," and `docs/django/request-validation.md` labels `validate_request` the legacy path. So the doc tells the implementer to write RF v2 **and** copy a legacy view — contradictory, and literally un-mixable in one file. Fix: keep "RF v2", cite a real RF-v2 reference (e.g. `billing/views/billing_contact.py`, also `video/views/rooms.py`, `email_conversations/views/api_email_conversations.py`) and **delete the `portfolio.py` citation**.

  ### B. NEW (substantive) — "a portfolio maps to a tree" is undefined for multi-brand portfolios
  There is **no constraint** that a portfolio's hotels share a `parent_brand_id` (`Portfolio.hotels` is a plain M2M through `PortfolioHotel`; only uniqueness on `(portfolio, hotel)`). A management-company portfolio can hold Wyndham + IHG + BW properties. §3 "Tree selection: a portfolio maps to a tree via its hotels' `parent_brand_id`" is silent on this. The doc must define behavior: derive the distinct set of `parent_brand_id`s among the portfolio's hotels that have a registered tree → 0 ⇒ hide section; exactly 1 ⇒ show it; **>1 ⇒ decide** (let the user pick which brand's tree — best; or 404; or a "primary brand"). As written an implementer silently picks whatever the first hotel yields.

  ### C. NEW (substantive) — `_ROOTS` is keyed by `GroupAttributes`, and the Best Western root gates on MSA, not brand alone
  `ConformityService._ROOTS: Mapping[GroupAttributes, ConformityDiamondTree]`; lookup iterates roots and calls `root.matches_hotel()`. Wyndham/IHG roots are keyed by `parent_brand_id` only, but the **BW root is `GroupAttributes(parent_brand_id=BEST_WESTERN, msa=BEST_WESTERN_GMS, live_msa=BEST_WESTERN_GMS)`**. Consequence the doc's simulator section gets wrong: it claims "an 'other country' option (a country in no group's list must still resolve, hitting only country-agnostic groups)." True for Wyndham/IHG; **false for BW** — any simulated combo lacking `msa=GMS`/`live_msa=GMS` fails `root.matches_hotel` → `matched_groups: []` regardless of country. So for MSA-gated roots, `simulator_dimensions` must surface (and effectively require) the root-level MSA criteria or BW simulation is dead-on-arrival. Add a carve-out; don't state "always resolves" as a blanket invariant.

  ### D. NEW (precision, will bite the implementer) — `GroupAttributes` (match criteria) vs `HotelAttributes` (resolve input) have mismatched names AND inverted cardinality, and `resolve` sits exactly on that seam
  Confirmed fields — HotelAttributes: `msas: list`, `live_msas: list`, `country: Country` (single), `region: CanaryRegion`, `arbitrary_identifiers: list`. GroupAttributes: `msa` (single), `live_msa` (single), `countries: frozenset` (plural), `canary_region`, `arbitrary_identifier` (single). The doc's `resolve` example uses `"canary_region": "EU"` but the HotelAttributes field is **`region`**; `arbitrary_identifier` (group) vs `arbitrary_identifiers` (hotel); and cardinality inverts per attribute (a group matches ONE msa / a hotel has MANY; a group lists MANY countries / a hotel has ONE). So the endpoint **cannot `HotelAttributes(**payload)`** — it needs an explicit, tested payload→HotelAttributes field map. Likewise `simulator_dimensions` is described as "union of non-null attributes across groups" (group-side names) but the What-If form must emit hotel-side names. The doc's JSON examples mix both schemes and would mislead toward a direct splat. State the mapping explicitly. (Also: `brand_id`/sub-brand isn't in the resolve payload — if the Wyndham tree discriminates on `brand_id`, it must appear as a simulator dimension; only `parent_brand_id` is legitimately fixed.)

  ### E. NEW (feasibility) — the key-existence system check should hit the runtime introspector, not the generated `.pyi`
  Doc says the check ensures "every `SettingDisplay` key exists in the generated setting-key types (`generate_setting_types` output)." That output is a **static `.pyi` stub** produced by `pyright --createstub` (build artifact; can be stale; runtime-parsing it is fragile). The clean runtime source already exists: `SettingTypeGeneratorService.get_all_fields()` introspects the 5 models live and yields the dotted keys. Point the system check (and the "non-allowlisted key never appears" test) at `get_all_fields()`, not at `conformity.pyi`.

  ### F. NEW (correctness subtlety in the headline feature) — provenance "source" is the last *definer* along the winning path, not the path terminus
  Verified the walk (`get_all_setting_values_for_hotel_attributes`, conformity.py ~358-384): every setting advances to its per-level `winner`, but the value updates **only when that winner defines it** (`new_value is not NO_VALUE_DEFINED`). So a key's true source group can be an *ancestor* of the deepest matched group. `explain_resolution` must record `source = winner` at the same `if new_value is not NO_VALUE_DEFINED` point — not report the terminal matched node. The doc's "surface the winner the walk already determines" is right in spirit; flag this so the implementer doesn't naively label the path end. Otherwise the provenance description (per-key winner via `max(default_weight, settings_weights[key])` on the child→parent edge, walked from root) **matches the real algorithm** (`get_override_weight`) — confirmed accurate.

  ### G. NEW (minor / awareness)
  - `break_tie` has **two** `InvalidConformityTreeError` raise paths, not one: equal weights to parent (doc covers this) AND a direct override edge existing between two applicable siblings (conformity.py:421-426). Both are the same exception, so catching `InvalidConformityTreeError` for the 422 covers both — but the doc's framing ("tie on weight") is incomplete; the 422 `{groups, setting}` shape and "latent tree bug" log apply to both.
  - Dropping numeric weights from serialization (good hotelier call) means the **static Rules Tree tab can't express relative precedence among siblings that co-override the same parent** — direction-only "takes precedence over X" is ambiguous when two children both override one parent. Only the What-If/provenance view reveals who wins. Acceptable for v1; worth one sentence so it's a known limitation, not a surprise.

  ### Round-2 bottom line
  Direction still approved. Pre-ticketing must-fixes: **(A)** finally resolve the RF-v2/portfolio.py citation (cite `billing/views/billing_contact.py`, drop portfolio.py); **(B)** specify multi-brand-portfolio tree selection; **(C)** carve out MSA-gated roots (BW) from the "always resolves" simulator claim. Precision fixes before an implementer starts: **(D)** explicit payload→`HotelAttributes` field map (incl. `canary_region`→`region`), **(E)** check against `get_all_fields()` not the `.pyi`, **(F)** record provenance source at the definition point. **(G)** are one-line awareness notes. No architectural objections; the engine claims and provenance algorithm verified accurate. No Notion edits made this round (review only — would need explicit approval to apply any of the above to the doc).
project: null
source_id: null
tags: []
time_minutes: 5
title: Review this above property dashboard rules based configuration proposal
updated: 2026-06-16 18:30:00
waiting_on: null
waiting_since: null
working_on: false
---

https://app.notion.com/p/canarytechnologies/Rules-Browser-Above-Property-UI-for-Rules-Based-Configuration-37c81468615181be923cec1df122e5fd


Review