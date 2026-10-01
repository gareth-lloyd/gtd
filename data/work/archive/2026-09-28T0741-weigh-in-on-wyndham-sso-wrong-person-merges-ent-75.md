---
area: null
completed_at: 2026-10-01 14:56:34.628498
contexts:
- react
created: 2026-09-28 07:41:13.876749
defer_until: null
due: 2026-09-28
energy: medium
id: 2026-09-28T0741-weigh-in-on-wyndham-sso-wrong-person-merges-ent-75
order: null
output: |-
  ## Agent run 2026-09-29T09:19:39Z

  ### The decision moved since this item was captured
  - Ryan canceled ENT-7582 on Sep 28 21:57Z (https://linear.app/canary-technologies/issue/ENT-7582/sso-email-merge-attaches-the-wrong-person-at-shared-mailbox-properties) and closed both name-match PRs unmerged: #57161 (https://github.com/canary-technologies-corp/canary/pull/57161) and #57814 (https://github.com/canary-technologies-corp/canary/pull/57814).
  - Outcome: wait for self-serve linking, ENT-6542 (https://linear.app/canary-technologies/issue/ENT-6542/self-service-sso-account-linking-let-users-bind-their-existing-canary).
  - The Slack thread has had no reply since Connor on Sep 25 (https://canarytechnologies.slack.com/archives/C0B1MN8F869/p1790348854630699?thread_ts=1790348854.630699&cid=C0B1MN8F869). You have not replied in it.
  - So a vote on options 1 to 5 is late. What is still open, per Ryan's cancel comment: the 5 wrong merges, the ongoing 409s, and the eng design and estimate Andrea asked for.

  ### Recommended position
  1. Agree with waiting, but "wait" has no date. ENT-6542 is in Backlog with no priority, no assignee, and the label "Blocked: Needs Design". As written it only covers the password-first direction (log in with password, then link). ENT-7582 needs the SSO-first direction, which is Lauta's caveat. Until that ships, about 1 wrong merge a week and about 7 lockouts a week continue. Ask for an owner and an estimate with the login side in scope.
  2. Make the silent failure visible in the meantime. Every merge logs `sso.merge_with_existing_user.success`. Wyndham US had 19 in 30 days, so a Groundcover monitor on that event for the Wyndham org, where the email differs from the name id, is a reviewable volume. It guesses nothing about identity and catches a wrong merge in days instead of never.
  3. Repair the 5 rather than leave them, after a per-account check. Reasons: each day the new person adds history to the wrong account, which makes separation harder later; ENT-6542 will not fix them retroactively; and about 1 more a week will arrive, so a repeatable runbook is needed anyway.

  ### What the repair has to do (from the code)
  - Clearing the name id alone is not enough. `merge_with_existing_user` (backend/canary/sso/services/sso_organization.py:232) picks any account in the org with the same email and a blank name id, so the old account becomes a merge candidate again on the next login, or pushes the user into a 409.
  - The merge also overwrote first name, last name and email on the old account through `update_user_details` (sso_organization.py:1061), which is why 2 of the 5 are only inferred from usernames.
  - Per account, in one transaction:
    - Confirm the prior owner from the legacy username and pre-merge event history.
    - Move the name id to a fresh account for the new person.
    - Take the old account out of the candidate pool (its email is the shared mailbox).
    - Restore the old account's name.
  - Check first whether the prior owner still uses password login on that account. Ryan's comment says password login is still enabled on the org. If so, two people are sharing one account today and that one is urgent.
  - Accounts: 3720766, 3722774, 3593477 confirmed; 3636016, 3593493 inferred.
  - This is a production write. I did not run or draft a script. It needs your explicit go-ahead and an owner.

  ### Two code facts worth raising
  - `merge_user_accounts` help text says it is "Only available when the Name ID format is set to 'email'" (backend/canary/sso/models/organization.py:153). At Wyndham the email is the property mailbox and differs from the name id, so the merge runs outside its documented precondition.
  - Deleted users stay in the pool. `_delete_user` (backend/canary/hotel_staff/services/hotel_staff_user.py:753) sets `is_active=False` and renames the username, but keeps the email, the SSO org and the blank name id. `_find_user_to_merge` has a second pass over inactive accounts (sso_organization.py:282). One deleted account on the mailbox gets merged into; two or more give a 409. The six deleted accounts at 04219 are this case. Excluding deleted accounts from that pass is a rule about account state, not a guess about identity, so it may fit the team's objection to option 2. The inactive pass looks deliberate, so check why it exists before proposing this.

  ### Not verified
  - No production data checked. Teleport session is expired and the canary MCP servers failed to connect. I did not use the Snowflake mirror in this session because outbound tools are loaded.
  - How many of the 15 lockouts came from the inactive pass versus 2+ active accounts.
  - What happens at login after a merge into an inactive account (whether it is reactivated).
  - I did not read the diffs of the closed PRs.

  ### Draft Slack reply (NOT sent, for the thread above)
  > Late to this, and I agree with waiting for linking over a login-time rule. Three things I'd add:
  > 1. ENT-6542 has no owner or estimate and is written for the password-first direction only. The Wyndham case needs the SSO-first side too, as Lauta said. Can we get an owner and a rough estimate so "wait" has a date?
  > 2. Until then, can we alert on `sso.merge_with_existing_user.success` for Wyndham where the email isn't the name id? It's about 19 a month, so reviewable, and it stops the wrong merges being silent.
  > 3. On the 5 existing ones, I'd repair rather than leave them. The new person keeps adding history to someone else's account and linking won't fix that retroactively. The repair has to move the name id to a fresh account and take the old account off the shared email in the same step, or the next login re-merges or 409s. Worth checking first whether any prior owner still logs in with a password on those accounts.
  > Separate question: deleted users stay merge candidates (they keep the email and a blank name id). Is there a reason the merge looks at inactive accounts at all?
project: 2026-04-16T1210-unblock-team
source_id: https://canarytechnologies.slack.com/archives/C0B1MN8F869/p1790348854630699?thread_ts=1790348854.630699&cid=C0B1MN8F869
tags:
- morning-gtd
- slack
time_minutes: 15
title: Weigh in on Wyndham SSO wrong-person merges (ENT-7582)
updated: 2026-10-01 14:56:34.628493
waiting_on: null
waiting_since: null
working_on: false
---

Ryan asked the team for thoughts: 5 of the last 19 Wyndham merges landed in another person's account, 15 users 409'd in 14 days. Andrea, Lauta and Connor lean 'wait for self-serve linking (option 5)'. Still undecided: what to do with the 5 existing wrong merges.
https://canarytechnologies.slack.com/archives/C0B1MN8F869/p1790348854630699?thread_ts=1790348854.630699&cid=C0B1MN8F869