---
area: null
completed_at: null
contexts: []
created: 2026-09-03 22:22:33.141966
defer_until: null
due: null
energy: low
id: 2026-09-03T2222-laura-will-share-latest-workup-redesign-doc-for-re
order: null
output: |
  ## Agent run 2026-09-04T12:32:04Z

  Read the doc: "📖 Unified investigate plugin design (readable version)"
  (https://app.notion.com/p/canarytechnologies/Unified-investigate-plugin-design-readable-version-3bf81468615181e58428e5a18d91433c?source=copy_link)
  Status: **APPROVED**, Product: Workup, Owner: doc's Created-by user, Team: Internal Tools.
  This is the readable companion to the denser normative doc: https://app.notion.com/p/3bf814686151816391a4d784f859afcd
  (a contradiction between the two is treated as a bug in the readable one).

  ### TL;DR
  Redesigns the `investigate` Claude Code plugin (canary/agent-plugins/claude-plugins/investigate/,
  v1.2.0 on trunk) that Workup (the production ticket-triage agent) runs on every handoff. Three
  changes: (1) every run now ends with a scored, structured "next step" declaration instead of free
  text: bucket + specific object + evidence citations; (2) a 9-stage pipeline classifies the ticket
  and resolves the hotel's setup *before* gathering evidence, so it only runs checks/gatherers the
  symptom implicates, and stops as soon as it has an `observed`-confidence answer (the "short-circuit"
  rule); (3) a new runner-side "gate" scores each declaration (high/medium/low) before Workup posts
  it to Linear, so a weak diagnosis can't post as a confident one — low score = nothing beyond intake
  resolution, goes to an internal digest instead.

  Converges three prior efforts: the current plugin, "bowerbird" (comms-core's triage tool — evidence
  rules/budgets/checks/learn loop), and a separate targeted-iterative-investigation design
  (classification/hotel-setup-resolution/selection/loop) at https://app.notion.com/p/3bb81468615181558b0cdb554d216a7d

  ### Status / rollout
  - Phase 1 (next-step declarations, telemetry, Next Step labeling) is merged and live since
    2026-08-24. Plugin side: TOOL-551 (https://linear.app/canary-technologies/issue/TOOL-551),
    merged 2026-08-20. Overlord label posting: TOOL-552
    (https://linear.app/canary-technologies/issue/TOOL-552), merged 2026-08-24.
  - Phase 2 (extract core/ and bindings/, domains/ skeletons) in progress: TOOL-568
    (https://linear.app/canary-technologies/issue/TOOL-568, at PR) and TOOL-569
    (https://linear.app/canary-technologies/issue/TOOL-569).
  - Phases 3a/3b/4/5/6 are scoped but not started; sequenced in dependency order in the doc's
    "Order of work" table.
  - Two out-of-phase-table tickets: TOOL-583 (https://linear.app/canary-technologies/issue/TOOL-583,
    persist full tool-call output for the replay corpus) and TOOL-584
    (https://linear.app/canary-technologies/issue/TOOL-584, port bowerbird's demo-mode/messaging
    checks, hand-wired until select.py exists).
  - Gate is still shadow-only pending judge calibration; not enforcing yet.

  ### Open questions flagged in the doc itself (worth your input if you have a view)
  - Loop tuning: confidence threshold, default iteration cap, suspect ranking per area — "start
    conservative, let telemetry inform."
  - Capability-driven configuration: whether merged value or stored column is authoritative
    (blocks phase 4).
  - Problem-area vocabulary: seeded from worked examples + bowerbird categories, expected to grow
    via team PRs.
  - Debate budgets: ~10 tool calls/agent starting point.
  - Gate thresholds: global vs. per-team, and shadow duration before enforcement.
  - Recording/evidence handling: storage, retention, size caps, redaction before leaving the sandbox.
  - What the learn loop may read: comments carry useful signal but also eval-contaminating
    ticket-resolution info — needs separate learning-input vs. eval-input rules.

  ### Things that stood out (not blockers, just notable)
  - Ownership model is clean: Internal Tools owns core/bindings/scripts/orchestrator; each team
    owns its own domain/gatherers/checks/resolvers and "never edits another pod's files" — Workup
    reads core/taxonomies and core/schemas directly so buckets/causes change in one place for both
    runners.
  - "Fault outside Canary" is explicitly a result, not a failure (bucket 5) — nice guard against the
    tool inventing internal causes for vendor-side problems.
  - Explicitly NOT doing: migrating bowerbird onto the framework yet, building the judge/eval
    framework (separate specs), a second runner, interactive degraded-tool negotiation, or renaming
    the plugin to "workup".
  - "Config change" next-step buckets are graded later against actual Linear resolution by a judge,
    with `indeterminate` as an allowed verdict since most config changes leave no trace in Linear.

  No blocking concerns found on a read-through; nothing here required a Salesforce or external
  write. Recommend deciding whether you want to comment inline on the doc (would need explicit
  approval per session rules) or just reply to Laura with a thumbs-up / questions from the "Open
  questions" list above.

project: null
source_id: null
tags: []
time_minutes: 5
title: laura will share latest Workup redesign doc for review
updated: 2026-09-04 12:32:04.386878
waiting_on: null
waiting_since: null
working_on: false
---

https://app.notion.com/p/canarytechnologies/Unified-investigate-plugin-design-readable-version-3bf81468615181e58428e5a18d91433c?source=copy_link