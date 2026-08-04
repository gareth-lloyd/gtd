---
area: null
completed_at: 2026-08-04 14:33:15.391817
contexts: []
created: 2026-08-04 13:25:03.275357
defer_until: null
due: null
energy: low
id: 2026-08-04T1325-laura-s-rollout-doc
order: null
output: |
  ## Agent run 2026-08-04T11:10:28Z

  Reviewed Laura DeWald's Workup rollout proposal (https://pages.cnry.cloud/workup-rollout-proposal/),
  sent via Slack DM on Aug 3 (https://canarytechnologies.slack.com/archives/D07U6KK5W1G/p1785777770833659).
  Context: she already shared it with Blake, Andy, and Stephanie and met all three on Aug 3
  evening, so these findings are follow-up ammo rather than pre-send edits.

  **Verdict: strong doc. Every external number checks out; the arithmetic is internally
  consistent; the caveats are honest. Four things worth raising, first two substantive.**

  Verified correct:
  - All arithmetic: 904 July tickets = ~29/day; 86% routed = ~25/day; 119 runs x $11.96
    = $1,423; full-rollout ~$9.3k intro; x1.5 = ~$14k standard; Opus x1.67 = ~$23k;
    weighted accuracy (27 + 18/2)/63 = 57.1%.
  - Anthropic pricing: Sonnet 5 intro $2/$10 through Aug 31, standard $3/$15, Opus 5
    $5/$25 - all match Anthropic's current published rates.
  - OpenAI pricing table verified against OpenAI's live pricing page
    (https://developers.openai.com/api/docs/pricing): gpt-5.6-sol $5/$30, terra $2/$12,
    luna $0.20/$1.20, gpt-5.4-mini $0.75/$4.50, cached input ~90% off - all exact.
    (Several third-party aggregator sites list different terra/luna prices; the doc used
    the primary source and is right.) GPT-5.6 GA July 9 also checks out. The "terra a
    third below Sonnet on input, 20% below on output" comparison is arithmetically correct.

  Findings to raise with Laura:
  1. **"~14 correct diagnoses/day" mixes weighted and fully-correct accuracy.** 57% is
     weighted (partials at half). Fully correct is 27/63 = 43% -> ~11/day; the other ~3.5
     are half-weighted partials. The 0.5-0.9 FTE value math inherits this - if a partial
     diagnosis saves less than 15-30 min, the low end drops. A sharp reader could poke
     this; suggest restating as "~11 fully correct + ~7 partially correct per day".
  2. **Internal inconsistency: 18 vs 19 wrong.** The hero stats say 63 judged with 18
     wrong; rollout step 4 says "8 of 19 wrong diagnoses". One of the two needs fixing
     (or the differing window explained).
  3. Minor: "near or above the $14k/month cost line" is generous at the low end - 0.5 FTE
     at a loaded ~$15-20k/month is ~$7.5-10k, below the line. Top end clears it.
  4. Unstated selection bias: accuracy is measured only on tickets that have resolved and
     been judged (63 assessable of 119 runs). Resolved-quickly tickets likely skew easier,
     so 57% may be optimistic for the full stream. The caveats cover sample size and team
     skew but not this.

  Also worth knowing: the Bottom line cites "Gareth Lloyd has reviewed these numbers and
  strongly supports the staged, accuracy-gated rollout" - consistent with your Jul 24 DM,
  but you're on the record by name in a doc visible to anyone with a Canary account.

  Doc figures vs the Jul 23 DM estimates: costs rose ($7.5k -> $9.3k intro, $11k -> $14k
  standard) and accuracy dipped (60% -> 57%) as the full-July data came in; the doc
  presents the updated numbers transparently.
project: null
source_id: null
tags: []
time_minutes: 5
title: laura's rollout doc from DM - review
updated: 2026-08-04 14:33:15.391806
waiting_on: null
waiting_since: null
working_on: false
---