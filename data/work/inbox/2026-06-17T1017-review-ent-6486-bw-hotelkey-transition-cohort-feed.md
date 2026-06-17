---
area: null
contexts:
- react
created: 2026-06-17 10:17:35.414097
defer_until: null
due: null
energy: medium
id: 2026-06-17T1017-review-ent-6486-bw-hotelkey-transition-cohort-feed
order: null
output: |
  ## Agent run 2026-06-17T07:28Z

  ### Bottom line
  ENT-6486 is marked **Done** but has effectively been **reopened by the customer-facing
  onboarder (Melissa Fairchild) and is going unaddressed**. The original fix is real and
  deployed — but Melissa's 6/16 retry failed again for a *different* reason. The ticket
  reading "Done" is masking a live blocker on the BW→HotelKey transition cohort.
  Issue: https://linear.app/canary-technologies/issue/ENT-6486/bw-hotelkey-transition-cohort-feedback-validate-fail-step

  ### What was already fixed (and is genuinely deployed)
  - Original root cause (from my 6/11 investigation comment): HotelKey `authenticate`
    validation called the third-party data-ingestion `room-status` endpoint
    unconditionally and treated its **401 as fatal**. HotelKey grants that endpoint
    per-property and most BW properties don't have it → every transition hotel failed
    validate with `pms_validation_failed_authenticate` / "Unknown PMS Gateway error".
  - Fix: PR #47873 (https://github.com/canary-technologies-corp/canary/pull/47873) made the
    room-status probe non-fatal (auto-disables `room_refresh_enabled` on 401/403, keeps
    `get_charge_types()` as the real credential check). File:
    `backend/pms-gateway/vendors/integrations/hotelkey/services/validation.py`.
  - Merge commit `588e02fff27`. **Confirmed in `origin/master`** and first released in
    **v2026.18.139, deployed 2026-06-12 19:58 UTC** — i.e. it was live ~4 days before
    Melissa's 6/16 retry (prod was running v2026.19.40 at the time). So the room-status
    path is NOT the cause of the 6/16 failure.
    (Note: this GTD worktree branch `worktree-portfolio-analytics-agent` predates the fix,
    so `validation.py` here still shows the old unconditional call — don't be fooled, master
    has the fix.)

  ### The unresolved part — Melissa's 6/16 retry still fails validate
  - 6/16 20:44Z comment: new cohort `171ca4be` / batch `b8bf24bc-2095-46b8-882d-15dd61e868f7`,
    fetch batches completed and reservations populated, **but validate still failed**.
  - 6/17 01:32Z follow-up — her own hypothesis: *"is the fetch run actually pulling from the
    OLD integration, so validate on the new (HotelKey) integration fails?"*
  - Lautaro Mena (assignee) last replied 6/12 ("Fixed, try again next week"). Her two
    reopen comments are **unanswered**.

  ### My diagnosis of the 6/16 failure (two candidates, ranked)
  I could NOT pull the exact 6/16 error code from Datadog — the onboarding validate runs
  async via `cron_run_onboarding_script_batches` and stores its result/error in the DB; the
  `configure_pms_integration_validate.*` structured events did not surface in logs search
  (different index / not full-text indexed). So the ranking below is reasoned from code +
  her description, not yet confirmed by her batch's error row.

  1. **MOST LIKELY — mixed-vendors guard (matches her own hypothesis).**
     `onboarding/plans/configure_pms_integration_validate_plan.py:65-74` iterates the gateway
     account's `validations` and raises `ERROR_PMS_MIXED_VENDORS` if ANY validation's
     `vendor != account.type` (only Synxis/Synxis-CRS pairing is tolerated). In a PMS
     *switch*, if the account still carries the previous BW vendor's validation entries, or
     `account.type` wasn't fully flipped to HOTELKEY when validate ran, this fails
     immediately — *before* authenticate even runs. Her flow is exactly the trigger: she's
     been "swapping the PMS value to HOTELKEY manually directly from within the cohort,"
     which can leave the gateway account in a mixed/stale state. This is a workflow /
     PMS-switch-ordering bug, not the room-status bug.

  2. **LESS LIKELY — a different validation kind now fails.** With the room-status probe
     fixed, authenticate should pass (she confirmed fetch works, which uses the same V4
     `get_charge_types` JWT path). Validation then proceeds through `VALIDATION_ORDER`
     (authenticate → fetch_reservations → fetch_reservation …); a downstream kind such as
     `fetch_reservation` could fail. Connection-health for HotelKey accounts shows
     `GetChargeTypes` ~0.73 success and `GetRoomStatus` 0.0 — so authenticate isn't bulletproof,
     but that 0.73 is an all-accounts aggregate, not her cohort specifically.

  ### Decisive next step (one data point disambiguates everything)
  Pull the **error code + context_string** from her 6/16 batch result row
  (`b8bf24bc-2095-46b8-882d-15dd61e868f7`) — via the onboarding script-batch detail
  page/admin or DB. The plan stores it through `raise_expected_error(code, context_string)`:
  - `pms_mixed_vendors` / "Account type ... and validation vendor ... are not compatible"
    → candidate 1 confirmed → fix the PMS-switch step to clear/replace the old vendor's
    validations (or correct the cohort step ordering). Not a gateway-validation-code bug.
  - `pms_validation_failed_<kind>` → candidate 2 → reopen the gateway investigation for that
    specific kind.

  ### Process recommendation
  Reopen ENT-6486 (or split a follow-up) and re-ping Lautaro. The customer-facing onboarder
  has a live blocker but the Done status is hiding it — this is the 4x BW
  `validate_pms_configuration` failures on 6/16 referenced in the GTD item.

  ### Draft Linear reply (NOT posted — needs your approval to send)
  > @Melissa @Lautaro — reopening: the 6/12 fix (room-status 401 made non-fatal, PR #47873)
  > is deployed and confirmed live since 6/12, so it's not the cause of the 6/16 failure.
  > The most likely cause of the new failure is the validate step's mixed-vendor guard:
  > if the gateway account still has the OLD BW vendor's validation entries attached (or the
  > account type wasn't fully switched to HOTELKEY) when validate runs, it fails with
  > "mixed vendors" before authenticate even runs — which matches Melissa's hypothesis about
  > the old integration. Can someone grab the exact error code + context from batch
  > b8bf24bc-2095-46b8-882d-15dd61e868f7? If it's `pms_mixed_vendors`, the PMS-switch step
  > needs to clear the old vendor's validations, not the gateway validation code.

  ### Caveats / not verified
  - Did not confirm her batch's actual error code (Datadog onboarding-validate events not
    surfacing; would need the script-batch result row or shell access to the cohort hotels).
  - Did not inspect the live gateway account state for her cohort hotels (read-only,
    no hotel IDs to hand).
project: null
source_id: https://linear.app/canary-technologies/issue/ENT-6486/bw-hotelkey-transition-cohort-feedback-validate-fail-step
tags:
- morning-gtd
- linear
- from-awareness
time_minutes: 20
title: 'Review ENT-6486: BW HotelKey transition cohort feedback — validate fail step'
updated: 2026-06-17 07:28:47.000000
waiting_on: null
waiting_since: null
working_on: false
---

mfairchild feedback on the validate-fail step; likely tied to the 4x BW validate_pms_configuration onboarding failures on 6/16. https://linear.app/canary-technologies/issue/ENT-6486/bw-hotelkey-transition-cohort-feedback-validate-fail-step