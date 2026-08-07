---
area: null
completed_at: null
contexts: []
created: 2026-08-05 21:39:09.185453
defer_until: 2026-08-10 09:00:00
due: null
energy: low
id: 2026-08-05T2139-i-need-to-push-ad-to-build-their-service-layer-for
order: 5
output: |
  ## Agent run 2026-08-06T13:23Z

  ### Bottom line

  The boundary will NOT hold as things stand. Two design docs each assign
  check-in config seeding to the OTHER team, and a live project is about to
  codify onboarding scripts writing legacy v2 fields directly.

  ### Slack

  - #wyndham, 7 May 2026 — origin of the goal. You proposed "AD owns a
    migration service layer; ENT calls it."
    https://canarytechnologies.slack.com/archives/C04STT7UPRQ/p1778146926830239?thread_ts=1778005781.503109&cid=C04STT7UPRQ
    - Dana Levine: "sounds like a good plan. We can add a service before we
      migrate more than the first few hotels to v3." <- only explicit yes.
    - Guido Percu: "We already have the service, guest_experience/services/v3_migration.py"
    - Vibhor never responded to the service-layer ask in that thread.
    - Scope of the yes was MIGRATION, not configuration ownership.
  - Group DM w/ Andrea + Connor, 15 May — you flagged the onboarding-interface
    doc for the v3 rollout. Went to ENT only, never to AD.
  - Group DM w/ Andrea + Lea, 1 Jul — good/bad patterns post (Addons /
    BookingGateway / CRS good; the two Wyndham providers bad). Lea has seen the
    principle. No reply.
    https://canarytechnologies.slack.com/archives/C0B4QD01GP8/p1782916253919979?thread_ts=1782913027.991959&cid=C0B4QD01GP8
  - #tmp-check-in-configuration-location (21 Jul - 4 Aug) — 40+ msgs, all about
    WHERE the configurator UI lives and CS permissions/SAG. Zero mention of
    onboarding scripts or a service boundary.
    https://canarytechnologies.slack.com/archives/C0BKDAG8FMY
  - #project-step-configurator — Lea building configuration_library (PR #48478).

  ### Notion — the decisive finding

  Two docs assign seeding to each other:

  1. AD's "Check-In V3 Configuration" (Lea, status REVIEW ME!, team Arrivals
     Departures) https://app.notion.com/p/365814686151808c805efb429b821412
     - OUT OF SCOPE: "Config seeding / generation — enterprise owns it
       (onboarding scripts + rules framework); we consume the seeded configs."
     - Cross-pod: "Enterprise team — owns seeding... we need alignment on
       write-collision / overwrite behavior and on the FINAL/FREE locking direction."
     - "no FINAL/FREE locks in current scope, so a CS edit can diverge from an
       enterprise-seeded value — whether to add locking/guardrails is open."
     => AD has explicitly DISCLAIMED the seeding path. Their buckets are a UI facade.

  2. "Automate Check-in Onboarding" (updated 5 Aug, Linear project in Product
     Definition, lead Stephanie Barry)
     https://app.notion.com/p/39e8146861518112abedc03bf47b0dc8
     - Q-008 decided by Vibhor 2026-07-27: "v3 has no config of its own — it
       derives from v2... the automation writes the SAME v2 FIELDS."
     - "Gotcha for eng: no post_save on RegistrationCard, so writing the card
       alone won't refresh the v3 flow — REQ-005 must also trigger a re-sync
       (save the Configuration or call sync_v3_flow)."
     - REQ-011: "the first time onboarding writes REQUIRED_WITH_OCR /
       OPTIONAL_WITH_OCR for anyone. Writes id_step_with_ocr."
     - Q-016 OPEN: "Which OCR flag is authoritative: has_id_document_ocr or
       id_step_with_ocr? needs eng confirmation."  <- the tell. Onboarding is
       reverse-engineering which legacy field is source of truth. Under a real
       boundary that question never reaches the caller.
     - "Eng Design — Not started" / TOOL-415 is the forcing function.

  3. Your standard: "How Onboarding Scripts Should Interface with Product Pod
     Domains" https://app.notion.com/p/36181468615181f390fae19af8a097ad
     - "The service layer should exist and be owned by the pod BEFORE the script
       is written — not retrofitted after a script has already reached into pod models."
     - Anti-pattern: "Pod learning about an ENT rollout against its domain after
       the fact (no joint planning)."

  ### Code verification (backend/canary)

  - migrate_hotel_to_v3(hotel, *, force) takes NO config arguments. It is a
    sync, not a configure. compute_desired_flow_spec(hotel) derives the whole
    flow from hotel.check_in_configuration + hotel.has_addons + RegistrationCard
    + Incode config. So "hand me a correctly configured hotel" is not expressible.
  - No onboarding caller. `grep guest_experience onboarding/` = zero hits.
    Callers are admin_views, signals, a mgmt command, a seed command, one tmp script.
  - CheckInConfigurationWriteService has exactly ONE method,
    update_id_configuration(), taking an HTTP-shaped UpdateIdConfigurationBody.
  - Existing precedent is the anti-pattern: wyndham_pms_config_provider.py
    lines 236-250 set 12+ check_in_configuration fields then blind .save().

  ### The precise gap

  Nothing exists shaped like:
      configure_check_in(hotel, spec: CheckInSetupSpec) -> None
  where spec is typed intent (country, OCR on/off, ID verification, deposit
  posture) and the SERVICE owns which fields that maps to. Everything that
  exists is either "sync whatever is already there" (migrate_hotel_to_v3) or
  "patch one UI bucket" (update_id_configuration).

  ### Recommended next action

  Get the service-layer contract made a precondition of TOOL-415 (Eng design:
  build country/OCR reg cards in the onboarding script) BEFORE it is written,
  and get Vibhor to say AD owns it. TOOL-415 is "not started" — this is exactly
  the joint-planning moment the standard demands, and the last cheap moment.

  Audience: Vibhor (decision), Lea (builds it), Stephanie Barry (leads the
  Automate project whose eng design is at stake).

  Draft message NOT sent — awaiting Gareth's authorship per policy.

  ### Open question for Gareth

  Q-016 (which OCR flag is authoritative) is currently addressed to "eng" as if
  it were onboarding's problem to solve. Answering it directly would be the
  wrong move — it entrenches the caller knowing legacy field internals. Worth
  deciding whether to answer it or use it as the concrete example of why the
  boundary is needed.
project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 5
title: Decide the next action for making sure AD team are building the service layer
  for Check-in V3 interaction
updated: 2026-08-07 12:20:07.377638
waiting_on: null
waiting_since: null
working_on: false
---

Goal I'm working towards:
Agreement from Vibhor and AD team that they will own a configuration service layer. Enterprise and non-enterprise hotel onboarding will be strictly clients of this service. 

I.e. onboarding decides WHEN and WHICH HOTEL(S). 
Then passes key facts to a service layer. 
Service layer is FULLY responsible for handing back a correctly configured hotel. 
Might require subtle/granular arguments, but onboarding scripts should never be handrolling check-in configuration settings to achieve outcomes. ONLY using a service layer. 

First, search Slack for messages between me and Vibhor or Lea referencing configuring Check-in V3. These might also reference Wyndham. 

Search for relvant checkin v3 and step configurator docs on Notion which might impact. 

pause to let me know what you found on Slack before continuing.