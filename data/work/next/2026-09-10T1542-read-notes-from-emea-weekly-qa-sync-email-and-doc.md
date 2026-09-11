---
area: null
completed_at: null
contexts: []
created: 2026-09-10 15:42:15.191340
defer_until: null
due: null
energy: low
id: 2026-09-10T1542-read-notes-from-emea-weekly-qa-sync-email-and-doc
order: null
output: |-
  ## Agent run 2026-09-10T17:11:34

  Sources:
  - Gemini notes doc (Sep 10, 2026, owner Martijn; includes full transcript tab): https://docs.google.com/document/d/1ajt1UoVvTMVgvG9asHDhMgZ1Wknu_ActmTj8rr4VA_E/edit
  - Email "Notes: EMEA - Weekly QA Sync Sep 10, 2026" from gemini-notes@google.com (Gmail thread 1a08b49eecbacb26): https://mail.google.com/mail/u/0/#all/1a08b49eecbacb26

  TL;DR: Only Lorena and Martijn actually attended (~20 min; Lorena: "it's just the two of us today"). No action items for Gareth. No decisions were made; both "decisions" are flagged Needs Further Discussion.

  What was discussed:
  1. QA <-> EMEA collaboration. Lorena says QA struggles to prioritise across IHG, Wyndham, Best Western. She restated the proposal (attributed to "he", almost certainly Gareth's June EMEA QA initiative): QA generates test plans/cases for CS to run per hotel, plus automation, then a retro to judge whether it's worth it. She explicitly wants a retro "at some point".
  2. Martijn is distanced from it. He says his team is removed from current EMEA strategic accounts (e.g. HOST, owned by PMS Gateway / arrivals-departures teams) and can't track all regional project detail.
  3. Duplicated work. Lorena's concern: a PMS Gateway engineer (transcript says "Martin"; likely not Martijn Dekker, whose team isn't on HOST) did a lot of HOST certification work, yet similar integration validation is repeated per hotel/contract. She has no solution for reusing verification work. Martijn: product x integration x custom requirement (UDFs etc.) permutations are effectively infinite, so reuse is hard.
  4. Strategic account playbook (Sebastian's). Martijn strongly wants it rolled out to ALL accounts, including in-flight ones: rate-code segmentation for isolated end-to-end journey testing, plus a CS checklist. Many CS people don't know it exists. Lorena will re-read it.
  5. IHG vs EMEA scaling. IHG onboarding-script testing hits thousands of hotels at once; EMEA is one bespoke hotel at a time, so not scalable. Wyndham easier due to a default config.
  6. Proactive post-go-live monitoring. Martijn: CS doesn't monitor Twilio errors or Meta approval/utility status of WhatsApp check-in templates; hotels edit journey messages, templates get unapproved, conversion drops, and it surfaces reactively via client -> CSM/support -> on-call. He is prototyping monitoring/alerts or a monthly review. Lorena suggested auto-creating Linear triage issues; she wants the same for Best Western, HotelKey and Wyndham.
  7. HotelKey hidden feature flag. Demoing HotelKey with Andre (new solutions engineer), Martijn found message configuration needs an undocumented, engineer-only feature flag. Lorena: QA hits this constantly; monorepo too big even for Claude to reliably surface. Martijn's team documents every product they touch (voice, mobile key).

  Next steps recorded (none owned by Gareth):
  - [Martijn] Send strategic account playbook to Lorena.
  - [Lorena] Review the playbook.
  - [Martijn] Set up a process to monitor Twilio errors / config issues.

  Possibly relevant to Gareth (my read, not from the notes):
  - The QA-collab experiment Gareth kicked off in June (https://docs.google.com/document/d/1Lw8X4v-fS2-0zkKTHOSYNkf26FV4tmHFk6yRfWO5IF0/edit) is drifting: Lorena is unsure what to work on and wants a retro. Martijn still sees the real gap as CS capability, consistent with his June objection (https://docs.google.com/document/d/1h1_uEjJw4K1Fp7iURHy3SAo7MgSF7vr_7h0xj4jzHH4/edit). Could be worth scheduling that retro.
  - Proactive Twilio/WhatsApp-template monitoring overlaps with the enterprise brand monitors (bw-monitor, wyndham-monitor, ihg-monitor, ent-monitor). Worth syncing with Martijn so it isn't built twice.
  - HotelKey messaging feature flag being undocumented is a concrete doc gap; could become a small docs ticket.

  Also noticed: the Sep 3 "EMEA - Weekly QA Sync" notes email is still UNREAD (thread 1a0673cc8f15eeeb; doc https://docs.google.com/document/d/1tFUFCTyYQ8Y_mN5cMSOyU7QtkRL1QMHzFKX8HIGb4Mw/edit). It covered GDPR retention schedules (30-day fallback), ID visibility audit, and pilot status ("Dubious" per Gemini, Kempinski, HOST cert). Not reviewed in depth here.
project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 5
title: read Notes from “EMEA - Weekly QA Sync” email and doc
updated: 2026-09-11 11:18:49.660964
waiting_on: null
waiting_since: null
working_on: false
---