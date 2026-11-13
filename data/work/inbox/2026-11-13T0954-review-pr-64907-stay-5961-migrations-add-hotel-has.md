---
area: null
completed_at: null
contexts:
- react
created: 2026-11-13 09:54:27.755729
defer_until: null
due: null
energy: medium
id: 2026-11-13T0954-review-pr-64907-stay-5961-migrations-add-hotel-has
order: null
output: |-
  ## Agent run 2026-11-13T10:07:57

  Verdict: do not approve yet. The change itself is sound, but CI is red for two reasons this PR causes. Nothing was posted to GitHub.

  PR #64907 (https://github.com/canary-technologies-corp/canary/pull/64907), +26/-0, 3 files: model field, migration 0789, admin fieldset entry. Ticket STAY-5961 (https://linear.app/canary-technologies/issue/STAY-5961/disable-anonymous-reservation-lookup-everywhere-except-paired-devices).

  ### Blocking: two generated files are stale

  Both `Backend linters` and `make test-backend` fail on these (4 failed, 111190 passed):

  1. `backend/canary/rules_based_configuration/types/setting_keys.py` is stale. Fix: `python manage.py generate_setting_types`. Fails `make check-generate-setting-types` and `test_generate_setting_types.py`.
  2. `backend/canary/canary_mcp/sql_grants/canary_mcp_ro.json` and `.sql` are missing `has_guest_sign_in`. Fix: `make generate-mcp-sql-grants`. Fails `make check-mcp-sql-grants` and three tests in `canary_mcp/services/tests/test_sql_grants.py`.

  Runs: linters https://github.com/canary-technologies-corp/canary/actions/runs/43379961397/job/131735174175 , tests https://github.com/canary-technologies-corp/canary/actions/runs/43379961331/job/131735173963

  `setting_keys.py` is on the migration-only linter allowlist (per the backend:split-migration skill). I did not confirm the MCP grant files are; if not, they go in #64911. The stacked PRs #64911 and #64913 also fail `Backend linters`, probably for the same reason (not checked).

  `Birdline policy` is red only because no approval exists yet.

  ### Worth raising with Ishwar

  - Default is on, so this stack does not close SEC-1762 by itself. Merging all of it changes no hotel; the exposure ends only when someone runs `set_guest_sign_in` (#64913, https://github.com/canary-technologies-corp/canary/pull/64913). New hotels will also be created with lookup on. The PR says the product owner chose default on. Ask what the rollout plan is and whether new hotels should default off once existing ones are flipped.
  - The field becomes a rules-based-configuration key, `hotel.has_guest_sign_in`, once setting_keys is regenerated. A rule could then turn sign-in on or off for a brand. That may be wanted (brand-wide off), but it is a security control, so confirm it is intended. That file is pod-enterprise CODEOWNERS, and your approval does not clear that gate.
  - The PR description frames this as a staff convenience switch and does not mention SEC-1762. Fine if deliberate.

  ### Checked and fine

  - Migration SQL is one statement: `ALTER TABLE "hotels_hotel" ADD COLUMN "has_guest_sign_in" boolean DEFAULT true NOT NULL`. Constant default, so no table rewrite on Postgres, and old code keeps working during deploy because of the DB default.
  - Migration depends on `0788_alter_omnidashboardoverride_surface`, which is the latest on origin/master. No number conflict today; PR is mergeable.
  - Added to `CONFIG_FIELDS`, so changes are logged as config-change events. Not a secret or PII, so the allowlist entry is appropriate.
  - Admin: placed in the "Guest Management" fieldset, editable.
  - Minor: sets both `default=True` and `db_default=True`; the neighbouring `has_tablet_reg_v1` uses `db_default` only. Harmless.

  Not done: I did not run the migration or tests locally, and did not review the three stacked PRs (#64911 backend enforcement https://github.com/canary-technologies-corp/canary/pull/64911 , #64912 frontend https://github.com/canary-technologies-corp/canary/pull/64912 , #64913 command). The enforcement in #64911 is where the security review matters.

  ### Draft review comment (not posted)

  > Change looks right, two things before I approve:
  > 1. CI is red because two generated files are stale: run `python manage.py generate_setting_types` and `make generate-mcp-sql-grants` and commit the results.
  > 2. Since the default is on, what is the plan for flipping existing hotels for SEC-1762, and should new hotels default off afterwards? Also note this becomes rules-settable as `hotel.has_guest_sign_in`; is that intended?
project: null
source_id: https://github.com/canary-technologies-corp/canary/pull/64907
tags:
- morning-gtd
- github
time_minutes: 15
title: 'Review PR #64907: [STAY-5961] Migrations: add Hotel.has_guest_sign_in'
updated: 2026-11-13 10:07:57.843920
waiting_on: null
waiting_since: null
working_on: false
---

SEC-1762 incident fix (disable anonymous reservation lookup except paired devices). Author in15 (Ishwar), branch in15/hotel-guest-sign-in-field. First of a 3-PR stack.
https://github.com/canary-technologies-corp/canary/pull/64907