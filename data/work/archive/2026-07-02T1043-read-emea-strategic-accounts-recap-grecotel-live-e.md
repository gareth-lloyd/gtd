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
output: "## Agent run 2026-07-02T16:20 — read & summarized\n\nRead Sebastian Cahill's
  EMEA Strategic Accounts meeting recap (Jun 30, 2026) in #emea.\nSource: https://canarytechnologies.slack.com/archives/C083M6Q65PX/p1782839158966589\n\nThe
  recap is broader than the title — 6 accounts, a pipeline section, and a key-risks\nroundup.
  Distilled below (engineering-relevant items flagged).\n\n### \U0001F534 Eurostars
  — Guest messaging PAUSED (GDPR)\n- Raquel's legal team told Eurostars to temporarily
  deactivate WhatsApp guest\n  messaging (consent-at-booking concern). Landed 10 min
  before the call.\n- NOT a product/platform issue — compendium-via-QR and everything
  else stays live.\n  KPIs strong but pausing WhatsApp will dent the metrics Javier
  championed.\n- Canary read: transactional (check-in/welcome) messages are fine;
  upsells = marketing\n  and need consent. Need Eurostars to pinpoint exactly where
  the concern sits.\n- Manuel + Manolo face-to-face in Barcelona Thursday; trying
  to fold their legal in.\n\n### \U0001F7E1 Travelodge UK — Google Wallet approved,
  CYR go-live this week\n- Google Wallet approved. CYR pilot believed ready; Isaac
  confirming with Holly/Vasudha/Gleb.\n- UDF decision: Gleb fine with reporting-only
  — no push to UDFs for now.\n- Biggest remaining workstream: ingesting prepaid early-in/late-out
  packages from their\n  site and honoring them for auto-check-in — NOT a CYR launch
  blocker (vibhor to scope).\n- \"Choose-Your-Room\" flagged as a potential Canary
  upsell/upgrade differentiator vs\n  Alliants (TUI has asked too). Owners: vibhor
  (CYR items + package ingestion), Isaac\n  (go-live readiness before Holly OOO).\n\n###
  \U0001F534 Doyle Collection — First voice bookings in; pivot to repositioning\n-
  First bookings landed (2 on Dupont via Voice, after welcome message shortened).\n
  \ Marylebone still zero.\n- Sentiment shifted from ~99% likely-to-churn-voice →
  may keep it if expectations reframed.\n- Strategy: reposition Voice for luxury (Jonathan
  Kennell's deck) — lead with\n  missed-call/FAQ/triage value, deprioritize \"we'll
  take your bookings\"; reset the\n  30%-of-revenue expectation.\n- +90 days of Voice
  free (extension) for runway. Hold repricing until after extension;\n  luxury AI-second/human-first
  usage could naturally drop them to a lower SaaS tier.\n- Open eng item (carried):
  Australia (+61) call-blocking + multi-rate-code (James Saram).\n  Jonathan + James
  OOO Mon–Wed incl. Jul 1; Sebastian covering.\n\n### \U0001F525 Kempinski — MSA close
  imminent; implementation call Wed Jul 1\n- Contract in final legal tweaks; MSA hopefully
  signed ~Jul 1. Frutt Mountain Resort\n  order form to be reminded to Daniel.\n-
  Tablet Reg is priority #1 and unlocks the other properties (want it live fast across\n
  \ multiple hotels incl. full digital check-in). Kiosk only envisioned at Frutt.
  Loyalty\n  is a separate parallel call, not a blocker.\n- Risk note ties this to
  SEC-421 (must close to unlock Tier 2 ahead of Aug 15).\n\n### \U0001F7E2 Grecotel
  — LIVE! (the headline)\n- Grecotel LIVE as of this week after the opt-in fix validated
  end-to-end.\n- Next: proactive reporting design (standard KPIs mirroring DeLuna)
  — Aksel + James +\n  Sebastian meeting Thursday. Data story anchored on marketing
  opt-in rate / # opt-ins\n  for retargeting, plus conversion (native app requires
  download, so Canary's conversion\n  + >75–80% messaging deliverability should shine).
  Alex Kelly to implement reporting,\n  let it run ~1 week, then share a positive
  story.\n\n### \U0001F7E1 DeLuna — Rates/availability working; payment path is the
  blocker\n- Correctly pulling rates + availability on a live DeLuna property via
  NeoBookings (same\n  for web chat). Integration slot form signed.\n- Payment gateway
  unresolved: ambiguity whether DeLuna is on PayNoPain vs Payments-by-Septeo\n  (maybe
  synonymous); old contact left, manager unresponsive. Must confirm PayNoPain is\n
  \ usable by Ulyses and hits DeLuna's existing acquiring account. Interim: push DeLuna
  to\n  Stripe while NeoBookings payment integration is built.\n- Same repositioning
  theme as Doyle: bookings good for order-taking, weak for exploration.\n  Owners:
  Aksel (PayNoPain vs Septeo + acquiring question, lock NeoBookings), Brad\n  (viable
  payment path + ETA), Manolo (Stripe interim).\n\n### \U0001F3AF Pipeline\n- Marriott
  — folio-split ask (Manuel to loop in James Saram + vibhor).\n- IHG MEA — big, fast-moving.
  Dubai corporate office controls MEA + parts of APAC. Likely\n  Africa first (no
  authority-integration restrictions), then Dubai. They want a clear\n  status + timeline
  on Department of Tourism integration (the gating question).\n- ME ID-scanner ↔ authority
  integrations: Dubai (~5x Abu Dhabi) is priority. H2O is the\n  only player integrated
  with Abu Dhabi authorities today; Samsotech (Dubai) went quiet.\n  Manuel in Dubai
  first week of Sept.\n\n### ⚠️ Key risks (Sebastian's roundup)\n- Eurostars WhatsApp
  paused on GDPR — messaging is our differentiator; need fast legal\n  resolution
  or KPIs slip.\n- Doyle Marylebone still zero into Jul 1/Jul 8 — reposition must
  land before extension.\n- Travelodge CYR must go live this week before Holly OOO.\n-
  DeLuna payment path unproven + partner ambiguity; vendor unresponsive.\n- Kempinski
  MSA/SEC-421 must close to unlock Tier 2 ahead of Aug 15.\n- IHG MEA Dept. of Tourism
  integration not yet available; timeline ask is gating.\n\n### Nothing actioned\nNo
  external writes made. This was a read/consume item — no reply posted, no tickets\ntouched.
  Eng-adjacent threads worth watching if they surface as tickets: Travelodge\npackage-ingestion
  → auto-check-in, Doyle Australia (+61) call-blocking + multi-rate-code,\nKempinski
  Tablet Reg / SEC-421, DeLuna NeoBookings payment integration, IHG MEA Dept.\nof
  Tourism authority integration.\n"
project: null
source_id: https://canarytechnologies.slack.com/archives/C083M6Q65PX/p1782839158966589
tags:
- morning-gtd
- slack
- from-awareness
time_minutes: 15
title: Read EMEA strategic accounts recap (Grecotel LIVE, Eurostars GDPR pause)
updated: 2026-07-07 13:20:05.060616
waiting_on: null
waiting_since: null
working_on: false
---

Sebastian Cahill's Jun 30 recap in #emea: Grecotel live, Eurostars WhatsApp paused on GDPR consent, Travelodge CYR go-live, Doyle voice repositioning.
https://canarytechnologies.slack.com/archives/C083M6Q65PX/p1782839158966589