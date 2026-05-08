---
area: null
contexts:
- consume
created: 2026-05-08 12:13:54.976146
defer_until: null
due: null
energy: medium
id: 2026-05-08T1213-read-feedback-on-continuous-upskilling-on-agentic
order: null
output: '## Agent run 2026-05-08T14:05Z


  Read the full memo and all 22 inline discussions. Feedback drafted below for Gareth
  — NOT posted to Notion or Slack. Decide what (if any) to convert into comments.


  ### Doc summary

  Tyler''s memo (~5 pages) makes the case that Cadiz reignited momentum on agentic
  dev and we cannot afford to lose it again. Argues no single intervention closes
  the gap (Amdahl''s-law framing) — needs continuous, multi-pronged push. Audiences:
  4 quadrants on belief × skill, with the axiom "belief follows skill." Proposes:
  tiered plugin architecture (root/pod/project, EE owns root); smaller invite-only
  Frontier Guild; new retro-template section for agentic dev; parallel-work plugin
  (project planning + day planning); design-doc template changes; onboarding lane;
  resurrected per-pod AI Office Hours; capture-and-diffusion mechanisms (changelog,
  Show & Tell, eng-announce, frontier guild as diffusion vector); measurement (Claude
  usage, plugin usage, feedback forms).


  ### Existing comments worth tracking (avoid duplicating)

  - Brian: code-review automation is foundational — EPD changes won''t help until
  that''s solved. Believes Projects fundamentally end up single-player → questions
  the whole "scoping parallel work" investment. OK with invite-only Frontier Guild.
  Says deprioritize onboarding lane (we''re not hiring much).

  - Sam: definition of "skill" with agentic tooling is unclear; tokens-as-metric will
  incentivize wrong behavior ("slop cannons"); proposed PR hook that flags missed
  plugin opportunities; thinks day-planning for parallel work is the biggest personal
  unlock.

  - Mike: how do we surface retro trends org-wide? (Tyler''s "Notion MCP skill emailing
  us reports" reply is glib — that''s a project, not an answer.)

  - Several: yes to design-doc template changes; yes to Office Hours; mention that
  pods don''t map 1:1 to code (Tyler''s "lean on permissive" reply dodges).


  ### My feedback for Tyler


  **1. Sequence and cost the proposals.** This reads as "do all 8 things." We won''t.
  Without a sequencing recommendation we''ll do 4 of them badly. Concrete ask: which
  2–3 land first if Q2 only fits that much? My take — capture/diffusion + a single
  outcome metric ship first because they''re the substrate everything else depends
  on; retro template + design-doc template are nearly free and should ship the same
  week; Frontier Guild is third; parallel-work plugin and onboarding lane sit behind
  those.


  **2. Reviewer skill is missing as a distinct audience.** The four quadrants treat
  every engineer as an author. With agent-authored volume rising, the bottleneck and
  the quality risk shift to review. Reviewer-side skill (spotting agent failure modes,
  validating test coverage, smell-detecting cargo-cult patterns) is a different muscle
  from authoring. Brian''s call-out on code-review automation is the tooling half
  of this; the human half is upskilling reviewers on what to look for. Worth calling
  out as its own lane.


  **3. Plugin governance has a hole.** "EE strict about graduation" is asserted but
  unspecified. Need: graduation criteria (e.g. >N pods using, stable for X weeks,
  passes audit), cross-pod ownership rules when teams don''t map to code (Sam''s question,
  Tyler''s "lean on permissive" doesn''t answer it), and — most missing — a sunset/pruning
  story. Skills will rot fast as models and harnesses change. Without active pruning
  we relive last year''s entropy with a more complicated taxonomy.


  **4. "Belief follows skill" is too clean.** Treating high-skill skeptics as people
  who "need to be pushed to leverage their skepticism" reads like managing around
  them. Their skepticism is calibration data the rest of us need. Concrete: invite
  at least one high-skill skeptic into the Frontier Guild charter explicitly. They''re
  a feedback-loop input, not a conversion target.


  **5. Outcome metrics, not just input metrics.** Every proposed metric is an input
  (Claude usage, plugin usage, feedback forms). Sam''s pushback on tokens generalizes
  — inputs get gamed or misread. Need at least one outcome anchor: PR cycle time,
  post-merge defect rate, or design-doc → merged-PR latency. Otherwise we tune input
  dials without knowing whether we moved the thing that matters.


  **6. Split the parallel-work plugin.** Brian''s "projects are single-player" critique
  and Sam''s "day-planning is the unlock" land in the same place: day-planning is
  universal, project-decomposition for parallel humans is a contested bet. Ship day-planning
  first as a standalone skill. Validate the project-decomp half against KBv2-shaped
  projects before investing further.


  **7. Frontier Guild — what changed?** Previous Acceleration Guild decayed: biweekly
  → monthly → dead. New version is "smaller, focused" but doesn''t articulate the
  structural change that keeps it alive this time. Make charter elements (sunset criteria,
  named accountability, monthly EPD report, pod-rep diffusion duties) hard requirements
  with explicit owners, not "should-haves." Otherwise this is a re-badging.


  **8. Retro trends need a real plan.** Mike''s question is the right one. "A skill
  on Notion MCP that emails us" is hand-wavy. Without an actual rollup mechanism (named
  owner, format, cadence, audience), retro action items become local journaling and
  the feedback loop never closes. This bridges problem 3 (forcing functions) and problem
  2 (diffusion) — deserves more than half a sentence.


  ### Smaller / nits

  - "We left Cadiz with the most aligned, agentic-fluent team we''ve ever had" — rhetoric.
  Worth grounding with one data point ("retros showed X% of pods now using Y") before
  the proposals, or this sounds like vibes.

  - "Vibe code the transformation" is a useful phrase. Keep.

  - The manager paragraph (diversity of opinion, grounded in skill) is the most undeveloped
  section. If a unified manager front matters, it''s a real workstream — coaching,
  hands-on sessions, expected demos at leads syncs — not a paragraph.


  ### Recommendation for me (Gareth)

  Pick 3–4 of the points above to surface in eng-leads thread or as Notion comments.
  Strongest: (1) sequencing/cost, (2) reviewer audience, (5) outcome metrics, (7)
  Frontier Guild charter rigor. Plus a concrete +1 to Sam on tokens and Brian on code-review
  automation since those are the load-bearing critiques already on the page.


  Did NOT post anything to Notion or Slack. Awaiting decision on whether to convert
  any of this into comments.

  '
project: null
source_id: https://canarytechnologies.slack.com/archives/C02MVAEJD0Q/p1778173477964119
tags:
- morning-gtd
- slack
- from-awareness
time_minutes: 15
title: 'Read & feedback on: Continuous Upskilling on Agentic Development doc'
updated: 2026-05-08 14:08:59.819361
waiting_on: null
waiting_since: null
working_on: false
---

Tyler @channel in #eng-leads asked all eng leads to read and provide feedback. https://www.notion.so/canarytechnologies/Continuous-Upskilling-on-Agentic-Development-34d81468615180f0b7f3fad751b61445 (Slack: https://canarytechnologies.slack.com/archives/C02MVAEJD0Q/p1778173477964119)