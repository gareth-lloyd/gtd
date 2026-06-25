---
area: engineering
contexts: []
created: 2026-06-24 10:31:29.274039
defer_until: null
due: 2026-06-24
energy: medium
id: 2026-06-24T1031-review-slack-notifications-for-onboarding-failures
order: null
output: |
  ## Agent run 2026-06-24T07:32Z — review of PR #48513
  (https://github.com/canary-technologies-corp/canary/pull/48513 — "onboarding: send
  script-run failure alerts to Slack instead of email"; your own PR, branch
  worktree-onboarding-failure-slack; +203/-127, 8 files; OPEN, no reviews yet)

  Verdict: solid, ready to merge after one real fix. The change mirrors the two existing
  Slack-posting precedents closely (onboarding `notify_portfolio_drift` in
  services/salesforce_onboarding_fields.py:629 and chat/.../post_chat_analysis/slack_digest.py),
  reusing the shared VOICE_AI_LOG log bot, the same no-op-when-unset + never-raise contract,
  and raw `requests.post` to chat.postMessage. Not reinventing — good. Context dict keys all
  line up with build_failure_blocks (hotel_name, identifier, batch_label, batch_type,
  plan_names, error_message, error_code, failed_plan, user_action, batch_url); error_message
  always defaults to "Unknown error" so the required field can't KeyError. Gating logic
  (monitored plans + first-failure-only) is untouched.

  ### Must fix (1)
  - **No `timeout=` on `requests.post`** (onboarding_slack.py ~line 90). Both sibling
    implementations pass `timeout=10` (slack_digest.py defines SLACK_REQUEST_TIMEOUT_S = 10;
    notify_portfolio_drift passes timeout=10). The docstring claims "a Slack outage must not
    break the failure-handling path" — but `requests` has NO default timeout, so a Slack
    network hang blocks the Celery worker thread indefinitely. That's a *hang*, not an
    exception, so neither the local try/except nor the task-level try/except saves you.
    Add `timeout=10` to match the precedents and honour the docstring's own promise.

  ### Confirm before merge (deploy-sequencing risk)
  - **Coverage can go fully dark on deploy.** This PR deletes the email path AND defaults
    SLACK_ONBOARDING_FAILURES_CHANNEL_ID to "" (settings/base.py). If the env var isn't set
    in the prod environment at deploy time, failure alerts produce *nothing* — no email, no
    Slack, just a `no_channel_id` warning log nobody watches. The PR's own "Open items"
    already flags baking in the real channel ID; treat that as a merge blocker, not a
    follow-up, and confirm (a) the channel ID is set in prod config and (b) the VOICE_AI_LOG
    bot is a member of that channel. Otherwise you silently lose the Wyndham onboarding-failure
    alert stream the PR set out to improve.

  ### Nits (optional)
  - No test asserts the never-raises-on-outage behaviour (post raises HTTP error / non-ok →
    swallowed). The configured/unconfigured/skip paths are covered well; a "doesn't propagate
    on Slack failure" test would lock in the core safety claim.
  - On a non-ok Slack response the code does `raise Exception(...)` then immediately catches it
    into `logger.exception`. Works, but the precedents log a structured `error=response_data.get("error")`
    field instead — nicer for alerting-on-the-alerter. Minor.

  Testing status per PR body: ruff/pyright clean; pytest not run locally (no local Postgres),
  relying on CI. Worth confirming CI green on the two touched test files before merge.

  No GitHub comment posted (review recorded here only, per session rules). If you want this
  as a PR review comment, say the word and I'll draft + post on approval.
project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 15
title: review slack notifications for onboarding failures PR
updated: 2026-06-25 12:18:36.850915
waiting_on: null
waiting_since: null
working_on: false
---

https://github.com/canary-technologies-corp/canary/pull/48513