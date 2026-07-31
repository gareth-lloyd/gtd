---
area: admin
contexts: []
created: 2026-07-30 15:32:23.240362
defer_until: null
due: 2026-07-31
energy: medium
id: 2026-07-30T1532-review-ian-s-investigation-agent-analysis
order: null
output: |
  ## Agent run 2026-07-30T15:45:00+03:00

  Read Ian's full artifact ("PMS Triage Agent — Hypothesis Accuracy, 1–29 July 2026",
  https://claude.ai/code/artifact/a2be0f41-be43-4b4c-b7dc-5ae2f0e96299 — WebFetch is
  blocked on it; read via Playwright browser) plus the #project-triage-agent thread it
  was posted in (https://canarytechnologies.slack.com/archives/C0AL1T2H43V/p1785414397930319?thread_ts=1785245103.410819&cid=C0AL1T2H43V).

  ### What the analysis says
  - 20 resolved PMS on-call tickets (1–29 Jul) had a gradeable agent hypothesis: 4 held,
    16 conflicted with the actual resolution.
  - The dominant failure is a single broken EU context probe: the canned "no PMS
    integration configured" false negative. All 14 instances came from the EU agent
    (14/21 EU investigations = 67%); the US agent produced zero in 38.
  - EU average post length 2,795 bytes vs US 10,613 — the EU agent reasons over ~1/4 the
    material. 10/13 probe-failure posts self-contradict (link a live Protel/Mews gateway
    account higher in the same comment).
  - Weekly probe-failure rate: 43% → 37% → 13% → 15% → 0%, but only 2 EU investigations
    since the last failure on 23 Jul — trend is suggestive, not proof of a fix.
  - Method is solid: isolated Sonnet 5 judge, texts scrubbed of IDs/links, "specific
    mechanism vs no mechanism in resolution" graded indeterminate, honest limits +
    revisions section (PMS-9581 regraded Failed→Held).

  ### My assessment
  Credible and useful — Ian's "directionally accurate" is fair. Three things worth
  flagging back:
  1. **Denominator mixing.** The "14 probe false negatives" tile sits next to "20
     graded" but is drawn from all ~59 investigations; only 7 probe rows appear in the
     graded-20 table. A skim reads "14 of 16 failures were the probe" when the graded
     table actually has 9 non-probe failures. Worth a caveat if this circulates wider.
  2. **The headline undersells the reasoning gap.** Excluding probe rows, substantive
     graded accuracy is 4 held / 13 (~31%). The three wrong-component misses (PMS-9521,
     PMS-9407, PMS-9408) share a shape the doc names well: when the true cause is
     outside Canary (vendor business rule, hotel DNS, deploy regression) the agent pulls
     it inward and blames the nearest Canary component. That's a prompt-level fix
     candidate, independent of the EU probe fix.
  3. **The PMS-9581 regrade is the most transferable lesson**: a judge that grades "the
     primary claim" penalises investigations that correctly separate diagnosis from
     recommendation. This should go straight into Laura's quality-dashboard LLM judge
     rubric (she said the Agree/Correct-this buttons exist to calibrate the judge).

  ### Suggested follow-ups (not actioned)
  - Identify what actually changed for the EU agent around 23 Jul — Ian only "presumes
    some fix on our end"; nobody has confirmed one. Until then the 0% W31 rate is 2
    data points.
  - Cheap guard: when the PMS-integration context probe returns nothing, the agent
    should say "integration context unavailable" rather than assert "no PMS integration
    configured". The 10/13 self-contradiction stat means this is also mechanically
    lintable pre-post.
  - Feed the diagnosis-vs-recommendation grading lesson to Laura's judge; supports your
    open ask to her on routes to increase the agent's query ability (thread reply
    https://canarytechnologies.slack.com/archives/C0AL1T2H43V/p1785414794683379?thread_ts=1785245103.410819&cid=C0AL1T2H43V).
  - The US 4× context size ↔ zero probe failures correlation is the strongest internal
    evidence for Ian's "it's losing out by not having access to data" point.

  No external writes made (no Slack/Linear/Notion posts).
project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 15
title: Review Ian's investigation agent analysis
updated: 2026-07-31 12:47:27.815164
waiting_on: null
waiting_since: null
working_on: false
---

https://claude.ai/code/artifact/a2be0f41-be43-4b4c-b7dc-5ae2f0e96299