---
area: null
completed_at: null
contexts: []
created: 2026-08-05 13:41:49.495862
defer_until: null
due: 2026-08-06
energy: low
id: 2026-08-05T1341-read-james-s-prioritization-doc
order: 3
output: |
  ## Agent run 2026-08-06T14:35

  Read: **EMEA Product Prioritisation Framework** (James Saram)
  https://app.notion.com/p/384814686151809ea6c1c4514a93aea4
  Parent: EMEA EPD Pod — https://app.notion.com/p/2f78146861518069a7b1e8998461a178

  ### What it is
  A framework for the EMEA pod to evaluate inbound requests with a consistent
  rationale — the foundation for both block planning and tactical prioritisation
  (and de-prioritisation). Short doc, still in review.

  ### The weighting (the operative bit)
  - Strategic Accounts — 40%
  - Non-strategic accounts (activation lag) — 20%
  - Foundational / country-specific — 20%
  - Sales cycle alignment — 20%

  ### Strategic bets for the year
  Activation lag · Voice AI · Service ticketing · Check-in V3 (specifically
  conditional ID logic) · GDPR + PII handling (incl. consent management).

  ### The four lanes, each with a core question
  1. **Strategic Accounts** — "Does winning this account unlock the region, or is
     it a standalone win?" Plus: which countries are viable today vs. have product
     or integration gaps. Examples: DeLuna (Spain — unlocks Neobooking + CEO-level
     referrals), Details Hotel Group (Portugal — first PT footprint).
  2. **Foundational / country-specific** — "Does building this once reduce friction
     for every market that follows?" Explicitly says: collaborate with the product
     *vertical* best placed to build it; EMEA pod unblocks/accelerates if the
     vertical is tight. EMEA owns the localisation layer, country config,
     compliance defaults, regional templates. Examples: GDPR/PII, Check-in V3
     conditional ID fields + regional templates, Voice AI multi-lingual/latency/
     WhatsApp.
  3. **Sales cycle alignment** — "Are we ahead of this sales cycle, or reacting to
     it?" Regular syncs with Manuel; look for requests blocking *multiple* deals.
  4. (Non-strategic / activation lag gets 20% of the weighting but has **no section
     of its own** in the doc — see open thread below.)

  Success metrics: EMEA CARR/ARR + product blocker tracker —
  https://emea.cnry.land/dashboards/emea-kpis/index.html
  Sub-metrics: % successful EMEA pilots, average resolution time of EMEA triage tickets.

  ### Open comment threads worth knowing (6, all unresolved)
  - **Martijn Dekker, 2026-08-05** (newest, on the Strategic Accounts heading):
    asks for a dedicated section for **Triage / non-strategic account activation** —
    "reality is that we have to help with onboarding non-strategic accounts, often
    for newer products such as Voice."
  - **Martijn Dekker, 2026-08-05** (on the "collaborate with the vertical" bullet):
    wants it moved to the top of the doc, since we coordinate with the vertical team
    first on all feature requests. Argues activation-related integrations carry edge
    cases / hidden commits that block onboarding — unplanned work verticals struggle
    to absorb. Cites **IC Berlin** and **Deluna**.
  - **Sebastian Cahill**: the compounding-wins argument applies equally to **new PMS
    integrations (Protel, Ulyses)** — James agreed.
  - **Sebastian Cahill**: WhatsApp deserves a call-out as an EMEA-specific channel —
    James added it under Voice AI.
  - **Sebastian / James**: sales-cycle visibility should surface in the SA meeting;
    James wants a **separate sync with Manuel** so EMEA roadmap input doesn't get lost.
  - **Sebastian**: opportunity to collaborate more with product marketing on
    pricing/packaging/positioning gaps.

  Next steps listed in the doc (all unchecked): align with Bree; James ↔ Manuel on
  EMEA sales strategy; James ↔ Dianna Kertz on which strategic accounts she joins.

  ### Linked doc you're named in
  The framework links to **Strategic Account Launch Playbook — EMEA (Testing Phase
  & QA)** by Sebastian, Draft v0.1 —
  https://app.notion.com/p/36781468615181b885cefd2197cd6207

  Two items in it land directly on eng / you:
  - §2 — "**Recommendation to eng (Gareth / Martijn): a pre-production 'definition
    of done' gate — including multi-language checks — for any release that touches
    live customer config.**" Framed as an eng quality-gate problem, tracked
    separately from the playbook. (Motivating incident: the Lugano Dante translation
    break.)
  - §9 — Bug SLA open item: "**ratify these targets and name a per-vertical on-call
    who owns fixes during a soft launch. Without a committed owner per product
    vertical, the loop will not close.**" Owner listed as Product / Eng.
  - §11 — open item assigned to Sebastian + James Saram: assess a Claude /
    Chrome-extension agent for automating the GJF-link-reachable browser flows
    (check-in web, upsells, compendium). Marked aspirational, needs James's input.

  Playbook context in one line: EMEA strategic accounts keep going live straight
  onto real guest reservations with no staging step (Grecotel, Eurostars, De Luna),
  so it proposes a ~4-week soft launch isolated via Guest Journey Flow segments on
  a test rate code, run by a per-launch tiger team. Also proposes funding a
  **dedicated EMEA QA engineer**.

  ### Suggested follow-ups (not actioned — no external writes made)
  - The framework has no lane owner for triage/activation despite it carrying 20% of
    the weight. Martijn has already raised it; worth backing him in the review.
  - The pre-prod definition-of-done gate is an ask on you with no ticket behind it.
  - Naming per-vertical on-call owners for soft-launch bug fixes is the thing that
    decides whether the playbook works at all.

  ## Agent run 2026-08-06T15:46 (revised 15:59)

  Task: boil the framework down to (a) core questions, (b) a flow chart.
  Source doc unchanged since the 14:35 run — worked from that read, no re-fetch.
  https://app.notion.com/p/384814686151809ea6c1c4514a93aea4

  **Revision note:** the first draft opened with a layer-ownership gate ("is the gap
  in EMEA's layer — localisation, country config, compliance defaults, regional
  templates?"). Wrong shape: that layer is narrow and most of the pod's real work
  sits outside it (activation integrations, onboarding edge cases, PMS work like
  Protel/Ulyses, the unplanned commits Martijn describes). A gate that rejects the
  majority case is not a gate. Ownership is a *mode of engagement*, and it belongs
  downstream — see Q3.

  ### (a) The framework as five questions

  **Q0 — Gate. Is an EMEA outcome on the line?**
  An EMEA account, an EMEA deal, or a market we're trying to enter. That's the only
  true filter. Nearly everything the pod sees passes it; what fails is genuinely
  someone else's request that arrived through an EMEA channel.

  **Q1 — Lane. Who is blocked, and what does that weigh?**
  Strategic account (40%) · non-strategic account blocked on activation (20%) ·
  foundational / country-specific (20%) · live sales cycle (20%).

  **Q2 — Leverage. Does solving it once compound?** One question per lane:
  - Strategic account → does winning this unlock the region, or is it a standalone win?
  - Foundational → does building this once reduce friction for every market that follows?
  - Sales cycle → does this block multiple deals, or one?
  - Activation → is this a recurring onboarding pattern, or one hotel's edge case?

  **Q3 — Engagement. Who has the capacity, and what does the pod do about it?**
  Three answers, not two:
  - EMEA's own layer (localisation, country config, compliance defaults, regional
    templates) → pod builds.
  - Vertical's surface, vertical has room → vertical builds; EMEA writes the spec
    and the evidence, and tracks it to done.
  - Vertical's surface, vertical is tight, or it's unplanned activation work → **pod
    builds it anyway.** The common case, and the one the framework doesn't name.

  **Q4 — Timing. Are we ahead of this, or reacting to it?**
  Ahead → block plan. Reacting *and* someone is live and blocked → triage lane, fix
  it, don't roadmap it. Reacting with nobody blocked → backlog with evidence.

  Tie-breaker when two requests land equal: does it sit on a year bet — activation
  lag, Voice AI (incl. WhatsApp), service ticketing, Check-in V3 conditional ID,
  GDPR/PII?

  ### (b) Flow chart (mermaid — pastes straight into a Notion code block)

  ```mermaid
  flowchart TD
    A[Inbound request] --> B{"Is an EMEA outcome on the line?<br/>an EMEA account · an EMEA deal ·<br/>a market we're trying to enter"}
    B -- No --> X["Not the pod's.<br/>Route to the owning team."]
    B -- Yes --> C{"Who is blocked?"}

    C --> L1["Strategic account<br/><b>40%</b>"]
    C --> L2["Non-strategic,<br/>activation-blocked<br/><b>20%</b>"]
    C --> L3["Foundational /<br/>country-specific<br/><b>20%</b>"]
    C --> L4["Live sales cycle<br/><b>20%</b>"]

    L1 --> K
    L2 --> K
    L3 --> K
    L4 --> K

    K{"Does solving it once compound<br/>beyond this one account / deal / hotel?<br/><i>see per-lane phrasing below</i>"}

    K -- Yes --> H{"Who has the capacity?"}
    K -- No --> I{"Is someone live<br/>and blocked right now?"}

    H -- "EMEA's own layer" --> R1["Pod builds — into the block plan"]
    H -- "Vertical's surface,<br/>vertical has room" --> R2["Vertical builds.<br/>EMEA writes the spec + evidence,<br/>tracks it to done."]
    H -- "Vertical's surface, vertical is tight,<br/>or unplanned activation work" --> R3["Pod builds it anyway.<br/>The common case — budget for it."]

    I -- Yes --> R4["Triage lane: fix now, don't roadmap it.<br/>needs a named owner — framework has none"]
    I -- No --> R5["Backlog with evidence.<br/>Revisit when a 2nd account asks."]
  ```

  Per-lane phrasing of **K** (the legend the chart points at):

  | Lane | Read K as |
  | --- | --- |
  | Strategic account | Does winning this unlock the region, or is it a standalone win? |
  | Non-strategic, activation-blocked | Recurring onboarding pattern, or one hotel's edge case? |
  | Foundational / country-specific | Does building it once reduce friction for every market that follows? |
  | Live sales cycle | Does it block multiple deals, or one? |

  **Layout note (revised 16:03):** the first draft gave each lane its own decision
  diamond, all four fanning into two shared targets. That's a 4→2 bipartite fan-in —
  it cannot be drawn without crossing edges, in any layout engine. Fixed by making the
  lane row pure classification and converging all four into a single compound test (K).
  4→1 fan-in is planar and everything after it is a tree, so the graph is now planar
  and cannot criss-cross. The per-lane questions moved into the legend above, which
  costs nothing — the compound test is one question instantiated four ways.

  ### Two things that fall out of drawing it
  - **"Collaborate with the vertical best placed to build it" reads as a routing rule,
    but it isn't one.** In practice the pod absorbs what the vertical can't take —
    activation integrations, onboarding edge cases, PMS work — and that absorption is
    uncapacitied and invisible. It's the R3 branch, and it's where the pod's time
    actually goes. If the framework exists to justify de-prioritisation, this is the
    branch that most needs a stated policy. Martijn's IC Berlin / Deluna comment and
    Sebastian's Protel / Ulyses comment are both instances of it.
  - **Triage / activation is a real terminal state with no owner.** 20% of the weight,
    no section in the doc, and the chart can't name who does the work when a request
    lands there. That's the biggest hole; backing Martijn on it is the highest-value
    review comment available.

  No external writes made — nothing posted to the Notion doc.
project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 5
title: Read James's prioritization doc
updated: 2026-08-07 12:20:15.118144
waiting_on: null
waiting_since: null
working_on: true
---

https://app.notion.com/p/canarytechnologies/EMEA-Product-Prioritisation-Framework-384814686151809ea6c1c4514a93aea4?source=copy_link

NEXT AGENT TASK:
* Attempt to boil the verbosity down two ways:
  * Core questions that determine alignment with pod
  * A flow chart