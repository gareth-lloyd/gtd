---
area: null
completed_at: 2026-09-23 15:57:22.528442
contexts:
- react
created: 2026-09-23 09:06:58.715808
defer_until: null
due: 2026-09-23
energy: medium
id: 2026-09-23T0906-re-review-pr-53770-tool-719-run-onboarding-post-su
order: null
output: |
  ## Agent run 2026-09-23T13:23:15+01:00

  **Verdict: approve.** The on_commit rewrite addresses my Sep 22 comment (honor the post_success_hook docstring for every caller, not just the batch runner). Ready to approve on GitHub; no review posted yet.

  PR: https://github.com/canary-technologies-corp/canary/pull/53770 (head 685c671, review-requested Sep 22, Laura approved Sep 23 00:19 UTC)
  Ticket: https://linear.app/canary-technologies/issue/TOOL-719 (In Review, Ramiro)

  **What changed since my last pass (commit 685c671 "Defer onboarding post_success_hooks to the outermost commit")**
  - `run_plans_on_hotel` now registers `_run_hooks` via `transaction.on_commit` and returns a `HotelCreateResult` whose `post_success_hook_results` is None until the outermost commit. Covers batch, admin (`onboard_individual_hotel`, @atomic), demo (`onboard_demo_hotel`, @atomic) and the dev crestline command with one primitive.
  - `_run_post_success_hooks` with `raise_on_error=True` now raises: `ExpectedOnboardingPlanError` passes through with its code; anything else becomes `OnboardingServiceError(failed_plan=plan, partial_plan_results=[*plan_results, *hooks_so_far])`. Laura's "green run with the error buried" concern is fixed.
  - Staging path keeps `raise_on_error=False` and runs the hooks directly after its own atomic block (already outside a transaction; unchanged behaviour).
  - Tests use `captureOnCommitCallbacks` / `django_capture_on_commit_callbacks` and assert hooks did NOT run while the transaction was open, then ran once. Three new tests cover wait-for-commit, generic hook failure -> OnboardingServiceError with failed_plan, and expected error keeps ERROR_ON_DEMAND_FETCH_FAILED.

  **Verified by reading the head, not by running locally**
  - Batch path (`script_run_attempt`): the Celery task holds no outer atomic, so the atomic in `onboard_hotel_from_salesforce_account` is outermost. Django runs on_commit callbacks inside `Atomic.__exit__` (via `set_autocommit(True)`), so a hook exception propagates out of the `with` block, past the post-run checks, into the existing `except ExpectedOnboardingPlanError` / `except OnboardingServiceError` handlers -> `fail_run`. The run is FAILED with `failed_plan` and rerunnable; no rollback of the plans' work.
  - `HotelCreateResult` is a plain (non-frozen) dataclass, so the closure assignment works.
  - Post-run hotel checks still execute after the hooks (hooks fire at atomic exit, checks are after the block), so ordering matches the previous behaviour apart from hooks now being post-commit.
  - CI: all blocking checks pass (backend tests included). Only failure is the non-blocking Playwright E2E shard 1/4, unrelated to onboarding. Canary Linter warns on `@patch("onboarding.services.onboarding.query_salesforce")` without autospec in the new tests; the file already has 24 identical patches, so it is consistent with the file, warning only.
  - I did not run the onboarding test suite locally (CI green; PR description reports 4305 passed with one pre-existing pytest-socket failure).

  **Non-blocking notes (optional to add on GitHub; Laura already raised the first two)**
  1. Fail-fast semantics: a non-robust on_commit callback that raises drops every later callback in the same commit (Django `run_and_clear_commit_hooks` pops the list into a local). So a raising hook skips the remaining plans' hooks AND any on_commit registered after `_run_hooks` in the same atomic. A rerun recovers, so fine for now; "run all hooks, raise one aggregated error" would be the more predictable follow-up.
  2. `ExpectedOnboardingPlanError` from a hook: the batch handler stores only `results_before_error`, so committed plan results are missing from the failed run's `result`. Laura's inline note at onboarding.py:787.
  3. Admin path (`onboard_individual_hotel`) still stores/returns only `plan_results`; a hook failure there surfaces as a 400/422 after the hotel exists. Laura asked for a Linear ticket; **none exists yet** (searched Internal Tools issues created since Sep 20, only TOOL-719). Worth nudging Rami to file it before merge so it is not lost.
  4. The `_dispatch_re_evaluation_after_commit` comment in `configure_guest_journey_messages.py:467` ("The batch runner holds a transaction open") is now stale: the hook runs post-commit, so that `on_commit` executes immediately. The PR description already flags it as a follow-up.

  **Suggested GitHub review text (not posted):**
  > Approving. `on_commit` in `run_plans_on_hotel` is the right primitive: it honours the hook contract for the batch, admin and demo callers alike, and a hook failure now reaches `fail_run` with the failed plan instead of a green run. Two things for the follow-up: (1) a raising hook drops the remaining hooks (and any later on_commit callbacks) until a rerun, so an aggregate-and-raise pass would be more predictable; (2) please file the admin-path ticket Laura asked for (store `post_success_hook_results` on the run, move the call out of the @atomic) and link it here.
project: 2026-04-16T1210-unblock-team
source_id: https://github.com/canary-technologies-corp/canary/pull/53770
tags:
- morning-gtd
- github
time_minutes: 15
title: 'Re-review PR #53770: [TOOL-719] Run onboarding post_success_hooks after the
  transaction commits'
updated: 2026-09-23 15:57:22.528426
waiting_on: null
waiting_since: null
working_on: false
---

Rami re-requested my review Sep 22; Laura approved (hooks moved to on_commit, failures reach fail_run).
https://github.com/canary-technologies-corp/canary/pull/53770