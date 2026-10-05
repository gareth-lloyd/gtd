---
area: null
completed_at: 2026-10-02 16:26:14.365640
contexts: []
created: 2026-10-01 13:33:37.867580
defer_until: null
due: 2026-10-02
energy: null
id: 2026-10-01T1333-review-decision-review-of-the-binding-rules-tree-p
order: null
output: |
  ## Agent run 2026-10-01 — decision review of the Binding Rules Tree prototype

  - PR: [#58570 [ENT-7614] Binding Rules Tree prototype](https://github.com/canary-technologies-corp/canary/pull/58570) (draft, closed unmerged 2026-10-01; 44 files, +3927/−345, about 770 added lines are generated stub overloads)
  - Spec: [Binding Rules Tree design doc](https://app.notion.com/p/3e58146861518147b489e3fa8e8aef09)
  - Ticket: [ENT-7614](https://linear.app/canary-technologies/issue/ENT-7614)
  - Claude Code session: `binding-review`

  **Status:** agenda built, walk paused at Decision 1/11 awaiting a verdict (accept · reject · discuss · flag). Nothing has been posted to GitHub, Notion or Linear.

  Verdicts are read as: **accept** means the doc should adopt the prototype's choice, **reject** means the prototype should go back to the spec. Line numbers refer to the PR head, not local master.

  ### Where the PR departs from the spec

  - **Authoring API:** the spec has `with ConformityService.defining_binding_rules():` plus `GROUP.define(key, OverridePolicy.BINDING, …)`. The PR uses `BindingRulesService.define(scope, key, constraint, authority=, explanation=, default=)` and splits `ConformityService` into definition, binding and resolution services.
  - **Conflicts are not boot errors:** the spec's E003 is a Warning (W003) in the PR, from a static scan that resolves neither tree and so over-reports. Real conflicts come from a new `report_binding_conflicts` command, and at runtime the rule wins over the brand value, which the spec says never happens.
  - **Predicates are binding-only:** brand defines reject predicates other than `ANY_NON_NULL`, where the spec widens every define to `T | Predicate[T]`.
  - **Public reads are only partly merged:** `get_all_setting_values…` and `get_final_setting_values…` stay brand-only. `get_setting_value…` returns the predicate object for constraint-only or conflicting keys, not the seeded default.
  - **Scope of the first rules:** the EU ID rule excludes both Italy and Spain, and there is no `ES_ID` exception. The retention reader imports `gdpr.services.retention` directly, which the spec says the engine should not do.
  - **Not in the PR:** `AllOf` and the cross-authority conjunction (equal-weight overlap raises the tie error instead); the authority-matches-subpackage guard and the registration-time predicate type check; `_constrained_setting_keys` and the `drift.py`, `signals.py` and `stored_hotel_attributes.py` changes; `explain()` and the CODEOWNERS lines.
  - **Beyond the spec:** hotel-aware sibling candidacy (`_subtree_yields`, ENT-7699), and the `GroupAttributes.__post_init__` check moved to registration so the empty binding root is allowed.

  ### Agenda

  | # | Decision | Kind | Door | Dependents |
  |---|---|---|---|---|
  | 1 | A brand/law conflict is resolved at runtime (rule wins), not a boot error | Behavioral | one-way | 3, 5, 9 |
  | 2 | Three services and a separate `BindingRulesService.define()` authoring API, not `GROUP.define(…, BINDING)` in a context manager | Structural / Contract | one-way | 6 |
  | 3 | Public reads are only partly merged, and `get_setting_value…` can return a predicate | Contract | one-way | 4 |
  | 4 | Real rules are registered and enforced through existing callers, for hotels without the product too (implicit) | Scope / Behavioral | two-way | 0 |
  | 5 | Static detection is an unresolved, over-reporting scan (W003) plus a per-hotel report command | Tradeoff | two-way | 0 |
  | 6 | Predicates are binding-only; brand defines keep plain values | Contract | two-way | 0 |
  | 7 | Binding precedence has no cross-authority conjunction; overlap at equal weight is a tie error and nesting must be contained | Behavioral | two-way | 0 |
  | 8 | Retention reader is registered from the rule module and imports `gdpr`; a `None` effective value violates the cap | Dependency / Behavioral | two-way | 0 |
  | 9 | First rules cover the EU minus Italy and Spain, with no `ES_ID` exception | Scope | two-way | 0 |
  | 10 | The ENT-7699 resolution change (`_subtree_yields`) rides in this PR | Scope | two-way | 0 |
  | 11 | Minor batch: empty `GroupAttributes()` root, finalize lifecycle, predicate details, explanation precedence, tests against real trees | mixed | two-way | 0 |

  ### Decision 1/11 — A conflict is resolved at runtime, not a boot error

  [Behavioral · one-way door · 3 dependents]

  - **CHOSE:** a brand value the binding rule refuses does not fail boot. `finalize()` accepts it; `merge()` (`services/conformity.py:1039`) returns an entry with the rule's constraint, policy `BINDING` and the conflict attached; `hotel_conforms` then tests the hotel against the rule and ignores the brand value.
  - **INSTEAD OF:** the spec: "conflicts are boot errors, never runtime overrides", with E003 failing `manage.py check` on the PR that adds the rule.
  - **RESTS ON:** nothing (root).
  - **SUPPORTS:** 3 (what reads return for a conflicting key), 5 (the check can be a warning), 9 (whether country carve-outs are still needed).

  **My read:** the prototype is right about the runtime behaviour, but it gives up the gate without replacing it.

  - **Why rule-wins is sound:** the conflicts already exist (IHG Italy, IHG Spain, Wyndham Spain under a Spanish exception). Under the spec, a law cannot ship until a brand edits its config, and the workaround is to carve countries out of the legal scope, which leaves independents there uncovered.
  - **What is lost:** goal 3 says a conflict is found at boot. A Django `Warning` is not a gate unless CI fails on warnings, so a new conflicting brand define can now merge unnoticed.
  - **The rule only wins in `hotel_conforms`:** `get_all_setting_values…` still returns the brand value, and `apply_portfolio_settings` writes from it. A conflicted hotel would have the brand value written and then be flagged by drift, with no state that satisfies both.
  - **The prototype does not rely on its own choice:** it still carves out Italy and Spain (decision 9), which is the workaround rule-wins was meant to remove.

  Recommendation: accept the runtime semantics and add a hard gate, a CI test that resolves both trees per country and fails on any conflict not in an explicit allowlist.

  ### Production callers the remaining decisions touch (master)

  - `monitoring/services/monitored_hotel_state.py:65` and `rules_based_configuration/services/drift.py:171` call `hotel_conforms(final_only=True)`, which now includes binding constraints.
  - `rules_based_configuration/services/drift.py:182` and `internal_support/views/config_drift.py:128` call `get_setting_value_for_hotel_attributes`, which can now return a predicate object.
  - `rules_based_configuration/management/commands/apply_portfolio_settings.py:107` calls `get_all_setting_values_for_hotel_attributes`, which stays brand-only.
  - `rules_based_configuration/signals.py:54` and `rules_based_configuration/services/hotel_config_health.py:137` call `validate_hotel_on_save`, which no longer returns `None` for an independent hotel inside a binding scope.

  ### Not read

  - The generated per-key overloads in `conformity.pyi` (skimmed only).
  - The three diagrams embedded in the Notion page.
  - No tests were run; the PR branch is not checked out locally.
project: 2026-04-16T1351-ship
source_id: null
tags: []
time_minutes: null
title: 'Review decision review of the Binding Rules Tree prototype (PR #58570)'
updated: 2026-10-02 16:26:14.365630
waiting_on: null
waiting_since: null
working_on: false
---

Decision review of https://github.com/canary-technologies-corp/canary/pull/58570 against the Binding Rules Tree design doc (https://app.notion.com/p/3e58146861518147b489e3fa8e8aef09).

The walk is paused at Decision 1 of 11, awaiting a verdict. The agenda and the first decision are in the agent output. Claude Code session: binding-review.