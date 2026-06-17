---
area: null
contexts:
- react
created: 2026-06-17 09:06:46.726470
defer_until: null
due: null
energy: medium
id: 2026-06-17T0906-re-review-pr-47878-ent-6490-clear-previous-pms-ven
order: null
output: |
  ## Agent run 2026-06-17T07:25:20Z

  Re-reviewed PR #47878 (https://github.com/canary-technologies-corp/canary/pull/47878)
  after abrad pushed updates following my CHANGES_REQUESTED on 2026-06-16. Still
  OPEN/CHANGES_REQUESTED (my review block is the only one outstanding; martinrodriguez
  already APPROVED). Latest commits: 0e113ad65 (rename) + c162703bb (ad-hoc stage).

  ### Verdict: all 3 of my points are fully addressed. Ready to clear my block / approve.
  I did NOT post anything to GitHub — see "draft GitHub action" below for approval.

  ### My 3 review comments and how each was resolved
  1. **Move it to an ad-hoc stage instead of wiring into every IHG run** — DONE.
     Plan now lives in `ad_hoc_stages` (property_configuration_processes.py:2171), with
     `next_stages=[]`. Base config still chains BASE → CREATE directly, so there is NO
     extra stage on every IHG onboarding. Two regression tests added:
     `test_ihg_pilot_cleanup_previous_pms_vendors_is_ad_hoc` (asserts it's in ad_hoc_stages,
     not in sequential stages, and base.next_stages == [CREATE]) and
     `test_ihg_pilot_sequential_stage_children_have_labels`.
  2. **"foreign" naming** — DONE. `_foreign_vendors`→`_previous_vendors`, enum
     `CLEANUP_FOREIGN_PMS_VENDORS`→`CLEANUP_PREVIOUS_PMS_VENDORS`, error codes use
     "previous". Rename migration already MERGED to master via #48078
     (https://github.com/canary-technologies-corp/canary/pull/48078). Grep confirms zero
     leftover "foreign" references in onboarding/ (outside migration history).
  3. **Loop error handling — record successes, raise expected error with prior cleanups
     in context** — DONE. Loop accumulates `cleaned`; on a cleanup exception it records
     `cleaned_vendors`/`blocked_vendors`/`failed_vendor` into results and raises
     `ERROR_PMS_PREVIOUS_VENDOR_CLEANUP_FAILED` with `results_before_error=results`.
     Verified `raise_expected_error` is annotated `NoReturn` and raises, so the
     post-`except` `cleaned.append` correctly does not run on failure. Covered by
     `test_execute__cleanup_failure_records_prior_cleanups`.

  ### Extra verification I did this pass
  - All external refs resolve: `PMSGatewayService.cleanup_rooms_and_account_validations`,
    `.get_account`, stubs `stub_account/stub_hotelkey_configuration/stub_opera_configuration`.
  - `Account` schema exposes per-vendor config attrs named by `vendor.value`, so the
    `getattr(account, vendor.value)` access pattern is sound; `is_enabled` defaults False.
  - 404-only catch on get_account with non-404 re-raise (rrgrs's earlier point) is in
    place + tested (`test_execute__reraises_non_404_http_error`).
  - New error codes have both WHAT_HAPPENED and WHAT_TO_DO entries (onboarding convention).
  - CI: no failures. The active workflow's linter + Select tests pass; the "skipping"
    Django/pytest jobs are the dedup'd duplicate workflow contexts from the PR stack,
    not real skips of this branch's tests.

  ### Non-blocking nits (optional — would mention, not block on)
  - PR description is now stale. It still says "Insert an AD HOC stage before CREATE in
    the IHG flow" with "BASE → CLEANUP_FOREIGN_PMS_VENDORS → CREATE → VALIDATE → GOLIVE".
    The implementation is now a true operator-triggered ad-hoc stage (`next_stages=[]`),
    NOT inserted into the sequential flow — operators must manually run the cleanup stage
    for affected hotels. Worth updating so CS understands the trigger model.
  - Branch is behind master: commit 0e113ad65 duplicates the already-merged #48078 rename,
    so `gh pr diff` still shows migration 0153. A rebase drops it; harmless, git reconciles.
  - Minor robustness (not reachable for IHG): if a target PMS config type isn't in
    `PMS_VENDOR_MAP`, `target_vendors` would be empty and every on-account vendor would be
    treated as "previous". HotelKey IS mapped, so safe today; just noting for future reuse.

  ### Draft GitHub action (NOT yet performed — needs your OK)
  My recommendation: clear my CHANGES_REQUESTED with an APPROVE. Suggested review body:
    "Thanks for the updates — all three points addressed: cleanup is now a true ad-hoc
     stage (base still chains straight to CREATE), naming renamed to 'previous', and the
     cleanup loop now records prior successes in the error context on failure. Tests cover
     each. Approving. Two non-blocking nits: the PR description still describes the old
     wired-in flow (now ad-hoc/operator-triggered), and the branch needs a rebase past the
     merged #48078 so the duplicate 0153 migration drops out."
  Say the word and I'll submit it (or post just the nits as a comment instead).
project: null
source_id: https://github.com/canary-technologies-corp/canary/pull/47878
tags:
- morning-gtd
- github
time_minutes: 15
title: 'Re-review PR #47878: [ENT-6490] Clear previous PMS vendors before configuring
  HotelKey (IHG)'
updated: 2026-06-17 10:25:20.000000
waiting_on: null
waiting_since: null
working_on: false
---

abrad pushed updates after my CHANGES_REQUESTED. Still OPEN/CHANGES_REQUESTED. https://github.com/canary-technologies-corp/canary/pull/47878