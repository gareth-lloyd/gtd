---
area: null
contexts:
- react
created: 2026-05-07 11:29:44.795919
defer_until: null
due: null
energy: medium
id: 2026-05-07T1129-review-pr-44759-new-pms-choices-and-migration
order: null
output: "## Agent run 2026-05-07T10:37Z\n\nReviewed PR #44759 (Ramiro — Part 1 of
  4 splitting #44607). Local checkout\non branch `pr-44759`, diffed against master.\n\n###
  Scope\n- Adds ~50 new entries to `PMSChoices` (TextChoices) in\n  `backend/canary/hotels/models/mixins/hotels/pms_choices.py`
  (+49 lines).\n- Adds matching migration `hotels/0738_alter_hotel_pms.py` (+525 lines)\n
  \ regenerating the full `choices=[...]` list on `Hotel.pms`.\n- Migration depends
  on `0737_hotel_rollout_hide_property_staff_default_role`\n  (current head on master)
  — numbering is correct, no conflict with master.\n\n### Risk\nLow. The auto-generated
  migration SQL is a no-op (BEGIN; -- (no-op); COMMIT)\nbecause `choices=[...]` lives
  at the Python/Django level only — the DB column\nis unchanged. No data backfill,
  no lock concern.\n\n### Verified\n- Model and migration are in lockstep: 481 (value,
  label) pairs each, sets\n  are identical. (Confirmed via Python regex extraction.)\n-
  No duplicate keys, no duplicate values, no duplicate human labels in\n  `PMSChoices`
  after the change.\n- Numbering (0738) is free on master.\n- Salesforce picklist
  push (`push_global_value_set_pms_picklist.py`)\n  iterates `PMSChoices.choices`
  so new entries flow through automatically —\n  no code change needed there. Worth
  a heads-up that the next run will push\n  ~50 new picklist values.\n\n### Things
  worth a comment from the reviewer\n\n1. **Conceptual duplicates — intentional?**
  Several new entries appear to\n   overlap with existing ones for the same vendor/product:\n
  \  - `AGILYSYS_VISUAL_ONE` (new) vs `VISUAL_ONE_AGILYSYS` (existing,\n     label
  \"Visual One Agilysis\" — note pre-existing misspelling)\n   - `AGILYSYS_LMS` (new)
  vs `LMS_AGILYSYS` (existing)\n   - `AGILYSYS_STAY` (new) vs `RGUEST_STAY_AGILYSYS`
  (existing,\n     label \"Rgust Stay Agiliysys\" — pre-existing typo)\n   - `ORACLE_OPERA`
  (new) vs `OPERA` (existing) — Oracle owns Opera\n   - `ORACLE_FIDELIO_SUITE8` (new)
  vs `FIDELIO_SUITE8` (existing)\n\n   These look like cleaner canonical names being
  added alongside legacy\n   keys (sensible if existing rows reference the old keys),
  but worth\n   asking Ramiro to confirm intent in the PR. If old keys are meant to
  be\n   deprecated, that should be tracked as a follow-up so we don't grow\n   parallel
  naming forever.\n\n2. **`pms_vendor_mapping.py` not updated.** The Vendor → PMSChoices
  map\n   currently has `Vendor.AGILYSYS_STAY → PMSChoices.DRURY` and\n   `Vendor.JONAS_CHORUM
  → PMSChoices.JONAS`. Now that\n   `PMSChoices.AGILYSYS_STAY` and `PMSChoices.JONAS_CHORUM`
  exist, those\n   mappings are misleading. Probably out of scope for \"Part 1\" but
  worth\n   flagging — easy follow-up PR.\n\n3. **PR description test plan still has
  open TODOs:** \"run migrate hotels\n   locally\" and \"confirm no makemigrations
  drift\". The migration SQL is a\n   no-op so this is low-risk, but the author should
  confirm both before\n   merge so we don't ship Part 2/3/4 on top of an unverified
  base.\n\n4. **Pre-existing spelling note (not blocking, not author's fault):** the\n
  \  existing `AGILYSIS` key/label uses the misspelling \"Agilysis\" while the\n   new
  entries correctly spell \"Agilysys\". A future cleanup could rename\n   the legacy
  entry, but that's a data-migration job, not this PR.\n\n### Recommendation\nApprove
  with a comment asking (1) confirmation that the duplicate Agilysys/\nOracle/Fidelio
  entries are intentional canonical-naming additions and not\nunintended duplicates,
  and (2) the test plan TODOs be checked off. No\nblocking issues — this is a safe,
  additive choices update with a no-op\nmigration.\n\n### Did NOT do (need approval)\n-
  Did not post a review or comment on GitHub.\n- Did not approve / request changes.\n\nDraft
  comment if you want to post it (verbatim, ready to send):\n\n> Looks good — additive
  PMSChoices update with a no-op migration (just\n> regenerates the choices field,
  no DB schema change). Migration numbering\n> and dependency are correct against
  current master. Model and migration\n> are in sync (481 entries each, no dup keys/values/labels).\n>\n>
  A couple of things worth confirming before merge:\n>\n> 1. Some new keys overlap
  with existing ones for the same product:\n>    `AGILYSYS_VISUAL_ONE` vs `VISUAL_ONE_AGILYSYS`,
  `AGILYSYS_LMS` vs\n>    `LMS_AGILYSYS`, `AGILYSYS_STAY` vs `RGUEST_STAY_AGILYSYS`,\n>
  \   `ORACLE_OPERA` vs `OPERA`, `ORACLE_FIDELIO_SUITE8` vs `FIDELIO_SUITE8`.\n>    Are
  the new ones meant to be the canonical names with the old ones\n>    deprecated,
  or are they actually distinct entities? If the former,\n>    worth tracking the
  deprecation as a follow-up so we don't grow\n>    parallel naming.\n> 2. `pms_vendor_mapping.py`
  still maps `Vendor.AGILYSYS_STAY` to\n>    `PMSChoices.DRURY` and `Vendor.JONAS_CHORUM`
  to `PMSChoices.JONAS`.\n>    Probably out of scope for Part 1, but those mappings
  should point at\n>    the new specific choices in a follow-up.\n> 3. Test-plan checkboxes
  in the description (`migrate hotels` locally,\n>    no makemigrations drift) are
  still TODO — please confirm before merge.\n"
project: null
source_id: https://github.com/canary-technologies-corp/canary/pull/44759
tags:
- morning-gtd
- github
- from-awareness
- unblock-team
time_minutes: 20
title: 'Review PR #44759: New PMS choices and migration'
updated: 2026-05-07 14:04:11.273166
waiting_on: null
waiting_since: null
working_on: false
---

Unblock team. Author: @ramironieto. Awaiting pod-enterprise / PMS Platform / pod-AD review.
https://github.com/canary-technologies-corp/canary/pull/44759