---
area: null
completed_at: 2026-08-10 19:00:27.125364
contexts: []
created: 2026-08-05 14:02:52.083195
defer_until: null
due: 2026-08-06
energy: low
id: 2026-08-05T1402-yes-no-decision-on-hotelkey
order: 4
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

  ## Agent run 2026-08-06T15:48

  Two additions: (a) Hotelkit scored explicitly against the EMEA Product Prioritisation
  Framework, (b) the four region-specific justifications expanded with *why each one costs
  you if it moves out of region*. Opinion is unchanged: **yes, EMEA, but not additively.**

  ---

  ### Scored against the EMEA Product Prioritisation Framework

  Framework: https://app.notion.com/p/384814686151809ea6c1c4514a93aea4
  Weighting: Strategic Accounts 40% / Non-strategic (activation lag) 20% /
  Foundational-Country-specific 20% / Sales cycle alignment 20%.

  **1. Strategic Accounts — 40% — partial, and don't overclaim it.**
  The bucket's first core question ("does winning this account unlock the region, or is it a
  standalone win?") doesn't apply — Hotelkit is an integration, not an account, and I could
  not find Bayerischer Hof, CERVO Zermatt or Schloss Elmau on any designated
  strategic-accounts list. The *second* core question is the one it answers dead-on:
  "which countries are viable today, which have product or integration gaps that need
  resolving." Hotelkit **is** the DACH integration gap — 4,000+ hotels, 180,000+ daily
  users, every guest-facing competitor already integrated. The framework's compounding
  clause ("each account making the next one easier") is the honest claim here, not the
  40% weighting itself.

  **2. Non-strategic accounts / activation lag — 20% — direct hit.**
  Framework's own ARR metric is "turn contracted into paying customer" plus "% of successful
  pilots in EMEA". 5+ live DACH accounts were onboarded expecting this; CERVO Zermatt is
  mid-onboarding and specifically asked for the use case. That is activation lag by
  definition. (Bayerischer Hof is the *CARR* side — not yet signed, blocked on a date.)

  **3. Foundational / Country-specific — 20% — hit, and it contains the framework's own
  answer to the EMEA-vs-Messaging question.** Two lines, verbatim:
  - *"Collaborate and share requirements with the product vertical who are best placed to
    build it. If timelines are tight or teams have competing priorities, the EMEA pod can
    help unblock and accelerate this foundational work (working closely with that vertical)."*
  - *"Own the localisation layer, country-specific configuration, compliance defaults, and
    regional templates are the EMEA pod's to build and maintain."*

  Read together those license exactly the split recommended last run: Ticket Gateway core
  stays Messaging's (Kelly Waters is the owner and a named reviewer in the PRD); the adapter,
  the de_DE request-type catalog and the DACH compliance defaults are the localisation layer,
  which is EMEA's by the framework's own words. And MSG's stacked Block 2 *is* the
  "competing priorities" condition under which the framework says EMEA accelerates.

  **4. Sales cycle alignment — 20% — hit, but we are reacting, not ahead.**
  Core question is "are we ahead of this sales cycle, or are we reacting to it?" Honest
  answer: reacting. Hotel Sacher Wien (~$12K) already closed-lost; Bayerischer Hof waiting
  on a date; Dialogshift/Straiv/Quicktext/HiJiffy/SuitePad using the gap in RFPs. The
  sub-questions both resolve yes — blocking multiple deals across the region (5+), and the
  window to ship ahead of it has **closed**. That reframes the decision from "is this worth
  doing" to "who ships it soonest", which is the EMEA argument. The framework's own example
  list for this bucket includes "Staff messaging/ticketing app".

  **Net:** clean hits on 3 of 4 buckets (60% of the weighting) plus the country-viability
  clause of the fourth. It also touches three of the five named strategic bets —
  **Service ticketing** (primary), **GDPR and PII handling** (blocking work), **Voice AI**
  (inherited via EMEA-430). Nothing else currently in EMEA's Block 2 queue lands on that many.

  **Caveat worth carrying into the room:** the framework page's own Next Steps are all still
  unchecked — align with Bree, James↔Manuel on sales strategy, James↔Dianna Kertz on which
  strategic accounts she joins. So "the framework says so" is a strong *reasoning* argument
  but not yet a ratified one.

  ---

  ### The region-specific justifications, expanded

  The test for each: *what does it cost if this moves out of region?*

  **1. German is an API field, not a translation task.**
  Hotelkit inverts the metadata pattern — `PUT /setup/requests` has Canary **push** the
  request-type catalog with `de_DE` labels. Every other vendor exposes a catalog we sync.
  Consequence: the request-type list *is* the AI's retrieval index, and its quality becomes
  a function of what we author rather than what we filter.
  Why that matters concretely: EMEA-367 (IC Berlin, closed 6 Jul, Martijn Dekker) was exactly
  this failure mode — voice couldn't map bathrobe / shaving set to the vendor catalog, and it
  took three PRs to fix (widen search, add synonym support, multi-item search).
  https://linear.app/canary-technologies/issue/EMEA-367
  That was over a vendor-supplied 1,311-item HotSOS catalog. Here the failure moves *upstream
  to us*: guests say Bademantel, Rasierset, Zimmerreinigung, and the labels also have to match
  the vocabulary DACH hoteliers already use inside Hotelkit. Machine-translated labels fail
  silently — not in tests, but in call transcripts a month into pilot, as "AI didn't
  understand me". HK-24 ("who authors the de_DE labels?") currently has no owner and is marked
  non-blocking, which understates it. This is a German-speaking-hotel-context task, not an
  engineering task; Messaging cannot staff it and would hand it back to EMEA anyway.

  **2. Certification is a vendor relationship, not a checkbox.**
  EMEA-431 — Hotelkit mandates a joint testing session before pilot approval, via
  api-support@hotelkit.net. No prior Canary integration had a vendor-controlled gate. Lead
  time is unknown (HK-23) and sits directly against the 90-day ask, so it is the single
  largest schedule unknown in the project. Hotelkit is Salzburg-based: overlapping working
  hours and language turn a two-week async round-trip into a two-day one, and the same
  channel carries HK-19 (partner agreement / integrations-directory listing). Certification
  gates are also where a vendor decides whether you're a partner or a support ticket —
  that's worth having a regional owner on the call.

  **3. GDPR is a launch blocker with calendar time attached, not a checklist.**
  Four items block pilot go-live: HK-13 hosting region + adding Hotelkit to Canary's
  subprocessor list, HK-14 whether a processor-to-processor DPA is needed, HK-15 retention
  and the erasure path for data already pushed to Hotelkit. DACH is the strictest-scrutiny
  market in EMEA — German enterprise properties routinely ask for the subprocessor list
  *before* agreeing to a pilot, so this is procurement-facing, not internal hygiene. It is
  also Legal's calendar, not engineering's: start it at kickoff or the code lands and the
  pilot waits. Two reasons it belongs in region: "GDPR and PII handling" is one of the five
  named EMEA bets and "compliance defaults" is explicitly EMEA-owned in the framework; and
  the institutional memory is local — EMEA-388 (HotSOS tasks carrying the full communication
  thread instead of a concise summary) was found by this pod, in this region, and is now
  P0 acceptance criterion #5. Whoever builds it needs to already know that story.

  **4. Pilot execution is a DACH relationship chain, and it is the actual deliverable.**
  Jerome (CS) owns pilot coordination, the request-type vocabulary and the real list of
  waiting accounts; Bendix Urlbauer (Sales) owns the timeline commitment to Bayerischer Hof;
  the pilot property itself is still contested (HK-22 — Linear says Bayerischer Hof, the
  business case says CERVO Zermatt, which is mid-onboarding and asked for this). The
  framework's Strategic Accounts section says to "plan high-touch engagement ahead of launch
  knowing that every new market will surface requirements we didn't anticipate" — that
  high-touch loop runs in German, on CET, through people EMEA already speaks to weekly. A
  remote pod inherits the code and subcontracts the loop back to EMEA regardless: you pay
  the coordination tax without saving the engineering.

  **5. Even the free part is regional.** Voice comes at zero marginal cost through EMEA-430 —
  but only because IC Berlin (a Berlin property, EMEA-led) shipped voice service tickets in
  July and left 60+ reusable `ICB-*` cases. Re-pointing that suite with German request types,
  instead of EMEA-433's build-a-QA-suite-from-scratch, is a saving the authoring team banks
  cheaply and anyone else re-learns.

  ---

  ### What this does *not* change

  Framework fit argues **EMEA over Messaging**. It does not argue **additive** — the
  framework ranks what to build, not how much a 3-person pod can hold. The capacity
  counter-argument from the previous run stands unaltered: 0% strategic roadmap capacity,
  4th engineer still pending, Marta booked 6–31 Aug on the OHIP attachment project. Name the
  trade or the date slips quietly.

  ### One question the framework surfaces for James / Bree

  If Hotelkit is being justified partly on the 40% Strategic Accounts weighting, someone
  should confirm whether any DACH property actually carries that designation — I couldn't
  find one. If it doesn't, Hotelkit is a 20+20 (+ country-viability) item, which changes how
  it ranks against EMEA's other Block-2 candidates and makes the "which commitment defers"
  conversation sharper rather than softer.

  ### Still not checked
  No Slack search on whether an MSG hand-off has been floated. No approach made to James,
  Kelly, Jake, Jerome or Bendix. Nothing posted anywhere — this remains a private opinion.
project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 5
title: Decide my opinion on whether HotelKey integration should be executed by EMEA
  team
updated: 2026-08-10 19:00:27.125354
waiting_on: null
waiting_since: null
working_on: false
---

Next agent task:
* Expand on the region-specific justifications for EMEA. Concise, but add context justifying their importance. 
* Measure against https://app.notion.com/p/canarytechnologies/EMEA-Product-Prioritisation-Framework-384814686151809ea6c1c4514a93aea4?source=copy_link