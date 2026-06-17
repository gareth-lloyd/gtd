---
area: null
contexts: []
created: 2026-06-17 19:46:26.869459
defer_until: null
due: null
energy: low
id: 2026-06-17T1946-review-amb-eng-design
order: null
output: |
  ## Agent run 2026-06-17T16:49Z — Review of AMB eng design (V2)

  **What this is:** Tincho's eng design to make Apple Messages for Business (AMB) a
  standard, automated part of the Wyndham config — for new onboardings AND the live
  portfolio (~4,761 US + 149 EU hotels; only 9 configured today), across Connect +
  Connect Plus.

  - Doc: Eng Design: AMB Configuration Plan & Rollout for Wyndham (V2)
    https://www.notion.so/canarytechnologies/Eng-Design-AMB-Configuration-Plan-Rollout-for-Wyndham-V2-37d81468615181caa47bd262de1304a8
  - Linear: ENT-6422
    https://linear.app/canary-technologies/issue/ENT-6422/eng-design-for-amb-configuration-plan-and-rollout-for-wyndham
  - Project: https://linear.app/canary-technologies/project/define-amb-configuration-plan-and-roll-out-for-wyndham-9ac472ed8a89
  - Slack thread (Connor → Kelly/Andrea clarifying Qs):
    https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1781709457532469?thread_ts=1781709445.988699&cid=C047K6WSUJY

  ### Verdict
  Strong, unusually rigorous design. I verified its load-bearing claims against the
  actual backend code and they hold up. Recommend approving Phase A + B for **US only**,
  with the granularity/safety caveats below addressed before stage 1. EU/AP is now
  explicitly out of the near-term path (see Slack).

  ### Code verification (I checked, claims are TRUE)
  - The central "enabling is not inert" claim is **correct**. `send_consent_request_if_eligible`
    (messaging_integrations/services/amb/messaging_outbound.py:983-1076) gates on
    `has_chat`, the brand link, `business_updates_enabled`, a per-phone thread-lock, and
    `brand_logo` — and does **NOT** gate on `amb_config.enabled` and does **NOT** read any
    GrowthBook flag. So linking a hotel to a brand config with `business_updates_enabled=True`
    arms proactive outbound regardless of the `enabled` flag. Tincho documented this exactly right.
  - GrowthBook flag `amb-business-updates-consent-flow` has **zero functional readers** (only
    its definition in feature_flags/generated/generated_features.py:560). Confirmed: it gates
    nothing today. The doc's "default-serve true, no wiring" decision is honest about this.
  - `update_amb_config` (chat/services/amb_config.py:18) indeed never writes `enabled` /
    `wyndham_help_bot_flow_enabled` — so a fresh AMBConfig stays off; the new `provision_amb_config`
    setting them explicitly is the right fix. `provision_amb_config` does NOT exist yet (correct).
  - Models, defaults (`AMBConfig.enabled` default False), `AMBBrandConfig` PK = `business_id`,
    and the Plan/Provider/KNOWN_PLANS/TargetedRollout(LIVE+ALL) framework all exist as described.

  ### Strengths
  - One shared code path (Plan + Provider) reused by both onboarding and the existing-site
    rollout — no bespoke backfill script. Idempotent `provision_amb_config`. Clean.
  - Correctly identifies and fails-loud on the EU footgun (running rollout before the EU brand
    config exists would auto-create a logo-less one and burn consent slots).
  - CI-atomic enum + ROLLOUTS + recipe seam called out (A2 ships provider w/o ROLLOUTS; B1 ships
    all three in one PR).
  - Rollback discipline: brand kill-switch AND a tested deactivation path (B6) required *before*
    stage 1. Staging as the primary throttle is the right mental model given the gating reality.

  ### Concerns / questions to raise with Tincho before approval
  1. **No per-hotel brake — only batch staging + a brand-WIDE kill-switch.** Because the
     GrowthBook flag is decorative and `enabled` doesn't gate sends, the only two brakes are
     (a) how fast you link hotels in batches and (b) `business_updates_enabled=False`, which is
     all-or-nothing for the whole brand (and also halts the 9 already-live hotels + AMB-first
     routing for opted-in guests). If one cohort goes bad mid-rollout there's no targeted stop
     short of killing the brand. Worth deciding explicitly: is that granularity acceptable, or
     is it worth cheaply wiring a real per-hotel/per-cohort gate? B6 should cover *targeted*
     deactivation, not just the brand kill.
  2. **Unsolicited first-contact opt-in messaging to ~4,900 hotels' guest streams.** Event-driven
     (no instant blast) but sustained, with re-sends to silent guests after 1+ day. This is a
     guest-experience/compliance surface, not just eng. Confirm Product/Legal/Wyndham have signed
     off on the consent message content + re-send cadence before arming it at portfolio scale.
  3. **Quantify the *real* send population via `has_chat`.** AMB is send-inert without `has_chat`,
     and Connect Plus onboarding never sets it. The doc flags this for the 9 Connect-Plus-only
     hotels, but the bigger question: of the ~4,761 live US hotels, how many actually have
     `has_chat=True`? That's the true proactive-send blast radius — worth a prod count before
     sizing stages (and it tells you whether the rollout silently no-ops for a big chunk).
  4. **Stage sizes + advance criteria should be concrete.** Default (5,10,500) jumps to 500/batch;
     doc rightly says set smaller. Propose an explicit conservative ladder and *quantitative*
     stage-advance gates (opt-out-rate ceiling, Apple delivery-failure ceiling) rather than B2's
     prose "stage-advance criteria."
  5. **Build + validate the monitoring dashboard BEFORE stage 1**, baselined against the 9
     already-live hotels — not during B2's run. You want working alarms and a baseline before
     the first new send.
  6. **Two tests worth adding** to the (already solid) test plan: kill-switch works
     (`business_updates_enabled=False` ⇒ no consent send) and the rollout fn raises when the
     brand config is absent (the EU guard the snippet omits).

  ### EU/AP — superseded by the Slack thread
  The Slack clarifications update the doc's EU plan: Kelly confirmed EU needs a **different
  Apple business_id**, the **EU MSP** selected on the Apple Business Register, and a **different
  webhook** (already provisioned; env vars believed to already point to EU/AP MSPs — Kelly to
  double-check). Wyndham being already approved should make the EU business-id approval easy.
  Andrea + Connor then decided to **split EU/AP into a separate milestone and keep this US-only**
  ("that's where most of the value is"). So: move B4 + Open Question #1 out of the critical path;
  OQ #1 is effectively answered (region-specific id, separate MSP/webhook). Reflect that in the doc.

  ### Suggested next step
  Reply in-thread / on the doc is NOT posted (I don't post to external services without your
  approval). If you want, I can draft a Notion comment or Slack reply with the points above —
  say the word and I'll show you the exact text first.
project: null
source_id: null
tags: []
time_minutes: 5
title: REVIEW AMB eng design
updated: 2026-06-17T16:49:38Z
waiting_on: null
waiting_since: null
working_on: false
---

https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1781709457532469?thread_ts=1781709445.988699&cid=C047K6WSUJY