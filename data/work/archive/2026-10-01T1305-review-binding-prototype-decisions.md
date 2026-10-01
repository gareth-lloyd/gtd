---
area: null
completed_at: 2026-10-01 14:33:20.997987
contexts: []
created: 2026-10-01 13:05:40.458797
defer_until: null
due: null
energy: null
id: 2026-10-01T1305-review-binding-prototype-decisions
order: null
output: |
  ## Agent run 2026-10-01T13:05

  Architecture review of the Binding Rules Tree prototype, [PR #58570](https://github.com/canary-technologies-corp/canary/pull/58570) (closed draft, "Not for merge"), judged against the [Binding Rules Tree spec](https://app.notion.com/p/canarytechnologies/Binding-Rules-Tree-3e58146861518147b489e3fa8e8aef09) (ENT-7614). Three questions were asked: which architecture decisions drove the design and what the alternatives are; what would make the work iterative instead of one wide PR; and which designs would touch the generated `conformity.pyi` less.

  The blast radius came from three choices the binding mechanism doesn't need: the three-service split, rerouting the shared read entry points in the same PR that registers rules, and putting all new code in the one module that is stubbed. All three are separable, and the stub cost drops from +770 lines to about 5–20.

  How this was produced: three subagents (stub impact, sequencing and blast radius, and an unanchored design from spec plus master only). I verified the stale-master, earlier-commit, retention-test and dependency claims myself; everything else is from the subagent reports. The unanchored design agent read the local `master`, which was 132 commits behind `origin/master`, so its `file:line` references and one of its arguments are dated (noted in decision 1).

  ### The decisions

  1. **Binding tree as a second `ConformityDiamondTree` with a match-everything root.** The alternative is a flat registry of scoped rules ordered by containment.
     - Keep the tree: it costs about 15 lines for the root plus a ~30-line `resolve_defining_groups` extraction, and later non-nested scopes (PMS, capabilities) will need weights or conjunction anyway.
     - The unanchored agent preferred flat, but partly because sibling resolution was broken on the master it read; [#57673](https://github.com/canary-technologies-corp/canary/pull/57673) has since fixed that on `origin/master`.

  2. **Merge wired into `hotel_conforms`, `validate_hotel_on_save` and `get_setting_value_…`.** The alternative is a sidecar: a parallel merged-read API that callers opt into one at a time.
     - This is the decision to change. The merge and conflict scan are already module-level functions over two frozen artefacts, so a sidecar is feasible.
     - Only the spec's "every public read goes through the merge" forces the coupling, and the PR already departs from it for two reads (`get_all_setting_values_…` and `get_final_setting_values_…` stay brand-only). The spec would need amending.

  3. **Three-service split** (`ConformityRulesDefinitionService`, `BindingRulesService`, resolution-only `ConformityService`). The alternative is to leave `ConformityService` alone, or split later.
     - Defer it. Commit `da4661a2ec5` has the whole mechanism in one service with `_ROOTS` intact, and the split is not in the spec.
     - The split accounts for nearly all 345 deletions and nearly all the modified existing tests.

  4. **Separate `BindingRulesService.define`, with predicates rejected in brand defines.** The alternative is the spec's `GROUP.define(key, BINDING, predicate)` with `T | Predicate[T]` everywhere.
     - Keep the PR's choice and update the spec. It makes `authority` and `explanation` statically required and keeps predicates out of brand configs.

  5. **Conflicts as warning W003 plus runtime "rule wins".** The alternative is the spec's boot error E003.
     - Warning-first is right as a stage, since Italy and Spain conflict with IHG today, with E003 as the end state once master is clean.
     - Neither agent found a `manage.py check` step in CI, so the PR-time gate would have to be a pytest over the real registry.

  6. **Engine imports `gdpr` for the retention reader.** The alternative is inverted registration: `gdpr` registers its reader through the existing `configuration_rules` autodiscovery.
     - Invert it. The PR adds a `rules_based_configuration → gdpr` edge, and `gdpr` already depends on `check_in`, which depends back on the engine (the engine and `check_in` already depend on each other).
     - The retention rule isn't ready regardless: the reader returns `None` for a German hotel with no override, so `AtMost(455)` flags all of them. The PR's own test asserts this (`test_hotel_conforms__flags_a_german_hotel_that_is_never_swept`).

  7. **One PR for the spec's releases 1 and 2, plus ENT-7699.** Fine for a prototype marked "Not for merge", but ENT-7699 already has its own open PR ([#58556](https://github.com/canary-technologies-corp/canary/pull/58556)), which this one duplicates.

  ### A more iterative sequence

  With zero rules registered, only ENT-7699 changes behaviour on deploy. Everything else becomes live once the first rules register, and the PR registers them in the same change.

  | # | Contents | Size | Inert on deploy | Gate |
  |---|---|---|---|---|
  | 0 | ENT-7699 via #58556 | +98/−4 | No (bugfix) | Own review |
  | 1 | `resolve_defining_groups` extraction | ~30 | Yes | Existing tests |
  | 2 | `predicates.py`, `ANY_NON_NULL` as a predicate | ~150 | Yes | Existing tests |
  | 3 | Allow a match-everything root | ~15 | Yes | — |
  | 4 | Binding service in its own module, zero rules | ~250 | Yes | — |
  | 5 | Merge, conflict scan, W003, report command, no caller rerouted | ~200 | Yes | W003 as warning |
  | 6 | First ID rules registered | ~80 | Yes for hotels | Report command gives the blast-radius counts |
  | 7–9 | Opt in one caller per PR: admin-save and health, then monitoring, then drift | ~20–40 each | No | Feature rollout or `@isolate` |
  | 10 | Retention rule | small | No | After the `None` question is settled |
  | 11 | W003 becomes E003 | one line | No | Master clean |

  Sizes are estimates from the diff tallies, excluding tests. The split, if still wanted, goes last as a mechanical refactor. `FeaturesService.get_feature_rollout`, `@isolate` and GrowthBook all exist in the repo for steps 7–9.

  What goes live once rules register in the PR as written (from the sequencing report, not all re-verified):
  - `validate_hotel_on_save` runs for in-scope independents, which produces admin-save warnings and `has_standard=True` in config health.
  - `get_setting_value_for_hotel_attributes` returns a `Predicate` object to `drift.py` and `config_drift.py` when no brand value stands; both `str()` it, so the text changes shape but nothing crashes.
  - `hotel_conforms` creates a `CheckInConfiguration` for EU hotels without check-in, and reports them non-conforming because the model default is `REQUIRED`.
  - `final_only=True` now includes every constraint, so `monitored_hotel_state.py` can turn UNHEALTHY and drift writes binding keys to `StoredHotelAttributes.drifts`.

  ### The stub

  The stub is `pyrefly stubgen` over the whole of `conformity.py`, with an exact-text staleness check in CI (`.github/workflows/canary_back_end_django.yml`). Anything public added to that module lands in the stub; code in any other module adds nothing.

  Of the +770 lines, 584 (76%) are the second set of 53 overloads for `BindingRulesService.define`, and about 160 are new classes that appear only because they live in `conformity.py`.

  | Option | Stub impact | Static safety |
  |---|---|---|
  | New code in separate modules, type check at registration | About 5–20 lines | No IDE error or key autocomplete on binding defines; errors at import |
  | Same, plus a separate generated binding stub | New ~600-line file, one-off | Same as the PR |
  | Spec's approach: widen the existing 53 overloads | +118/−53 one-off, no doubling | Brand defines accept predicates; `authority` not statically required |
  | `SettingKey[T]` constants with one generic signature | Replaces ~950 lines of overloads and aliases | Same as today, but 551 `.define(` call sites to migrate |
  | Typed keys for binding only | Brand overloads untouched; ~110–210 lines elsewhere | Keeps the PR's guarantees |

  Recommendation: the first row. There are three binding call sites today, and 584 stub lines is a poor price for checking three calls statically. The registration check is not free, though: the field type data is sometimes a string such as `"list[CardNetworks]"`, and predicates have no uniform way to expose their values.

  Side effects in the PR's regenerated stub: `BindingRulesService.ROOT` is a bare `Final` and comes out untyped for callers; `BindingRule` and `MergedEntry` constructor arguments are typed `Incomplete`, so they are unchecked.

  ### Spec amendments this implies

  - Reads opt in to the merge one caller at a time, replacing "every public read goes through the merge".
  - Binding rules are authored through their own `define`, and brand defines stay plain values.
  - Brand-vs-binding conflict starts as a warning and becomes a boot error once master is clean.
  - The `gdpr` reader is registered from the `gdpr` side.
  - The German retention rule waits on a decision about what `None` means.
  - The first EU ID scope excludes Spain as well as Italy.

  ### Not verified

  - Where a Django system-check warning would surface in CI: no `manage.py check` step was found.
  - Step sizes in the sequence table.
  - Stub findings were checked against pyrefly 1.1.1 only, not pyright.
project: null
source_id: null
tags: []
time_minutes: null
title: Review binding prototype decisions
updated: 2026-10-01 14:33:20.997977
waiting_on: null
waiting_since: null
working_on: false
---