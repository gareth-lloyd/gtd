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
output: ''
project: 2026-09-08-workup
source_id: null
tags: []
time_minutes: null
title: 'Workup next-step accuracy: review iteration ideas and select some for implementation'
updated: 2026-10-01 14:56:22.711685
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