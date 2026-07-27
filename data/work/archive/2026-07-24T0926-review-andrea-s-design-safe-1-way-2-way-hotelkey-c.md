---
area: null
contexts:
- react
created: 2026-07-24 09:26:13.680476
defer_until: null
due: 2026-07-24
energy: medium
id: 2026-07-24T0926-review-andrea-s-design-safe-1-way-2-way-hotelkey-c
order: null
output: |
  ## Agent run 2026-07-24T10:12:10+03:00

  Read Andrea's doc (https://app.notion.com/p/canarytechnologies/Safe-1-way-2-way-Cutover-Gated-Onboarding-Pipeline-3a6814686151819ea466f0f40d589c47),
  the Slack post (no replies yet as of this run: https://canarytechnologies.slack.com/archives/C0B1MN8F869/p1784838485897769),
  and ENT-6947 (https://linear.app/canary-technologies/issue/ENT-6947), then verified the doc's claims against the
  codebase (backend/canary onboarding + backend/pms-gateway) with two exploration agents. Nothing was posted to
  Notion/Slack/Linear — feedback below is drafted for you to deliver.

  VERDICT: Strong design. All five production problems it cites are real and verified in code (load_v2
  account-scoped missing-detection really can flip API-synced reservations to UNKNOWN; dropped webhooks,
  fetch_run race, untracked skips, wrong-vendor mid-switch all check out). The pipeline shape and the
  "checks fail fast, retryable, never poll" rail are right. Main feedback: two sub-tickets are underspecified
  on the DATA needed to implement them, and one cross-team ask is mis-specified.

  ### Substantive feedback (worth sending to Andrea)

  1. ENT-6934 (webhook-received check) has no datum to power it — this is the biggest gap.
     The gateway keeps NO persisted, account-scoped, source-tagged record of webhook receipt:
     - Raw webhook events are transient dataclasses (events/schemas/event.py); S3 payloads are deleted on consume.
     - metrics.Event rows are vendor-tagged but have no account FK and cannot distinguish webhook-sourced from
       API/fetch-sourced loads (the WEBHOOK marker in meta.updated_by is never persisted). Since HotelKey validation
       itself does FETCH_RESERVATION, a vendor=HOTEL_KEY metrics row does NOT prove inbound webhooks work — which is
       the entire point of the check.
     - Dropped events (config disabled/unresolved) leave no trace at all.
     - Canary-side EventService reservation events (the reservation_arrivals.py pattern) are not vendor/source-tagged either.
     => ENT-6934 needs new gateway work: persist e.g. last_webhook_received_at on the HotelKey config (or an
     account-scoped webhook-receipt record) + a gateway API canary can query. The doc should call this out as new
     work; right now the check reads as if the data already exists.

  2. The PMS-9414 ask "include HotelKey in the consume.config_disabled alert" is mis-specified.
     HotelKey's handler never logs consume.config_disabled (that string belongs to cloudbeds/sihot/synxis_crs/etc.).
     HotelKey folds is_enabled=True into the config lookup (hotelkey/services/event.py get_config), so a DISABLED
     config is logged identically to an UNKNOWN property (hotelkey_webhook.get_config.unknown_property). Before any
     alert is possible, the HotelKey handler must split that query to distinguish disabled vs unknown. Reword the
     dependency ask accordingly — and note this same split is a prerequisite for debugging a red ENT-6934 check.

  3. ENT-6949 (surface skipped checks) needs schema work, not just UI.
     skipped_check_names is a bare ArrayField on OnboardingScriptHotel — no who/when/why is persisted anywhere
     (only an ephemeral structlog line). The doc's Support section promises "who skipped what"; that requires new
     fields (skipped_by/skipped_at/reason) or event logging. Make sure ENT-6949's scope includes the attribution
     data, else the UI can only ever show WHICH checks were skipped.

  4. The NO_ACTIVE_ARRIVALS_INTEGRATION pre-run check needs a gateway READ API that doesn't exist.
     Canary's PMSGatewayService has no arrivals endpoints at all; arrivals state lives only in pms-gateway. The doc
     specifies the retire (write) endpoint but the VALIDATE pre-run check also needs "does this account have an
     active arrivals integration?" — either a read endpoint, or have retire return state, or have the check treat
     the ENT-6933 gateway-side guard as the only enforcement. Small, but it's unlisted new work.

  5. Stage wiring nuance for ENT-6948: CLEANUP_PREVIOUS_PMS_VENDORS is an AD-HOC stage in IHG_PILOT
     (property_configuration_processes.py:2337, inside ad_hoc_stages), not part of the ordered flow — "IHG_PILOT
     already runs it" slightly oversells it. For BW MSA, decide explicitly: ordered stage before
     CREATE_PMS_CONFIGURATION (which actually enforces the doc's "ordered pipeline") vs ad-hoc (operator-triggered,
     ordering enforced only by the pre-run check safety net). Also note BW MSA has its own PMS_SWITCH_ARCHIVE /
     PMS_SWITCH_CLEANUP_PREVIOUS stages (lines 1985-1988) — worth a sentence on how the extended plan relates to those.

  6. Suggest adding a one-off data audit to the rollout: accounts that TODAY have an enabled 2-way config AND a
     live ArrivalIntegration (ignore=False) are already in the corrupting state; the pipeline only protects future
     cutovers. A quick sweep + bulk retire would close the existing exposure. (Supporting evidence: pms-gateway
     already half-knows this risk — ArrivalIntegration._validate_account_integrations blocks multiple feeds on
     DETECT_MISSING accounts with a comment admitting it's "not bulletproof", but nothing guards the 1-way+2-way
     coexistence case.)

  ### Minor nits
  - Doc says ENT-6933 "shipped" in Goals but "in review" in Rollout; PR #50997
    (https://github.com/canary-technologies-corp/canary/pull/50997) was not yet merged to master as of this check —
    pick one status.
  - Retire route shape: existing routes are api/accounts/me/<vendor>/<action>; "arrivals" is not a Vendor enum
    member, so api/accounts/me/arrivals/retire is a slight pattern deviation. Fine, just intentional.
  - IHG_PILOT currently has pre_run_hotel_checks={} (deliberately, per comment at ~:2378) — wiring these checks into
    a future IHG 1-way→2-way type will be the first pre-run checks for that family; no blocker, just context.

  ### Verified-correct claims (no action, good to affirm to Andrea)
  - load_v2._detect_and_update_missing_reservations scopes candidates by account + check-in window only
    (load_v2.py:1247-1251) — the UNKNOWN-clobber risk is real.
  - ArrivalIntegration.ignore is admin-only today (no API/service/command writes it); processor short-circuits with
    DISABLED_INTEGRATION before parsing. Retire-when-nothing-to-retire idempotency is trivially safe.
  - _enable_account enables only when zero INCOMPLETE validations remain; HotelKey webhooks are dropped until
    is_enabled=True. Both match the doc.
  - Pre-run checks are per-hotel, retryable, skippable (skippable=True only), skips gated on >=1 failed run —
    the GOLIVE gate pattern already exists in BW MSA (Twilio + 4 BW checks), so ENT-6934's placement is sound.

  Suggested next step: send points 1-6 to Andrea (Slack thread reply or Notion comments) — I can draft either on request.
project: 2026-04-16T1210-unblock-team
source_id: https://canarytechnologies.slack.com/archives/C0B1MN8F869/p1784838485897769
tags:
- morning-gtd
- slack
time_minutes: 30
title: 'Review Andrea''s design: Safe 1-way→2-way HotelKey cutover pipeline'
updated: 2026-07-27 13:35:50.609581
waiting_on: null
waiting_since: null
working_on: false
---

Andrea @-mentioned you + Tincho in #epd-enterprise-engineers (Jul 23): BW HotelKey 1way→2way cutover needs the manual ArrivalsList-disable folded into cutover scripts; her lightweight design doc ties the threads together (parent ENT-6947 + subs already created, will adjust from feedback).
Doc: https://app.notion.com/p/canarytechnologies/Safe-1-way-2-way-Cutover-Gated-Onboarding-Pipeline-3a6814686151819ea466f0f40d589c47
https://canarytechnologies.slack.com/archives/C0B1MN8F869/p1784838485897769