---
area: null
contexts:
- react
created: 2026-05-03 10:37:09.307623
defer_until: null
due: null
energy: medium
id: 2026-05-03T1037-triage-ent-6104-hotel-aristocrate-inaccurate-frenc
order: null
output: "## Agent run 2026-05-06T17:30Z\n\n**Triage status: largely already done —
  Ryan Rogers picked it up 2026-05-05 and has shipped/queued fixes for 4 of 6 reported
  issues. Ticket is now `In Review`, Medium priority, label `UX impact`.**\n\n###
  The 6 reported issues, mapped to fixes\n\nRyan's triage comment used slightly off
  numbering (duplicate \"2.\"); aligned to the original numbering below.\n\n| # |
  Issue | Status | Fix |\n|---|---|---|---|\n| 1 | \"Heure du Check-in\" → \"Il est
  temps de vous enregistrer\" | ✅ Shipped | PR #44481 (Guido Percu, merged 2026-05-01)
  |\n| 2 | \"Procéder au check-in\" → \"procéder à l'enregistrement\" | ✅ Shipped
  | PR #44481 (same) |\n| 3 | Dates of stay rendering in English | \U0001F7E1 Fix
  in review | **PR #44768** — `ReservationRenderable.context()` was using `self.language_preference`
  with no fallback (empty string for guests w/o pref). Patch falls back to `hotel.default_guest_language`,
  mirroring the same fallback already present 2 lines below for `gettext(\"Dear\",
  ...)`. Cascades to all wrappers (CheckOut/MobileKey/F&B/PurchaseOrder/Tip/Housekeeping).
  Includes regression tests. |\n| 4 | Gray strip + reg-card \"Check-in\"/\"Check-out\"
  labels | \U0001F7E1 Fix in review | **PR #44765** — `frontend/check-in/src/locale/fr.json`:
  replace English loanwords with `Enregistrement` / `Départ` (manifest already marks
  both keys `human` for `fr`). |\n| 5 | \"View reservation\" button rendering English
  | \U0001F534 Open — needs per-hotel template fix | Hotel template data, not code.
  The FR body of one of bw-67007's email templates is missing the `: Voir ma réservation`
  text override on the `guest_url_button` merge tag. Ryan said he'd share a per-template
  diagnostic to pinpoint which one. **Action: confirm with Ryan whether the diagnostic
  ran and whether the override has been added in the template editor.** |\n| 6 | Reg-card
  custom fields untranslated (Company Name, Address, etc.) | \U0001F534 Blocked —
  access issue | Custom hotel-defined fields. Originally Ryan's plan was \"hotel admin
  updates in dashboard,\" but Melissa pushed back 2026-05-05 21:35: **BW SSO role
  does not grant access to the check-in product settings page**, and even her own
  account couldn't save changes there. Two sub-problems to resolve: (a) the access/permissions
  gap for BW SSO users (and possibly for CS), (b) actually backfilling the FR translations
  for bw-67007's custom fields. |\n\n### Open follow-ups (post-triage)\n\n- **Get
  PR #44765 and #44768 merged.** Both are `OPEN` / `REVIEW_REQUIRED` with no reviewer
  assigned. Worth nudging a reviewer.\n- **Issue #5: per-template diagnostic.** Ryan
  owes a follow-up showing which template's FR body is missing the `: Voir ma réservation`
  override on `guest_url_button`. Likely Pre-arrival or Day-of-arrival for BW. Once
  identified, fix is a hotel-template edit, not code.\n- **Issue #6: two open questions
  back to Melissa / CS:**\n  1. Was the loyalty reg-card update actually responsible
  for wiping the FR translations on custom fields, or were they never set? (Worth
  a quick check on the audit history of those custom fields if available — would inform
  whether other BW hotels are similarly affected.)\n  2. Who owns backfilling these
  — eng, or CS with elevated access? Permissions issue may warrant a separate ENT
  ticket if it affects BW more broadly.\n- **Cycle/owner.** Already in current cycle,
  assigned Ryan Rogers, started 2026-05-05.\n\n### Memory cues\n- bw-67007 = Hotel
  Aristocrate; is the canonical exemplar for `default_guest_language='fr'` issues
  — guests with empty `language_preference` were getting English date strings in otherwise-French
  emails.\n- Reporter Melissa Fairchild flagged 2026-05-01.\n\n### My action\nNo code
  changes needed from me right now — the engineering work is already in flight under
  Ryan. Triage write-up only. Safe to archive or move to `waiting` (waiting on review
  of #44765/#44768 + Ryan's template diagnostic for #5 + a CS/permissions decision
  for #6).\n"
project: null
source_id: https://linear.app/canary-technologies/issue/ENT-6104/hotel-aristrocrate-reporting-inaccurate-french-translations-on-our
tags:
- morning-gtd
- linear
time_minutes: 20
title: 'Triage ENT-6104: Hotel Aristocrate inaccurate French translations on hardcoded
  check-in'
updated: 2026-05-07 11:41:42.833533
waiting_on: null
waiting_since: null
working_on: false
---

BW-67007 (Best Western). Several wrong French strings on hardcoded check-in pages — possibly wiped during loyalty reg card update. Filed by Melissa Fairchild 2026-05-01, still in Triage. https://linear.app/canary-technologies/issue/ENT-6104