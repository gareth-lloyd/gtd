---
area: engineering
contexts:
- react
created: 2026-05-29 11:33:52.557149
defer_until: null
due: 2026-05-29
energy: high
id: 2026-05-29T1133-triage-ent-6362-best-western-loyalty-member-number
order: null
output: |
  ## Agent run 2026-05-29T12:55

  ### TL;DR
  Connor's hypothesis is CORRECT and confirmed in code. The loyalty number BWH
  sees in `fact_check_in` is sourced from the **reservation's PMS-synced
  membership record** (`MembershipProgram.vendor_id`), NOT from the Best Western
  enrollment API response. When a guest enrolls *during* check-in, the reg card's
  loyalty_number was already prefilled (blank, because they weren't a member yet),
  and the new member number returned by the BW enrollment API is never written
  back to the reservation membership, the CheckIn, or the reg card. So the fact
  record stays blank even though enrollment succeeded on BWH's side. Not a
  regression / not an outage — it's a data-completeness gap. Triage severity:
  Medium (matches current Linear priority). This is a Feature-request-shaped fix,
  not a hotfix.

  ### Data flow (confirmed in code)
  1. Reg card render-time prefill sets the `loyalty_number` tag from
     `get_loyalty_info(reservation).vendor_id`:
     - backend/canary/guest_experience/steps/schema_form/prefill.py:121,160
     - backend/canary/guest_experience/steps/schema_form/service.py:51-62
       -> `MembershipProgramService.get_reservation_membership_program(reservation).vendor_id`
     - `vendor_id` is populated from PMS sync via
       MembershipProgramService.create_or_update (guest/services/membership_program.py:51+),
       and PMS membership records key on (vendor_id, raw_kind) — i.e. a PMS can
       expose multiple membership identifiers/programs (Connor's 2nd point).
  2. Guest checks the loyalty enrollment box -> enroll_guest_in_membership()
     calls the BW gateway, which returns a fresh memberId:
     - backend/canary/membership_gateways/vendors/best_western/provider.py:75,124-135
       (`member_id = response.get("memberId", "")`, wrapped as Membership.number)
     - backend/canary/check_in/services/check_in_membership.py:34-110 sets
       `CheckIn.membership_enrollment_status = ENROLLED` and returns the Membership.
       It does NOT persist `membership.number` anywhere local.
  3. push_membership_to_gateway() (check_in_membership.py:163-228) pushes the
     number to the PMS via PMSGatewayService.add_memberships(). Comment at :211
     confirms "the PMS will reconcile via normal sync." The returned
     GatewayReservation (with membership_information[].vendor_id) is discarded.
  4. CheckIn model only has `registration_card_membership_enrollment` (bool) and
     `membership_enrollment_status` (enum) — NO field for the member number:
     - backend/canary/check_in/models/check_in.py:550-561
  5. The fact_check_in loyalty column BWH receives is built downstream by dbt /
     Snowflake (NOT in this repo — no loyalty fields in
     backend/canary/data_warehouse/*), almost certainly from the reg card
     `loyalty_number` submitted/prefilled value. Since that was blank at render
     time, the fact row is blank.

  ### Why the number is missing (root cause)
  Timing + no write-back. At reg-card render the guest is not yet a member, so the
  prefilled loyalty_number is "". Enrollment happens later in the same check-in;
  the new memberId is sent to BW + pushed to the PMS but is never written back to
  the reservation's MembershipProgram, the CheckIn, or the submitted reg-card
  values that feed the warehouse. The PMS eventually reconciles the membership,
  but by then the fact_check_in row has already been created blank. (Connor's
  secondary note also applies: BW/the PMS may expose more than one identifier per
  program, so even after sync we must confirm we're surfacing the BWR loyalty
  number and not some other vendor id.)

  ### Recommended next steps (for the eventual fix — NOT done here)
  - Confirm the dbt/Snowflake source column for the BWH fact_check_in loyalty
    field (separate repo) to verify it reads the reg-card loyalty_number tag.
  - Decide the write-back point. Cleanest: when enroll_guest_in_membership()
    succeeds, persist `membership.number` back to the reservation MembershipProgram
    (via MembershipProgramService.create_or_update with the BWR raw_kind) and/or
    onto the CheckIn / submitted reg-card values so the warehouse picks it up.
  - Verify which BW identifier is the canonical loyalty number (Connor: PMS may
    have multiple). Check what BW's create_member returns vs what the PMS later
    syncs back as vendor_id for raw_kind=BWR.
  - Owning area: check_in / membership_gateways (BW). Loop in whoever owns the
    membership-enrollment-during-check-in flow. Data team may need a dbt change if
    the column needs re-pointing.

  ### Triage recommendation
  - Keep priority Medium. Reclassify: this is a real data gap but Feature-request /
    enhancement shaped (add member-number write-back), not a P1/outage. Single
    affected guest example so far (Property 14223, guest Darnel Aba-Gibson, arr
    5/18/26). Enrollment itself works; only the reporting field is blank.
  - Reproduces for any BWH guest who enrolls *during* check-in (vs already-members,
    whose vendor_id is already synced from the PMS and prefills correctly).

  ### NOT done (needs your call)
  - No Linear comment/status change/assignment posted (external-write guard).
  - No code changes — investigation only.
  - Draft Linear reply available on request if you want to respond to Connor.

  ## Agent run 2026-05-29T13:09 — CORRECTION (after viewing the ticket screenshots)

  IMPORTANT: my first run's primary root cause ("field is blank because the
  enrolled number is never written back") is WRONG. I had not looked at the three
  attached screenshots. They show the field is POPULATED, with the WRONG number.

  ### What the screenshots actually show
  - Canary Data (the fact_check_in feed BWH receives): `loyalty_member_number =
    13617126`, loyalty_enrollment = true, property 14233. (Row appears twice —
    possible join fan-out or two membership records; minor, note for later.)
  - BWH System (source of truth): member number `7887490076`, BWR, Program Code
    GMS, Tier BLUE, Status ACTIVE, Member Since / Enrollment 05/18/2026.
  - So Canary sends 13617126 (8 digits) while the real BWR loyalty number is
    7887490076 (10 digits). NOT blank — wrong. This is Connor's SECOND hypothesis
    ("PMS may have more than one identifier; we may surface the wrong one"), and
    the first run's timing/write-back theory does not explain a populated wrong
    value.

  ### Verified selection path (code)
  Reg-card loyalty_number prefill -> get_loyalty_info (service.py:51-62) ->
  MembershipProgramService.get_reservation_membership_program (membership_program.py:168-177)
  -> get_canonical_membership (membership_program.py:106-165):
    - Takes guest.membership_programs, keeps those whose raw_kind is valid for the
      hotel's program identifier (BWR for Best Western),
    - sorts by (expiry_at, id) DESC,
    - returns the first record's `vendor_id`.
  => 13617126 is the `vendor_id` of whichever BWR-valid MembershipProgram won that
  sort for this guest. The fix question is "why is that vendor_id not the guest's
  BWR loyalty number?"

  ### Strong supporting clue
  membership_program.py:205-216 `create_random_best_western_membership` sets
  `vendor_id=""` with the comment "Best Western doesn't supply a vendor_id." If
  real BW PMS syncs also don't reliably populate vendor_id with the loyalty
  number, then 13617126 is likely a *different* PMS identifier (internal profile/
  membership id) that landed in vendor_id — exactly Connor's concern. The "Program
  Code GMS" vs the "BWR" badge in the BWH screen also signals BW exposes multiple
  program/identifier codes.

  ### Also confirmed
  Enrollment is ASYNC (check_in.py:1476-1484 -> enroll_guest_in_membership.apply_async)
  and only updates membership_enrollment_status; it never writes the enrolled
  memberId to MembershipProgram/CheckIn (check_in_membership.py:34-228). So even
  if we wanted to surface the enrollment-API number, nothing persists it today.
  This is a real secondary gap but is NOT the cause of the wrong value.

  ### Honest confidence / what's still unverified
  - NOT verified: that fact_check_in.loyalty_member_number is sourced from the
    reg-card loyalty_number tag specifically. The dbt/Snowflake lineage is in a
    separate repo I did not inspect. It may instead read MembershipProgram.vendor_id
    directly. Either way the surfaced value is the same vendor_id, so the
    wrong-identifier root cause holds — but the exact column lineage is an
    assumption.
  - KEY UNKNOWN (requires prod data, NOT done — needs approval to query): what is
    13617126? Need this guest's MembershipProgram rows (vendor_id, raw_kind,
    expiry_at, id) for guest_uuid 56f74d9c-7cc6-4e4b-8d00-7fc7821c7d2e and the PMS
    membership sync payload, to see which identifier the PMS exposes for the BWR
    membership and why vendor_id != 7887490076. That is the real next triage step.

  ### Revised recommendation
  - Reframe the issue: WRONG loyalty number surfaced to customer reporting (data
    correctness), not a missing/blank field. Arguably worse than "blank" because
    it's silently incorrect, but still not an outage. Medium priority is fine.
  - Next step is a data lookup (above), not a code change yet. Once we see the
    MembershipProgram rows + PMS payload we can decide between: (a) map the correct
    PMS identifier into vendor_id during sync, (b) fix selection if multiple BWR
    records exist and we pick the wrong one, or (c) persist the BW enrollment
    memberId back to MembershipProgram as the authoritative loyalty number.
  - Do NOT tell Connor "the field is blank / we don't store it" — that's wrong and
    would be a high-impact public error. The honest message is: confirmed we're
    surfacing a different PMS identifier than the BWR loyalty number, investigating
    which PMS field carries the real number.

  ## Agent run 2026-05-29T13:30 — ROOT CAUSE CONFIRMED (shell + code)

  Definitive. PMS for this hotel is AUTO_CLERK. Read-only Canary + code review of
  the pms-gateway AutoClerk integration pin it down exactly.

  ### Canary shell (guest 245467564, hotel 129239235, sso 14233)
  - Exactly ONE membership program: raw_kind='BWR', vendor_id='13617126',
    raw_level='BLUE', canonical_level='BW_BLUE', created 2026-05-18 14:56 (≈23 min
    after the 14:33 check-in), updated 2026-05-21. So it was written by PMS sync,
    not the enrollment code path (which never writes MembershipProgram).
  - get_loyalty_info(reservation) -> vendor_id='13617126' (matches the feed).
  - Gateway ids: reservation 3bbf5962-48b6-4cd6-82e8-9b7d3f07f442, guest
    3e2bcbde-369c-499d-93e6-8b9790d3af48, confirmation BB10184809000. hotel.pms=AUTO_CLERK.

  ### THE BUG (pms-gateway AutoClerk loader)
  backend/pms-gateway/vendors/integrations/autoclerk/services/load.py:282-295
  `_extract_memberships`:
      Membership(
          # FIXME: We need an ID for the membership but Autoclerk does not provide
          # one so we will temporarily use the guest's profile ID.
          vendor_id=guest.profile_id,          # <-- profile_id used AS the loyalty no.
          raw_kind=DEFAULT_LOYALTY_PROGRAM,     # "BWR" (load.py:46-47: all AutoClerk = BW)
          raw_level=guest.loyalty_level,
      )
  - AutoClerk's guest payload has NO member-number field — its GuestSchema only has
    profile_id, loyalty_level, name, contact (autoclerk/schemas/guest.py:8-39).
  - So when AutoClerk sends loyalty-level, the loader stamps the guest's AutoClerk
    profile_id (=13617126) into Membership.vendor_id as a placeholder (explicit
    FIXME). That syncs to Canary MembershipProgram.vendor_id and flows to the reg
    card prefill and BWH's fact_check_in.loyalty_member_number.
  - The real BWR loyalty number (7887490076) only exists in BW's loyalty system /
    the BW enrollment API response; AutoClerk never relays it and Canary never
    persists the enrollment memberId. Hence the mismatch.

  ### Verdict on Connor's notes
  Both correct and now precisely located: (1) "number is coming from the PMS not
  the enrollment API" -> yes, it's the AutoClerk profile_id via PMS sync. (2) "PMS
  may have more than one identifier; see if it exposes the right one" -> AutoClerk
  exposes only profile_id + loyalty_level and NO loyalty number at all, so there is
  no right one to map; the placeholder is a known stopgap (FIXME).

  ### Pending final confirmation (PMS Gateway shell — script handed over)
  Expect gateway Guest 3e2bcbde-...'s guest.vendor_id (AutoClerk profile_id) and
  its Membership.vendor_id to both equal 13617126. If so, airtight. (Code already
  proves the mechanism; this just shows the value end-to-end.)

  ### Scope / blast radius
  This is NOT guest-specific or enrollment-specific. EVERY AutoClerk (= all Best
  Western on AutoClerk) guest with a loyalty level gets profile_id as their
  loyalty_member_number in the data feed. The enroll-during-check-in case is just
  how BWH noticed. Worth a count of affected MembershipProgram rows (raw_kind=BWR
  where vendor_id == the guest's AutoClerk profile_id) to size it.

  ### Fix direction (NOT implemented — needs owning team + product call)
  The placeholder must be replaced with a real loyalty number source. Options:
  (a) Get AutoClerk to send the BWR number and map it (best, but depends on the PMS
      feed — may not be possible; that's the root limitation).
  (b) Persist the BW enrollment API memberId back to the membership as authoritative
      (covers enroll-via-Canary, not pre-existing members).
  (c) Stop populating loyalty_member_number from profile_id when we don't have a
      real number (better to send blank than a wrong number to customer reporting).
  Owning areas: pms-gateway AutoClerk integration + membership_gateways/check_in.
  Likely also a data/dbt note since the bad value is already in the warehouse feed.

  ### Updated triage recommendation
  - Confirmed data-correctness bug with a known FIXME root cause; reproduces fleet-
    wide for AutoClerk/BW. Still not an outage. Medium is defensible; could argue
    higher given it's wrong data in customer reporting across all BW-on-AutoClerk.
  - Ready to draft a corrected, specific Linear reply to Connor on request.

  ## Agent run 2026-05-29T13:45 — VENDOR + VALUE ORIGIN CONFIRMED (PMS gateway shell)

  Verified the vendor independently (didn't trust hotel.pms alone) and traced where
  13617126 actually comes from.

  - Account 25599 = "Best Western Bolingbrook Hotel", type='autoclerk' (Autoclerk).
    AutoClerk assumption CONFIRMED.
  - The 13617126 value lives in the RESERVATION-LEVEL MembershipInformation
    (reservations/models/membership_information.py) for reservation 259570735:
    vendor_id='13617126', raw_kind='BWR', raw_level='BLUE'. This is what syncs to
    Canary MembershipProgram and out to fact_check_in.
  - The reservation guest's CURRENT AutoClerk profile_id (gateway Guest.vendor_id)
    is 14621898 — NOT 13617126. And that gateway guest has 0 live guest-level
    memberships. A separate guests.Membership row with vendor_id=13617126 exists on
    a different guest. => 13617126 is an OLDER/different AutoClerk profile_id; the
    guest was re-profiled (most likely the BW enrollment spun up a new profile
    14621898), while the reservation's MembershipInformation kept the stale
    profile_id 13617126.
  - Net: the loyalty_member_number BWH sees is an AutoClerk guest profile_id reused
    as the membership vendor_id (per the FIXME in autoclerk/services/load.py:282-295),
    and after re-profiling it's even a STALE profile_id. The real BWR number
    7887490076 is never present in the AutoClerk feed.

  Correction to my 13:30 note: the profile_id reused is NOT this guest's current
  profile_id (14621898); it's a prior/other profile_id (13617126) carried on the
  reservation-level membership. Mechanism (profile_id-as-vendor_id) unchanged and
  confirmed; the specific record is reservation-level MembershipInformation, and
  profile churn explains the exact value.

  ## Agent run 2026-05-29T13:58 — POSTED to Linear (user-approved)

  Root-cause comment posted to ENT-6362 (comment id e89843b1-f0c2-4520-b34b-
  45f68f8ad560, authored as Gareth Lloyd). Approved explicitly by Gareth ("yes
  post"); kept joint Gareth+Claude attribution and the fix-options section.
  Content = confirmed AutoClerk profile-id-as-loyalty-number root cause with
  evidence (fact value 13617126 vs real 7887490076, reservation MembershipInformation
  source, autoclerk/services/load.py:282-295 FIXME, fleet-wide scope, 3 fix
  options). No status/assignee/priority change made — left to the user.
project: 2026-04-16T1210-unblock-team
source_id: https://linear.app/canary-technologies/issue/ENT-6362/best-western-loyalty-member-number-in-fact-check-in
tags:
- morning-gtd
- linear
time_minutes: 15
title: 'Triage ENT-6362: Best Western - loyalty_member_number in Fact Check In'
updated: 2026-05-29 13:58:10.009528
waiting_on: null
waiting_since: null
working_on: false
---

ENT, Triage state, unassigned. I'm on Enterprise on-call today. https://linear.app/canary-technologies/issue/ENT-6362/best-western-loyalty-member-number-in-fact-check-in