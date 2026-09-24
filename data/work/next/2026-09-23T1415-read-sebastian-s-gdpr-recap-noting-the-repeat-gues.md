---
area: null
completed_at: null
contexts:
- consume
created: 2026-09-23 14:15:48.910147
defer_until: null
due: 2026-09-24
energy: low
id: 2026-09-23T1415-read-sebastian-s-gdpr-recap-noting-the-repeat-gues
order: null
output: |
  ## Agent run 2026-09-24T10:30:00+02:00

  Read Sebastian's recap in full (msg of 22 Sep 18:08 UTC in the "Subject: GDPR Compliance" thread with Tanya Chib, Privacy Rules):
  https://mail.google.com/mail/?authuser=glloyd@canarytechnologies.com#all/thread-f:1868802491066946609|msg-f:1877056434435186253

  ### What the recap says (all five sections)

  - Retention/obfuscation: invoice/fiscal retention is the hotel's problem as controller. 30 days post-checkout as Canary's default anonymisation window is defensible for a processor if clarified with the controller upfront. Guests do not need notifying; hotels do — one standard notice framed as part of a broader systems/UI overhaul, 1-2 week window to flag data to retain, opt-out per account. Tanya offered to draft the notice.
  - Video kiosk (remote human operator): notice at point-of-camera; separate explicit consent for recording (purpose named: quality + AI training); flow must work if recording declined; DPIA required before EU launch (Canary writes it incl. data flow, infra, storage location, access; goes to Tanya then Alex). For the future AI-agent version Tanya will send ~20 scoping questions.
  - Voice recordings: notice-at-call-start is fine (implied consent). ~2 years defensible on product-improvement basis. Once PII removed GDPR stops applying; re-check anonymisation every 5-7 years.
  - Repeat-guest profiles: see below.
  - Middle East: non-US processing runs in Germany. KSA/UAE residency and EU-transfer-with-clauses (DPA?) still open; Tanya checking with a contact.

  ### Repeat-guest profile implications for CRM – Unified Guest Record

  Project: P-PMS-2229 "CRM – Unified Guest Record", lead Mike Bretherick, PMS Engineering, status Ready for Eng, target 2026-11-05 (https://linear.app/canary-technologies/project/crm-unified-guest-record-9d7ee2032df0). Product owner Nicolas Garnier. Slack channel C0C1YRB7U6N. Parked eng design: https://app.notion.com/p/canarytechnologies/CRM-Unified-Guest-Record-39781468615180b28e85dde4a519ed67 . PRD: https://app.notion.com/p/canarytechnologies/Upsells-Guest-Records-MVP-39081468615180ee8093c3c4922d22ec

  Tanya's three tiers map directly onto the project's scope choices:

  1. Per-hotel only (current MVP: "one guest record per person, per hotel; cross-hotel sharing out of scope") is the safe tier. Same controller both sides, Canary stays processor. No new legal basis needed beyond what the hotel already has. The recap does not constrain this.
  2. Intra-group / portfolio is "workable": contact data potentially on legitimate interest, sensitive data (passport, DOB, biometric) on consent. NOTE the Linear description has "per ~~property~~ portfolio" struck through in the summary line, so someone is already nudging scope toward portfolio. The moment that happens, the GuestAccount model fields split into two buckets: name/email/phone/address/language (LI-arguable) vs date_of_birth, nationality, country/place_of_birth, IdDocument, GuestAccountIdImage (consent). The data model should carry that distinction rather than treat the record as one blob.
  3. Inter-group sharing needs a data-subject notice per controller-to-controller transfer. "Materially more complex". Effectively rules out cross-brand/cross-management-company records without a consent product. Consistent with the project already excluding it.

  Two points from the recap that are decisive for the open project questions:

  - Who initiates linking decides Canary's status. Tanya: if Canary initiates the sharing rather than acting on hotel instruction, Canary becomes a controller. Project next-step 2 is exactly the unresolved "automatic (existing eng design, no human review) vs staff-initiated link/unlink (kickoff decision)" conflict. Within a single hotel either is fine. Across hotels, automatic Canary-side matching is the controller-making move; staff-initiated linking keeps the "on hotel instruction" framing. This should be the argument that settles step 2 if portfolio scope is ever taken.
  - The "group" definition is a prerequisite to any formal view (brand vs management company). Canary already has two competing answers in code: Portfolio (hotels grouped for staff access, via PortfolioService) and guest_account.AccountPool (named per brand, e.g. "EXAMPLE-HOTEL-BRAND", GuestAccount unique on (pool, email)). AccountPool is already an intra-group guest identity keyed by brand, so the guest_account app has implicitly answered "group = brand". The Unified Guest Record work needs to either reuse that or explicitly diverge, and the definition Sebastian gives Tanya should match whichever is chosen.

  Retention interaction (project next-step 4):
  - Tanya's 30-day processor default is defensible, but the live rollout is the GDPR: PMS data anonymisation project (P-EMEA-1927, lead Yauheni Danchanka, https://linear.app/canary-technologies/project/gdpr-pms-data-anonymisation-4a24518aa6a7) with an EU regional default of 7 days via ConfigurationRuleEngine (EMEA-350). Canary side has Hotel.pii_retention_days (1..1827 days, null = not swept). A 7-day EU default leaves essentially no guest history for a repeat-guest record, and applies to EU citizens at US properties too, so "US first" does not dodge it.
  - Martijn Dekker's pending async doc (does it apply to all hotels by default, all guests or only Canary check-ins, and should guest records get a longer schedule, e.g. 3 years) is the piece that reconciles the two. Tanya's "one notice to hotels, 1-2 week retain-window" is the mechanism if the default changes for existing customers.
  - A guest record that must outlive the reservation-level sweep needs its own retention purpose stated to the controller upfront; the recap's "provided it's clarified with the controller upfront" is the hook.

  Consent (project next-step 8, unowned, Nicolas + Sebastian): the recap is the framework Martijn asked for on 15 Sep. The deliverable Sebastian promised Tanya (product specifics + data flow diagram + infrastructure components + group definition, before a formal view) is the same artifact step 8 needs. Nobody owns producing it yet.

  Cross-region (project next-step 6): non-US processing is in Germany. A record spanning US and EU regions is itself a transfer and would need to be in the data flow diagram. KSA/UAE residency is open, which matters if any Middle East portfolio is a target.

  ### Suggested follow-ups (not done, nothing sent)

  - Forward the recap (or the repeat-guest section + the two decisive points above) to Mike Bretherick and drop a pointer in the project Slack channel C0C1YRB7U6N, so steps 2, 4 and 8 pick it up. Sebastian's recap CC list (Martijn, Sebastian, Vikram, Ben, Zach, Jackie, Andrea) does not include Mike or Nicolas.
  - Ask Mike who owns producing the data flow diagram + product specifics for Tanya; propose it doubles as the step 8 consent write-up.
  - Flag the "per ~~property~~ portfolio" edit in the project summary: if portfolio is the intent, the LI-vs-consent field split and the staff-initiated linking constraint become design requirements now, not later.
project: 2026-07-20-gdpr
source_id: https://mail.google.com/mail/?authuser=glloyd@canarytechnologies.com#all/thread-f:1868802491066946609
tags:
- morning-gtd
- gmail
- from-awareness
time_minutes: 15
title: Read Sebastian's GDPR recap, noting the repeat-guest profile implications for
  the CRM Unified Guest Record work
updated: 2026-09-24 10:14:58.898432
waiting_on: null
waiting_since: null
working_on: false
---

Sebastian's recap of the call with Tanya Chib (I'm CC'd). Key for guest profiles: intra-group sharing workable (contact data on legitimate interest, sensitive data on consent); inter-group sharing needs data-subject notice per controller-to-controller transfer; if Canary initiates it rather than acting on hotel instruction, Canary becomes a controller. Need product specifics, a data flow diagram and a definition of 'group' (brand vs management company) before a formal view. Also: 30-day post-checkout anonymisation defensible; hotels get one notice with 1-2 week retention window; DPIA for video kiosk; KSA/UAE residency open. Ties to Ian Clark's pointer that Mike runs CRM – Unified Guest Record.
https://mail.google.com/mail/?authuser=glloyd@canarytechnologies.com#all/thread-f:1868802491066946609