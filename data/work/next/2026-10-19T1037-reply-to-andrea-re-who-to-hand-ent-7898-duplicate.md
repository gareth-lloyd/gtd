---
area: null
completed_at: null
contexts:
- react
created: 2026-10-19 10:37:05.217077
defer_until: null
due: null
energy: low
id: 2026-10-19T1037-reply-to-andrea-re-who-to-hand-ent-7898-duplicate
order: null
output: |-
  ## Agent run 2026-10-19 12:48:18.543563

  **Recommendation: no handoff to integrations, gateway or A/D.** Nothing is broken in the integration, the gateway, or authorizations. The fix is one Canary Admin setting, and the rest is a product gap in Digital Check-In. The ticket is one step from done.

  **Where ENT-7898 stands** (https://linear.app/canary-technologies/issue/ENT-7898/duplicate-card-authorization-from-ota-check-in):
  - Golem's diagnosis: Digital Check-In has no OTA or virtual-card handling. It pushes the guest's card to Opera window 2, the OTA virtual card stays on window 1, and Opera authorizes both. The IHG script didn't cause it; the hotel's window 2 is a manual value the script leaves alone.
  - 2026-10-15: Dan Logan reported that the Rooms Manager chose **Option A**: set `check_in_configuration.credit_card_step = disabled` for `ihg-lancp` (hotel 178). He would rather post cards manually from Digital Authorizations.
  - Dan's caveat: the auth-form card *auto*-push for this hotel was turned off on 2026-05-29. If manual posting depends on the same thing, disabling the check-in card step would leave no way to get a card onto the reservation.
  - Nobody has changed the setting yet. The ticket is still In Progress, assigned to Andrea.

  **I checked Dan's caveat in code.** `authform/services/pms_operations.py:402-412`: `integration_auto_post_cc_to_pms` gates only the *automatic* push. A manually triggered push still goes through when auto-post is off. The one flag that blocks *all* auth-form card pushes, manual ones included, is `authorization_configuration.v2_do_not_post_cards_to_pms`. So before flipping the setting, check in Canary Admin (https://www.canarytechnologies.com/canary-admin/hotels/hotel/178/change/) that `v2_do_not_post_cards_to_pms` is off for hotel 178. If it is off, Option A is safe. I did not check prod data.

  **Who owns what:**
  - Flipping the setting: Enterprise or CS, in Canary Admin. It needs no handoff.
  - Long-term fix (online check-in skips the card step, or sets the guest's window to cash, on OTA and virtual-card bookings, as the kiosk already does): a Digital Check-In feature request for **Guest Experience / In-Stay**, not A/D. Raise it only if more hotels hit this.

  **Draft Slack reply** (thread: https://canarytechnologies.slack.com/archives/C0B1Y5K9AMC/p1792168274917149). NOT SENT.

  > I don't think it needs a handoff. Nothing's broken in integrations, gateway or auths. Online check-in just has no OTA or virtual-card awareness, and the Rooms Manager has already picked Option A (disable the check-in card step for `ihg-lancp`).
  >
  > On Dan's caveat: auto-push being off on the auth forms doesn't block manual posting. The auto-post flag only gates the automatic push. The one thing that would block manual posting is `v2_do_not_post_cards_to_pms`, so check that's off for hotel 178, then set `credit_card_step` to disabled and close it out.
  >
  > If we want the proper fix (skip the card step for OTA/VCC bookings, like the kiosk does), that's a Digital Check-In feature request for Guest Experience, not A/D. I'd only raise it if we see this at more hotels.
  >
  > Since you're out this week, [I can flip it / I'll ask <name> to flip it] so Lansing isn't waiting.

  **Your call:** Andrea is OOO and the hotel has a live payment issue. Decide who flips the setting this week (you, or someone on Enterprise or CS) and fill in the last line. Nothing was sent to Slack or Linear, and no settings were changed.

  ## Agent run 2026-10-19T16:29

  > Follow-up asked: "before flipping the setting, check in Canary Admin that v2_do_not_post_cards_to_pms is off for hotel 178. If it is off, Option A is safe. ... check with snowflake or /debug_in_shell"

  **Result: `v2_do_not_post_cards_to_pms` is OFF (false) for hotel 178, so Option A is safe.** Manual card posting from Digital Authorizations is not blocked.

  I checked the prod mirror in Snowflake (`CANARY_RAW.CANARY`). It is read-only and was synced today at 13:01 UTC, so it is current.

  Hotel 178 (`ihg-lancp`), latest row in each table:
  - `authorization_authorizationconfiguration`: `v2_do_not_post_cards_to_pms = false` and `integration_auto_post_cc_to_pms = false` (auto-push has been off since 2026-05-29, as Dan said). This row last changed on 2026-10-06. It has been `false` in every snapshot back to 2025-09.
  - `check_in_configuration`: `credit_card_step = required`. **Option A has not been applied yet.** The row was touched on 2026-10-15, but the step was still `required` after that.

  Updated draft line for the Slack reply: "Checked: `v2_do_not_post_cards_to_pms` is off for Lansing, so manual posting from Digital Authorizations still works. Safe to set `credit_card_step` to disabled."

  Still to do: someone sets `credit_card_step = disabled` in Canary Admin (https://www.canarytechnologies.com/canary-admin/hotels/hotel/178/change/), then closes ENT-7898. Nothing was sent or changed.
project: 2026-08-31-ihg
source_id: https://canarytechnologies.slack.com/archives/C0B1Y5K9AMC/p1792168274917149
tags:
- morning-gtd
- slack
time_minutes: 10
title: Handle ENT-7898 (duplicate OTA card auth) including handing off to eNT team
  member
updated: 2026-10-19 16:32:48.510106
waiting_on: null
waiting_since: null
working_on: false
---

Andrea asked whether to pass ENT-7898 on after the initial investigation, and to whom: integrations, gateway, or A/D. Open 2 days. Andrea is OOO this week.
https://canarytechnologies.slack.com/archives/C0B1Y5K9AMC/p1792168274917149
https://linear.app/canary-technologies/issue/ENT-7898/duplicate-card-authorization-from-ota-check-in