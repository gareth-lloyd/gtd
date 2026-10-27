---
area: null
completed_at: 2026-10-26 15:20:34.125283
contexts:
- react
created: 2026-10-26 12:54:53.773167
defer_until: null
due: null
energy: medium
id: 2026-10-26T1254-review-pr-61317-ent-7967-stop-querying-the-deleted
order: null
output: |
  ## Agent run 2026-10-26T14:45
  PR #61317 (https://github.com/canary-technologies-corp/canary/pull/61317), ENT-7967 (https://linear.app/canary-technologies/issue/ENT-7967)

  Verdict: approve. Nothing blocks it. Nothing has been posted to GitHub.

  What it does: drops `Check_In_Monthly_Cap__c` from SALESFORCE_ACCOUNT_FIELDS_TO_QUERY (salesforce_pull and update_salesforce_hotel_metadata both use this list), deletes the `Hotel.check_in_monthly_cap__c` property, removes the cap branch in calculate_check_in_usage, and removes the cap mocks from 5 tests.

  Verified:
  - No reference to "monthly_cap" is left anywhere in the PR head (case-insensitive grep across the repo).
  - The field list is the only place the field was queried. The cached fallback in get_field_from_salesforce_account re-runs the same query, so this one edit fixes the pull, the billing path and the CSM lookups.
  - CI: 39 checks pass, 32 skipped, 0 failing. Review is still REVIEW_REQUIRED.
  - Business sign-off: rrgrs asked about the billing risk inline. Martin replied that billing (MJ) confirmed Little America Flagstaff stays on usage billing and billing will handle its cap in January. The removed code returned inf when the cap was blank, so for every other hotel the result is unchanged.

  Non-blocking notes, if you want to leave a comment:
  - calculate_check_in_usage has no direct unit test (billing/tests has none). The PR does not make this worse. A one-line test of count times rate would pin the new behaviour.
  - The caveats Martin already lists are real and out of scope: future Salesforce field deletions break every reader again (same as ENT-873), and SalesforceMalformedRequest gets logged as DoesNotExist. A follow-up ticket for those would be worth having.
  - Timing: it must deploy before 2026-11-01 00:00 UTC.

  Draft approval comment (not posted):
  > LGTM. The field list is the single choke point, there are no remaining refs, and billing has signed off on the Little America cap. Worth a follow-up ticket on the SOQL fragility for deleted fields (ENT-873 pattern).
project: null
source_id: https://github.com/canary-technologies-corp/canary/pull/61317
tags:
- morning-gtd
- github
time_minutes: 20
title: 'Review PR #61317: [ENT-7967] Stop querying the deleted Salesforce cap field'
updated: 2026-10-26 15:20:34.125275
waiting_on: null
waiting_since: null
working_on: false
---

https://github.com/canary-technologies-corp/canary/pull/61317
Author: martinrodriguezcanary. Personally requested.