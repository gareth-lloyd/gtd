---
area: null
contexts:
- react
created: 2026-07-22 10:42:23.584798
defer_until: null
due: null
energy: medium
id: 2026-07-22T1042-triage-ent-6926-bw-hotelkey-transition-validation
order: null
output: |
  ## Agent run 2026-07-22T12:24:27Z — Triage ENT-6926

  ### TL;DR
  Root cause found. The "Validate PMS Config" step for BW property 37140 fails
  because HotelKey's single-reservation lookup returns
  `400 pms_reservation_not_found` ("Reservation not found in PMS") for EVERY
  confirmation number the validator samples — across 3 separate attempts and 6
  different confirmation numbers. This is a HotelKey integration lookup problem,
  NOT a Canary onboarding-tooling bug and NOT a transient fetch issue. Bulk
  reservation sync into Canary is working fine (the hotel is live, sending
  check-in invites and processing reservations), which is why the "fetch run"
  completed but "Validate PMS" still failed.

  ### Entities (verified against prod logs / Groundcover)
  - Hotel: `bw-37140` = "GLo Best Western Enid OK Downtown/Convention Center
    Hotel", Enid OK. hotel_id 129234586, uuid 00f789e7-88eb-4494-a989-18a1997e20fa,
    SSO org 313, account_uuid 4adb0fd7-a69d-4c73-8ad3-a5be5f425109.
  - Cohort: id 42703, uuid 826c0047-235f-4d9c-a2dc-490c48d0385d,
    onboarding_type `best_western_msa`, state `in_progress`.
  - Batch: id 73669, uuid eaea32e5-9f38-4fbb-b286-7b1e75a7d386, label
    "Best Western MSA - Validate PMS Config", script_type
    `validate_pms_configuration`, plan `ConfigurePMSIntegrationValidatePlan`.
  - PMS: HotelKey. Region: us-west-2 (US).
  - Ticket filed by tdrakeley (human); Enterprise Triage; no priority; no labels
    (NOT "Routed by AI").

  ### Root cause (evidence)
  The validate step does a LIVE single-reservation re-fetch from HotelKey for up
  to 3 candidate reservations (arrival within +/-6 days of today, newest-synced
  first). Each call is:
    POST https://gateway.canarytechnologies.com/api/accounts/me/hotelkey/validate
    {"validation": "fetch_reservation", "args": {"confirmation_number": "<N>"}}
  Every call returned:
    400 Bad Request -> {"success": false, "error": {"type":
    "pms_reservation_not_found", "message": "Reservation not found in PMS"}}

  Groundcover shows this repeated across 3 validation runs on 2026-07-21:
  - 19:47 run 290760: confirmation 53216 -> not_found
  - 19:53 run 290762: 53216, 53212, 53218 -> all not_found
  - 20:54 run 290775: 52889, 53064, 53065 -> all not_found
  6 distinct confirmation numbers, 0 found. So it is systematic, not a stale
  sample. Meanwhile bulk sync works: reservation confirmation 52710
  (res 267135638) was processed by the purchase-order cron, and check-in invites
  are actively sending for this hotel — the integration is otherwise healthy.

  Interpretation: HotelKey's `create_or_update_reservation(confirmation_number)`
  cannot resolve the identifier Canary stores as `pms_confirmation_number` for
  this property. Likely either (a) the confirmation-number key Canary sends is
  not HotelKey's expected lookup key for single-reservation fetch, or (b) this
  property's HotelKey API access for single-reservation fetch is not fully
  activated even though bulk pull works. Either way it is a HotelKey
  vendor-integration question, best answered by INT / PMS-Gateway.

  ### Code path (for whoever picks this up)
  - Plan: `backend/canary/onboarding/plans/configure_pms_integration_validate_plan.py`
    (`ConfigurePMSIntegrationValidatePlan.execute`). Candidate selection in
    `_perform_validation` (~lines 157-201): up to
    `FETCH_RESERVATION_CANDIDATE_COUNT = 3`, arrival +/-6 days, newest first,
    excl. demos; `_get_confirmation_number` uses `pms_confirmation_number`.
  - HotelKey validations are only [AUTHENTICATE, FETCH_RESERVATION]:
    `backend/pms-gateway/vendors/integrations/hotelkey/services/configuration.py:117`.
    Auth PASSED here (we reached fetch_reservation), so this is the
    FETCH_RESERVATION leg failing -> `ERROR_PMS_VALIDATION_FAILED_FETCH_RESERVATION`.
  - Gateway per-field checks: `backend/pms-gateway/accounts/services/account_validation.py`
    `fetch_reservation` (~124-156). Here it never got that far — HotelKey itself
    returned not_found before per-field validation.

  ### Classification
  - Primary cluster: 9 — PMS integration (HotelKey, "PMS validate",
    pms_reservation_not_found).
  - Secondary: 4 — Hotel transition / BW MSA go-live.
  - Misroute?: PARTIAL. Cluster 9 default routing = INT or PMS-Gateway. The
    catalog carve-out keeps Enterprise as owner when the failure blocks a
    go-live, which it does (BW MSA cohort go-live). So: Enterprise legitimately
    owns the ticket as go-live coordinator, but the technical root cause
    (HotelKey single-reservation lookup) needs INT / PMS-Gateway (HotelKey vendor
    integration) to diagnose. Recommend co-assigning / looping in INT rather than
    a clean reassignment. Note ticket is human-filed, not AI-routed, so the
    auto-misroute gate does not fire.
  - KB article: none exists for Cluster 9 (HotelKey PMS validate). Good candidate
    for `/enterprise:add-to-kb` once resolved.

  ### Action mode: No-write investigation + INT hand-off
  Not a Canary DB script and not an obvious Enterprise-side code fix. Suggested
  next steps:
  1. Ask INT / PMS-Gateway (HotelKey integration owner): why does
     `POST /api/accounts/me/hotelkey/validate` (fetch_reservation by
     confirmation_number) return `pms_reservation_not_found` for this property
     (129234586) for every confirmation number, while bulk reservation pull
     succeeds? Is the confirmation-number the correct lookup key for HotelKey
     single-reservation fetch, or does HotelKey key on a different id?
  2. Confirm with HotelKey whether this property's single-reservation fetch API
     is fully activated (parallel to the known per-property key-activation gap).
  3. Product/robustness follow-up (Enterprise, optional): the validator hard-fails
     the whole go-live step when 3 sampled confirmation numbers cannot be live
     re-fetched. If HotelKey single-fetch is inherently unreliable for freshly
     transitioned properties, consider making this leg tolerant (e.g. treat
     bulk-sync + auth as sufficient) — but only after INT confirms the lookup
     semantics.

  ### Escalation signals
  - Blocks a BW MSA go-live (cohort in_progress) — flag if there is a go-live SLA.
  - The CS/onboarding operator already retried (created a new fetch batch
    555b304e-1c20-4831-bb0a-8691b46fc118 from the validation at 21:55) and it
    failed the same way — retrying alone will not fix it; the HotelKey lookup
    question must be answered first.

  ### Draft Linear comment (NOT posted — for your review/approval before sending)
  ---
  Root cause: the Validate PMS step for BW-37140 (hotel 129234586) fails on the
  HotelKey FETCH_RESERVATION check. Every single-reservation lookup to
  gateway .../hotelkey/validate (fetch_reservation by confirmation_number) returns
  400 pms_reservation_not_found. This happened across 3 validation runs on
  2026-07-21 (19:47, 19:53, 20:54) covering 6 different confirmation numbers
  (53216, 53212, 53218, 52889, 53064, 53065); none were found. Auth passes and
  bulk reservation sync is working (the hotel is live and sending check-in
  invites), so the fetch run completing is expected; the failure is isolated to
  HotelKey single-reservation lookup by confirmation number. This looks like a
  HotelKey integration question (does HotelKey key single-reservation fetch on
  the confirmation number Canary stores, or is this property's single-fetch API
  not fully activated?) and likely needs INT / PMS-Gateway input. Re-running the
  fetch batch alone did not help.
  ---

  ### Notes / limitations
  - Local canary MCP backend was not reachable (not running), so entity checks
    were done via Groundcover prod logs (tenant canary, cluster
    prod-main-us-west-2) rather than the MCP hotel tools. All IDs above are from
    live logs.
  - Did not post anything to Linear or anywhere external. Read-only triage only.

  ## Agent run 2026-07-22T12:36:59Z (addendum) — transition-artifact cause confirmed in code

  Confirmed in code that the leading cause is the PMS transition itself: the
  validator samples reservations Canary already holds and re-fetches them from
  HotelKey by their stored `pms_confirmation_number`; after a PMS switch those
  are OLD-PMS confirmation IDs that HotelKey never issued -> not_found.

  Evidence in `configure_pms_integration_validate_plan.py` (backend/canary/onboarding/plans):
  - Lines 171-175 (verbatim comment): "The FETCH_RESERVATION validation succeeds
    if it's possible to retrieve any reservation from the PMS. The endpoint
    requires an argument, which we grab from the most recently synced
    reservations: after a PMS switch the hotel still holds reservations from the
    previous PMS that the new one cannot fetch, so prefer fresh reservations and
    try a few candidates."
  - Candidate query (176-185): reservations with arrival +/-6 days, created_via
    RESERVATION, non-demo, ordered by `canary_gateway_updated_at` desc, take 3.
  - `_get_confirmation_number` (204-219): uses `pms_confirmation_number` (non-OHIP),
    falling back to `reservation.confirmation_id`. For a pre-transition reservation
    this is the previous PMS's confirmation number.

  So the newest-synced-first + 3-candidate retry is an explicit mitigation for
  exactly this transition case — but it FAILED here: all 3 candidates per run and
  6/6 confirmation numbers across 3 runs returned not_found. That means the
  freshest reservations Canary currently holds for this property are still
  old-PMS records (no HotelKey-native reservations yet in the +/-6-day arrival
  window), OR HotelKey genuinely cannot fetch them by confirmation number.

  Revised read on ownership/next steps:
  - Most likely benign timing/transition artifact: once real HotelKey-originated
    reservations land in the +/-6-day arrival window (or the on-demand fetch
    refreshes these reservations with HotelKey-native confirmation numbers),
    re-running Validate PMS should pass. Worth checking whether this property has
    any NEW (post-cutover) reservations in Canary yet.
  - Still worth an INT / PMS-Gateway sanity check IF the property has genuinely
    post-cutover reservations whose `pms_confirmation_number` is HotelKey-native
    and those still return not_found — that would point to a HotelKey
    single-fetch API / activation issue rather than a transition artifact.

  ### Revised draft Linear comment (NOT posted)
  ---
  Root cause: the Validate PMS step for BW-37140 (hotel 129234586) fails on the
  HotelKey FETCH_RESERVATION check. It samples reservations Canary already holds
  and re-fetches each from HotelKey by its stored confirmation number; every
  lookup returns 400 pms_reservation_not_found (6 different confirmation numbers
  across 3 runs on 2026-07-21: 53216, 53212, 53218, 52889, 53064, 53065). Auth
  passes and bulk sync is healthy (the hotel is live and sending check-in
  invites), so the fetch run completing is expected.

  This is most likely a side effect of the PMS transition: the validator re-fetches
  the most-recently-synced reservations, but after a PMS switch the property still
  holds reservations from the previous PMS carrying the OLD PMS's confirmation IDs,
  which HotelKey cannot fetch. The onboarding code even calls this out and tries to
  avoid it by preferring fresh reservations and trying 3 candidates; here all
  candidates still resolve to pre-cutover confirmation numbers, so it fails.

  Suggested next step: confirm whether this property has any NEW (post-cutover)
  HotelKey-originated reservations in Canary within a +/-6 day arrival window yet.
  If not, this should clear once fresh HotelKey reservations sync and Validate PMS
  is re-run. If it DOES have post-cutover reservations with HotelKey-native
  confirmation numbers that still return not_found, loop in INT / PMS-Gateway to
  check the HotelKey single-reservation fetch API / property activation.
  ---

  POSTED to Linear as Gareth Lloyd on 2026-07-22T12:39:40Z (comment id
  0123af97-be28-4838-8541-65519bf7d09e), per explicit user approval in-session.
project: null
source_id: https://linear.app/canary-technologies/issue/ENT-6926/bw-hotelkey-transition-validation-failed-despite-fetch-run-completing
tags:
- morning-gtd
- linear
time_minutes: 20
title: 'Triage ENT-6926: BW Hotelkey transition — validation failed despite fetch
  run completing'
updated: 2026-07-22 15:44:14.433798
waiting_on: null
waiting_since: null
working_on: false
---

ENT team, in Triage, unassigned. Best Western Hotelkey transition blocker.
https://linear.app/canary-technologies/issue/ENT-6926/bw-hotelkey-transition-validation-failed-despite-fetch-run-completing