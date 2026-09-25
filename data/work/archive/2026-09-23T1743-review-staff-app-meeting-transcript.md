---
area: null
completed_at: 2026-09-24 15:15:52.276869
contexts: []
created: 2026-09-23 17:43:47.138654
defer_until: null
due: 2026-09-24
energy: low
id: 2026-09-23T1743-review-staff-app-meeting-transcript
order: null
output: |
  ## Agent run 2026-09-24T10:30:00+03:00

  Source: Granola "Mobile block planning", 23 Sep 2026 17:01 GMT+3 (https://notes.granola.ai/d/5bc6a835-e3a9-4c2f-b7fe-d01293a11c74). Run by Caitlin (mobile) then Mike (Staff Ops). Attendees inc. Diana, Francisco, Connor, Blake, James, Eric, Marshall. Transcript tail (~last 20 lines) is unrelated TV audio, ignore.

  ### Mobile block (Caitlin)

  1. **Custom views (Best Western)** - top priority. BW rejects every standard SDK view (IHG/Wyndham use "flavors" of standard SDK). Audit found more gaps than expected: some APIs not exposed in React Native, TPIN-on-checkout unfinished, BLE custom views don't exist at all. Concern raised: past comms overstated readiness (same pattern as IHG/Wyndham, 2 months of post-launch fixing). Connor confirmed BW is actively building on custom views: reservation lookup + check-in done, seen only on recordings. DECISION: proceed. Estimate 3 weeks, Diana + Francisco + 1. Francisco: custom views work tidies the shared API, both paths use the same flow so both stay maintainable.
  2. **Push notifications in staff app** - reported broken; mobile owns investigate + fix.
  3. **Team chat -> staff app** - mobile owns. <30 hotels on team chat today, pricing/commercial status unclear (Jake handed to Rachel, nobody has spoken to her since). Strong brand pull: Bainbridge, Remington, Hilton all say staff must not use WhatsApp about guests. "No hesitation" on prioritising. Ownership split: Staff Ops = ticketing/housekeeping; mobile = team chat + guest messaging in staff app. Not religious about it.
  4. **Loyalty gift page in check-in SDK (IHG)** - break welcome gifts out of the upsells step into its own step. 1-2 weeks, aligned with Arrivals & Departures timeline. Same API contract. Action: brain dump from Vebor so SDK is built for configurable check-in V3 steps, not narrowly for welcome gifts.
  5. **Apple Pay / Google Pay in tipping (Wyndham in-stay)** - "easy win", build a generic wallet component reusable across flows. Coordinate with Tracy/Yasmin (payments pod actively improving both). Diana to get brain dump from Yasmin on "Canary payment form" / payment submitter. Not this block: payments pod building external wallets (Wyndham cards on file) - mobile should start thinking about it.
  6. **BLE in Wyndham SDK** - BLE SDK built (Francisco + physical access), tested on Salto; Dormakaba + Assa next, then embed in Wyndham app. Direction: push everything into Wyndham's in-stay app and sunset the WyndhamKey white-label OpenKey app; non-member access unresolved. Note WyndhamKey runs on old OpenKey servers, so there's a handoff period. Guest App / OpenKey sunsetting isn't on this plan but Wyndham is the first customer to work it through over the next few blocks.
  7. **Messaging SDK enhancements (Langham, due January)** - attachments, membership-level (vs reservation-level) message view. Both exist on web already.
  8. **Accessibility (Diana)** - AA certification is contractual before IHG uses the SDK. Third-party audit done (likely Level Access). ~1 week eng fixes, ~3 weeks certification. Diana meeting Amanda same day.

  ### Leadership themes worth noting

  - Three times in the session prioritisation stalled because nobody was close to the user/outcome (BW progress, team chat usage, Langham). Ask from leadership: come prepared with justification; "historical work creates new work and teams look for work"; respecting eng time.
  - Product-to-SDK parity will always be "one catches up to the other" on the guest side because native SDKs are a hard requirement. On the staff side the web and React Native messaging UIs could share far more. Blake wants to reassess ownership boundaries / a "donation" model where product teams contribute to mobile as they build. I flagged Shopify moving away from React Native toward platform-native with heavy tooling; I offered to find the article link (small open loop).

  ### Staff Ops block (Mike)

  - Last block was 0->1 for ticketing + housekeeping (pilots lined up, ticketing going live this/last week, housekeeping dev finishing ~end of block). Next block goal: 1->10 pilot properties. Later tranches 10->100, 100->1000, each with different unlocks.
  - Adoption = ~2 weeks continuous daily core-action usage. Signal is slow because it changes whole-department workflow (unlike check-in, where the guest side forces adoption). Onboarding quality is critical; Mike + Marshall doing in-person property visits to build a playbook. Network effect inside a hotel, hence the mobile login/frictionless auth work.
  - Backlog if capacity allows, priority order: preventative maintenance (all 4 ticketing pilot conversations asked; recurring tasks keyed off last-completed date rather than housekeeping's schedule model); agentic features (mass create/edit tickets, natural-language ticket creation, supervisor room-assignment automation). Brand interest: IHG next week, Marriott week after; competitors named: HotSOS/Alice-type incumbents and upstarts (Lance, Tempo).
  - PMS integration (TAM expansion, more relevant at 100->1000): starting with Opera Cloud (~2,000 properties). Housekeeping needs write-back for room status or PMS desyncs. David Thompson (PMS Gateway) idea: one-way read + trigger the PBX room-clean code via AI voice from the mobile app as a pseudo write-back. Connor: robust integrations (10+) can expose room status read/write easily, not a blocker; PBX path still worth exploring but should be pushed to PMS Gateway to own, not built by Staff Ops. Marriott on Agilysys: no integration possible until next year at earliest, PBX path relevant there.

  ### Actions recorded in the meeting

  - Connor: pulse-check Best Western on custom views progress; get Caitlin into their Teams.
  - Caitlin: brain dump from Vebor on check-in V3 direction before loyalty gift SDK work.
  - Diana: brain dump from Yasmin on Canary payment form; confirm AA certification process with Amanda.
  - Caitlin/Mike: follow up with Rachel on team chat pricing/ownership.
  - Me (soft): send Blake/Caitlin the Shopify React Native article I mentioned.
project: 2026-09-08-mobile
source_id: null
tags: []
time_minutes: 5
title: Summarize mobile block planning transcript from 23rd September granola
updated: 2026-09-24 15:15:52.276850
waiting_on: null
waiting_since: null
working_on: false
---