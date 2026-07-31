---
area: null
contexts:
- react
created: 2026-07-31 10:56:46.374152
defer_until: null
due: null
energy: medium
id: 2026-07-31T1056-review-pr-51433-tool-470-dedup-product-change-call
order: null
output: |
  ## Agent run 2026-07-31T11:19
  Reviewed PR #51433 (https://github.com/canary-technologies-corp/canary/pull/51433) — Ramiro's TOOL-470 dedup fix. Verdict: LGTM, recommend approving. No blocking or non-blocking findings.

  What the PR does: in `HotelProductsPlan.execute`, collapses `config.all_products` (set of Salesforce `ProductType`) through `PRODUCT_TYPE_TO_CANARY_PRODUCT` into a set of `CanaryProducts` before calling `HotelService.change_product_state`, so each product-change callback fires once per CanaryProduct instead of once per ProductType. Plus a regression test.

  Verification performed locally (not just read):
  - Confirmed the duplication is real: the mapping in `onboarding/salesforce.py` sends 5 ProductTypes to AUTHORIZATIONS and 3 to CHAT; `change_product_state` enqueues a Celery task per registered callback with unique SQS dedup IDs, so duplicate calls genuinely enqueued duplicate async tasks (guest-journey seeding, kiosk card seeding etc.).
  - Ran the new test on the PR head: passes.
  - Ran the new test against master's version of hotel_products_plan.py: fails exactly as claimed (4 calls, AUTHORIZATIONS fired 3x) — it's a genuine regression test.
  - Semantics preserved: the `.get() is not None` filter still excludes ignored ProductTypes (_KIOSK, _MOBILE_KEYS...); ordering was already nondeterministic (all_products is a set), so set iteration changes nothing; the add-products path (`OnboardingService.activate_hotel_products`) already dedups the same way, so this aligns creation with it.
  - Style checks out: walrus parenthesized per repo rules, comment explains why, test extends the existing class-based suite with the file's conventions (`# Act` only, autospec patches, existing stubs).
  - CI: everything passes except `review-bot`, which only fails because required human reviews are missing (gareth-lloyd is on the required list — that's why Ramiro asked). Branch is 164 commits behind master; merge queue handles that.

  NOT done (needs your approval): no GitHub review/approval was submitted. If you want, say the word and I can submit an approval, or you can approve at https://github.com/canary-technologies-corp/canary/pull/51433
project: null
source_id: https://github.com/canary-technologies-corp/canary/pull/51433
tags:
- morning-gtd
- github
time_minutes: 20
title: 'Review PR #51433: [TOOL-470] Dedup product change callbacks in HotelProductsPlan'
updated: 2026-07-31 12:47:02.823724
waiting_on: null
waiting_since: null
working_on: false
---

Personally requested by Ramiro (with Laura). https://github.com/canary-technologies-corp/canary/pull/51433