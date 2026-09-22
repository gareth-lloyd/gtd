---
area: null
completed_at: null
contexts:
- consume
created: 2026-09-21 00:00:00
defer_until: null
due: null
energy: low
id: 2026-09-21T0000-review-friday-s-show-tell-recording
order: null
output: |
  ## Agent run 2026-09-21T15:25:04Z

  Source: Zoom recording GMT20260918-145930 (Fri 2026-09-18, ~64 min) in ~/Downloads. Read the full
  transcript (.transcript.vtt) and chat log end to end. The video was still downloading
  (.crdownload) so slides and screen shares were NOT viewed; everything below is from audio + chat.
  Host: Andy Monroe (Blake out). First ~10 min is social chat; demos start at 11:30.

  ### TL;DR
  - 3 demos ran (events architecture, upsells inventory, Dallas Lab rail service). Andy had 4-5
    queued; Jason Flax's and at least one other were bumped when SJ took the last 24 min for an
    unscheduled company update.
  - SJ's update is the part worth your time (40:16-1:04:00). Headlines: Q2 board meeting went
    well, IHG deal signed and called out twice as a big driver, "widen our aperture" beyond
    guest-facing into hotel-operations agents, M&A is on the table, and he named PMS gateway as
    "another big worry of mine".

  ### 1. Tommy Slater - Physical Access events / event-driven architecture (11:35-23:35)
  - Pitch: Canary is moving from monolith to service-oriented; direct service-to-service calls
    don't scale, so move toward an event bus with pub/sub fan-out. Motivating case: guest checks
    in but their mobile key doesn't reflect it because the update takes many hops to reach
    Credential Manager.
  - Status: in progress, not in production. Showed current state plus target.
  - Asks: point your model at the doc for context; think in events rather than API calls; consider
    EDA in your next design doc; talk to him if you want to help design the broader architecture.
  - Q&A: Yasmin Lucero wants one central place for event/state-transition design philosophy and
    floated an "event schema czar". Tommy admits event structures have already drifted and wants
    interested pods to align on a shared contract shape, then extend per use case. Jordan Sterling
    pointed to the Kafka schemas in the repo schema registry as the starting point. Andy suggested a
    shared library. On Kafka onboarding: tooling is good now, but there is still a fair amount of
    code and decisions. Rule of thumb for Rafael Nunes: fan-out inside the Canary VPC -> Kafka;
    other cases may be SQS.
  - Docs (found via Notion search, not linked in the call; "PA Events - Vision" was edited the day
    of the demo so is most likely what he showed):
    - PA Events - Vision: https://app.notion.com/p/3d081468615181c892fdeaef110196f4
    - PA Events for Credential Manager: https://app.notion.com/p/3c3814686151801fb104d147863af5e2
    - Related: PA-476 "Move canary->CM reservation push to Kafka":
      https://linear.app/canary-technologies/issue/ba1e9f28-ceb6-41f8-a8e8-845ff353deea

  ### 2. Facundo Marco del Pont - Upsells inventory (23:40-32:16)
  - Inventory now exists for add-ons, early check-in and late check-out. NOT for room upgrades or
    reservation extensions.
  - Per-item inventory card under Availability: toggle on/off, count, and usage duration
    ("whole stay" e.g. breakfast/crib vs "one time" e.g. bottle of wine).
  - Deliberately not e-commerce style: guests are never blocked and nothing is reserved at request
    time (no websockets; count is whatever loaded with the page). Two guests can both request the
    last item and the front desk picks who to approve.
  - Guest side: "Only a few left" tag at 3 or fewer, and requestable quantity is capped at what's
    left. At zero the item disappears from the guest flow.
  - Staff side: warning modal when an approval uses the last of the inventory, and another when it
    would go over the limit (approval is still allowed, since hotels often set the count below real
    stock).
  - Limits called out in Q&A: no partial approval (can't approve 1 of 2 requested); no one-off
    "bump for today", you edit the inventory number itself; an inventory sell-out can't be cleared
    with the normal "make available" action; no calendar view of per-date limits for staff (Nicolas
    Garnier). Plan is to watch hotel usage and iterate.

  ### 3. Eugenio Portella (QA) - Dallas Lab rail service (32:20-40:10)
  - OpenKey's Dallas lab has 15 rails with real phones and real locks from every major lock vendor
    plus Canary's own modules. Previously only one team could drive it.
  - New small HTTP service in front of the lab: discover rails, lease one (queues if none free),
    move it, release it. 4 plain HTTP calls, ~20 lines, any language, no MQTT or lock-protocol
    knowledge. Also serves simulators from the lab's Mac Minis when you don't need hardware.
  - Proven with a real end-to-end test run from CI on the Dallas runner. He drove a phone to a lock
    from Brazil.
  - Honest status: Phase 1 done. No repo runs scheduled nightly jobs on it yet (first one being
    wired); first adopters will hit rough edges. Self-serve guide, no gatekeeper.
  - Extras: David Dietz noted you can remote-debug a physical phone with breakpoints via the lab
    laptop. Jordan Sterling said webcams have been bought so runs can be watched live; Andy wants a
    follow-up demo once wired.
  - Guide: https://app.notion.com/p/canarytechnologies/How-to-use-the-Dallas-Lab-rail-farm-for-hardware-tests-3d681468615181da9069f3f0338e0bd9
  - His #eng-announce post: https://canarytechnologies.slack.com/archives/C03P563GB4M/p1789749984577359
  - PRD: https://app.notion.com/p/38881468615180ea97dbc7e18117d531
  - Code lives in lab/rail-service/ (has its own CLAUDE.md).

  ### 4. SJ Sawhney - unscheduled company update (40:16-1:04:00)
  - Q2 board meeting (held late) went very well. IHG signing was "very helpful", and momentum in
    US and international hotels is strong beyond that one deal.
  - TAM thesis: AI expands the addressable market from what hotels spend on software to software
    plus addressable labor; hotels spend ~10x more on labor than software. Explicit realism:
    not replacing housekeepers, and probably not the front desk agent who hands out keys.
  - Why small 2-3 person entrants are appearing (agentic sales & catering, communication agents).
    His three requirements to win in hospitality: product that works, a go-to-market team that
    knows how to sell to hotels ("not build it and they will come"), and human time spent helping
    hotels adopt. Hotel users do not self-adopt tools; "my hotel user is quite different than me".
    Claims no one is close to Canary's position: AI messaging is the biggest AI product, AI voice
    the fastest growing, Agentic Sales Coordinator has strong PMF.
  - Main reflection: success with the guest management system has narrowed the aperture to
    guest-facing agents (messaging, voice, kiosk with computer-use agents). Hotel-operations
    opportunities he listed: finance agent (PMS reporting, reconciling OTA reservations and
    payments), shift/labor scheduling from forecast demand, agentic marketer for past-guest
    remarketing (a $5-10k tool vs a $100k hire), plus "5 or 6" others.
  - M&A: "not a bad idea", no need to go 0 to 1 on everything; strong balance sheet and excited
    investors. To Jordan: would not acquire for product surface alone, target needs traction, happy
    live customers and a good team. Build cost has collapsed but the time to iterate to
    product-market fit has not. Sales & catering is a domain outside Canary's DNA where buying
    expertise could make sense.
  - Who owns exploring new bets (Arihant Daga): no dedicated PM, it should be SJ, so the unlock is
    freeing his time. PMs stay 80-90% on committed execution. Gaps he named: he is over-invested in
    GMS since Bri left (helping Vibhor and Mehul; hiring a guest-journey replacement); comms is
    covered by Jonathan Kennell and Kevin; and "the PMS gateway is another big worry of mine", with
    Ian, Mal and Connor "filling the hole" and "we're kind of just navigating that".
  - Who to build for (Yasmin): NOT the staff user. Build for the owner and GM. Front desk agents
    don't want the kiosk to succeed (Albert sees it on installs); hotel salespeople aren't logging
    in to approve AI drafts in Agentic Sales Coordinator (Rachel Kim seeing this firsthand).
  - Green-light criteria (Dana Levine): evidence of traction somewhere, market big enough,
    sequencing right for Canary.
  - Market pull (Bruno Cruz): pull is around the laundry list of tasks the GM absorbs; the layers
    of hotel management roles (AGM, front desk manager, front office manager) are the addressable
    part.
  - Framed as context going into block planning. "Slack me, I love hard questions, DMs are open."

  ### Relevant to you
  - PMS gateway was named by the CEO, in front of all of eng, as a big worry with a leadership gap
    being covered by Ian, Mal and Connor. Worth knowing before block planning given how much of your
    enterprise work (OHIP posting, BW membership push, HotelKey pilot) runs through it.
  - IHG is carrying a lot of narrative weight with the board. That raises the stakes on ENT-6032
    (IHG HotelKey + FreedomPay Pilot Wave 1).
  - Tommy's events push touches your area: Rachel Kim's Booking Confirmation GJ message that shipped
    the same day is only available on event-driven PMSes (Mews, Cloudbeds, OHIP, Sabre, HotelKey),
    not polling ones: https://canarytechnologies.slack.com/archives/C024LKAN727/p1789738763423289
    If you have views on event contracts for PMS/reservation events, Tommy is explicitly asking for
    collaborators.
  - Upsells inventory limits (no partial approval, no per-date view, no room upgrades) are likely
    to come back as enterprise tickets once brands turn it on.

  ### Possible follow-ups (your call, nothing actioned)
  - Skim "PA Events - Vision" and decide whether to engage Tommy on a shared event contract.
  - Take SJ up on the open DMs if you want to raise the PMS gateway ownership question.
  - No action items were assigned to you in the call; you did not speak and were not mentioned.

  ### Not covered
  - Video/slides not reviewed (download incomplete at run time). Tommy's Claude-generated flow
    animation and Eugenio's lab footage are the two things worth actually watching.
  - Jason Flax's bumped demo topic is not stated anywhere in the transcript or chat.
project: null
source_id: null
tags: []
time_minutes: 30
title: Review Friday's show & tell recording
updated: 2026-09-21 18:25:04.054448
waiting_on: null
waiting_since: null
working_on: false
---

review this week's Friday Demos / Show & Tell recording.

files in downloads