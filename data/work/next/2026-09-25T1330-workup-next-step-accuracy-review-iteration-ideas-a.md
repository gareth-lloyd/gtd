---
area: null
completed_at: null
contexts: []
created: 2026-09-25 13:30:29.056626
defer_until: null
due: null
energy: null
id: 2026-09-25T1330-workup-next-step-accuracy-review-iteration-ideas-a
order: 1
output: |
  ## Agent run 2026-10-15T15:10

  Re-checked the seven ideas against what changed since 24 Sep: the handoff at ~/projects/plans/workup-workstreams-handoff.md (workstream map to 10-14, backtest), plus Linear. Selection is yours; this is my recommendation.

  ### What changed since the ideas were written
  - #4 is done. TOOL-608 config-against-capability, messaging first: Done 10-06, Kevin Cormier (https://linear.app/canary-technologies/issue/TOOL-608/investigate-plugin-config-against-capability-messaging-first).
  - #3 is partly done. Laura shipped two Code Fix rules: TOOL-733, code_bug needs an execution read (https://linear.app/canary-technologies/issue/TOOL-733) and TOOL-745, Code Fix needs a verdict on every open candidate (https://linear.app/canary-technologies/issue/TOOL-745). Per-queue base rates in classify are not done. Nobody has measured whether Code Fix over-declaration (49 declared, 8 agreed) dropped.
  - #6 is moving. TOOL-825 config auto-close is In Review (agents#409, canary#59747). TOOL-842 No Action auto-close is in Backlog. End to end stops being zero by construction once one gate lands.
  - The backtest sharpens #2 and #3. Workup gets 52.7% on 91 anchored labels (CI 43-63%), but only 4/21 on no-action tickets and 44/70 (63%) on the rest. The close cluster is its weakest area, and TOOL-842 targets exactly that bucket.
  - I have no accuracy figure after 18 Sep. The handoff already lists "ask Laura" as an open follow-up. Without it, nothing shows whether the 18-21 Sep pipeline changes moved the number.
  - Readability is not on this list but now has a PR: canary#59753 (compact 350-word report, Laura, no ticket).

  ### Recommendation
  Select:
  1. **#1 Trust the number.** Add a second grader to reach ~250 labels and put the bucket-only interval beside the headline. Still the highest leverage, it removes the single-grader bus factor before Laura's leave, and it costs less than 1% of run spend. Pair it with the ask for a post-18-Sep figure.
  2. **#2 Collapse the close cluster in the headline.** It is a cheap dashboard change. The 4/21 no-action result says the 8-way grid is noisiest exactly there, so do this before TOOL-842 ships or its effect will be hard to read.
  3. **#3, the remaining part.** First measure Code Fix declared/agreed on runs after TOOL-733/745 shipped. Only if it is still inflated, add per-queue base rates to classify. Don't rewrite rules that already shipped.
  4. **#5, CI fixture test only.** A gatherer that returns empty against recorded traffic should fail the build. Six silent-empty gatherers were the main September input bug. The dashboard indicator can wait.

  Defer / drop:
  - #4: drop, it's done. A follow-on worth asking about is how often the short-circuit now fires on messaging tickets before a second check gets built.
  - #6: defer until TOOL-825 lands, then reopen the end-to-end definition with Blake and Jason using real gate numbers.
  - #7: hold. Act only if someone proposes productionising Engram; the evidence (24 tickets, diagnosis judge) has not changed.

  Suggested block-review story: "~50% bucket-level once taxonomy noise is removed, CI-bounded; no-action/close cluster is the weakest area and auto-close is aimed at it; Code Fix rules shipped, effect being measured."

  ### Not done (needs your go-ahead)
  No Linear tickets, comments or messages sent. Selecting 1-3 implies drafting tickets (no owner exists for #1/#2) and asking Laura for the post-18-Sep figure. Say the word and I'll draft them locally for review.
  ## Agent run 2026-10-15T15:30 - option space, decision rule, research programme

  ### Options
  A. Measurement (does not move accuracy, decides whether we can see a move)
  - A1 Second grader, ~250 labels, inter-rater agreement as the ceiling
  - A2 Headline with the close cluster collapsed (and Config/Ops merged); 8-way grid kept as a diagnostic
  - A3 Post-18-Sep accuracy figure; freeze the judge while the pipeline changes so moves can be attributed
  - A4 Intermediate value metric: did the engineer act on the declaration without re-investigating?
  B. Accuracy movers
  - B1 Code Fix over-declaration: per-queue base rates in classify (after TOOL-733/745)
  - B2 No-action detection: expected-behaviour checks, TOOL-842 auto-close (backtest 4/21)
  - B3 Context gaps: CI fixture test for silent-empty gatherers, gap-free rate per queue
  - B4 More config-vs-capability checks beyond messaging (TOOL-608)
  - B5 Domain file coverage (8 of 9 thin)
  - B6 run_sql in EU/AP (TOOL-813)
  - B7 Nudge for Info (Request Info bucket, P-TOOL-2236)
  - B8 Engram memory
  - B9 Object sharpness when the bucket is right (Code Fix object 3/8)
  C. Value and cost
  - C1 Compact report (canary#59753)
  - C2 Auto-close gates (TOOL-825, TOOL-842)
  - C3 Cost: Haiku and fewer calls (P-TOOL-2141)

  ### Decision rule
  1. Measurement gates everything. At n~200 a 95% CI on bucket accuracy is about +/-7 pts; on a week (~70) it is about +/-11; one judge prompt edit swung 5.5. A mover expected to add less than ~5 headline pts can only be judged on a targeted subset eval, not the dashboard. Do A1-A3 first.
  2. Impact = tickets/week in the affected slice x share currently wrong x expected fix rate, in tickets/week moved to correct. Report it as a range with a confidence grade.
  3. Effort = engineer-days plus run spend to validate, sized by the likely owner.
  4. Rank by impact/effort. Take 2-3 with one owner each and a metric registered before the work starts. Kill or keep on the subset result, not the headline.

  ### Research programme (~2 weeks, mostly existing data)
  Phase 0, measurement (week 1, ~3 days of grading plus 1 day of dashboard work)
  - Pull the post-18-Sep figure. Second grader independently labels 50 runs already graded; compute human-human agreement. That is the ceiling and sets how much judge noise to tolerate.
  - Recompute the headline with the collapsed cluster across All/30d/7d.
  Phase 1, error attribution (week 1, ~2-3 days)
  - Take every bucket-wrong scored run since 18 Sep. Tag one primary cause from a fixed list: taxonomy ambiguity; missing context (gap present, and which gatherer); wrong conclusion with full context; Code Fix default; no-action missed; out of domain coverage; bucket right/object wrong. Two people tag a 30-run overlap to check the tags hold.
  - Output: share of errors per cause = the impact ceiling for B1-B9. This is the single most useful artefact; most options map one-to-one to a cause.
  Phase 2, per-option probes (week 2, top 3-4 causes only)
  - Use the replay harness (TOOL-743) on a 20-30 ticket subset per option with and without the intervention, same judge. At ~$11/run that is ~$300-650 per probe.
  - B1: replay the Code-Fix-declared subset with base rates injected.
  - B2: replay the no-action labels with an expected-behaviour check.
  - B3: re-run the gapped runs with the gatherer fixed; measures what gaps cost.
  - B4/B5: count how many wrong runs fall in a domain where a check or domain file would apply; no replay until that count is material.
  - B6/B7: read volume only (EU/AP share of tickets; Request Info share of labels).
  - B8: TOOL-583 replay through the next-step judge (Stephanie, ~1 day).
  - Effort: 30-minute sizing with the owner per option.
  Phase 3, decide (one meeting)
  - One table: option, impact range, confidence, effort, cost, owner. Pick 2-3.

  ### Unknowns
  Weekly ticket volume per queue; whether the replay harness can inject an intervention without a code change; who the second grader is.
project: 2026-09-08-workup
source_id: null
tags: []
time_minutes: null
title: 'Workup next-step accuracy: review iteration ideas and select some for implementation'
updated: 2026-10-15 15:26:15.208685
waiting_on: null
waiting_since: null
working_on: false
---

## Next action

Review these iteration ideas and select some for implementation.

## Context (investigation, 24 Sep 2026)

Reviewed six weeks of commits in the canary monorepo (`agent-plugins/claude-plugins/investigate/`, ~50 commits, ~42 by Laura DeWald) and the `canary-technologies-corp/agents` repo (86 commits, judge + dashboard, nearly all Laura), plus the Next Step metric doc, the judge spec, the unified plugin design, Laura's three Linear status updates (8, 15, 21 Sep), and the 23 Sep Workup sync transcript (mostly Engram evals and the SQL tool).

**Dashboard as of 24 Sep** (agents.cnry.land/workup, default range All): 30% right bucket and object on 208 scored; 84 of 208 (40%) right bucket alone; judge agreement 74% (66-80% at 95%) on 145 hand grades, still "provisional"; 0 of 216 resolved end to end; 557 runs, $10.77 avg, $643 this week; 444 runs with context gaps; duplicate auto-close gate failed (6 of 15 resolved, 2 wrong, max 1 allowed). 7d: 28% on 68. 30d: 30% on 194.

**What the team has done (five fronts):**
1. Made output scorable: 8-bucket + specific_object declaration on every terminal path since 20 Aug; two-pass judge (script from Linear records, then blind Sonnet bucket pick, then object grade); calibration bar = Wilson LB > 70% on >= 50 grades; eligibility rate shown beside headline.
2. Restructured pipeline: classify-area first, `select.py` picks gatherers/checks from frontmatter, 11 Bowerbird checks ported, short-circuit on unopposed observed claim, loop over ranked suspects (shipped 18 Sep), selection cut over from team filter 21 Sep, debate only if unresolved.
3. Fixed inputs: six gatherers parsing Datadog-era paths returned empty for present data; Groundcover account queries zero rows on 45/106 runs; Zendesk bodies unread; attachments unreadable 9 days; EU/AP MCP not region-routed; self-duplicates; 39% of Workup-team tickets never handed off.
4. Sharpened taxonomy and judge rules: Config vs Ops by persistence; team move is routing not Escalate; close-cluster tie-break (7 > 6 > 4 > 8); quiet close = null; duplicates with later-filed targets excluded.
5. Moved deterministic steps into code: sufficiency, duplicate, ceiling, branch, declare, region, summarize now Python; declare refuses off-taxonomy; only classify fork may write classification.json; sync sub-agent dispatch forced by hook.
Plus: read-only SQL tool (Teleport first, Sallyport later, staging next week); Engram claims 17-22% lift on 24 tickets but scored on diagnosis by a different judge; Blake wants Haiku cost analysis first.

**Why it is hard:** ground truth barely exists (tickets close silently, 41% ineligible all-time); buckets are judgment calls even for humans (Workup's declarations matched graders on 51/95); correct requires the object too (Code Fix sharpness 3/8); judge noisy at this n (one prompt edit swung 5.5 pts; identical runs differ ~1 ticket/class; single grader); wrong inputs fail silently (76% of runs have gaps); model follows prose ~half the time; budget tight (median wave 78/120 calls); coverage long tail (8 of 9 domain files "thin"; fast path theoretical until a config-vs-capability check exists); pipeline and judge change same weeks so moves are hard to attribute.

## Suggested improvements (ranked by leverage)

1. **Make the number trustworthy before moving it.** Add a second grader; get to ~250 labels (< 1% of run spend). Also fixes grading bus factor before Laura's leave. Block review shows bucket-only + interval beside the headline, never 30% alone.

2. **Collapse the close cluster in the headline.** Treating Request Info / Duplicate / No Action / Feature Request as one "closes without a fix" box lifts bucket-only from 84 to 96 of 208 (40% -> 46%); merging Config/Ops adds 7 more (50%). ~10 pts of the gap is taxonomy noise. Keep 8-way grid as diagnostic. Raised 9 Sep, no owner. Assign it.

3. **Attack over-declared Code Fix.** Declared 49 times, judge agreed 8; 22 ended Duplicate or No Action; object right 3/8 when bucket right. Code Fix has become the default when no config cause is found. Rules: Code Fix requires an observed claim naming a code path + log line, else declare Escalate with what was checked. Put per-queue base rates into classify so PMS tickets don't start from "probably a bug."

4. **Ship one config-vs-capability check (TOOL-608, messaging).** Short-circuit design is theoretical until one exists. Unassigned. Small scope (reuses server-side template validation).

5. **Track context gaps as the leading indicator.** 76% of runs have gaps; most Sept fixes were gatherers returning empty for existing data. Dashboard: gap-free runs per queue with a target. CI fixture test: gatherer returning empty against recorded traffic fails the build.

6. **Settle the end-to-end metric with Blake and Jason.** 0/216 is by construction (Workup can't close; duplicate gate just failed). Either fund the gate or stop reporting a number that can only be zero. Intermediate metric: did the engineer act on the declaration without re-investigating (label-correction rate, time-to-resolve on correct vs incorrect runs).

7. **Don't productionise Engram on current evidence.** 24 tickets, different judge, diagnosis not next-step. Replay corpus exists (TOOL-583): ask Stephanie to run same tickets with/without memory through the next-step judge (~1 day). Hold Laura's memory-poisoning concern open until then.

For the block review: lead with 1, 2, 3. Story becomes "40% bucket-level, ~10 pts taxonomy noise, one fixable failure mode driving most of the rest."

## Links
- Dashboard: https://agents.cnry.land/workup
- Catch-up brief: https://app.notion.com/p/canarytechnologies/Workup-catch-up-brief-16-Sep-2026-3dd8146861518127a5baca7c17b32a0e
- Next Step metric doc: https://app.notion.com/p/3b38146861518008b312fa94262e4ef4
- Judge spec: https://app.notion.com/p/3c28146861518170a05fdbcf46a6f7d2
- Plugin design (readable): https://app.notion.com/p/3bf81468615181e58428e5a18d91433c
- Accuracy project: https://linear.app/canary-technologies/project/ai-workup-accuracy-1bfe6e72996f
- 23 Sep sync transcript: https://docs.google.com/document/d/1sL60Nw08QGXBN4TfGSewKoMId_yMIOjcKbf0vE3loXw/edit