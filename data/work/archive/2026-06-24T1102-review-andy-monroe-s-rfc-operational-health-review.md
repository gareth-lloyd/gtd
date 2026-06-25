---
area: admin
contexts:
- consume
created: 2026-06-24 11:02:30.072048
defer_until: null
due: 2026-06-24
energy: medium
id: 2026-06-24T1102-review-andy-monroe-s-rfc-operational-health-review
order: null
output: |
  ## Agent run 2026-06-25T14:55 — Review of Andy Monroe's RFC: Operational Health Reviews (OHRs)

  RFC: https://www.notion.so/canarytechnologies/RFC-Operational-Health-Reviews-OHRs-38781468615180d9b0afea3c5d152cb1
  Slack (#eng-directors): https://canarytechnologies.slack.com/archives/C09UN3697KK/p1782237738024519

  ### What the RFC proposes (TL;DR)
  - **Weekly**: an email data digest per team + management chain. Snapshot of charts (from Snowflake, via Omni), with the team lead explicitly prompted to add context and others to ask questions. Email is a point-in-time snapshot + link to Omni (source of truth).
  - **Monthly**: a recorded sync call per Product Area, led initially by Blake (SJ optional), director presents their area's data, everyone reads live and asks questions; each manager ends by declaring what changes they'll make to their OHRs.
  - **Why**: visibility into ongoing issues that don't reach Support (perf degradations, conversion, integration reliability), and a consistent way to assess product health to drive investment.
  - **Scope now**: Director / Product-Area level only. Explicitly intends to push down through every EPD team later (out of scope for now).
  - **Ask to directors**: produce an initial list of metrics to track (minimum 15) and work with Data to build dashboards.

  ### State of the discussion (already on the Notion doc — don't repeat blindly)
  The doc is NOT settled. Substantial unresolved debate, mainly **Andy Monroe (author) vs Jordan Sterling**:
  - **Meeting structure**: Jordan argues there must NOT be two separate priority meetings — pod-health review should happen *inside* block planning (review only reds/yellows; no-op pods cruise through). Andy counters that data review always loses to anecdote/intuition when it competes for time, so it needs dedicated, protected time. Andy has conceded he's "willing to try a lightweight version to start."
  - **Accountability mechanism**: Jordan wants metrics tied to director/lead **performance reviews** ("if it's measured it gets taken seriously"; targets per-team, some teams none). Andy worries this incentivizes owners to set the easiest threshold they can get away with and makes metrics hard to iterate on / delegate. Unresolved.
  - **Medium**: Jordan favors an Omni dashboard (all-eng, drill down) and/or Slack (can @-tag the one person who needs to respond, avoid "30 leads replying 'all good'"). Andy prefers email for guaranteed eyeballs + instant load (snapshot, since Omni loads slowly). Unresolved; Andy open to also pushing to Slack.
  - **Audience** (Ian Clark): clarified to leadership + director + manager-level (leads, PMs) for the area; ICs excluded.
  - **Metrics definition** (Sudarshan Muralidhar): "all of the above" — product, DORA, system health, triage load, PR review time — anything mappable to business implications.
  - **Your two existing comments**: (1) questioned the "minimum 15" — don't want people inventing metrics to hit a floor; (2) asked whether the monthly call is driven by product director or director of engineering. Both still good and open.
  - Blake Vanlandingham left "I'm good with this!" (he's the approver per the Who section).

  ### My substantive review (angled at Andy's stated design goal: sustainably useful, not another ignored dashboard)

  **1. The biggest tell that this risks becoming theater is the RFC's own action loop.** The monthly call ends with each manager declaring "what changes they intend to make to their OHRs to make them more useful." That's a change to the *report*, not a change to the *product/system in response to a bad number*. A health review is only sustainably useful if its output is "what are we going to do about this metric," not "how do we tweak the dashboard." Reframe the closing ask to a decision/owner/date on any metric out of bounds; dashboard-tuning should be the rare case.

  **2. No targets = no forcing function = guaranteed drift into noise.** The highest-leverage anti-"ignored dashboard" mechanism is exception-based review: a metric only demands attention when it breaches a defined target/SLO. The RFC commits to no targets, so every chart is merely "interesting" and nothing is actionable — Jordan's SLA-objective instinct is right. Without targets you also get exactly the failure Jordan named: one line in a 30-line graph, 30 leads replying "all good." Recommend targets (or an explicit "no target — awareness only") be a *required* attribute of every metric from day one.

  **3. "Minimum 15" is backwards (you flagged this — I'd push harder).** A floor manufactures vanity metrics, the fastest route to an ignored dashboard. Invert it: a small org-level *standard set* everyone reports (so cross-area comparison works), plus *as few* area-specific metrics as genuinely map to a decision. Quality / decision-relevance over count. If anything, cap — don't floor.

  **4. Cadence looks mismatched to how these metrics move.** Weekly email for slow-drifting metrics trains people to ignore it (alert fatigue = the stated failure mode); monthly may be too slow for an acute regression. Cleaner: always-on dashboard (source of truth) + monthly digest aligned to the sync + real-time exception alerts (Slack) on breach. The weekly cadence is the part most likely to die first.

  **5. The Andy-vs-Jordan "separate meeting vs block planning" split is the real decision — I lean to a synthesis, not either pole.** Jordan is right that two competing priority meetings is unsustainable and that autonomous teams shouldn't roll health review all the way up by default. Andy is right that data review loses to anecdote when unprotected. Synthesis: review health data *within* block planning by default (exception-only — reds/yellows get a timebox), and reserve a dedicated cross-area sync only for areas currently breaching, plus a periodic (e.g. quarterly) full read. Protects the time Andy wants without a standing all-directors monthly that won't survive calendars.

  **6. Scale math undercuts the single roll-up call.** 15+ metrics/director × directors, heading to 20-30 pods = hundreds of charts. A one-by-one roll-up to Blake/SJ doesn't scale and will be first to be cut. Exception-based review is what makes it scale — design for it now, not later.

  **7. Ownership is underspecified.** "The email prompts the lead to add context" is a weak forcing function. Name a single accountable owner per metric (not a team), and make "metric is red and nobody commented" itself a visible signal. On Jordan's perf-review idea: separate *process accountability* (did you track the right things and act on breaches — fair game for reviews) from *outcome accountability* (did the number hit target — softer, contextual, and the thing that gets gamed if hard-coupled to comp). That resolves most of Andy's gaming concern while keeping Jordan's "it gets taken seriously" benefit.

  **8. Pilot before org-wide.** Best way to avoid the ignored-dashboard fate: run it in ONE product area, 5-7 metrics each with a target, inside an existing meeting, for 2 cycles, and measure one thing — did it change a single real decision? Expand only if yes. De-risks the "lightweight version" Andy already said he's willing to try.

  ### Suggested next action for you
  Your two comments are already in. The most valuable additions are a top-level POV on (a) the action-loop reframe (#1), (b) targets-as-required / exception-based review (#2,#4,#6), and (c) where you land on the Andy-vs-Jordan meeting-structure fork (#5) — the unresolved fork Blake will ultimately decide. Draft below — NOT posted; needs your explicit go-ahead before anything goes to Notion or Slack.

  ---
  DRAFT comment (for your approval — not sent):

  "Strong +1 on doing this; feedback all aimed at the 'not another ignored dashboard' goal.
  1. The thing that makes or breaks this is the action loop. I'd change the end-of-review ask from 'what changes will you make to your OHRs' to 'for any metric out of bounds: what's the decision, who owns it, by when.' Tuning the dashboard should be the rare case, not the default output.
  2. Make a target (or explicit 'no target — awareness only') a required attribute of every metric, and make the review exception-based: a metric only demands a response when it breaches. Without that, every chart is 'interesting' and nothing is actionable — and we get the 30-leads-reply-'all-good' problem.
  3. +1 to my earlier note on '15' — invert it to a small shared org-level set + as few area-specific metrics as map to a real decision. A floor manufactures vanity metrics.
  4. On the meeting question (Andy/Jordan thread): I lean toward health review living inside block planning by default, exception-only, with dedicated time reserved only for areas currently breaching + a periodic full read — rather than a standing monthly all-directors sync. Protects the time without a meeting that won't survive calendars.
  5. Before org-wide: pilot in one area, 5-7 metrics with targets, 2 cycles, judged on whether it changed one real decision."

project: 2026-04-10T0840-ticket
source_id: https://canarytechnologies.slack.com/archives/C09UN3697KK/p1782237738024519
tags:
- morning-gtd
- slack
- from-awareness
time_minutes: 15
title: 'Review Andy Monroe''s RFC: Operational Health Reviews (OHRs)'
updated: 2026-06-25 14:55:00.000000
waiting_on: null
waiting_since: null
working_on: false
---

Andy posted an intentionally-short RFC in #eng-directors on a data-review process for Canary; asks directors for feedback (esp. how to keep it sustainably useful and not another ignored dashboard). RFC: https://www.notion.so/canarytechnologies/RFC-Operational-Health-Reviews-OHRs-38781468615180d9b0afea3c5d152cb1 — Slack: https://canarytechnologies.slack.com/archives/C09UN3697KK/p1782237738024519