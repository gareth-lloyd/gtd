---
area: null
contexts:
- react
created: 2026-05-11 21:46:22.808145
defer_until: null
due: null
energy: medium
id: 2026-05-11T2146-review-pr-44332-ent-6055-disable-email-on-bw-post
order: null
output: '## Agent run 2026-05-12T15:00Z


  **Verdict:** Ready to merge from a code perspective. PR is already APPROVED (rrgrs,
  2026-05-11). All six of rrgrs''s pre-merge items are addressed in the diff. One
  off-PR operational item (CS confirmation) is the only thing I can''t verify from
  here — flag below.


  **State**

  - Title: "ENT-6055 Disable email by default on BW non-pilot variants + manual-enable
  allowlist" (mergeable, APPROVED, auto-deploy label set).

  - Last commit aa5d406 (2026-05-11 20:01Z) added the Notion source-of-truth link.

  - CI: bulk CANCELLED entries are merge-queue churn from the re-trigger after aa5d406,
  not real failures. Playwright E2E shard 1/4 FAILURE is flagged non-blocking per
  the bot comment. Re-run before merge if it stays red.


  **rrgrs items — status after the latest commit**

  1. Stale title → renamed; new title covers placeholder fix + cascade + allowlist.
  ✅

  2. Re-run strips manually-enabled non-check-in email rows on non-allowlist hotels
  → docstring in `manually_enabled_email_hotels.py` calls this out ("Re-running onboarding
  doubles as the cleanup operation"). **Still no on-thread confirmation that CS/BW
  account managers know.** This is the only outstanding item — the 20 hotels marked
  `[3-msg]` in the allowlist plus an unknown number of non-allowlist hotels with checkout/welcome
  email manually enabled will silently lose those `email_template` rows on next rerun.
  Worth a one-liner from Martin on the PR or a Slack screenshot confirming Mel/CS
  has acknowledged before this merges. ⚠️ off-PR

  3. Inline `from unittest.mock import patch` in tests → refactored to use the pytest
  `monkeypatch` fixture; no inline imports remain in the new tests. ✅

  4. `_propagate_email_override` — explain why both layers exist → added an inline
  docstring on the helper and a 4-line comment at the call site pointing to `configure_guest_journey_messages.py:444`.
  ✅

  5. Promote helper to shared util alongside IHG''s `_with_email_disabled` → not done;
  rrgrs marked this non-blocking. Reasonable to defer — IHG''s helper only handles
  False, this one cascades either polarity, so a true shared util wants a small refactor
  on IHG''s side too. Worth a follow-up ticket but not a merge blocker.

  6. Link source of truth for the hotel list → Notion page created and linked at top
  of `manually_enabled_email_hotels.py`. ✅


  **Code spot-checks I did**

  - `_propagate_email_override` is correctly applied to check-in main + reminder,
  checkout, and welcome variants. Reminder uses `check_in_spec.reminder` (not `check_in_spec`),
  which is the right spec to read `override_enable_email` from. ✅

  - For `MANUALLY_ENABLED_EMAIL_HOTELS`, `check_in_spec = replace(BW_CHECK_IN_MESSAGE_SPEC,
  override_enable_email=True)` keeps the 1-day timing/title intact, distinct from
  `BW_CHECKIN_EMAIL_MESSAGE_SPEC` (which is the pilot''s 2-day branch). Matches the
  table in the PR body. ✅

  - The two placeholders (`POST_CHECK_OUT_MESSAGE`, `MID_STAY_MESSAGE`) get `override_enable_email=False`
  even though they''re `DISABLED_IF_CREATED`. Necessary because `_sync_schedule_spec_channel_flags`
  still reads the schedule_spec channels on those rows. Test `test_post_check_out_and_mid_stay__email_channel_disabled`
  covers it. ✅

  - Allowlist contents look sane: 2 EU + 35 US = 37, matches the body. Hotel 16107
  (Omaha Airport Inn) is in the list, matching the original ENT-6055 description ("Property
  16107 should be the only one with email sending active" — note this is now stale;
  per the rerun-script work, 36 more hotels are also legitimately email-enabled and
  the allowlist is the formal record of that).


  **Recommendation to user**

  - The remaining gate is operational, not code. Nudge Martin (or check in #ent-platform
  / wherever) for an explicit "Mel/CS confirmed they know about the strip-on-rerun
  behavior" before letting this auto-deploy on merge. Once that''s logged, this is
  fine to merge.

  - Optional follow-up ticket: pull `_propagate_email_override` + IHG''s `_with_email_disabled`
  into a single helper on `configs/guest_journey_message.py`. Non-urgent.


  **No new review comment posted** — outstanding item is operational and the PR is
  already approved. Defer to user on whether to nudge on the PR or via Slack.

  '
project: null
source_id: https://github.com/canary-technologies-corp/canary/pull/44332
tags:
- morning-gtd
- github
time_minutes: 20
title: 'Review PR #44332: ENT-6055 Disable email on BW post-checkout/mid-stay placeholders'
updated: 2026-05-12 14:44:39.668933
waiting_on: null
waiting_since: null
working_on: false
---

Re-review requested by canary-review-bot after @rrgrs raised pre-merge operational items.
https://github.com/canary-technologies-corp/canary/pull/44332