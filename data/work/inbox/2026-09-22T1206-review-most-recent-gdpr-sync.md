---
area: null
completed_at: null
contexts: []
created: 2026-09-22 12:06:52.487443
defer_until: null
due: null
energy: low
id: 2026-09-22T1206-review-most-recent-gdpr-sync
order: null
output: |
  ## Agent run 2026-09-22

  Most recent GDPR sync notes in email: Gong recording of "Weekly GDPR sync", Sep 16 2026, 26 min
  (https://us-66902.app.gong.io/call?id=6950190727898807981). Gmail message id 1a0aadc7a7a85916, still UNREAD.
  Participants: Martijn Dekker, Sebastian Cahill, Z Lee, James Saram, Bernard, Greg, Alina Glumova, Alex (+ others).

  ### Key points
  1. Spain expansion: Martijn wants to grow the Canary team in Spain; a new partner manager is joining in Madrid.
  2. GDPR rollout status (EMEA eng): solidifying country defaults, finalising hotel dashboard designs, end-to-end data obfuscation testing.
  3. IHG kiosk/check-in: Sebastian working on locale-specific consent and notice language for the scripts.
  4. GDPR UI dashboard: James training product teams and preparing CS comms ahead of rollout.
  5. Customer notification strategy: still debating how to communicate the rollout; option to frame it as a UI change.
  6. French local storage question: a French property manager keeps asking about localStorage use for chat session IDs; Bernard raised a messaging-team ticket.
  7. S3 bucket audit: Alina updating policies, closing open public buckets, identifying dead buckets to remove.
  8. SIEM for PII: Bernard moving investigation data to SIEM to cut PII in Groundcover; SIEM access limited to security team + leads.
  9. Fuel Travel breach: phone numbers leaked at Jonas Krum / Fuel Travel; Bernard sees a surge in WhatsApp spam/phishing inquiries as a result.
  10. AI governance: Alex flagged no formal AI governance or questionnaire-response process; wants a dedicated oversight meeting.

  ### Next steps recorded on the call (none assigned to Gareth)
  - James: walk Annie through the GDPR UI dashboard on Fri Sep 18.
  - Greg: Notion page tracking breached companies (when, method).
  - Bernard: DM Alex the AI team lead's name; share the AI model doc ("iicco") with Alex.
  - Alex: talk to Z about setting up an AI governance / oversight meeting (inventory + ownership).
  - Sebastian: trust center mechanism to prompt doc refreshes (e.g. EU AI Act classification) via expiry dates + admin pings.

  ### Things worth Gareth's attention
  - Point 6 lands on the messaging team. Worth checking the ticket exists and has an owner, since it's a recurring customer inquiry.
  - Point 2 (obfuscation e2e testing, country defaults) is the EMEA eng workstream; no blockers noted on the call.
  - Point 9 may explain any recent uptick in WhatsApp-related support noise.
  - Follow-on meeting already on calendar: "GDPR customer comms sync", Wed Sep 23 16:30-17:00 EEST, invited by James Saram (Gmail thread 1a0a4c9ebec9a1dc). Point 5 above is the agenda.

  Older syncs in the same 30-day window, for context: Sep 9 (attestation letter blurb, Gmail 1a086ca4bcea6ed6) and Sep 2 (Alina joining security, Gmail 1a062c414265664e, starred).
project: null
source_id: null
tags: []
time_minutes: 5
title: review most recent gdpr sync notes from email
updated: 2026-09-22 12:08:00.409164
waiting_on: null
waiting_since: null
working_on: false
---