---
area: null
completed_at: null
contexts: []
created: 2026-08-05 14:02:52.083195
defer_until: null
due: 2026-08-06
energy: low
id: 2026-08-05T1402-yes-no-decision-on-hotelkey
order: null
output: |
  ## Agent run 2026-08-06T09:58

  **Note on the name:** this is **Hotelkit** (DACH hotel-ops / ticketing platform), not
  HotelKey (the PMS). Two different vendors, easy to conflate.

  ### Recommended opinion: YES — EMEA should execute it, but not additively

  The build is the cheap part; the regional wrapper around it is the expensive part, and
  that wrapper is EMEA-shaped. Handing it to Messaging swaps a ~32-point templated adapter
  build for a large coordination tax and *still* doesn't fix the schedule.

  ### The artifacts (both exist, PRD is fresh)

  - **PRD: HotelKit Service Ticketing** — v0.3, 2026-08-03, owner James Saram. Lives under
    the EMEA EPD Pod page. https://app.notion.com/p/3b181468615180c48182c852ac5b08ae
  - **Linear project** — "Hotelkit Service Ticketing integration (DACH region)", team
    **EMEA**, initiative **EMEA - Integrations**, High priority, labelled 2026 Q3 Block 2.
    **Backlog, no lead, no target date, no milestone dates.**
    https://linear.app/canary-technologies/project/hotelkit-service-ticketing-integration-dach-region-29dc0b19a086
  - **Origin ticket** EMEA-393 https://linear.app/canary-technologies/issue/EMEA-393
  - Business case (Google Doc):
    https://docs.google.com/document/d/18axflhSH___KwynkCjkEheW_s0WviRjFJ8b6MmI_9e8/edit
  - No separate eng design doc yet — the PRD explicitly says it is *not* the engineering
    artifact. The `ticketing-integration-builder` skill requires a signed-off design doc
    (Gate 4) before code. That doc is missing from the plan and the estimates.
    Skill: https://github.com/canary-technologies-corp/canary/pull/51598

  ### Why EMEA

  1. **Direct precedent, same team, same pattern.** BPN Maestro — Canary's 7th ticketing
     integration — was built by **EMEA**, lead **Marta Ochowicz Malarz**, Q2 Block 2,
     9 Apr → 19 Jun, completed. The PRD names BPN as the closest template (HubOS for the
     webhook receiver). Second time through is faster.
     https://linear.app/canary-technologies/project/new-ticketing-integration-bpn-maestro-fbc8bbf13311
  2. **Small, templated build.** 32 points over 12 tickets (EMEA-424→433, EMEA-555), all
     already written and labelled `Feature / Ticket Gateway`. It's an adapter implementing
     `TicketService` + `RecommendedTicketVendor`, a webhook receiver, and an FE adapter.
  3. **Voice comes free.** Voice service tickets shipped July 2026 via IC Berlin (HotSOS),
     led by **Martijn Dekker** — EMEA. Hotelkit inherits it through EMEA-430. That context
     is already in EMEA's heads, plus 60+ reusable ICB-* test cases.
  4. **Strategy fit.** "Service ticketing" is one of the five named bets in the EMEA Product
     Prioritisation Framework. Hotelkit is DACH-only — it is a regional market wedge by
     definition. https://app.notion.com/p/384814686151809ea6c1c4514a93aea4
  5. **The hard parts are regional, not technical:**
     - Hotelkit **inverts** the metadata pattern — Canary *pushes* request types via
       `PUT /setup/requests` with **de_DE labels**. Someone needs real DACH hotel vocabulary;
       machine-translated labels degrade AI match quality (the EMEA-367 lesson).
     - **Vendor-controlled certification gate** — a joint testing session before pilot
       approval. No prior integration had this.
     - **GDPR / subprocessor listing / DPA** are blocking for launch, in the strictest-scrutiny
       region. That muscle sits in EMEA.
     - Pilot coordination runs through Jerome (CS) and Bendix Urlbauer (Sales) — EMEA contacts.
  6. **Ownership model already says so.** Q3 Block 1 internal review (2026-07-06): AJ clarified
     EMEA owns all EMEA accounts, in-flight and pre-flight.
     https://app.notion.com/p/39581468615180e9b082f5e82dc150d4

  ### Why Messaging is the worse option

  MSG's 2026 Q3 Block 2 is **already stacked and dated** — ~14 projects, with Send eFolio
  (7–21 Aug), Follow-up Questions for Service Tickets (7–14 Aug), WebChat Interactive
  (→14 Aug), Triage Workup (21–28 Aug), AI Monitoring/Groundcover (21 Aug–4 Sep),
  Post-Chat Analysis V2 (28 Aug–4 Sep), OAuth (→28 Aug). Taking Hotelkit means displacing a
  committed project or sliding to Block 3 — which is precisely the "where does it sit in
  their planning block" problem, and it lands *later* than EMEA could deliver. MSG also has
  no DACH context, no German, no GDPR/subprocessor muscle, and no Hotelkit/Bendix/Jerome
  relationship.

  ### The honest counter-argument (the thing to actually negotiate)

  EMEA has **0% strategic roadmap capacity**. Capacity Plan EMEA 2026 (2026-07-30): 3 engineers
  including the eng lead; ~80% strategic accounts + activation support, ~20% platform. The
  4th-engineer ask is still pending. https://app.notion.com/p/3958146861518096b54af101aef8ab01

  EMEA's Q3 Block 2 board has exactly one other dated project — "Push attachment to
  reservation in OHIP" (Marta, 6–31 Aug). So the one person who has built a ticketing vendor
  before is booked for the first four weeks of the block.

  **So: say yes, with conditions. Do not accept it as additive.**
  - Name the trade explicitly: either the 4th engineer lands, or one EMEA Block-2 commitment
    defers. A pod at 0% roadmap capacity accepting new work is how a date silently slips and
    Sales gets a miss.
  - Ask Messaging for the *cheap* help, not the project: Kelly Waters / Jake Wilhelm as
    reviewers on the Gate-4 design doc, and MSG owning anything touching Ticket Gateway core.
  - Cheapest shape: Marta owns design + certification + de_DE request-type authoring;
    the EMEA-425→429 build (~15 pts) runs through the `ticketing-integration-builder` skill
    with whoever has hands.

  ### Before committing a date to Bendix

  1. **HK-23 — certification lead time from Hotelkit.** Vendor-controlled, unknown, and it
     sits directly against the 90-day ask. Get this number first; it sizes everything.
  2. **HK-12 / HK-8** — sandbox auth + which status transitions actually fire the webhook.
     EMEA-424 is timeboxed to 1–2 days; run it before the clock starts.
  3. Assign a lead and set milestone dates *as part of* prioritisation, not after.
  4. **HK-22 pilot conflict** — Linear says Bayerischer Hof, the business case recommends
     CERVO Zermatt (already onboarding, asked for this use case). Resolve before rollout.

  ### Money at stake
  ~$35K ARR Bayerischer Hof (blocked on a *timeline*, not a delivery) + ~$30K at-risk DACH
  (Schloss Elmau, CERVO Zermatt, Mercure Wiesbaden City, Mercure Bad Oeynhausen). Hotel Sacher
  Wien (~$12K) already closed-lost on this. Dialogshift, Straiv, Quicktext, HiJiffy and
  SuitePad all integrate with Hotelkit and use the gap in DACH RFPs.

  ### Not checked
  Did not ask Jake Wilhelm / Kelly Waters / James Saram whether a Messaging hand-off has
  already been discussed anywhere — no Slack search was run, and nothing was posted anywhere.
  Bear notes have nothing on this decision (no "Messaging pod" mention at all).
project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 5
title: Decide my opinion on whether HotelKey integration should be executed by EMEA
  team
updated: 2026-08-06 13:00:01.667362
waiting_on: null
waiting_since: null
working_on: false
---

First, look for PRDs or eng designs for hte integration with this 3rd party ticketing 

Messaging pod would take this otherwise. The problem is where it would sit in their planning block.