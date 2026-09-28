---
area: null
completed_at: 2026-09-25 11:19:41.492036
contexts:
- react
created: 2026-09-25 09:05:07.900449
defer_until: null
due: null
energy: medium
id: 2026-09-25T0905-re-review-pr-53770-tool-719-run-onboarding-post-su
order: null
output: |
  ## Agent run 2026-09-25T10:47:31+03:00

  **Verdict: approve.** Head 3b5687c implements the refactor I asked for on Sep 23 (https://github.com/canary-technologies-corp/canary/pull/53770#pullrequestreview-5291257973, my COMMENTED review Sep 23 12:57 UTC) and Laura's two inline notes. Nothing blocking. Review not yet posted on GitHub; suggested text below.

  PR: https://github.com/canary-technologies-corp/canary/pull/53770 (head 3b5687c, re-requested Sep 25 03:01 UTC, reviewDecision APPROVED via Laura)
  Ticket: https://linear.app/canary-technologies/issue/TOOL-719 (In Review, Ramiro)

  **What changed since my last pass (commits 4962ec0 "Run every post_success_hook and collate the failures", 3b5687c "List the other failed hooks on an expected hook error")**
  - `_run_post_success_hooks` now does one thing: runs every hook, returns `(results, [(plan, exception)])`, never raises. The `raise_on_error` flag and the `plan_results` parameter are gone. Expected errors log at warning (kept out of Sentry), everything else `log.exception`.
  - Policy moved to the callers, as suggested. The `_run_hooks` on_commit closure calls a new `_raise_for_failed_hooks`: if any failure is an `ExpectedOnboardingPlanError` it re-raises one with the same error code, other failures appended to `context_string` ("Other failed hooks: Plan: msg; ..."), `from` the original. Otherwise one `OnboardingServiceError("Post success hooks failed: ...")` naming every plan with `failed_plan` = first failure. Staging path formats failures into its existing `{"plan", "error"}` entries (now appended after the successful results, test updated).
  - `ExpectedOnboardingPlanError` gained keyword-only `partial_plan_results` (default []), and the batch handler now stores `[*e.partial_plan_results, e.error_context.results_before_error or {}]`. That answers Laura's onboarding.py:787 note (committed plan results were missing from the failed run).
  - Tests: the fail-fast test became "every hook ran, error names both failures, blames the first"; expected-error test now asserts the later hook still ran and partial results carry through; new test for expected + unexpected mix asserts the expected code wins regardless of order and the other failure lands in `context_string`. Batch test asserts `run.result["partial_plan_results"]` ordering. `autospec=True` added to the new `query_salesforce` patches (fixes the linter warning I noted last time).

  **Verified**
  - Ran `onboarding/tests/services/test_onboarding.py` and `test_onboarding_batch.py` locally at 3b5687c in a throwaway worktree: 185 passed in 9.6s (worktree removed afterwards).
  - CI on head: all blocking checks green; only the non-blocking Playwright E2E shard 1/4 fails, unrelated.
  - No subclasses of `ExpectedOnboardingPlanError` exist and all constructor call sites are positional-context-only, so the new keyword arg is backwards compatible. `OnboardingPlanErrorContext` is a plain dataclass, so `dataclasses.replace` is fine; `context_string` may be "" or None and both branches are handled.

  **Non-blocking notes**
  1. Batch handler still appends `results_before_error or {}`; for a hook-raised expected error `results_before_error` is None, so an empty `{}` trails `partial_plan_results` on the run. Pre-existing quirk, now slightly more visible. Optional: `[*e.partial_plan_results, *([r] if (r := e.error_context.results_before_error) else [])]`, or leave it.
  2. The admin-path follow-up Linear ticket Laura asked for on Sep 23 still does not exist (checked Internal Tools issues created since Sep 22; only TOOL-719 relates). Worth asking Rami to file and link it before merge.
  3. Stale "batch runner holds a transaction open" comment on `_dispatch_re_evaluation_after_commit` in configure_guest_journey_messages.py remains a described follow-up in the PR body.

  **Suggested GitHub approval text (not posted, needs your OK):**
  > Approving. This is exactly the shape I was after: `_run_post_success_hooks` runs every hook and reports, and each caller applies its own policy. The expected-error-wins rule with the other failures in `context_string` is a sensible way to keep one error code per run, and the batch run now carries the committed plan results on that path too. Local run of both onboarding service test files passes at 3b5687c. One ask before merge: please file and link the admin-path (`onboard_individual_hotel`) follow-up ticket Laura mentioned so it is not lost.
project: null
source_id: https://github.com/canary-technologies-corp/canary/pull/53770
tags:
- morning-gtd
- github
- resurfaced
time_minutes: 15
title: 'Re-review PR #53770: [TOOL-719] Run onboarding post_success_hooks after the
  transaction commits'
updated: 2026-09-25 11:19:41.492026
waiting_on: null
waiting_since: null
working_on: false
---

Resurfaced: archived 2026-09-23 as `2026-09-23T0906-re-review-pr-53770-tool-719-run-onboarding-post-su`, but new activity at the source since then.

Rami re-requested my review 09-25 03:01 (my last review: COMMENTED). ldewald already approved: 'Moving the hooks to on_commit fixes the incident and the batch path'. Branch fix/onboarding-post-success-hooks-after-commit.
https://github.com/canary-technologies-corp/canary/pull/53770