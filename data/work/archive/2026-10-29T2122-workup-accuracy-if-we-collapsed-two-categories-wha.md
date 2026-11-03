---
area: null
completed_at: 2026-10-30 16:34:05.239457
contexts: []
created: 2026-10-29 21:22:54.957125
defer_until: null
due: null
energy: low
id: 2026-10-29T2122-workup-accuracy-if-we-collapsed-two-categories-wha
order: null
output: |-
  ## Agent run 2026-10-30T13:08

  **Answer.** Merging code-fix and no-action helps most: 53.3% to 60.0% (56 to 63 of 105 human labels). I would not ship it, because it hides Workup's worst error. The best merge that still makes sense is request-info and no-action: 56.2% (+3 tickets).

  **Data.** This is the 2026-09-18 snapshot in backend/canary/tmp/data/workup_typesafe: 201 declarations, 105 human labels. Any merge raises raw accuracy or leaves it flat, so I also report kappa, which corrects for chance. Base kappa is 0.453.

  | Merge | Tickets gained | Accuracy | Kappa |
  |---|---|---|---|
  | code-fix + no-action | +7 | 60.0% | 0.494 |
  | config-change + no-action | +5 | 58.1% | 0.473 |
  | ops-action + code-fix | +4 | 57.1% | 0.458 |
  | config-change + code-fix | +4 | 57.1% | 0.436 |
  | request-info + no-action | +3 | 56.2% | 0.480 |
  | config-change + ops-action | +3 | 56.2% | 0.435 |

  code-fix + no-action is the top merge in 52% of bootstrap resamples, so the ranking is moderately stable, not settled. It also comes out joint top for Jev v1 (42.9% to 50.5%, tied with config-change + no-action).

  **Why not code-fix + no-action.** All 7 tickets are one error: Workup said code-fix and the human said no-action. Workup has 27 labelled code-fix calls, 9 right and 18 wrong, so this is 7 of those 18 misses. Merging would stop counting the case where an engineer gets sent to write a PR for behaviour that is expected.
  - The judge's reasoning says the behaviour was expected or already fine on 4: ONC-25785, ONC-25806, ONC-25817, ONC-26252 (https://linear.app/canary-technologies/issue/ONC-25785, https://linear.app/canary-technologies/issue/ONC-25806, https://linear.app/canary-technologies/issue/ONC-25817, https://linear.app/canary-technologies/issue/ONC-26252).
  - ONC-26201 closed because logs had expired, so that label is hindsight (https://linear.app/canary-technologies/issue/ONC-26201).
  - The judge said config-change on ONC-25833 and has no grade on ONC-26296, so those 2 labels are soft (https://linear.app/canary-technologies/issue/ONC-25833, https://linear.app/canary-technologies/issue/ONC-26296).

  **Why request-info + no-action is the defensible one.** It has the second-best kappa, and both buckets mean no Canary fix is pending.
  - Workup is 0 of 4 on request-info as labelled, and humans called 3 of those 4 no-action: ONC-26173, ONC-26266, ONC-26507 (https://linear.app/canary-technologies/issue/ONC-26173, https://linear.app/canary-technologies/issue/ONC-26266, https://linear.app/canary-technologies/issue/ONC-26507).
  - All 3 already carry cause category `expected_behavior`.
  - Precision on the merged bucket is 7 of 10, up from 4 of 6 for no-action and 0 of 4 for request-info.
  - The cost: request-info tells someone to go back to the reporter, and the merge loses that instruction. It also gains only 3 tickets.

  **What this says about the metric.** The accuracy loss is mostly no-action, not two buckets that blur together. Humans said no-action 22 times and Workup got 4. config-change + ops-action, the pair the taxonomy spends most effort separating, gains 3 tickets and lowers kappa, so that boundary is not the main problem. The earlier no-action gate attempt failed and cost Workup 4 correct answers (see NOTES.md), so I have no cheap fix to offer.

  **Limits.**
  - The data is 6 weeks old and pools plugin versions. next-steps.md has changed since: Hand off was renamed on 2026-10-23 and narrowed on 2026-10-28, and declare gained a sufficiency requirement on 2026-10-28. These numbers may not describe current Workup.
  - I did not re-pull. The overlord DB is prod with a full-write role, and the repo rules require your explicit go-ahead for prod access.
  - Human labels were made after seeing Workup's answer, and the blind relabel from NOTES.md is still undone. Treat these as internal numbers.
  - Against the LLM judge instead of humans, the top merge is code-fix + duplicate (+10, 42.9% to 49.7%). Humans show only 3 such tickets. NOTES.md says 10 of the judge's rows are mechanical duplicate calls, which may explain it, but I did not check that overlap.

  Script: /private/tmp/claude-501/-Users-garethlloyd-projects-canary/472f8a9c-8446-4105-9b94-eb33b0b269cd/scratchpad/collapse.py

  ## Agent run 2026-10-30T14:07

  This run supersedes the conclusion above, which came from the stale September snapshot. Data: your exports from prod on 2026-10-30, /Users/garethlloyd/Downloads/q1.csv to q6.csv. 789 tickets, 218 human labels, 2026-08-20 to 2026-10-30.

  **Answer on current behaviour.** Since 09-21 the top merge is Hand off (escalate) + no-action: +4 on human labels (60.0% to 64.7%, n=85, joint top) and +25 on the judge (40.5% to 46.4%, n=427). The all-time winner, code-fix + no-action (54.1% to 58.3%, n=218), is historical: 8 of its 9 tickets predate 09-21. The metric already scores a Hand off to a hotel: or vendor: owner and a no-action close as the same class (next-steps.md line 201). My counts use strict equality and do not apply that rule, because `owner` is null on 92 of 121 recent Hand offs.

  | Since 09-21 | Human labels | Judge |
  |---|---|---|
  | Accuracy | 60.0% of 85 | 40.5% of 427 |
  | Hand off precision | 11 of 20 | 24 of 95 |
  | Code-fix precision | 0 of 3 | 16 of 49 |
  | Request-info precision | 2 of 7 | 1 of 25 |
  | Duplicate recall | 7 of 18 | 26 of 63 |
  | No-action recall | 8 of 18 | 15 of 71 |

  **Where the agent is wrong now.**
  1. Unproven code bugs handed off. Code-fix fell from 25% to about 10% of declarations, and Hand off rose from 12% to about 20%. Hand offs with cause `code_bug` are 43 of the 121 recent Hand offs, and the judge agrees on 3 of 33. It said duplicate 8, no-action 7, code-fix 6, config-change 5, ops-action 2, feature-request 2. next-steps.md line 181 makes this route deliberate. The weak code-theory problem looks moved, not fixed. That link is an inference from timing and cause.
  2. Missed duplicates. 11 of the 34 recent human-label misses. On 6 the judge's mechanical duplicate rule fired with no exclusion for a later target: PMS-10656, MSG-6370, MSG-6374, INT-11387, MSG-6554, PMS-11307. One human note says VXP tickets should not be duplicate candidates (PMS-11113).
  3. Missed no-action. 10 of the 34. Recall on human labels rose from 15% to 44%, but the judge shows 21%. Some are hindsight, such as INT-11591, a temporary glitch.

  **Possibly already improving.** Hand off share is 11% of 53 tickets since 10-28, down from 23% of 378 earlier in October. TOOL-836 merged on 10-28 (https://github.com/canary-technologies-corp/canary/pull/61920). Those tickets are young, so this is not yet evidence.

  **Measurement problems.**
  - Humans labelled 62% of tickets before 09-21 and 15% since, and only 5 of 84 in the latest week.
  - Labelled tickets look easier: Workup agrees with the blind judge on 36 of 69 labelled and 119 of 319 unlabelled. The 60% is probably optimistic. Human and judge agree on 52 of 69, so neither is firm truth.
  - Q5 per plugin version is too sparse to use: most versions have a handful of labels.
  - Q4: none of the 12 Nudge asks has a human label, so its effect on request-info is unmeasured. 10 of the 12 were answered.
  - Judge scores on request-info grade how the ticket closed, not whether asking was right, so 1 of 25 understates it.
  - Q1 shows 0 labels predating their declaration, where NOTES.md says 6 of 91. I did not resolve this.

  **Next step.** Read the 33 judged `code_bug` Hand offs before changing the agent. Q2 lacks reasoning and `specific_object`, so this needs one more query. No agent changes were made.

  ## Agent run 2026-10-30T14:11

  Read all 43 `code_bug` Hand offs since 09-21 (Q7 export, pasted in session). This corrects the run above: 3 of 33 overstates how wrong Workup is, and "the weak code theory moved" is only partly right.

  **Finding: this Hand off cannot score right on its own terms.** The rule at next-steps.md line 183 hands an unproven `code_bug` to the owning team, usually the ticket's own team. The judge only awards Hand off when a hotel or vendor runs the fix.
  - The 3 agreements are not credits for the theory: PMS-11514 (IHG chain code), STAY-5659 (Simphony POS codes), MSG-6526 (Booking.com). In all 3 the declared object named Canary code, and the fix was external.
  - Of the 11 rows with `owner` set, 10 name the team the ticket is already on. The exception is APAC-242. A human note on MSG-6281 says the same: "weird to have declared an escalation here since the ticket was already being routed to MSG."
  - This bucket works as "could not prove it", not as a next step.

  **What the 33 judged tickets became:**
  - Duplicate 8 (10 before the 2 exclusions, STAY-5386 and MSG-6520). Duplicate outranks the unproven route, so finding the target would have made these right. I do not know whether search missed them or the gate rejected them.
  - No-action 7. Some look knowable: AD-10168's declared object names the `NO_CARD_ON_FILE` safeguard that was working as designed.
  - Code-fix 6. Judging by PR titles only, not diffs, the declared location looks right on PMS-11487 and SDM-5223, and the area looks right on AD-10378 and AD-10320. The bar blocked these from code-fix.
  - Config-change 5, ops-action 2, feature-request 2. Theory wrong or fix elsewhere.

  **Evidence gaps.** About 11 of the 43 name a real access or budget failure, such as PMS-11480 (canary-mcp-us timed out for the whole run), MSG-6374 (canary-mcp-eu 403) and MSG-6281 (canary-mcp-eu 404/500, no fallback tried). 15 rows report findings "in no claim pool" (`scripts/pipeline/run.py:485`). Those findings stay in their envelope, so this is not proof the debate lost them. Q8 tests whether either kind of gap lowers agreement. Q8 is on the clipboard and not test-run: /private/tmp/claude-501/-Users-garethlloyd-projects-canary/472f8a9c-8446-4105-9b94-eb33b0b269cd/scratchpad/q8.sql

  **Recommendation.**
  1. Find out why the duplicates were missed. It is the largest group, and the fix would change the declared step, not just the score.
  2. Report "could not prove it" separately, as an abstention rate next to accuracy. Without the 33, judge agreement moves from 40.5% to 43.1% (170 of 394), and 7.7% of graded tickets abstain. This changes the measure, not the agent. It needs the paired agents-repo change if it becomes a bucket.
  3. Do not loosen the code-fix bar yet. 6 of 33 is the upside, and 16 of 33 had a wrong theory or a fix elsewhere.

  No agent changes were made.

  ## Agent run 2026-10-30T14:15

  Q8 result, 573 runs since 09-21. Evidence gaps show no link to agreement with the judge, so they come off the accuracy ranking.

  | Findings | Access or budget | Runs | Hand offs | Graded | Right | Agreement |
  |---|---|---|---|---|---|---|
  | Dropped | Gap | 23 | 7 | 20 | 8 | 40.0% |
  | Dropped | No gap | 108 | 25 | 77 | 32 | 41.6% |
  | None dropped | Gap | 51 | 12 | 40 | 17 | 42.5% |
  | None dropped | No gap | 391 | 77 | 291 | 117 | 40.2% |

  Limits: the gap detection is a text match on `tool_gaps`, so it misses gaps a run did not report. The judge is not firm truth. Runs with gaps may differ in other ways. Runs with an access or budget gap hand off slightly more often (26% vs 20%). This query counts 1 more graded ticket than earlier (428 vs 427), which I did not trace.

  Findings dropped from the claim pool affect 23% of runs (131 of 573). That may be worth fixing as data quality, but this data does not show an accuracy gain.

  The ranking is unchanged otherwise: duplicates first, abstention reporting second, code-fix bar left alone. No agent changes were made.

  ## Agent run 2026-10-30T14:53

  Missed duplicates investigation, since 09-21. This replaces the earlier duplicates ranking: missed duplicates are no longer the first thing to fix.

  **Size:** the 8.7-point ceiling falls to 4.7 (20 of 427 graded tickets), counting only pairs that are really the same problem. It is 8.4 if partial overlaps count. Since 10-09 the strict ceiling is 2.4 points (5 of 208).

  **Where the misses happened:**

  | Stage | Same problem | Partial overlap | Unclear | Total |
  |---|---|---|---|---|
  | Search: target not found | 6 | 10 | 1 | 17 |
  | Debate: target seen, no duplicate call | 10 | 4 | 0 | 14 |
  | Debate never ran | 1 | 0 | 0 | 1 |
  | Evidence missing | 3 | 2 | 0 | 5 |
  | Total | 20 | 16 | 1 | 37 |

  The other 22 of the 59 tickets are outside that table. 20 had targets that didn't exist in time, including INT-11731, whose target appeared 15 seconds before declaring. 2 have no target identified (MSG-6371, MSG-6650).

  **Findings:**
  - **Gate:** it never rejected a final target. 47 tickets had a rejection, and only 3 of them later graded as duplicates. None of those rejections hit the final target.
  - **Debate:** all 10 same-problem misses predate 10-09. TOOL-796, TOOL-745 and TOOL-839 landed from 10-02 to 10-09, which fits but doesn't prove they helped.
  - **Search:** targets are often named after the internal mechanism, such as "Fix addressed informational", while Workup searches by symptom. Replaying 16 tickets' symptom queries found the target in the top 11 for 5 of them. In a 3-query depth check, targets ranked 43rd and 74th, and one was absent.
  - **Concentration:** two targets, MSG-5578 and PMS-10910, account for 11 of the 37. Only 4 of those 11 are same-problem pairs.
  - **Wrong duplicates:** the judge disagrees with 22 of the 48 duplicates Workup declared, though humans disagree with only 1 of 8. That is as many as the real misses, and those 22 haven't been audited.

  **Recommendation:** don't change duplicate matching yet. Audit the 22 disputed declarations first. Raising the search limit is not supported, because the gatherer keeps only 5 symptom-only tickets and the 3-query check suggests deeper results are mostly noise. If the audit clears those declarations, the next fix is mechanism-aware search. No-action detection is now the better first target for accuracy, though its labels haven't had this audit.

  **Limits:**
  - Labels came from one AI read of each pair. It overrode human links on 13 of the 16 partial overlaps, and 2 same-problem calls are borderline.
  - Replays use today's Linear data and ranking, and 5 replay queries were retried after rate limits.
  - `run_id` never matched between evidence and declarations. Ticket identifiers matched on 27 files. The other 22 show a different identifier, which looks like team moves, but I only saw that on the search-stage rows and didn't verify it.
  - The planned spot check of 5 tickets per stage wasn't done, and only 3 tickets were checked by hand. The gate replay wasn't needed, because no final target was rejected.

  Working files are in /private/tmp/claude-501/-Users-garethlloyd-projects-canary/472f8a9c-8446-4105-9b94-eb33b0b269cd/scratchpad/ (`classified.csv`, `label_audit.csv`, `replay.csv`). No agent changes were made.

  ## Agent run 2026-10-30T15:20

  Audits of declared duplicates and missed no-actions, since 09-21. This replaces the 14:53 recommendation. Fix wrong duplicates first, then no-action. Don't build mechanism-aware search yet.

  **Declared duplicates (68 pairs audited):**
  - 43 are the same problem, 19 only related and 6 different.
  - 22 (32%) would have dropped a real problem that needed its own work.
  - The rate hasn't improved: 10 of 32 before 10-09, 12 of 36 since.
  - The auditor separates the judge's groups: 13 of 22 disputed declarations are harmful, against 2 of 25 agreed ones.
  - 3 of the 13 graded `auto_closed` declarations look harmful: MSG-6531, MSG-6602 and PMS-11426.
  - Cause doesn't explain it, because harm is spread across causes (`not_implemented` 7 of 19, `code_bug` 6 of 16). A cause-based rule won't work.
  - 5 of the 22 share only the hotel with their target.

  **Missed no-actions (57 tickets audited):**
  - 30 needed nothing, 26 needed action and 1 is unclear.
  - Of the 30, Workup could have known on 20, partly on 7 and not on 3.
  - The ceiling is 4.7 points (20 of 427), or 6.3 with the partly knowable. Since 10-09 it is 4.3 points (9 of 208), against 2.4 for missed duplicates.
  - Workup declared Hand off on 8 of the 20, and 7 of the 20 had a `code_bug` cause. An "is this working as designed?" check on unproven bugs reaches only those 7.
  - 2 of the 20 had cause `expected_behavior` and still weren't declared no-action (MSG-6469, AD-10270). This is unexplained.

  **Recommendation:**
  1. Tighten duplicates. Pull `same_mechanism` and the match type for the 68 pairs, then test candidate rules with the audit as labels. A rule must block most of the 22 harmful pairs and few of the 43 good ones.
  2. Then work on no-action. First explain the 2 `expected_behavior` tickets, then audit the 39 no-actions Workup declared, because the judge agrees with only 15 of 28.
  3. Hold mechanism-aware search. It would add more duplicate candidates while a third of current declarations are harmful.

  **Needs a human look:** these look like live problems. I changed nothing in Linear.
  - Closed as duplicates: MSG-6531, MSG-6602, PMS-11426.
  - Still open: MOB-1322, MSG-6494, PMS-11190, MSG-6818.

  **Limits:**
  - Each ticket had one AI read. It saw ticket text and comments only, no screenshots or logs, and read few target comment threads.
  - The audit and humans differ: 5 of the 10 tickets humans labelled no-action came out `action_needed`. One cause may be the audit counting a hotel or vendor step as action, which the official metric doesn't always do.
  - The ceilings can't be added, because tickets overlap (PMS-11421 is in both audits). No rule has been tested yet.
  - Four identifiers now resolve to other tickets: PMS-10748, MSG-6316, MSG-6472, INT-11705.

  Audit files are in the same scratchpad folder: `dup_declared_audit.csv` and `noaction_audit.csv`. No agent changes were made.

  ## Agent run 2026-10-30T15:45

  All data for this investigation now lives in `~/projects/canary/backend/canary/tmp/data/workup_accuracy/`, which is gitignored. Start with `NOTES.md` there. It maps every export, query, script and audit, and gives the next step. It replaces the scratchpad paths in the runs above.
  ## Agent run 2026-10-30T16:30

  Worked the three recommendations. Details are in `backend/canary/tmp/data/workup_accuracy/NOTES.md`.

  **Duplicates.** TOOL-862 already removes 5 of the 22 harmful declarations. No metadata rule separates the other 17. A blind re-read did. Version 1 blocked 14 of 17 harmful and 13 of 43 good, so it failed the bar of 9 harmful and 10% of good. The tuned version blocked 8 harmful and 2 good, one short of 9. Since 10-09 it blocked 5 of 8 harmful and 0 of 22 good. It was tuned on these pairs, so it needs fresh data. Agreement with the judge moves -0.2 points.

  **Draft.** Worktree `.claude/worktrees/workup-dup`, branch `glloyd/workup-duplicate-drop-test`, uncommitted and not pushed. Wording only, plugin 1.57.0. 1826 plugin script tests pass. No real debate has run with it.

  **No-action.** MSG-6469 and AD-10270 predate TOOL-833. Of the 39 declared no-actions, 16 were right, 7 had a hotel or vendor step, 15 needed Canary and 1 is unclear. 18 of 39 would drop a real problem, and 8 of 16 since version 1.39. The judge disagreed on 15 of 30. Decision: don't widen no-action.

  **Search.** Still held.

  ## Agent run 2026-10-30T16:45

  Filed TOOL-937 with your approval: https://linear.app/canary-technologies/issue/TOOL-937. It's in Backlog with no assignee or priority, and related to TOOL-862. The draft branch is still uncommitted and not pushed.
project: 2026-09-08-workup
source_id: null
tags: []
time_minutes: 5
title: 'workup accuracy: if we collapsed two categories, what would most improve the
  accuracy?'
updated: 2026-10-30 16:34:05.239450
waiting_on: null
waiting_since: null
working_on: false
---