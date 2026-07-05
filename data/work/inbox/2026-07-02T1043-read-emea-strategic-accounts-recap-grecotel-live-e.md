---
area: null
contexts:
- consume
created: 2026-07-02 10:43:04.336333
defer_until: null
due: null
energy: low
id: 2026-07-02T1043-read-emea-strategic-accounts-recap-grecotel-live-e
order: null
output: |
  ## Agent run 2026-07-02T16:20 — read & summarized

  Read Sebastian Cahill's EMEA Strategic Accounts meeting recap (Jun 30, 2026) in #emea.
  Source: https://canarytechnologies.slack.com/archives/C083M6Q65PX/p1782839158966589

  The recap is broader than the title — 6 accounts, a pipeline section, and a key-risks
  roundup. Distilled below (engineering-relevant items flagged).

  ### 🔴 Eurostars — Guest messaging PAUSED (GDPR)
  - Raquel's legal team told Eurostars to temporarily deactivate WhatsApp guest
    messaging (consent-at-booking concern). Landed 10 min before the call.
  - NOT a product/platform issue — compendium-via-QR and everything else stays live.
    KPIs strong but pausing WhatsApp will dent the metrics Javier championed.
  - Canary read: transactional (check-in/welcome) messages are fine; upsells = marketing
    and need consent. Need Eurostars to pinpoint exactly where the concern sits.
  - Manuel + Manolo face-to-face in Barcelona Thursday; trying to fold their legal in.

  ### 🟡 Travelodge UK — Google Wallet approved, CYR go-live this week
  - Google Wallet approved. CYR pilot believed ready; Isaac confirming with Holly/Vasudha/Gleb.
  - UDF decision: Gleb fine with reporting-only — no push to UDFs for now.
  - Biggest remaining workstream: ingesting prepaid early-in/late-out packages from their
    site and honoring them for auto-check-in — NOT a CYR launch blocker (vibhor to scope).
  - "Choose-Your-Room" flagged as a potential Canary upsell/upgrade differentiator vs
    Alliants (TUI has asked too). Owners: vibhor (CYR items + package ingestion), Isaac
    (go-live readiness before Holly OOO).

  ### 🔴 Doyle Collection — First voice bookings in; pivot to repositioning
  - First bookings landed (2 on Dupont via Voice, after welcome message shortened).
    Marylebone still zero.
  - Sentiment shifted from ~99% likely-to-churn-voice → may keep it if expectations reframed.
  - Strategy: reposition Voice for luxury (Jonathan Kennell's deck) — lead with
    missed-call/FAQ/triage value, deprioritize "we'll take your bookings"; reset the
    30%-of-revenue expectation.
  - +90 days of Voice free (extension) for runway. Hold repricing until after extension;
    luxury AI-second/human-first usage could naturally drop them to a lower SaaS tier.
  - Open eng item (carried): Australia (+61) call-blocking + multi-rate-code (James Saram).
    Jonathan + James OOO Mon–Wed incl. Jul 1; Sebastian covering.

  ### 🔥 Kempinski — MSA close imminent; implementation call Wed Jul 1
  - Contract in final legal tweaks; MSA hopefully signed ~Jul 1. Frutt Mountain Resort
    order form to be reminded to Daniel.
  - Tablet Reg is priority #1 and unlocks the other properties (want it live fast across
    multiple hotels incl. full digital check-in). Kiosk only envisioned at Frutt. Loyalty
    is a separate parallel call, not a blocker.
  - Risk note ties this to SEC-421 (must close to unlock Tier 2 ahead of Aug 15).

  ### 🟢 Grecotel — LIVE! (the headline)
  - Grecotel LIVE as of this week after the opt-in fix validated end-to-end.
  - Next: proactive reporting design (standard KPIs mirroring DeLuna) — Aksel + James +
    Sebastian meeting Thursday. Data story anchored on marketing opt-in rate / # opt-ins
    for retargeting, plus conversion (native app requires download, so Canary's conversion
    + >75–80% messaging deliverability should shine). Alex Kelly to implement reporting,
    let it run ~1 week, then share a positive story.

  ### 🟡 DeLuna — Rates/availability working; payment path is the blocker
  - Correctly pulling rates + availability on a live DeLuna property via NeoBookings (same
    for web chat). Integration slot form signed.
  - Payment gateway unresolved: ambiguity whether DeLuna is on PayNoPain vs Payments-by-Septeo
    (maybe synonymous); old contact left, manager unresponsive. Must confirm PayNoPain is
    usable by Ulyses and hits DeLuna's existing acquiring account. Interim: push DeLuna to
    Stripe while NeoBookings payment integration is built.
  - Same repositioning theme as Doyle: bookings good for order-taking, weak for exploration.
    Owners: Aksel (PayNoPain vs Septeo + acquiring question, lock NeoBookings), Brad
    (viable payment path + ETA), Manolo (Stripe interim).

  ### 🎯 Pipeline
  - Marriott — folio-split ask (Manuel to loop in James Saram + vibhor).
  - IHG MEA — big, fast-moving. Dubai corporate office controls MEA + parts of APAC. Likely
    Africa first (no authority-integration restrictions), then Dubai. They want a clear
    status + timeline on Department of Tourism integration (the gating question).
  - ME ID-scanner ↔ authority integrations: Dubai (~5x Abu Dhabi) is priority. H2O is the
    only player integrated with Abu Dhabi authorities today; Samsotech (Dubai) went quiet.
    Manuel in Dubai first week of Sept.

  ### ⚠️ Key risks (Sebastian's roundup)
  - Eurostars WhatsApp paused on GDPR — messaging is our differentiator; need fast legal
    resolution or KPIs slip.
  - Doyle Marylebone still zero into Jul 1/Jul 8 — reposition must land before extension.
  - Travelodge CYR must go live this week before Holly OOO.
  - DeLuna payment path unproven + partner ambiguity; vendor unresponsive.
  - Kempinski MSA/SEC-421 must close to unlock Tier 2 ahead of Aug 15.
  - IHG MEA Dept. of Tourism integration not yet available; timeline ask is gating.

  ### Nothing actioned
  No external writes made. This was a read/consume item — no reply posted, no tickets
  touched. Eng-adjacent threads worth watching if they surface as tickets: Travelodge
  package-ingestion → auto-check-in, Doyle Australia (+61) call-blocking + multi-rate-code,
  Kempinski Tablet Reg / SEC-421, DeLuna NeoBookings payment integration, IHG MEA Dept.
  of Tourism authority integration.
project: null
source_id: https://canarytechnologies.slack.com/archives/C083M6Q65PX/p1782839158966589
tags:
- morning-gtd
- slack
- from-awareness
time_minutes: 15
title: Read EMEA strategic accounts recap (Grecotel LIVE, Eurostars GDPR pause)
updated: 2026-07-02 16:20:00.000000
waiting_on: null
waiting_since: null
working_on: false
---

Sebastian Cahill's Jun 30 recap in #emea: Grecotel live, Eurostars WhatsApp paused on GDPR consent, Travelodge CYR go-live, Doyle voice repositioning.
https://canarytechnologies.slack.com/archives/C083M6Q65PX/p1782839158966589