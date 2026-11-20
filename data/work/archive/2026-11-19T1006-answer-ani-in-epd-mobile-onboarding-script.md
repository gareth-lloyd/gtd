---
area: null
completed_at: 2026-11-19 15:34:33.565319
contexts:
- react
created: 2026-11-19 10:06:55.957131
defer_until: null
due: null
energy: medium
id: 2026-11-19T1006-answer-ani-in-epd-mobile-onboarding-script
order: null
output: |-
  ## Agent run 2026-11-19T12:47:20

  **Bottom line: Ani was not asking you anything. No reply is owed.** Nothing was sent to Slack.

  Read in context, "@Gareth onboarding script" answers Francisco's question directly above it: "When you say 'MSA go live run', do you mean the go-live step of our onboarding scripts, or the hotel's Salesforce opportunity is marked LIVE/COMPLETE?" Ani tagged you (you had just said Enterprise can advise) but the content is the answer to Francisco: use the onboarding go-live script, not `is_live`.
  Message: https://canarytechnologies.slack.com/archives/C09M5GRJPL2/p1794934826665329?thread_ts=1790006579.628339&cid=C09M5GRJPL2

  What happened after it, all without you:
  - Francisco proposed a new one-time backfill plus an onboarding change keyed on "go-live script has run, or Salesforce says live" instead of `is_live`. Ani: "Yes, thank you!!"
  - Ani confirmed tipping stays on for hotels live on Wyndham Tipping but not yet GMS. Andrea pointed to `can_be_tipped` on the tip config.
  - Francisco opened PR #65534 (https://github.com/canary-technologies-corp/canary/pull/65534), Linear MOB-1635 (https://linear.app/canary-technologies/issue/MOB-1635), under MOB-1470 (https://linear.app/canary-technologies/issue/MOB-1470).
  - Ani asked "is this in"; Francisco: needs Andrea's re-review, then merge and backfill. Ani: "Thank you". These are the last messages in the thread.

  PR #65534 state, checked 2026-11-19:
  - Open, mergeable, not merged. Last push 2026-11-18 16:46 UTC.
  - Diana Perez approved 2026-11-18 12:27 UTC, before that last push. GitHub shows APPROVED, but the "Needs 1 approval from @pod-enterprise" check and "Birdline policy" are failing.
  - Andrea (abrad) has only commented (2026-11-17) with one [Blocking] point: a past Salesforce go-live date counted as live even when status was still CONFIGURATION. Francisco's 2026-11-18 commit ("Count a hotel live on GMS by its opportunity's status") addresses it. Andrea's review is re-requested and still pending, so the PR is waiting on Andrea only.
  - You cannot unblock it: your approval does not clear the pod-enterprise gate.

  Your concern from the thread is covered. You flagged that `is_live` is wrong for an existing hotel moving onto the Wyndham MSA. The PR drops `is_live` for any hotel with an open Wyndham MSA opportunity.

  One difference from what Ani agreed to, for awareness: Francisco's Slack proposal said "Salesforce go-live date has passed" for hotels that predate the script. After review the PR uses opportunity status LIVE or COMPLETE with no opt-out, whatever the date. That is stricter on slipped go-lives and looser on hotels set live early. Both reviewers pushed it that way; I don't think it needs raising with Ani.

  Also out of scope in the PR: Wyndham Connect Plus-only hotels keep the `is_live` rule.

  Optional reply, only if you want to close the loop (draft, NOT sent):
  > Catching up here: agreed on keying off the onboarding go-live rather than `is_live`, that covers the existing-hotel case I raised. #65534 is waiting on @Andrea's re-review, then Francisco merges and runs the backfill.

  Suggested next step: none needed from you. If you want it to move faster, the lever is nudging Andrea on the re-review.
project: null
source_id: https://canarytechnologies.slack.com/archives/C09M5GRJPL2/p1794934826665329?thread_ts=1790006579.628339&cid=C09M5GRJPL2
tags:
- morning-gtd
- slack
time_minutes: 15
title: 'Answer Ani in #epd-mobile: onboarding script'
updated: 2026-11-19 15:34:33.565303
waiting_on: null
waiting_since: null
working_on: false
---

Ani wrote "@Gareth onboarding script" in the long-running SDK thread. Francisco's PR #65534 is waiting on Andrea's re-review, then merge and backfill. Thread not read in full. Open 1 day, no reply from me.
https://canarytechnologies.slack.com/archives/C09M5GRJPL2/p1794934826665329?thread_ts=1790006579.628339&cid=C09M5GRJPL2