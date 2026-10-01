---
area: null
completed_at: 2026-10-01 14:42:37.992115
contexts:
- react
created: 2026-10-01 11:37:58.118735
defer_until: null
due: null
energy: medium
id: 2026-10-01T1137-review-andrea-s-3-pr-stack-unwinding-tipping-confi
order: null
output: |
  ## Agent run 2026-10-01T11:25:55Z

  Read-only review of Andrea's stack for ENT-7657 (https://linear.app/canary-technologies/issue/ENT-7657/update-above-property-dashboard-pyramid),
  from her Slack post (https://canarytechnologies.slack.com/archives/C0B1MN8F869/p1790794624736299, no replies yet).
  Nothing was posted anywhere. I read the diffs and surrounding code at the PR heads; I did not run the tests locally.

  ### Verdict

  - PR #58583 (https://github.com/canary-technologies-corp/canary/pull/58583), script-type migration: fine. Migration 0170 follows 0169 on master, model + migration only. Already approved by lmenaolivares.
  - PR #58633 (https://github.com/canary-technologies-corp/canary/pull/58633), labels: fine. Already approved.
  - PR #58521 (https://github.com/canary-technologies-corp/canary/pull/58521), logic: approach is sound and well tested, approved by jbueno (tipping). It cannot merge yet (CI red), and I have one real safety concern plus some smaller ones below.

  The idea itself holds up: removing only the PortfolioHotel row would leave the hotel in Pyramid's payroll report (the report selects hotels by `tip_configuration.hr_gateway_config_uuid`, not by portfolio) and leave Pyramid's Property IDs attached. Reusing `DeactivateTippingPlan` + `DeactivateHotelPlan` behind a new ad hoc stage matches the Marriott precedent.

  ### Findings on #58521, most important first

  1. CI is failing: `Backend linters` -> `make check-dependency-changes`. The new check `onboarding/checks/tipping.py` imports `ledger.services`, a new onboarding -> ledger app dependency that `ci/deps/opinionated_state.py` does not list. Fix is either to regenerate that file, or to move the balance check into `tips` (see 4), which removes the new dependency. `merge_gatekeeper` is red only because of this.

  2. The HR gateway and generic `PROPERTY_ID` are removed without checking they belong to the company being left. `_clear_tip_hr_gateway` nulls whatever gateway is set, and `PROPERTY_ID` is deleted regardless of value. `_has_ties` accepts a hotel on any one of portfolio / company Property ID / gateway. So a hotel that moved from Pyramid to another Canary tipping company (e.g. Stonebridge) and was re-onboarded there first still passes the Pyramid tie check via its old portfolio row, and the Pyramid removal then strips the Stonebridge gateway and Property ID and turns tipping off. Suggest clearing the gateway only when it equals `ties.hr_gateway_config_uuid`, and removing `PROPERTY_ID` only when its identifier equals the company Property ID. The PR description lists the unchecked `PROPERTY_ID` removal as a known caveat "same as Marriott", but Marriott archives the hotel, so the cases differ.

  3. The money check is non-skippable with a zero threshold. A department holding a few undistributable cents blocks the script permanently with no override. The existing `unconfigure_tipping` command has `--dust-threshold` for exactly this. Worth deciding what ops do in that case before this ships.

  4. The money gate is a narrower copy of `unconfigure_tipping._check_money_gates` (`backend/canary/tips/management/commands/unconfigure_tipping.py`). That command also gates on `TipsSelector.get_unpaid_tips` (tips awaiting an FBO/payout sweep), and re-runs the gates after turning the product off inside the transaction so a tip landing mid-run rolls it back. The new check runs once, before `DeactivateTippingPlan`. Unpaid FBO tips are probably zero for wallet companies and the race window is small, but sharing one implementation in `tips` would close both gaps and fix finding 1.

  5. Payroll-report timing is an ops footgun that only the PR description and a docstring mention. Once the gateway is cleared, the hotel drops out of the company payroll report, including tips earned earlier in the current pay period. Ops running this from the Cohort UI will not see that warning. The MVW note is surfaced in the result, but that is after the run.

  6. Side effect worth confirming with tipping: HR-feed deactivations resolve the hotel through the gateway (`TipsSelector.get_hotel_from_hr_gateway_and_employee`), so after removal the hotel's HR-managed wallet profiles are never deactivated by the feed; the callback logs `hotel_resolution_failed` and returns. Tipping is off, so impact is limited, and it keeps wallets redeemable. The description says wallet profiles are "not changed" but not that they become unmanaged.

  7. Not verified end to end. Andrea's description says no run from the manage app was done, only tests. A staging or live-branch run of one hotel through the Cohort UI before the Pyramid batch would be reasonable.

  Nits: PR title has a stray space ("Remove_hotel _from_mgmt_company"); the stage definition is repeated four times in `property_configuration_processes.py`; backend label "Remove from Management Company" differs from the frontend "Cut Hotel's ties to Management Company".

  ### Open question on the idea

  The script turns tipping off entirely (`has_tipping` and `can_be_tipped` false) for hotels leaving the company. In the Linear thread Andrea asked two questions in one comment (remove from portfolio? unwind tipping too?) and Natalya answered "that is correct!", which does not clearly cover the second. If any of the removed Pyramid hotels still take tips, or are moving to another management company, guests would hit dead QR codes. Worth an explicit confirmation of which hotels are in the batch and that tipping should stop at each.

  ### Checked and fine

  - Script type is registered everywhere the UI needs it (backend enum, label map, frontend enum, label, and the four `VALID_SCRIPT_TYPES_BY_ONBOARDING_TYPE` lists: Pyramid, MVW, Buffalo, Stonebridge). Ad hoc stages count as valid script types.
  - Pre-run check and plans run inside one transaction in `OnboardingService`, so a provider error rolls back the tipping deactivation.
  - Portfolio removal goes through `PortfolioService.remove_hotel` with child portfolios.
  - `keep_amb` and `clear_tip_hr_gateway` default to False, so Wyndham, BW, IHG and Marriott deactivation behaviour is unchanged, with tests covering both defaults.
  - The stale `review-bot` failure has since re-run green.

  ### Draft review comment for #58521 (not posted)

  > Approach looks right to me, and thanks for splitting it up. A few things before merge:
  >
  > 1. `Backend linters` is red on `check-dependency-changes`: the new check adds an onboarding -> ledger dependency that isn't in `ci/deps/opinionated_state.py`.
  > 2. `_clear_tip_hr_gateway` clears whatever gateway is set and `PROPERTY_ID` is removed regardless of value. If a hotel has already been re-onboarded under another tipping company but still has the old portfolio row, this strips the new company's gateway and ID. Could we clear only when the gateway equals `ties.hr_gateway_config_uuid` and the `PROPERTY_ID` identifier matches the company Property ID?
  > 3. The department-funds check is non-skippable at > 0 cents. `unconfigure_tipping` has a dust threshold and also gates on `get_unpaid_tips`, then re-checks after disabling tipping. Could the two share one gate in `tips`? That would also remove the new ledger dependency.
  > 4. The payroll-report timing caveat only lives in the PR description. Can we put it somewhere ops see before running?
  > 5. Has the list of hotels been confirmed as "tipping should stop", not only "leave the Pyramid dashboard"? Natalya's reply on the ticket was to a two-part question.
  > 6. Worth one run through the Cohort UI on staging before the Pyramid batch, since only tests have exercised it.
project: null
source_id: https://canarytechnologies.slack.com/archives/C0B1MN8F869/p1790794624736299
tags:
- morning-gtd
- slack
- from-awareness
time_minutes: 20
title: Review Andrea's 3-PR stack unwinding tipping config on portfolio removal
updated: 2026-10-01 14:42:37.992099
waiting_on: null
waiting_since: null
working_on: false
---

Promoted from the 2026-10-01 awareness report (Slack highlights, item 6).
https://canarytechnologies.slack.com/archives/C0B1MN8F869/p1790794624736299