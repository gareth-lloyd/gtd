---
area: null
completed_at: 2026-11-20 14:32:23.488058
contexts: []
created: 2026-11-19 20:41:39.654167
defer_until: null
due: null
energy: low
id: 2026-11-19T2041-choose-whether-to-do-tool-962-or-tool-937-based-on
order: null
output: |
  ## Agent run 2026-11-19T20:43:45+0200

  **Recommendation: do TOOL-937 first, then TOOL-962.**

  - TOOL-937, stricter duplicate rule: https://linear.app/canary-technologies/issue/TOOL-937
  - TOOL-962, grade "does Canary act" and "who acts" separately: https://linear.app/canary-technologies/issue/TOOL-962

  ### Why 937 first

  1. **Its main weakness can now be fixed for free.** The wording was tuned on the same 61 pairs it was scored on. Workup has declared 39 new duplicates since 10-31, none audited, and the ticket's own test asks for at least 30.
  2. **The problem hasn't gone away.** No duplicate-rule change has shipped in canary-agents since the ticket was filed. On the judged duplicates since 10-31, the judge agrees on 5 of 18 and says Canary had config, ops or code work to do on 9 of 18. Earlier periods were 7 of 15 and 5 of 17.
  3. **Someone is waiting on it.** TOOL-998 (https://linear.app/canary-technologies/issue/TOOL-998, Blocked, Sam Kariu) asks whether to widen duplicate auto-close for Messaging, and names the 937 finding as the check on revert rate.
  4. **Laura has already agreed the shape.** Her 11-03 comment on TOOL-937 backs the third rule as a separate field, and drops "the target must carry live work". Your reply proposed `drops_work` plus `drops_work_reason`. She hasn't replied since you shared the 68 pairs.
  5. **It changes what Workup does.** 962 changes only what we measure.

  ### The case for 962, and why it loses

  962 covers the larger error class. Using buckets as a rough proxy, 37 of 85 judge disagreements since 11-03 sit on "does Canary act" or "who acts" (125 of 272 before). Duplicates touch 19 of 85: 12 wrong declarations and 7 misses.

  But 962 is a metric, so it fixes none of those errors by itself. It has no comments and nobody waiting. Its cheap test also needs you to label 30 tickets blind. One thing raises its value later: TOOL-842 shipped on 11-13 (shadow first), so Workup will start closing working-as-designed tickets, and "said no when the answer was yes" becomes a dropped ticket.

  ### Fresh numbers (overlord DB, read-only, run today)

  | Period | Declared | Duplicates | Judged dups | Judge agrees | Judge says Canary work |
  | -- | -- | -- | -- | -- | -- |
  | 09-21 to 10-08 | 270 | 33 | 17 | 6 | 5 |
  | 10-09 to 10-30 | 314 | 38 | 15 | 2 | 7 |
  | 10-31 to now | 298 | 39 | 18 | 5 | 9 |

  | Judged tickets | Before 11-03 | Since 11-03 |
  | -- | -- | -- |
  | Total | 456 | 160 |
  | Agree with judge | 184 (40.4%) | 75 (46.9%) |
  | Workup says act, judge says no action | 32 | 15 |
  | Workup says no action, judge says act | 6 | 5 |
  | Workup escalates, judge says Canary acts | 31 | 10 |
  | Workup says Canary acts, judge escalates | 29 | 2 |
  | Workup escalates, judge says no action | 27 | 5 |

  "Act" means config change, ops action, code fix or feature request.

  ### Limits

  - The judge's bucket is a proxy. "Judge says Canary work" on a duplicate isn't the same as the audit's "harmful" label, so the harmful rate since 10-31 is unknown until the 39 are audited.
  - The bucket proxy for 962 undercounts. The 11-02 audit found 64 to 72 "said yes, was no" cases in 406 tickets by reading each one.
  - Humans labelled 7 of the 39 new duplicates and agreed on 6, which is a small counterweight.

  ### Suggested first step on 937

  Re-run `queries/q12.sql` and `q13.sql` for declarations from 10-31, then run the v2 blind re-read and the harm audit on those 39 pairs, unchanged. That gives an untuned result to post on TOOL-937 and to hand to TOOL-998. The uncommitted draft is in worktree `.claude/worktrees/workup-dup`, and it still needs reshaping to the `drops_work` field.

  Nothing was written to Linear or any other service. Queries are in the session scratchpad and weren't saved to the investigation folder.

  ## Agent run 2026-11-19T21:15:37+0200

  **Decision: TOOL-937 first, TOOL-962 after.**

  Draft comment for TOOL-937, not sent. Post it by hand, or ask for it to be sent:

  > Picking this up ahead of TOOL-962. Fresh numbers from the overlord DB, run 2026-11-19:
  >
  > | Period | Declared | Duplicates | Judged dups | Judge agrees | Judge says Canary work |
  > | -- | -- | -- | -- | -- | -- |
  > | 09-21 to 10-08 | 270 | 33 | 17 | 6 | 5 |
  > | 10-09 to 10-30 | 314 | 38 | 15 | 2 | 7 |
  > | 10-31 to 11-19 | 298 | 39 | 18 | 5 | 9 |
  >
  > "Canary work" means the judge chose config change, ops action or code fix.
  >
  > What this says:
  >
  > * Workup has declared 39 duplicates since the audit, and none of them were used to tune the wording. That is enough for the fresh test the description asks for.
  > * No duplicate-rule change has shipped since this was filed, and the judge's disagreement rate hasn't fallen.
  >
  > The judge's bucket is only a proxy. It isn't the audit's "harmful" label, so the harmful rate on the 39 is unknown for now. Humans labelled 7 of them and agreed with Workup on 6.
  >
  > Next step: run the tuned wording and the harm audit, both unchanged, on those 39 pairs and post the result here. It should also give TOOL-998 a revert-rate estimate. The rule would then take the shape agreed above: a separate `drops_work` field, without "the target must carry live work".
project: null
source_id: null
tags: []
time_minutes: 5
title: choose whether to do tool-962 or tool-937 based on data
updated: 2026-11-20 14:32:23.488049
waiting_on: null
waiting_since: null
working_on: false
---