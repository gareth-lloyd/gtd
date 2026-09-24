---
area: null
completed_at: 2026-09-24 10:43:40.444398
contexts: []
created: 2026-09-23 17:57:54.554029
defer_until: null
due: null
energy: null
id: 2026-09-23T1757-review-the-mechanism-for-targeting-which-wyndham-h
order: null
output: |
  ## Agent run 2026-09-24T10:25

  ### Verdict
  Eric's mechanism is right on the serialisation but wrong on ownership. After PR 56743 the app hides "Check In Now" whenever `Hotel.has_check_in` is False, so Messaging-only Wyndham properties need nothing. But neither knob is "on Wyndham's side": both are Canary Django-admin fields. Canary owns per-property rollout, which is what Caitlyn originally suspected. The thread currently records the opposite and should be corrected.

  ### How it works after the merge
  - Guest payload `hotel.check_in_configuration.has_check_in_mobile` = `CheckInConfiguration.has_check_in_mobile AND Hotel.has_check_in` (backend/canary/check_in/schemas/check_in_configuration_external.py, Method field). Covers both guest endpoints (reservations + hotel).
  - Wyndham app (WyndhamDigital PR 2099, https://github.com/WyndhamDigital/whr_frontend_reactnative/pull/2099) shows the button when `hasCheckInMobile != false`. Diana: the app also hides every Canary button unless BOTH hotel and reservation resolve from the Canary API.
  - `check_out` is already nulled via `has_check_out`, app gates on it; no change needed there.

  ### Who owns the knobs (correction to the thread)
  - `Hotel.has_check_in`: Django admin "Product Flags" fieldset (backend/canary/hotels/admin/hotel.py:937). The "Hotel Dashboard settings" Sofya used in MOB-1253 is the canary-admin hotel change page, not a Wyndham-facing dashboard.
  - `CheckInConfiguration.has_check_in_mobile`: model default True, exposed only via Django admin ConfigurationAdmin (check_in/admin.py:319, no field restriction). External schema is dump_only; no hotel-dashboard or adminland writer exists (grep of frontend found readers only in stubs/tests/schemas).
  - Wyndham has no self-serve toggle. Someone at Canary (onboarding/CS/eng) flips these per property. Worth naming that owner and keeping a rollout list.

  ### Default-on semantics for a slow rollout
  - Default is ON: `has_check_in_mobile` defaults True and the Wyndham v1->v2 migration (onetime_migrate_bw_wyndham_v1_to_v2.py) targeted exactly the hotels with it True. So every Wyndham property with `has_check_in=True` shows the button the moment the app ships. Opt-out, not opt-in.
  - Two levers, use the right one:
    1. Property never had check-in (Messaging-only): `has_check_in=False` already, nothing to do post-merge.
    2. Property has the check-in product live on web/guest-journey but Wyndham doesn't want it in-app yet: set `has_check_in_mobile=False` on the CheckInConfiguration. After the PR that hides only the app button; web check-in and existing `check_in` state survive (no other non-test backend reader of the flag besides the v1 reg-card dashboard filter and the one-time migration).
  - Edge case in the `!= false` check: the backend always emits a boolean now, but if a Wyndham hotel has NO check_in_configuration row the nested object dumps null, `hasCheckInMobile` is undefined, and the app shows the button. Ask Eric whether the app should gate on `== true` instead, or confirm every Wyndham hotel has a config row.

  ### The caveat from the PR
  - With `has_check_in=False`, `guest_reservations_view.py` nulls `check_in` on every reservation, so already-checked-in guests regress to "Check In Now" in the app. Harmless for properties that never had check-in. For PAUSING a live property use `has_check_in_mobile=False` (lever 2) rather than the product flag, which avoids the regression. PR author flagged this as a product decision; agreed, and lever 2 sidesteps it.

  ### PR 56743 status (https://github.com/canary-technologies-corp/canary/pull/56743)
  - Open, approved by leandro-alvarez 2026-09-21, last commit 2026-09-16 (5995fdaa), mergeStateStatus UNKNOWN (likely needs a rebase/merge-queue kick). AD-8391 is "Ready for Deploy", assignee Rafael Nunes (https://linear.app/canary-technologies/issue/AD-8391).
  - Failing checks: Non-blocking Playwright E2E shards 3/4 and 4/4 (sdm/authorizations.spec.ts, unrelated to a serializer change); two "API breaking-change approvals" runs CANCELLED; Macroscope "not approvable" only because its approval-risk check was skipped. None block merge. Nobody has merged for 3 days; the Wyndham re-test (MOB-1253, https://linear.app/canary-technologies/issue/MOB-1253, Sofya) is blocked on it.
  - MOB-1279 (missing badge on Days Prior screens) was canceled 2026-09-22 as a Wyndham/Telus-side wrong-URL issue, not ours.

  ### Suggested thread reply (DRAFT, not posted)
  > Quick correction on ownership: neither flag is on Wyndham's side. `has_check_in` (product flag) and `has_check_in_mobile` (check-in config) are both Canary Django-admin fields, so per-property rollout is ours to run. Post-merge: Messaging-only properties need nothing (has_check_in=False hides the button). To hold back a property that already has check-in live on web, set has_check_in_mobile=False on its CheckInConfiguration rather than turning the product off, so checked-in guests keep their state. Note it's opt-out (default true), so we should keep a list. One question for Eric: if a hotel has no check_in_configuration row the app sees hasCheckInMobile undefined and shows the button; should the app gate on == true? Also 56743 is approved but unmerged since Mon, can Rafael/Leandro land it so Sofya can retest?

  ### Follow-up 2026-09-24: does default-true expose new Wyndham properties?
  - No, on its own. `Hotel.has_check_in` defaults False; onboarding (onboarding/plans/hotel_products_plan.py:128) sets it True only when Check-in or Tablet Registration is in the sold products. New Messaging-only properties never show the button.
  - `has_check_in_mobile` predates the app (migration 0366, PR #30181, 2025-08-21) and was a general mobile-web check-in switch. Flipping its default would silently disable mobile web check-in for every new hotel across all brands, so leave it.
  - Real issue: PR 56743 makes this flag double as the app-visibility switch. Any Wyndham property sold check-in is live in the app by default, and holding one back is a manual Django admin edit. A staged app launch across existing check-in properties means a hand-maintained opt-out list.
  - If staged launch is wanted, a dedicated app-facing flag or Wyndham portfolio allowlist is cleaner than repurposing this one. Needs SDK + app to read a new field, so decide before the app ships broadly.
  - There is also onboarding/management/commands/disable_wyndham_msa_products.py which bulk-sets has_check_in=False (and other products) for Wyndham hotels; useful if a batch needs pulling back.

  ### Snowflake distribution 2026-09-24 (CANARY_RAW.CANARY, distinct hotels in any wyndham* portfolio excl. staging, 6,829 total)
  | is_active | is_live | has_check_in | has_check_in_mobile | app button visible post-merge | hotels |
  | --- | --- | --- | --- | --- | --- |
  | true | true | true | true | YES | 4,986 |
  | true | false | true | true | YES (if hotel resolves) | 806 |
  | true | true | false | true | no | 744 |
  | true | false | false | true | no | 250 |
  | false | true | false | true | no | 25 |
  | false | false | false | true | no | 7 |
  | false | true | true | true | YES (inactive!) | 6 |
  | false | false | true | true | YES (inactive!) | 4 |
  | true | true | true | false | no | 1 |
  - Every Wyndham hotel has a check_in_configuration row (0 no_config), so the null-config edge case is moot for Wyndham today.
  - has_check_in_mobile=False on exactly ONE Wyndham hotel: 126245 Days Inn by Wyndham Cheyenne (config last changed 2026-07-22). Nobody has ever used this flag as a rollout lever.
  - Post-merge the app button is on for ~5,800 Wyndham properties (4,986 active+live, 806 active not-live, 10 inactive with has_check_in still true). Staged rollout via this flag = flipping thousands of rows to false first, then back on per property. That is the wrong tool; an allowlist/new flag is the right shape if staging is wanted.
  - ~1,000 Messaging-only style properties (has_check_in=false) are correctly hidden by the PR.
  - Hotel counts by portfolio overlap heavily (Connect GMS = Connect International = 5,368, Connect Plus 1,805, wyndham 6,730, deactivated 435). Note wyndham_deactivated still has 53 hotels with has_check_in=true; the app would show the button there too if the hotel resolves.

  Slack thread: https://canarytechnologies.slack.com/archives/C09M5GRJPL2/p1790171519216139?thread_ts=1790006579.628339&cid=C09M5GRJPL2
project: null
source_id: null
tags: []
time_minutes: null
title: Review the mechanism for targeting which Wyndham hotels get the in-stay / mobile
  check-in flows
updated: 2026-09-24 10:43:40.444380
waiting_on: null
waiting_since: null
working_on: false
---

From #epd-mobile thread "All good with Wyndham :)" (Sept 21-23), cc'd by Caitlyn Levine.
https://canarytechnologies.slack.com/archives/C09M5GRJPL2/p1790171519216139?thread_ts=1790006579.628339&cid=C09M5GRJPL2

Proposed mechanism (Eric): once PR 56743 (AD-8391) merges, guest payload sends has_check_in_mobile = config flag AND hotel.has_check_in. Wyndham app checks hasCheckInMobile != false, so unset = button shown by default. Wyndham then controls rollout per property by setting has_mobile_check_in true only where they want it live.

Things to sanity-check:
- Default-on semantics (unset -> visible) for a slow rollout
- Caveat: with product off, check_in is still null on guest reservations, already-checked-in guests lose state
- Who owns the per-property config: Wyndham side vs Canary side
- PR 56743 open, approved, not merged; only non-blocking E2E failures