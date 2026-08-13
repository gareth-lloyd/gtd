---
area: null
completed_at: null
contexts: []
created: 2026-08-12 21:12:50.368560
defer_until: null
due: null
energy: low
id: 2026-08-12T2112-check-on-onboarding-scripts
order: null
output: |
  ## Agent run 2026-08-13T05:06Z

  ### Bottom line
  The thread resolved well and Andrea's documentation follow-up already landed —
  faster than the 1-1 implied. Two loose ends need a nudge from you: **PR #52923
  (the docs PR) is approved but still unmerged**, and **Tyler's superseded PR
  #52466 is still open** after he agreed to close it. Both are one-click.

  The bigger item — "rest of the org defaults to management commands" — is real
  and I found hard evidence: this exact conversion has now happened **three
  times in 11 weeks**, always caught late by the Enterprise pod.

  ### 1. The Slack thread resolved — rollout framework won
  Thread: https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1786385978988089
  - Tyler Minard asked for Enterprise review of PR #52466 (TIP-5179, Marriott
    departments) — a new `ensure_marriott_departments` **management command**.
    https://github.com/canary-technologies-corp/canary/pull/52466
  - Andrea commented on the PR (8/10) suggesting the logic belongs in a service +
    rollout, then had Claude build PR #52768 as a demonstration.
    https://github.com/canary-technologies-corp/canary/pull/52768
  - Tyler conceded on 8/11, verbatim: *"Agreed — went and looked at #52768 and
    it's the better shape... let's ship yours and close this one out."*
  - **#52768 merged 2026-08-12.** `ENSURE_MARRIOTT_DEPARTMENTS_20260810` is on
    origin/master; `TargetedRollout` is now 9 members.
  - Worth noting: jbueno-canary's review on #52466 had already found 2 blocking
    bugs in the command (unscoped `--hotel` could provision Marriott departments
    onto any hotel in the system; one hotel missing tips config would abort the
    whole portfolio loop mid-run). Both classes of bug are structurally absent in
    the rollout framework — good ammunition for the "why this matters" argument.

  ### 2. Andrea's doc follow-up DID happen — next day
  She said *"I don't know if we've really documented the rollout framework, so
  I'll follow up on that."* She shipped both halves on 8/11:
  - **Notion:** "🚀 Rollout Recipes: Reconfigure Live Hotels at Scale", created
    2026-08-11, filed in Enterprise pod → Core knowledge base.
    https://app.notion.com/p/3b98146861518122b22bc85fd86987b7
    Genuinely good: populations, selection modes, staging, execution flow, how to
    add a recipe, worked examples, key-files table. Leads with the exact norm —
    *"Do not write a one-off management command for this."*
  - **Repo:** PR #52923 "Document rollout recipes in onboarding docs" (+45 lines
    to `docs/onboarding/README.md` and `backend/canary/onboarding/CLAUDE.md`).
    https://github.com/canary-technologies-corp/canary/pull/52923
    **Status: APPROVED, 0 failing checks, still OPEN since 8/11.**
  - ⚠️ Until #52923 merges, `docs/` and `onboarding/CLAUDE.md` on origin/master
    contain **zero** mentions of "rollout" — I verified. So the in-repo path
    (and every coding agent reading CLAUDE.md) still can't discover the
    framework. This is the single highest-leverage unblock here.
  - Minor: the Granola summary of your 8/12 Andrea 1-1 credits "Margarita" with
    the Notion doc, but both artifacts are authored by Andrea (`abrad`). Likely a
    transcription slip — check before crediting anyone publicly.

  ### 3. "Rest of the org isn't up to date" — confirmed, with numbers
  **Adoption is confined to the Enterprise pod.** All 9 targeted rollouts ever
  merged were authored by exactly three people: Martin Rodriguez (4), Andrea
  Bradshaw (3), you (1 infra + 1). Nobody outside the pod has used it.

  **Meanwhile, repo-wide in the last 90 days:** 173 new management commands, of
  which ~70 are `onetime_*` / `backfill_*` / `ensure_*` / `migrate_*` style. Not
  all of those should be rollouts (many are legitimately data migrations rather
  than hotel-config changes), but the ratio against 9 rollouts is stark.

  **The same conversion has now happened three times — each caught late:**
  | # | Original management command | Author | Outcome |
  |---|---|---|---|
  | 1 | `onetime_backfill_wyndham_availability_rate_code` (STAY-3604, 5/27) | Joanne C. | **You reverted it** 6/3 (#46522); replaced by `configure_wyndham_availability_rate_code_20260529` |
  | 2 | `onetime_enable_wyndham_pilot_dynamic_pricing` (STAY-3625, 6/16) | Joanne C. | Deleted by Andrea 7/30 (#51633); replaced by `enable_wyndham_dynamic_pricing_20260730` |
  | 3 | `ensure_marriott_departments` (TIP-5179, 8/6) | Tyler Minard | Replaced by Andrea's #52768, merged 8/12 |

  That's a recurring rework tax paid by your pod, three times, on a ~monthly
  cadence. It is a process gap, not a people problem — until 8/11 there was
  genuinely nothing to point anyone at.

  **One guardrail already works:** Macroscope auto-flagged #52466 with *"management
  commands that write data are on the hard deny-list and require human review."*
  That's the existing detection point. Worth asking whether its message should
  now link the new Notion doc / CLAUDE.md section — that would convert a generic
  block into an actual redirect, and it fires automatically on every offender.

  ### 4. Adjacent live thread you may want to fold in
  Your 8/6 group DM with Dana Levine, Vibhor, Stephanie Barry, Connor, Andrea
  about the check-in v3 config-service boundary:
  https://canarytechnologies.slack.com/archives/C0BNGM6R3UJ/p1786023015210429
  (references the older v2→v3 migration thread in C04STT7UPRQ)
  - The "Checkin V3 Rollout Sync" did happen Tue 2026-08-11 22:00 EEST (Connor,
    Dana, Vibhor, Stephanie, Andrea, Guido, Laura, you).
  - Per your 8/12 Andrea 1-1 Granola: **Connor and Margarita decided against a
    rollout script** for the v2→v3 version flag change — "just two boolean flag
    flips" — and **you flagged the missing audit trail**.
  - So the first real test of the freshly-documented methodology, one day after
    it was written, was answered with "not this time." That may well be the right
    call for two booleans, but it's the live example of the exact drift you're
    trying to close, and it involves an enterprise-sensitive rollout where timing
    matters to Wyndham. Probably the most valuable thing to press on.

  ### Suggested next actions (not taken — your call)
  1. Ping Andrea to merge #52923 — approved, green, just sitting there.
  2. Ask Tyler to close #52466 (he already agreed to).
  3. Decide the audit-trail question on the v2→v3 flag flip with Connor.
  4. Consider: link the new doc from Macroscope's management-command deny-list
     message, so the guardrail redirects rather than just blocks.

  ### Verification notes
  - Local `master` was 2 weeks stale (7/29); all repo claims re-verified against
    freshly fetched `origin/master` (27d60293217, 8/13).
  - No external writes made. Nothing posted to Slack, GitHub, Linear, or Notion.
  - Item #3's "decided against a rollout script" comes from the Granola summary
    of your 1-1, not from a primary source — worth confirming with Connor directly.
project: null
source_id: null
tags: []
time_minutes: 5
title: Check on onboarding scripts. Context from yesterday 1-1 Andrea granola
updated: 2026-08-13 08:06:35.944603
waiting_on: null
waiting_since: null
working_on: true
---

- Check-in on the direct/response here: https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1786385978988089
    - documented rollouts in response to this
    - Rest of the org is not up to date with our rollout methodology
    - Everyone defaults to management commands