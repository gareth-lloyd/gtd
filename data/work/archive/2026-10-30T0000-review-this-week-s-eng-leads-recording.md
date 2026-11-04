---
area: null
completed_at: 2026-11-03 09:15:41.226213
contexts:
- consume
created: 2026-10-30 00:00:00
defer_until: null
due: null
energy: low
id: 2026-10-30T0000-review-this-week-s-eng-leads-recording
order: null
output: |
  ## Agent run 2026-11-03T09:30:00+00:00

  Sources: Notion note + AI transcript (https://app.notion.com/p/canarytechnologies/2026-10-29-Eng-Leads-Weekly-40c814686151802b8371d70616cedff5) and the speaker-attributed transcript at ~/Downloads/Eng Leads Weekly.txt. Attribution below is from the second file; the Notion AI summary mislabels a couple of speakers (its "Andrea" tech-debt point is Andrea Bradshaw; the "is SJ getting the right technical advice" question is Ian Clark).

  ### TL;DR

  SJ hijacked the first ~40 min to think out loud about 2027 team structure. Nothing decided. Pod realignments "could be" announced in the next couple of months (Blake, answering Dana). Platform teams (PMS Gateway, Payments) are the part under scrutiny, so Gateway-adjacent people are the most directly affected. Two norms were stated as policy: no Slack DMs for work, record every customer call. Demo time limit is 5 min. Code-review-changes retro was punted.

  ### SJ's thesis (not a plan)

  - Team cohesion around a customer outcome structurally produces product cohesion. Examples: kiosk + mobile check-in should have produced "straight to room"; late checkout sold in the departure-time dropdown lifted conversion ~180% once Upsells and Arrivals worked together (14 months after Nico first wanted it); same pattern for early check-in on reg cards and choose-your-room.
  - Consolidation candidates: arrivals + kiosk + mobile key + upsells; tipping + housekeeping + ticketing once ticketing/housekeeping launch.
  - New categories needing space: CRM/marketing (Canary owns the guest profile; Salesforce is "a truck to move a book", Revinate is legacy) and "operator" (GM/owner runs the hotel through an agent).
  - Platform teams: "no one gets fired for building a platform team." Internally they cede the benefit of being one company; the Gateway team gets requirements (OHIP, StayNTouch, Infor) without the customer outcome and wants to be in discovery earlier. He wants to keep platform teams' long-term ownership but let app teams build on their own timeline without "Tetris sequencing."
  - Framing exercise: if every job were done by agents with infinite context and perfect attention, how would you organize? Not applicable literally, but it surfaces ideas.

  ### Pushback and nuance

  - Yasmin (Payments, one year in): Payments was called a platform but didn't act like one; the wins came from building relationships with product teams. Three answers to "let tipping build FreedomPay/Apple Pay themselves": technical (refactor the product/platform contract, design doc mid-flight, she offered to send it to SJ), organizational (roadmap that ships customer value incrementally, "where we're floundering"), and tension (Stripe COGS and the gateways genuinely need a single cross-cutting owner). She also thinks the real problem is product depth, not platform teams: the "advanced fraud check" we sold needs a check-in product decision nobody on check-in has the payments depth to make, because quarter-over-quarter objective churn leaves no time to go deep.
  - Jordan Sterling: agrees teams are too small and hyper-focused; suggests only high-level block reviews, not per-team. Disagrees on platform teams: Delta, Stripe COGS, async payments never get done without one, and any tiger team grows into a full-time team. Counter-example: physical access is building directly into check-in for a court without sequencing because the work is small. Also: if the platform team signs off and reviews, anyone can build it; doc review should be faster.
  - Blake's version of "have both": platform teams own strong boundaries, harnesses and self-healing of integrations, not each integration (e.g. not the Protel rate-code work for live availability). Jordan: that matches the "strong interfaces, really good testing" message already given to all teams.
  - Andy Monroe: Luke's friend at a voice AI company gets far lower latency because they own the infra layer; our voice pod can't put latency (1200ms to 800ms, SJ guesses abandonment 30% to 15%) in its art-of-the-possible. But a dozen pods depend on the monolith, so some platform ownership is needed.
  - SJ on product org (to Andrea Bradshaw): the biggest product gap is no Gateway PM. Ian, Kush and Maul tried to cover it and "it's really hard to do both." A PM is needed on the Gateway pod as long as sequencing has to happen.
  - Ian Clark: SJ is naming a real problem that could be solved many ways; is he getting the right advice on technical ramifications? Blake: this meeting is one way Eng gets a voice.
  - Andrea Bradshaw: fast, wide-touching projects (kiosk) left tech debt that slows other teams; the contribution model needs explicit ownership. Blake agreed: if kiosk contributes to platform code and it breaks, kiosk owns it end to end; that gets baked into whatever plan emerges. Andy: without that speed there'd be no kiosk product.

  ### Stated norms / asks

  - No DMs for work conversations; public channels only. DMs reserved for HR-sensitive or personal messages. Not retroactive (Blake and SJ both said existing DMs stay private). SJ floated public-by-default email next year.
  - Every PM gets a Canary phone; all customer calls and Zooms recorded.
  - Demos capped at 5 minutes.
  - Show-and-tell is short on submissions (two in one huddle). Andy asked for more in the database and in the channel.
  - Pre-meeting: Andy asked Z Lee to get Birdline demoed at show-and-tell (next week, or the following day if the author was up for it) because not everyone understands how it works yet.
  - Blake's close: some attendees are more directly impacted than others; resist what-if spiralling; impacted people will be consulted, no big reveal.

  ### Relevance to Gareth

  - Gateway pod is the named example of a platform team with both a PM gap and a "we want in earlier" complaint. If realignment happens, expect it to touch Gateway, Payments and the arrivals/kiosk/upsells cluster first.
  - Blake described the PMS Gateway boundary as "strong but empty": strategic pass-through that can't build a PMS. Expect pressure to go deeper on what a PMS does, not just workflow slices.
  - Yasmin's design doc on refactoring the product/platform payments contract is worth asking for; it's the one concrete artifact mentioned.
  - Possible follow-ups (user's call): ask Ian how Gateway is positioning itself for the realignment; check whether the Birdline demo got scheduled; audit own DM usage against the new norm.

  No external writes made.
project: null
source_id: null
tags: []
time_minutes: 30
title: Review this week's Eng Leads recording
updated: 2026-11-03 09:32:00.000000
waiting_on: null
waiting_since: null
working_on: false
---

Watch this week's Eng Leads meeting recording (meets Thursdays; recording usually posted Thursday evening/Friday).
https://app.notion.com/p/canarytechnologies/2026-10-29-Eng-Leads-Weekly-40c814686151802b8371d70616cedff5?source=copy_link