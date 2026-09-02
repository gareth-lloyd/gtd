---
area: null
completed_at: null
contexts:
- react
created: 2026-09-01 21:37:20.576463
defer_until: null
due: 2026-09-02
energy: medium
id: 2026-09-01T2137-reply-to-luiza-re-rebase-or-supersede-draft-pr-428
order: null
output: |
  ## Agent run 2026-09-01T22:05

  DECISION: (1) Luiza rebases and lands #42860 herself, under SDM-4990. Not (2): I'm not in this area this block and she's blocked on me. Not (3): the six rules are done, tested (21 tests, 100% new-line coverage), and the rebase cost is two generated files.

  Nothing was sent. Three drafts below need your approval: Slack reply, SDM-4989 comment, ENT-6097 description fix.

  ### What I verified

  - PR #42860 (https://github.com/canary-technologies-corp/canary/pull/42860): open draft, branch gareth-lloyd/ent-5030, 5044 commits behind master, no reviews. Real commits: dfebf3a195, 56de9caf51, 724c4eefa6 (rest are master merges).
  - Dry-run merge onto master (git merge-tree): conflicts ONLY in backend/canary/rules_based_configuration/services/conformity.pyi and backend/canary/ci/deps/opinionated_state.py. Both are generated; regenerate, don't resolve. Rule code and tests merge clean.
  - Rule discovery (SDM-4989 part 2): master's rules_based_configuration/apps.py calls autodiscover_modules("configuration_rules"), so any installed app's configuration_rules/ package loads with no registration. The __init__.py re-exports in #42860 are harmless but unnecessary.
  - Keys: every hotel.authorization_configuration.* and hotel.check_in_configuration.* key the rules read still exists in master's conformity.pyi. The hotel.addons_configuration.* keys are absent from master only because #42860 is the PR that adds AddonsConfiguration to CONFIGURABLE_MODELS; regenerating the stub restores them.
  - Overlap with Luiza's PR #54997 (SDM-4992, APPROVED, https://github.com/canary-technologies-corp/canary/pull/54997): it touches check_in/configuration_rules/consistency_rules.py, setting_type_generator.py, and test_consistency.py, all of which #42860 also touches. She should land #54997 first, then rebase #42860 on top.
  - Two fixes needed in passing: precheckin_method_requires_auto_post has an inline import of check_in.models.configuration.Configuration (Canary linter warned on the PR). Rules B and C are null-presence rules ("slot is set -> auto-post on"), so per ENT-7201 (https://linear.app/canary-technologies/issue/ENT-7201) they only fire at the admin-save warn layer, never the tree/CI layer (ANY_NON_NULL sentinel). Fine for warn-only, worth a line in the PR.
  - Rule C (auth deposit slot requires integration_auto_post_cc_to_pms) overlaps SDM-4990's "posting prerequisites" bullet; extend it rather than add a sibling.
  - ENT-5030 no longer resolves in Linear (get_issue: not found). The PR is tagged to a dead ticket; re-tag the new PR to SDM-4990.
  - ENT-6097 (https://linear.app/canary-technologies/issue/ENT-6097) Background says "added six consistency rules" and "pattern + 6 rules already merged". False; still an open draft. Rules G-K and Part 2 assume they're in master. Correction drafted below.
  - Both gaps she raised are tracked: admin surfacing -> SDM-4992 (In Review, #54997 approved); HotelAttributes PMS/capability dimension -> ENT-6097 Part 2 (hotel.pms.capabilities.* synthetic settings), with SDM-4991's consistency rule as the stopgap. SDM-4991 also points at ENT-7113 for the same need.
  - SDM-4989 has no comments yet; the decision has not been recorded anywhere.

  ### DRAFT 1: Slack DM reply to Luiza (thread https://canarytechnologies.slack.com/archives/D0BTZ2ALLBE/p1788185158074229)

  Sorry for the slow answer. Yes, please take #42860 over: rebase it and land it yourself under SDM-4990. You're already in those files and I won't get to it this block.

  Notes from looking at it this morning:
  - It's ~5k commits behind master but I dry-ran the merge: the only conflicts are the two generated files (`conformity.pyi` and `ci/deps/opinionated_state.py`), so regenerate rather than resolve. The rule code and tests merge clean. Easiest path: fresh branch off master, cherry-pick the three real commits (dfebf3a195, 56de9caf51, 724c4eefa6), open a new PR against SDM-4990 (ENT-5030 no longer exists in Linear), and I'll close #42860 as superseded.
  - Land it after #54997 merges. That PR touches the same three files (check_in rules, setting_type_generator, test_consistency), so you'd otherwise conflict with yourself.
  - Rule discovery: master now has `autodiscover_modules("configuration_rules")` in `rules_based_configuration/apps.py`, so a `configuration_rules/` package in any installed app loads on its own. The `__init__.py` re-exports in the draft are harmless but not needed. That answers part 2 of SDM-4989.
  - I checked the auth and check-in keys the rules read against master's stub; they all still exist. The addons keys are missing only because this PR is what registers `AddonsConfiguration` in `CONFIGURABLE_MODELS`; regenerating the stub brings them back.
  - Two things to fix in passing: `precheckin_method_requires_auto_post` has an inline import of `Configuration` (the linter warned), and rules B and C are null-presence rules, so per ENT-7201 they'll only fire at the admin-save layer, not the tree/CI layer. Fine for warn-only, but worth a line in the PR.
  - Rule C (auth deposit slot requires `integration_auto_post_cc_to_pms`) is the one that overlaps your "posting prerequisites" rule. Extend it rather than add a sibling.

  On your two gaps, both are already covered:
  - AuthorizationConfiguration admin not surfacing warnings: that's SDM-4992, and #54997 is approved.
  - HotelAttributes has no PMS/capability dimension: ENT-6097 Part 2 proposes `hotel.pms.capabilities.*` synthetic settings for exactly that, and SDM-4991's consistency rule is the right stopgap until it exists. ENT-6097's Background wrongly says the six #42860 rules are already merged; I'll fix that today.

  I'll record the decision on SDM-4989.

  ### DRAFT 2: Linear comment on SDM-4989 (https://linear.app/canary-technologies/issue/SDM-4989)

  **Decision (Gareth, 2026-09-01): rebase and land #42860 as the starting point.** Luiza owns it; land under SDM-4990, not ENT-5030 (that ticket no longer exists).

  Findings:
  1. Dry-run merge onto master conflicts only in the two generated files (`conformity.pyi`, `ci/deps/opinionated_state.py`). Regenerate. Rules and tests merge clean. Real commits to cherry-pick: dfebf3a195, 56de9caf51, 724c4eefa6.
  2. Sequence after #54997 (SDM-4992) merges; it touches the same three files.
  3. **Rule discovery: no registration needed.** `rules_based_configuration/apps.py` calls `autodiscover_modules("configuration_rules")`, so any installed app's `configuration_rules/` package loads. The draft's `__init__.py` re-exports are unnecessary.
  4. All `hotel.authorization_configuration.*` / `hotel.check_in_configuration.*` keys the draft reads exist in master's `conformity.pyi`. The `hotel.addons_configuration.*` keys appear once the draft's `CONFIGURABLE_MODELS` change is applied and the stub regenerated.
  5. Fix in passing: inline import in `precheckin_method_requires_auto_post`. Rules B/C are null-presence rules and only fire at the admin-save layer (ENT-7201).
  6. Rule C overlaps SDM-4990's "posting prerequisites"; extend rather than duplicate.

  ### DRAFT 3: ENT-6097 description edit (https://linear.app/canary-technologies/issue/ENT-6097)

  Replace the first Background sentence:
    OLD: "PR #42860 (ENT-5030) added six consistency rules for PMS integration config dependencies, all sourced from triage tickets."
    NEW: "PR #42860 (originally ENT-5030) proposes six consistency rules for PMS integration config dependencies, all sourced from triage tickets. As of 2026-09-01 it is still an open draft; SDM is rebasing and landing it under SDM-4990 (decision recorded on SDM-4989). Rules G-K and Part 2 below assume those six rules are in master, so this ticket sequences after SDM-4990."

  Replace the prior-art bullet:
    OLD: "PR #42860 (ENT-5030) — pattern + 6 rules already merged"
    NEW: "PR #42860 (ENT-5030, draft) — pattern + 6 rules, landing via SDM-4990"

  Also add to "Relevant prior art": "ENT-7201 — decorator accepts unknown keys and the tree/CI layer cannot fail null-presence rules; affects rules G, H, J here."

  ### Next (your call)
  - Approve/edit Draft 1 and send in the DM thread.
  - Approve Draft 2 and post on SDM-4989.
  - Approve Draft 3 and edit ENT-6097.
  - Once her new PR is open, close #42860 as superseded.
project: 2026-04-16T1210-unblock-team
source_id: https://canarytechnologies.slack.com/archives/D0BTZ2ALLBE/p1788185158074229
tags:
- morning-gtd
- slack
time_minutes: 20
title: 'Reply to Luiza re: rebase or supersede draft PR #42860'
updated: 2026-09-02 11:12:43.862175
waiting_on: null
waiting_since: null
working_on: false
---

She asked 2026-08-31, I've now promised twice without answering ("I'll look shortly", then "I'll look today"). She's blocked: SDM-4989 is In Progress and SDM-4990 + SDM-4991 are blocked by it.

Her question: rebase and land #42860 herself, or build on top and leave it to me? PR is +507/-3 across 10 files, draft since 2026-04-07, untouched since 2026-06-18.

Decide: (1) she rebases and lands it, (2) I finish it, (3) supersede and SDM writes fresh under SDM-4990. Record the decision on SDM-4989 — it explicitly says to.

Also flag: ENT-6097's Background claims #42860's six rules are "already merged". They are not — still an open draft. ENT-6097's whole scope (rules G-K, hotel.pms.capabilities.*) assumes they're in master. Needs correcting.

Both gaps she raised are already tracked, tell her so:
- AuthorizationConfiguration admin not surfacing warnings -> SDM-4992, In Review
- HotelAttributes has no PMS/capability dimension -> ENT-6097 Part 2 already proposes hotel.pms.capabilities.* synthetic settings; SDM-4991's consistency rule is a stopgap for that.

https://canarytechnologies.slack.com/archives/D0BTZ2ALLBE/p1788185158074229
https://github.com/canary-technologies-corp/canary/pull/42860
https://linear.app/canary-technologies/issue/SDM-4989
https://linear.app/canary-technologies/issue/ENT-6097