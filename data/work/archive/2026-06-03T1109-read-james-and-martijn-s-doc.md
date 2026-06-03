---
area: null
contexts: []
created: 2026-06-03 11:09:11.827772
defer_until: null
due: 2026-06-03
energy: medium
id: 2026-06-03T1109-read-james-and-martijn-s-doc
order: null
output: |
  ## Agent run 2026-06-03T12:00

  Read in full: **Strategic Account Launch Playbook — EMEA (Soft Launch & QA)**
  (Notion, Draft v0.1, author Sebastian. NB: titled "James and Martijn's doc" but
  authored by Sebastian — it carries asks directed at eng incl. you/Gareth, Martijn,
  and James Saram.)
  https://app.notion.com/p/36781468615181b885cefd2197cd6207

  ### What it is
  A proposed launch process for EMEA strategic-account go-lives. Core problem: EMEA
  accounts go live straight onto real guest reservations with no staging/sandbox, so
  bugs surface in production (Grecotel, Eurostars, De Luna, Lugano Dante). Fix is a
  deliberate, customer-sanctioned **soft launch** before hard launch.

  ### The mechanism (the clever bit)
  - **GJF (Guest Journey Flow) isolation** is the backbone control. Since guests can
    only reach check-in / F&B / compendium / upsells via GJF links, isolating GJF to
    test reservations isolates the *entire* downstream journey end-to-end with one
    control.
  - Primary method: a property-confirmed **test-only rate code** segment (must be
    confirmed *in writing* before toggling anything). Alternatives when no clean rate
    code (e.g. Grecotel custom PMS): dedicated test room number; email-address segment
    (NOT YET BUILT).
  - Model: ~4-week soft launch (2wk setup/validation + 2wk rigorous testing) → Go/No-Go
    → hard launch. Cross-functional "Tiger Team" (CSM, CS lead, 1-2 engineers for live
    triage, PM, Enterprise QA loop-in). Forks enterprise QA's Test Plan → Test Cases →
    Test Runs → Summary Report structure.

  ### What's directed at YOU (Gareth) / eng — action-relevant
  1. **§2 — explicit recommendation to "Gareth / Martijn":** stand up a pre-production
     "definition of done" quality gate (incl. multi-language checks) for ANY release
     touching live customer config. This is framed as an eng-quality-gate problem,
     deliberately scoped OUT of the launch playbook and routed to eng. The Lugano Dante
     translation break is the motivating example. → This is the most concrete eng ask;
     likely the reason this landed on your plate under "Unblock team."
  2. **§11 + §15 open item — "Sebastian + James Saram":** assess feasibility of a
     Claude / Chrome-extension agent that walks GJF-link-reachable flows (check-in web,
     upsell pages, compendium) and asserts pass/fail (transliteration, language, field
     population). Marked aspirational, "needs James's input before we commit." PMS-side
     reservation creation stays manual, so it complements (not replaces) the bug bash.
  3. **§9 open item — Product/Eng:** ratify the bug-fix SLA (P0 ack 4 bus-hrs / fix 1-2
     days; P1 1 day / 3-5 days; P2 2 days / within window) AND name a per-vertical
     on-call who owns fixes during a soft launch. Doc is explicit: "Without a committed
     owner per product vertical, the loop will not close."

  ### Other open items (FYI, not eng-owned)
  - Ratify entry thresholds (ARR ≥ $40k / close prob ≥ 80% — placeholders).
  - On-site mandatory at ARR ≥ $100k (Eurostars F&B lesson).
  - Build email-address-as-segment for GJF testing (Sebastian + James Saram + Rachel Kim).
  - Proposal to fund a dedicated EMEA QA hire (~80% of next-12mo sales projected
    mid-market/strategic); CS currently borrowed as fault-finder, which isn't their remit.

  ### Rollout intent
  Retrofit GJF isolation to Grecotel now (stabilise at-risk deal); first clean run on
  Danubius (if signed) + Travelodge UK.

  ### My read / suggested next actions for you
  - The doc's headline ask of you is the **pre-prod DoD / quality gate (§2)** and
    **naming per-vertical on-call owners (§9)**. Worth a direct reply to Sebastian on
    those two before the Tuesday/Strategic-Accounts review where thresholds get ratified.
  - The **James Saram automation thread (§11)** overlaps with your area (Claude/Chrome
    agent) — if you have a view on feasibility, that unblocks one of the open items.
  - No code change required by this task; it's a read + position-forming exercise.
    (No external writes made — Notion comments / replies not posted per approval rules.)
project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 15
title: read James and Martijn's doc
updated: 2026-06-03 13:26:44.629440
waiting_on: null
waiting_since: null
working_on: false
---

https://www.notion.so/canarytechnologies/Strategic-Account-Launch-Playbook-EMEA-Soft-Launch-QA-36781468615181b885cefd2197cd6207?source=copy_link