---
area: null
contexts: []
created: 2026-07-16 13:30:51.394603
defer_until: null
due: null
energy: low
id: 2026-07-16T1330-review-and-respond-to-james
order: null
output: |
  ## Agent run 2026-07-16T13:33:01

  James (DM: https://canarytechnologies.slack.com/archives/D0B1X0GJQSZ/p1784197824980009)
  wants a second opinion on his permission-structure justification in PR #50416
  (https://github.com/canary-technologies-corp/canary/pull/50416, MOB-997 — mints the 6
  Service Tickets permissions + registers the product; enforcement follows in MOB-885).

  **Verdict: his justification is valid.** Reviewed the diff and checked his claims
  against the codebase:

  - His precedent claim ("permissions already deduce behaviour, not just gate actions")
    is real: `voice/selectors/recap.py` picks recap recipients from holders of
    VOICE_CAN_MANAGE_AI; `push_notifications/tasks/send_staff_push.py` routes pushes by
    MESSAGES_HAS_PRODUCT_ACCESS; credit-card security + authorization notifications pick
    audiences the same way. So `can_be_assigned` / `can_bypass_auto_assignment` as
    behaviour markers is not a break from existing practice.
  - Breaking out `can_be_assigned` instead of inferring from a manager perm is the
    better call — inference would couple assignment eligibility to admin powers with no
    way to make a role unassignable.
  - Permissions beat a separate admin surface: a parallel per-role settings table would
    drift from roles and give admins two places to manage one concept.
  - Strength-tier placement checks out (manage=ADMIN; assign/bypass=POWER_USER;
    access/create/be-assigned=STAFF), and default-role placement is coherent.
  - One watch-item (non-blocking): `can_bypass_auto_assignment` inverts the usual
    "more grants = more capability" model (granting it removes you from round-robin).
    Role-editor copy in MOB-885 should make the effect obvious — an admin ticking it
    for everyone silently breaks auto-assignment.

  **Draft Slack reply (NOT sent — awaiting your approval):**

  > Had a look — I think your justification holds up. There's genuine precedent for
  > permission-presence driving behaviour: voice recap recipients are selected from
  > VOICE_CAN_MANAGE_AI holders (voice/selectors/recap.py), staff push routing filters
  > on MESSAGES_HAS_PRODUCT_ACCESS (push_notifications/tasks/send_staff_push.py), and
  > the CC-security/authorization notifications pick their audience the same way. So
  > you're following an established pattern, not introducing one.
  >
  > Breaking out can_be_assigned rather than inferring it from a manager perm is the
  > right call too — inference would couple assignment eligibility to admin powers and
  > leave no way to make a role unassignable. And I agree permissions beat a separate
  > admin surface; a parallel per-role settings table would just drift from roles.
  >
  > One thing to be deliberate about in MOB-885: can_bypass_auto_assignment is a grant
  > that *reduces* what happens to you (skipped by round-robin), which inverts the usual
  > "more permissions = more capability" mental model in a role editor. The "bypass"
  > naming helps, but make sure the role-editor copy makes the effect obvious — an admin
  > ticking it for every role silently breaks round-robin.

  To send: reply in the DM thread (channel D0B1X0GJQSZ, thread_ts 1784197824.980009).
project: null
source_id: null
tags: []
time_minutes: 5
title: review and respond to james
updated: 2026-07-16 14:49:57.043653
waiting_on: null
waiting_since: null
working_on: false
---

https://canarytechnologies.slack.com/archives/D0B1X0GJQSZ/p1784197824980009