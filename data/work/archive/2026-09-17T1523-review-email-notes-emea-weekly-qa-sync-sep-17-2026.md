---
area: null
completed_at: 2026-09-18 15:19:14.819672
contexts: []
created: 2026-09-17 15:23:58.140463
defer_until: null
due: null
energy: low
id: 2026-09-17T1523-review-email-notes-emea-weekly-qa-sync-sep-17-2026
order: null
output: |
  ## Agent run 2026-09-18T12:23

  **Bottom line: nothing assigned to you, no decision waiting on you. Awareness only.** You were invited but do not appear in the transcript (speakers: James Saram, Eugênio Portella, Martijn Dekker). Short call, ~12 min.

  Sources:
  - Email (Gemini notes, 2026-09-17): https://mail.google.com/mail/u/0/#all/1a0af50fff86f8d8
  - Gdoc with notes + full transcript (owner Martijn Dekker): https://docs.google.com/document/d/1Fh64ARF_QDp6PCKI9oBhZSBedB1hKmRvmIr3nK7_3_M/edit
  - Transcript tab: https://docs.google.com/document/d/1Fh64ARF_QDp6PCKI9oBhZSBedB1hKmRvmIr3nK7_3_M/edit?usp=drive_web&tab=t.fcy3ltd4bv4m
  - Note: the Drive folder entry in "EMEA - Weekly QA Sync (recurring)" is a shortcut that reads empty via the API; the real doc is the ID above.

  Gemini garbles names throughout: "Kapinsky/Kapitzky" = Kempinski, "Host/FHOST" = the Host PMS, "Villa Thoughts/Villa Force" = the Host pilot property (one property, two spellings), "Nubius" probably Newhotel/Nuvola-type name - unverified, "ARI driven" = ARR driven.

  ### Worth your attention
  1. **Tablet Reg OCR is the live customer complaint (Kempinski and all tablet-reg properties).** Feedback: passport/ID scanning feels buggy and slow, does not lock on when the iPad or document moves. James, Marine and Mona were to test on iPads the same afternoon (Sep 17). James flagged it as third-party OCR + camera settings + hotel low lighting, so not automatable, only physical/manual QA. James also said Kempinski has "a new requirement and multi room" in flight, unrelated to QA. Relevance: same Tablet Reg surface as the Grecotel pilot.
  2. **Opera sync failures on two other tablet-reg properties**: a property in Italy (transcribed "Mangayas") and Casa Camper Barcelona - company guests not pushed correctly / not syncing to Opera. Kempinski's pass-to-PMS round trip is clean, which James credits to Eugênio's earlier QA. Hypothesis from James: same code, but those hotels are on older configuration versions. Eugênio will diff configs/settings, but James explicitly capped it at 10-30 min spare time. So this is effectively un-owned; if it turns into an ENT ticket it likely lands on engineering without a root cause.
  3. **Priority call by James: Kempinski is top QA priority, ARR-driven.** Everything else on tablet reg is best-effort.
  4. **Next quarter: AP Hotels (Portuguese group) onboarding on Host PMS.** Decision recorded: QA effort goes to AP Hotels via the Host integration once Martijn finishes certification on the pilot property. James: ~$1M ARR tied to Host PMS plus regional benefit for Portugal. Timeline "hopefully a couple of weeks". Eugênio will pair with Martijn.
  5. **QA capacity is thin.** Eugênio said he is buried and that QA hiring has stopped across teams. "Nubius" v5 work (Sam, with Alberta helping) has no QA coverage at all. James mentioned a later-in-year item transcribed as "Machang ... Seahorn" - too garbled to identify.
  6. James wants to work out where **Tablet Reg V2** stands and what to improve; no owner or date.

  ### Action items recorded (none yours)
  - James Saram, Marine, Mona: test OCR scanning on iPads for passports and IDs.
  - Eugênio Portella: compare configuration between properties for the tablet-reg Opera sync issues (time-boxed).
  - Eugênio Portella: pair with Martijn on Host certification and share testing knowledge.
  - Martijn Dekker: finalize Host + pilot-property certification ahead of AP Hotels.

  ### Possible follow-ups (your call, nothing sent)
  - Ask James for the outcome of the Sep 17 iPad OCR test and his "analysis on cloud", if OCR quality bears on Grecotel/Kempinski work you own.
  - Check whether the Italy / Casa Camper company-guest Opera sync issue has a Linear ticket before it arrives as an escalation.
project: null
source_id: null
tags: []
time_minutes: 5
title: 'Review email "Notes: “EMEA - Weekly QA Sync” Sep 17, 2026"'
updated: 2026-09-18 15:19:14.819651
waiting_on: null
waiting_since: null
working_on: false
---

Get associated gdoc transcript and summarize for my attention