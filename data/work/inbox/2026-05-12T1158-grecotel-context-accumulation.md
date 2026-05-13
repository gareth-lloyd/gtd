---
area: null
contexts: []
created: 2026-05-12 11:58:23.049295
defer_until: null
due: null
energy: low
id: 2026-05-12T1158-grecotel-context-accumulation
order: -5
output: '## Agent run 2026-05-12T12:05:00


  Read #grecotel (C0AHERMJRHN) back to 2026-04-21 and pulled the Grecotel Hardening
  Linear project. Saved long-term context to `project_grecotel_pilot.md` (now in MEMORY
  index). Headline state below.


  ### Where the deal stands

  - **Status: at risk.** Other products (messaging, F&B/compendium, upsells, checkout)
  are live at Caramel since 2026-04-30. **Check-in is the blocker.** Ioannis (KDM)
  asked 2026-05-08 for a written timeline of solves before deciding; explicitly does
  not want more test calls until things actually work. They are reviewing Duve and
  have a native app ready to deploy.

  - **Strategic stakes:** Lambros (HIT/Grecotel partner) signaled partnership + 1M
  EUR Greek market access if Caramel succeeds. Caramel is seasonal (closes November)
  — any Q3 slip on the custom V3 check-in flow likely means no use this season.

  - **Ian Clark (PMS lead) proposed sending an eng on-site** 2026-05-08 to debug live
  with HIT and Grecotel''s developer. Waiting for Aksel to clear with the hotel.


  ### Linear: Grecotel Hardening project

  Project: https://linear.app/canary-technologies/project/grecotel-hardening-7ace7eaa814a


  **Completed / Deployed (since 2026-05-08):**

  - EMEA-242 Protel additional adults not being set (Urgent) — Deployed

  - EMEA-248 ID dropdown Greek translations — Deployed

  - AD-7618 Log more info for additional-guest OCR failures — Done

  - AD-7619 Fix MRZ processing — Done

  - Greek-text-in-OCR fix deployed 2026-05-11 (A&D)

  - Additional-guest count edge cases fix deployed 2026-05-11 (Martijn)


  **In flight:**

  - EMEA-244 Hide additional guest fields entirely (not just read-only) — In Review
  (Martijn)

  - AD-7621 Accompanying guest ID submission for OCR failing — In Progress (Laura).
  Dana pushed a candidate fix 2026-05-12 05:46, needs test reservations to verify.


  **Backlog / unowned timeline:**

  - AD-7623 Move signature to end of check-in flow (V3) — **Q3 target, customer calls
  it deal-breaker for go-live.** Vibhor wants to scope on a call early next week and
  asked for an example reservation showing their desired flow.

  - EMEA-245 Delay immediate GJ-sending (handle 5-min Protel companions sync lag for
  walk-ins) — Medium priority.


  ### Vibhor''s 11 follow-ups from 2026-05-09 message (current state)

  - 1a/b done or in review.

  - 2a known (additional guest miscount). 2b blocked on 2c being fixable. 2c = AD-7621,
  in progress.

  - 3 Greek-text OCR — Dana shipped deploys; needs verification on real test res.

  - 4 ID translation — EMEA-248 deployed.

  - 5 Mobile login on EU domain — **still no owner.** Awaiting Aksel clarification.

  - 6a customer accepted pushback on primary name overwrite. 6b = AD-7623 (signature
  flow); Vibhor wants a call to spec exactly where signature lives (after primary?
  after all guests?).

  - 7 Name-swap bug (reservation primary swapping with companion) — Laura fixing;
  Vibhor asked Aksel for the specific failing example.

  - 8 Re-edit of accompanying ID should refresh OCR data — needs example reservation.

  - 9 Required vs optional fields — config task on Aksel.

  - 10 Child information capture — requirement unclear, Vibhor asked Aksel/Sebastian
  to clarify.

  - 11 Duve pilot status — Vibhor flagged contradiction (Manolo previously said they
  weren''t piloting Duve). Vibhor wants a copy of Grecotel''s own native-app flow
  so we know what we''re benchmarked against. **Manolo had not responded as of 2026-05-12
  07:55.**


  ### Open user-side asks blocking progress

  - **Test reservations on Caramel** — repeatedly requested (Laura 2026-05-11, Dana
  2026-05-12, Martijn 2026-05-12). Aksel/Manolo to provide; without these the freshly
  deployed fixes can''t be QA''d.

  - **Push back next hotel meeting** so Vibhor can join — Aksel to schedule for early
  next week, 17:30+ Greek time (07:30 PT).

  - **Get example reservation in Grecotel''s native app** to anchor V3 flow scope.

  - **Push to KDM:** written timeline (bug-by-bug dates + honest Q3 date for V3).
  Sentiment around Aksel/Manolo holding off direct convo until that timeline is finalized
  internally.


  ### Tech context worth carrying forward

  - PMS = Protel On-Prem; reseller is HIT (not Planet). Grecotel maintains accompanying
  guests in a *custom local DB table* ("companions") that''s not exposed via Protel
  API. Yauheni emailed Protel 2026-04-29 asking for a new companions API; in parallel
  Grecotel is building a sync trigger from accompanying-guest profiles → companions
  table. Workaround couldn''t be confirmed because 2c blocked it; unblocks once AD-7621
  lands.

  - Rate-plan error (`RatePlanId does not match to RatePlanCode!`) traced to COMP
  / Virtual rate code in Grecotel master data — HIT response: hotel-side config fix,
  not Canary.

  - WhatsApp message editing/deleting surfaced 2026-05-08 as new P2 ask (no ticket
  yet).

  - Restaurant bookings — they have this in their native app, part of their "why Canary"
  calculus (no ticket).


  ### Suggested follow-ups for you (not actioned without approval)

  - Chase Aksel/Manolo on test reservations + Vibhor''s #11 (Duve pilot + benchmark
  flow).

  - File tickets for the two un-ticketed P2 items: WhatsApp edit/delete, restaurant
  bookings link.

  - Push for the on-site visit decision (Ian''s 2026-05-08 proposal).

  - Decide internally on the written timeline message before next KDM touch.


  Full long-term context saved to `project_grecotel_pilot.md` in memory.


  ## Agent run 2026-05-12T12:35:00 — Crete visit prep


  Gareth flagged he may be the engineer Ian proposed sending on-site. Below is what
  he should know that isn''t already in his head (he already has: Protel webhook+responses-table
  pattern, additional-guest hack, no sandbox, companions = their own system, HIT goal,
  Vibhor/Dana/AD on the step issue).


  ### People at the property

  - **Ioannis (KDM)** — frustrated, has explicitly told Aksel no more test calls until
  things actually work. Wants a written timeline before deciding stay-or-Duve. Don''t
  demo, show results.

  - **Maria (GM)** — warmer. Said "Canary is the last of her worries" because messaging
  is delivering. Relationship insurance if Ioannis sours.

  - **Minas + Lucas** — FO managers; the day-to-day at reception during testing.

  - **Grecotel''s internal developer** — built the native check-in app and is building
  the trigger that syncs accompanying-guest profiles → companions table. This is the
  person to spend hours with, not Ioannis. Also grab a copy of the native-app flow
  (still open: Vibhor''s #11).

  - **HIT** — Vaios found the rate-plan mapping issue. Lambros (HIT exec) is the partnership
  lever — Brad/Ian have been framing this trip as deepening HIT, not just fixing one
  hotel.


  ### Concrete prep before flying

  - **Self-service test-reservation capability.** Aksel called this out as the #1
  bottleneck (20+ scenarios from your laptop, no Ioannis dependency). Confirm with
  Yauheni/Ian what access you''ll have on site — Protel UI? Script via HIT? If you
  land without this the trip stalls within an hour.

  - **Mobile EU-domain login bug (Vibhor #5)** still has no owner. Could be SSO config,
  could be a real bug. Bring a checklist: hotel wifi, iOS + Android, personal + company
  phones, `eu.canarytechnologies.com`. Easy win if you can crack it on the ground.

  - **Rate-plan error** (`RatePlanId does not match to RatePlanCode!`) — HIT response
  was that it''s a hotel-side Stammdaten config issue (COMP/Virtual rate code). Raise
  it with HIT in person; otherwise it''s a chargeable remote-config job they''ll never
  schedule.

  - **Companions table schema** — Yauheni identified the table Protel uses. Get the
  exact table + column structure from him before you fly so you can validate the sync
  trigger end-to-end with their developer.

  - **V3 signature-at-end flow** — Q3 target, customer calls it deal-breaker. Don''t
  volunteer dates. Vibhor wants to spec where signature actually lives (after primary?
  after all guests?) — get an example reservation in their native app on site and
  bring it back.


  ### Tech state you''ll walk into (post 2026-05-11/12 deploys)

  - Greek-text OCR fix, ID dropdown translations, additional-adult miscount, additional-guest
  count edge cases, and MRZ processing all deployed but **unverified on real Protel
  data** because no test reservations.

  - AD-7621 (accompanying-guest OCR submit failing) — Laura/Dana fix pushed 2026-05-12
  05:46, unverified.

  - Companions workaround never confirmed end-to-end because OCR submit blocked it.
  The loop on site: generate reservation → primary check-in → accompanying with ID
  → confirm OCR + doc attach → confirm companions table row → confirm it surfaces
  in Protel UI.


  ### Landmines

  - They want Roman/English characters only because Protel runs in English. Don''t
  suggest preserving Greek as fallback — they actively don''t want it.

  - They''re benchmarking us against their own native app AND Duve in parallel. "This
  is hard" gets compared to two working alternatives — frame as "here''s what we do
  that they don''t."

  - Caramel closes in November (seasonal). Q3 slip = no use this year.

  - Two un-ticketed P2 asks that may come up in person: WhatsApp message edit/delete,
  and a restaurant-bookings link from Canary. Log if raised; don''t scope on the spot.


  ### What success looks like

  1. Leave with self-service test-reservation capability — no longer Ioannis-dependent.

  2. Companions sync trigger working end-to-end on at least one test reservation.

  3. Mobile EU-domain login fixed or root-caused.

  4. Copy of their native check-in flow handed to Vibhor for V3 scoping.

  5. Working channel with HIT (Vaios + whoever owns Stammdaten) so rate-plan + future
  config issues stop bouncing through Aksel.


  The framing: this trip isn''t about demoing fixes. It''s about removing every bottleneck
  that has us testing through Ioannis. Make the next demo bulletproof without him.

  '
project: null
source_id: null
tags: []
time_minutes: 5
title: Grecotel context accumulation
updated: 2026-05-12 14:44:52.921154
waiting_on: null
waiting_since: null
working_on: false
---

Read through slack channel
https://canarytechnologies.slack.com/archives/C0AHERMJRHN

Follow leads