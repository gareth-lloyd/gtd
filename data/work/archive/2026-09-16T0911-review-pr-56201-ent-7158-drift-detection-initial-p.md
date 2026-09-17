---
area: null
completed_at: 2026-09-16 16:00:59.865882
contexts:
- react
created: 2026-09-16 09:11:57.979174
defer_until: null
due: null
energy: medium
id: 2026-09-16T0911-review-pr-56201-ent-7158-drift-detection-initial-p
order: null
output: |
  ## Agent run 2026-09-16T16:05 — review of PR #56201 (https://github.com/canary-technologies-corp/canary/pull/56201)

  Nothing was posted to GitHub, Slack or Linear. Findings below are ready to paste as a review.

  **Context**
  - PR: ENT-7158 (https://linear.app/canary-technologies/issue/ENT-7158/initial-property-view), author Martin Rodriguez, 18 files, +2551/-1, review requested from pod-enterprise, Pod: Internal Tools, ldewald. No reviews or inline comments on GitHub yet (Andrea's "questions, comments" in the Slack thread are not on the PR — probably on the Loom or an unsubmitted review).
  - Slack thread: https://canarytechnologies.slack.com/archives/C0B1MN8F869/p1789500273590499?thread_ts=1789500273.590499&cid=C0B1MN8F869 ; Loom: https://www.loom.com/share/4e5abff4abf846afa9d731fe72fc9c0d
  - Scope: 3 staff-gated internal_support endpoints (list, detail, glossary) + a recalc POST, `DriftSelector`, `ConformityService.get_final_setting_keys()` cached at finalize, three /manage screens (list, detail, color glossary) behind the `drift-detection-ui` flag (already on master in generated-features.ts).
  - CI: all required checks green (backend tests, typecheck, lint, knip, i18n). E2E non-blocking failures on chat/compendium/F&B-settings/sales-booking specs — unrelated to this diff. Meticulous flagged 142/811 screens; menu item is flag-gated so likely base noise, but worth Martin approving/dismissing.

  **Verdict: approve with comments.** Flag-gated, staff-only, read-mostly spike; backend shape is sound. Two things I'd ask for before merge (1, 2), rest is follow-up.

  **Ask before merge**
  1. `ConfigDriftDetail.vue` `goBack()` → `router.back()`. The list deliberately supports middle-click open-in-new-tab (`onTableAuxClick`), and in a fresh tab `back()` leaves /manage or does nothing. Fall back to `router.push({ name: RouteName.CONFIG_DRIFT })` when there's no in-app history (`window.history.state?.back == null`). Same in `DriftGlossary.vue`.
  2. Recalculate has no error path. `useHotelDrift.recalculate` doesn't catch, `onRecalculate` only resets the spinner, so a 404 ("no drift-capable MSA") or 500 becomes an unhandled rejection with no UI. Set `error` (or a toast) in the catch. Backend POST also has zero tests (list/detail GETs are covered).

  **Should fix / follow-up**
  3. Test gap on the only interesting backend logic: `HotelDriftDetailSchema._drift_item` with real `HotelAttributes` (expected/actual + `NO_VALUE_DEFINED` mapping) is untested — the detail test only asserts the keys exist. Also no test for `ConformityService.get_final_setting_keys()` / the glossary endpoint.
  4. Recalc is `POST /api/internal_support/config_drifts` with `{hotel_uuid}` in the body. `POST /config_drifts/<uuid>/recalculate` reads better and matches the detail URL. Cheap to change now, annoying later.
  5. `_hotel_attrs_or_none` swallows every `ValueError` (unknown MSA string, missing SF account) and returns None, so the detail page silently shows "—" for expected/actual with no hint why. Log it at least; the UI could show "could not compute expected values".
  6. `:deep([class*="rowCell_"])` in `ConfigDriftList.vue` couples to CanaryTable's CSS-module class names; a rename breaks it silently. Either add a column-divider option to CanaryTable or leave a TODO.
  7. Hardcoded Tailwind-ish hex colors throughout (#6b7280, #374151, #fffbeb, #92400e…) instead of canary tokens, and `<style module>` without `lang="scss"` (frontend/CLAUDE.md convention). Fine for a spike, but this is now three screens' worth.
  8. Route guard checks only the feature flag, not `is_canary_staff`. Menu hides the entry for non-staff, but a non-staff user with the flag on who hits the URL gets a 401 rendered as "Could not load configuration drift". Low, since backend gate is correct (framework runs the class gatekeeper even when the handler doesn't declare the `gatekeeper` param — confirmed in shared/request_framework/core_test.py).
  9. `HotelDriftListSchema._brand_display` returns None for any brand_id not in `BrandId`, so those hotels show "—" and drop out of the brand filter. Related to the known BrandId.get() silent-None loophole (see memory). Acceptable now; worth a note.
  10. Minor: `DriftKeySchema` and `GlossarySettingSchema` are the same shape; `onUpdated → measureSettingsOverflow → reactive write → re-render` converges only because of the `!==` guards — fragile but OK; glossary empty-state says "No drifting settings." though it lists all FINAL settings.

  **Good**
  - v2 request framework + `StaffUserGatekeeper` (MFA default), `@readonly_database` on GETs and `@no_readonly_database` on the POST, matching sibling internal_support views.
  - List endpoint is cheap (read-model only), 1000-row cap with `truncated` + warning log; expected/actual only on detail.
  - Filters persisted in URL query; stale-drift nudge on detail; menu-section tests cover flag/staff matrix.
project: 2026-04-16T1210-unblock-team
source_id: https://canarytechnologies.slack.com/archives/C0B1MN8F869/p1789500273590499?thread_ts=1789500273.590499&cid=C0B1MN8F869
tags:
- morning-gtd
- slack
- from-awareness
time_minutes: 20
title: 'Review PR #56201: ENT-7158 Drift detection initial property view in /manage'
updated: 2026-09-16 16:00:59.865860
waiting_on: null
waiting_since: null
working_on: false
---

Martin Rodriguez shared the latest Drift Detection UI tweaks (loom in thread). PR is open, review required.
https://github.com/canary-technologies-corp/canary/pull/56201
https://canarytechnologies.slack.com/archives/C0B1MN8F869/p1789500273590499?thread_ts=1789500273.590499&cid=C0B1MN8F869