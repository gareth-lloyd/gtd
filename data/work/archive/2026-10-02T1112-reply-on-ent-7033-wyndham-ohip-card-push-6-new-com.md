---
area: null
completed_at: 2026-10-02 13:01:38.545278
contexts:
- react
created: 2026-10-02 11:12:14.607222
defer_until: null
due: null
energy: low
id: 2026-10-02T1112-reply-on-ent-7033-wyndham-ohip-card-push-6-new-com
order: null
output: |
  ## Agent run 2026-10-02T09:28:16Z

  **Nothing was posted. No reply is owed; one optional reply is drafted below.**

  ### Where the thread stands
  ENT-7033 (https://linear.app/canary-technologies/issue/ENT-7033/wyndham-ohip-50-hotels-failing-check-in-card-push-payment-method-is) is In Progress, Andrés owns it. The 6 new comments are all between Andrés and Andrea Bradshaw, 2026-10-01:
  - Andrés (https://linear.app/canary-technologies/issue/ENT-7033/wyndham-ohip-50-hotels-failing-check-in-card-push-payment-method-is#comment-84588b50): Wyndham confirmed the remaining failing hotels have no payment terminals integrated with Opera, so Chip and PIN off is correct. The failures come from `authorization_configuration.pms_payment_method_strategy=tokenize`: Opera rejects tokens when `ChipPinYN` and `AuthAtCheckinYN` are both N, and accepts card numbers. About 250 auth forms failed in 30 days. He proposes (1) set the 8 hotels to `raw_cc`, pilot one first, and (2) make go-live set tokenize only where Opera accepts tokens.
  - Andrea asked whether the strategy is set at onboarding and whether the scripts can know. Andrés: yes, go-live sets it unconditionally; the scripts could check Opera's LOV first. Andrea asked for a sub-ticket. Andrés: "Will do!"
  - He did: ENT-7732 (https://linear.app/canary-technologies/issue/ENT-7732/check-opera-token-acceptance-before-wyndham-go-live-sets-tokenize), In Progress, child of ENT-7033.
  - ENT-7627 (the Wyndham chip-flag escalation, https://linear.app/canary-technologies/issue/ENT-7627/escalate-to-wyndham-enable-chip-and-pin-at-9-hotels-where-every-card) was closed Done on 2026-10-01. ENT-7625 and ENT-7626 were already Done.

  ### What I checked in the code (master, read-only)
  - Go-live sets tokenize unconditionally for any hotel with an integration key: `backend/canary/onboarding/configuration_providers/wyndham/wyndham_go_live_provider.py:94-95`.
  - The Wyndham rule for this field is `OverridePolicy.FREE`: `backend/canary/enterprise_wyndham/configs/wyndham.py:346-350`. FREE keys are excluded from conformity and drift checks (`rules_based_configuration/services/conformity.py:345-351`, `drift.py:132`). So a hand-set `raw_cc` will not be flagged or reverted by the rules engine. The rule does not need to change for the fix to hold.
  - The only thing that reverts a hand-set `raw_cc` is re-running the Wyndham go-live step on that hotel before ENT-7732 ships.
  - Every auth-side push path reads the same field (`authform/services/pms_operations.py:326, 707, 1110`, `authform/views/push_card_to_pms.py:137`, `payment_links/services/payment_link_pms_operations.py:242`), so one field change covers them all.

  ### Two gaps I see in the plan (not verified against prod data)
  1. **The 8 hotels are probably not the whole exposed set.** Go-live puts tokenize on every hotel with an integration key, and Andrés's audit found 338 chip-off hotels. ENT-7732's evidence only covers the 1,123 hotels that made token pushes between 31 Aug and 1 Oct. A chip-off hotel on tokenize that sent no auth form in that window fails on its first one. I could not count that set: the chip-off list lives in Andrés's audit output, and the canary prod MCP servers were down this session.
  2. **12 vs 8.** ENT-7732 says 12 hotels fail on every token push, and lists "fixing the 8 hotels that fail today" as out of scope. The ticket does not say what the other 4 are.

  ### Draft reply (optional, NOT posted — say "yes, post it" if you want it sent)
  Destination: reply in the 2026-09-24 thread on ENT-7033, under Andrés's update.

  > Good find on tokenize. Two questions on the plan:
  >
  > 1. Is 8 the whole set? Go-live sets tokenize on every hotel with an integration key, and the audit found 338 chip-off hotels. The 8 are the ones that sent auth forms recently. Any other chip-off hotel on tokenize fails on its first auth push. Worth switching every hotel that is both chip-off and on tokenize, not only the 8. ENT-7732 also counts 12 that fail every token push. What are the other 4?
  > 2. Until ENT-7732 ships, re-running go-live on a switched hotel puts it back on tokenize (`wyndham_go_live_provider.py:95`). The Wyndham rule for this field is FREE, so the rules engine will not flag or revert `raw_cc`.

  ### Other things you may want to do yourself
  - The ENT-7033 description (you wrote it) still says the root cause is Opera-side config that Wyndham must fix, and still carries the "Ask (Wyndham)" section. Both are now wrong. Andrés may update it; otherwise it will mislead the next reader.
  - Marta Ziaei offered on 2026-09-29 in #wyndham to take the chip-flag request to Wyndham corporate. That request is now moot. I did not check whether anyone told her.
  - My memory file on this issue (`project_ent5610_wyndham_payment_posting.md`) is stale on the same points. I have not updated it; say so if you want it refreshed.
project: null
source_id: https://linear.app/canary-technologies/issue/ENT-7033/wyndham-ohip-50-hotels-failing-check-in-card-push-payment-method-is#comment-84588b50
tags:
- morning-gtd
- linear
time_minutes: 10
title: 'Reply on ENT-7033: Wyndham OHIP card push, 6 new comments'
updated: 2026-10-02 13:01:38.545269
waiting_on: null
waiting_since: null
working_on: false
---

6 new comments. Andrés: Wyndham confirmed the remaining failing hotels have no payment terminals integrated with Opera, so Chip and PIN off is correct; the failures come from pms_payment_method_strategy=tokenize. Plan: check Opera's LOV in the scripts before setting tokenize (now ENT-7732, In Progress). Latest: Andrés 'Will do!'. Nothing addressed to you.
https://linear.app/canary-technologies/issue/ENT-7033/wyndham-ohip-50-hotels-failing-check-in-card-push-payment-method-is