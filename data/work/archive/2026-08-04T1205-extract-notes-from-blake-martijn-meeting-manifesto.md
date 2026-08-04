---
area: null
completed_at: 2026-08-04 14:49:14.979102
contexts: []
created: 2026-08-04 12:05:15.497936
defer_until: null
due: null
energy: low
id: 2026-08-04T1205-extract-notes-from-blake-martijn-meeting-manifesto
order: null
output: |
  ## Agent run 2026-08-04T14:07 EEST

  Searched Bear, Granola, and Google Calendar. **There is no captured record of a
  Blake/Martijn meeting on Friday 31 July** — your calendar that day shows only
  Show & Tell, Canary Huddle, and an OOO block; Granola has no capture between
  30 Jul and 3 Aug; and the word "manifesto" appears in none of your ~1500 Bear
  notes. Most likely the Friday-31st conversation was Blake↔Martijn without you,
  relayed to you in this morning's 1:1.

  The manifesto content WAS captured — in today's Granola note "Martijn Dekker"
  (Tue 4 Aug 2026, 11:46, meeting id 6960cb03-cb16-4b48-b886-6edde2d5013c).
  Extracted notes:

  ### Why Blake wants a manifesto
  - SJ and Blake are not aligned on what the EMEA team should own.
  - Live example: hotel kits (CRS integration). SJ approved it for EMEA; Blake
    says it belongs with the messaging/core integrations team.
  - James/Jerome counter: "you can't sell without the integration"
    (chicken-and-egg). You side with Blake — core integrations should do proper
    market analysis, not EMEA.

  ### What the manifesto must cover (Blake's ask)
  1. Purpose — what the EMEA team exists to do
  2. North Star metrics — how success is measured
  3. An "elevator pitch" — a framing usable for prioritization decisions

  ### Status / decisions
  - Nothing final agreed; the explicit goal is to start the conversation,
    not produce a finished document.

  ### Action item (yours, time-sensitive)
  - Draft the team manifesto + North Star metrics BEFORE the capacity review
    meeting with Blake this Friday, 7 August.

  Suggested follow-up: this inbox item could become a next action "draft EMEA
  manifesto + North Star metrics" due Thu 6 Aug. If notes from the actual
  Friday-31st Blake/Martijn conversation exist, they'd be in Martijn's or
  Blake's own notes — worth asking one of them directly.

  ## Agent run 2026-08-04T14:12 EEST

  Correction from Gareth: the meeting is the Granola note "EMEA resource sync"
  from THURSDAY 30 July 2026, 16:06 (meeting id
  4e068a17-80df-40fd-a238-12e9eefb9a8a), not Friday 31st. Extracted notes —
  this is effectively the raw material for the manifesto:

  ### EMEA pod strategic positioning (the "purpose" ingredients)
  - Two core structural advantages: (1) time-zone overlap with customers,
    (2) no long-term product ownership burden.
  - A third surfaced in the meeting: engineers close to activation produce
    high-quality product feedback.
  - Operating principle: every workstream should maximize at least one of the
    two primary advantages (time-zone-critical, or tight to a specific
    customer). Work that uses neither should be pushed elsewhere.

  ### Good fits vs caution areas (the "elevator pitch" for prioritization)
  - Good fits: Crown Resorts (time-sensitive), GDPR ownership, voice language
    improvements, customer-specific integrations. GDPR fits because EMEA is
    closest to customer needs and activation complexity; coordination overhead
    is currently minimal (~2 hrs/week) and the team is well-aligned.
  - Caution areas: localized replacement (cited as straying too far — should
    have gone to a platform team), ticketing gateway, kiosk edge work (kiosk
    projects heading EMEA's way; skepticism warranted).
  - Named risk: EMEA becomes the easiest pod to absorb work other teams should
    prioritize harder. The pod must maintain back pressure so the business
    makes sound prioritization decisions. Analogy used: engineers taking every
    ticket without a PM removes the PM's ability to say no.
  - GDPR progress is blocked by reactive workload; wish that Martha or Monta
    could focus on it fully. Q4 expectation: reactive load significantly
    reduced, GDPR in much better state.

  ### Headcount
  - No headcount in Q3; Q4 more likely, Q1 possible. Conversations ongoing
    about hiring pace, including whether to bring in an enterprise IC for
    GDPR focus work.

  ### Action items from that meeting
  - (Gareth) Document the EMEA prioritization framework: work the pod is
    maximally leveraged at vs work to be skeptical of. Precedent: this
    framework was "a game changer" for the data team (Dana and Vort).
  - Schedule follow-up discussion for next week (hiring, prioritization,
    enterprise IC for GDPR) — this became the Friday 7 Aug capacity review
    with Blake.

  ### How this connects to the manifesto ask (from the Aug 4 Martijn 1:1)
  Blake's three-part ask (purpose, North Star metrics, elevator pitch) maps
  directly onto this meeting's content: positioning → purpose; good-fits vs
  caution-areas → elevator pitch. The gap to fill when drafting: North Star
  metrics — nothing in either meeting proposes concrete metrics yet.

  ## Agent run 2026-08-04T14:20 EEST — distilled framework for future discussion

  ### EMEA Pod Framework (draft — discussion scaffold, not a finished manifesto)

  **1. Purpose**
  The EMEA pod exists to exploit two structural advantages no other pod has:
  - Time-zone overlap with EMEA customers.
  - Freedom from long-term product ownership, enabling fast, customer-tight
    delivery.
  Secondary advantage that follows: proximity to activation generates
  high-quality product feedback for the owning teams.

  **2. The leverage test (the filter for all incoming work)**
  Blake's own framing from the meeting: "time zone and customer are the two
  closenesses that you have." Take a workstream only if it exploits one of
  the two closenesses:
  - Closeness in time: genuinely time-zone-critical — needs same-day
    iteration with an EMEA customer, OR
  - Closeness to a customer: per Blake's Kempinski hypothetical, take the
    work when "the tightness with that specific customer is the optimization
    path, not the feature set itself."
  Work that exploits neither closeness belongs to a platform/product team,
  even if EMEA could technically do it.

  **3. Applying the test today**
  - Passes: Crown Resorts (time-sensitive), GDPR ownership (closest to
    customer needs and activation complexity; ~2 hrs/week coordination),
    voice language improvements, customer-specific integrations.
  - Fails or suspect: localized replacement (should have been platform),
    ticketing gateway, kiosk edge work, hotel kits/CRS integration (Blake:
    belongs with core integrations, who should do proper market analysis;
    counter-argument from James/Jerome: can't sell without the integration).

  **4. Operating principle: back pressure**
  EMEA must not be the path of least resistance for work other teams should
  prioritize harder. Saying no is a service to the business: it forces sound
  prioritization decisions. (Analogy from the meeting: engineers taking every
  ticket without a PM removes the PM's ability to say no. Precedent: the data
  team's equivalent framework was "a game changer".)

  **5. Open questions for the Friday 7 Aug discussion with Blake**
  - North Star metrics: nothing proposed yet in either meeting. Candidate
    directions implied by the purpose: activation velocity/time-to-live for
    EMEA customers, EMEA customer retention/expansion, GDPR compliance
    milestones. Needs deliberate choice.
  - Hotel kits ownership: resolve the SJ/Blake disagreement using the
    leverage test rather than case-by-case argument.
  - Reactive load: GDPR is blocked by it; Q4 target is reactive load down,
    GDPR healthy. Does the framework need an explicit reactive-work budget?
  - Headcount: no Q3 headcount; Q4 likely, Q1 possible. Whether to bring in
    an enterprise IC for GDPR focus depends on the priorities above.
project: null
source_id: null
tags: []
time_minutes: 5
title: extract notes from blake/martijn meeting Friday 31st - manifesto for EMEA team
updated: 2026-08-04 14:49:14.979092
waiting_on: null
waiting_since: null
working_on: false
---