---
area: null
completed_at: 2026-10-02 15:07:05.848913
contexts: []
created: 2026-10-02 11:04:43.512950
defer_until: null
due: 2026-10-02
energy: low
id: 2026-10-02T1104-review-martijn
order: null
output: |
  ## Agent run 2026-10-02T09:32:00Z

  Reviewed PR #58771 "[EMEA-702] Fake GDPR check-in & check-out" by mdekkernet
  (https://github.com/canary-technologies-corp/canary/pull/58771), head fdc6a5efd.
  Ticket: EMEA-702 (https://linear.app/canary-technologies/issue/EMEA-702/gdpr-hotel-dashboard-ui-fake-obfuscation).
  Nothing was posted to GitHub. Review is local only.

  **Verdict: do not approve yet.** The design is sound, but the PR cannot merge as is,
  has had no CI on its current head, and ships one failing test.

  ### Blocking

  1. **Merge conflict, so no CI has run.** The PR conflicts with master in
     `backend/canary/feature_flags/generated/generated_features.py`. Master already has
     `GDPR_OBFUSCATION` (flag sync #58535, with `tags=("EMEA",)`), so the fix is to drop
     the PR's hand-added hunk. Because of the conflict, only the three
     `pull_request_target` workflows ran on the head commit: no tests, linters,
     coverage or dependency checks. The "Auto-Merge Migrations Failed" comment on the
     PR is stale (it is from the push before the force-push).
  2. **One new test fails deterministically.**
     `gdpr/tests/selectors/test_stay_obfuscation.py::test_obfuscation_status__none_for_a_reservation_less_check_in`
     fails on `assert check_in.reservation is None`. `stub_check_in` always calls
     `CheckInIngestionService.sync_check_in_data_to_reservation`, which creates a
     reservation. The test it replaced used `CheckIn.objects.create(...)` directly;
     restoring that fixes it.

  ### Worth raising

  3. **Guest-facing schema picked up the field.** `GuestCheckOutSchema` now carries
     `obfuscation`, and it is served by the public guest API
     (`check_out/views/guest/guest_check_out.py`). The ticket scopes this to the hotel
     dashboard. This adds a flag evaluation to every guest check-out load and exposes
     the status to guests. Ask him to drop it unless the guest frontend needs it.
  4. **`reservation_is_obfuscated` got heavier on every activity-log open.** It was one
     `EXISTS` query. It now loads full `CheckIn` and `CheckOut` rows joined to hotel,
     and each `obfuscation_status` call lazy-loads `stay.reservation` and
     `primary_guest` again, flag on or off. Suggest keeping `EXISTS` for the really
     erased case and loading only `departure_date` when the flag is on. The "Known
     limit" comment about soft-deleted check-ins losing their reservation FK was also
     dropped, though the limit still applies. Side effect to confirm as intended: an
     erased `CheckOut` now hides the history too (before, only `CheckIn` did).
  5. **Duplicated retention logic.** `StayObfuscationSelector._retention_days` is a
     copy of `retention_period_days_for` in `gdpr/services/retention.py` minus the
     `is_country_default_enabled` gate. Two copies will drift when the real gate opens.
     Suggest one shared helper in `retention.py`. `get_country_by_country_code`
     (`shared/geo/country/country.py`) would also replace the `try/except ValueError`.
  6. **Which flag is this?** `retention.py` says the real sweep's country-default gate
     waits on "the rollout flag shared with PMS Gateway". If `gdpr-obfuscation` is that
     flag, fake display and real deletion end up on one switch. If it is fake-only, the
     name is too broad. Worth asking.
  7. **Check-out has no frontend consumer yet.** Nothing on master reads `obfuscation`,
     and Marc's open PRs wire check-in only: #58571
     (https://github.com/canary-technologies-corp/canary/pull/58571) and #58722
     (https://github.com/canary-technologies-corp/canary/pull/58722). The API still
     returns full PII for these stays (by design per the ticket), so the check-out half
     is invisible until a frontend change lands. Ask whether that is ticketed.
  8. Nit: the PR description still has the empty template sections; "What I verified"
     is blank.

  ### Checked and fine

  - The per-hotel flag cache on `ObfuscationStatusField` is safe: marshmallow deep-copies
    fields per schema instance, and all four schemas are instantiated per request, so
    the flag is read once per hotel per response and never goes stale.
  - Boundary matches the real sweep: obfuscated when today (UTC) > departure + retention.
  - No new N+1 on the dashboard lists by reading the code (hotel, reservation and
    primary guest are already loaded by existing fields). I did not measure query counts.

  ### What I ran (PR head in a scratch worktree, since removed)

  - New gdpr tests: 32 passed, 1 failed (item 2).
  - Existing check-in dashboard/details, check-out dashboard, reservation audit log and
    `ci/deps` tests: 143 passed, 1 skipped.
  - ruff check, ruff format and pyrefly on the changed files: clean.
  - Not run: the full backend suite, OpenAPI staleness, coverage.

  ### Draft comment (not posted)

  > Design looks right to me, and the per-request flag cache on the field is neat. A few
  > things before I approve:
  > 1. The branch conflicts with master in `generated_features.py` (master already has
  >    `GDPR_OBFUSCATION` from the flag sync), so CI has not run on this head. Dropping
  >    your hunk should clear it.
  > 2. `test_obfuscation_status__none_for_a_reservation_less_check_in` fails locally:
  >    `stub_check_in` syncs to a reservation, so `check_in.reservation` is never None.
  >    The old test used `CheckIn.objects.create` directly.
  > 3. Is `obfuscation` on `GuestCheckOutSchema` intended? That schema serves the guest
  >    API, and the ticket is dashboard-only.
  > 4. `reservation_is_obfuscated` went from one EXISTS to loading full CheckIn and
  >    CheckOut rows plus lazy reservation/guest loads on every activity-log open. Could
  >    we keep EXISTS for the erased case and only read `departure_date` when the flag
  >    is on? The "Known limit" comment also got lost.
  > 5. `_retention_days` duplicates `retention_period_days_for` minus the gate. Can they
  >    share a helper in `gdpr/services/retention.py`?
  > 6. Is `gdpr-obfuscation` fake-display only, or the flag that will also open the real
  >    sweep's country-default gate?
  > 7. Is there a frontend ticket for check-out? I only see check-in wired in #58571 and
  >    #58722.
project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 5
title: review martijn
updated: 2026-10-02 15:07:05.848909
waiting_on: null
waiting_since: null
working_on: false
---

https://github.com/canary-technologies-corp/canary/pull/58771