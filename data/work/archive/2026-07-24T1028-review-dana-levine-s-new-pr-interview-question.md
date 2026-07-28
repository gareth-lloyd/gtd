---
area: null
contexts:
- consume
created: 2026-07-24 10:28:48.269976
defer_until: null
due: null
energy: medium
id: 2026-07-24T1028-review-dana-levine-s-new-pr-interview-question
order: null
output: |
  ## Agent run 2026-07-27T14:35:00+03:00

  Reviewed Dana's PR interview question end-to-end: read the sample PR
  (https://github.com/canary-technologies-corp-interviews/dana11235-at-gmail-com-availability/pull/3),
  the README, the planted ai-code-review.md, and game.ts; cloned the repo, ran the test
  suite (7 pass, 1 revealing skip), and empirically verified every planted bug with a probe
  script. Slack context: https://canarytechnologies.slack.com/archives/C09MAQZ9LEN/p1784757314642589

  ### Verdict
  Excellent question — the best-designed "AI-era" code review exercise I've seen. The core
  mechanic (adjudicate an AI review that mixes correct, wrong, overstated, and actively
  harmful comments, then find what it missed) tests exactly the skill we hire for now.
  Two real risks: delivery format (if take-home, the no-AI rule is unenforceable and any
  frontier model finds every planted bug in one paste — I effectively just demonstrated
  that), and the one-hour budget is tight for everything it asks.

  ### What's great (verified by running the code)
  - The planted AI review is the star. Comment 1 correct (inclusive `overlaps` bounds break
    half-open turnover). Comment 2 wrong and push-back-able (ISO date strings compare fine
    lexicographically; switching to Date parsing would ADD timezone bugs). Comment 3 is a
    devious trap: it tells you to make `occupancy` reuse `isAvailable`'s overlap-count —
    but `occupancy` is the CORRECT method; following the AI propagates the deep bug.
    Comment 4 (TOCTOU/locking) overstated for single-threaded in-memory JS. Comments 6-7
    invent requirements (case-insensitivity, cancelled status field that doesn't exist).
    Comment 8 generic filler.
  - Layered bugs the AI misses, all confirmed live:
    1. DEEP: `isAvailable` counts reservations overlapping ANY night of the stay against
       total rooms instead of taking the per-night PEAK. Two disjoint reservations block a
       2-room type for a spanning stay (verified: peak occupancy 1, but isAvailable false).
       This is why the game's par ($2,840) is unreachable.
    2. `availableRoomTypes` derives types from RESERVATIONS not inventory — empty hotel
       returns [] (verified).
    3. `upgradeOptions` offers DOWNgrades (suite guest offered double at quoted rate;
       verified: ['double','king']).
    4. `getReservations` leaks the internal array — external push changes occupancy
       (verified).
    5. Unanchored date regex (no ^$) + no reversed-date check: 'junk 2026-06-05 junk' with
       checkOut < checkIn is accepted (verified).
    6. `addReservation` never checks availability → overbooking (verified; arguably API
       design, since game.ts gates on isAvailable first — rubric should take a position).
  - The test suite is itself a review target: the one test that would catch the turnover
    bug is `it.skip`ped with a false "flaky" excuse (it's deterministic); the
    "keeps the room blocked on departure day" test asserts behavior CONTRADICTING the
    README's half-open convention (and contradicts the occupancy test in the same file);
    one test asserts only `toBeDefined()`. Style nits planted for calibration (`!=`,
    `total_rooms`, "avaliable" typo).
  - Game design is genuinely clever: the calendar renders via freeRooms/occupancy (correct
    per-night logic) while booking gates via buggy isAvailable — so the terminal visibly
    contradicts its own calendar, and the "par nobody can hit" mystery has a real cause.
    Rewards candidates who run the code without requiring it.

  ### Suggestions for Dana
  1. Format: run it live/synchronous (or as a discussion anchor in a follow-up call). As a
     take-home the no-AI constraint is honor-system only, and this question is exactly the
     shape LLMs ace.
  2. Time: adjudicating 8 AI comments + finding 2+ hidden bugs + playing the game is a lot
     for 60 min. Either extend to 90, cap the game ("10 min max"), or explicitly say
     depth-over-coverage is scored (README gestures at this already).
  3. Write an interviewer rubric mapping findings→levels before others run it: e.g.
     junior = comment-1 confirmation + nits; senior = per-night-peak bug + pushback on
     comments 2/3; staff = test-suite contradiction + requirements-conflict framing of the
     departure-day test. Also pre-decide the expected call on addReservation availability
     checking.
  4. Tiny: `nightsBetween` uses local-time Date math (DST off-by-one in some TZs) — fine as
     a bonus find since the game stays in June, but worth knowing it's there.

  ### Suggested Slack reply (NOT sent — for you to post in #blake-directs thread)
  "Ran through the sample PR properly (cloned it, played night auditor, probed the service).
  This is really strong — the ai-code-review.md mechanic is the best interview test of
  'use AI critically' I've seen, and comment 3 steering people toward breaking the one
  correct method is delightfully evil. The calendar-vs-terminal contradiction in the game
  explaining the unhittable par is great design. Three thoughts: (1) as a take-home the
  no-AI rule is unenforceable and frontier models find every planted bug in one paste —
  I'd run it live; (2) 60 min feels tight for 8 AI comments + hidden bugs + the game —
  maybe 90, or cap game time; (3) before other interviewers run it, a rubric mapping
  findings to levels (comment-1 confirm = junior bar, per-night-peak bug + pushback on
  comments 2/3 = senior bar, spotting the test-suite contradiction = strong) would keep
  scoring consistent. Happy to be a calibration data point with my own repo if useful."
project: null
source_id: https://canarytechnologies.slack.com/archives/C09MAQZ9LEN/p1784757314642589
tags:
- morning-gtd
- slack
- from-awareness
time_minutes: 20
title: Review Dana Levine's new PR interview question
updated: 2026-07-27 16:15:34.418426
waiting_on: null
waiting_since: null
working_on: false
---

First revision of Dana's new PR question in #blake-directs; sample PR linked, offer to generate you a repo to run the question yourself.
Sample: https://github.com/canary-technologies-corp-interviews/dana11235-at-gmail-com-availability/pull/3
https://canarytechnologies.slack.com/archives/C09MAQZ9LEN/p1784757314642589