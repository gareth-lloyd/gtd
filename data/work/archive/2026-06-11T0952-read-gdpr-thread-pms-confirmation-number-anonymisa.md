---
area: null
contexts:
- consume
created: 2026-06-11 09:52:52.163160
defer_until: null
due: null
energy: medium
id: 2026-06-11T0952-read-gdpr-thread-pms-confirmation-number-anonymisa
order: null
output: |
  ## Agent run 2026-06-11T14:05:00+01:00

  Read the full thread (https://mail.google.com/mail/u/0/#inbox/19eb26768f7ef998) and
  cross-checked the confirmation-number question against the obfuscation code.

  **Thread state (Sebastian Cahill ↔ Tanya Chib, privacy counsel; latest msg 2026-06-10):**
  - Consent screen: Tanya wants (i) an explicit Controller sentence ("[Hotel] ... acts
    as Controller under UK GDPR") and (ii) the hotel's (controller's) privacy policy
    linked. Sebastian says the hotel policy is already linked in his latest version.
  - Incode side-letter: Tanya flagged Part A ("images and biometric data deleted once
    verification is complete") as contradicting the faceprint reality (Incode retains
    under own policy). She proposed a 3-part clause: (a) faceprint deletion within a
    defined max period, (b) no model-training/own-purpose use without separate consent,
    (c) written confirmation of UK/EU faceprint retention. Sebastian is relaying to the
    US law firm handling the Incode workstream rather than accepting Tanya's draft directly.
  - UK transfer mechanism: pending check whether Incode holds UK Extension to the
    EU-US Data Privacy Framework certification; otherwise UK Addendum needed urgently.
  - DPIA: drafted under UK law for IHG; Sebastian asked how to template it for all
    future clients and whether UK-law drafting covers the EU (Tanya hasn't answered yet).
    Children clause being checked internally. Biometrics live at only 2 UK IHG pilot
    sites; EMEA expansion (DK/IE/FR/AT, maybe PL/HU) planned in coming months.
  - Renate engaged for the RIRA (re-identification risk assessment) report.

  **The open question (directly adjacent to our data-obfuscation work):** Sebastian
  asked Tanya (2026-06-10, unanswered): after obfuscation Canary retains the PMS
  confirmation number, which could be linked back to an individual via the PMS if the
  hotel (controller) hasn't obfuscated its side. With no visibility into the controller's
  handling, does retaining that identifier still constitute valid anonymisation, or is
  the theoretical re-identification path through the PMS a compliance issue?

  **Codebase facts (verified, useful when Tanya replies or for the RIRA):**
  - Confirmation numbers are NOT obfuscated. ConfirmationNumber
    (backend/pms-gateway/reservations/models/confirmation_number.py) does not inherit
    ObfuscatableModel; tests confirm confirmation_numbers pass through
    obfuscate_guest_information() unchanged
    (backend/pms-gateway/load/tests/services/utils/test_obfuscate.py).
  - Obfuscation is irreversible random replacement: uuid4().hex with "__redacted__"
    prefix (backend/pms-gateway/load/services/utils/obfuscate.py); no keyed hash, no
    retained mapping in ObfuscationPlan/ObfuscationPolicy. So Sebastian's "we replace
    values rather than reversible hash, no retained mapping" working assumption is
    correct on the pms-gateway side — but his question stands: the confirmation number
    itself is the residual linkable identifier.
  - Note: GDPR/EDPB practice treats this as pseudonymisation rather than anonymisation
    if a realistic re-identification path exists via the controller's PMS ("motivated
    intruder" / singling-out test) — expect Tanya to land roughly there; mitigations
    would be dropping/obfuscating the confirmation number too, or documenting in the
    RIRA why the PMS path is not "reasonably likely" means.

  **Possible next actions (user's call):**
  - Decide engineering position on obfuscating confirmation numbers (would break
    PMS-side reconciliation/lookups — needs design thought) ahead of Tanya's answer.
  - Feed the codebase facts above into the RIRA/Renate workstream and the
    Alex/Dyran/Blake/Martijn/Bree obfuscation-methodology session output.
project: null
source_id: https://mail.google.com/mail/u/0/#inbox/19eb26768f7ef998
tags:
- morning-gtd
- gmail
- from-awareness
time_minutes: 20
title: 'Read GDPR thread: PMS confirmation-number anonymisation question'
updated: 2026-06-11 13:59:47.268974
waiting_on: null
waiting_since: null
working_on: false
---

Sebastian ↔ Tanya (privacy counsel) round on consent screen, Incode side-letter, DPIA; open question whether retaining PMS confirmation numbers breaks anonymisation — adjacent to data-obfuscation work.
https://mail.google.com/mail/u/0/#inbox/19eb26768f7ef998