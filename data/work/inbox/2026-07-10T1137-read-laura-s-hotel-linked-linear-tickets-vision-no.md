---
area: null
contexts:
- consume
created: 2026-07-10 11:37:07.430570
defer_until: null
due: null
energy: low
id: 2026-07-10T1137-read-laura-s-hotel-linked-linear-tickets-vision-no
order: null
output: |
  ## Agent run 2026-07-13T14:10:00

  Read the page (https://app.notion.com/p/canarytechnologies/Hotel-linked-Linear-tickets-vision-398814686151800984ecd164282e5683). Summary:

  **End state:** Every Linear ticket about a hotel is linked to that hotel and visible to
  staff on its property page, replacing today's manual Linear/Zendesk searching. Linking and
  showing are treated separately: link every ticket from every source (recording how each
  link was made via a `source` field; guessed links get a review flag), but choose per
  audience/phase what the property page actually shows.

  **Prior art:** `ZendeskTicketHotel` (in `internal_support`) already does this for Zendesk —
  ticket ID column, FK to hotel, `source` field (AI extraction vs person), matched text for
  auditing, exact-match-only extraction with cross-region search. `LinearIssueHotel` copies
  this shape.

  **Three phases:**
  1. Tickets from Canary manage-page forms (integration request / PMS migration send hotel ID
     directly; New Issues form has parseable @-mentions) + backfill. Eng design: TOOL-399
     (https://linear.app/canary-technologies/issue/TOOL-399); approved recommendation on
     TOOL-371 (https://linear.app/canary-technologies/issue/TOOL-371).
  2. TOOL-400 (https://linear.app/canary-technologies/issue/TOOL-400) — linear_agent already
     resolves hotels during Oncall triage into `LinearIssueContext`; write a link row there
     + backfill existing rows.
  3. TOOL-401 (https://linear.app/canary-technologies/issue/TOOL-401) — extend extraction
     beyond Oncall triage to any team; guessed matches flagged for review. CustOps and
     hand-created INT tickets benefit first.

  **Key rules:** one link table (`LinearIssueHotel`, many-to-many); keyed on Linear issue UUID
  (not ONC-1234-style identifiers, which change on team moves — current identifier fetched
  live); deterministic sources never guess and AI-proposed matches need lookup confirmation
  before save; nothing depends on the stale `LinearIssue` cache table; links live in the
  hotel's own region; ticket status fetched live from Linear, never stored (page degrades
  gracefully if Linear is down).

  **Related:** PRD (https://app.notion.com/p/c5406fb00ea84a6ead49d924179633c0); Linear project
  "Show Hotel-Related Linear Tickets on the Property Page"
  (https://linear.app/canary-technologies/project/show-hotel-related-linear-tickets-on-the-property-page-54331254b86c).

  Note: the page has two inline discussion markers (on the per-audience "showing" paragraph
  and the Phase 3 paragraph), but the comments API returned nothing — likely resolved threads.
  No action taken beyond reading; nothing posted anywhere.
project: null
source_id: https://mail.google.com/mail/u/0/#inbox/19f4910835ef11f9
tags:
- morning-gtd
- gmail
time_minutes: 15
title: 'Read Laura''s ''Hotel-linked Linear tickets: vision'' Notion page'
updated: 2026-07-13 14:10:00.000000
waiting_on: null
waiting_since: null
working_on: false
---

https://app.notion.com/p/canarytechnologies/Hotel-linked-Linear-tickets-vision-398814686151800984ecd164282e5683