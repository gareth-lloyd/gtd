---
area: null
completed_at: null
contexts:
- deep
- fun
created: 2026-04-10 08:40:18.618057
defer_until: null
due: null
energy: high
id: 2026-04-10T0840-experiment-with-how-to-specify-gjms-in-r
order: 4
output: |
  ## Agent run 2026-06-18T16:24

  Design experiment — code-grounded against `backend/canary/`. No repo changes made;
  this is a worked design with concrete sketches. Sibling design doc:
  "Onboarding scripts use rules-based configuration"
  https://www.notion.so/canarytechnologies/Onboarding-scripts-use-rules-based-configuration-3828146861518176b79af4c6b5455905

  ### The key realization: SELECTION vs MATERIALIZATION
  The Notion doc lists guest-journey messaging as "irreducibly imperative" — but that
  conflates two separable layers:
  1. **Materialization** — turning a message spec (timing/template/channel/variants) into
     `GuestJourneyMessage` rows. This is genuinely imperative (static-file templates, Twilio
     WhatsApp templates, segment variants, languages). Keep it.
  2. **Selection** — WHICH messages a hotel of a given brand/MSA/region/live-state should get.
     This is pure config and is exactly what RBC is for. THIS is what the task targets.
  The task hint ("group attributes define a list of `GuestJourneyMessageUseCase`; at plan run
  time look up use-cases in a registry for the spec values") = make *selection* declarative,
  leave *materialization* imperative. That split is the whole experiment.

  ### Current state (grounding)
  - Use-case enums (per portfolio, unioned): `onboarding/models/use_case.py:6-105`
    (`BW/Wyndham/IHGGuestJourneyMessageUseCases`; union `GuestJourneyMessageUseCase`).
  - The "spec" already exists: `GuestJourneyMessageSpec`
    (`onboarding/configuration_providers/configs/guest_journey_message.py:24-56`) — carries
    `use_case`, timing (delta/anchor/direction/send_time), `template_path`, channel overrides,
    `enabled_policy`, `reminder`, `variants`.
  - TODAY the brand providers build `message_specs: dict[GuestJourneyMessage.Type,
    GuestJourneyMessageSpec]` imperatively in `__init__` (e.g.
    `configuration_providers/best_western/guest_journey_messages_provider.py`). **That dict is
    already a registry — it's just inlined in the provider and keyed by Type, not use-case.**
  - `ConfigureGuestJourneyMessagesPlan.execute` (`onboarding/plans/configure_guest_journey_messages.py`)
    iterates specs and calls `update_or_create_guest_journey_message(...)` →
    `GuestJourneyMessageService.create/create_system/update` + `GroupUseCaseService.set_..._for_use_case`.
    All idempotent, keyed by use-case.
  - RBC mechanics: settings are `(OverridePolicy FREE|FINAL, value)` tuples on `GroupAttributes`
    nodes (`enterprise_wyndham/configs/wyndham.py`); resolved by
    `ConformityService.get_all_setting_values_for_hotel_attributes` (`services/conformity.py:339-384`)
    → `dict[str, Any]`. Values may be lists today (e.g.
    `hotel.check_in_configuration.id_options`, conformity.pyi:366) and an enum/list value is
    opaque to resolution. Override replaces the WHOLE value at the winning node (no element merge).

  ### The decisive constraint
  Generic apply (`apply_portfolio_settings.apply_setting:165-173`, and the doc's proposed
  `apply_settings_to_hotel`) writes settings by dotted-path `setattr` and **hard-raises on any
  key not starting with `hotel.`**. There is NO `hotel.guest_journey_messages` model field —
  GJMs are separate rows materialized by a service. So a use-case-list setting is a
  **virtual / effectful setting**: it must NOT flow through the generic field-apply. It is
  resolved by RBC but *consumed by a dedicated plan*, not setattr'd.

  ### Proposed design (3 pieces)
  **(1) Registry — `use_case -> GuestJourneyMessageSpec`.** Hoist the specs currently inlined in
  each provider `__init__` into a module-level dict per portfolio (idiomatic: same shape as
  `KNOWN_PLANS`, `TOOL_REGISTRY`). The registry holds the STATIC spec skeleton only; dynamic
  context (languages, creator, group_name, rollout flags, feature-flag-driven channel overrides)
  stays computed at plan time and is merged in.
  ```python
  # onboarding/configuration_providers/<brand>/guest_journey_message_registry.py
  GJM_SPEC_REGISTRY: dict[GuestJourneyMessageUseCase, GuestJourneyMessageSpec] = {
      WyndhamGuestJourneyMessageUseCases.CHECK_IN_24_HRS: GuestJourneyMessageSpec(...),
      WyndhamGuestJourneyMessageUseCases.CHECKOUT_SAME_DAY: GuestJourneyMessageSpec(...),
      ...
  }
  def spec_for(use_case: GuestJourneyMessageUseCase) -> GuestJourneyMessageSpec:
      try: return GJM_SPEC_REGISTRY[use_case]
      except KeyError: raise <typed error>   # plan converts to raise_expected_error(...)
  ```
  **(2) RBC setting holding the use-case list — declared on group nodes.** A VIRTUAL key,
  deliberately NOT `hotel.`-prefixed so generic field-apply skips it by its existing guard:
  ```python
  # enterprise_wyndham/configs/wyndham.py
  WYNDHAM_CONNECT_GMS_LIVE.define(
      "guest_journey.message_use_cases", OverridePolicy.FINAL,
      [WyndhamGuestJourneyMessageUseCases.CHECK_IN_24_HRS,
       WyndhamGuestJourneyMessageUseCases.CHECK_IN_72_HRS_WITH_REMINDER,
       WyndhamGuestJourneyMessageUseCases.CHECKOUT_SAME_DAY, ...])
  ```
  Region/country variation falls out of RBC for free (declare a different list on
  `WYNDHAM_NORTH_AMERICA_LIVE`, or IHG AMER vs EMEA nodes) — that is the main payoff over the
  inlined dict, which has to branch on country in Python today.
  **(3) An effectful plan consumes the resolved list.** Either parameterize
  `ConfigureGuestJourneyMessagesPlan` or add a thin `ApplyRBCGuestJourneyMessagesPlan`:
  ```python
  def execute(self, hotel):
      attrs = HotelGroupAttributesService.fetch_hotel_attributes_for_hotel(hotel, sf=self.data.sf)
      resolved = ConformityService.get_all_setting_values_for_hotel_attributes(attrs)
      use_cases = resolved.get("guest_journey.message_use_cases", [])
      specs = {spec_for(uc).<type>: spec_for(uc) for uc in use_cases}   # registry lookup
      config = GuestJourneyMessageConfig(group_name=..., creator=..., available_languages=...,
                                         message_specs=specs, portfolio_identifier=...)
      # reuse existing materialization path (update_or_create_guest_journey_message)
  ```
  Net: RBC owns SELECTION (declarative, brand/region/live aware); the registry holds the spec
  per use-case; the plan does MATERIALIZATION (unchanged, imperative). Resolution stays a pure
  attributes→settings function; the virtual key is one extra consumer alongside generic
  field-apply (each filters the resolved dict to its namespace: `hotel.*` vs `guest_journey.*`).

  ### Design decisions / trade-offs to settle before building
  - **Virtual-key handling.** Cleanest = key-namespace convention: generic
    `apply_settings_to_hotel` applies only `hotel.*` keys (its guard already enforces this);
    `guest_journey.*` keys are owned by the GJM plan. Avoids inventing an "applier registry."
    The doc's apply service must explicitly *skip* (not raise on) non-`hotel.` keys.
  - **Whole-list override, no merge.** FREE/FINAL apply to the entire list value. A live node
    can't "add one message" to the base list without restating it. Acceptable for brand-level
    selection (lists are short, declared per terminal node). If per-message toggling is ever
    needed, the alternative is N boolean `guest_journey.use_case.<name>` keys — rejected: explodes
    the key space and the type stub. Recommend the single-list form.
  - **FREE vs FINAL.** The SET of messages a brand integration ships is an invariant ⇒ FINAL on
    the live node (re-asserted at go-live, matches the doc's FINAL-only go-live apply). Per-hotel
    CONTENT (template text, send_time tweaks) stays FREE and lives on the message rows, untouched
    by re-selection — `update_or_create` already preserves edited content where the spec leaves
    fields None. Worth verifying that re-running selection at go-live doesn't clobber ops edits.
  - **Static vs dynamic spec.** Registry = static skeleton; languages/creator/group_name/rollout
    flags + flag-driven `override_enable_*` stay plan-time. Don't try to push dynamic bits into RBC.
  - **Type safety.** `conformity.pyi` is pyright-generated; runtime `define()` takes `Any`, so the
    list-of-enum value works immediately. For typed `define()` overloads, add a
    `ListGuestJourneyUseCaseSettingKey` to the stub/generator — nice-to-have, not blocking.
  - **`enabled` / `has_*_messages` flags are a SEPARATE layer** already handled by the doc's first
    payload (`hotel.has_check_in_messages` → FINAL scalar, setattr). This experiment is orthogonal:
    flags via field-apply, message-set via the virtual key. They compose.

  ### Recommendation & smallest viable next step
  Option B (virtual RBC key + registry + effectful plan) is the right shape and fits the doc's
  "RBC is a pure resolve; some settings are effectful and owned by a dedicated plan" philosophy.
  Smallest spike to prove it end-to-end: pick ONE portfolio (Wyndham — single MSA, already the
  doc's worked example), (a) hoist its inlined specs into `GJM_SPEC_REGISTRY`, (b) add
  `guest_journey.message_use_cases` FINAL on `WYNDHAM_CONNECT_GMS_LIVE`, (c) write a unit test
  that resolves the list for a live Wyndham hotel and asserts registry lookup yields the exact
  specs the provider builds today. No materialization change, no go-live wiring — just prove
  selection round-trips. That de-risks the virtual-key/skip-in-generic-apply decision cheaply.

  ### Open questions for the human
  - Should selection live in the SAME diamond tree as `hotel.*` settings (one resolve, namespace
    filter) or a parallel GJM-specific tree? (Recommend same tree + namespace.)
  - Is whole-list override acceptable, or is per-hotel add/remove of individual messages a real
    requirement? (Drives single-list vs per-use-case-boolean.)
  - Re-asserting the message SET at go-live: confirm it won't revert ops-customized content on
    existing messages (the FREE/FINAL content-vs-selection boundary).

  ## Agent run 2026-06-18T16:42 — IHG segmentation / variants deep dive

  Pressure-tested the design against IHG (the hardest case: tier segmentation, AMER/EMEA,
  V2 variants, hardcoded Twilio segments). IHG does NOT break the model — it forces splitting
  three axes currently tangled in one provider `__init__`.

  ### Three axes, three layers
  - **A. Selection** (WHICH messages) — driven by brand/region/MSA/pilot, all HOTEL-level ⇒ RBC.
  - **B. Tier targeting / variants** (within a message, which template a guest gets) — driven by
    per-RESERVATION loyalty tier × recurrence, evaluated at SEND time
    (`SegmentEvaluator.evaluate_segment`, `guest_journey/services/message_variant.py:402-478`)
    ⇒ lives in the registry spec, NEVER in RBC.
  - **C. Content/materialization** (templates, Twilio/WhatsApp, IHGHardcodedSegment, channels)
    ⇒ imperative, unchanged.

  The earlier "IHG can't be a declarative list because the set is derived from (region, brand,
  onboarding_type)" is a MISREAD: region+brand ARE RBC group attributes. The IHG provider's
  `get_ihg_region(country)` → `ALL_BRANDS_CUSTOM_MESSAGES_BY_REGION[region]` +
  `BRAND_SPECIFIC_MESSAGES_BY_REGION[region][brand_id]` branching
  (`onboarding/configuration_providers/ihg/guest_journey_messages_provider.py`) is a hand-rolled
  diamond-tree resolution. Moving it to RBC nodes SIMPLIFIES selection.

  ### Axis B is the key answer: variants stay OUT of RBC
  A variant's `segment_expression` (JSON tree over loyalty/recurrence/rate_code/stay_length) is
  per-guest RUNTIME data; RBC group attributes are hotel-scoped. A guest's IHG loyalty tier is
  not a hotel property ⇒ member/non-member/elite split can't be a group attribute. IHG's
  "5 checkout use-cases per region" is a V1 transitional artifact: TWO segmentation systems are
  live at once — V1 (separate top-level message per tier + legacy `GuestSegment.segments_data`)
  and V2 (`rollout_message_variants=True`: ONE message, N `MessageVariant` rows w/
  segment_expression, picked at send time by `get_best_variant_for_reservation`, priority desc +
  None-expression fallback). Under V2 the tier fan-out collapses INTO a single message's variants.
  ⇒ The durable RBC selection unit is the message/use-case; tier variants ride inside its spec.
  Target V2; follow the V1→V2 consolidation — do NOT encode the V1 tier-per-use-case explosion.

  ### Axis A needs a NEW resolver primitive: UNION, not override-winner
  Biggest concrete finding. RBC resolution picks ONE winning node per key (`break_tie`,
  `conformity.py`). But IHG message sets are ADDITIVE: regional base + brand luxury add-on
  (Kimpton Inner Circle, IC Royal Ambassador) + pilot extras. With override-replace, a
  Kimpton-AMER node must RESTATE the whole AMER base list + the add-on — combinatorial
  restatement across every brand×region, strictly worse than today's `.extend()`. The task's own
  phrasing ("GROUP attributes define a list") implies the fix: each matching node CONTRIBUTES its
  slice; hotel set = UNION over all matching nodes. That's a second resolve primitive:
  ```python
  # NEW, alongside get_all_setting_values_for_hotel_attributes (diamond winner)
  ConformityService.collect_set_valued_setting(attrs, "guest_journey.message_use_cases")
  #   -> set().union(*[node.list for node in matching_nodes])   # maps .extend() exactly
  ```

  ### Registry holds spec FACTORIES, not frozen specs
  Pure `dict[use_case, frozen_spec]` works for BW but not IHG: the VARIANT SET is brand-dependent
  (`get_variant_specs_for_message_type(POST_CHECK_IN_MESSAGE, brand_id, region)` → 6 or 8
  variants). So registry value = `Callable[[SpecContext(brand_id, region, languages,...)],
  GuestJourneyMessageSpec]` — the per-message builders hoisted out of the provider `__init__`.
  brand_id/region come from the resolved RBC attrs. Plan = resolve union of use-cases →
  factory(ctx) per use-case → existing GuestJourneyMessageVariantsService materialization.

  ### Genuinely hard caveats
  - **De-selection under union.** Union adds trivially but can't REMOVE. Today's plan has
    `use_cases_to_delete` (deprecated IHG pre-arrival set). Need a parallel
    `guest_journey.deprecated_use_cases` collect-set the plan subtracts, OR keep deprecation
    imperative. Decision needed.
  - **Selection != enabled-state.** Pilot messages are selected-but-disabled at go-live
    (`enabled_at_go_live=False`). Use-case list = "exists"; per-use-case `enabled_policy` stays in
    the spec — don't model on/off in RBC.
  - **V1/V2 ordering.** Land RBC selection AFTER/with the V1→V2 variant consolidation per
    portfolio. BW (mostly V2, simple) first; IHG (mid-migration) is the real validation.
  - **Conditional extras.** `IHG_PILOT` is already an onboarding-type/MSA ⇒ natural RBC node.
    `should_enable_greener_stay(data)` is a feature flag — arbitrary_identifier group attr OR
    plan-time condition on the resolved set.

  ### Updated recommendation
  BW-first round-trip spike still right, but it only proves the easy 80%. Add a SECOND spike that
  ports IHG's region/brand `.extend()` branching to union-resolved RBC nodes — that exercises the
  two must-build pieces (UNION/collect resolver + factory-valued registry) that BW never touches,
  and is what actually de-risks the approach.

  Key files: `guest_journey/services/message_variant.py:402-478` (send-time variant pick),
  `guest_journey/services/guest_journey_message_variants_service.py` (variant materialization),
  `guest_journey/models/message_variant.py` (variant model),
  `segmentation/models/segment.py` + `segmentation/services/segment_evaluator.py` (segment_expression),
  `guest_journey/constants.py:46-76` (IHGHardcodedSegment),
  `onboarding/configuration_providers/ihg/guest_journey_messages_provider.py` (region/brand branching),
  `onboarding/configuration_providers/configs/guest_journey_message.py:81-131` (variant spec).

  ## Agent run 2026-10-14T15:04 — fit with the ENT-7726 rules registry

  > Follow-up asked: "In the context of this proposal, look at the system which is currently
  > being prototyped using this plan: ~/.claude/plans/zippy-soaring-metcalfe.md. The predicates
  > e.g. SuperSetOf plus the `reader` mechanism should come in handy. Report back your conclusions"

  Read: the plan (all 657 lines), `predicates.py` in the ent-7726 worktrees, `problem_with_define`
  and `get_actual_hotel_setting` on `glloyd/ent-7726-merge-and-boot-checks` (#59059),
  `GroupUseCaseService` and `GuestJourneyMessageGroupUseCase`, and `onboarding/models/use_case.py`.
  Nothing was run. No repo changes.

  ### Conclusion: yes, it fits. Two earlier calls change
  **1. `SupersetOf` conjunction gives the UNION primitive, so no new resolver is needed.**
  Run 2 asked for a `collect_set_valued_setting` union resolver, because IHG message sets add up:
  the regional base, plus a luxury-brand add-on, plus pilot extras. In the registry, every rule
  that matches a hotel applies, and their constraints are joined with AND.
  `AllOf(SupersetOf(*AMER_BASE), SupersetOf(*KIMPTON_EXTRAS))` means "the hotel has at least the
  union of both lists". The planned `AllOf.candidate_values` merged candidate (plan step 13,
  "union of its SupersetOf parts, in authored order") is that union, computed. So:
  - selection is `SupersetOf(...)` on a use-case-set key;
  - the union falls out of the conjunction;
  - `satisfiable` and the boot checks already cover it. For example, a PMS rule
    `SubsetOf(...allowed...)` that forbids a message a brand requires fails at boot. That is the
    real `PMS_CAPABILITY` use: "this PMS can't drive pre-arrival".

  `SupersetOf` (not `Equals`) is also the right semantics for drift. Ops-added or hotel-specific
  extra messages don't drift. Only a MISSING required message does.

  **2. The `reader` mechanism replaces run 1's "virtual key" hack, and makes conformity and drift
  work.** Run 1 needed a key that generic apply skips. The plan's step 9 reader
  (`services/value_readers.py`, per-key, "consulted only inside the conformity comparison, NOT by
  `get_actual_hotel_setting`") does that properly.
  - The reader for `guest_journey.message_use_cases` returns `frozenset(use_case_identifier)` from
    `GuestJourneyMessageGroupUseCase` for the hotel. Model:
    `onboarding/models/guest_journey_message_use_case.py`, unique per (hotel, use_case_identifier).
    Stale associations are already filtered by `GroupUseCaseService.get_guest_journey_messages_by_use_cases`.
  - Payoff: `hotel_conforms`, drift, monitoring and the config-drift view report "hotel X is missing
    CHECKOUT_SAME_DAY" with no new code, and `ConformityError.failed_rules` cites the rule.
  - The planned guard, "finalize() rejects a brand plain value or any default= on a key with a
    reader", is exactly what we want here. RBC never writes this key, so generic
    `apply_portfolio_settings` cannot touch it. Writing (materialization) stays with the dedicated
    GJM plan. Selection and materialization split along the reader boundary.
  - Registration follows the gdpr pattern: guest_journey or onboarding registers its reader from a
    `configuration_rules/` module picked up by autodiscover. The engine doesn't import
    guest_journey. Expect a new dependency edge in `ci/deps/opinionated_state.py`.

  ### How the plan consumes it
  The GJM plan reads the merged entry's `constraint`, not a value. Its required set =
  the merged `SupersetOf` candidate. Its forbidden set = the `SubsetOf` parts. It then:
  - looks up each required use-case in the spec registry (run 2: factories, per portfolio);
  - materializes the missing ones through the existing `update_or_create_guest_journey_message`
    path.

  It needs one small public helper, e.g. `required_members(predicate) -> list`. Don't make callers
  reach into `candidate_values`, which exists for satisfiability, not for writes. It also keeps
  "value reads never return a predicate" true.

  ### Gaps: what the registry does NOT give us today
  - **Key universe.** `problem_with_define` raises `unknown setting key` for anything that isn't a
    Django field in the generated `SettingKey` aliases. `guest_journey.message_use_cases` is not a
    field. It needs a "virtual setting" declaration: the key, an item domain (the use-case enum),
    and its reader. `_mismatch` and `can_store` must check items against that domain. Typing cost:
    a seventh key alias means another overload on BOTH `GroupAttributes.define` and
    `ScopedRules.define`. That is the "fourteen-signature edit" risk the plan already flags.
    Alternative: allow virtual keys only with predicates and type their `value` as `Predicate`.
  - **Brand selection lives in the brand tree, which is winner-takes-one.** GJM selection is a
    brand preference. It is not LAW / PMS_CAPABILITY / PLATFORM, and the registry's `Scope` is
    countries only, with no brand or MSA dimension. So the IHG brand×region union only happens if
    it is authored as registry rules, and brands are not an authority. Options:
    (a) Brand tree, `FINAL SupersetOf(...)`, with each defining node restating its list from Python
        constants (`SupersetOf(*AMER_BASE, *KIMPTON_EXTRAS)`). No engine change. It works if the
        IHG tree already has the brand×region nodes. NOT verified. Check the IHG tree before
        choosing.
    (b) An engine change: mark a key "conjunctive", so the brand resolver joins the predicates of
        every matching group with AND instead of picking the winner. With predicates this is
        well-defined and boot-checkable. It is the clean form of run 2's union resolver, but it
        changes the brand resolver, which the plan deliberately leaves alone.
    Recommend (a) first and (b) only if restatement blows up.
  - **No negative predicate.** De-selection (the deprecated IHG pre-arrival set,
    `use_cases_to_delete`) needs "contains none of". `SubsetOf` would mean listing every allowed
    member. Add `NoneOf(*values)` / `DisjointFrom`, the mirror of `SupersetOf`. Its candidates are
    `[]`, and it merges with the `SupersetOf` union candidate. Small, but must go in the
    satisfiability matrix test. The GJM plan then deletes the forbidden ones that are present.
  - **Defaults don't union.** Two co-matching CONVENTION rules on one key is a boot error, and a
    binding default is "first that satisfies". So don't try to express selection as defaults. The
    constraint-driven plan above avoids defaults entirely, which is consistent with the
    reader-key rule that rejects `default=`.
  - **StrEnum value collisions.** `welcome_message`, `mid_stay_message` and
    `post_check_out_message` exist in more than one portfolio enum. StrEnum `==` and hash compare
    by string, so `BW.WELCOME_MESSAGE == Wyndham.WELCOME_MESSAGE`. Predicates compare by `==`.
    Conformity is fine, because a hotel belongs to one portfolio. But the item-domain check can't
    tell the portfolio enums apart, and a single cross-portfolio spec registry dict would collide.
    Keep the spec registry per portfolio (as run 1 had it), or key it by
    (portfolio, use-case).
  - **Exists vs enabled.** The reader should report "message exists" (pilot messages are selected
    but disabled at go-live). An enabled-set check, if wanted, is a second key with its own reader.
  - **Not yet built.** `SupersetOf` is planned for #59043 and is not in any worktree yet.
    `value_readers.py` is plan step 9 (PR 2) and not started. Both are prerequisites. Nothing here
    needs the convention work (PR 4).

  ### Updated recommendation
  1. Keep the selection / materialization split. Swap run 2's "new union resolver" for
     `SupersetOf` + conjunction, and swap run 1's "virtual key skipped by apply" for a
     reader-backed key.
  2. Engine asks to feed back into ENT-7726 (not urgent; after PR 2):
     - virtual-setting registration (key + item domain + reader);
     - a `NoneOf` predicate;
     - a public `required_members` helper.
     Flag the brand-tree winner-takes-one question as an open design point. Don't build it yet.
  3. Spike (replaces run 2's IHG spike, after `SupersetOf` and readers land):
     - register the `guest_journey.message_use_cases` reader;
     - put `FINAL SupersetOf(...)` on Wyndham Connect live;
     - assert that `hotel_conforms` flags a live Wyndham hotel whose CHECKOUT_SAME_DAY association
       was deleted, and that the merged constraint's required set equals what
       `WyndhamGuestJourneyMessagesProvider` builds today.
     Then try IHG AMER + Kimpton as two `SupersetOf` defines to test option (a).

  Plan: ~/.claude/plans/zippy-soaring-metcalfe.md. Stack: #59043 / #59047 / #59059
  (https://github.com/canary-technologies-corp/canary/pull/59043,
  https://github.com/canary-technologies-corp/canary/pull/59047,
  https://github.com/canary-technologies-corp/canary/pull/59059), ENT-7726
  (https://linear.app/canary-technologies/issue/ENT-7726/implement-binding-rules-tree-prototype).
project: 2026-04-16T1319-rules-based-config
source_id: null
tags:
- focus
time_minutes: 60
title: Experiment with how to specify Guest journey messages in Rules based configuration.
  Circulate doc
updated: 2026-10-14 17:59:56.486087
waiting_on: null
waiting_since: null
working_on: false
---

* The group attributes could define list of `GuestJourneyMessageUseCase` enum values
* At plan run time, use-cases could be looked up  in a registry for the spec values