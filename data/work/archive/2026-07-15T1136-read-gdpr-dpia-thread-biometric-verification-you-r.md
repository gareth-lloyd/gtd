---
area: null
contexts:
- react
created: 2026-07-15 11:36:23.638373
defer_until: null
due: null
energy: medium
id: 2026-07-15T1136-read-gdpr-dpia-thread-biometric-verification-you-r
order: null
output: |
  ## Agent run 2026-07-15T14:06:42

  Read the full 8-message thread (Jun 23 → Jul 13, plus quoted history back to May 20):
  https://mail.google.com/mail/u/0/#inbox/19ef51f6db691431

  **Who/what**: Tanya Chib (external privacy counsel, Privacy Rules, tanyachib@proton.me)
  and Sebastian Cahill are iterating on a Canary processor-level DPIA for biometric
  verification (Incode), part of a broader EMEA GDPR push (Danubius/IHG deals contingent;
  live UK deployment = 2 IHG pilot sites). Alex Foley (external CISO, Axl.net), Martijn
  Dekker, Z Lee, Bree Sullivan et al. CC'd. Gareth CC'd throughout — no direct asks to him.

  **DPIA state**: v0.2 attached to Tanya's Jun 30 email (Canary_Privacy Impact
  Assessment_v0.2.docx) with input needed tagged in comments; she also added a
  "storage location" column to the Data Flow table (needs engineering-accurate answers).
  As of Sebastian's last email (Jul 13) the internal DPIA review discussion had NOT yet
  happened ("yet to have internal discussion"). Thread is now waiting on Tanya's reply
  to Jul 13 questions.

  **Engineering-relevant points**:
  - Retention: Sebastian wrote "30 days after checkout" as default PII deletion window
    (fraud/chargeback rationale), configurable per controller; awaiting Tanya's
    acceptance. DPA retention schedule currently circular/unspecified — needs a real
    per-data-element retention schedule that DPIA/RoPA/DPA all point to.
  - Obfuscation: Tanya challenges retaining the PMS confirmation number in the
    obfuscated dataset (re-identification pathway via hotel PMS) — recommends replacing
    with a Canary-internal reference. RIRA in progress with Renate; CJEU C-413/23 P
    (EDPS v SRB) cited as context. Current working assumption to verify: irreversible
    replacement, no retained mapping.
  - ID image + selfie purge: configurable immediate purge post-OCR shipped
    (Linear EMEA-127 ID image, EMEA-128 selfie; kiosk path was still in progress).
  - Incode side letter still unexecuted — faceprint residual risk stays Medium until
    Incode's deletion practice is confirmed in writing (delete faceprints within defined
    max period, no model training, written retention confirmation).
  - EU AI Act: Tanya recommends per-message "AI" badge in mixed human/AI threads (and
    Voice AI equivalent); Sebastian pushed back Jul 13 (prefers no per-message label,
    esp. for human-reviewed AI drafts) and asked how conservative that advice is. Open.
  - Transcripts: retention of message/voice transcripts needs documented purpose;
    sensitive data (health, religion...) in transcripts ⇒ explicit consent + auto-purge,
    and must be assessed in the processor DPIA. Sebastian asked (open) whether non-PII
    transcripts can be kept indefinitely.
  - PMS data pulls: pre-populating e.g. passport number from PMS is OK only with
    controller lawful basis + instruction.
  - CLI/call forwarding (Dublin hotel, ComReg): Tanya recommends hotel PBX present the
    hotel's own number, not the guest's; Sebastian pushed back (wants guest number for
    follow-up SMS). Open.
  - Processor posture on non-compliant controller configs (e.g. bundled marketing
    consent): notify in writing, don't implement until controller provides written
    risk-acceptance; even then Canary retains exposure as the enabling platform —
    pattern across multiple hotels raises platform-level finding risk.

  **Privacy Pack gaps Tanya flagged**: Swiss addendum missing from DPA (Canary has Swiss
  customers), TIA doesn't exist as standalone, RoPA has gaps (no legal-basis column,
  retention "defaults to never", Activity Log retention indefinite), privacy/cookie
  policy not yet reviewed. Canary not DPF certified — relies on SCCs.

  **No action required from Gareth right now** — this was a read/awareness item. Possible
  future engineering pull-through: 30-day post-checkout purge implementation, PMS
  confirmation-number replacement in obfuscated data, per-message AI labeling, transcript
  retention/purge, storage-location answers for the DPIA data-flow table.
project: null
source_id: https://mail.google.com/mail/u/0/#inbox/19ef51f6db691431
tags:
- morning-gtd
- gmail
- from-awareness
time_minutes: 15
title: 'Read: GDPR DPIA thread (biometric verification) — you''re CC''d, v0.2 attached'
updated: 2026-07-15 16:27:57.456685
waiting_on: null
waiting_since: null
working_on: false
---

Tanya/Sebastian iterating on the DPIA for Canary as processor for biometric verification; v0.2 attached with input tagged in comments; retention written as 30 days after checkout.
https://mail.google.com/mail/u/0/#inbox/19ef51f6db691431