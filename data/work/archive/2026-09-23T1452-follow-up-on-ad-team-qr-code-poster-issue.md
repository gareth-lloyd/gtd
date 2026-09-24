---
area: null
completed_at: 2026-09-24 10:16:04.389947
contexts: []
created: 2026-09-23 14:52:52.391786
defer_until: null
due: null
energy: low
id: 2026-09-23T1452-follow-up-on-ad-team-qr-code-poster-issue
order: null
output: |
  ## Agent run 2026-09-24T10:10:31

  Ticket NOT created. Creating a Linear issue is an outbound write and needs your explicit "yes, create it". Draft below, ready to send verbatim.

  Verified the code claims from the body against master (frontend/check-in):
  - `check-in/src/router.ts:118-131` — `/lookup/:hotelSlug` redirects to LOOKUP and forces `mode: "full"` (comment: "can never be cleaned up because QR codes point to it").
  - `check-in/src/views/Booking/BookingStartPage.vue:337-350` — "look up my reservation" button links to LOOKUP with `mode=full`, `trk_source=booking_availability_search`, `trk_medium=qr_scan`.
  - `check-in/src/views/Lookup/Lookup.vue:144-152` — when registration card not submitted and `mode == LookupMode.FULL`, `router.push({ name: RouteName.CHECK_IN })`. No v3 check.
  - `check-in/src/reservation/Reservation.vue:238` and `check-in/src/reservation/ReservationHeader/Actions.vue:330` — the only two `/guest-experience/` redirects; both gated on `hotel.check_in_configuration.checkin_version === V3`.
  - `check-in/src/views/CheckIn/CheckIn.vue` — no `checkin_version` / v3 guard at all.

  Linear target (read-only lookup):
  - Team: Arrivals / Departures (id d61c0652-d17e-4141-a483-20d0b31130b3), state Triage (id 2ca908e0-1c26-4afe-a538-0df73c8d8e73)
  - Suggested labels: Bug, Feature / GMS: Check-in
  - Suggested priority: Medium (3)

  --- DRAFT TICKET ---

  Title: QR-poster lookup (mode=full) sends guests at v3 hotels into the legacy v2 check-in flow

  Description:

  **Summary**
  Guests at hotels migrated to check-in v3 who arrive via the on-property QR poster and use "look up my reservation" are pushed into the legacy v2 check-in app (`/reservation/<hotel>/<code>/check-in/review`) instead of the guest-experience app (`/guest-experience/<hotel>/<code>`). The pre-arrival link for the same reservation opens v3. The hotel is effectively running two check-in experiences depending on entry point.

  **Observed**
  AmericInn Shakopee (Wyndham), flipped to v3 in the 2026-09-17 batch per Snowflake. A guest landed on `/reservation/<hotel>/<code>/check-in/review?source=qr_lookup&mode=full&trk_source=booking_availability_search&...` — the v2 registration-card review step.

  **Root cause (client-side routing, frontend/check-in)**
  The redirect to `/guest-experience/...` exists in exactly two places, and the lookup flow hits neither:
  1. `check-in/src/reservation/Reservation.vue:238` — reservation landing page redirects to v3 only when the guest previously viewed a check-in link and did not finish.
  2. `check-in/src/reservation/ReservationHeader/Actions.vue:330` — the Check In button redirects to v3 on click.

  The lookup flow bypasses both:
  - `check-in/src/router.ts:118-131` — `/lookup/:hotelSlug` (the plain QR poster URL) forces `mode=full`.
  - `check-in/src/views/Booking/BookingStartPage.vue:337-350` — the booking start page's "look up my reservation" button (on-site-booking QR poster, `source=qr_lookup`) also adds `mode=full`.
  - `check-in/src/views/Lookup/Lookup.vue:144-152` — when the registration card is not yet submitted and `mode == LookupMode.FULL`, it does `router.push(RouteName.CHECK_IN)` with no `checkin_version` check.
  - `check-in/src/views/CheckIn/CheckIn.vue` and the CHECK_IN route in `router.ts` have no v3 guard either. Nothing on the backend redirects; routing is entirely client-side.

  **Impact**
  Every migrated hotel, both QR poster variants (`/lookup/<hotel>` and the on-site-booking start page). Both flows write to the same check-in model, so submissions should still succeed, but v3-only behaviour (whatever differs in the new flow) is skipped for walk-up / QR guests. Affects the Wyndham v3 migration wave; worth flagging to Guido and Lea as a migration gap.

  **Suggested fix**
  Add the same `isCheckInV3` branch to the `LookupMode.FULL` push in `Lookup.vue` (redirect to `/guest-experience/<hotel>/<slug>?<query>` via `window.location.assign`), or better, a single guard on the CHECK_IN route (`beforeEnter` in `router.ts`) so every entry point is covered. Confirm the guest-experience app handles `source=qr_lookup` / `mode=full` / `trk_*` query params sensibly.

  **Caveats**
  Read from master, not the deployed build. Hotel version confirmed via the Snowflake mirror only, not the live API. The specific reservation was not inspected.

  --- END DRAFT ---

  To create it, reply "yes, create it" (optionally with label/priority changes). I will create it via the Linear MCP in team Arrivals / Departures, state Triage.

  ## Agent run 2026-09-24T10:13:47

  User approved ("yes create"). Created AD-10097 (https://linear.app/canary-technologies/issue/AD-10097/qr-poster-lookup-modefull-sends-guests-at-v3-hotels-into-the-legacy-v2) in Arrivals / Departures, state Triage, priority Medium, labels Bug + Feature / GMS: Check-in. Description as drafted above (minus the Guido/Lea name-drop, which was kept out of the ticket). Branch name: glloyd/ad-10097-qr-poster-lookup-modefull-sends-guests-at-v3-hotels-into-the
project: null
source_id: null
tags: []
time_minutes: 5
title: Create a AD team triage ticket for QR code poster issue
updated: 2026-09-24 10:16:04.389939
waiting_on: null
waiting_since: null
working_on: false
---

The route. The path /reservation/<hotel>/<code>/check-in/review is the registration-card review step of the legacy check-in app in
  frontend/check-in. The v3 flow lives at /guest-experience/<hotel>/<code> and is a different app. The hotel, AmericInn Shakopee, was
  flipped to v3 in the 2026-09-17 batch according to Snowflake.

  How the guest got there. The query string tells the story. The hotel has on-site booking enabled, so its QR poster points at the
  booking start page with source=qr_lookup. That page has a "look up my reservation" button which adds mode=full and
  trk_source=booking_availability_search and sends the guest to the lookup form. When the lookup finds a reservation whose registration
  card is not yet submitted, and mode is full, the lookup view pushes the guest straight into the v2 check-in route. The first step it
  lands on is review.

  Why no redirect to v3 happened. The redirect to the guest-experience app exists in exactly two places in the v2 app, and this path hits
  neither:

  - The reservation landing page redirects to v3 only when the guest previously opened a check-in link and did not finish.
  - The check-in button on the reservation header redirects to v3 when clicked.

  The lookup flow with mode=full bypasses both by pushing directly into the check-in route. The check-in router itself has no guard on
  the hotel's version. Nothing on the backend redirects either, since routing is entirely client-side.

  What this means. Any guest at a migrated Wyndham hotel who arrives via the QR poster and looks up their reservation gets the v2
  experience, while a guest who opens the pre-arrival link gets v3. The same applies to the plain /lookup/<hotel> QR posters used by
  hotels without on-site booking, because that route also forces mode=full. Both flows write to the same check-in model, so the
  submission should still work, but the hotel is effectively running two check-in experiences depending on entry point. That is worth
  raising with Guido and Lea as a migration gap, and it is relevant to your earlier question about what differs between migrated and
  non-migrated hotels: for QR-lookup guests, nothing does.

  Caveats. This is read from master, not the deployed build. I did not look up the reservation itself, and I did not confirm the hotel's
  version through the live API, only through the Snowflake mirror as of yesterday evening.