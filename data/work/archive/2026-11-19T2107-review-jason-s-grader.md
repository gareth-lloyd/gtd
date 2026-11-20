---
area: null
completed_at: 2026-11-20 15:26:22.891620
contexts: []
created: 2026-11-19 21:07:16.045491
defer_until: null
due: null
energy: low
id: 2026-11-19T2107-review-jason-s-grader
order: null
output: |-
  ## Agent run 2026-11-20T11:07:43Z

  I read the code of both PRs this time, not only the descriptions. I did not run either harness or its tests locally, and I posted nothing.

  - agents#473 (https://github.com/canary-technologies-corp/agents/pull/473), head 243b3ea8, +2,103 lines
  - agents#474 (https://github.com/canary-technologies-corp/agents/pull/474), head baf363db, +5,710 lines

  ### Verdict

  Both are careful plumbing and safe to merge: they add scripts and tests, and touch no cron, SQL or judge prompt. The problems are about what the numbers will mean, not about the code. #473 can make Orbital look better than it is in two ways (below). #474 keeps the answer key in the folder the room works from, and its cases look too easy to separate Orbital from production.

  ### State (corrects the note in the body)

  - CI passes on both PRs, including #474 (dashboard, orbital-access, overlord, overlord-image-boot).
  - Both merge cleanly into current main and into each other (checked with git merge-tree).
  - Still no reviewer, no review, no Linear ticket. Last commits 26 Oct. The only comments are Jason's own.
  - I found no results from running either harness in the PRs. I did not search Slack.

  ### #473: scoring an Orbital room with the replay judges

  What holds up:
  - The judge is the production one. Each ticket gets two calls with the identical prompt, few-shot block and model: one on the original posted diagnosis, one on the room's report. That paired comparison is sound.
  - The docs set a protocol: about 40 tickets, two baseline runs first for a noise floor (they quote about 1 in 4 tickets flipping on re-synthesis, and 86% judge self-agreement).
  - Bad or missing room files become per-ticket errors, not crashes. 1,258 lines of tests.

  Findings, most important first:

  1. A room can skip the cause judge by declaring no hypothesis. A valid zero-hypothesis report (push-back or request-info) is never judged and is left out of the improved/regressed tally (room.ts `readRoomRun`, `importTallies`). Every original in the pool did offer a hypothesis. So a room that abstains on the hard tickets is compared only on the easy ones. The count is printed (`causeNotScored`) but the headline tally ignores it. Ask for abstentions to be shown against the original's verdict, e.g. "abstained where production was correct" counted as a regression.
  2. More hypotheses score better, and nothing caps them. The judge prompt gives `correct` when the resolution confirms "one of the diagnosis hypotheses". The import only requires one cause line per hypothesis. A room that lists more candidates than production gets an easier `correct`.
  3. report.md and hypothesis.json are not checked against each other. The cause judge reads the report. The bucket score and the driver read the JSON. The only cross-check is zero versus non-zero hypotheses, so the two files can name different causes. The `ticket` field inside hypothesis.json is not checked against the folder name either.
  4. Pinning the model does not pin the judge. The judge version hashes the template, the few-shot block and the model. The few-shot block is the six most recent human-labelled examples, so it changes whenever someone adds feedback. The PR description says pinning `WORKUP_JUDGE_MODEL` keeps the judge identical; that is only true if no feedback is added between runs. The paired tally is unaffected (both sides share one prompt). The "against the stored verdict" tally and comparisons across run directories are affected. The compare script does warn on a version mismatch.
  5. A ticket imported too early is stuck. If the room has not finished a ticket when the import runs, the ticket is stored as `skipped`, and `needsRerun` never retries a skipped ticket. A later import into the same `--out` silently keeps the stale result. Same for a report the room later rewrites. Workaround: a fresh `--out` each time. Worth a line in the docs or a fix in resume.ts.
  6. The next-step score is not a judge call. "Needed bucket" is the stored result of the next-step judge on the original run; the room's bucket is compared to it by equality. That is cheap and fine, but it is anchored on what the judge decided after reading production's diagnosis.

  Limits that this PR inherits and does not create:
  - The resolution evidence is the human comments posted after production's diagnosis. Those comments often react to that diagnosis ("confirmed", "no, it was X"). A room that is right in a different way is harder to confirm. This tilts toward production.
  - Stages 0 to 5 are frozen from the production run, as the earlier note said. I confirmed it in the code: the room gets the files production gathered, with production's conclusions stripped.

  ### #474: simulated cases with a mechanical scorer

  What holds up:
  - The scorer is deterministic and names the failure per case (red herring picked, right cause wrong bucket, asked the reporter when it should have acted).
  - Cases are validated hard: synthetic ids only, every cited file must exist, hashes match. The PR says each planted truth also passes the plugin's own `pipeline declare`.
  - A later commit added `--evidence-root`, so citations can be checked against only what the model was shown.

  Findings, most important first:

  1. The answer key sits beside the exam. `generate` writes `truth.json` into the same `<TICKET>/` folder the room reads its evidence from (generate.ts line 393). The only guard is the doc line "tell every seat not to open truth.json". Without `--evidence-root`, a citation of `truth.json` even counts as a valid citation. Ask for truth to be written to a separate directory by default.
  2. The cases look too easy to tell systems apart. I read two of the eleven in full (reminder-parent-disabled, ask-retry-failed-post). Each has five small gatherer results and one to four check claims, and a check or finding states the mechanism almost word for word. Real tickets fail on noise and missing evidence. I expect both production and Orbital to score near the top, which would show nothing. This is my judgment from two cases, not a measured result.
  3. Owner scoring tests reading a file, not routing. Owner must equal the truth exactly, and the truth comes from a made-up two-team policy (`team:triage`, `team:pms-gateway`) written into every case as `routing-policy.json`. That file was added on 26 Oct, after the first version. The 2 Nov accuracy work found the real errors are "does Canary act" and "who acts". The sim does not measure the second one.
  4. Eleven cases, one run each. One case is 9 points. The scorer has no notion of repeat runs, and the rooms are not deterministic. Ask for N runs per case and a pass rate.
  5. Coverage gaps. No case has bucket 4 as the answer. Eight of eleven cause categories appear. One push-back case, one short-circuit case.
  6. Object matching is loose in places. The declared object passes if it contains every `object_terms` entry as a substring. For pushback-no-hotel the terms are "reservation" and "hotel"; for request-info-on-hypothesis, "confirmation" and "reservation". Almost any request would pass.
  7. Short-circuit and push-back are self-reported. They come from the room's own `run-summary.json` when present. The scorer cannot see whether a debate actually ran.
  8. The hypothesis-v1 schema is already two copies that differ. answer.ts copies #473's schema with a comment saying to keep them identical. #473's later commit added a rule (evidence path required except on a zero-hypothesis request-info) and provenance fields that the sim copy lacks. A file can pass the sim and fail the import.
  9. Vocabularies are copied from canary at commit 72310a5 (gatherer names, check classes). Nothing will flag it when the plugin changes.

  ### Suggested bullet, revised

  > The test harness for Orbital is unreviewed. Jason's two PRs (agents#473, agents#474) have been open since 22 Oct with no reviewer. They reuse today's judges and test only the last two stages, on evidence production already gathered. As written, a room can avoid being graded on a ticket by declaring no hypothesis, and the simulated cases keep the answer file in the room's working folder.

  ### If you want to post review comments

  I would post findings 1, 2 and 5 on #473 and findings 1, 2 and 8 on #474. They are not drafted as GitHub comments yet; say so and I will draft them for your approval.
