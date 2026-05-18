---
area: null
contexts: []
created: 2026-05-18 12:28:55.274726
defer_until: null
due: null
energy: low
id: 2026-05-18T1228-iot-docs-summarize-hte-doc
order: -18
output: "## Agent run 2026-05-18T13:05 — Summary of \"PRD: In-Room Controls Integration
  [Explore]\"\n\nNotion: https://www.notion.so/3428146861518121afb9e7991b3eaec4\nStatus:
  Explore · PM: Belinda Wang · Eng Lead: TBD (Blake Vanlandingham evaluating)\nLinear:
  Crown Resorts — In-Room Controls Integration\n\n### What it is\nIntegrate in-room
  hardware controls (HVAC, curtains, lights) into Canary\nCompendium so guests control
  their room from a web UI (in-room tablet or own\ndevice). Trigger: Crown Resorts
  is dropping Intelity and wants this in\nCompendium. Potential to become a repeatable
  product for any IoT-enabled hotel.\n\n### Commercial framing (important)\n- NOT
  in Crown's original signed scope — surfaced March 2026, after the\n  contract project
  wrapped (BAU as of Apr 9). We are not contractually\n  obligated; declining is an
  option. Should be priced as net-new\n  premium/add-on revenue, not a make-good.\n-
  Crown's end-of-Aug-2026 deadline is driven by Intelity contract expiry\n  (Sept
  2026) — their pressure, not ours. Dan (CS) owns commercial proposal.\n\n### Confirmed
  technical path: NETx + BACnet\nCanary Cloud → NETx MP Server (Windows VM at hotel)
  → BACnet/IP → IC3 Server\n→ B574 Edge Router → in-room hardware. NETx replaces Intelity's
  Edison Server\nin the existing topology; no guestroom hardware changes. Canary consumes\nNETx's
  REST Tree API like any other SaaS integration.\n- Pricing: €6,440 one-time per property
  (NETx Offer AN-20260294, perpetual\n  license, no recurring fee), valid till 31
  Jul 2026. Sydney = another €6,440.\n- May 18: NETx delivered full Tree API docs
  + Postman collections;\n  WebSocket real-time push confirmed (no inefficient polling
  needed).\n\n### Scope\n- P0: thermostat + curtain control from web UI. P1: lights.
  P2: TV (out).\n- Thermostat works via default BACnet (confirmed). Curtains/lights
  are\n  reachable on the same INNCOM backbone but NOT writable in Honeywell's\n  default
  BACnet.cfg — needs Honeywell to extend config (open question;\n  fallback = FastPack
  to B574-F). Crown accepted an MVP approach, so\n  thermostat-only first launch is
  acceptable.\n\n### Customers / scale\n- Crown Perth (Honeywell INNCOM) = first.
  Crown Sydney (Crestron) = phase 2,\n  same NETx+BACnet pattern, Sydney docs still
  outstanding.\n- Aman Resorts (7 APAC properties, Lutron) = separate workstream —
  NETx does\n  NOT support Lutron; likely direct Lutron MyRoom XC cloud API. Tablet-first,\n
  \ no AI chat. Validates demand but architecturally different → makes a\n  vendor-neutral
  abstraction layer critical for this to scale.\n- Demand audit: only Crown (committed)
  + Aman & Pan Pacific (discovery). We\n  are slightly ahead of the demand curve,
  not behind a backlog.\n\n### Competition\nDigiValet is the main threat — only platform
  with proven direct integrations\nto Honeywell INNCOM, Crestron AND Lutron. Most
  rivals (SuitePad, Volara)\nintegrate via Interel middleware. Strategic open question:
  evaluate an Interel\npartnership to collapse Crown+Aman into one workstream vs.
  building direct.\n\n### Key open items / blockers (gating build)\n1. Honeywell:
  extend BACnet.cfg for writable lights/curtains? (scope-defining)\n2. Dan/SJ greenlight
  on NETx purchase + scope (Slack thread May 13)\n3. Crown IT approval to host the
  NETx Windows VM (deployment blocker)\n4. Eng feasibility sign-off (Blake/Nicolas)
  — Blake hesitant given mobile\n   priorities; staying in Explore until commercial
  answers are in\n5. Implementation resourcing: train a Canary specialist on NETx\n
  \  (recommended, scales to Aman/future) vs. engage a NETx partner integrator\n6.
  Latency: validate NETx+BACnet round-trip meets <1s guest expectation\n\n### Bottom
  line\nFeasible and priced for Crown Perth HVAC; commercially attractive as a\nnet-new
  premium add-on. Still in Explore — not yet committed to build,\npending Honeywell
  config answer, Crown IT VM approval, and eng/commercial\nsign-off. Lutron (Aman)
  remains unsolved by the chosen path.\n"
project: null
source_id: null
tags: []
time_minutes: 5
title: IoT docs - summarize hte doc
updated: 2026-05-18 12:30:48.073227
waiting_on: null
waiting_since: null
working_on: false
---

https://www.notion.so/canarytechnologies/PRD-In-Room-Controls-Integration-Explore-3428146861518121afb9e7991b3eaec4?source=copy_link