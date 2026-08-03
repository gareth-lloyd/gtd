---
area: null
contexts: []
created: 2026-07-28 16:43:38.657591
defer_until: null
due: 2026-07-29
energy: low
id: 2026-07-28T1643-review-this-ticket-should-reservations-always-be-a
order: null
output: |
  ## Agent run 2026-07-30T10:02

  Reviewed ENT-6126 (https://linear.app/canary-technologies/issue/ENT-6126/validate-and-update-csr-idhotel-id-during-initial-configuration).
  Status: already **Deployed** — PR #50359 (https://github.com/canary-technologies-corp/canary/pull/50359)
  merged 2026-07-29 by Andrea Bradshaw.

  **Question origin**: Andrea asked Marta on the ticket "should old reservations be archived,
  even if they are the same pms gateway type?"; Marta answered yes, and the PR implemented that.

  **Verdict: yes — always archiving on a hotel_id change is the right call.**
  - When the SynXis CRS ID changes on a brand flip, the old id stops receiving updates: active
    reservations under it go stale but keep driving guest messaging and dashboard arrivals.
  - The new CRS id re-sends the same physical stays under new confirmation numbers, so
    unarchived old reservations would duplicate them.
  - The archive is well scoped (`onboarding/plans/pms_switch_archive_plan.py`): only active
    statuses (RESERVED / DUE_IN / INHOUSE), 30 days back — history (checked-out/cancelled)
    is untouched. It reuses the proven PMS-switch archive → cleanup → complete pipeline.
  - Escape hatch exists: the new pre-run check gating reconciliation on completed archive +
    cleanup is skippable, so Ops can bypass in an edge case where archiving is unnecessary.

  **Caveats (accepted tradeoffs, same as any PMS switch)**:
  - INHOUSE guests get archived mid-stay and re-fetched as new reservation objects, losing
    linkage to prior check-in/payment state.
  - PR notes SphCrsConfiguration.hotel_code / OHIP hotel_code drift is out of scope; the
    ad-hoc UPDATE_PMS_CONFIGURATION stage remains the remedy there (Marta confirmed both are
    set from the same 5-digit Wyndham Site ID by the onboarding provider, so low risk).

  Nothing to change — the decision and implementation look correct. No follow-up needed
  unless a brand flip surfaces the mid-stay-guest edge case in practice.

  ## Agent run 2026-07-30T14:58 — why the CRS ID is critical (code-verified)

  Deep-dive into the code to ground the review; key facts:

  - The "SynXis CRS ID" (Salesforce `SynXis_CRS_ID__c`) is `SynxisConfiguration.hotel_id`
    in pms-gateway (`vendors/integrations/synxis/models/configuration.py:93`), unique per
    `(hotel_id, environment)` and `(hotel_id, username)`.
  - Every outbound SynXis API call is scoped by it: injected as a `hotelId` header on ALL
    requests (`synxis/network/plugins/headers.py:16`), in the single-reservation fetch URL
    `/api/reservation/hotel/{hotel_id}/{conf_number}` (`client.py:535`), and in reservation
    search + availability payloads (`client.py:548/690/749/807`). It is the ONLY property
    selector — wrong id means every read/write targets the wrong or dead property.
  - Reservation identity is scoped to it too: CRS confirmation numbers are only meaningful
    within a hotel_id, which is why an id change orphans all existing reservations (they
    never receive updates) and motivates the always-archive decision.
  - Brand-flip failure mode pre-fix: SynXis issues a NEW CRS id on a flip, but the
    onboarding create plan only created *missing* configs, so the stale hotel_id survived
    and the gateway kept polling the old id → dashboard showed stale/no arrivals; Ops
    hand-edited the gateway config as a workaround (the original ENT-6126 request).
  - Same 5-digit Wyndham Site ID also feeds SphCrsConfiguration.hotel_code and OHIP
    hotel_code via wyndham_pms_config_provider.py — deliberately out of scope in PR #50359.
project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 5
title: Review this ticket - should reservations always be archived?
updated: 2026-07-31 12:54:21.390196
waiting_on: null
waiting_since: null
working_on: false
---

https://linear.app/canary-technologies/issue/ENT-6126/validate-and-update-csr-idhotel-id-during-initial-configuration