project: null
source_id: null
tags: []
time_minutes: 5
title: review jason's grader
updated: 2026-11-20 15:26:22.891599
waiting_on: null
waiting_since: null
working_on: false
---

I found two pull requests, both in the agents repo, and they change what I told you. Jason did not rebuild the grader: he left the judges alone
  and built two things around them.

  ┌───────────────────────────────────────────────┬──────────────────────────────────────────────────────────────────┬──────────────────────┐
  │                      PR                       │                           What it does                           │        State         │
  ├───────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────┼──────────────────────┤
  │ agents#473, "Score an Orbital room's Workup   │ Feeds an Orbital run into the existing replay harness, so the    │ Open since 22 Oct,   │
  │ run with the replay judges"                   │ same two judges score it.                                        │ +2,103 lines         │
  ├───────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────┼──────────────────────┤
  │ agents#474, "Add simulated Workup cases with  │ Adds 11 made-up tickets with a planted right answer, and a       │ Open since 22 Oct,   │
  │ a mechanical scorer"                          │ scorer that checks the result with no AI judge.                  │ +5,710 lines         │
  └───────────────────────────────────────────────┴──────────────────────────────────────────────────────────────────┴──────────────────────┘

  Both have no reviewer requested, no reviews, no Linear ticket, and no commits since 26 Oct. CI passes on #473; I did not check it on #474.

  What matters for your feedback

  - The judges are unchanged. Both PR descriptions say judge prompts, SQL and the cron are untouched. So Orbital's scores can be compared with
    today's, if the judge model is pinned.
  - The pin is manual. The judge version is not stored per ticket. "Same judge" depends on setting WORKUP_JUDGE_MODEL the same for each run.
  - Orbital is only tested on the last two stages. The harness freezes stages 0 to 5 from the production run and hands Orbital the gathered
    evidence. A good Orbital score says nothing about gathering.
  - The simulated cases are a new, second test. There are 11, all written by hand by the person building the system under test. The scorer checks
    cause, bucket, owner and whether it asked the reporter when it should have acted.
  - Nobody has reviewed either. That part of my earlier point stands.

  Suggested rewording of the bullet

  ▎ The test harness for Orbital is unreviewed. Jason's two PRs (agents#473, #474) have been open since 22 Oct with no reviewer. They reuse
  ▎ today's judges, but only test the last two stages, on evidence production already gathered.

  I read the PR descriptions and file lists, not the code. I did not find any results from running either harness, and I did not search Slack
  this time. The earlier GTD run said the rebuilt eval was in no PR, which was wrong.