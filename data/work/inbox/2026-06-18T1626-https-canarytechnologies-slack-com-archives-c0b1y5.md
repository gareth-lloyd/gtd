---
area: null
contexts: []
created: 2026-06-18 16:26:09.828937
defer_until: null
due: null
energy: low
id: 2026-06-18T1626-https-canarytechnologies-slack-com-archives-c0b1y5
order: null
output: |
  ## Agent run 2026-06-18T13:31:34Z

  **Task:** Andrea asked (group DM with me + Connor, https://canarytechnologies.slack.com/archives/C0B1Y5K9AMC/p1781789131712189):
  "give Tinchos Eng design on drift a look, he's updated it." Tincho = Martin Rodriguez
  (martinrodriguez@canarytechnologies.com), Sr SWE @ Enterprise.

  **Doc reviewed:** "Eng Design (v2): Configuration Drift Detection for Enterprise Hotels"
  (https://app.notion.com/p/38181468615181fdbfa5c6d79a11deba) — ENT-6488
  (https://linear.app/canary-technologies/issue/ENT-6488/eng-design), Status WIP.
  Against my PRD: https://app.notion.com/p/37c814686151813884b7d338378b5c18

  ### Bottom line
  Strong design — implement-ready after a couple of decisions are nailed. I verified every
  load-bearing code claim against the actual codebase (two parallel read-only sweeps) and they
  are ALL accurate, including the subtle central one. Tincho clearly knows this area. It covers
  the PRD goals, respects every non-goal (read-only, internal admin only, no auto-remediation),
  follows house patterns (segmentation fan-out, the periodic-task migration that omits `enabled`,
  acks_late + FIFO idempotency), and is honest about its one real wart. My pushback is on 3
  decisions, not on the architecture.

  ### Claims I verified TRUE in code (so we can trust the design's premises)
  - Central insight is correct: `ConformityService.finalize()` discards the `OverridePolicy`
    when freezing values (`conformity.py` ~545: `{key: value for key,(_,value) in ...}`), so
    today `hotel_conforms` flags FREE mismatches identically to FINAL. The `enforced_only` flag
    genuinely does not exist and is needed — this is the heart of the design and it's real.
  - `validate_path_from_node` does raise when a key is redefined below a FINAL ancestor, so
    "FINAL is sticky down a path" is sound — the winning-definition-policy reading is valid.
  - Wyndham config really is 39 FINAL / 27 FREE — i.e. ~40% of the rule surface would be
    false-positive drift without the fix. The "number one trust risk" framing is accurate.
  - Infra: `MSA_HOTEL_PROVIDERS` has only WYNDHAM_CONNECT_GMS today; StoredHotelAttributes is
    1:1 w/ Hotel and stores msas/live_msas/parent_brand/brand/mgmt_co but NOT region/country;
    segmentation master->per-entity->batch(250) pattern exists; periodic-task migration omits
    `enabled` from defaults on purpose; `task_acks_late=True` + `default.fifo` confirmed;
    `apply_portfolio_settings` overwrites FINAL+FREE alike. All as the doc states.

  ### Push on these 3 before it ships (in priority order)
  1. **The "two coexisting drift definitions" wart is the real risk — escalate Open Q #1 to a
     decision, don't ship it as an open question.** After this lands, the new admin shows
     *enforced-only* drift while the monitoring health check
     (`monitored_hotel_state.py` CONFORMS_TO_RULE_BASED_CONFIGURATION) and the on-save admin
     warnings (`signals.py`) keep *all-settings* semantics. So the same hotel can read "No drift"
     in the new view while monitoring says UNHEALTHY and the save page warns. The PRD's #1 risk
     is "false positives erode trust" — two contradictory drift surfaces is exactly that. The
     doc's mitigation (label the column "enforced drift" + a model comment) is weak; it relies
     on operators noticing a label. Stronger argument the doc doesn't make: the monitoring check
     counting FREE divergence as UNHEALTHY is arguably *already a latent bug* (FREE is allowed to
     diverge by definition), so aligning it to enforced-only may be lower-risk than leaving the
     contradiction in place. Recommend: at minimum give Open Q #1 an owner + ticket before V1;
     ideally fold the monitoring-check alignment into V1's PR1 (conformity policy tracking).
  2. **Log level for `detect_drift.non_conforming` (Open Q #2): demote it.** It fires daily,
     per drifted key, per hotel, at error level. Predictable daily error logs for known states =
     alert fatigue + Groundcover cost. The stored admin state is the system of record now, not
     the log stream. Keep error/warning for `new_drift` only; demote the recurring per-key event
     to info. (Idempotency note in its favor: because `new_drift` is derived from the persisted
     `previous` drifts read fresh each run, SQS redelivery won't double-emit it — nice property.)
  3. **First-run Salesforce fetch (flagged under Dependencies/Impact): state the threshold +
     contingency, don't just "check the count."** First run does one SFDC fetch per hotel missing
     a StoredHotelAttributes row. Serial FIFO batching mitigates a thundering herd (calls are
     serialized, so rate-limit risk is low), but a high missing-row count makes the first run very
     long. Recommend the doc say what count is "too high" and the fallback (e.g. a one-off
     pre-seed/backfill of rows, or a throttled first pass) rather than discovering it at rollout.

  ### Smaller notes / nits
  - PR split (Open Q #4): endorse the 3-PR sequence — PR1 (conformity policy tracking) is
    independently valuable + testable and is the natural place to also fix #1 above.
  - Schedule (Open Q #3): 06:30 UTC is fine — off-peak in both US (overnight) and EU (early am).
    No constraint I know of.
  - "Drifted setting" admin filter builds its dropdown via a distinct-key scan over all `drifts`
    arrays on every changelist render — O(table) per page load. Negligible at one-MSA scale;
    worth a sentence as a "watch as more MSAs onboard" item (pairs with the deferred GIN index).
  - `.update(drifts=..., calculated_at=now())` deliberately bypasses signals — good — but it also
    skips any `auto_now` on StoredHotelAttributes; confirm nothing relies on that timestamp
    (drifts_calculated_at covers freshness, so likely fine).
  - Doc hygiene: there are TWO eng-design pages both dated 2026-06-16 — v1
    (https://app.notion.com/p/380814686151818f881ae8fea4be36ea) and v2 (reviewed). Suggest
    confirming v2 is canonical and archiving v1 so reviewers don't split across both.

  ### PRD coverage check (all met)
  Goal 1 visible + FREE excluded ✅ (the enforced_only work IS this); Goal 2 per-hotel/per-setting
  queryable ✅ (admin filters); Goal 3 fresh daily ✅ (beat job); stretch alerting w/o flood ✅
  (baseline-run suppression + new_drift events); cohort-gap risk ✅ (the "never checked" null-
  timestamp state directly answers the PRD's "don't confuse no-drift with not-checked"). Appendix
  on policy-aware re-apply is correctly fenced as post-V1 (ENT-6403).

  ### Not done (needs your approval — external writes)
  Did NOT post anything to Notion/Slack/Linear. If you want, I can draft a Notion comment on the
  v2 doc or a Slack reply to Andrea summarizing the above — just say the word and I'll show you
  the exact text first.
project: null
source_id: null
tags: []
time_minutes: 5
title: https://canarytechnologies.slack.com/archives/C0B1Y5K9AMC/p1781789131712189
updated: 2026-06-18 16:31:34.847211
waiting_on: null
waiting_since: null
working_on: false
---