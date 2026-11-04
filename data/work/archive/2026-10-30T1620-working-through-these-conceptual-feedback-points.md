---
area: null
completed_at: 2026-11-04 16:42:54.896221
contexts: []
created: 2026-10-30 16:20:41.252179
defer_until: null
due: null
energy: null
id: 2026-10-30T1620-working-through-these-conceptual-feedback-points
order: null
output: |-
  ## Agent run 2026-11-02T14:45

  I checked each claim against the 10-30 exports (q2.csv, since 09-21). Two cheap analyses change the picture. Script: /private/tmp/claude-501/-Users-garethlloyd-projects-canary/bc52282a-2b66-4300-b428-3eb81b651fac/scratchpad/concept.py. No agent, Linear or other external changes were made.

  **Claims that hold**
  - Score misses the harm: 14 of 17 harmful blocked by v1, and -0.2 points for v1 and v2 (NOTES.md).
  - 20 of 59 missed duplicates had targets that did not exist yet.
  - Ceilings since 10-09: 2.4 points for duplicates, 4.3 for no-action, and they overlap.
  - Churn: 36 plugin versions over 573 tickets, plus 20 with no version. The median is 13 tickets per version, so it is a bit worse than "about 16".

  **Noise floor: a rough proxy already exists, and it is about 75%**
  - On the 69 tickets that have both a human label and a blind judge grade, human and judge agree on 52 (75.4%, kappa 0.70).
  - On the same 69 tickets, Workup agrees with humans 65.2% of the time and with the judge 52.2%.
  - Caveat: all 85 human labels came after the declaration, so humans saw Workup's answer. Workup agreeing more with humans than with the judge fits that anchoring. Labelled tickets also look easier. Treat 75% as an optimistic ceiling.
  - So "60% is near the limit" is too strong. It is roughly 10 to 15 points under the human ceiling, and the 40.5% judge score is about 35 points under it.
  - The review is right that most of the 59.5-point gap can't be won. But the named ceilings add up to well under 10 points, so most of the winnable gap has no diagnosis yet.

  **Taxonomy: the data supports the split strongly**
  - Workup and the judge disagree on 233 of 388 blind-graded tickets. Only 50 of those disagree within "what work is needed" (config, ops, code or feature), the boundary next-steps.md spends the most effort on.
  - 183 disagree across questions. 114 of those pair labels that could both be true at once: work and already tracked, work and who acts, or work and do we know enough. The other 69 are real conflicts, with one side saying nothing is needed. 22 of those are Workup Hand off against judge no-action, which the hotel/vendor rule partly covers.
  - That gives an upper bound: up to about half of all disagreement may come from the single label, not from wrong diagnosis. It is structural only. I did not read tickets to confirm both labels were true.
  - Split alone won't close the gap. Scored only on which question was answered, Workup agrees with the judge 52.8% of the time, against 81.2% for humans. Workup often answers a different question from the reviewers, which is a real problem as well as a scoring one.

  **My view on the suggested order**
  1. Keep the blind relabel, but it no longer gates everything. The 75% proxy already shows a large winnable gap. The relabel mainly removes the anchoring bias. Labelling has nearly stopped (5 of 84 tickets in the latest week, per the 10-30 run), so it needs a named owner and time.
  2. Move the label split up. It is the only lever sized to explain a large share of the gap. A cheap first step: re-score past data at question level with multi-label credit, before changing the agent.
  3. Change the target: agreed. The harm audits (22 of 68 duplicates and 18 of 39 no-actions would drop a real problem) are the evidence that agreement is the wrong number.
  4. Replay harness and slower releases: agreed. At 13 tickets per version, no wording change, TOOL-937 included, can be proven in production.
  5. TOOL-937 (https://linear.app/canary-technologies/issue/TOOL-937): pausing patches doesn't need to block it. The draft branch `glloyd/workup-duplicate-drop-test` is still uncommitted. It is the first candidate the replay harness should prove.

  **Open decisions for you**
  - Who does the blind relabel, and is 50 tickets enough? It is enough to compare 75% with 60%, but not to give per-bucket numbers.
  - Is "question answered" (the five questions in the review's table) the right split to score, or should cause stay a separate axis?
  - Should this go to the Workup/TOOL owners as a write-up? I have not drafted or sent anything.

  ## Agent run 2026-11-02T15:20, taxonomy deep dive

  Data: blind-graded tickets since 09-21 (q2.csv, n=388) and 85 human labels. Sources: next-steps.md (plugin, last changed 10-28) and next-step-judge.md (canary-agents origin/main). Script: /private/tmp/claude-501/-Users-garethlloyd-projects-canary/bc52282a-2b66-4300-b428-3eb81b651fac/scratchpad/tax.py. No external writes.

  **1. The taxonomy is already several questions, and each side ranks them differently.**
  - Workup checks in order: push-back (do we know enough?) → strong duplicate (is it tracked?) → ceiling (who acts?) → short-circuit → cause mapped to a step (what work?).
  - The judge checks: duplicate → unanswered ask → routed to product → working as intended. It then scores "the PRIMARY step that resolved the report".
  - The orders differ, so some disagreement comes from two different decision rules, not a wrong diagnosis.

  **2. Cause sets Workup's bucket, and the overrides are where the raters split.**
  - 262 of 375 declarations are just the cause mapped to its default step.
  - Against the judge, that default alone scores 43.7%, against Workup's 41.3%. On the 113 overrides, Workup is right 23 times and the default 32.
    - Request-info: Workup right 1, default right 8.
    - Hand off: 11 against 14.
    - Duplicate: 8 against 5.
  - Against humans the overrides win: 14 of 26, against 2 for the default.
  - On the 66 tickets graded by both, humans back the override 10 of 18 times and the judge 6 of 18.
  - The raters disagree most where a question other than "what work" takes priority. That is direct evidence that the single label is the contested part.

  **3. "Code fix" means a different thing to each side.**
  - Judge: 50 of 53 code-fix verdicts have a linked PR, so in practice it means "a PR exists".
  - Workup: it means "a code bug proven at high confidence".
  - Of 88 `code_bug` causes, the judge scored 17 as config-change. That fits a config workaround resolving the ticket while the bug stays.
  - That is an axis the review missed: the fix for this ticket versus the fix for the cause.

  **4. Hand off is a catch-all, and "who acts" is mostly empty.**
  - Of 86 Hand offs, the judge said: hand off 24, no action 22, config 12, duplicate 9, code 8, ops 8.
  - `owner` is set on 83 of 388. Scoring "who acts" separately needs Workup to fill it in first.

  **5. A split needs a new ground truth.**
  - The judge emits one bucket and drops the other questions through its primary-step rule. The existing data can't score the axes separately.
  - The only partial axis today is cause, and the judge doesn't grade cause.

  **6. A replay harness already exists.**
  - TOOL-743 (side-by-side prompt replay) and TOOL-909 ("build the debate taxonomy from a plugin checkout") are in canary-agents. I haven't checked whether they replay the declaration step. If they do, the review's step 4 is partly done.

  **Proposed shape (for discussion):**
  - **Tracked:** links to tickets, never a close by itself.
  - **Needed:** does Canary need to act? Yes, no or unknown.
  - **Who acts:** Canary team, hotel, vendor or reporter.
  - **What work:** config, ops, code or feature, split into the fix for this ticket and the fix for the cause.
  - **Enough evidence:** yes, or the specific missing input.
  - **Cause:** as today.
  - Score each axis only where the evidence answers it. Derive the Linear "Next Step" label from the axes with one published order that the plugin and the judge share.

  **Next step needs read access:** to test the "both labels true" upper bound (114 of 233), read the judge reasoning and evidence quote, Workup's specific object and the human notes for a stratified sample of about 40. Then pilot a judge that answers each axis on about 60 tickets.

  ## Agent run 2026-11-02T16:10, taxonomy audit of all 240 disagreements

  Data: the overlord DB, read-only through ~/.overlord-db-url (you approved this session). 406 blind-judged declarations since 09-21, 240 of them disagreements, with judge reasoning, Workup's declared object and human notes. Four AI readers each took 60 rows and read every one. Files are in backend/canary/tmp/data/workup_accuracy/: exports/q14_disagreements.csv, audits/tax_audit_[0-3].csv, scripts/tax_audit_summary.py. NOTES.md is updated. No external writes.

  **Headline: about half the disagreement comes from the single label.**

  | Relation | Tickets |
  |---|---|
  | Both labels true | 103 |
  | Same facts, different ranking rule | 23 |
  | Workup wrong | 99 |
  | Unclear | 14 |
  | Judge wrong | 1 |

  - Agreement is 40.9% strict, 66.3% counting both-true as right, and 71.9% counting ranking differences too.
  - Real Workup errors are about 24% of graded tickets, not 59%.
  - That puts Workup near the judge's own noise. The replay harness doc reports the judge agreeing with itself on 86% of tickets.

  **Where each step stands**
  - Request-info is the worst: 18 of 23 wrong. On 19 of the 23, the missing input was not blocking, and engineers fixed the ticket without it.
  - Code-fix: 17 of 29 wrong, mostly config or intended behaviour.
  - Hand off: 28 both true, 14 ranking (unproven bug sent to its own team, which then fixed it), 18 wrong.
  - Duplicate as the judge's answer: 16 of 17 both true. Workup found something true, and the ticket was also tracked. That supports a duplicate being a link, not the label.
  - No-action and feature-request declared by Workup are mostly both true (10 of 13 and 10 of 15).

  **Agreement on each question (within the 240, where both sides are known)**

  | Question | Agree | Main miss |
  |---|---|---|
  | Already tracked | 83% of 229 | Workup missed a tracked ticket 29 times |
  | Does Canary need to act | 58% of 182 | Workup said yes, actual no: 64. The reverse: 13 |
  | Who acts | 44% of 228 | Workup said Canary, actually the hotel 38 and nobody 29 |
  | What work | 20% of 158 | Many "none" against a declared step |

  - The fix for this ticket differs from the fix for the cause on 49 of 240 (20%). That axis is real.
  - The real errors cluster on "does Canary act, and who acts". Workup over-claims Canary work about 5 to 1. That costs wasted effort more than dropped problems, which the earlier harm audits didn't measure.

  **What this means for the taxonomy**
  1. **Split the label.** Score "tracked" as a link, "does Canary act", "who acts", "what work" for this ticket, "what work" for the cause, and "missing input" as separate fields. The Linear label becomes a derived summary with one ranking that the plugin and the judge share.
  2. **Make request-info a flag, not a step.** Declare a best-guess step plus "would help: X". As a standalone step it is 5 of 23 right.
  3. **Prioritise "does Canary act / who acts".** It holds most of the real errors, and it decides both kinds of harm. It should be the headline metric, scored for both directions of error.
  4. **Unproven code bug sent to the owning team** is a ranking rule, not a step. It accounts for most of the 23 ranking cases. Report it as an abstention with the best-guess work type attached.

  **Caveats**
  - One AI read per ticket, with hindsight. The readers almost never blamed the judge (1 of 240), which may be deference.
  - "Both true" is a generous reading. A true but secondary aspect is not always a useful next step.
  - The 166 agreements were not audited per question, so these question-level rates cover the disagreements only.
  - Worth a human check on about 20 rows across the relation types before using the 66% figure outside this item.

  ## Agent run 2026-11-02T16:40, proposals drafted

  Your decisions this session: TOOL-937 (https://linear.app/canary-technologies/issue/TOOL-937) goes ahead as filed. You will do the spot check. The output of this work is proposals for TOOL, not code.

  **Spot check sheet:** backend/canary/tmp/data/workup_accuracy/audits/spot_check.md. 20 rows, stratified: 7 both true, 4 ranking, 6 Workup wrong, 2 unclear, 1 judge wrong. Each has a Linear link, both sides' steps, the judge's reasoning, the audit verdict and blanks for your verdict.

  **Proposal drafts** (local, not shared), in backend/canary/tmp/data/workup_accuracy/proposals/, in the TOOL-937 hypothesis format:
  - 00-overview.md: the evidence and the order.
  - 01-request-info-as-note.md: request info is right on 1 of 27 graded. Make it a note on a best-guess step. Plugin only.
  - 02-align-plugin-and-judge.md: one shared ranking, and report an unproven bug as an abstention.
  - 03-score-by-question.md: the judge answers each question. Lead with "does Canary act" and "who acts", scored for both directions of error.
  - 04-multi-step-declaration.md: a list of work steps plus links, missing input and "nothing needed". Tested against proposal 3's ground truth.

  **Next:**
  1. You fill in spot_check.md. I update the proposal numbers if verdicts move.
  2. You choose how to share: Linear tickets like TOOL-937, a Notion doc, or a Slack post. Nothing is posted until you approve the exact text.

  ## Agent run 2026-11-02T17:20, second independent audit

  A second AI audit, prompted differently and blind to the first, graded each label separately as useful, true but secondary, or false. It also picked the step that would most have helped. 239 of 240 graded: MSG-6755 was skipped. Files: audits/tax_audit2_[0-3].csv and scripts/tax_audit_compare.py. A blind spot-check sheet now exists: audits/spot_check_blind.md (fill this one in; spot_check.md is the key).

  **The two audits agree.**
  - On whether Workup's step is true of the ticket: 91% (kappa 0.81).
  - On the facts: tracked 92%, Canary acts 98%, who acts 94%, work 83%.
  - They share a model, so this shows consistency, not correctness. Your spot check is still the only human check.

  **The headline changes.** The first audit's "both true" was mostly "true but not useful".

  | Workup's step on the disagreements | Tickets |
  |---|---|
  | True and useful | 36 |
  | True but secondary | 85 |
  | False | 110 |
  | Unclear or missing | 9 |

  - Of the first audit's 103 "both true", 23 are useful and 69 secondary.
  - Agreement: 40.9% strict, 49.8% counting useful, 70.7% counting secondary too.
  - With hindsight, the most useful step matched the judge's on 201 and Workup's on 26. Hindsight favours the judge, which reads the resolution.

  **What holds**
  - "Does Canary act" errors: 72 said yes when it was no, 15 the reverse.
  - "Who acts": 42% agreement.
  - Request-info: false on 19 of 22. The input was not needed on 20 of 22.

  **Proposals revised** in proposals/:
  - The overview leads with the second audit.
  - 01 and 03 cite both audits and are stronger.
  - 04 (several steps) is marked weaker: only 36 disagreements had a useful second step.

  The single label costs about 9 points (36 of 406), not 25. Most of the gap is real errors about whether Canary acts and who acts.

  ## Agent run 2026-11-02T17:45, alignment ticket drafted

  Draft ticket, scoped only to aligning the plugin and the judge: backend/canary/tmp/data/workup_accuracy/proposals/02-ticket-draft.md. It is in the TOOL-937 format. Not filed.

  Evidence it uses:
  - Team-owned or `code_bug` hand offs since 09-21: the judge agrees on 4 of 31. Since the 10-23 rename it agrees on 3 of 11. Hotel- or vendor-owned hand offs: 4 of 6 since 10-23, plus 1 counted as matched.
  - The plugin and the judge rank the questions differently, and their duplicate tests differ.
  - The definitions are synced by hand across three copies, including replay/taxonomy.ts.

  Proposed changes:
  1. An unproven `code_bug` becomes a best-guess work step with `proven: false`, still routed to the owning team.
  2. One ranking written in next-steps.md.
  3. The plugin becomes the single source for the judge's definitions.

  Correction: owners have been set on every hand off since 10-23, so I dropped a "require owner" change.

  ## Agent run 2026-11-03T07:25, TOOL-937 reply posted

  With your approval, I posted a reply to Laura DeWald's comment on TOOL-937 (https://linear.app/canary-technologies/issue/TOOL-937) and attached dup_audit_share.csv (68 audited duplicate pairs with labels and re-read decisions; source: backend/canary/tmp/data/workup_accuracy/audits/dup_audit_share.csv).

  Laura's points, all accepted in the reply:
  - Auto-close is safe (2 of 13 wrong). The audit also has exactly 2: MSG-6531 and PMS-11426.
  - The "dropped work" rule becomes its own field. The reply suggests `drops_work` plus `drops_work_reason`, with `same_mechanism` unchanged.
  - Drop "the target must carry live work" (8 of 22 open targets were fine). Narrow it to "a closed target with no fix".
  - She asked for the 68 pairs: attached.

  Waiting on Laura to compare the labels with what happened in Linear. The draft branch glloyd/workup-duplicate-drop-test still uses the old wording (same_mechanism and "live work"). It needs updating if TOOL wants the draft.

  ## Agent run 2026-11-04T13:55, TOOL-962 filed

  Filed proposal 1 (grade "does Canary act?" and "who acts?" separately) as a Backlog ticket in TOOL: https://linear.app/canary-technologies/issue/TOOL-962/hypothesis-grading-does-canary-act-and-who-acts-separately-would-show (related to TOOL-937). Local copy: backend/canary/tmp/data/workup_accuracy/proposals/03-ticket-draft.md. Narrowed from five questions to two, kept short.
project: 2026-09-08-workup
source_id: null
tags: []
time_minutes: null
title: working through these conceptual feedback points
updated: 2026-11-04 16:42:54.896213
waiting_on: null
waiting_since: null
working_on: false
---

Workup conceptual review, 2026-10-30. Context: TOOL-937 and `~/projects/canary/backend/canary/tmp/data/workup_accuracy/NOTES.md`. This is judgement from accuracy data. I haven't looked at whether engineers find Workup useful.

## Verdict

Mostly sound, but we're probably measuring the wrong thing. Gathering evidence, debating a cause and letting code enforce the rules looks right. The weak part is compressing each ticket into one of eight next steps and scoring that label.

## Is it conceptually sound?

Partly. Diagnosis suits an agent, and deterministic gates are the right check on it. But Workup assumes each ticket is one problem with one right next step.

- Many harmful duplicates were tickets with a second fault or a one-off request.
- Some wrong no-actions were expected behaviour that still turned up a real bug.

## Are we targeting the right things?

Probably not.

- The score misses the harm. The first duplicate wording blocked 14 of 17 harmful calls, yet judge agreement fell 0.2 points.
- The score rewards matching what people did. Saving engineers time and avoiding dropped problems would be better targets.

## Is the taxonomy correct?

No, but merging categories won't fix it. The eight buckets answer different questions:

| Question | Buckets |
|---|---|
| What work is needed? | config change, ops action, code fix, feature request |
| Who acts? | hand off |
| Do we know enough? | request info |
| Is it already tracked? | duplicate |
| Is anything needed at all? | no action |

A ticket can be both a code fix and already tracked, so one label creates disagreement no agent can resolve. The scoring already treats a hand-off to a hotel or vendor and a no-action as the same class, which suggests the same problem.

## Are these problems solvable?

Some are, but less than the 40.5% score suggests.

- Remaining gains are small. Since 10-09 the ceilings are about 2.4 points for duplicates and 4.3 for no-action, and they overlap.
- Some misses were unknowable. 20 of the 59 missed duplicates had targets that didn't exist yet.
- The noise floor is unknown. As far as I've seen, nobody has measured how often two people agree on these labels. If it's around 70%, the 60% agreement with humans is near the limit.
- Churn blocks measurement. About 35 plugin versions over 573 tickets leaves roughly 16 tickets each, so most fixes can't be evaluated.
- TOOL-937 is one more wording patch tuned on a small sample, though it's still worth trying.

## Suggested order

1. **Measure the noise floor:** have two people label the same 50 to 100 tickets blind. It's cheap, and it shows how much of the gap is winnable.
2. **Split the label:** score cause, already tracked, who acts and enough evidence separately. A duplicate then becomes a link rather than a closure, which removes much of the risk.
3. **Change the target:** weight dropped problems well above wasted effort, and track engineer time saved.
4. **Build a replay harness and slow the releases:** rerun past tickets against each change, so a fix can be proven before it ships.

Pause further accuracy patches until step 1 is done, because its result decides how much more of them is worth doing.