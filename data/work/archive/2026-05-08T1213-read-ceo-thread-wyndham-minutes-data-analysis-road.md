---
area: null
contexts:
- consume
created: 2026-05-08 12:13:55.037025
defer_until: null
due: null
energy: low
id: 2026-05-08T1213-read-ceo-thread-wyndham-minutes-data-analysis-road
order: null
output: '## Agent run 2026-05-08T14:05:00


  **Thread**: "Re: Fwd: Minutes data by category" — wyndham-team Google Group. You''re
  CC''d via the alias.


  **Status as of today (May 8)**: Harman replied to Val''s analysis with: *"This is
  informative. Thanks for sharing Val. I imagine we''ve adjusted the roadmap of areas
  we''re working on given this?"* — open question, no answer back yet. Pending response
  presumably from Val / Jeff (and engineering by extension).


  **Chronology**:

  - May 1 — Jeff (Head of Enterprise Sales) asked Janesh Patel (SVP, Wyndham Global
  Contact Center) for handle-time-by-category data, to align Canary''s roadmap with
  their cost-reduction goals.

  - May 2 — Janesh: teams can''t generate handle-time-to-reason-codes as a report.
  They manually listened to 250 calls and produced a sheet. Stated focus is "answering
  revenue calls, confirmations, cancels, and modifications". Noted Justin Shaughnessy
  is meeting Canary in STJ next week.

  - May 4 (internal) — Jeff to Harman: wrap descriptions don''t help much for prioritizing;
  should we take first turn at sending capability list back to Janesh, or is that
  too risky?

  - May 5 — Harman: "Not sure I''m understanding. What do you mean by the first turn
  on listing out our capabilities?"

  - May 6 — SJ Sawhney looped wyndham-team in, suggested pulling raw audio for analysis
  + agent training.

  - May 6 — Ani: we already have the audio (Drive folder, Wyndham still sending calls).
  Val and team had already done initial analysis.

  - May 6 — **Val''s analysis (the meat)** — see below.

  - May 8 (today) — Harman''s roadmap-adjustment question.


  **Val''s analysis** — pulled the 10K+ calls beyond Janesh''s 250 sample, re-weighted
  forecast by call duration (minutes) instead of call count.


  Call-center level (% of volume → % of minutes):

  - SRS: 38% → 25% (short, mostly IVR cancels)

  - Gen Res: 51% → 63% (longer, agent-driven)

  - Wyndham Rewards: 9% → 10% (flat overall, mix changes a lot)

  - Customer Care: 2% → 2%


  Gen Res (% of Gen Res calls → % of Gen Res minutes):

  - Booking without points: 14% → 19%

  - Partner redirect: 5% → 8%

  - Cancellation: 40% → 34% (still biggest, proportionally less)

  - Other: 23% → 19%


  Wyndham Rewards — biggest shift:

  - Check point balance: 22% → 10% (~2:30 avg, IVR self-serve)

  - Password change: 15% → 4% (~1:40 avg)

  - Redeem points for free rooms: 17% → 22% (~7:30 avg, agent-handled)

  - Redeem points for discounted rooms: 8% → 10%

  - Other (account merge, retro credits, fraud integrity): 26% → 40%


  Val''s recommendations for the capability list back to Wyndham:

  1. **Elevate redemption flows (free + discounted)** from P2/P3 — ~32% of WR handle
  time, matches Janesh''s "answer revenue calls".

  2. **Keep Gen Res booking-without-points P2** with real engineering investment —
  jumps 7% → 12% of total minutes.

  3. Check-point-balance + password change still automatable but smaller than the
  call-count view implies; shouldn''t crowd out redemption.

  4. **Re-scope WR "Other"** (account merges, retro credits, fraud, missing-points
  claims) — 40% of WR minutes; some of this feasible via voice AI.


  Sheet: https://docs.google.com/spreadsheets/d/1S9oDYDhWsfxEzpuufp70g28qITuXXtKZWPX2VQynO80/edit

  Audio folder: https://drive.google.com/drive/folders/1E_ibjVkYWu8LDadksp2B16mG3SSsvkpa


  **Why you''re CC''d / what''s potentially relevant for engineering**:

  - Roadmap-prioritization shift implied — redemption (free + discounted), Gen Res
  booking-without-points, and WR "Other" escalations all need elevation; check-balance
  / password-change can come down a peg in priority order.

  - STJ meeting with Justin Shaughnessy is *next week* — the capability list (and
  any roadmap-adjustment story) needs to be tight before then.

  - Harman''s question is the live thread state. If Val/Jeff don''t have a written
  roadmap-adjustment answer ready, engineering leadership may be pulled in.

  - Bear had no prior notes on this minutes-vs-calls analysis. This is fresh context.


  **No reply needed from you on the thread itself** — the open ask is to Val/Jeff,
  not to engineering directly. But worth keeping awareness of: if a "did we actually
  adjust the roadmap?" check-in lands on the voice/AI team, you''ll want this context
  to hand. Possible follow-up next-actions you might want to capture: (1) confirm
  with Val/voice-team lead that the roadmap actually reflects this re-weighting before
  STJ; (2) skim the spreadsheet if you want to validate the categorization yourself.

  '
project: null
source_id: ceo-thread-wyndham-minutes-2026-05-08
tags:
- morning-gtd
- gmail
- from-awareness
time_minutes: 10
title: 'Read CEO thread: Wyndham minutes data analysis — roadmap adjustment Q'
updated: 2026-05-08 14:54:37.049043
waiting_on: null
waiting_since: null
working_on: false
---

Harman asked Val if we've adjusted the roadmap given the call-recording analysis (10K+ Wyndham calls, re-weighted forecast by call duration). I'm CC'd on wyndham-team. https://mail.google.com/mail/u/0/#inbox/19dfe590f4c83b7c