---
area: null
completed_at: 2026-11-23 17:24:22.407964
contexts:
- react
created: 2026-11-23 09:30:59.000866
defer_until: null
due: null
energy: low
id: 2026-11-23T0930-respond-on-stay-6027-how-many-of-the-147-had-push
order: null
output: |-
  ## Agent run 2026-11-23T14:37:53

  **Answer: all 147.** The count was already limited to hotels that push purchases to the PMS as charges.

  - The 2026-11-20 query filtered on `addons_configuration.integration_push_purchases_to_charges = true` (plus Best Western org, `has_addons`, `is_active`). It did not filter on `integration_enabled`.
  - Re-run today (read-only, `canary prod-db query canary`, US), split by both settings the ticket proposes:
    - Push to charges on + `integration_enabled` on: 148 hotels, 469 paid blank-code rows (was 147 / 467 on 2026-11-20; one hotel and two rows of drift).
    - Push to charges off + `integration_enabled` on: 2 hotels, 18 rows. These do not post charges, so the banner should not flag them.
    - Push to charges on + `integration_enabled` off: none.
  - Whole Best Western portfolio (active, `has_addons`): 1,547 hotels have both settings on, 5 have only `integration_enabled`, 85 have neither. No hotel has push on with `integration_enabled` off.
  - So the ticket's two-setting condition catches every affected Best Western hotel. About 1 in 10 push-enabled hotels (148 of 1,547) would see the banner.
  - Rows counted: enabled, not deleted, price > 0, blank code, across `addons_upsell` (kind addon, `integration_gateway_code`), `addons_earlycheckinaddon.code` and `addons_latecheckoutaddon.code`.
  - Not re-run: the "92 sold one in the last 30 days" figure. It used the same push-enabled filter on 2026-11-20.

  **Nothing posted.** Draft reply for Guillermo's comment (https://linear.app/canary-technologies/issue/STAY-6027/upsells-flag-upsells-that-have-no-pms-code-when-the-hotel-pushes#comment-4be74c69), as a reply in that thread:

  > All of them. The 147 only counted hotels with `integration_push_purchases_to_charges` on. I re-ran it today split by both settings: 148 hotels (469 rows) have both `integration_enabled` and push to charges on. 2 more hotels have blank paid codes with push off, so they are fine. No Best Western hotel has push on with `integration_enabled` off, so the two-setting condition in the spec catches every affected hotel.
  >
  > For scale, 1,547 Best Western hotels have both settings on, so about 1 in 10 would see the banner.
  >
  > Agreed on the empty check first. Code validity can be a later ticket.

  The last line of the draft is my guess at your position on his validity point; cut it if you want to push for the Visual Matrix four-character check now.
project: null
source_id: https://linear.app/canary-technologies/issue/STAY-6027/upsells-flag-upsells-that-have-no-pms-code-when-the-hotel-pushes#comment-4be74c69
tags:
- morning-gtd
- linear
time_minutes: 20
title: 'Respond on STAY-6027: how many of the 147 had push to PMS enabled'
updated: 2026-11-23 17:24:22.407953
waiting_on: null
waiting_since: null
working_on: false
---

Guillermo: "for those 147 how many had the push to PMS enabled?" He noted CAN_POST_FREE_UPSELLS, says code-validity checks are much more work than the empty check, and legacy addons are being migrated. Issue: https://linear.app/canary-technologies/issue/STAY-6027/upsells-flag-upsells-that-have-no-pms-code-when-the-hotel-pushes
https://linear.app/canary-technologies/issue/STAY-6027/upsells-flag-upsells-that-have-no-pms-code-when-the-hotel-pushes#comment-4be74c69