---
area: null
completed_at: 2026-11-20 15:06:11.078380
contexts: []
created: 2026-11-19 22:48:35.309818
defer_until: null
due: null
energy: null
id: 2026-11-19T2248-action-the-review-findings-on-ent-7726-pr-59059
order: null
output: |-
  ## Agent run 2026-11-20T13:12

  Findings 1, 2, 3, 4, 6, 9 and 10 are actioned in the worktree `.claude/worktrees/ent-7726` for PR #59059 (https://github.com/canary-technologies-corp/canary/pull/59059). Nothing is committed or pushed: the changes sit uncommitted beside the earlier four fixes. Finding 5 needs your wording decision; 7 and 8 are left as they are.

  ### What changed

  - **Findings 1, 2, 4 (one fix):** `ConformityService.get_explanation_for_hotel_setting` now takes the hotel's merged entries instead of its attributes. Rule reasons come from `entry.binding_rules`; the brand reason is given only when `entry.brand_group` is set. `None` entries (attributes could not be fetched) give the generic every-hotel text; a key with no entry gives no explanation. The private view helper `_explanation` is gone, and the views, the admin and drift detection all call the one method.
  - **Finding 3:** the admin `drifts_display` catches the `ValueError` from the attribute fetch and falls back to the generic text, as the views do.
  - **Finding 6:** `_ack_item` and `_drift_item` no longer take `hotel_attrs`, so the silent `None` default is gone. New view tests assert the explanation for a bound hotel, an unbound hotel and a hotel with no attributes, on the list schema, the detail schema and the acknowledgement list endpoint. A new admin test covers both the fetched and the failed-fetch case.
  - **Finding 9:** `_free_brand_predicate` and `_final_brand_predicate` take the predicate, the group and (for FINAL) the default, not the whole `brand`.
  - **Finding 10:** confirmed. With the fix-4 ordering reverted, `test_validate_hotel_on_save__reports_the_final_brand_value_when_a_rule_is_broken_too` fails; the fix was then restored.
  - New service test for finding 1: a Days Inn hotel no longer gets the reason Super 8 registered for the same key.

  ### Verification

  - 2,318 tests passed across `rules_based_configuration`, `internal_support` and `monitoring`. After `ruff format` touched two files, the four edited test files were rerun: 151 passed.
  - `ruff check` is clean and `pyrefly` reports 0 errors on the eight changed files. The full-project `pyrefly` step of `make check-fix` still does not cover this worktree and was not run.
  - Finding 1 was not reproduced against the old code; the new test pins the new behaviour only.

  ### Cost of the list view (finding 7)

  The drift list now resolves merged entries once per row. Measured locally against the real trees: 0.38 ms per Wyndham hotel (61 keys) and 0.30 ms per IHG hotel (33 keys), so about 0.4 s at the 1,000-row cap. This branch registers no binding rules, so the figure will rise as rules are added. No query-count assertion was added; the list still relies on `select_related("hotel")` for the attribute fetch.

  ### Decision for you: finding 5 (staff-facing wording)

  Untouched. The text still reads `law: German retention law. Brand standard.` per hotel and `law (countries:DE): ...` in the glossary. My recommendation: keep the authority prefix, replace `countries:AT,BE,...` with country names in the glossary text only, and join reasons with a line break or ` | ` rather than a space. Say which you want and it is a small change in `get_explanation_for_setting` and `_joined_reasons` plus the pinned test strings.

  ### Still open

  - Brand reasons are stored per key, not per `(group, key)`. A hotel whose brand tree resolves the key now gets a brand reason, but it can be the text another group registered for that key. I did not change this because it also changes behaviour: a child group that redefines a key without an explanation would lose its parent's text.
  - Finding 8 (`get_explanation_for_setting` raises before `finalize()`): left, tests and scripts only.
  - The three first-review items with no proposed fix (entries recomputed in the drift paths, dead read paths in `conformity.py`, duplicated path enumeration in `boot_checks.py`) are untouched. `drift.py` still computes merged entries twice per drifted hotel.
  - Next step once you are happy: commit and push to `glloyd/ent-7726-merge-and-boot-checks`, then merge up the stack (#61725, #61724, #63320 are based on it).

  Handoff this run worked from: `/Users/garethlloyd/.claude/plans/zippy-soaring-metcalfe.review-handoff-2026-11-19.md`

  ## Agent run 2026-11-20T13:40

  Brand reasons are now stored per (group, setting), per the approved plan `/Users/garethlloyd/.claude/plans/plan-the-fix-for-synthetic-knuth.md`. Still uncommitted in `.claude/worktrees/ent-7726` for PR #59059 (https://github.com/canary-technologies-corp/canary/pull/59059). This closes the first "Still open" item of the previous run.

  - A hotel gets the reason of the group whose definition wins for it. If that group gave no explanation the hotel gets no brand reason (no inheritance, your decision).
  - The glossary and the no-attributes fallback list every group's reason, labelled with the group, e.g. `parent_brand_id:EXTENDED_STAY_AMERICA: Printing is deliberately off for this brand. parent_brand_id:FOUR_SEASONS: Every active property prints...`. The label is `GroupAttributes.__str__`, so it joins the finding-5 wording decision.
  - Changed: `rules_based_configuration/services/conformity.py`, `rules_based_configuration/testing.py`, `tests/services/test_conformity.py`. No view, admin, frontend or API-shape change.

  Verification:

  - 2,321 tests passed across `rules_based_configuration`, `internal_support` and `monitoring`. `ruff` clean, `pyrefly` 0 errors on the changed files, `manage.py check` clean.
  - Against the real configs in a local shell: an ESA hotel and a Four Seasons hotel each get their own text for `can_print_authorization_form`; an IHG GMS Core hotel gets no brand reason for `integration_auto_post_to_pms` or `has_e_folio` (it used to get Wyndham's and the IHG pilot's); a Wyndham Connect GMS hotel keeps Wyndham's.
  - Behaviour change to expect: 24 settings are defined by more than one group, so some hotels lose a brand reason that was never theirs, and the glossary text for those settings gets longer.

  ## Agent run 2026-11-20T14:30

  After a `/code-review` of the uncommitted tree, three follow-ups you asked for are applied (still uncommitted, PR #59059 https://github.com/canary-technologies-corp/canary/pull/59059):

  - Glossary text is back to plain brand reasons: no group label, each distinct reason once. Rule lines keep their authority and scope prefix.
  - A hotel whose attributes cannot be fetched gets no explanation (it used to get the every-hotel text).
  - Read paths cut: `ConformityService.get_setting_value_for_hotel_attributes`, `ConformityService.matching_rules`, `ConformityService.surviving_rules`, and the tree's `get_final_setting_values_for_hotel_attributes` are deleted. The tree's single-setting read now goes through `resolve`, so there is one resolution walk. `hotel_conforms` uses `get_final_entries_for_hotel_attributes`.
  - Kept: `get_all_setting_values_for_hotel_attributes` has no production caller but 111 call sites in the config tests.

  Verification: 2,321 tests passed across the three apps; `ruff` clean; `pyrefly` 0 errors on the changed source files.

  Open, needs your decision:

  - Per-group brand reasons blank explanations IHG hotels used to show: 19 of 27 FINAL settings for IHG GMS Core, 10 for IHG Pilot (review probe on the real configs). Options: add `explanation=` to those defines; fall back to the setting-level text when only one distinct reason exists for the setting (my recommendation, no config edits); or revert per-group storage.
  - When merging up the stack: `tests/rules/test_live_registry.py` in #61725 calls one of the removed `ConformityService` wrappers and needs repointing to the registry.
  - Review nits not actioned: drift list fails whole on a non-ValueError from resolution; admin repeats the views' fetch-and-merge fallback; drift detection merges entries twice; the new view and admin tests patch `fetch_hotel_attributes_for_hotel`.

  ## Agent run 2026-11-20T14:50

  Per-group brand reasons are reverted at your request: brand reasons are stored per setting again, so the IHG explanations are back. This supersedes the 13:40 run and closes the open decision in the 14:30 run. Known and accepted: a hotel whose tree resolves a setting can still see text another group registered for it (ESA and Four Seasons share one reason for `can_print_authorization_form`).

  Kept from the earlier runs: explanations built from the merged entry, no explanation when attributes cannot be fetched, the admin guard, the merge helper signatures, and the dead read-path cut. 2,318 tests passed across the three apps; `ruff` clean; `pyrefly` 0 errors on `conformity.py`. Still uncommitted on PR #59059 (https://github.com/canary-technologies-corp/canary/pull/59059).
project: null
source_id: null
tags: []
time_minutes: null
title: 'Action the review findings on ENT-7726 PR #59059'
updated: 2026-11-20 15:06:11.078367
waiting_on: null
waiting_since: null
working_on: false
---

PR: https://github.com/canary-technologies-corp/canary/pull/59059

Worktree: `.claude/worktrees/ent-7726` (fixes are uncommitted in the working tree)

Handoff file: `/Users/garethlloyd/.claude/plans/zippy-soaring-metcalfe.review-handoff-2026-11-19.md`

## Agent output

# Handoff: review findings on the uncommitted ENT-7726 changes

Written 2026-11-19. Branch `glloyd/ent-7726-merge-and-boot-checks` (PR #59059), worktree `.claude/worktrees/ent-7726`.

## Where things stand

The working tree holds four uncommitted fixes from the first review of the PR. A second review of those fixes produced the findings below. None of the findings has been acted on except the missing test (finding 10).

| Fix | What it did | Files |
|---|---|---|
| 9 | Keyword-only arguments on `merge()` and its helpers | `services/merge.py`, callers, tests |
| 10 | `Any` replaced by `object` in `merge.py` and `_satisfies` | `services/merge.py`, `services/conformity.py` |
| 3 | Rule explanations surfaced; brand reason gated per hotel | `services/conformity.py`, `services/drift.py`, `admin.py`, `internal_support/views/config_drift.py` |
| 4 | A broken FINAL brand value is reported before a broken constraint | `services/conformity.py` |

Verification of the working tree:

- 2,304 tests passed across `rules_based_configuration`, `internal_support` and `monitoring`, before the last test was added.
- After adding the finding-10 test, only `test_conformity.py` was rerun: 65 passed.
- `ruff` is clean. `pyrefly` reports 0 errors on the changed files.
- The full-project `pyrefly` step of `make check-fix` matches no files in this worktree, so it has not run.

## Findings

Confidence is how sure I am the finding is true as stated. "Reproduced" means a test or a run showed it; otherwise it comes from reading the code.

### On fix 3 (explanations)

| # | Finding | Location | Confidence | Basis |
|---|---|---|---|---|
| 1 | The brand reason can come from a group that does not bind the hotel. The gate checks whether the hotel's tree defines the key anywhere, not whether a group on the hotel's path does. | `conformity.py`, `get_explanation_for_hotel_setting` | High | `setting_keys_in_subtree[root]` holds every key in the tree. Not reproduced. |
| 2 | The per-hotel explanation recomputes what `MergedEntry.binding_rules` and `brand_group` already carry. Three callers hold the entry and ignore it. | `conformity.py`, `drift.py`, `config_drift.py` | High that the duplication exists. Medium that the two paths disagree in practice. | Read from code. |
| 3 | The admin `drifts_display` fetches attributes with no guard. A `ValueError` from the fetch makes Django render the field empty, hiding drifts the hotel has. | `admin.py:240` | Medium | Depends on Django's read-only field swallowing `ValueError`, and on a stored row holding a value the enums reject. Neither was reproduced. Stored enum values have been corrupted before (repaired 2026-06-11), so the input is plausible. |
| 4 | The "no attributes, use the generic text" rule lives in a private view helper. The views, the admin and drift detection each handle missing attributes differently. | `config_drift.py`, `_explanation` | High | Read from code. A design finding, not a defect. |
| 5 | Staff-facing text exposes internals: the raw authority value, `Scope.__str__` (`countries:AT,BE,...`), superseded rules beside their replacements, and reasons joined by a bare space. | `conformity.py`, `get_explanation_for_setting` | High | One test pins the string `law (countries:DE): German retention law. Brand standard.` Whether this is acceptable is a wording decision for Gareth. |
| 6 | No view test asserts an explanation value. `_ack_item` defaults `hotel_attrs` to `None`, so a caller that omits it silently gets the generic text. | `config_drift.py`, `internal_support/tests/views/test_config_drift.py` | Medium to high | A grep of the view tests for `explanation` found nothing. The mutation the reviewer describes was not tried. |
| 7 | The drift list builds attributes per row. It costs no extra query only because `select_related("hotel")` primes the reverse one-to-one cache. | `config_drift.py`, `HotelDriftListSchema.from_model` | Medium | Reasoned from Django internals. No query count was asserted. No defect today. |
| 8 | `get_explanation_for_setting` raises `RuntimeError` before the registry is finalized, where it used to return `None`. | `conformity.py` | High, reproduced | One test failed for this reason and needed a `finalize()` call. Production always finalizes at startup, so the impact is on tests and scripts only. |

### On fixes 9 and 10

| # | Finding | Location | Confidence | Basis |
|---|---|---|---|---|
| 9 | `_free_brand_predicate` and `_final_brand_predicate` take `suggestion` / `requirement` as well as `brand`, so the same predicate is passed twice and nothing ties the two together. | `merge.py` | High | I introduced this to carry the `isinstance` narrowing once `BrandResolution.value` became `object`. Low severity: both callers are in `merge()`. |

### On fix 4

| # | Finding | Location | Confidence | Basis |
|---|---|---|---|---|
| 10 | No test pinned the reordered `expected_value`. | `test_conformity.py` | Resolved | The test was reported as added but had not been; the command that wrote it was refused. `test_validate_hotel_on_save__reports_the_final_brand_value_when_a_rule_is_broken_too` now exists and passes. It was not run against the pre-fix code, so it is unconfirmed that it fails without the fix. |

## Recommended next step

Findings 1, 2, 4 and 7 share one fix: build the per-hotel explanation from the merged entry, behind one service method that also accepts missing attributes.

- Rule reasons come from `entry.binding_rules`.
- The brand reason is given only when `entry.brand_group` is set.
- Cost: the drift list and the admin page need merged entries per hotel, which is one tree resolution per row. The list is capped at 1,000 rows. Unmeasured.
- Still open after that: brand reasons are stored per key, not per group, so the text can be another group's even when `brand_group` is set. Storing reasons per `(group, key)` closes it.

Alongside it:

- Finding 3: guard the admin fetch the way the views do.
- Finding 6: add view tests that assert the explanation on both branches.
- Finding 9: pass the helpers the predicate, group and default instead of the whole `brand`.
- Finding 5: needs a wording decision before any change.

## Decisions already made

- Rejected by Gareth: a fallback for hotels with no `HotelAttributes` (not an important case), and avoiding config-row creation during the `getattr` traversal (known and accepted).
- First-review finding 5 (boot check resolves every tree key): Gareth is unsure. Measured at about 175 ms per process start with one 27-country rule on a key in each real tree (Wyndham 129 ms, IHG 45 ms). Recommendation: skip for now.

## Not yet addressed from the first review

- Merged entries are recomputed in the drift paths (`drift.py`, `drift_acknowledgement.py`, `config_drift.py`).
- Dead and duplicated read paths in `conformity.py`: `get_final_entries_for_hotel_attributes` has no production caller, and `hotel_conforms` repeats its filter inline.
- `root_to_node_paths` in `boot_checks.py` repeats the path enumeration in `get_all_possible_setting_combinations`.

No fix has been proposed for these three.