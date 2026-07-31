---
area: null
contexts: []
created: 2026-07-30 14:36:51.834808
defer_until: null
due: null
energy: low
id: 2026-07-30T1436-review-gdpr-email-thread
order: null
output: |
  ## Agent run 2026-07-31T08:18:16Z

  Reviewed the "Re: Subject: GDPR Compliance" Gmail thread (12 messages, Jun 23 - Jul 29 2026)
  between Sebastian Cahill (scahill@) and Tanya Chib, external privacy counsel at Privacy Rules
  (tanyachib@proton.me); you are cc'd. Thread link (from this item's body):
  https://mail.google.com/mail/u/0/#inbox/FMfcgzQgMVlgssGfKqFPBpnGWQRNKMQh

  ### What the thread covers
  Building Canary's customer-facing "privacy pack": DPIA for biometric/ID verification (Incode),
  DPA, RoPA, TIA, privacy + cookie policies — plus a running set of legal Q&As that have direct
  engineering impact.

  ### Engineering-relevant rulings from counsel
  - **EU AI Act disclosure (Webchat/Messaging/Voice AI)** — Tanya's position (Jul 15 + Jul 29):
    - Messages sent autonomously by AI (no human in send loop) need a per-message "AI Assistant"
      label/signature. Draft-assist messages genuinely reviewed and sent by staff do NOT need it.
    - An upfront first-message disclosure ("you're chatting with an AI-powered virtual assistant")
      is ALSO required — a webchat footer note is supplementary only, not a substitute.
    - Applies based on where the guest/recipient is (EU), not where the property is
      (Art. 2(1)(c) + Art. 50 Guidelines para 10). Same obligations for Voice AI.
  - **Retention / obfuscation (feeds the GDPR Obfuscation Service design)**:
    - Sebastian proposed 30 days post-checkout as default PII deletion/anonymization window
      (fraud/chargeback rationale), controller-configurable earlier.
    - Transcripts may be retained only with documented purpose + lawful basis; sensitive data
      (health, religion...) needs explicit consent + automatic purge; if truly anonymized
      (not linkable via booking/property/dates context) GDPR doesn't apply — retention is free.
    - DPA/RoPA currently lack per-data-element retention periods (RoPA says "defaults to never",
      Activity Log retention indefinite) — flagged as not customer-ready.
  - **PMS data pulls**: pre-populating e.g. passport numbers from PMS is fine if the hotel
    (controller) has lawful basis, has disclosed it, and instructs Canary as processor.
  - **Call forwarding / CLI**: presenting the guest's number when routing through Canary is not
    spoofing, provided the hotel's privacy notice covers the purpose.

  ### Open items as of last message (Jul 29, Sebastian; Jake Wilhelm now added)
  1. Sebastian's 4 unanswered questions to Tanya: (a) how recipient-location-based disclosure is
     actioned in practice (3 scenarios: US guest in EU / EU guest in US / etc.), (b) whether
     machine-readable marking (Art. 50(2)) + upfront disclaimer suffices instead of a
     human-readable per-message signature, (c) confirm footer is optional, (d) confirm hotels
     with AI disabled need no disclaimers.
  2. Cookie policy review — Tanya to revert "next week" (w/c Aug 3; she was off rest of Jul 29 week).
  3. DPIA v0.2 — Sebastian still owes Canary's internal response (storage locations, TOMs, DPF).
  4. Incode side letter still unexecuted — faceprint residual risk stays Medium until then.
  5. DPA (now with Swiss addendum) + RoPA redlines shared with team Jul 28 for review.

  ### Relevance to your work
  The AI-label rules (autonomous vs draft-assist, first-message disclosure) are the same
  questions Mati/Bernard raised in #epd-emea-gdpr, and the 30-day anonymization default +
  per-entity retention schedule is a direct input to the Canary GDPR Obfuscation Service design
  doc you're reviewing with Martijn Dekker. No action was requested of you in the thread itself.
project: null
source_id: null
tags: []
time_minutes: 5
title: review gdpr email thread
updated: 2026-07-31 12:44:01.620328
waiting_on: null
waiting_since: null
working_on: false
---

https://mail.google.com/mail/u/0/#inbox/FMfcgzQgMVlgssGfKqFPBpnGWQRNKMQh