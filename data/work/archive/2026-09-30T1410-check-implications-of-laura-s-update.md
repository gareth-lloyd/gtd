---
area: null
completed_at: 2026-09-30 14:29:44.035041
contexts: []
created: 2026-09-30 14:10:49.109867
defer_until: null
due: null
energy: low
id: 2026-09-30T1410-check-implications-of-laura-s-update
order: null
output: |
  ## Agent run 2026-09-30 14:14:24

  Thread: Laura's shadow-mode update on judged duplicates, 2026-09-22 (https://canarytechnologies.slack.com/archives/C0AL1T2H43V/p1790092390082679)

  ### What the thread decided
  - Policy: when a ticket is expected behavior or a missing feature and an open ticket already tracks the change, Workup should call it a Duplicate of that ticket, link, and close (Blake). Mati: fine as long as it links.
  - Add-on: Workup should leave a comment on the TARGET ticket when it marks a duplicate, so the target's watchers see the new instance (Mati proposed, Blake and Laura agreed it is part of "executing the next step").
  - Closing, or duping against a closed ticket, is the most dangerous action and stays recommend-only for a while (Blake).
  - Mati wants to be tagged on every action Workup takes, at least for a while.
  - MSG-6265 correction: the right target was MSG-3694 (show detected language in header), not MSG-6100 (update stored preference after engagement). Mati confirmed and fixed MSG-3694's description on 09-24.
  - Unanswered in thread: Mati asked whether Linear notifies the target's subscribers when another issue is marked duplicate of it. Nobody answered. I have not verified Linear's behaviour either.

  ### Where the four cases stand today (2026-09-30)
  - MSG-6245 -> MSG-5865: correct, closed Duplicate.
  - MSG-6265 -> MSG-6100: on 09-28 re-resolved as Duplicate of MSG-3694 (https://linear.app/canary-technologies/issue/MSG-6265). Judge will see right bucket, wrong target. Still a miss.
  - PMS-10657 -> MSG-6066: Ian Clark closed it Done on 09-24 after finding the hotel's Hapi/OWS API returns SYS 81 errors and escalating to Hapi (https://linear.app/canary-technologies/issue/PMS-10657). Not marked duplicate, only related. Mati's "looks correct" on 09-23 predates Ian's resolution. Judge will grade this wrong bucket (human = escalate/vendor, Workup = duplicate).
  - MSG-6269 -> MSG-4075: Mati re-marked as Duplicate on 09-23. Correct.
  - Net: 2 of 4 graded wrong under the judge's human-resolution rule. The TOOL-708 auto-close gate is 15 declared with at most 1 wrong, so this batch alone already breaches it unless the judge is re-run after the re-resolutions and the gate is split by same-hotel/cross-hotel (it is). All four of these are cross-hotel judged duplicates against backlog improvement tickets, so they fall in the class TOOL-709 keeps label-only anyway.
  - Not verified: I could not read workup_declarations / workup_next_step_judgments (canary MCP servers failed to connect this session), so the actual verdict rows are unconfirmed.

  ### What the milestone already covers
  - TOOL-709 auto-close same-hotel duplicates behind a flag, In Review, agents PR #315 (https://linear.app/canary-technologies/issue/TOOL-709, https://github.com/canary-technologies-corp/agents/pull/315). Does relation + Duplicate state + a comment mentioning the on-duty triage person. Guards: target open, older, not itself, no human comment, ticket still in Triage. Cross-hotel stays label-only. Covers Blake's "closed target is dangerous" (target-open guard) and most of Mati's "tag me" ask (mention goes to whoever is on triage duty, not a fixed reviewer).
  - TOOL-756 grade auto-closed tickets by revert, In Review, agents PR #314 (https://linear.app/canary-technologies/issue/TOOL-756).
  - TOOL-745 code fix needs a verdict on every open candidate, In Review, canary PR #58298 (https://linear.app/canary-technologies/issue/TOOL-745). Came out of this thread's MSG-6269 case.
  - Judged-duplicate declare already rejects closed targets (next-steps.md, "a closed target means the problem came back"). Bucket 8 closes are not automated at all. So "recommend-only for closing" needs no new work.

  ### Gaps the thread opens that nothing tracks yet
  1. Comment on the TARGET ticket. TOOL-709 comments on the closed ticket, not the target. Mati's ask was the target. Either add a fourth write to TOOL-709 (a short comment on the target linking the new instance) or confirm Linear already notifies target subscribers on a duplicate relation, which Blake asserted and nobody checked. Also the bucket 7 completion_condition in next-steps.md ("the tickets linked") could name the target comment.
  2. Taxonomy prose. next-steps.md bucket 4 and 8 "Don't confuse with" columns do not mention bucket 7, and the judged-duplicate rule says "describes the same problem". The thread's decision is that a working-as-designed or not-implemented finding with an open ticket tracking the change IS bucket 7. Worth one sentence in next-steps.md and the Judged duplicate bullet in propose-hypothesis SKILL.md so the debate stops writing "expected behavior, see MSG-xxxx" as bucket 8. Labels unchanged, so no agents-repo mirror change.
  3. Adjacent-target precision (the MSG-6265 shape). Workup's own comment listed MSG-3694 under related tickets and still chose MSG-6100. TOOL-745's per-candidate same_mechanism verdict is scoped to code-fix declarations. Extending it to the duplicate path (for each open candidate: would shipping it make the reporter's complaint go away?) would have forced the choice between 3694 and 6100. Consider folding into TOOL-745 or a follow-up.
  4. Ground truth drift. Two of four cases were re-resolved by a human days after the first resolution. The judge grades against whatever the human did at tick time. TOOL-756 re-grades on history change for auto-closed tickets; check the label-only path re-grades too, otherwise MSG-6265 and MSG-6269 keep their first verdicts.
  5. Process ask, not code. The new policy only pays off if MSG/PMS engineers mark such tickets Duplicate rather than Done/Canceled with a comment. Otherwise the judge keeps counting Workup wrong on exactly the calls Blake said he wants. Worth saying to Mati and Jason explicitly.
  6. Fixed reviewer vs on-duty person. Mati asked to be tagged on every action. TOOL-709 tags the on-duty triage person. If Mati means himself specifically, a per-team reviewer override is a small addition; otherwise the on-duty mention is the answer and should be said back to him.

  Nothing was posted anywhere. No Linear, Slack, or code changes made.
project: null
source_id: null
tags: []
time_minutes: 5
title: Check implications of Laura's update
updated: 2026-09-30 14:29:44.035026
waiting_on: null
waiting_since: null
working_on: false
---

https://canarytechnologies.slack.com/archives/C0AL1T2H43V/p1790092390082679