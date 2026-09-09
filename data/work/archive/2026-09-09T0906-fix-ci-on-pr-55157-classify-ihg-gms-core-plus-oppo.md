---
area: null
completed_at: 2026-09-09 10:23:44.448353
contexts:
- react
created: 2026-09-09 09:06:47.339083
defer_until: null
due: null
energy: medium
id: 2026-09-09T0906-fix-ci-on-pr-55157-classify-ihg-gms-core-plus-oppo
order: null
output: |-
  ## Agent run 2026-09-09T10:35

  **Verdict: nothing to fix. PR #55157 is not actually blocked — merge it when you're ready.**
  https://github.com/canary-technologies-corp/canary/pull/55157

  ### What CI is actually saying

  One red check, and only one:
  `Non-blocking / Playwright E2E Tests (Shard 3/4)` — run 34229574299, job 102073041850
  https://github.com/canary-technologies-corp/canary/actions/runs/34229574299/job/102073041850

  Failing test: `e2e-tests/tests/messaging/journey-message-variants.spec.ts:534`
  "Guest Journey Segmentation (message variants) > staff disables a message with the guest-journey-settings toggle"

  Assertion, at `e2e-tests/pages/JourneyMessagesPage.ts:290`:
  `expect(switch).toBeChecked({ checked: false })` — expected unchecked, got checked, 10s timeout.
  The enable toggle for "E2E Segmented Welcome" never flipped off. Failed on first attempt and on retry #1; the 6 later tests in that serial group then did not run. 105 passed, 1 failed, 1 skipped.

  ### Why it is not this PR

  The diff is backend Python only — no frontend, no messaging, no template:
  - `backend/canary/canary/salesforce_ids.py`
  - `backend/canary/onboarding/services/salesforce_onboarding_fields.py`
  - `backend/canary/onboarding/services/salesforce_opportunity.py`
  - `backend/canary/onboarding/services/types.py`
  - `backend/canary/rules_based_configuration/models/msa.py`
  - plus three test files

  There is no causal path from a Salesforce opportunity-import change to a guest-journey message toggle in the staff UI.

  Confirmed empirically: the identical test at `:534` fails on unrelated branch `nk/operator-chat-follows-new-messages`
  https://github.com/canary-technologies-corp/canary/actions/runs/34304616609

  ### The E2E suite is broadly red right now (separate problem, not yours)

  Sampled recent runs across unrelated PRs. Failing on nearly every one:
  - `tests/messaging/service-tickets-unlink.spec.ts:40`
  - `tests/messaging/thread-realtime.spec.ts:66`, `:182`, `:398`

  Seen on `cluxton/infra-652-*`, `adil/apac-90-*`, `key-dispenser-cleanup-hotel-devices`, `pgao/apac-122-*`, `ashish/pms-10429-*`, `nk/operator-*`, `growthbook-feature-flag-sync` and others. This looks like a repo-wide messaging-E2E breakage worth someone owning — but it is not a #55157 problem and fixing it does not belong in this PR.

  ### The check is non-blocking by design

  `.github/workflows/canary_ui_e2e_tests.yml:703-718` documents it: a shard failure marks the check red for visibility but does NOT gate the merge queue. `merge_gatekeeper.yml` passes `--exclude-pattern '^9\.CAN\.AUTO UI E2E Tests'` to `workflow_monitor.py`. The "Non-blocking /" name prefix is deliberate, added precisely because devs kept reading it as a blocker.

  Corroborating state on the PR:
  - `merge_gatekeeper` check: SUCCESS
  - `mergeStateStatus`: UNSTABLE (failing non-required check — not BLOCKED)
  - `reviewDecision`: APPROVED (abrad, 2026-09-02)
  - `make test-backend`, `make check-fix-lint check-fix-format`, `check-migrations`, `OpenAPI specs`, `Backend linters`: all SUCCESS

  ### Branch health

  129 behind / 5 ahead of master. Trial merge (`git merge-tree`) is **clean**. Zero master churn in any of the five source files this PR touches since the merge-base (`422cd6a8dfb`), so the staleness carries no semantic-conflict risk. Last commit is a master merge from 2026-09-08.

  ### What I did not do (needs your say-so)

  - Did not re-run the failed shard. It is a GitHub state change; say the word and I'll kick it, though it only buys a cosmetic green — the merge gate already ignores it.
  - Did not merge. Per your standing rule, you merge.
  - Did not touch the flaky messaging specs or reach for `dx:flaky-skip`. That is a separate PR and probably a separate owner; flagging it here rather than expanding this PR's scope.

  ### Recommendation

  Merge #55157 as-is. If the red check bothers you, re-run shard 3 first — but it will likely just land on one of the other broken messaging specs.
project: null
source_id: https://github.com/canary-technologies-corp/canary/pull/55157
tags:
- morning-gtd
- github
time_minutes: 30
title: 'Fix CI on PR #55157: Classify IHG GMS Core Plus opportunities on Salesforce
  import'
updated: 2026-09-09 10:23:44.448342
waiting_on: null
waiting_since: null
working_on: false
---

Approved but CI failing; IHG Core vs Core Plus import view.
https://github.com/canary-technologies-corp/canary/pull/55157