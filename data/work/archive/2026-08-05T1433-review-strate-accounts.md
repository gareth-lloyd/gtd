---
area: null
completed_at: 2026-08-06 12:57:22.613844
contexts: []
created: 2026-08-05 14:33:42.376566
defer_until: null
due: null
energy: low
id: 2026-08-05T1433-review-strate-accounts
order: null
output: |
  ## Agent run 2026-08-05T15:34

  Reviewed Sebastian Cahill's EMEA Strategic Accounts meeting recap (Aug 4, 2026)
  (https://canarytechnologies.slack.com/archives/C083M6Q65PX/p1785869629660919).
  Nothing is assigned to you directly. Digest, engineering-relevant first:

  **Likely to land on eng / worth watching:**
  - **Eurostars (live again, all channels)** — open debate on sending a WhatsApp
    opt-out acknowledgment message. Request came from Eurostars' GDPR team; Sebastian
    thinks it's odd/riskier. James Saram is checking scope + effort with Jake W;
    Aksel/Manolo deciding whether to push back. No Linear ticket exists yet (I
    checked) — if it goes ahead it will need a messaging build.
  - **Bespoke Hotels / Guestline** — Guestline conceded after ~1 year; API keys
    emailed to the integrations alias. Brad says no eng work needed (build done long
    ago); Isaac is asking shales to name an integrations/eng owner to finish testing.
    Only outstanding item — someone from eng may get tapped.
  - **Net-new PMS integration process** — Manolo to create a dedicated public
    channel; Ian flagged that siloed parallel threads are unworkable for eng. A
    longer session will build the full process using Host as the case study.
    Sebastian's QA playbook: https://app.notion.com/p/canarytechnologies/Strategic-Account-Launch-Playbook-EMEA-Testing-Phase-QA-36781468615181b885cefd2197cd6207
  - **Travelodge Spain (Voice, time-critical)** — OHIP PMS + Synergy CRS (same as
    Eurostars), goal is replacing the call centre; end-to-end booking is the
    prerequisite. Sponsor (Carlos) on holiday from Aug 6; hoping for signature Aug 5.
  - **Travelodge UK** — Choose Your Room live Thursday. Security concern: QR link +
    surname + dates could expose a room; the IDV liveness check is the fail-safe and
    needs to be reliable.

  **Other headlines:**
  - Doyle Collection: Voice stays (triage only); Messaging + WebChat across remaining
    6 properties from September; F&B/upsells/check-in/mobile-key expansion sized at
    a couple hundred K.
  - Danubius/Ensana: signed after 8.5 months; pilot early September on Tablet Reg v2
    + pre-arrival IDV; tablets shipping to Hungary.
  - Kempinski: Prague (Augustine) is pilot #3; worldwide IT call moved to Aug 20.
  - DeLuna/Neobookings: full E2E Voice booking passed in production; Voice go-live
    next week, WebChat after.
  - TUI: approved for Voice on first property (German island, ~98% German guests);
    open product question on translation visibility.
  - Host (Villa Foz): slipping to September; needs test reservations before GM leaves
    end of week.
  - Pipeline: MONDON/Abu Dhabi+Dubai authorities (needs named pilot property, IHG ME
    meeting Thursday); AXIOM non-hotel Voice use case priced as a paid pilot.

  No action needed from you unless the Eurostars opt-out acknowledgment or the
  Guestline testing owner lands on Enterprise — neither has a ticket yet.
project: null
source_id: null
tags: []
time_minutes: 5
title: review strate accounts
updated: 2026-08-06 12:57:22.613836
waiting_on: null
waiting_since: null
working_on: false
---

https://canarytechnologies.slack.com/archives/C083M6Q65PX/p1785869629660919