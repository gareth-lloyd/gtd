---
area: null
completed_at: 2026-11-13 12:15:29.553907
contexts: []
created: 2026-11-11 01:07:02.394218
defer_until: null
due: null
energy: null
id: 2026-11-11T0107-file-ticket-kiosk-pair-device-has-no-attempt-limit
order: null
output: |
  ## Agent run 2026-11-13T12:09Z

  **Not filed.** Filing is a Linear write and needs your explicit yes. The draft is ready to file as below.

  ### Duplicate check: no duplicate found

  Searched Linear (open, closed and archived) for "pair-device", "pairing code", "kiosk MFA", "kiosk rate limit", "kiosk device token", and all kiosk tickets from the last 5 days. Nothing covers an attempt limit on pairing or the physical-demo MFA skip.

  Closest tickets, none of which cover this:
  - SEC-87 (https://linear.app/canary-technologies/issue/SEC-87/medium-kiosk-device-pairing-endpoint-allows-unauthenticated-device), Done 2026-07-18. Same endpoint. It closed pairing by hotel slug for real hotels. Its acceptance criteria "rate limit device creation" and "log and alert on unusual pairing activity" were never built, so this ticket is the unfinished part of SEC-87.
  - AD-10823 (https://linear.app/canary-technologies/issue/AD-10823/guest-profile-mfa-verify-has-no-attempt-limit-so-the-6-digit-code-can-be-brute-forced), guest profile MFA with no attempt limit. Same class of bug, different endpoint. Sibling, not a duplicate.
  - AD-10738 (https://linear.app/canary-technologies/issue/AD-10738/anonymous-hotel-device-channel-exposes-guest-pii-and-device-tokens), Triage. Device tokens leak over the anonymous SSE channel. Different route to the same never-expiring token.
  - SEC-1029 (https://linear.app/canary-technologies/issue/SEC-1029/hotel-device-tokens-are-logged-in-plain-text-and-the-token-alone), Todo. Device tokens logged in plain text.
  - AD-10367 (https://linear.app/canary-technologies/issue/AD-10367/unify-kiosk-device-pairing-and-setup-under-one-devices-resource), Backlog. Pairing refactor, no security scope.
  - STAY-5961 (https://linear.app/canary-technologies/issue/STAY-5961/disable-anonymous-reservation-lookup-everywhere-except-paired-devices), In Review, and AD-10844 (https://linear.app/canary-technologies/issue/AD-10844/require-confirmation-on-reservation-lookup-from-apps-without-a-paired), Triage. Both make a paired device the only way to do an anonymous reservation lookup. That raises the value of a device token, and so of this ticket.

  ### Code re-checked on current master

  Checked `origin/master` at `bc530137bf3` (the draft cites `414aa1c07f4`). `kiosk/views/devices/pair.py` and `DeviceManagementService._validate_mfa_token`, `generate_pairing_code` and `get_kiosk_configuration_for_pairing_code` are unchanged: still `NoAuthValidator`, CSRF-exempt, no rate limit, and MFA is skipped when `has_physical_demo_simulation` is set and no token is sent. No commit has touched these files since AD-10550 (#62046). The other line references and the production counts were not re-checked.

  ### Recommended filing

  - **Team: Arrivals / Departures**, not Security. CODEOWNERS line 505 gives `/backend/canary/kiosk/` to `pod-arrivals-departures`, and SEC-1766 (https://linear.app/canary-technologies/issue/SEC-1766/evaluate-unauthenticated-api-and-guest-api-endpoints-in-backendcanary) files each finding with the owning pod (AD-10823 is the precedent).
  - **Product is Kiosk, not Tablet Reg V1.** The endpoint is `/kiosk_api/app/pair-device` in `backend/canary/kiosk/`, with a `KioskConfiguration` pairing code and TOTP. Tablet Reg V1 pairs through `hotels/views/api/hotel_device/` with a staff-approved handshake (see AD-10738). Federico's comment on AD-10819 (https://linear.app/canary-technologies/issue/AD-10819/front-desks-cannot-find-reservations-on-the-tablet-reg-v1-page-paired) draws that line and says AD is the right route either way. Tablet Reg V2 setup also uses a pairing code (AD-10799 title), so it may share this flow; not checked in code.
  - The Kiosk Linear team (KSK) is still in use (PR #64432 is on a `ksk-6585` branch), but the October kiosk security tickets (AD-10347, AD-10348, AD-10370) all went to AD, so AD is the recommendation.
  - **Priority:** Medium (3). **State:** Triage.
  - **Labels:** `Security` and `SEC-1762`, as on SEC-1766. Not verified that both labels exist on the AD team.
  - **Relations:** related to SEC-1766, SEC-1762 (https://linear.app/canary-technologies/issue/SEC-1762/block-reservation-lookup-enumeration-with-header-and-parameter-checks), SEC-87, AD-10738.
  - **Title:** unchanged.
  - **Description:** the draft in the body, unchanged, with this section added between Likelihood and Ask:

  ```
  ## Context

  - Found during SEC-1766 (audit of unauthenticated endpoints) after the SEC-1762 enumeration attack.
  - SEC-87 closed pairing by hotel slug for real hotels. Its rate-limit and alerting criteria were not built. This ticket covers them.
  - STAY-5961 and AD-10844 make a paired device the only way to do an anonymous reservation lookup, so a device token is worth more to an attacker than before.
  - AD-10738 and SEC-1029 cover other ways a device token can leak. AD-10823 is the same missing attempt limit on guest profile MFA.
  ```

  ### Still open

  - Counts (122 configurations, 8 physical-demo hotels) and the traffic baseline are still one region only. I did not run anything against production. The ticket already says so in its agent notes.
  - The "Separate, smaller scoping gaps" section is left in this ticket. Splitting it into a second ticket is your call.

  ### Filed 2026-11-13T12:15Z

  Filed on your approval as **AD-10851** (https://linear.app/canary-technologies/issue/AD-10851/kiosk-pair-device-endpoint-has-no-attempt-limit-and-skips-mfa-for). Arrivals / Departures, Triage, Medium, labels `Security` and `SEC-1762`, related to SEC-1766, SEC-1762, SEC-87 and AD-10738. Unassigned. Description is the body draft plus the Context section above. The "Not filed" line at the top of this run is superseded.
project: null
source_id: null
tags: []
time_minutes: null
title: 'File ticket: kiosk pair-device has no attempt limit and skips MFA for physical-demo
  hotels'
updated: 2026-11-13 12:17:00.000000
waiting_on: null
waiting_since: null
working_on: false
---

Draft ticket text below. Not filed in Linear yet. Suggested team: Security (or the kiosk pod under CODEOWNERS for `backend/canary/kiosk/`). Suggested priority: Medium. Related: SEC-1766, SEC-1762.

Before filing: the configuration counts are from one region's shell. Run the count script in the other two regions if a full number is needed.

---

# Title

Kiosk pair-device endpoint has no attempt limit and skips MFA for physical-demo hotels

# Description

## Problem

`POST /kiosk_api/app/pair-device` (`url_name: kiosks_app_pair_device`) needs no authentication and returns a kiosk device token to a caller who supplies a valid pairing code. Nothing in the application limits attempts.

- The pairing code is 6 characters from A-Z and 0-9, about 2.2 billion values. It is generated once per kiosk configuration, never rotated, and reusable.
- An invalid code returns `invalid_pairing_code` before MFA is checked, and a valid code without a token returns `missing_mfa_token`. A caller can confirm valid codes without the MFA token.
- MFA is a 6-digit TOTP with `valid_window=1` and no attempt cap, about 333,000 guesses on average.
- MFA is skipped when the kiosk configuration is in physical-demo mode and no token is sent. 8 active hotels on a real PMS are in that mode, so the pairing code alone pairs a device there.

## Impact

A device token never expires and is scoped to its hotel. It allows:

- Guest search at that hotel by first and last name plus a date, confirmation number or membership number. The response includes name, email, phone, address, nationality, ID document, room number and mobile keys.
- Reading the kiosk configuration, which includes the staff-override PIN.
- Starting kiosk sessions for a found reservation: payment, ID capture, checkout and key encoding.
- Exemption from the guest reservation lookup rate limiter, and trusted-caller status there, at that hotel.

Pairing raises no alert and writes no audit event. The dashboard device list shows only devices created in the last hour or recently connected, so an idle rogue device drops out of view while its token stays valid.

## Likelihood

Low today, and noisy. With 122 kiosk configurations, a guess hits a valid code about once in 18 million tries, and one of the 8 no-MFA hotels about once in 270 million. Normal traffic on the route is 5 to 25 requests a day, and the past week shows no brute-force attempt. A distributed source at a few hundred thousand requests an hour could find a valid code in days.

## Ask

1. Add a rate limit and an attempt cap to `pair-device`. A per-IP limit alone is not enough against distributed sources, so include a fleet-wide or per-code budget.
2. Add an attempt cap to MFA validation per kiosk configuration.
3. Return one error for an invalid code, a missing MFA token and an invalid MFA token.
4. Do not skip MFA for a hotel on a real PMS, whatever its simulation mode. Review the 8 hotels now in physical-demo mode and switch off the mode where it is not needed.
5. Alert on new device pairings, and add a monitor at 50 failures an hour fleet-wide on `kiosks_app_pair_device`.
6. Consider rotating the pairing code after a device pairs, and giving device tokens an expiry.

## Separate, smaller scoping gaps (could be a second ticket)

- `PeripheralsAPIView.get` takes a hotel slug and no token.
- `PeripheralsAPIView.post` does not compare the token's hotel with `hotel_slug` before creating an encoder.
- Kiosk hardware-server attach has no hotel check.

+++ Agent notes

- View: `backend/canary/kiosk/views/devices/pair.py` (`PairAPIView`, `NoAuthValidator`, CSRF-exempt).
- Service: `backend/canary/kiosk/services/device_management.py`: `generate_pairing_code` at 131-133, `_validate_mfa_token` at 109-121, `get_kiosk_configuration_for_pairing_code` at 136.
- Model: `backend/canary/kiosk/models/configurations/kiosk_configuration.py`: `mfa_secret` at 467, `pairing_code` at 560, generation at 826-834.
- Device-token reach: `backend/canary/kiosk/views/reservations.py` (search parameters 53-60 and 209-217, limit 20 a minute and 200 an hour per device at 62-63), `backend/canary/kiosk/views/hotel.py`, `backend/canary/kiosk/views/sessions/sessions.py`.
- Lookup exemption: `backend/canary/guest/views/guest_reservations_view.py:490-537`.
- Scoping gaps: `backend/canary/kiosk/views/devices/peripherals.py:76-115`, `backend/canary/kiosk/services/kiosk_hardware_server.py:23-34`.
- All line numbers are from `origin/master` at `414aa1c07f4`.
- Not verified: whether Cloudflare limits this path; what physical-demo mode changes on a kiosk with a real PMS; whether key encoding yields a usable key remotely; `PACSGatewayService.create_encoder`; `kiosk/views/workbench/*` views that use `NoAuthValidator`.
- Counts: 122 configurations, 1 with no MFA secret (not a real active hotel), 8 real active hotels in physical-demo mode. One region only.
- Traffic baseline: Groundcover, us-west-2, 4 to 11 November 2026. EU and AP not checked.

+++