---
area: null
completed_at: null
contexts: []
created: &id001 2026-10-08 14:24:28.966146
defer_until: null
due: null
energy: null
id: 2026-10-08T1424-review-staff-notes-in-messaging-prd-with-prepared
order: null
output: ''
project: null
source_id: null
tags: []
time_minutes: null
title: Review Staff Notes in Messaging PRD with prepared points
updated: *id001
waiting_on: null
waiting_since: null
working_on: false
---

Review PRD: Staff Notes in Messaging (Belinda Wang)
https://app.notion.com/p/canarytechnologies/PRD-Staff-Notes-in-Messaging-3eb814686151817f92f1f4195c733181

Points to raise:

**Where notes live (req 2):** today ReservationNote has a required `reservation` FK and no thread link. The PRD wants the note on the conversation (chat.Thread), plus the reservation when there is one, so the migration makes `reservation` nullable and adds a `thread` FK (separate migration PR). Thread <-> reservation is many-to-many through guests (chat/models/thread.py:86-89), so these cases are undefined:
- A Messaging note on a thread linked to 2+ reservations: which reservation(s) does it attach to? A single FK can't hold both.
- A Check-in note on a reservation with several threads (SMS/WhatsApp/webchat): which thread(s) get the grey line?
- "Reservation linked later": backfill the FK when the link happens, or look notes up through the links at read time? (Read time makes the FK redundant.)
- Unlinking: do notes disappear from Check-in/Messaging?
- Suggest: a note has exactly one owner (thread OR reservation) and is shown wherever it's reachable through links at read time.

1. Writer-only edit (req 3): today reservation_note_view.py has no ownership check, so this is a real Check-in behaviour change. There's no manager override for inappropriate notes or notes left by a staff member who has since left.
2. Guests never see notes (req 5): doesn't cover the AI side. If the AI reply agent or summaries read activity lines or notes as context, a note could leak through a generated reply. Name AI context, transcripts and exports explicitly.
3. Grey lines (reqs 8/9) depend on the per-hotel flag CHAT_THREAD_ACTIVITY_EVENTS; nobody has checked how many hotels have it on, and turning it on also changes other lines those hotels see. Rollout dependency.
4. "Nothing phased" while most dependencies have TBD owners and are Not started. Req 10 (close returns to the conversation) is the most separable piece.
5. Access (req 4): the endpoints are gated on CHECK_IN_HAS_PRODUCT_ACCESS. Which permission replaces it? Probably both, OR'd, with the reservation-scoped endpoints still Check-in gated.
6. "Open questions: None" doesn't hold up given the above.
7. The handoff-to-reply metric (with vs without notes) is self-selected. Treat it as directional or compare before and after per hotel.