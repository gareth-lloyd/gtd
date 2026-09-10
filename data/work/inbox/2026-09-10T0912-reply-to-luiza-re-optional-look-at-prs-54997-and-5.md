---
area: null
completed_at: null
contexts:
- react
created: 2026-09-10 09:12:48.921431
defer_until: null
due: null
energy: low
id: 2026-09-10T0912-reply-to-luiza-re-optional-look-at-prs-54997-and-5
order: null
output: |
  ## Agent run 2026-09-10T08:23:03Z

  Read both diffs, all review threads, and the Slack DM. Nothing was sent to Slack or posted to GitHub. The reply below is a draft for you to send.

  ### Status
  - PR #54997 (https://github.com/canary-technologies-corp/canary/pull/54997), SDM-4992: approved by jwhart91 and abrad. Joshua's two predicate comments (`has_pms_sync`, `credit_card_step != DISABLED`) and Macroscope's "NONE isn't a valid strategy" finding are fixed in the code. Luiza answered Andrea's question well: 330 hotels with no tree match vs about 24 with a match in 7 days, so about 93% of edited hotels got no consistency checking. **The PR body says "Needs Enterprise sign-off before merge"** for the rules-engine change: the early return is gone and consistency rules now see every key. You own that engine, so that sign-off is probably yours, and it's the one real reason to reply with substance.
  - PR #55050 (https://github.com/canary-technologies-corp/canary/pull/55050), SDM-4993: approved by jwhart91 and martinrodriguezcanary (Tincho). Joshua's review got the signal dropped in favour of a direct call from the `set_hotel_live` admin action. The Salesforce call that could block is avoided via `allow_remote_attribute_fetch=False`, which already exists on master (`hotel_config_health.py:88`). Hotel-name prefixes on the warnings are in.
  - The only CI failures on either PR are the E2E Playwright shards, which don't block merge. The PR says they fail the same way on unrelated branches.

  ### What I checked myself
  - **The two PRs conflict with each other.** A trial `git merge-tree` of the two heads conflicts in `rules_based_configuration/signals.py`: both add an import right after the `ConsistencyService` import (keep both). It also conflicts in `hotels/tests/admin/test_hotel.py`, where both append tests. Whichever PR lands second needs a quick rebase. Worth telling Luiza.
  - The engine change is low-risk today. Only two consistency rules exist on master, both in `check_in/configuration_rules/consistency_rules.py`: `payment_gateway_required_for_tokenization` and `id_step_required_for_additional_guests_id`. Both fire only on real misconfiguration. The tokenization rule is the one that could produce new warnings on the ~330 hotels outside the trees.
  - Cost per save: about 228 related-config keys plus Hotel's own fields, all attribute reads after 4 related-object lookups. Cheap.
  - Optional nit, not sent: a missing related config makes `ConformityService.get_actual_hotel_setting` log one `get_actual_hotel_setting.attribute_not_found` info line per key. Django's `RelatedObjectDoesNotExist` subclasses `AttributeError`. On every Hotel or Auth admin save, a hotel without a check-in config would log 138 lines, and one without a membership-gateway config would log 6. That's log noise only, nothing breaks. It could be a follow-up that short-circuits once per prefix.

  ### Draft reply (DM D0BTZ2ALLBE, reply to https://canarytechnologies.slack.com/archives/D0BTZ2ALLBE/p1788961038094659)
  > Had a look at both, they look good to me 👍
  >
  > *#54997*: happy to give the Enterprise sign-off on the conformity-tree change. Dropping the early return and running consistency rules against the full key set is the right call, and the 93% no-tree-match number makes the case well. There are only the two check-in rules live today so the new warnings should be small, but worth watching how often `payment_gateway_required_for_tokenization` fires on non-tree hotels in the first week.
  >
  > *#55050*: calling it straight from the admin action and keeping it offline with `allow_remote_attribute_fetch=False` both look right.
  >
  > One heads-up: the two PRs conflict with each other in `rules_based_configuration/signals.py` (both add an import after `ConsistencyService` — just keep both) and at the end of `hotels/tests/admin/test_hotel.py`, so whichever lands second needs a quick rebase.

  Edit the sign-off line if you'd rather not be the Enterprise approver, or want to leave a GitHub approval instead of a Slack note.
project: null
source_id: https://canarytechnologies.slack.com/archives/D0BTZ2ALLBE/p1788961038094659
tags:
- morning-gtd
- slack
time_minutes: 10
title: 'Reply to Luiza re: optional look at PRs #54997 and #55050'
updated: 2026-09-10 11:23:03.000000
waiting_on: null
waiting_since: null
working_on: false
---

Andrea and Tincho already approved; she offered them in case I want to check.
https://github.com/canary-technologies-corp/canary/pull/54997
https://github.com/canary-technologies-corp/canary/pull/55050
https://canarytechnologies.slack.com/archives/D0BTZ2ALLBE/p1788961038094659