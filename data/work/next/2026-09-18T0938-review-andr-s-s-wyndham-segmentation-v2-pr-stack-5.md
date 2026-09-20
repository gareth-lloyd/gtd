---
area: null
completed_at: null
contexts:
- react
created: 2026-09-18 09:38:23.413683
defer_until: null
due: null
energy: medium
id: 2026-09-18T0938-review-andr-s-s-wyndham-segmentation-v2-pr-stack-5
order: null
output: |
  ## Agent run 2026-09-18T14:42

  **Status: the review request is stale.** All three PRs merged at 10:07 UTC today (2026-09-18),
  approved by abrad (Andrea), merged by Andrés. This is a post-merge read of origin/master.
  Nothing was posted anywhere. Review was by code reading only; I ran no tests.

  - PR #56242 rollback plan + recipe (ENT-7411): https://github.com/canary-technologies-corp/canary/pull/56242
  - PR #56243 script types, choices-only migration 0169 (ENT-7412): https://github.com/canary-technologies-corp/canary/pull/56243
  - PR #56244 migration recipe + stages, lazy provider config (ENT-7412): https://github.com/canary-technologies-corp/canary/pull/56244
  - Slack thread (Andrés asked Andrea, not you, by name): https://canarytechnologies.slack.com/archives/C0B1MN8F869/p1789650428512129?thread_ts=1789650428.512129&cid=C0B1MN8F869

  **Verdict:** no merge-blocking bug found. The design fails safe: every per-hotel path raises and
  rolls back rather than half-applying. One real operational gap (1) and two trade-offs worth
  knowing before the first wave (2, 3).

  ### Findings

  1. **A rolled-back hotel cannot be re-migrated through the wave (medium, fails safe).**
     Rollback disables the v2 welcome but leaves the row. After
     `classify_wyndham_segmentation_v2_migration_hotels --release`, a hotel with both v1 welcomes on
     reclassifies to READY_TO_MIGRATE. On the second wave the gate snapshots `{members: True,
     non_members: True}`, but `_welcome_message_v2_enabled_policy` sees the existing v2 message and
     returns LEAVE_AS_IS, so v2 stays disabled. Verify's `_assert_enabled_state_matches_snapshot` then
     expects enabled=True, gets False, and raises `segmentation_v2_verification_failed`. The hotel
     keeps v1, so no guest impact, but rollback → fix → re-migrate is blocked for the common case
     until someone hand-enables or deletes the v2 welcome. No test covers migrate → rollback →
     release → re-migrate. Files: `wyndham_guest_journey_messages_provider.py` (enabled policy),
     `wyndham_segmentation_v2_migration_verify_provider.py`.

  2. **Rollback ignores what the hotel did to the v2 welcome after migration (design trade-off).**
     Restore reads only the gate snapshot, by design. Consequence: a hotel that deliberately switched
     its v2 welcome off after migration gets both v1 welcomes switched back on by a rollback. Worth a
     line in the runbook, or a check of v2 enabled state in the rollback result so operators can spot
     these hotels.

  3. **Lazy `WyndhamGuestJourneyProvider.config` weakens the assemble-first check (low).**
     `_execute_plans` assembles all plans before executing any, "to catch misconfigurations before
     making changes to the hotel". Config build errors for this provider (missing SupportUser, SF
     fields) now surface mid-run in BASE_CONFIGURATION_NEW and staging too, not just the wave. DB
     writes still roll back; external side effects of earlier plans (gateway upserts) do not. The
     cache is safe: providers are assembled per hotel per run.

  4. **Test gaps (low).** Rollback tests run against stubs, never against real migration output, so
     there is no end-to-end migrate → rollback test. The canary linter also flagged the new
     `mock.patch` without `autospec` in the rollback provider test (warning only).

  ### Checked and fine

  - Post-commit re-evaluation: hooks run after `_execute_plans`' atomic block, and dispatch goes
    through `transaction.on_commit`, so an outer batch transaction that rolls back drops the tasks.
  - State flips are single conditional UPDATEs (gate and rollback), so concurrent runs cannot
    double-apply. `_touched_message_schedule_spec_ids` is per-provider-instance, and instances are
    per hotel.
  - `rollout_guest_segmentation` is True in both v1 and v2 configs, so rollback does not need to
    touch it. Rollback does reset `rollout_message_variants`, which is what gates variant resolution
    in the send path (`guest_journey/services/message_variant.py`).
  - Separate SEGMENTATION_V2_MIGRATION and SEGMENTATION_V2_ROLLBACK stages; CUSTOM is back to AMB
    only. Migration 0169 is a choices-only AlterField.

  ### Not verified

  - Whether the rollout batch runner wraps a whole 500-hotel stage in one outer transaction. If it
    does, row locks and all re-evaluation dispatches are held until the batch commits.
  - Whether leftover v2 rows on a released hotel trip the classifier's `drift` signal (which would
    change finding 1 from "verify fails" to "never re-staged").

  ### Suggested next step (your call)

  Nothing to approve any more. If you want to raise finding 1 with Andrés, a draft (not sent):

  > Post-merge note on the seg v2 stack: I think a rolled-back hotel can't be re-migrated. Rollback
  > leaves the v2 welcome disabled, the enabled policy returns LEAVE_AS_IS because the row exists, and
  > verify then fails the snapshot check (expects enabled). Fails safe, but `--release` → re-wave
  > won't work without hand-fixing the v2 welcome. Worth a test for migrate → rollback → release →
  > re-migrate?
project: 2026-04-16T1210-unblock-team
source_id: https://canarytechnologies.slack.com/archives/C0B1MN8F869/p1789650428512129?thread_ts=1789650428.512129&cid=C0B1MN8F869
tags:
- morning-gtd
- slack
time_minutes: 45
title: 'Review Andrés''s Wyndham segmentation v2 PR stack (#56242, #56243, #56244)'
updated: 2026-09-18 15:19:35.090089
waiting_on: null
waiting_since: null
working_on: false
---

Rollback plan + recipe, migration/rollback script types, migration recipe and stages. Saved from #epd-enterprise-engineers.
https://github.com/canary-technologies-corp/canary/pull/56242
https://github.com/canary-technologies-corp/canary/pull/56243
https://github.com/canary-technologies-corp/canary/pull/56244
https://canarytechnologies.slack.com/archives/C0B1MN8F869/p1789650428512129?thread_ts=1789650428.512129&cid=C0B1MN8F869