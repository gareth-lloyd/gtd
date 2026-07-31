---
area: null
contexts:
- react
created: 2026-07-30 10:02:02.633099
defer_until: null
due: null
energy: medium
id: 2026-07-30T1002-read-and-digest-leadership-decision-above-property
order: null
output: |
  ## Agent run 2026-07-30T14:58:58

  **Thread read in full** ("Above property dashboards for Web Chat and Voice AI",
  https://mail.google.com/mail/u/0/#inbox/19fae64f4e4aef47). Aligned Jul 27 with zero
  dissent: SJ proposed, Connor defined the ownership split, Kevin Li and Jonathan
  Kennell both signed off ("clear to me, makes sense" / "Sounds good"). Connor
  forwarded to you + Andrea Jul 29.

  ### The decision

  - SJ's framing: when the customer is a portfolio, the Above Property dashboard is
    the PRIMARY home for products, not a secondary view. Enterprise retrofitting it
    for one-off customer requests is "the wrong ownership model and it will not scale."
  - Above Property becomes a horizontal/shared surface any team can build into —
    explicitly analogous to the hotel dashboard / hotel settings today.
  - Enterprise KEEPS four horizontal capabilities: (1) portfolio creation,
    (2) managing properties within a portfolio, (3) managing user access to the
    portfolio and contained pages, (4) the dashboard UI as a container (navigation).
    Everything else: product pods drive, Enterprise advisory only.
  - First movers: Messaging + Voice pod owns the Wyndham Voice AI corp-level
    dashboard and Mitsis' Web Chat portfolio experience (Kevin confirmed explicitly).
  - Jon's Voice AI above-property use cases — call-center missed-call queue with
    callbacks, live-call assist plug-in, corp performance/value/improvement
    analytics, central KB management — all land in the pod-driven bucket per Connor.
  - Connor called out interactive (edit-capable) experiences for operational teams
    (e.g. call-center agents) as exactly where Enterprise must stop being a bottleneck.
  - Kevin: portfolio/brand-level demand is growing, especially APAC & EMEA — invest more there.

  ### Roadmap implications for Enterprise

  1. Stop accepting one-off above-property feature requests; redirect to owning pods.
     Decide the fate of any in-flight retrofits (finish vs hand off).
  2. Mandate shifts to platform work: for pods to "build into" the container,
     Enterprise likely needs to invest in extension points — page registration /
     navigation extensibility, conventions, and docs. This is new roadmap work and
     it sits on Voice's Wyndham critical path (Voice is under heavy Wyndham contract
     pressure), so sequencing is urgent.
  3. Access control gets stressed: Enterprise keeps user-access-to-pages, but
     interactive pod-built pages (call-center agents editing data) will demand
     finer-grained portfolio-scoped permissions. Prior notes already flag portfolio
     role-grant UX confusion (Bear: "EOD" Dec 2024) — expect this to surface fast.
  4. Define the advisory model concretely (design-review intake, response SLA) or
     Enterprise becomes the bottleneck the decision was meant to remove.
  5. Consistent with prior strategy thinking that put Above Property at the center
     of enterprise investment (Bear: "Enterprise Strategy 2025 Summary for
     Engineering Objectives") and with the Management-area ownership of dashboard/
     SSO/permissions in the team-structure drafts (Bear: "Enterprise team structure
     and leadership thoughts").

  ### Open questions to discuss with Andrea

  - Which in-flight above-property work do we hand to pods vs finish?
  - Who owns portfolio-level analytics now (existing universal Explo portfolio
    dashboards — GMS 8155, Tipping 7271, Auths 8231)?
  - What does "container UI" ownership include exactly — nav only, or shared
    layout/page framework pods must consume? What do Messaging+Voice need from us
    first for Wyndham corp dashboard + Mitsis Web Chat, and by when?
  - Permission model roadmap: do we get ahead of edit-capable portfolio pages
    (call-center roles) or react per request?
  - How do we formalize advisory (office hours? required design review? embedded
    engineer for first pod builds)?

  No external actions taken (no replies, no Linear/Notion writes). Suggested next
  step for you: grab time with Andrea; optionally draft a short "Above Property as
  a platform" positioning doc for the pod.
project: null
source_id: https://mail.google.com/mail/u/0/#inbox/19fae64f4e4aef47
tags:
- morning-gtd
- gmail
time_minutes: 15
title: Summarize leadership decision — Above Property becomes a horizontal surface
updated: 2026-07-30 15:11:09.899994
waiting_on: null
waiting_since: null
working_on: false
---

Connor forwarded (to me + Andrea) the SJ/Kevin/Jonathan thread: Above Property dashboards become primary product surfaces owned by product pods (Wyndham Voice AI corp dashboard, Mitsis Web Chat); Enterprise keeps portfolio creation, membership, user access, and the container UI, advisory otherwise. Decide implications for team roadmap + discuss with Andrea.
https://mail.google.com/mail/u/0/#inbox/19fae64f4e4aef47