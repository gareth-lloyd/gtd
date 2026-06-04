---
area: null
contexts:
- react
created: 2026-06-03 12:19:45.972995
defer_until: null
due: null
energy: medium
id: 2026-06-03T1219-follow-up-on-bwh-loyalty-member-specific-check-in
order: null
output: |
  ## Agent run 2026-06-03T11:54Z

  **Status: largely handled by the team already — main gap is no PR yet + copy sign-off + the rerun across BWHs. Probably not Gareth's to drive (assigned to Tincho), but here's the full picture.**

  ### What happened
  - BWH loyalty-member check-in SMS/WhatsApp templates lost the line
    "Thank you for being a Best Western Rewards member, we look forward to seeing you soon!"
  - Root cause: PR #42883 (ENT-5813, "BW member check in template update", merged 2026-04-08).
    It intentionally changed "check in" -> "pre-register" for loyalty members, but ALSO
    stripped the BWR-member sentence to "align with the non-member template style".
    Per Andrea, only the check-in->pre-register change was intended; removing the
    Rewards line was a mistake.
  - Net effect: the loyalty-member template became byte-for-byte identical to the
    non-member template (verified locally) — i.e. the loyalty variant lost its only
    differentiator.

  ### Tracking
  - Linear: ENT-6412 "Loyalty member check-in SMS messages content" (Enterprise team,
    High priority, project "Migrate BWH Guest Journey Messages to new Segmentation model").
    Status: **Todo** as of this run. Assignee: Tincho Martin Rodriguez.
    AC: (1) loyalty sentence added back, (2) configuration scripts rerun, (3) validated.

  ### Fix state (verified in repo)
  - Tincho already committed the fix on remote branch
    `tinchomartinrodriguez/ent-6412-missing-loyalty-member-check-in-sms-messages`
    (commit 00bb1418091 "Restore BW Rewards member line in loyalty check-in templates").
  - I verified the diff: it re-adds the Rewards sentence in en/de/es/fr SMS + WhatsApp
    templates while KEEPING the "pre-register" wording, and flips the test assertions
    back (test_best_western_guest_journey_messages_provider.py). This is the correct fix.
  - **No PR has been opened for this branch yet** (gh pr list for ENT-6412 = empty).
    No tests run by me on the branch.

  ### What still needs to happen (the actual "follow up")
  1. Open the PR from Tincho's branch and get it merged + deployed.
  2. Copy validation BEFORE merge — in the thread Connor flagged (reply 18) that the
     Notion/Google-doc copy "still isn't exactly matching the doc Melissa had shared".
     Source-of-truth churn is the real friction here; Andrea started a Notion page
     "BW Guest journey Templates" to consolidate. Get final English copy signed off by
     Connor/Melissa before merge.
  3. Re-run the configuration scripts/plan across all EXISTING BWH properties (template
     change alone does not retroactively update already-migrated hotels) — the team
     planned to bundle this with the email-template update at "end of week / beginning
     of next week" (~week of 2026-06-02).
  4. Confirm new BWH onboarding picks up the corrected template going forward.

  ### Suggestion (optional)
  - Add a regression test asserting the loyalty-member and non-member check-in templates
    are NOT identical (they were, post-#42883). Would have caught this class of "aligned
    them into being the same message" bug.

  ### Gareth's involvement
  - This is assigned to Tincho and the code fix is done; the open items are PR/merge,
    business copy sign-off, and the rerun. If you're not driving it, this is mostly an
    awareness/nudge item — worth a quick ping to confirm the PR gets opened and the
    rerun is actually scheduled with the email batch. No external messages sent.

  Links: ENT-6412 https://linear.app/canary-technologies/issue/ENT-6412
         Cause PR #42883 https://github.com/canary-technologies-corp/canary/pull/42883
         Slack thread https://canarytechnologies.slack.com/archives/C07BX379GQK/p1780426260969329
project: null
source_id: https://canarytechnologies.slack.com/archives/C07BX379GQK/p1780426260969329?thread_ts=1780426260.969329&cid=C07BX379GQK
tags:
- morning-gtd
- slack
- from-awareness
time_minutes: 20
title: Follow up on BWH loyalty member-specific check-in SMS overwritten in migration
updated: 2026-06-03 14:58:33.972098
waiting_on: null
waiting_since: null
working_on: false
---

Connor + Melissa spot-checked migrated BWH messages; member check-in SMS lost the BWR-member line. Likely needs another change run across BWHs. https://canarytechnologies.slack.com/archives/C07BX379GQK/p1780426260969329?thread_ts=1780426260.969329&cid=C07BX379GQK