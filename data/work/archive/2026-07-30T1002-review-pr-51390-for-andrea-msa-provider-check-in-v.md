---
area: null
contexts:
- react
created: 2026-07-30 10:02:01.886233
defer_until: null
due: 2026-07-30
energy: medium
id: 2026-07-30T1002-review-pr-51390-for-andrea-msa-provider-check-in-v
order: null
output: |
  ## Agent run 2026-07-30T15:45:00+03:00

  Reviewed PR #51390 (https://github.com/canary-technologies-corp/canary/pull/51390),
  branch abradshaw/ENT-6639/dont-reset-check-in-to-v1, head 919a19c. Verdict: **the change is
  correct and well-tested — approve.** Facundo already approved (his frozen-dataclass
  suggestion was adopted). Nothing posted to GitHub or Slack — draft reply below for you to send.

  ### Verified mechanics

  - `AddRegistrationCardPlan.execute` (registration_card_plans.py:59) runs the provider's
    `perform_hotel_configuration` first, then applies `check_in_configuration_updates`
    declared in provider `__init__` via `get_check_in_config_update_kwargs()` with
    `save(update_fields=...)`. All three touched providers (Default, BW, Wyndham) now
    declare `rollout_check_in_v2_level=STABLE` there; both MSA providers' writes removed.
    Grep confirms zero remaining imperative writers of the field in onboarding.
  - Plan ordering (property_configuration_processes.py): for both WYNDHAM_MSA and
    BEST_WESTERN_MSA, AddRegistrationCardPlan runs in BASE_CONFIGURATION_NEW *before*
    EnableMsaProductsPlan — confirming Andrea's Q1 diagnosis: full runs went NONE→STABLE
    inside one transaction (invisible), reg-card-only reruns committed NONE onto live
    hotels. EnableMsaProductsPlan also runs at GOLIVE where the reg-card plan doesn't, so
    the PR removes a silent GOLIVE "repair path" — Andrea already flags this in the
    description; acceptable given ENT-6977 backfills the stuck data.
  - Blast radius of all 8 AddRegistrationCardPlan wirings checked: Wyndham MSA/staging and
    BW MSA/staging → STABLE (intended); DEFAULT/DEMO → DefaultRegistrationCardProvider,
    STABLE same as before (moved imperative→declarative, net no-op); IHG_PILOT/IHG_STAGING
    → IHGRegistrationCardProvider, which never touched the field before or after — no change.
  - Bonus behavior worth noting to Andrea: BW previously wrote NONE unconditionally; now a
    reg-card rerun on a live BW hotel actively repairs it to STABLE, so the portfolio starts
    converging ahead of the ENT-6977 backfill (she noted this in the ticket).
  - Edge cases checked: no ROLLOUTS registered on reg-card providers (execute_rollout
    bypasses execute, so declared config wouldn't apply there — not an issue today);
    provider exceptions propagate before the config write; BW provider always returns a
    dict, never None. frozen=True + dataclasses.replace correctly protects the shared
    ADDITIONAL_GUEST_STEPS_BY_COUNTRY constants; asdict() handles enums fine.

  ### Answers to Andrea's two questions

  **Q1 (MSA provider overriding on rerun):** Her diagnosis is exactly right — verified
  against plan ordering above. Single-writer-in-the-reg-card-plan is the right fix because
  `check_in/services/registration_card.py` picks the v1-vs-v2 template from this field, so
  schema and version must be written by the same plan execution.

  **Q2 (why was the value set in configure_hotel rather than during initialization):**
  Two-part answer:
  1. *Structural:* provider `__init__` only receives `OnboardingPlanData` (account/brand
     scope — no Hotel), so only hotel-independent values can be declared there; the plan
     applies them uniformly. `perform_hotel_configuration(hotel)` is the only hook with the
     hotel, needed for per-hotel conditionals. The v2 level is a static brand constant, so
     declarative `__init__` is where it belongs — Andrea's move is correct.
  2. *Historical (it was me):* I added the imperative NONE writes in PR #28648
     (https://github.com/canary-technologies-corp/canary/pull/28648, commit 435f283bc4a,
     July 2025) to override PR #26963 (June 2025), which had just made
     DefaultRegistrationCardProvider write STABLE imperatively — Wyndham/BW weren't on v2
     yet. `rollout_check_in_v2_level` wasn't a field on CheckInConfigurationUpdates then, so
     I mirrored the default provider's imperative style — path of least resistance, no
     deeper design reason. It became a landmine once the MSA providers later gained STABLE
     writes. Her refactor is what it always should have been.

  ### Draft Slack reply to Andrea (NOT sent — awaiting your approval)

  > Had a look at the PR — LGTM, approving. On your questions: (1) your diagnosis is right;
  > I verified the plan order — reg card plan runs before EnableMsaProductsPlan in
  > BASE_CONFIGURATION_NEW, so full runs masked the NONE and standalone reruns committed it.
  > Making the reg card plan the single writer is the right call since the reg card service
  > picks the v1/v2 template off that field. (2) Confession: the imperative writes were
  > mine (#28648) — a quick override after #26963 made the default provider write STABLE,
  > back when Wyndham/BW weren't on v2. The field just wasn't on CheckInConfigurationUpdates
  > at the time, so I matched the existing imperative style. Nothing structural — provider
  > __init__ only has OnboardingPlanData (no hotel), but since this value is a static brand
  > constant that's exactly where it belongs. Your version is what it should have been.
  > One thing worth keeping in mind: with the MSA plan no longer writing at GOLIVE, the old
  > accidental repair path is gone — but ENT-6977 covers that, and reg-card reruns now
  > actively fix live BW hotels to stable.

  Suggested next steps: (a) approve the PR on GitHub (I did not submit any review),
  (b) send Andrea the Slack reply (Slack DM: https://canarytechnologies.slack.com/archives/D061NMRMFB3/p1785351894555019).
project: 2026-04-16T1210-unblock-team
source_id: https://canarytechnologies.slack.com/archives/D061NMRMFB3/p1785351894555019
tags:
- morning-gtd
- slack
time_minutes: 15
title: 'Review PR #51390 for Andrea: MSA provider check-in version override'
updated: 2026-07-30 15:29:38.839550
waiting_on: null
waiting_since: null
working_on: false
---

Andrea (DM, last night): "if you have a chance tomorrow" (= today). Questions: 1) MSA provider was setting check-in version, overriding reg-card provider values on rerun; 2) why set the value in configure_hotel rather than during initialization.
https://github.com/canary-technologies-corp/canary/pull/51390
https://canarytechnologies.slack.com/archives/D061NMRMFB3/p1785351894555019