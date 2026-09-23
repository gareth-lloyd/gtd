---
area: null
completed_at: null
contexts: []
created: 2026-09-22 13:37:55.250659
defer_until: null
due: null
energy: low
id: 2026-09-22T1337-review-context-in-this-thread-including-prs-summar
order: null
output: |
  ## Agent run 2026-09-22T14:05+03:00

  The item carries no thread link, so I matched it against the two Slack threads you touched this morning around 10:10 EEST. Both are summarized; the second has the "PRs" (plural).

  ### Thread A: #epd-internal-tools-engineers, AI compendium onboarding failure blocking IHG onboarding
  https://canarytechnologies.slack.com/archives/C0A8L5RJM5K/p1790026710851299?thread_ts=1790026710.851299&cid=C0A8L5RJM5K

  - Laura posted screenshots at 00:31 EEST; Rami replied "investigating". Laura ran Seer on Sentry CANARY-186M: the AI compendium onboarding task is published to SQS before the outer hotel-creating transaction commits, so the worker cannot find the hotel. Rami confirmed that is the root cause.
  - Rami says it is an onboarding-scripts architecture bug, not AI-compendium-specific. Draft fix: PR #53770 (https://github.com/canary-technologies-corp/canary/pull/53770), "run post_success_hooks after commit on the salesforce path". Opened 2026-08-20, still DRAFT, 2 files (+94/-5), review required.
  - The bug blocked Taylor from onboarding IHG hotels. Workaround Rami gave her: run the other plans first, then the AI compendium plan after they finish.
  - You CC'd Andrea at 10:10 EEST. No replies since.
  - PR #53770 state: Laura reviewed on 2026-09-21 with three inline notes. The one she wants addressed before merge: on the batch path a hook failure now becomes a {"plan","error"} entry in plan_results, script_run_attempt marks the run COMPLETED, and get_warnings() only reads non_fatal_warnings, so a failed hook (e.g. PMS on-demand fetch HTTPError) shows green and nobody sees it. Follow-up-sized notes: the admin path (OnboardingBatchService.onboard_individual_hotel) is wrapped in @transaction.atomic so hooks still run pre-commit there and errors are now swallowed; and a test rename since TestCase never actually commits.
  - Diff shape: hotel-creating atomic block calls run_plans_on_hotel with run_post_success_hooks=False, then runs _run_post_success_hooks(raise_on_error=False) after the block; HotelCreateResult gains executed_plans. Two new tests assert savepoint depth and captured hook failures.
  - Unblock read: Rami has the fix but it has sat as a draft for a month and now has a blocking review note. Decide whether hook failures should surface as warnings (Laura's ask) before it ships, and whether Andrea or Rami owns pushing it through. IHG onboarding (ENT-6032 wave) is exposed until then.

  ### Thread B: #eng-enablement, feature-flag sync PRs timing out in backend tests
  https://canarytechnologies.slack.com/archives/C09D2A5LYN9/p1790028105271349?thread_ts=1790028105.271349&cid=C09D2A5LYN9

  - Santi reported the auto-generated feature-flag sync PR #57077 (https://github.com/canary-technologies-corp/canary/pull/57077) failing with SUITE TIMEOUT after 1800s (78k tests done, 26 workers).
  - James Morton diagnosed it: the sync flips use-ai-translation-inbound to default True. ThreadService.translate_thread_message then calls the prompt gateway with max_retries=5; pytest-socket blocks the first attempt but litellm sleeps through backoff on the other four (~7s per message). Two tests push enough messages to blow the 90s per-test limit; several messaging test files went from ~3-8s to 100-240s.
  - Fix: PR #57283 (https://github.com/canary-technologies-corp/canary/pull/57283) "Cap LiteLLM retries to zero under test". Adds PROMPT_GATEWAY_MAX_NUM_RETRIES (None in base, 0 in settings/test.py); LiteLLMClient caps num_retries on completion and streaming paths. 4 files, +16/-4. He first opened #57281 off the growthbook-feature-flag-sync branch (green run there), closed it, and reopened as #57283 off master.
  - PR #57283 state: approved by aditmeno at 07:12Z. Latest CI run is green on make test-backend, merge_gatekeeper, backend linters, OpenAPI. The red checks shown on the PR page (OpenAPI specs failure, cancelled jobs) are from the superseded first push. Playwright critical fails on the same two checkin-v3 additional-guests specs that also fail on #57077, so unrelated. Macroscope flagged "not approvable" only because settings/ is excluded from auto-approval; human approval covers that. Not merged yet.
  - Merge was blocked this morning by lockdown issue #57293 (INFRA-503 gateway DB migration window, https://github.com/canary-technologies-corp/canary/issues/57293); that issue is now CLOSED, so nothing blocks merging #57283.
  - #57077 kicked off another make test-backend at 10:07Z (13:07 EEST), still in progress at time of writing. Without #57283 in master it will time out again.
  - James notes ~85 tests exercise the AI translation path unintentionally and should patch AITranslationService.translate; he left that as a follow-up.
  - Unblock read: nudge James (or anyone) to merge #57283 now that lockdown is off, then re-run #57077. Follow-up ticket for the ~85 tests is worth filing so the next flag flip does not repeat this.

  No external writes made. Sentry lookup of CANARY-186M via MCP returned 404 (org slug mismatch), so the root cause above is quoted from the thread.
project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 5
title: Review context in this thread including PRs, summarize to me
updated: 2026-09-22 13:52:42.417234
waiting_on: null
waiting_since: null
working_on: false
---