---
area: null
completed_at: null
contexts:
- react
created: 2026-08-12 07:20:04.148450
defer_until: null
due: 2026-08-12
energy: low
id: 2026-08-12T0720-reply-to-andrea-s-notion-comment-on-segmentation-f
order: null
output: |
  ## Agent run 2026-08-12T11:06

  **Doc:** "Segmentation for Wyndham" — https://app.notion.com/p/3ad81468615180759a4fed4a9d9c7e1b
  **Linear project:** Enterprise Rollout: Segmentation for Wyndham — https://linear.app/canary-technologies/project/96bb77fa-cff6-412d-859a-1d56e90026f5
  (author/lead: Andrés Figueira; reviewers: you, Andrea Bradshaw, Martin Rodriguez)

  ### Correction to the task premise
  "Great start delving into the GJM onboarding code" was written by **you**, not Andrea
  (2026-07-31). Andrea's Aug 10 reply landed *in your thread* — that's what generated the
  Gmail notification. Her reply is just: "Looking good, I have a few more questions and
  comments before we begin implementation." It asks you nothing directly.

  So there is no question strictly owed. But three of Andrea's comments are still
  **unresolved**, and all three sit squarely in the territory you raised (management-command
  proliferation vs. re-running the config provider). Answering them is the high-value move.

  ### Andrea's three open comments
  1. On "Dry-run": *"Do we have dry-runs built in to our system? Or this is a management
     command to validate?"*
  2. On `verify_wyndham_gjm_migration`: *"What is this? A method that is part of the plan?
     a mgmt command? Where does the output live?"*
  3. On `dry_run_wyndham_gjm_migration`: *"I'm concerned about keeping logic changes in sync
     between this, the confirm command, and the actual configuration scripts"*

  Already resolved by Andrés since: the `Hotel.use_segmentation_v2` field became a join table
  (Andrea's push), Parts 3/4 were swapped, and Andrea landed "a plan is better than a manual
  step" re: `EnableWyndhamSegmentationV2GatePlan`.

  ### Codebase findings (verified, backend/canary/onboarding)
  - **No generic dry-run exists.** `OnboardingPlan` (plans/base.py) has one write path,
    `execute()`. No plan-level preview/diff. So the proposed command would be bespoke — and
    would carry a second copy of "what the plan should produce". Andrea's concern (3) is
    well-founded.
  - **`check_hotel_configuration` is the built-in verify mechanism.**
    `ConfigProvider.check_hotel_configuration(hotel)` → `list[tuple[MonitoredCheckType,
    CheckResultData]]`, reached via `OnboardingPlan.check_hotel_configuration_without_instantiation`.
    Results persist as `MonitoredCheckResult` and **already feed cohort membership** through
    `CohortHotelService` (services/cohort_hotel.py); `services/health.py` runs them. This is a
    better home for `verify_wyndham_gjm_migration` AND absorbs most of `sync_wyndham_case_cohorts`.
  - **`TargetedRollout` removes the manual per-wave flag step.**
    `onboarding/models/targeted_rollout.py` runs a rollout function on the config provider
    instead of `execute()`, riding the existing recipe infra (population selection, staging,
    batching, retries, results UI). Live precedents: `ENABLE_WYNDHAM_AMB`,
    `ENABLE_WYNDHAM_DYNAMIC_PRICING_20260730` in
    `configuration_providers/wyndham/wyndham_amb_config_provider.py`. Better than a separate
    gate plan — one code path, no manual step.
  - **The "segment events fire only after commit" fix is right regardless.**
    `post_success_hook` exists for exactly post-transaction work (per onboarding/CLAUDE.md).

  ### DRAFT REPLY — NOT POSTED (needs your approval + your own words)
  ---
  Re: dry-runs and keeping the commands in sync — your instinct is right, and it's the same
  thing I flagged at the top of the thread.

  There's no generic dry-run in the onboarding framework. `OnboardingPlan` has one write path
  (`execute()`); there's no plan-level preview or diff. So `dry_run_wyndham_gjm_migration`
  would be bespoke, and it would carry a second copy of "what the plan should have produced"
  — which is exactly the drift you're worried about.

  Two mechanisms already exist that I'd reach for instead:

  1. Verification → `check_hotel_configuration`. `ConfigProvider.check_hotel_configuration(hotel)`
     returns `MonitoredCheckType` + `CheckResultData`, surfaced through
     `OnboardingPlan.check_hotel_configuration_without_instantiation`. Results persist as
     `MonitoredCheckResult` and already feed cohort membership via `CohortHotelService`. That's
     a better home for `verify_wyndham_gjm_migration`: verification becomes a continuously-run
     check with output in monitoring and cohorts, instead of a one-shot command whose output
     lives in a terminal. It also removes most of `sync_wyndham_case_cohorts` — most of the
     buckets are just check outcomes.

  2. The manual flag step → `TargetedRollout`. `onboarding/models/targeted_rollout.py` runs a
     rollout function on the config provider instead of `execute()`, riding the existing recipe
     infrastructure — population selection, staging, batching, retries, and the results UI.
     `ENABLE_WYNDHAM_AMB` and `ENABLE_WYNDHAM_DYNAMIC_PRICING_20260730` are live precedents in
     `wyndham_amb_config_provider.py`. The rollout function can set the gate and run the config
     in the same targeted run, which removes the manual per-wave step without needing a separate
     gate plan.

  If you do keep a dry run, have it call the same check functions as (1) rather than a second
  set of assertions — one source of truth for "correct".

  One more: the doc notes the dry run needs "a small fix so segment events fire only after
  commit". That fix is worth making on its own merits — `post_success_hook` exists for exactly
  this, so segment event dispatch should move there (or to `transaction.on_commit`) regardless
  of whether we build the dry run.
  ---

  **Nothing was posted to Notion.** Say the word and I'll post it (or your edited version) as a
  reply to Andrea's page-level comment, or split it across her three inline threads.
project: 2026-04-16T1210-unblock-team
source_id: https://mail.google.com/mail/u/0/#inbox/19fedc8407b45adf
tags:
- morning-gtd
- gmail
time_minutes: 15
title: Reply to Andrea's Notion comment on "Segmentation for Wyndham"
updated: 2026-08-12 11:47:40.947142
waiting_on: null
waiting_since: null
working_on: false
---

Andrea commented on the design doc addressing me directly ("Great start delving into...").
https://mail.google.com/mail/u/0/#inbox/19fedc8407b45adf
Andrés reshared it with changes highlighted (#epd-enterprise-engineers, 11 Aug) and Andrea commented "a few more questions and comments before we begin implementation". My earlier note pushed the config-provider + GuestJourneyMessageGroupUseCase route over management commands — check the revision honours that.
https://www.notion.so/canarytechnologies/Segmentation-for-Wyndham-3ad81468615180759a4fed4a9d9c7e1b