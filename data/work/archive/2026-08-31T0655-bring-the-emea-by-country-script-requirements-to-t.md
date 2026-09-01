---
area: null
completed_at: 2026-08-31 14:38:29.609583
contexts:
- deep
created: 2026-08-31 06:55:56.379016
defer_until: null
due: 2026-08-31
energy: high
id: 2026-08-31T0655-bring-the-emea-by-country-script-requirements-to-t
order: null
output: |
  ## Agent run 2026-08-31T09:56Z — prep for tonight's IHG weekly sync

  **Meeting:** "IHG Enterprise script: weekly sync", tonight 22:30 Athens (Zoom 967 5906 9980), Lorena's cadence.
  SJ + Blake were added to this call on 26 Aug, so it has an exec audience for the first time.
  DRI: Bryan ultimately responsible / Dianna point (Conor Gorman supporting) / Taylor implementation.
  Dianna's open ask on the thread: "getting the rest of the EMEA by-country script requirements aligned on and provided to Taylor."

  ### The headline for the room

  Dianna's ask is not blocked on someone writing a list. It is blocked on a **prioritisation decision that was already taken**, and on a **taxonomy defect nobody has adjudicated**. Both need an exec in the room, which is why tonight is the right time.

  From the 6 Aug "IHG Country DB" session (https://app.notion.com/p/3b481468615180349343ca1165d200a6):
  - "Conditional logic for European nations in enterprise scripts is dependent on V3 readiness" (V3 targeted production-ready by end of September).
  - **Decision taken: Welcome Amenity was prioritised for Q3 over conditional logic for European nations.** IHG + the loyalty/mobile team pushed for Welcome Amenity; international app rollout was judged not imminent.

  So "the rest of the EMEA by-country script requirements" is downstream of a trade-off already made against it. If SJ/Blake want EMEA to scale, that trade-off is the thing to revisit — not the list.

  ### What "aligned on" actually requires — three separable things

  Worth separating these in the room, because they have different owners and different unblock paths.

  **1. Legal/compliance requirements per country (owner: Dianna, with Sebastian + Vibhor)**
  Dianna is building country setup guides in Notion covering: required vs optional reg-card fields, OCR enablement + purge criteria, accepted ID types, consent/notice language, language settings.
  - UK template is the most complete. The rest are in progress.
  - Open action from 6 Aug: **Sebastian to provide notice/consent language for the ~8 remaining IHG countries** (excluding UK, US, Canada). Worth asking tonight whether that has landed — it gates everything Taylor can implement.
  - Vibhor owns confirming legal requirements per region (per "IHG Script Changes – Scaling Prep", https://app.notion.com/p/3a381468615181aa97cccc47e6a2990a).
  - Supporting tool: Guest Data Compliance Hub — https://guest-data-compliance-ihg.vercel.app (README: https://app.notion.com/p/3bf81468615181d3b671c843e2284c75)
  - Known staleness: the Notion country table still lists Special Requests, which has been removed from the forms (QA-1003, https://linear.app/canary-technologies/issue/QA-1003).

  **2. Which countries are even in EMEA (owner: unassigned — this is the gap)**
  This is ENT-7353 (https://linear.app/canary-technologies/issue/ENT-7353), currently **Backlog / Low priority and unassigned**. I think that priority is wrong given it is the substrate for Dianna's ask, and that is a cheap thing to fix in the room.

  **3. The mechanism that applies them (owner: Taylor / eng)**
  Largely working now — ENT-7355 (settings declared but never applied) is Deployed, ENT-7372 (always override customised reg cards) is In Progress.

  ### The concrete finding I can bring — our region model disagrees with IHG's

  IHG's own taxonomy is in "Canary IHG Operating Countries 7-20-26" (https://docs.google.com/spreadsheets/d/1TRCyzFzHa6f9Mwb8t0O7YIYlXxD-MeB9LR6TExhmCdg), 119 operating countries. I diffed it against what our code actually does (`get_ihg_region` in `backend/canary/onboarding/services/vendor/ihg/ihg_definitions.py`).

  **IHG has FOUR top-level regions. Our code has three.**
  - IHG: AMER, EMEAA, **GCHINA**. EAPAC, EUROPE and IMEA are *subregions of EMEAA*, not peers.
  - Our code: AMER, EAPAC, EMEAA — with EAPAC promoted to a peer of EMEAA, and **no concept of GCHINA at all**.

  That single modelling difference produces **10 mismatches across 119 countries**:

  | Country | IHG region | IHG subregion | Our code says |
  |---|---|---|---|
  | Hong Kong | GCHINA | HONGKONG | EAPAC |
  | Taiwan | GCHINA | TAIWAN | EAPAC |
  | Macao | GCHINA | MACAU | EAPAC |
  | India | EMEAA | IMEA | EAPAC |
  | Bangladesh | EMEAA | IMEA | EAPAC |
  | Nepal | EMEAA | IMEA | EAPAC |
  | Bhutan | EMEAA | IMEA | EAPAC |
  | Mongolia | EMEAA | EUROPE | EAPAC |
  | Northern Mariana Islands | EMEAA | EAPAC | EMEAA (fell through) |
  | French Polynesia | EMEAA | EAPAC | EMEAA (fell through) |

  Notes on that table:
  - The GCHINA rows are live right now — I am on `glloyd/ent-7078-modify-country-china-to-greater-china` this week doing exactly the Greater China relabel. Mainland China does not appear on IHG's operating-country sheet at all, while our code puts it in EAPAC. Someone should say out loud whether Greater China is in scope for scripting.
  - India/Nepal/Bangladesh/Bhutan being IMEA (i.e. under EMEAA) means **IHG considers South Asia part of EMEAA**. ENT-7353 framed this as "Wyndham says Europe, IHG says Asia-Pacific, the code says both" and posed it as an open question for Product. IHG's own sheet answers it: **EMEAA at region level, IMEA at subregion level**. That open question can be closed tonight with IHG's own data rather than left hanging.

  **The design defect underneath it.** `get_ihg_region` is `if AMER ... elif EAPAC ... else EMEAA`. EMEAA is the residual bucket, so any country nobody classified silently becomes European. That is exactly how Northern Mariana Islands and French Polynesia end up EMEAA, and how ENT-7353 found Sint Maarten (Caribbean) and New Caledonia (Pacific) being given European reg cards, European messages and WhatsApp on.

  **We already have the fix pattern in-house.** Wyndham's `ADDITIONAL_GUEST_STEPS_BY_COUNTRY` is one explicit country→config table, and if a hotel's country is not in it the provider **raises and onboarding stops**. Fail-loud, one list. That is precisely what ENT-7353 asks for, and it is a known-good pattern rather than a new design. Worth proposing as the answer.

  ### What I would ask for in the room

  1. **Revisit the Q3 trade-off.** Welcome Amenity was chosen over EU conditional logic. Dianna's ask cannot be satisfied while that holds. Either it changes, or we say plainly that EMEA by-country scripting lands after V3 (end of Sept) and set expectations with SJ/Blake accordingly.
  2. **Close the South Asia question using IHG's own sheet** — EMEAA/IMEA, not APAC. It has been an open Product question on ENT-7353 since 27 Aug and IHG has already answered it.
  3. **Decide on GCHINA.** We have no such region. Hong Kong, Taiwan and Macao are live IHG countries with ~6.5k rooms between them and are currently mis-regioned. In scope or explicitly out?
  4. **Get ENT-7353 prioritised and owned.** It is Backlog/Low/unassigned, and it is the foundation the by-country requirements sit on. Nothing is broken today because none of the affected countries are pilot countries — it breaks precisely as we scale, which is the thing this meeting exists to do.
  5. **Confirm Sebastian's ~8 countries' notice/consent language has landed.** That is the actual long pole for handing Taylor something implementable.

  ### Links

  - Source email thread (SJ, "Rigor on IHG deployment"): https://mail.google.com/mail/u/0/#inbox/1a01fdd46f5762d0
  - Linear project: https://linear.app/canary-technologies/project/ihg-scripting-changes-pilot-to-scale-e52e4a381d06
  - ENT-7353 country lists disagree: https://linear.app/canary-technologies/issue/ENT-7353
  - ENT-7355 settings declared but never applied (Deployed): https://linear.app/canary-technologies/issue/ENT-7355
  - ENT-7372 always override customised reg cards (In Progress): https://linear.app/canary-technologies/issue/ENT-7372
  - QA-1003 remove Special Requests + fix Notion country table: https://linear.app/canary-technologies/issue/QA-1003
  - IHG Country DB meeting notes (6 Aug, the prioritisation decision): https://app.notion.com/p/3b481468615180349343ca1165d200a6
  - IHG Script Changes – Scaling Prep: https://app.notion.com/p/3a381468615181aa97cccc47e6a2990a
  - IHG Testing Session & Agenda: https://app.notion.com/p/3c381468615180a89e18c026f350f726
  - IHG Enterprise Runbook: https://app.notion.com/p/3ae8146861518130a7f3cb58c384d0dd
  - Canary IHG Operating Countries sheet: https://docs.google.com/spreadsheets/d/1TRCyzFzHa6f9Mwb8t0O7YIYlXxD-MeB9LR6TExhmCdg
  - Guest Data Compliance Hub: https://guest-data-compliance-ihg.vercel.app
  - Code: `backend/canary/onboarding/services/vendor/ihg/ihg_definitions.py` (get_ihg_region, 3 regions) and `backend/canary/onboarding/services/vendor/ihg_definitions.py` (a second, disagreeing set of lists, comment says "Based on combined Wyndham + Best Western lists")

  ### Caveats

  - The 10-country diff is mine, computed this morning from the 20 Jul sheet against current `master` code. It has not been reviewed by Taylor or Lauta — present it as a finding to confirm, not as settled fact.
  - I did not locate Dianna's per-country Notion setup guides themselves (the UK template and the in-progress ones). Search surfaced the meeting notes describing them but not the pages. If you want them before the call, ask Dianna directly for the Configuration Hub link.
  - No external writes were made: nothing posted to Linear, Notion, Slack or the email thread.
project: 2026-08-31-ihg
source_id: https://mail.google.com/mail/u/0/#inbox/1a01fdd46f5762d0
tags:
- morning-gtd
- gmail
time_minutes: 45
title: Bring the EMEA by-country script requirements to tonight's 22:30 IHG weekly
  sync
updated: 2026-08-31 14:38:29.609569
waiting_on: null
waiting_since: null
working_on: false
---

Dianna's open ask on SJ's thread: "getting the rest of the EMEA by-country script requirements aligned on and provided to Taylor". That is the same problem as the four disagreeing country lists (ENT-7353). SJ and Blake asked to be added to this weekly Monday call, so tonight it has an exec audience. DRI now settled: Bryan ultimately responsible, Dianna point, Taylor implementation.
https://mail.google.com/mail/u/0/#inbox/1a01fdd46f5762d0