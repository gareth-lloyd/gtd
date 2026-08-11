---
area: null
completed_at: 2026-08-07 14:47:50.768868
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

  ## Agent run 2026-08-07T14:26

  Fetched the live doc (first time reading the actual prose rather than a summary),
  adversarially tested the Appendix A flowchart against it, then designed a
  replacement. Nothing written to Notion.

  ### Note: the flowchart is live in the doc
  The revised chart now sits in James's page as `# Appendix A - The framework as a
  flowchart`. Not written by me — no agent writes have been made at any point.
  It currently asserts three things James did not write (see below), so it's worth
  pulling or replacing fairly promptly.

  ### Adversarial review — why the chart fails against the prose
  Structural (the spine is wrong):
  1. **Lanes aren't exclusive, but the chart forces one choice.** Doc frames
     40/20/20/20 as "weighting the various areas" — an additive score. Proof in the
     doc's own text: **Voice AI is an example under BOTH Foundational and Sales Cycle
     Alignment**; Check-in V3 appears in the bets and in Foundational. A request can be
     strategic + foundational + sales-blocking at once, and that's exactly when it
     should win. The chart makes that unrepresentable.
  2. **The weights do no work.** Printed on L1–L4 as decoration; nothing downstream
     reads them. The chart routes, it doesn't prioritise.
  3. **"Who is blocked?" inverts the doc.** Strategic Accounts is about opportunity
     ("unlocks the region", "proves viability in a country we haven't operated in").
     Sales is about getting *ahead* ("window to ship it before it becomes a blocker").
     The entry node turns a planning tool into a triage queue.
  4. **Ignored the doc's own axis.** Metrics section distinguishes unlocking CARR from
     unblocking ARR — a native decision axis tied to the tracked dashboard. I invented
     "does it compound?" instead, which is Foundational's vocabulary and appears
     nowhere in Sales Cycle Alignment.

  Fidelity (asserted things the doc doesn't say):
  5. **Q0 scope gate is fabricated** — the doc never contemplates declining a request
     as out-of-region. Scope refusal attributed to James.
  6. **R3 contradicts the doc.** Prose: pod "can help unblock and accelerate ... working
     closely with that vertical". My R3: "Pod builds it anyway. The common case —
     budget for it." That's ownership transfer + a resourcing ask.
  7. **R4 embeds a criticism of the doc as a node label** ("needs a named owner —
     framework has none") — review feedback escaped into the artefact.
  8. **L2 is invented and hides the gap it should expose** — makes the doc look more
     complete than it is, the opposite of backing Martijn.

  Dropped content:
  9. **Sales lane's core question is gone.** Doc: "are we ahead of this sales cycle, or
     are we reacting to it?" — I promoted its sub-bullet ("multiple deals?") and
     dropped timing entirely. Also lost: "window to ship before it becomes a blocker".
  10. **SA's second core question missing** — country viability: "which have blockers
      that would slow us down regardless of the account".
  11. Minor: "activation-blocked" ≠ the doc's "activation lag" (incident vs duration).
  12. Never rendered — `<b>`/`<i>` in node labels and K's shape defined after its
      inbound edges are unverified in Notion's mermaid renderer.

  ### The replacement design (drafted, not written anywhere)
  Diagnosis: the doc conflates **ranking** (which request wins — the weights) with
  **routing** (who builds it). Prose lets it get away with that; a tree can't express
  an additive score. Answer is two small tables, not a chart.

  **Table 1 — scoring rubric.** Every request scores on all four dimensions, 0–3,
  weighted. Columns: Dimension (weight) | Core question in the doc's own words |
  Score anchors | Moves (CARR/ARR).
  - Strategic accounts 40% — 3 unlocks a market (new country, a PMS/CRS that opens one
    e.g. Neobooking, or a reference generating onward deals) · 2 expands a market we
    already serve · 1 standalone win · 0 not strategic. → CARR
  - Activation lag 20% — ⚠ flagged in-table as "no section in the doc, anchors are a
    proposal to ratify": 3 recurring blocker across onboardings · 2 blocks a live
    onboarding, likely to recur · 1 one-off single property · 0 none. → ARR
  - Foundational / country 20% — 3 compounds across markets incl. beyond EMEA into
    APAC · 2 unlocks one further market / kills a class of config work · 1 single-market
    localisation · 0 no reuse. → CARR
  - Sales cycle 20% — 3 blocks multiple deals across the region · 2 one deal in a
    product sales is actively pushing · 1 single deal · 0 none. → ARR

  Two design choices to argue rather than assume:
  - **Timing is scheduling, not score.** "Ahead or reacting?" sets *when* (block plan
    vs triage lane); breadth sets *how much*. Folding both into one number lets a
    one-deal fire outrank a regional unlock. Recovers the timing question the chart lost.
  - **Country readiness is an intake field, not a score** — Ready / product-integration
    gap / Blocked regardless. A "blocked regardless" flag should hard-stop the work
    whatever it scores.

  **Table 2 — worked examples** (the part that makes it real):
  | Request | SA×.4 | Act×.2 | Found×.2 | Sales×.2 | Score | Timing |
  | DeLuna — Neobooking integration gaps | 3 | 2 | 2 | 2 | **2.4** | Reacting, live |
  | Check-in V3 conditional ID + regional templates | 2 | 2 | 3 | 2 | **2.2** | Ahead |
  | Voice AI — WhatsApp + multi-lingual | 1 | 2 | 3 | 3 | **2.0** | Ahead |
  | IC Berlin — single-property config edge case | 0 | 1 | 0 | 0 | **0.2** | Reacting, live |

  DeLuna tops it *because* it scores on all four — the thing exclusive lanes can't
  express. IC Berlin lands at 0.2 while still being work someone must do today: exactly
  Martijn's tension, made arguable instead of hidden.

  **Table 3 — engagement mode** (straight tabulation of the doc's own sentences, no
  editorialising): localisation/country config/compliance defaults/regional templates →
  pod builds and maintains · everything else + vertical has capacity → vertical builds,
  EMEA shares requirements + evidence and tracks to done · everything else + vertical
  tight → vertical with EMEA alongside, "help unblock and accelerate". Deliberately
  does NOT say "pod builds it anyway" — if Martijn is right that it should, that's a
  conscious change for James to make, near the top of the doc per his comment.

  Stays prose: strategic context + the five bets, account examples, metric links,
  Manuel/SA cadence.

  Fallback if the pod balks at arithmetic: same table, drop the multiplication, use as
  a checklist with 40/20/20/20 as tie-break order. Loses ranking, keeps the thing that
  matters — four named tests with concrete anchors so two people score alike.

  ### Open questions for James (not resolved unilaterally)
  1. Activation lag carries 20% with no section and no anchors — ratify or drop the weight.
  2. Ahead-vs-reacting as scheduling rather than score — agree?
  3. Engagement mode 3: "accelerate alongside" or "pod absorbs"? Martijn says the latter.
  4. Triage lane still has no named owner (same open question as the Launch Playbook's
     per-vertical on-call).
  5. Does a "blocked regardless" country flag hard-stop the work?

  ### POSTED TO NOTION 2026-08-07T14:38 (user-approved)
  On explicit instruction, appended the replacement appendix to the end of James's
  framework doc as **"Appendix B — Scoring a request (proposal)"**:
  https://app.notion.com/p/384814686151809ea6c1c4514a93aea4
  Verified by re-fetch — all three tables rendered as native Notion tables with header
  rows, ⚠️ activation-lag flag intact, five open questions numbered at the bottom.
  This is the only external write made across all runs on this item.

  Two follow-ups left open (not actioned — second write not approved):
  - The original **Appendix A (the mermaid flowchart) is no longer on the page.** It
    was present at the 2026-08-06 fetch, absent at the 2026-08-07 fetch. Not removed by
    me (insert_content appends, cannot delete) — presumably pulled by Gareth after the
    adversarial review recommended it.
  - Consequently the posted appendix is misnumbered ("Appendix B" with no A) and its
    framing line refers to "the Appendix A flowchart" that a reader won't find. One
    edit fixes both: renumber to A and reword the clause, OR restore the flowchart.

  ### Paste-ready appendix drafted
  Final copy written to the session scratchpad (ephemeral — say the word to relocate
  it somewhere durable): `appendix-a-proposal.md`. Four sections — rubric, worked
  examples, who-builds-it, open questions — framed throughout as a proposal for James
  to reject or amend, with the invented activation-lag anchors flagged inline. Not
  posted to Notion.
project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 5
title: Read James's prioritization doc
updated: 2026-08-07 14:47:50.768861
waiting_on: null
waiting_since: null
working_on: false
---

https://app.notion.com/p/canarytechnologies/EMEA-Product-Prioritisation-Framework-384814686151809ea6c1c4514a93aea4?source=copy_link

NEXT AGENT TASK:
* Attempt to boil the verbosity down two ways:
  * Core questions that determine alignment with pod
  * A flow chart