---
area: null
contexts:
- consume
created: 2026-06-30 12:19:46.152790
defer_until: null
due: null
energy: low
id: 2026-06-30T1219-read-ramiro-s-epd-internal-tools-engineers-thread
order: null
output: |
  ## Agent run 2026-07-01T14:45:00

  Read the full #epd-internal-tools-engineers thread (Ramiro Nieto, 2026-06-29 → 06-30).
  Thread: https://canarytechnologies.slack.com/archives/C0A8L5RJM5K/p1782763288134409?thread_ts=1782763288.134409&cid=C0A8L5RJM5K

  ### What Ramiro is proposing
  Revive a project deprioritized a few months ago: detect drift between Salesforce
  (agreed source of truth) and Canary. Today there is NO way to know when a hotel or
  a subset of products is deactivated in SF but still active/in-use in Canary — i.e.
  usage we may not be billing for. At hotel-creation / product-add time we pull from
  SF, but nothing detects later drift.

  He scopes v1 to **non-enterprise hotels** (limit edge cases) with two related-but-distinct goals:
  1. **Reporting** — list of hotels with products active in Canary but not active in SF
     (money left on the table). Get via an Omni/Snowflake query. An Omni dashboard is enough.
  2. **In-product surfacing** — show a "product mismatch" indicator on the properties page
     so CSMs can self-serve fixes on their own hotels. Needs real design + implementation.
     Note: #1 is a *subset* of #2's mismatches; they are not the same query.

  ### Positions / debate
  - **Asher Davidson** — pushed on ROI. Argues it's not net-new revenue and likely
    not much per-hotel infra savings; asked what a set-up hotel actually costs/month
    (PMS connectivity fees? mostly AI products?). Even if we find unbilled usage, if
    the customer churned/was cancelled we probably can't claw it back — collections is
    hard, small recovery at best. BUT concedes drift makes us "look unorganized" and
    is worth addressing; real question is whether it beats other projects on ROI.
  - **Ramiro** — frames value as revenue *leakage* (money left on the table, not net-new),
    and more fundamentally: we have a source-of-truth agreement with SF and no way to
    verify Canary hasn't drifted. Agrees the effort should be **time-boxed**.
  - **Stephanie Barry** — previously did substantial work here; hit a big rabbit hole,
    queries have many edge cases and are time-consuming. Wants clear impact justification
    before committing. Sees **more value in enabling automated onboarding off a reliable
    source of truth** than in recovering money left on the table (feels CS is on top of
    assigned onboardings). Couldn't recall offhand whether her edge cases were mostly
    driven by enterprise SF setups — needs to re-check her metrics.

  ### Asher's open question (v1 shape)
  Does #1 need a UI at all, or is a **weekly cron → Slack roundup** enough for a first pass?
  Ramiro's answer: for #1 an Omni dashboard suffices; #2 is different — a weekly Slack
  message is not enough because the goal is CSMs taking action on their own hotels via
  the properties page, not tracking an aggregate number.

  ### Where it landed
  No decision — this is planning-phase discussion for "the next block." Consensus that
  a way to verify Canary matches SF is needed (Stephanie: "I completely agree"), but
  scope/priority still open. Key unresolved items:
  - Quantify impact first (mismatch rate on non-enterprise) before committing.
  - Whether the primary win is revenue recovery vs. enabling automated onboarding.
  - Whether Stephanie's earlier edge cases were mostly enterprise-driven (would validate
    the non-enterprise scoping).
  - v1 delivery: Omni dashboard (#1) vs. properties-page indicator (#2), time-boxed.

  ### Suggested next actions for you (not taken — awaiting your call)
  - Nothing required beyond reading. If you want to engage: weigh in on the
    revenue-recovery-vs-onboarding-automation framing, and note that scoping to
    non-enterprise should be validated against Stephanie's edge-case metrics first.
  - People to loop / already cc'd: Laura (U06V62WG492), Stephanie Barry (owns prior work).

  No external writes made (read-only research per task rules).
project: null
source_id: https://canarytechnologies.slack.com/archives/C0A8L5RJM5K/p1782763288134409?thread_ts=1782763288.134409&cid=C0A8L5RJM5K
tags:
- morning-gtd
- slack
- from-awareness
time_minutes: 10
title: 'Read Ramiro''s #epd-internal-tools-engineers thread: revive Salesforce-vs-Canary
  reconciliation'
updated: 2026-07-01 14:45:00.000000
waiting_on: null
waiting_since: null
working_on: false
---

Ramiro wants to revive the deprioritized project to find SF↔Canary mismatches (hotels/products active in Canary but deactivated in SF = unbilled usage). https://canarytechnologies.slack.com/archives/C0A8L5RJM5K/p1782763288134409?thread_ts=1782763288.134409&cid=C0A8L5RJM5K