---
area: null
contexts: []
created: 2026-05-12 11:58:23.049295
defer_until: null
due: null
energy: low
id: 2026-05-12T1158-grecotel-context-accumulation
order: -5
output: '## Grecotel / Caramel — context snapshot (2026-05-13)


  Sources: [#grecotel Slack](https://canary-tech.slack.com/archives/C0AHERMJRHN) (back
  to 2026-04-21), [Notion consolidated requirements](https://www.notion.so/canarytechnologies/Grecotel-Pilot-Consolidated-Requirements-35e8146861518158b8b1dcee789fb970)
  (24 items, maintained by Bree Sullivan), [Linear: Grecotel Hardening](https://linear.app/canary-technologies/project/grecotel-hardening-7ace7eaa814a).
  Long-term context in `project_grecotel_pilot.md` memory.


  ### Deal status: RED

  Messaging, F&B, upsells, checkout live at Caramel since Apr 30. **Check-in is the
  blocker.** KDM Ioannis demanded a written timeline May 8; no more test calls until
  things work. Actively evaluating Duve + has a native app ready. Caramel is seasonal
  (closes Nov) — Q3 slip = lost season. Stakes: Lambros (HIT) signaled 1M EUR Greek
  market + partnership if Caramel succeeds.


  ### Critical path

  1. **Test reservations** — #1 bottleneck. Laura/Dana/Martijn all asked repeatedly
  (May 11-12); Aksel/Manolo to provide. Multiple deployed fixes sit unverified.

  2. **[AD-7621](https://linear.app/canary-technologies/issue/AD-7621) Accompanying
  guest OCR submit** — Dana pushed fix May 12 05:46, unverified. Blocks companions
  workaround validation.

  3. **[EMEA-244](https://linear.app/canary-technologies/issue/EMEA-244) Hide additional
  guest fields** — in review (Martijn).

  4. **[AD-7623](https://linear.app/canary-technologies/issue/AD-7623) Signature at
  end of check-in flow (V3)** — Q3 target, customer calls it deal-breaker. Vibhor
  needs to join next hotel call to spec requirements.

  5. **Written timeline to KDM** — Ioannis waiting. Vibhor says he can''t give ETAs
  without V3 requirements pinned down. Chicken-and-egg.


  ### Scorecard (24 Notion items)

  Done (9) | In progress (4) | Backlog (3) | Open/no owner (5) | Not Canary (2) |
  Out of scope (1)


  Key open/unowned: mobile EU-domain login (no ticket), arrival-time vs upsells conflict
  (#13, no ticket), Salesforce Marketing Cloud (#18, deferred), F&B compendium not
  showing (#20, stale since Apr 13).


  ### PMS / tech context

  - Protel On-Prem via HIT (reseller, not Planet). Hotel id 4739.

  - **Companions:** Grecotel uses a custom local DB table not exposed via Protel API.
  Grecotel building a sync trigger from accompanying-guest profiles to companions
  table. Yauheni emailed Protel Apr 29 asking for a new API (long-shot). Separately,
  Yauheni investigating whether documents even attach to accompanying-guest profiles
  on Protel On-Prem — potential second gap beyond table sync.

  - **Greek OCR:** MRZ fix deployed ([AD-7619](https://linear.app/canary-technologies/issue/AD-7619)),
  but non-MRZ Greek IDs (e.g. driver''s license) still return Greek chars. Plan: LLM
  transliteration — no ticket, no ETA. Customer wants Roman-only (Protel runs in English).

  - **Rate-plan error** (`RatePlanId != RatePlanCode`) — COMP/Virtual rate code in
  Grecotel master data. HIT says hotel-side Stammdaten fix; not Canary.

  - **CC sync** done (INT-8476). Awaiting PCI tokenizer install on Grecotel''s side.

  - **GJ delay for walk-ins** ([EMEA-245](https://linear.app/canary-technologies/issue/EMEA-245))
  — Martijn proposes ~1hr delay. Not a launch blocker.

  - Name-swap root cause ([AD-7612](https://linear.app/canary-technologies/issue/AD-7612),
  fixed): additional guest inherited primary''s `vendor_id`.


  ### On-site visit

  Ian Clark proposed May 8 sending an eng on-site. Ian followed up May 12 ("Any news
  Aksel?"). Pending customer agreement.

  **People on-site:** Ioannis (KDM, frustrated — show results not demos), Maria (GM,
  warmer — messaging wins), Minas + Lucas (FO managers), Grecotel''s internal developer
  (built native app, building companions sync trigger — the key person to pair with),
  HIT: Vaios (found rate-plan issue), Lambros (exec, partnership lever).

  **Prep before flying:**

  - Self-service test-reservation capability (Protel UI access? script via HIT?).
  Without this the trip stalls immediately.

  - Get companions table schema from Yauheni + doc-attachment investigation status.

  - Mobile EU-domain login checklist: hotel wifi, iOS + Android, `eu.canarytechnologies.com`.

  - Rate-plan Stammdaten fix — raise with HIT in person.

  - Capture their native check-in app flow for Vibhor''s V3 scoping.

  - Don''t volunteer V3 dates. Don''t suggest keeping Greek as fallback.


  **On-site verification loop:** reservation -> primary check-in -> accompanying with
  ID -> confirm OCR + doc attach -> confirm companions table row -> confirm in Protel
  UI.

  **Success:** (1) self-service test-res capability, (2) companions e2e on one reservation,
  (3) EU login fixed/root-caused, (4) native app flow captured, (5) direct HIT channel
  for config issues.


  ### Out-of-scope asks that may surface

  - WhatsApp edit/delete — Kevin Li confirmed integration doesn''t support it.

  - Restaurant bookings — in their native app, part of "why Canary" calculus.

  - Salesforce Marketing Cloud — push check-in URLs from CRM. Deferred; KDM-relevant.

  - Arrival time field vs early-check-in upsells — dropped, no resolution. Don''t
  promise without Vibhor/James.

  '
project: null
source_id: null
tags: []
time_minutes: 5
title: Grecotel context accumulation
updated: 2026-05-14 12:14:23.071302
waiting_on: null
waiting_since: null
working_on: false
---

This notion summarizes: https://www.notion.so/canarytechnologies/Grecotel-Pilot-Consolidated-Requirements-35e8146861518158b8b1dcee789fb970?source=copy_link