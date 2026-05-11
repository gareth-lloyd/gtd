---
area: null
contexts:
- craft
created: 2026-04-30 00:00:00
defer_until: null
due: null
energy: high
id: 2026-04-30T0000-90-day-review-for-afigueira
order: 3
output: "## Agent run 2026-05-07T08:23:27Z\n\nResearched the process and prepped notes.
  Review itself still TODO — handing back.\n\n### Subject\n- **Andrés Figueira** (afigueira@canarytechnologies.com),
  Enterprise pod, SWE.\n- **Start date**: 2026-01-26 → today is **day 101** (90-day
  mark was 2026-04-26, so slightly overdue).\n- **Lead + Manager**: Gareth. **Mentor**:
  Lautaro Mena.\n- Onboarding page: https://www.notion.so/2f08146861518056aac8e146b2df0ab5
  (the \"60-90 Days\" section is empty — fill it after the review).\n- 1-1 journal:
  https://www.notion.so/30c81468615180ca93d0d7c870928698 (sparse — only 2026-02-19
  and 2026-04-01 entries).\n\n### Process status\nThere is **no formal 90-day review
  template** yet. Two inputs to lean on:\n1. **\"90 Day Reviews in Lettuce\"** discussion
  topic — Andy Monroe, 2026-04-29, https://www.notion.so/3518146861518034891fc2951a744d00.
  Soliciting EM feedback on what Lettuce's eventual form should include. Proposed
  fields:\n   - Current performance level (1-5), graded on expectation of role at
  90 days\n   - Strengths demonstrated so far\n   - Any concerns to watch for\n   -
  Manager's manager notified on submission\n2. **Engineering Ladder** — https://www.notion.so/2588146861518021a764ecb0b83b2787.
  Five pillars: **Accountability, Proactivity, Stewardship, Decision-Making, Collaboration**.
  Per the Messaging Team Check-In Template, first-ever reviews should color the Competency
  Matrix (Google Sheet) red/yellow/green at the engineer's current title and one above.\n
  \  - Matrix template: https://docs.google.com/spreadsheets/d/1d9NesaONslAUTU3Sq3_2aDCHOfb8g7mICN3NSOUBXeg/edit\n\n###
  What the review should cover\nCombine the two: use the Lettuce fields as the summary,
  use the five pillars as the structured backbone.\n\n1. **Overall performance level
  (1-5)** vs expectation at 90 days, plus a one-sentence rationale.\n2. **Strengths
  / superpower** — 2-4 bullets, each with a concrete example (PR / Linear ticket /
  1-1 anecdote). What is he uniquely good at?\n3. **Concerns / watch-outs** — 1-3
  bullets, each with what we'd want to see different in the next 90 days.\n4. **Pillar-by-pillar
  notes** — short paragraph per pillar where there's signal:\n   - Accountability
  — follow-through on commitments, owning outcomes\n   - Proactivity — raising risks
  early, taking initiative without prompting\n   - Stewardship — long-term care of
  systems, docs, cleanup\n   - Decision-Making — tradeoffs between speed/quality/scope\n
  \  - Collaboration — pod, mentor, cross-functional partners\n5. **Plan for next
  90 days** — 2-3 focus areas tied to upcoming Enterprise work and any matrix gaps.\n6.
  **Color the Competency Matrix** at his current title and one above (clone the Google
  Sheet template).\n\n### Evidence to pull before writing\n- Linear (assignee = Andrés
  Figueira) since 2026-01-26 — strong throughput on Enterprise pod tickets. Notable:
  Project Owner on **BW Extendable Registration Cards** (ENT-4674 → ENT-5438, in progress);
  eng design on **Call transcripts** (ENT-5913); deployed bug fixes incl. ENT-5712,
  ENT-5358, ENT-5562, ENT-5663, ENT-5719. ~30+ tickets shipped.\n- GitHub PRs authored
  & reviewed since 2026-01-26 (`gh search prs --author=<gh-handle> --created='2026-01-26..'`).\n-
  Quick Slack ping to **Lautaro** (mentor) for a mentor read-out.\n\n### Where to
  put the output\n- Create child page under his onboarding page titled \"90-day review
  — 2026-05-XX\".\n- Embed the colored competency matrix sheet.\n- Backfill the empty
  \"60-90 Days\" section of the onboarding page with a summary + link.\n- Log a \"90-day
  review\" entry in the 1-1 journal for the discussion.\n- Per the Lettuce design
  intent: tag/DM **Blake (VP Eng)** with a link before the 1-1 with Andrés.\n\n###
  Out of scope\n- Building the Lettuce form (Andy Monroe's project).\n- Promotion
  / comp discussion.\n\nPlan file: /Users/garethlloyd/.claude/plans/mellow-mapping-parrot.md\n\n##
  Agent run 2026-05-07T12:14:29Z\n\nPulled the evidence and drafted the prep notes.
  Meeting is already on the calendar; no scheduling action needed. Open items called
  out at the bottom.\n\n### Meeting logistics — already scheduled\n- **2026-05-11
  11:00 Europe/Athens** — \"Andrés Figueira - 90 day check-in\" (one-off, distinct
  from the recurring Wed 1-1 on 2026-05-13). Calendar event id `5q2lfdmk4f775mde05b5hc7s05`,
  Andrés invited (response pending).\n- Title in Slack profile: **Senior Software
  Engineer**. Review against senior bar, not entry-level expectations.\n\n### Headline
  message: keep it up\nAt 90 days he is operating at full senior level on Enterprise
  pod. Strong throughput, clear ownership, real stewardship. The biggest job of the
  1-1 is to reinforce what's working and channel his already-stated appetite for broader
  scope into a meaty next-quarter anchor.\n\n### Evidence (receipts to bring)\n- **43
  Linear issues** since 2026-01-26: 31 Deployed + 2 Done = 33 shipped, 1 In Progress
  (his own BW reg cards project ENT-5438), 3 In Review, 5 Todo, 1 Canceled.\n- **42
  PRs merged** in `canary-technologies-corp/canary` since 2026-02-03 (handle `andresfigueira`)
  plus the cloudflare onboarding PR (#83). ~98% merge rate.\n- **Project Owner**:
  BW Extendable Registration Cards (ENT-4674 → ENT-5438), an 8+ PR arc: extracted
  legacy flow into private methods (ENT-5436), replaced `VENDOR_TEMPLATES` → `VENDOR_CONFIG`
  (ENT-5435), added the OnboardingValue + admin CSV upload (ENT-5434, ENT-5525), added
  a comparison panel for verification (ENT-5536), now driving the migration step.
  Refactor-before-extend then incremental rollout — exactly the shape you want from
  a senior.\n- **Eng Design ownership**: Call transcripts (ENT-5913), currently In
  Review.\n\n### Strengths (with anchors)\n1. **Drives multi-month projects to completion.**
  BW Extendable Reg Card project — refactor before extension, then incremental rollout
  with self-built admin tooling for verification. Anchors: ENT-5438 + the eight constituent
  PRs.\n2. **Stewardship beyond his ticket.** While doing batch work he investigated
  a 15-min Karpenter celery-onboarding pod cycling loop, filed PLAT-4194 for the Platform
  team with a full investigation doc. Anchor: 2026-04-15 EOD update in #epd-enterprise.\n3.
  **Defensive, thoughtful refactors.** WhatsAppPlan: bare asserts → `raise_expected_error`
  + partial-state handling (ENT-5715). Twilio area-code crash: asked clarifying questions
  in #epd-voice about intent for non-US hotels before fixing (PR #40812). Removed
  dead `RequireAuthenticationMiddleware` (ENT-5714).\n4. **Manages upward / agenda-driven
  1-1s.** Sets his own 1-1 agenda, brings architectural questions, has explicitly
  asked for broader scope (Bear note \"andres Figueira\", 2026-05-06).\n5. **Cross-team
  collaboration.** Active in #epd-enterprise, #epd-platform, #epd-voice, #epd-pms-gateway,
  #wyndham; coordinated Sevilla retreat transport (#apr-25-transfer-11-am). Steps
  up beyond engineering tasks.\n\n### Watch-outs / light constructive feedback\nKeep
  these short and forward-looking. Tone: \"here's where the next 90 days go\", not
  corrective.\n\n1. **Channel the appetite for broader scope.** He's asked. Anchor
  next 90 days on (a) shipping Call transcripts end-to-end as Project Owner from eng
  design through rollout, plus (b) one explicit cross-pod or cross-functional collaboration
  — leveraging the muscle PLAT-4194 already showed.\n2. **Visibility outside Enterprise.**
  Most output lands cleanly inside the pod. As he stretches toward senior-plus, want
  more of his thinking surfaced in eng-wide forums (design docs, RFCs, post-mortems).
  The BW reg-card refactor pattern is a strong write-up candidate — he's done the
  work, just needs to claim airtime.\n3. **(Self-note, not feedback for him)** 1-1
  journal is sparse — only 2 entries in 100 days. On me, not him. Commit to logging
  every 1-1 going forward so the next review has more granular threads.\n\n### Pillar
  coloring — Engineering Ladder (propagate into the Competency Matrix)\n\n| Pillar
  | At Senior | At Senior+/Staff |\n|---|---|---|\n| Accountability | GREEN — 33 shipped,
  daily EOD updates, owns BW reg card project end-to-end | YELLOW — wants ownership
  crossing pod boundaries |\n| Proactivity | GREEN — PLAT-4194 investigation, defensive
  refactors beyond ticket scope, asked for broader scope unprompted | YELLOW — surface
  findings to wider audiences, not just file the ticket |\n| Stewardship | GREEN —
  refactor-before-extend, dead code removal, ENT-5470 cohort heartbeat monitor, assertion
  hygiene | YELLOW — codify patterns into reusable guidance |\n| Decision-Making |
  GREEN — eng design for Call transcripts, scoped extendable reg card incrementally
  with safety gate | YELLOW — make tradeoffs visible to non-pod stakeholders |\n|
  Collaboration | GREEN — works across 5+ Slack channels, asks clarifying questions
  before patching, organized retreat logistics | YELLOW — mentor newer engineers,
  lead pairing/design sessions |\n\n### Plan for next 90 days (proposed — anchor for
  the conversation)\n1. **Ship Call transcripts (ENT-5913) end-to-end as Project Owner**
  — eng design → impl → rollout.\n2. **One cross-pod / cross-functional contribution**
  — Platform follow-up on Karpenter, a Voice handoff, or something he picks himself.\n3.
  **One piece of written eng leadership** — internal doc, blog post, or RFC. BW extendable
  reg card pattern is a strong candidate.\n\n### Pre-meeting checklist (for Gareth,
  before Monday 11:00 Athens)\n- [ ] Decide performance level (1-5). Based on the
  evidence above I'd land at 4 / above expectation against the senior bar — confirm
  with your in-room read.\n- [ ] Clone the Engineering Ladder Competency Matrix template
  ([sheet](https://docs.google.com/spreadsheets/d/1d9NesaONslAUTU3Sq3_2aDCHOfb8g7mICN3NSOUBXeg/edit))
  and color in the cells per the table above.\n- [ ] Skim the BW reg card PR thread
  for any specific anecdotes you want to read back to him.\n- [ ] Decide whether to
  bring the \"broader scope\" framing as a question (\"what would you pick?\") or
  a proposal (\"here's what I'd anchor on\"). The Bear note suggests he'd respond
  well to either.\n\n### Post-meeting checklist\n- [ ] Backfill the empty \"60-90
  Days\" section of his Notion onboarding page with a summary + link to the colored
  matrix.\n- [ ] Log a \"90-day review\" entry in the 1-1 journal.\n- [ ] DM Blake
  (VP Eng) a link per the Lettuce design intent for manager-of-manager visibility.\n\n###
  What I deliberately did NOT do (needs your call)\n- Did not create the Notion review
  child page.\n- Did not clone the competency matrix Google Sheet.\n- Did not DM Lautaro
  (mentor) for a read-out — drop the word and I'll draft the message for your approval.\n-
  Did not DM Blake.\n- Did not edit the Notion onboarding page or 1-1 journal.\n\nAll
  of the above are external writes that the runbook says I should ask for explicitly.\n"
project: 2026-04-10T0840-people
source_id: null
tags: []
time_minutes: 30
title: 90 day review for afigueira
updated: 2026-05-07 15:17:42.205178
waiting_on: null
waiting_since: null
working_on: false
---

* check notion for process
* schedule meeting
* prep notes 
  * constructive feedback mostly "keep it up"