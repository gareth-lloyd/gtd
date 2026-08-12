---
area: null
completed_at: null
contexts:
- react
created: 2026-08-10 11:40:43.176856
defer_until: null
due: 2026-08-12
energy: low
id: 2026-08-10T1140-follow-up-on-fix-payment-gateway-required-for-toke
order: null
output: |
  ## Agent run 2026-08-10T14:04:04Z — SUPERSEDED by the 14:09:41Z run below

  Two claims in this section are wrong (the startup/boot risk, and the blast-radius
  framing). Kept for the audit trail; use the corrected run below for the ticket text.

  Verified Joshua's finding in the repo. It is worse than reported — **both** keys in
  the rule are dead, and the rule has never been able to fire. Also found a real design
  tension that makes this more than a two-string rename. Draft ticket below, ready to
  paste into Linear.

  ### What I verified (all read-only, nothing changed, nothing posted)

  Rule: `backend/canary/check_in/configuration_rules/consistency_rules.py:9-24`

  ```python
  tokenizes   = settings.get("hotel.check_in_configuration.tokenize_card") is True
  has_gateway = settings.get("hotel.payment_gateway_config_id") is not None
  ```

  The setting keyspace is generated from model fields by
  `rules_based_configuration/services/setting_type_generator.py` (CONFIGURABLE_MODELS =
  Hotel, CheckInConfiguration, CheckOutConfiguration, AuthorizationConfiguration,
  MembershipGatewayConfiguration) and materialised as Literal unions in
  `rules_based_configuration/services/conformity.pyi`. Checked both keys against it:

  | Key in rule | Exists? | Real key |
  | --- | --- | --- |
  | `hotel.check_in_configuration.tokenize_card` | **No** | `hotel.check_in_configuration.is_tokenizing_with_hotel_payment_gateway` (`BoolSettingKey`, conformity.pyi:182) |
  | `hotel.payment_gateway_config_id` | **No** (not a field on `Hotel`) | `hotel.check_in_configuration.payment_gateway_config_id` (`UUIDNullableSettingKey`, conformity.pyi:132) |

  Because the *first* key is also wrong, `tokenizes` is always `False`, so the rule
  returns `[]` unconditionally. It is a permanent no-op, not a half-working rule.
  Joshua spotted the gateway key; the tokenize key is a second, independent typo.

  The sibling rule in the same file (`id_step_required_for_additional_guests_id`) uses
  valid keys — this is isolated to one rule.

  **Why the tests didn't catch it:** `rules_based_configuration/tests/services/test_consistency.py:91-135`
  hand-builds the settings dict using the *same* two wrong keys, so the test is
  self-consistent with the bug and passes. Zero protection. Fixing the rule without
  fixing the test leaves the test asserting on a keyspace that doesn't exist.

  ### The part that isn't a rename

  `CheckInConfiguration.clean()` (`check_in/models/configuration.py:1263-1280`) already
  encodes the real invariant, and it has an exemption the rule lacks:

  ```python
  if (self.is_tokenizing_with_hotel_payment_gateway
          and not hotel.payment_gateway.gateway):  # Exclude old payment gateway configs for Freedompay and Shift4
      if not self.payment_gateway_config_id:
          raise ValidationError(...)
  ```

  Hotels on legacy FreedomPay/Shift4 gateway configs tokenize *without* a
  `payment_gateway_config_id`. A naively-fixed rule flags every one of them.
  And `hotel.payment_gateway.gateway` is a related object, so it is **not expressible
  in the flat scalar keyspace** the consistency rules operate on. The only
  gateway-ish scalars on `Hotel` are `payment_gateway_name` (free-text survey field,
  `hotels/models/hotel.py:925`) and `has_payment_gateway_settings` (adminland UI
  toggle, :1084) — neither is authoritative. `clean()` also checks a second condition
  the rule doesn't: that the gateway actually advertises `PaymentGatewayCapability.TOKENIZE`.

  ### Blast radius of turning it on — read this before scoping as "small"

  Four call sites consume `ConsistencyService.validate_settings`, and they are not all
  warn-only:

  1. `services/conformity.py:672` — inside `ConformityService.finalize()`. **Raises**
     `ConfigurationConsistencyError` if any tree combination trips a rule. This is
     app-startup. If any MSA tree declares `is_tokenizing_with_hotel_payment_gateway=True`
     without a `payment_gateway_config_id`, canary stops booting. This is the real risk
     in the ticket, and it contradicts the "warn-only, treat it as the linter layer"
     framing I gave Joshua — that framing is accurate for the *save* path only.
  2. `checks.py:19` — Django system check over tree combinations (CI surface).
  3. `signals.py:64` — admin save path, warn-only via `messages.warning`. Genuinely non-blocking.
  4. `services/hotel_config_health.py:163` — fleet health page, runs against **actual
     hotel settings**, so this one starts reporting on the real fleet immediately.

  (2) and (3) are safe. (1) is a boot risk and (4) is a "how many hotels light up"
  question. Both need checking before merge, which is why I've scoped this as three
  steps rather than one.

  ---

  ## DRAFT LINEAR TICKET

  **Title:** `payment_gateway_required_for_tokenization` references two non-existent setting keys and has never fired

  **Team:** whichever owns `rules_based_configuration` (mine, I think — confirm vs Asher/Tincho)
  **Labels:** bug, tech-debt, rules-based-configuration
  **Priority suggestion:** Medium. Nothing is broken in production *because* of this — the
  rule is inert, so there's no bad behaviour to unwind. But it's load-bearing for
  credibility: Joshua is planning next block's oncall-improvement work on top of
  `configuration_consistency_rule`, and the flagship example of that decorator is a
  no-op. Worth fixing before his work lands on it, not urgent this week.

  ### Context

  Joshua Hart found this while evaluating `configuration_consistency_rule` for the SDM
  oncall-improvement project:
  https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1785950349523259
  (my reply committing to the fix:
  https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1785956358642849?thread_ts=1785950349.523259&cid=C047K6WSUJY)

  Design doc: https://app.notion.com/p/canarytechnologies/Rules-based-hotel-configuration-269814686151800f8812f8373d3f90e3
  Tree visualisation (Asher): https://pages.cnry.cloud/rules-based-config/

  ### Problem

  `check_in/configuration_rules/consistency_rules.py:9-24` reads two setting keys that
  do not exist in the generated keyspace:

  - `hotel.check_in_configuration.tokenize_card` → should be
    `hotel.check_in_configuration.is_tokenizing_with_hotel_payment_gateway`
  - `hotel.payment_gateway_config_id` → should be
    `hotel.check_in_configuration.payment_gateway_config_id`

  Because the tokenization key is also wrong, the guard is always `False` and the rule
  returns `[]` for every input. It has never fired. The unit tests pass because they
  construct the input dict with the same two wrong keys.

  ### Scope

  **1. Fix the rule, with the legacy-gateway exemption.**
  Port the semantics from `CheckInConfiguration.clean()` (`check_in/models/configuration.py:1263`),
  which is the existing source of truth. Decide how to handle the FreedomPay/Shift4
  exemption — `hotel.payment_gateway.gateway` is a related object and isn't in the flat
  keyspace. Options:
  - (a) Narrow the rule to what's expressible and accept false positives on legacy
    hotels. Cheapest; needs a count first (see step 3).
  - (b) Expose legacy-gateway presence as a derived scalar setting so the rule can be
    written accurately. Correct, but widens the keyspace and touches
    `setting_type_generator`.
  - (c) Drop the rule and lean on `clean()`. Rejected in my view — `clean()` doesn't
    feed the fleet-health page, and this rule is the reference example for the decorator.

  My lean is (b) if the derived setting is cheap, else (a) with the false-positive count
  documented in the PR. The capability check (`PaymentGatewayCapability.TOKENIZE`) is out
  of scope for a consistency rule — it needs a live gateway API call, which doesn't
  belong in a pure settings predicate.

  **2. Make this class of bug impossible.**
  Right now a rule can `settings.get()` any string it likes and silently never fire.
  Proposal: have `@configuration_consistency_rule` take a declared key list
  (`@configuration_consistency_rule(keys=[...])`), and validate those keys against the
  generated keyspace at import or in `ConsistencyService.finalize()`. Fail loudly on an
  unknown key. The keyspace is already available — the Literal unions in `conformity.pyi`
  are generated, and `HotelComparisonService.get_comparable_setting_keys()` exists at
  runtime. Alternatively type the keys as the generated Literal unions so pyrefly rejects
  a typo, though the current `AnySettingKey` alias is only the residual untyped bucket
  (13 i18n/opaque keys), not the full union — a `SettingKey` union alias would need
  generating first.

  This step is arguably the more valuable half of the ticket. One dead rule is a typo;
  a decorator that silently accepts dead rules is a trap for everyone building on it next
  block.

  **3. Check blast radius before merging.**
  - Confirm no MSA tree combination trips the corrected rule — `ConformityService.finalize()`
    (`services/conformity.py:672`) **raises** on a consistency error, so a tripped rule is
    an app-startup failure, not a warning. `MSA_HOTEL_PROVIDERS` currently only has
    Wyndham Connect GMS, so the surface is small today, but check it explicitly.
  - Count how many live hotels the corrected rule flags via
    `HotelConfigHealthService._check_consistency` (`services/hotel_config_health.py:163`),
    which runs against actual hotel settings. If legacy-gateway hotels dominate the count,
    that decides step 1 in favour of (b).
  - Fix `tests/services/test_consistency.py:91-135` to use real keys, and add a case
    covering the legacy-gateway exemption.

  ### Out of scope

  - Adding a blocking mode to the config-save path (`signals.py` is warn-only by design;
    separate decision).
  - Tree definitions for ESA / Four Seasons / Drury (flagged separately in the same thread).
  - Template/named-config packages (the entity-shaped-data gap Joshua raised; unbuilt part
    of the design doc).

  ### Acceptance criteria

  - The rule references only keys present in the generated setting keyspace.
  - The rule returns an error for a tokenizing hotel with no check-in gateway config, and
    does **not** error for a legacy FreedomPay/Shift4 hotel.
  - Tests exercise real setting keys, including the legacy-gateway case.
  - A rule referencing an unknown setting key fails loudly (test proving it).
  - `ConformityService.finalize()` still succeeds for every registered tree.

  ---

  ### Notes for you before filing

  - I have **not** created the Linear ticket, and have **not** replied in the Slack thread
    — both need your say-so. Say the word and I'll create the ticket with the text above
    (or a trimmed version); for Slack you'd need to write the reply yourself per the
    human-authored-communication rule.
  - One thing to decide: my Slack reply told Joshua the rules are "warn-only at this time
    / treat as the linter layer." That's true of the save path but **not** of
    `ConformityService.finalize()`, which raises at startup. If he's designing against
    "warn-only", that's a misconception worth correcting in-thread before he builds on it.
  - Tests not run — this was analysis only, no code changed.

  ---

  ## Agent run 2026-08-10T14:09:41Z — corrected after reading the whole system

  Re-examined the full app (apps.py wiring, conformity.py 848 lines, hotel_comparison.py,
  hotel_config_health.py, drift.py, the three tree config modules, git history). Three
  corrections, one of which kills my headline risk, and one new finding that is more
  important than the original bug.

  ### Retracted

  **1. There is no startup/boot risk. My main risk claim was wrong.**
  I asserted that fixing the keys could make `ConformityService.finalize()` raise at app
  ready. Checked the actual tree definitions: `enterprise_wyndham/configs/wyndham.py:361-366`
  declares **both** keys on the **same group** (`WYNDHAM_NORTH_AMERICA_LIVE`):

  ```python
  WYNDHAM_NORTH_AMERICA_LIVE.define(
      "hotel.check_in_configuration.payment_gateway_config_id", OverridePolicy.FINAL, ANY_NON_NULL)
  WYNDHAM_NORTH_AMERICA_LIVE.define(
      "hotel.check_in_configuration.is_tokenizing_with_hotel_payment_gateway", OverridePolicy.FINAL, True)
  ```

  `get_all_possible_setting_combinations` (conformity.py:482-511) accumulates a
  *per-group dict* along each root→node path, so these two keys always travel together.
  No combination yields `tokenizing=True` without the gateway key. `best_western.py` and
  `ihg_pilot.py` declare neither key, so they can't trip it either. The corrected rule
  passes `finalize()` cleanly. The mechanism I described is real (finalize() *is* called
  in `apps.py:ready()` and *does* raise) — it just isn't reachable with today's trees.
  It stays a latent hazard for a future tree, not a present risk. Priority drops.

  **2. "It starts reporting on the real fleet immediately" was too broad.**
  The save path is far narrower than I implied. `validate_hotel_on_save`
  (conformity.py:811-848) returns `None` early when the hotel matches no tree, and builds
  `actual_settings` from `list(expected_settings.keys())` — **only tree-declared keys**.
  So the save-path consistency check runs only for tree-matched hotels and only sees keys
  the tree declares. It is not a general fleet linter. Only
  `HotelConfigHealthService._check_consistency` (hotel_config_health.py:153-164) evaluates
  all comparable keys for any hotel.

  ### New finding — bigger than the typo

  **A consistency rule shaped `settings.get(k) is not None` can never fail in the tree
  layer, by construction.** The tree's idiom for "must be set, value varies per hotel" is
  the `ANY_NON_NULL` sentinel (`conformity.py:32-46`) — a singleton *instance*. So
  `settings.get("...payment_gateway_config_id") is not None` evaluates `ANY_NON_NULL is not
  None` → `True`. The rule concludes a gateway is present because the tree said "some
  gateway will be present".

  Consequence: `ConformityService.finalize()` and `checks.py` — the two layers that look
  like the CI/linter guarantee — are **structurally incapable of catching any
  null-presence violation**. They can only catch contradictions between concrete declared
  values. Every rule of this shape is a no-op there regardless of whether its keys are
  spelled correctly. That's the defect worth fixing; the typo is just what made it visible.

  ### Also worth knowing before prioritising

  **The invariant is already enforced for the cohort that matters, twice over.** For
  Wyndham NA live hotels, `payment_gateway_config_id = ANY_NON_NULL` + `is_tokenizing = True`
  as `OverridePolicy.FINAL` already produces a **conformity** error (expected ANY_NON_NULL,
  actual None → `ConformityError` via `_compare_settings`, conformity.py:768-773) — a
  different code path from consistency, and one that works today. On top of that,
  `CheckInConfiguration.clean()` (`check_in/models/configuration.py:1263-1280`) enforces it
  on save *with* the legacy FreedomPay/Shift4 exemption. So the fixed rule's genuine
  marginal value is narrow and specific: **hotels with no tree definition, surfaced on the
  fleet-health page**. That is still real value (it's most of the fleet), but it is not
  "an unenforced invariant".

  ### Confirmed from run 1 (re-verified, these hold)

  - Both keys are wrong; `tokenize_card` has never existed on the model
    (`git log --all -S "tokenize_card = "` on `check_in/models/configuration.py` → no hits).
    Real keys: `...is_tokenizing_with_hotel_payment_gateway` and
    `hotel.check_in_configuration.payment_gateway_config_id`. Rule is inert.
  - The rule *is* registered in production — `autodiscover_modules("configuration_rules")`
    in `rules_based_configuration/apps.py:22`, before `finalize()`. It's dead, not unwired.
  - Tests (`test_consistency.py:91-135`) hand-build the dict with the same wrong keys.
  - Neither key is filtered by the sensitive-key regex (ran `_SENSITIVE_FIELD_RE` against
    both: no match — the regex comment at hotel_comparison.py:86-89 deliberately word-bounds
    `token`/`sid` to protect `is_tokenizing_with_hotel_payment_gateway`). So both reach the
    fleet-health check. My worry that they'd be filtered out was unfounded.
  - Consistency rules are **not** part of drift detection — `drift.py` only calls
    `ConformityService`. Tincho's answer to Joshua was correct.
  - `MSA_HOTEL_PROVIDERS` (drift.py:31-34) does contain only `WYNDHAM_CONNECT_GMS`, so my
    Slack flag about ESA/Four Seasons/Drury lacking tree definitions was accurate.
  - The legacy-gateway exemption problem is real: `hotel.payment_gateway` is an
    `AutoOneToOneField` related object (`hotels/models/payment_gateway.py:24`), not one of
    the five `CONFIGURABLE_MODELS`, so it is not expressible in the flat keyspace.

  ---

  ## REVISED DRAFT LINEAR TICKET

  **Title:** Consistency rules can't express null-presence invariants; `payment_gateway_required_for_tokenization` is dead and proves it

  **Team:** owner of `rules_based_configuration`
  **Labels:** bug, tech-debt, rules-based-configuration
  **Priority suggestion:** Medium-low as a bug, Medium as a foundation fix. Revised down
  from my first pass: there is no production breakage, no boot risk, and the invariant is
  already enforced for Wyndham NA live hotels by tree conformity (`ANY_NON_NULL`) and by
  `CheckInConfiguration.clean()`. What justifies doing it is that Joshua is planning next
  block's oncall-improvement work on `configuration_consistency_rule`, and the decorator
  currently (a) accepts rules referencing keys that don't exist, and (b) silently no-ops
  null-presence rules in the CI layer. Both are traps for anyone building on it.

  ### Context

  Found by Joshua Hart while evaluating the decorator for the SDM oncall project:
  https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1785950349523259
  My reply committing to a fix:
  https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1785956358642849?thread_ts=1785950349.523259&cid=C047K6WSUJY
  Design doc: https://app.notion.com/p/canarytechnologies/Rules-based-hotel-configuration-269814686151800f8812f8373d3f90e3
  Tree visualisation (Asher): https://pages.cnry.cloud/rules-based-config/
  Introduced in ENT-4739 / #35648 (`d744af02bc5`, 2026-01-06).

  ### Problem 1 — the rule is dead (the visible symptom)

  `check_in/configuration_rules/consistency_rules.py:9-24` reads two keys that do not
  exist in the keyspace generated by `setting_type_generator.py`:

  | In the rule | Correct key |
  | --- | --- |
  | `hotel.check_in_configuration.tokenize_card` | `hotel.check_in_configuration.is_tokenizing_with_hotel_payment_gateway` |
  | `hotel.payment_gateway_config_id` | `hotel.check_in_configuration.payment_gateway_config_id` |

  Both are wrong, so `tokenizes` is always `False` and the rule returns `[]` for every
  input. It has never fired. Tests pass because they build the input dict with the same
  two wrong keys.

  ### Problem 2 — the layer that looks like CI enforcement can't enforce this class of rule

  `ConformityService.finalize()` (conformity.py:665-676) and `checks.py` validate rules
  against *tree-declared* settings. The tree expresses "must be set, per-hotel value" as
  the `ANY_NON_NULL` sentinel instance, so any rule testing `is not None` sees a non-None
  sentinel and passes. These two layers cannot catch a null-presence violation for any
  rule, correctly spelled or not. Only the actual-value layers can:

  | Call site | Key universe | Values | Useful for this rule? |
  | --- | --- | --- | --- |
  | `conformity.py:672` (`finalize()`, app ready, **raises**) | tree-declared only | may be `ANY_NON_NULL` | No — sentinel defeats it |
  | `checks.py:19` (Django system check) | tree-declared only | may be `ANY_NON_NULL` | No — same |
  | `signals.py:64` (admin save, warn-only) | tree-declared only, tree-matched hotels only | real | Partially (Wyndham NA only) |
  | `hotel_config_health.py:163` (fleet health page) | all comparable keys, any hotel | real | **Yes — this is the one** |

  ### Scope

  **1. Make the decorator reject unknown keys.**
  Have `@configuration_consistency_rule` declare the keys it reads
  (`@configuration_consistency_rule(keys=[...])`) and validate them against the generated
  keyspace at registration or in `ConsistencyService.finalize()`. Fail loudly. The
  universe is already available: `SettingTypeGeneratorService.get_all_fields()` →
  `HotelComparisonService.get_all_setting_keys()`. This is the item that stops the bug
  class recurring, and it's cheap.

  **2. Decide what consistency rules do about `ANY_NON_NULL`.**
  Options: make rules sentinel-aware (treat `ANY_NON_NULL` as "unknown, skip" rather than
  "present"); or tag rules with the layers they're valid in so the tree layer skips
  presence rules instead of silently passing them; or accept that presence rules are
  fleet-health-only and document it. Needs a call — this determines whether the CI layer
  is trustworthy for the rules Joshua wants to add next block. My lean: sentinel-aware,
  skipping on `ANY_NON_NULL`, because "the tree promised a value" genuinely is not evidence
  that a hotel has one.

  **3. Fix the rule itself, with the legacy exemption.**
  Port semantics from `CheckInConfiguration.clean()` (`check_in/models/configuration.py:1263`),
  the existing source of truth, which skips the check when `hotel.payment_gateway.gateway`
  is set (legacy FreedomPay/Shift4 hotels tokenize without a `payment_gateway_config_id`).
  That relation isn't in the flat keyspace, so either expose legacy-gateway presence as a
  derived scalar setting, or scope the rule to what's expressible and count the false
  positives first. The `PaymentGatewayCapability.TOKENIZE` check in `clean()` stays out of
  scope — it needs a live gateway API call, which doesn't belong in a pure settings predicate.

  **4. Fix the tests.** `tests/services/test_consistency.py:91-135` must use real keys, plus
  a case for the legacy-gateway exemption and a case proving an unknown key fails loudly.

  ### Pre-merge check (was "blast radius", now much smaller)

  Count how many hotels the corrected rule flags via `HotelConfigHealthService._check_consistency`
  — that's the only layer where it does real work, and it runs fleet-wide, so legacy-gateway
  hotels are the false-positive risk. If they dominate, that decides step 3 toward the
  derived-setting option. No startup risk to check: verified that no current tree can trip it.

  ### Out of scope

  - Blocking mode on the config-save path (`signals.py` is warn-only by design).
  - Tree definitions for ESA / Four Seasons / Drury (`MSA_HOTEL_PROVIDERS` has only
    Wyndham Connect GMS) — separate thread item.
  - Template/named-config packages (the entity-shaped-data gap Joshua raised).

  ### Acceptance criteria

  - A rule referencing a key outside the generated keyspace fails loudly, with a test.
  - A decision is recorded on `ANY_NON_NULL` handling, and the tree layer's behaviour for
    presence rules is either fixed or explicitly documented as out-of-scope-by-design.
  - The corrected rule errors for a tokenizing hotel with no check-in gateway config, and
    does not error for a legacy FreedomPay/Shift4 hotel.
  - `ConformityService.finalize()` still succeeds for all registered trees.

  ---

  ### Notes for you

  - Nothing created in Linear, nothing posted to Slack. Both need your say-so.
  - Correction to what I told Joshua: I said the rules are "warn-only at this time / treat
    as the linter layer". The warn-only half is right (`signals.py` uses `messages.warning`).
    The "linter layer" half oversells it — for null-presence rules the CI layer can't fail,
    and the save path only covers tree-matched hotels. If he's planning against "the linter
    catches this in CI", that's worth correcting in-thread before he builds on it. This is
    now the most useful thing in the follow-up, more than the typo fix itself.
  - Tests not run; analysis only, no code changed.

  ---

  ## Agent run 2026-08-10T14:14Z — final ticket drafted

  Clean ticket text (investigation narration stripped, code references kept) written to:
  `/private/tmp/claude-501/-Users-garethlloyd-projects-canary/bbcf9e22-2c3d-4f54-934c-1a0d6f3d3f7f/scratchpad/linear-ticket-consistency-rules.md`

  Title: "Consistency rules can't express null-presence invariants;
  `payment_gateway_required_for_tokenization` is dead and proves it"

  Structure: Summary → Problem 1 (dead rule) → Problem 2 (CI layer can't fail
  null-presence rules) → what's already enforced → 4 scope items → pre-merge check →
  out of scope → acceptance criteria → references.

  Still NOT created in Linear — needs your approval plus a team/project. Scratchpad is
  session-temporary, so if it isn't filed soon, copy it somewhere durable.
project: 2026-04-10T0840-ticket
source_id: https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1785956358642849?thread_ts=1785950349.523259&cid=C047K6WSUJY
tags:
- morning-gtd
- slack
time_minutes: 10
title: 'Follow up on: fix payment_gateway_required_for_tokenization referencing a
  dead field'
updated: 2026-08-12 13:47:30.516066
waiting_on: null
waiting_since: null
working_on: true
---

I parked my own reply in #epd-enterprise on Aug 5: told Joshua the consistency rules are the linter layer, and "Good catch on payment gateay. We'll fix that." payment_gateway_config_id doesn't exist so the rule can't fire.
https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1785956358642849?thread_ts=1785950349.523259&cid=C047K6WSUJY

Output should be a draft linear ticket ready for prioritization.