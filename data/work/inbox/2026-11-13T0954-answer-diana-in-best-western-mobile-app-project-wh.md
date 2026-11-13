---
area: null
completed_at: null
contexts:
- react
created: 2026-11-13 09:54:28.196189
defer_until: null
due: null
energy: medium
id: 2026-11-13T0954-answer-diana-in-best-western-mobile-app-project-wh
order: null
output: |-
  ## Agent run 2026-11-13T10:09

  Nothing was posted. A draft reply is below for you to send or edit.

  ### What the tag actually is

  Diana tagged you at 11:13 GMT on Nov 12, ten minutes into your 1-1 with her (Granola: https://notes.granola.ai/d/c5de9107-3f90-4e4d-bcbe-c7a681ab71bd). It is a pointer to the thread she was describing, not a fresh question. In that 1-1 you said you would get Connor's take and come back to her with a next step. That is the open commitment.

  ### The decision has mostly moved on since the thread started

  - Best Western declined codebase access on Nov 10. Connor: "Monte doesn't want to give us access to the codebase - we're going to get access to test versions of the app for us to test but won't be directly touching code (as of now)", and BW is bringing Telus back to finish the work they did not complete, reg card included. https://canarytechnologies.slack.com/archives/C0AQLLSLGH0/p1794352746877039?thread_ts=1794349692.962069&cid=C0AQLLSLGH0
  - Leopoldo Toro (after talking to Ron Stenger) asked for a pause on any code work until a lightweight SOW and contract terms are signed: incidents, support and cybersecurity are all undefined today. Connor agreed. https://canarytechnologies.slack.com/archives/C0AQLLSLGH0/p1794349692962069
  - So Caitlyn's option 3 (Telus owns) is the de facto state. Her three options: https://canarytechnologies.slack.com/archives/C0AQLLSLGH0/p1794266110062059?thread_ts=1794257012.596689&cid=C0AQLLSLGH0
  - Diana's last messages in the thread (Nov 10) predate or sit alongside this; she was not in Leopoldo's thread, so she may not have registered that option 1 is off the table.
  - The BW call did happen on Thursday Nov 12. The only readout in the channel is Martin's: BW said there is no BRD, only Figma, though Connor confirms the BRD doc is theirs and the miss was WorldHotels not directing Telus. https://canarytechnologies.slack.com/archives/C0AQLLSLGH0/p1794511069714339
  - Scope is check-in only (Connor, Nov 10), with custom views, so BW/Telus own the UI.

  ### Not verified

  - Whether you raised this with Connor. Your Nov 12 14:16 session with Andrea and Connor (https://notes.granola.ai/d/0c5e49d3-f540-48d6-948d-4d2b9e6638d6) has no note or transcript hit on the BW app, Telus or codebase access; BW came up only for Skim, card embed and the Jan 5 rebrand. The draft below therefore does not claim a Connor conversation. Add his take if you have it.
  - I have no readout of what the Nov 12 BW call decided about Telus resourcing.

  ### Draft reply (thread: https://canarytechnologies.slack.com/archives/C0AQLLSLGH0/p1794481981112849?thread_ts=1794257012.596689&cid=C0AQLLSLGH0)

  The position is built from what you said in the 1-1 (be led by the client, open to it with the right relationships, read access helps even if they make the edits) plus the Nov 10 developments.

  > Catching up on this after my 1-1 with Diana. My read:
  >
  > 1. Telus should own the integration. Monte has said no to codebase access and BW is bringing Telus back, so that is where we are anyway, and I think it is the right default. Caitlyn's concern is the one that worries me most: with one Telus dev on their side, anything we write in their app becomes ours to fix forever.
  > 2. We can still get most of the speed benefit without owning their code. I'd offer an IHG-style focused integration week (remote is fine) aimed at the reg card hard-codes, and ask for read-only access to the SDK embed so we can debug and give Telus exact instructions rather than guessing from test builds.
  > 3. If BW later comes back and asks us to write code, that is a separate decision with two gates: the SOW Leopoldo described (scope limited to the SDK embed, custom views UI stays theirs, a named owner on their side for maintenance, time-boxed), and an explicit call on what moves in Q4B, since Caitlyn has flagged it lands on Wyndham BLE and Guest App.
  >
  > Diana, Caitlyn: does that match where you landed after Thursday's call?

  ### Suggested follow-ups (yours to decide)

  - Get Connor's read on the Nov 12 call outcome before or after sending; the draft is safe either way.
  - Diana asked in the 1-1 who made the original Wyndham arrangement and wants the team protected from a repeat. Point 3 covers that; worth saying to her directly.
project: null
source_id: https://canarytechnologies.slack.com/archives/C0AQLLSLGH0/p1794481981112849?thread_ts=1794257012.596689&cid=C0AQLLSLGH0
tags:
- morning-gtd
- slack
time_minutes: 15
title: 'Answer Diana in #best-western-mobile-app-project: who integrates the SDK into
  the BW app'
updated: 2026-11-13 10:09:30.000000
waiting_on: null
waiting_since: null
working_on: false
---

Diana tagged me (bare @) on Connor's thread: Best Western is pushing back on Telus, and Connor wants BW to give us their codebase so we do the reg-card cleanup. Caitlyn worries we would own fixes forever (Wyndham model vs IHG model vs Telus owns) and that it delays Wyndham BLE and Guest App. The BW call was moved to Thursday Nov 12. Open 1 day, no reply from me.
https://canarytechnologies.slack.com/archives/C0AQLLSLGH0/p1794481981112849?thread_ts=1794257012.596689&cid=C0AQLLSLGH0