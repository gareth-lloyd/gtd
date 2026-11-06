---
area: null
completed_at: 2026-11-05 16:11:13.855727
contexts:
- react
created: 2026-11-05 14:03:27.149951
defer_until: null
due: null
energy: medium
id: 2026-11-05T1403-reply-on-ent-7726-should-martin-attempt-the-gjm-re
order: null
output: |
  ## Agent run 2026-11-05T13:01Z

  Nothing was posted. Draft reply below for you to paste on ENT-7726 (https://linear.app/canary-technologies/issue/ENT-7726/implement-binding-rules-tree-prototype#comment-fcb5f0f2).

  ### What Martin asked (2026-11-04)
  Linear comment fcb5f0f2: should he attempt the GJM reader as part of the eng design, or do you already have an idea to fold into your PRs? He notes the value reader can only attach to a real column. Follow-up a9478da3 links PR #61725 thread r4471587063 (https://github.com/canary-technologies-corp/canary/pull/61725#discussion_r4471587063): `ValueReaderRegistry.add` requires an existing hotel field, so a column-less reader-only setting cannot register; `message_use_cases` has no column.

  ### Verified facts
  - Martin is right. In `.claude/worktrees/ent-7726-rules` `services/value_readers.py:30` rejects any setting not in `SettingTypeGeneratorService.get_fields_by_setting_key()`, and `services/conformity.py:949` `get_actual_hotel_setting` raises ValueError for any key not starting with `hotel.`. A column-less `guest_journey.message_use_cases` cannot exist in the stack as built.
  - Your plan (~/.claude/plans/zippy-soaring-metcalfe.md, "PR 6: settings backed by a reader (not agreed)") already sketches exactly this work and marks it not discussed. Your Notion high-level proposal (https://app.notion.com/p/3f9814686151813da661eb802029d0eb, WIP, Martin is the reviewer) says the same and calls itself "not a full eng design". So the natural answer is: Martin owns the column-less reader in his eng design; the ENT-7726 stack stays column-backed.
  - Two related Martin review comments on #61725 feed into this: r4471586474 (conformity.py:1094, `HotelValidationResult` returns raw `actual_settings` while the compare used the reader value; https://github.com/canary-technologies-corp/canary/pull/61725#discussion_r4471586474) and r4471586788 (conformity.py:989, column-less key has no column to read; does `get_actual_hotel_setting` degrade to `NO_VALUE_DEFINED`? Answer today: no, it raises; https://github.com/canary-technologies-corp/canary/pull/61725#discussion_r4471586788).
  - Separate top-level question from Martin on #61725 (2026-11-04T18:27:48Z): #61724 and #61725 are siblings off #59059 (confirmed: both base `glloyd/ent-7726-merge-and-boot-checks`) and `predicates.py` has diverged, with `SupersetOf` and the `AllOf` candidate fix only in #61724. He asks the intended merge order. Not answered here; note that GJM's design needs `SupersetOf`, which lives in the conventions PR.

  ### Draft reply for Linear
  Yes, please take the GJM reader in your eng design. You're right about the gap, and it's deliberate for this stack: `ValueReaderRegistry.add` only accepts a key that is a real hotel field, and `get_actual_hotel_setting` raises on anything that doesn't start with `hotel.`. The retention reader in #61725 replaces a column's value in the comparison only, and I don't want to widen a stack that's already four PRs deep to carry a column-less setting nobody has agreed yet.

  What I'd want the design to settle (the PR 6 sketch in my proposal is a starting point, not a decision):
  - A declared reader setting (`ReaderSetting`, registered via something like `ConformityService.declare_reader_setting`) sitting beside the column readers in `value_readers.py`. The unknown-key check in `add` is the seam.
  - Key prefix outside `hotel.` (`guest_journey.message_use_cases`), predicates only (`SupersetOf`, `SubsetOf`, `NoneOf`, `Empty`, `AllOf` of those), no plain value, no `default=`, allowed items declared with the setting and checked at define time.
  - Audit every caller that assumes `hotel.`: `get_actual_hotel_setting` / `get_all_actual_hotel_settings` (your r4471586788: they raise today, and should skip or return `NO_VALUE_DEFINED` for reader-only keys), `admin.py`, `get_final_setting_keys`, the drift glossary, `hotel_comparison.py`, `consistency.py`, `drift.py`, `hotel_config_health.py`, and `apply_defaults` in PR 5, which must skip reader keys.
  - Brand resolution stays winner-takes-one; IHG's additive set is the open question (nine new nodes or a conjunctive resolver).

  Your r4471586474 (`HotelValidationResult` returning the raw value after comparing the effective one) is a bug for retention too, so I'll fix that in #61725 rather than leave it to the GJM work.

  On merge order between #61724 and #61725: [fill in: which lands first, and that `SupersetOf` moves with it].

  ### Open for you
  - Confirm you want to fix r4471586474 in #61725 (the draft promises it).
  - Decide the #61724 / #61725 merge order and where `SupersetOf` + the `AllOf` fix should live, then fill the last line.
project: null
source_id: https://linear.app/canary-technologies/issue/ENT-7726/implement-binding-rules-tree-prototype#comment-a9478da3
tags:
- morning-gtd
- linear
time_minutes: 15
title: 'Reply on ENT-7726: should Martin attempt the GJM reader as part of the eng
  design?'
updated: 2026-11-05 16:11:13.855722
waiting_on: null
waiting_since: null
working_on: false
---

Martin asks whether I want him to attempt the Guest Journey Messages reader in the eng design or whether I already have an idea to fold into my PRs; he notes the value reader can only attach to a real column. 2 new comments; also links PR #61725 discussion r4471587063.
https://linear.app/canary-technologies/issue/ENT-7726/implement-binding-rules-tree-prototype