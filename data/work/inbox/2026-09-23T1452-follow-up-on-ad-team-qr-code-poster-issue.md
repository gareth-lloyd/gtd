---
area: null
completed_at: null
contexts: []
created: &id001 2026-09-23 14:52:52.391786
defer_until: null
due: null
energy: low
id: 2026-09-23T1452-follow-up-on-ad-team-qr-code-poster-issue
order: null
output: ''
project: null
source_id: null
tags: []
time_minutes: 5
title: Follow up on AD team QR code poster issue
updated: *id001
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