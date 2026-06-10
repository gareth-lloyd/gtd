---
area: null
contexts:
- react
created: 2026-06-03 11:21:51.605609
defer_until: null
due: null
energy: medium
id: 2026-06-03T1121-catch-up-on-iot-slack-channel-generally
order: null
output: |
  ## Agent run 2026-06-03T13:05

  Caught up on the IoT Slack activity. Note: the link in this item points to
  #crown-resorts (C02JKFTV7K9), but the real IoT discussion lives in the
  dedicated **#integrations-iot** channel (C0AS48SEGNQ) — you joined it today.
  Read both. Summary below.

  ### What the channel is about
  In-room IoT controls (thermostat / lighting / fan) surfaced inside Canary
  Compendium (web) and eventually the mobile SDK app. Driven by two luxury
  customers asking for it: **Crown Resorts** and **Aman**. Belinda's thesis:
  this is the leading edge of broader luxury-brand demand and being first
  helps win future deals. Three GRMS vendors in play: Honeywell (INNCOM),
  Lutron, Crestron.

  ### Crown specifics
  - Crown uses Honeywell INNCOM (Perth) + Crestron (Sydney), today via
    **Intelity**, whose contract expires **end Sep 2026**. They're frustrated
    with Intelity and want to replace it — and we said yes to IoT in the RFP,
    so there's commitment pressure.
  - **NETx middleware** is the proposed technical path (Belinda sourced it).
    NETx sits between Canary Cloud and Crown's existing Honeywell/Crestron
    hardware via BACnet, exposing a REST/JSON "Tree API" (plus MQTT/websocket
    for live data). ~€6,440 one-time per property (by datapoint), no recurring.
    Requires an on-prem Windows VM at Crown; cannot be whitelabelled today.
    Does NOT support Lutron, so it's not a fit for Aman.
  - Proposed plan: NETx → Crown Perth as Phase 1, thermostat MVP by **end Aug**
    (ahead of the Sep Intelity expiry); Sydney = Phase 2. Aman = separate
    Lutron MyRoom XC cloud path, more eng.
  - Eng feasibility (Blake): confident it can be staffed with **1 eng across
    June–Aug, run out of the In-Stay team**, backend+frontend mostly reusable.
    Painful part = mapping varied per-room hardware configs into a coherent UI.
    Belinda (APAC) to quarterback the integration-partner setup + on-site NETx
    install (leaning toward engaging a NETx partner integrator initially).
  - Commercials (Daniel/SJ): Crown willing to commit to a longer-term deal and
    pay for build/support. Daniel handling this directly with Rohit.

  ### >>> CURRENT STATUS (most important — as of Jun 2) <<<
  IoT is effectively **on hold / waiting on Crown**. After the latest meeting,
  Crown took it back for evaluation because they're **planning to switch their
  IoT vendor from Honeywell/Crestron to Interel** (which would be a much simpler
  API integration for us). If that happens, NETx becomes only an *interim*
  solution / a fallback for properties that don't move to Interel. **No timeline
  from Crown** on the decision. (Interel context also discussed in #crown-resorts
  on ~Apr 22: Interel is now a GRMS provider/competitor, signed to replace all
  Honeywell+Crestron at Crown within ~2 years, cloud-native with an open API.)

  ### Decoupled piece likely to proceed: Compendium device binding
  Separate from IoT: Crown wants in-room tablets to auto-display an
  authenticated Compendium session bound to the room's current reservation
  (must rotate between guests). A pure static link is rejected (security — the
  link also works on phones). Blake's proposed flow: a device-binding step that
  caches a room↔device JWT on the tablet so the URL stays static, with
  reservation state cleared at checkout (hackable without MDM lockdown).
  **Adil** to scope it. Belinda wants this delivered FIRST and independently of
  the IoT decision — valuable for expanding Compendium onto tablets regardless.
  Worth tracking as its own potential action.

  ### People
  Belinda (customer/APAC lead) · Blake, Ishwar, Adil (eng; Adil pulling NETx
  Tree/MQTT/websocket Postman collections) · James Saram + Martijn Dekker (newer
  joiners, May) · SJ + Daniel Mourad (commercial).

  ### Suggested follow-ups (your call)
  - Nothing actionable required right now; the ball is in Crown's court on
    Interel-vs-NETx. Consider moving this to `waiting` on Crown's decision.
  - If you want eng to keep momentum, the device-binding piece is the one item
    that's greenlit-ish and decoupled — could be split into its own next-action.

  ## Agent run 2026-06-03T13:45 — deep dive: Compendium device binding

  Pulled the source of truth: Belinda's mini-PRD in Notion ("Auto-Authenticated
  In-Room Compendium Tablets", page 35081468615181f4b257c16688018eee, authored
  2026-04-28), cross-referenced with Blake's Slack design and existing tablet
  infra in Linear.

  ### One-liner
  Guest walks into the room; the in-room tablet ALREADY shows their personalized,
  authenticated Compendium — no QR scan, no last-name+dates, no app download. When
  the room is vacant it shows generic content. Belinda wants this shipped FIRST and
  INDEPENDENTLY of the Crown IoT decision (valuable on its own until the SDK app
  becomes the norm).

  ### Key de-risking insight
  Compendium auth is already URL-bound, not user-bound. Guest enters last name +
  dates (or confirmation #); backend matches Canary's local Reservation table
  (hydrated from Opera via pms-gateway); the frontend just stores the reservation
  UUID in localStorage — that IS the session. No JWT / no server session token
  today. Requests pass the UUID as a query param; endpoints use NoAuthValidator and
  trust it. So binding a tablet reuses the same primitive a guest types in today,
  just provisioned by staff. Not a new auth system.

  ### Two design variants (complementary, not contradictory)
  - Belinda PRD (documented plan): server-side room→reservation binding record.
    Tablet opens static URL compendium.canary.tech/r/<hotel>/<room>; resolver
    302-redirects to the authed Compendium for whatever UUID is currently bound to
    that room (or generic if null). Tablet polls ~30s. No JWT.
  - Blake (Slack): device-binding flow caching a room↔device JWT on the tablet
    (scoped to room, persists across reservations in that room): admin add-device →
    scan QR → link carries JWT → webapp stores it → URL stays static; reservation
    state cleared client-side at checkout. Caveat: HACKABLE without MDM locking down
    the browser's dev tools.
  - In practice they layer: JWT = static room/device identity; resolver maps that
    room → current reservation UUID. Blake "confident we can build this."

  ### Three paths Belinda considered
  - Path A — Opera PMS auto-trigger (subscribe to RESERVATION_CHECKED_IN, auto-mint
    binding). ~4-6 wks. Verdict: right destination, wrong start — Celery latency is
    minutes not seconds, guest can beat the event to the room, walk-ins/room-moves
    multiply edge cases. Layer on as v2.
  - Path B — Front-desk activated (staff clicks "Activate Room 304" at check-in →
    writes UUID to binding record → tablet polls/refreshes). ~1-1.5 wks. *** RECOMMENDED
    v1 ***: instant, hotel keeps control + audit trail, reuses UUID auth, forward-
    compatible (Path A calls the same endpoint). Risk: staff forgets the button →
    default-on in check-in flow.
  - Path C — Guest self-bind via QR/NFC on key-card sleeve. ~3-5 days. Fallback only —
    breaks the "magic", not differentiated from "use your phone".
  Recommendation: build B as v1, layer A as v2 (B's primitives are exactly what A needs).

  ### Path B build spec
  1. Tablet device registry: <hotel>+<room> → device_id + currently_bound_reservation_uuid + bound_at
  2. Activation endpoint: POST /tablet/<hotel>/<room>/activate {reservation_uuid}, staff-auth gated
  3. Activation UI: button in existing check-in flow ("Activate Room Tablet"), default-on
  4. Tablet resolver: GET /r/<hotel>/<room> → 302 to authed Compendium (or generic if null)
  5. Tablet polling: lightweight 30s client check for binding changes
  6. Release logic: auto-clear on PMS checkout event + manual "Release" button for housekeeping

  ### Risks (PRD)
  - Staff adoption — skip the button = feature dies → default-on + visible state.
  - Stale bindings — failed checkout release leaks prior guest data → PMS webhook +
    nightly sweep + manual release.
  - Hardware variance — beta tablets differ in OS/browser; validate polling everywhere.

  ### Open questions Belinda flagged for Nico (unresolved)
  1. Which 2-3 beta hotels (need existing tablet hardware)?
  2. Generic/vacant mode — reuse public Compendium or build a slimmer "lobby mode"?
  3. Activation button placement — in check-in flow vs separate surface?
  4. Room moves mid-stay — auto-rebind via Opera room-change event or manual?
  5. Multi-tablet suites — one binding fans out or per-tablet?
  6. Staff training / preview mode before guest arrival?
  7. Binding lifetime — full stay vs rolling 24h refresh?

  ### Status / ownership / connections
  - Status: DISCOVERY/SCOPING. PRD by Belinda Wang 2026-04-28 ("for review with Nico").
    Adil scoping eng. NO dedicated Linear ticket exists yet (all tablet hits in Linear
    are the EXISTING check-in/kiosk "Tablet Registration" feature, not this auto-auth
    piece).
  - Origin: surfaced in the Crown IoT thread (Crown wants Compendium on in-room iPads
    replacing Intelity); Belinda decoupled it so it proceeds even though Crown's IoT
    integration is frozen pending the Interel decision.
  - Reusable infra: Canary already has "Tablet Registration"/"Push to Tablet" for
    check-in kiosk devices (HotelDevicePopup.vue, device-settings admin, add/unlink
    flows) — likely foundation, but owned by Arrivals/Departures while Compendium is
    In-Stay (team-ownership question to resolve).
  - Adjacent: STAY-3400 ([Compendium] room-specific QR codes, Pomeroy Hotel, In-Stay,
    backlog) is a lighter cousin — shares design space with Path C.

  ### Two things to verify before treating the PRD as final
  1. Which design eng adopts — Belinda's no-JWT server-side binding record vs Blake's
     JWT-cached-on-device (security models differ; Blake's needs MDM lockdown).
  2. Which team owns it given In-Stay (Compendium) vs Arrivals/Departures (existing
     tablet registry) split.
project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 15
title: catch up on IoT slack channel generally
updated: 2026-06-09 15:28:13.528263
waiting_on: null
waiting_since: null
working_on: false
---

https://canarytechnologies.slack.com/archives/C02JKFTV7K9/p1778718190577629