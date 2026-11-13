---
area: null
completed_at: null
contexts:
- react
created: 2026-11-13 09:54:27.847873
defer_until: null
due: null
energy: medium
id: 2026-11-13T0954-review-pr-64911-stay-5961-refuse-guest-lookups-whe
order: null
output: |-
  ## Agent run 2026-11-13T10:08

  Reviewed PR #64911 (https://github.com/canary-technologies-corp/canary/pull/64911) by reading the diff and the surrounding code at the PR head. Nothing was posted to GitHub. I did not run the tests.

  **Verdict: the diff is correct and I found no bug in it. Two things to confirm with Ishwar before approving, neither of them a code defect in the 125 lines.**

  ### Confirm before approving

  1. **The gate can be skipped with one forged header unless production runs `IDENTITY_TOKEN_MODE=enforce`.** The new check only runs for callers that are not "trusted", and trusted includes `edge_application_sid(request) is not None`. Below enforce mode that function returns the app from the `X-Canary-Source` header as sent (`backend/canary/api_gateway/services/api_identity_token.py:306`); the settings default is `off` (`backend/canary/canary/settings/base.py:872`). The view's own comment says the header "alone can be forged". So with the mode at off or shadow, an attacker who adds `X-Canary-Source: service=..., app=...` gets past the sign-in gate, the product gate, and the full-identity requirement. The PR body acknowledges this as a Codex finding and declines it as pre-existing, which is true, but a hotel switched off because of SEC-1762 (https://linear.app/canary-technologies/issue/SEC-1762) is not protected from a deliberate attacker unless the mode is enforce. I did not check the production value (it lives outside the repo, and I did not read prod config). Ask: what is the mode in each prod region, and does the edge strip a client-sent `X-Canary-Source`?

  2. **Turning a hotel off also kills its `/cl/` and `/ul/` links.** Those are the confirmation-number + last-name links hotels embed in their own PMS emails; nothing in the repo generates them. The ticket STAY-5961 (https://linear.app/canary-technologies/issue/STAY-5961) says "Keep guest journey message links". Canary's own journey messages carry slug links, which stay open, so I read the PR as consistent with the ticket, but the PR body calls `/cl/` and `/ul/` "guest message links", so the wording is worth one explicit check: does the product owner know a switched-off hotel's PMS-email check-in and upsell links will land on the not-found page?

  ### What the PR does, checked

  - `GuestReservationsView.get` (`backend/canary/guest/views/guest_reservations_view.py:523`): anonymous callers at a hotel with `has_guest_sign_in` off get 404 with code `reservation_lookup_blocked`. The gate sits after the trusted-caller decision and before the rate limiter and the reservation query, so a refused request never reaches the database query. Paired devices and gateway apps pass.
  - `CheckInLookup` and `UpsellLookup` (`backend/canary/check_in/views/api_standard_link.py:34`, `:94`): redirect to `/check-in/404/404` when off.
  - `GuestHotelSchema` exposes `has_guest_sign_in` for the frontend PR #64912 (https://github.com/canary-technologies-corp/canary/pull/64912).
  - By-slug and by-uuid reads (`GuestReservationView`, `ReservationExternalView`) are untouched, as intended.
  - Tests cover on and off for all three surfaces, and paired-device and gateway-app exemptions under enforce mode.
  - Default is on, so nothing changes at deploy. Note the ticket title says "disable everywhere"; this stack ships a per-hotel switch that someone must flip, via PR #64913 (https://github.com/canary-technologies-corp/canary/pull/64913).

  ### CI

  - `Backend linters` fails on two stale generated files, both caused by the new field in the base PR #64907 (https://github.com/canary-technologies-corp/canary/pull/64907), not by this diff: `rules_based_configuration/types/setting_keys.py` (`python manage.py generate_setting_types`) and `canary_mcp_ro.json` / `canary_mcp_ro.sql` (`make generate-mcp-sql-grants`). The fix belongs in #64907.
  - #64907 itself is unreviewed and also fails `make test-backend` and `Birdline policy`; I did not look into those. This PR cannot land before it.
  - `setting_keys.py` is under `rules_based_configuration/`, so the regenerated file will need a pod-enterprise approval, which yours does not satisfy.

  ### Minor, non-blocking

  - Left open and listed in the PR's own caveats: `/staff/arrivals/<hotel>?conf_no=` (`StaffLinkLookup`) is unauthenticated, needs only a confirmation number, and answers a hit and a miss with different redirects, so it tells a caller whether a confirmation number exists and stamps `external_link_first_accessed_at`. Also the group-booking authorization link and authform reservation validation. Worth a follow-up ticket if none exists.
  - The two link views log `hotel_slug` only, without `short_index` or the hotel log context that `raise_if_hotel_has_no_guest_sign_in` uses. Nit.
  - The distinct `reservation_lookup_blocked` code tells a caller the hotel has sign-in off. That is hotel-level, and the hotel payload now publishes the same fact, so I would not push on it.

  ### Draft review comment (not posted; say if you want it sent)

  > Diff looks right to me, and the gate placement before the limiter and query is good. Two questions before I approve:
  > 1. What is `IDENTITY_TOKEN_MODE` in each prod region? Below enforce, `edge_application_sid` trusts a client-sent `X-Canary-Source`, so one forged header skips this gate. I know it is the same check as the product gate, but for a hotel we switch off because of SEC-1762 that is the whole protection.
  > 2. Can you confirm product knows `/cl/` and `/ul/` stop working for a switched-off hotel? Those are in hotels' PMS emails, and the ticket says to keep guest journey message links.
  >
  > The linter failure is stale generated files from the field in #64907 (`generate_setting_types`, `make generate-mcp-sql-grants`).
project: null
source_id: https://github.com/canary-technologies-corp/canary/pull/64911
tags:
- morning-gtd
- github
time_minutes: 20
title: 'Review PR #64911: [STAY-5961] Refuse guest lookups when sign-in is off'
updated: 2026-11-13 10:08:46.182797
waiting_on: null
waiting_since: null
working_on: false
---

SEC-1762 incident fix. Author in15 (Ishwar), branch in15/guest-sign-in-toggle-backend.
https://github.com/canary-technologies-corp/canary/pull/64911