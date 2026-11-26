---
area: null
completed_at: null
contexts: []
created: 2026-11-24 15:35:27.769802
defer_until: null
due: null
energy: null
id: 2026-11-24T1535-workup-accuracy-next-steps-from-the-confidence-che
order: null
output: |
  ## Agent run 2026-11-25T13:10:55Z

  Steps 1, 3 and 4 are analysed. Steps 2, 5, 6, 7 and 8 are drafted. Nothing was sent, posted or filed.

  All drafts are in one file: `/Users/garethlloyd/projects/canary/backend/canary/tmp/data/workup_accuracy/confidence/drafts.md`. The scripts moved out of the scratchpad to `backend/canary/tmp/data/workup_accuracy/scripts/confidence/`. Data is the local mirror, snapshot `workup-20261123-080952Z`, declarations 21 Sep to 22 Nov.

  ### Step 4: the finding holds on blind-graded rows

  Blind means `actual_source = 'judge'`: 647 of the 711 rows.

  | Confidence | All 711 | Blind 647 |
  |---|---|---|
  | High | 230 of 439 (52%) | 207 of 398 (52%) |
  | Medium | 81 of 249 (33%) | 71 of 226 (31%) |
  | Low | 1 of 13 | 1 of 13 |
  | None | 0 of 9 | 0 of 9 |

  - The gap is 21 points on blind rows (z = 5.0). It appears in each month: September 50% against 34%, October 49% against 28%, November 58% against 35%.
  - Hand off on blind rows: medium 20 of 77, high 26 of 45. Request-info: the grader chose it on 13 of 647, and Workup's asks were right 0 of 32.
  - One caution on duplicates. The 64 non-blind rows are mostly graded from the duplicate link itself, and score 30 of 30. On blind rows, high-confidence duplicates are right 8 of 29. Quote the blind figure for duplicates.

  ### Step 1: cost of a second pass on medium-confidence runs

  - Volume: 142 of 441 declarations in the last four weeks were medium (32%), about 36 a week.
  - Cost: a medium run averages $11.90 (high: $10.73). A full second pass costs about $1,690 per four weeks, or $420 a week. That adds 34% to Workup's spend of $4,899 over the same four weeks.
  - "Unsure is about the cause" checks out. Diagnosis is correct on 106 of 228 medium runs (46%), against 293 of 409 high runs (72%). With a correct diagnosis, medium runs get the next step right 53 of 106.
  - Size of the gain, as an estimate: if a second pass lifted medium runs to the high-confidence diagnosis rate, about 18 more next steps would be right out of 711, or +2.5 points. The ceiling, where medium runs match high ones, is +49 tickets, or +7 points. That is roughly $60 to $165 per extra right answer.
  - Cheaper option: run the second pass only on medium hand-offs, ops-actions and request-infos. Those are 127 of the 249 medium runs and score 24 of 127 (19%). That halves the cost.
  - Not shown: that a second pass by the same agent fixes the cause. These are correlations. A replay of about 50 medium tickets with a second pass would cost about $600 and would answer it. I did not run it.

  ### Step 3: gating auto-actions on high confidence

  | Declared step | High | Medium |
  |---|---|---|
  | Config change | 91 of 138 (66%) | 29 of 56 (52%) |
  | No action | 28 of 40 (70%) | 10 of 16 (63%) |
  | Duplicate, blind rows | 8 of 29 | 6 of 23 |

  - Blind-only figures are close: config 91 of 134 (68%), no-action 28 of 39 (72%).
  - The one-sided 95% lower bounds are 59% for config and 57% for no-action. Confidence alone is far from 90%.
  - Proposal: make high confidence a required condition for any close, on top of the existing gates. It keeps 138 of 194 config declarations (71%). The wording is in section 4 of the drafts file, as an addition to the Notion comment.

  ### Step 2: dashboard split for Hand off (draft ticket text, not filed)

  - Hand off overall: 50 of 143 (35%). High confidence: 27 of 48 (56%). Medium: 22 of 87 (25%). Low or none: 1 of 8.
  - Draft ticket text is in section 5 of the drafts file. Confidence comes from `workup_investigations.hypotheses[0].confidence`, joined on `usage_id`.
  - I did not read the dashboard code. The metric code is likely `overlord/src/workup-quality/db.ts` and `next-step-core.ts` in the agents repo. Say if you want this filed through /write-linear-ticket.

  ### Step 5: talking points corrected

  - Section 1 of the drafts file has the full corrected text. Old item 5 (request-info as a note) and old item 8 (name an owner) are removed. The confidence finding is a new "why" bullet and a new item 5. The hand-off bullet now gives the confident and unsure split.
  - The copy saved on 24 Nov in the old scratchpad is gone, so I rebuilt it from that session's transcript. Your clipboard still holds whatever was last copied; I did not touch it.
  - Optional and not applied: the request-info bullet still says 1 in 24, from the 2 Nov export. The current snapshot says 0 of 33.

  ### Step 6: Orbital feedback and a reviewer

  - Both PRs are unchanged since 26 Oct, checked today: agents#473 (https://github.com/canary-technologies-corp/agents/pull/473) and agents#474 (https://github.com/canary-technologies-corp/agents/pull/474). Both are open, mergeable, with 4 passing checks, no reviewer requested and no reviews. CI also passes on #474, which the earlier run had not checked.
  - The reworded grader bullet and ask are in section 2 of the drafts file.
  - Reviewer: the agents repo has no CODEOWNERS file. Since 1 Sep, commits under `overlord/src/workup-quality` are Laura DeWald 28, Sam Kariu 4, three others 1 each. Laura is on leave. I suggest Sam for the code and you for the method. A draft message to Jason, Sam and Rami is in section 3. It is not sent. Tell me the channel and say "send it" if you want it sent.

  ### Step 7: Workup Improvement Plan

  - Plan: https://app.notion.com/p/4188146861518179847fd617300bd320. Close-gates design, which sets the bar: https://app.notion.com/p/41881468615181a9b025c5b0adafb15f. Neither has changed since 16 Nov.
  - The 1-in-6 figure is confirmed. "15 at 90%" means 14 of 15. A setting right 80% of the time passes with probability 16.7%. At 75% it is 8.0%, and at 70% it is 3.5%. The bar reads "15 or more", so repeated checks raise those odds.
  - A stricter bar: 45 of 50 lets an 80% setting through 4.8% of the time. For the 95% lower bound itself to reach 90%, it takes 58 of 60.
  - The design doc lists "Is 15 at 90% the right unlock bar? It is a guess" as an open question, so the comment answers a question the author asked.
  - The clash is real in the text. The plan says "Don't widen merges or auto-closes" until items 1 and 2 are live. The Q4B notes (https://app.notion.com/p/41681468615181a58ce7f5765e5b811a) have "Actioning — support Messaging: Dmitry's 1–2 wk closing-expansion; start with config closes".
  - The draft comment is in section 4. It is not posted. The "three tickets still closed as duplicates" line comes from the 30 Oct audit (MSG-6531, MSG-6602, PMS-11426). I did not re-check their status today.

  ### Step 8: TOOL-838

  - TOOL-838 (https://linear.app/canary-technologies/issue/TOOL-838/workup-stop-copying-investigate-plugin-rules-into-the-agents-repo) is still in Backlog, unassigned, and unchanged since 9 Oct.
  - A draft comment proposing steps 1 and 3 as a precondition for the Orbital parallel validation is in section 6. It is not posted. The same point is added to the Orbital feedback as a line under ask 1.

  ### Not done

  - No Slack, Notion, Linear or GitHub writes.
  - No replay test of the second pass.
  - No refresh of the mirror. The data ends 22 Nov.
  - `NOTES.md` in the workup_accuracy folder has a new "Confidence check" section pointing at the scripts and drafts.

  ## Agent run 2026-11-25T13:25:09Z

  Follow-up asked in session: check Jason's test, look up the three old tickets, plan the experiment. Nothing was sent, posted, filed or run. Full text is in sections 7 and 8 of the same drafts file.

  ### The three flagged tickets

  - MSG-6531 (https://linear.app/canary-technologies/issue/MSG-6531/create-hotsos-valet-retrieval-tickets-from-guest-calls-or-texts): still Duplicate, of VOX-4247.
  - PMS-11426 (https://linear.app/canary-technologies/issue/PMS-11426/check-in-pms-sync-failure-for-cards-to-hotelkey): still Duplicate, of ENT-7708.
  - MSG-6602 (https://linear.app/canary-technologies/issue/MSG-6602/cannot-save-concierge-engagement-message-html-due-to-unrecognized): no longer closed as a duplicate. It was reopened to Triage on 6 Nov, 22 days after the close, and is now Done.
  - So "three still closed" is now two. MSG-6602 is a better example: the plan's 14-day window would have scored it as a good close. The Notion comment draft is updated.

  ### Method review of agents#473 and #474

  I read both descriptions, both docs, `replay/room.ts`, and the changes to `scripts/workup-replay.ts` and `replay/drive.ts`. I did not read the tests, the case files or `sim/score.ts`, and I ran nothing.

  agents#473 (https://github.com/canary-technologies-corp/agents/pull/473):
  - The next step is not judged. The room's bucket is matched against the stored answer from production's next-step judge. Only the cause is re-graded. The earlier line "the same two judges score it" was wrong.
  - The two sides are treated differently. The room's raw bucket is compared with production's bucket after the plugin's `declare` remapped it. This is TOOL-838 step 1, now with a concrete case.
  - The protocol uses about 40 tickets. With one ticket in four flipping on a re-run, that is roughly plus or minus 15 points. It can catch a broken room and cannot show "no worse".
  - The 40 are picked from tickets with no evidence gaps, which is the easy end.
  - Stages 0 to 5 are frozen, as the earlier run said. The Verifier's output is recorded and never read.
  - Correction: a `judgeVersion` hash is stored per ticket and the compare script warns on a mismatch. My 24 Nov note said the judge version was not stored.

  agents#474 (https://github.com/canary-technologies-corp/agents/pull/474):
  - It tests rules and plumbing. The authoring guide requires the answer to be reachable from clean evidence, so 11 of 11 is a floor.
  - `truth.json` sits in the folder the room reads. The only guard is telling each seat not to open it.
  - There are 11 cases by one author, who is building the system under test. Three of them tempt towards "Canary must act", our largest real error.
  - There is no baseline run of today's Workup or of a room on the corpus.
  - It pins the plugin at canary `72310a5` and copies the hypothesis-v1 reader. This is TOOL-838 step 3.

  Asks before the parallel run: report the room's driven bucket and require `--drive` on imports, run the next-step judge on a sample of room answers, use 150 or more tickets including ones with gaps, and move `truth.json` out of the room's folder. The reviewer message draft (section 3) now carries the three main points.

  ### Second-pass experiment plan

  - My earlier $600 figure was wrong. The replay harness cannot gather new evidence, and its debate costs about $0.55 a ticket (from `overlord/docs/WORKUP_REPLAY.md`).
  - Test A, thinking again over the same evidence: replay the 249 medium tickets and 100 high ones as a control, twice, with `--drive`. About $420 in total. A win is medium improving by 8 points or more, and by more than the control. It needs your OK to spend and read-only `OVERLORD_DB_URL` access, because transcripts are not in the local mirror.
  - Test B, a second investigation with new evidence: this cannot be done on past tickets. It needs a forward shadow test by the TOOL team, about 140 pairs in four weeks for about $1,700.
  - Order: A first. Its result decides whether B is worth a ticket.
  - A free check found no natural experiment: only 6 tickets since 21 Sep have two declarations.
project: null
source_id: null
tags: []
time_minutes: null
title: 'Workup accuracy: next steps from the confidence check'
updated: 2026-11-25 15:25:09.000000
waiting_on: null
waiting_since: null
working_on: false
---

Finding (24 Nov, local mirror snapshot workup-20261123-080952Z, 711 graded declarations, 21 Sep to 22 Nov):
Workup's stated confidence predicts being wrong. High: next step right 230 of 439 (52%). Medium: 81 of 249 (33%). Evidence-gap signals (tool gaps, budget exhaustions) predict nothing.
Hand off is the de facto "not sure" box: 35% of medium-confidence tickets go there and are right 22 of 87.
"Ask for more info" was the right answer on 13 of 711 (2%); Workup's asks were right 0 of 33.

Next steps:
1. Cost a second investigation pass on medium-confidence runs. Being unsure is mostly about the cause.
2. Report medium-confidence hand-offs separately on the dashboard, so they stop dragging the Hand off number.
3. Propose gating auto-actions on high confidence (config 66%, no-action 70%; still short of the 90% bar).
4. Re-run the confidence cut on blind-graded rows only, to confirm it holds.
5. Fix the talking points: remove item 5 (request-info as note) and item 8 (name an owner). Add the confidence finding.
6. Orbital feedback: reword the grader bullet. Jason's agents#473 and #474 reuse today's judges, are unreviewed since 22 Oct, and test only the last two stages. Find a reviewer.
7. Raise on the Workup Improvement Plan (Notion): the unlock bar (15 actions at 90%) passes by luck about 1 time in 6; audit closes that stayed closed; reconcile "don't widen" with Actioning for Messaging.
8. TOOL-838 steps 1 and 3 as a precondition for Orbital parallel validation.

Scripts: scratchpad conf.py (session c4f4563f). Notes: backend/canary/tmp/data/workup_accuracy/NOTES.md