---
area: null
contexts: []
created: 2026-06-03 11:21:51.605609
defer_until: null
due: null
energy: low
id: 2026-06-03T1121-catch-up-on-iot-slack-channel-generally
order: null
output: |
  ## Agent run 2026-06-03T13:05

  Caught up on the IoT Slack activity. Note: the link in this item points to
  #crown-resorts (C02JKFTV7K9), but the real IoT discussion lives in the
  dedicated **#integrations-iot** channel (C0AS48SEGNQ) — you joined it today.
  Read both. Summary below.

  ### What the channel is about
  In-room IoT controls (thermostat / lighting / fan) surfaced inside Canary
  Compendium (web) and eventually the mobile SDK app. Driven by two luxury
  customers asking for it: **Crown Resorts** and **Aman**. Belinda's thesis:
  this is the leading edge of broader luxury-brand demand and being first
  helps win future deals. Three GRMS vendors in play: Honeywell (INNCOM),
  Lutron, Crestron.

  ### Crown specifics
  - Crown uses Honeywell INNCOM (Perth) + Crestron (Sydney), today via
    **Intelity**, whose contract expires **end Sep 2026**. They're frustrated
    with Intelity and want to replace it — and we said yes to IoT in the RFP,
    so there's commitment pressure.
  - **NETx middleware** is the proposed technical path (Belinda sourced it).
    NETx sits between Canary Cloud and Crown's existing Honeywell/Crestron
    hardware via BACnet, exposing a REST/JSON "Tree API" (plus MQTT/websocket
    for live data). ~€6,440 one-time per property (by datapoint), no recurring.
    Requires an on-prem Windows VM at Crown; cannot be whitelabelled today.
    Does NOT support Lutron, so it's not a fit for Aman.
  - Proposed plan: NETx → Crown Perth as Phase 1, thermostat MVP by **end Aug**
    (ahead of the Sep Intelity expiry); Sydney = Phase 2. Aman = separate
    Lutron MyRoom XC cloud path, more eng.
  - Eng feasibility (Blake): confident it can be staffed with **1 eng across
    June–Aug, run out of the In-Stay team**, backend+frontend mostly reusable.
    Painful part = mapping varied per-room hardware configs into a coherent UI.
    Belinda (APAC) to quarterback the integration-partner setup + on-site NETx
    install (leaning toward engaging a NETx partner integrator initially).
  - Commercials (Daniel/SJ): Crown willing to commit to a longer-term deal and
    pay for build/support. Daniel handling this directly with Rohit.

  ### >>> CURRENT STATUS (most important — as of Jun 2) <<<
  IoT is effectively **on hold / waiting on Crown**. After the latest meeting,
  Crown took it back for evaluation because they're **planning to switch their
  IoT vendor from Honeywell/Crestron to Interel** (which would be a much simpler
  API integration for us). If that happens, NETx becomes only an *interim*
  solution / a fallback for properties that don't move to Interel. **No timeline
  from Crown** on the decision. (Interel context also discussed in #crown-resorts
  on ~Apr 22: Interel is now a GRMS provider/competitor, signed to replace all
  Honeywell+Crestron at Crown within ~2 years, cloud-native with an open API.)

  ### Decoupled piece likely to proceed: Compendium device binding
  Separate from IoT: Crown wants in-room tablets to auto-display an
  authenticated Compendium session bound to the room's current reservation
  (must rotate between guests). A pure static link is rejected (security — the
  link also works on phones). Blake's proposed flow: a device-binding step that
  caches a room↔device JWT on the tablet so the URL stays static, with
  reservation state cleared at checkout (hackable without MDM lockdown).
  **Adil** to scope it. Belinda wants this delivered FIRST and independently of
  the IoT decision — valuable for expanding Compendium onto tablets regardless.
  Worth tracking as its own potential action.

  ### People
  Belinda (customer/APAC lead) · Blake, Ishwar, Adil (eng; Adil pulling NETx
  Tree/MQTT/websocket Postman collections) · James Saram + Martijn Dekker (newer
  joiners, May) · SJ + Daniel Mourad (commercial).

  ### Suggested follow-ups (your call)
  - Nothing actionable required right now; the ball is in Crown's court on
    Interel-vs-NETx. Consider moving this to `waiting` on Crown's decision.
  - If you want eng to keep momentum, the device-binding piece is the one item
    that's greenlit-ish and decoupled — could be split into its own next-action.
project: null
source_id: null
tags: []
time_minutes: 5
title: catch up on IoT slack channel generally
updated: 2026-06-03 13:05:00.000000
waiting_on: null
waiting_since: null
working_on: false
---

https://canarytechnologies.slack.com/archives/C02JKFTV7K9/p1778718190577629