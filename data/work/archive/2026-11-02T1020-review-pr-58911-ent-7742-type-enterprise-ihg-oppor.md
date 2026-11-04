---
area: null
completed_at: 2026-11-04 16:31:12.651932
contexts:
- react
created: 2026-11-02 10:20:40.302739
defer_until: null
due: null
energy: medium
id: 2026-11-02T1020-review-pr-58911-ent-7742-type-enterprise-ihg-oppor
order: null
output: |
  ## Agent run 2026-11-02T13:47:34.177653

  Reviewed PR #58911 (https://github.com/canary-technologies-corp/canary/pull/58911), head after the 2026-10-28 and 2026-10-30 commits. Nothing posted to GitHub.

  **Verdict: the typing change is correct and small. One thing to raise before approving: the "newest wins" tiebreak in `get_onboarding_states`.**

  What changed since the 2026-10-08 archive:
  - Merged master twice, and added `order_by("created_at", "id")` in `CohortHotelService.get_onboarding_states` (cohort_hotel.py:556) so the newest opportunity wins when two share a type.
  - PR body updated: as of Oct 28 RevOps has split the 6 accounts that had no Core Plus opportunity.
  - Blocker #62150 (https://github.com/canary-technologies-corp/canary/pull/62150, ENT-7793) merged on 2026-10-30, so that dependency is cleared.
  - Still a draft, with no human reviews. CI has nothing failing; only "Check draft status" is pending. Macroscope says a human must review (concern: commercial Core Plus records that carry the markers by mistake get retyped Core).

  Typing logic (types.py `derive_onboarding_type`): correct. IHG parent plus checkbox gives Core. Without the checkbox the package type still decides. No parent plus checkbox stays Core Plus. Non-IHG parents are unchanged. Both sync paths pass the checkbox through: `SalesforceOpportunityData.onboarding_type`, plus the per-account sync, which now SELECTs `Enterprise_Deployment__c`. The parametrized tests cover each branch.

  Points to raise:
  1. **The tiebreak orders by local `created_at`, which is when the row entered the mirror, not when Salesforce created the opportunity.** The model has no Salesforce CreatedDate field. If an account's old Qualified opportunity and its Core half were imported in the same run (for example the initial backfill), the order comes from the SOQL result order, so the stale opportunity can still win. A tighter rule that fits the problem: prefer an opportunity whose stage is in `IHG_CORE_OPPORTUNITY_STAGES` (active or Agreement Sent) over a pipeline-stage one such as Qualified, then use `created_at`. Suggested comment:
     > `created_at` here is when the mirror first saw the row, not Salesforce's CreatedDate, so two opportunities imported in the same sync tie-break on SOQL order. Since the stale ones are pipeline-stage (Qualified), could we prefer the opportunity in an active / Agreement Sent stage first and only fall back to `created_at`?
  2. Other code that reads by type is unaffected by duplicate Core opportunities. `get_local_onboarding_data` uses `.first()` without ordering, but it only reads account-level data, so either opportunity gives the same result. `SalesforceOpportunitySelector.get_go_live_date` returns None when dates disagree, but only Wyndham calls it. The `msa.py` live/configuring checks take a union of types. No action needed; noted so you don't have to re-check.
  3. The reviewer checkbox in the PR body is still open: has the onboarding team been warned, and does ENT-7791 have a RevOps owner? ENT-7791 (https://linear.app/canary-technologies/issue/ENT-7791) is in **Backlog and unassigned** (last updated 2026-10-07). Andrea or RevOps needs to sort that out before merge, because about 105 of the 153 healthy hotels will turn unhealthy on the first monitoring run.
  4. Nit: the new types.py comment "may carry the IHG parent" makes the checkbox the only thing that separates the halves. That matches RevOps' design, but a Core Plus add-on with the checkbox ticked by mistake would be silently retyped Core (Macroscope's concern). ENT-7791 is meant to catch those records, which is one more reason it needs an owner.

  Suggested next step: approve once Andrea has answered point 1 (or changed the ordering) and confirmed the warning and ENT-7791 ownership. CODEOWNERS: onboarding/ isn't on the pod-enterprise list in memory, so your approval should count, but I haven't confirmed that.
project: null
source_id: https://github.com/canary-technologies-corp/canary/pull/58911
tags:
- morning-gtd
- github
- resurfaced
time_minutes: 20
title: 'Review PR #58911: [ENT-7742] Type enterprise IHG opportunities as GMS Core'
updated: 2026-11-04 16:31:12.651921
waiting_on: null
waiting_since: null
working_on: false
---

Resurfaced: archived 2026-10-08 as `2026-10-08T0939-review-pr-58911-ent-7742-type-enterprise-ihg-oppor`, but new activity at the source since then.

Draft by abrad (Golem branch), personally requested. IHG Core/Core Plus attribution.
https://github.com/canary-technologies-corp/canary/pull/58911