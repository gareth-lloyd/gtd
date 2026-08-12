---
area: null
completed_at: 2026-08-12 11:46:14.949433
contexts:
- react
created: 2026-08-10 11:40:42.968217
defer_until: null
due: null
energy: medium
id: 2026-08-10T1140-reply-to-sj-sawhney-re-wyndham-july-reservation-to
order: null
output: |
  > **CURRENT ANSWER — scope: the ~4,770 live Wyndham Connect sites only.**
  > July-arrival reservations: **4,887,531** all statuses / **3,999,115** excluding
  > cancellations. Sent 1,730,647 (**43.3%**), submitted 317,396 (**7.9%**).
  > **~2.27M reservations at live properties we never sent to.**
  > Full working + the draft reply to send are in the 14:16Z run at the bottom.
  > The 14:11Z run below is the earlier whole-portfolio cut, kept for the methodology
  > only — **its numbers are superseded.** Nothing has been sent to anyone.

  ## Agent run 2026-08-10T14:11Z — SUPERSEDED SCOPE (whole Wyndham Portfolio)

  Answered the denominator question from Snowflake. Retained for the reproduction /
  verification work, which still stands. The scope was later narrowed to live Connect
  sites only — see the 14:16Z run for the numbers to actually use.

  Thread: https://mail.google.com/mail/u/0/#inbox/19fce4e9cb549c58
  Draft also saved at: /private/tmp/claude-501/-Users-garethlloyd-projects-canary/b7c7eee4-3c6e-4c4e-a883-2758d697d30d/scratchpad/sj-reply-draft.md

  ### Methodology is verified, not assumed

  I reverse-engineered the basis of Ani's reported figures before answering, so the
  denominator is measured on exactly the same population as the numerator:

  - Scope: `analytics_public.dim_portfolio` portfolio_id **166 "Wyndham Portfolio"** (6,572 hotels)
  - Grain: reservations with **arrival_date in July 2026**, `reservation_status <> 'cancelled'`
  - Sent = `fact_check_in` with any of email_sent_at / sms_sent_at / whatsapp_sent_at
  - Submitted = `fact_check_in.submitted_at IS NOT NULL`

  Reproduction check against the email:
  | metric | Ani reported | my query | delta |
  |---|---|---|---|
  | Sent check-ins | 1,753,043 | 1,754,949 | +0.11% |
  | Submitted check-ins | 321,129 | 321,134 | +5 rows |

  Matching to 0.1% confirms the scope definition. Residual is CDC replication lag.

  ### The answer to SJ's question

  - **Total July-arrival reservations, all statuses: 5,931,293**
  - Cancelled: 1,080,174
  - **Non-cancelled (the real addressable base): 4,851,119**

  So: sent 1.75M = **36.2%** of reservations. Submitted 321k = **6.6%** of reservations
  (vs the 18.3% quoted, which is submits/sends). **We could not send to ~3.10M reservations.**

  ### Where the 3.10M gap goes

  | # | Reason | Reservations | % of gap |
  |---|---|---|---|
  | 1 | Properties not activated for check-in messaging | 796,398 | 25.7% |
  | 2 | No email AND no phone on the PMS record | 703,363 | 22.7% |
  | 3 | No check-in record ever created (active hotels) | 584,828 | 18.9% |
  | 4 | Booked <24h before arrival (send window closed) | 387,073 | 12.5% |
  | 5 | `booked_at` NULL — unclassifiable | 414,977 | 13.4% |
  | 6 | Other | 209,531 | 6.8% |

  **Bucket 1 is the headline and it's an activation problem, not a product one.**
  1,246 properties fed us July reservations and sent literally zero check-ins.
  Of those, 1,227 have `has_check_in_messages = false` and 739 have `is_live = false`.
  This is consistent with Ani's activation table: 4,770 live Connect sites out of
  6,572 portfolio hotels.

  Per-hotel send-rate distribution (non-cancelled July reservations):
  - 1,246 hotels @ 0% send rate — 796,398 reservations
  - 66 hotels @ <10% — 58,646
  - 1,049 hotels @ 10–35% — 780,183
  - 3,426 hotels @ 35–60% — 2,981,831  (the healthy bulk)
  - 308 hotels @ 60–85% — 232,577
  - 10 hotels @ 85%+ — 1,484

  **Contactability ceiling:** only 3,193,212 of 4,851,119 reservations (65.8%) arrived
  with any email or phone at all. Of that reachable pool we sent to 1.75M = **55%**.
  That's the more flattering and arguably fairer framing if SJ pushes back.

  Bucket 3 (585k) is the one I could not fully explain and it is worth a follow-up:
  these are ordinary transient reservations (`reservation_kind = 'reservation'`,
  `created_via = 'reservation'`) at properties that were actively sending — not group
  or multi-room masters. Candidate causes: mid-month activation dates, `cutoff_checkin_hours`
  config, or PMS sync gaps. Not investigated further.

  ### Caveat to state if you use these numbers externally

  "Reservations" is per-booking, not per-guest — one guest booking three rooms counts
  three times. So the true "guests we couldn't reach" number is somewhat lower than 3.1M.

  ### Draft reply — REMOVED

  This run's draft quoted the whole-portfolio denominator (5.93M / 4.85M / 36%) and led
  on the property-activation bucket. That framing was rejected. Deleted deliberately so
  it cannot be pasted into the thread by mistake — **use the v2 draft in the run below.**

  ### Suggested follow-ups from this run (superseded — see run below)

  - ~~Get the 1,246 zero-send property list to Ani/Bryan as an activation target list.~~
    Out of scope: those properties are not live on Connect.
  - Investigate bucket 3 (585k missing check-in records at active hotels). **Still valid**
    and carried forward — it survives the rescope at 580k.

  ## Agent run 2026-08-10T14:16Z — REVISED SCOPE (supersedes the run above)

  Gareth's steer: **the ~4,770 live Wyndham Connect sites are the true denominator —
  non-live members of the Wyndham Portfolio are out of scope.** Everything below
  replaces the numbers in the previous section. Use THIS draft, not the earlier one.

  ### Scope now used

  `dim_portfolio` portfolio 166 ∩ `dim_hotel.is_live` ∩ `has_check_in_messages`
  = **4,821 properties** with July reservations. Sensitivity-checked against two
  alternative definitions, all within 0.5%:

  | scope definition | hotels | reservations | sent | submitted |
  |---|---|---|---|---|
  | portfolio 166 ∩ live ∩ check-in msgs (**used**) | 4,821 | 3,999,115 | 1,730,647 | 317,396 |
  | Wyndham Connect GMS portfolio ∩ live | 4,807 | 3,991,501 | 1,723,726 | 315,663 |
  | Connect GMS ∩ live ∩ active ∩ check-in msgs | 4,801 | 3,977,668 | 1,722,318 | 315,186 |

  Restricting to live sites keeps **98.6% of the sends** (1,730,647 of 1,753,043) but
  cuts the denominator from 4.85M to 4.00M. The ~22k sends outside the live set come
  from deactivated / not-yet-live properties still emitting traffic.

  ### The answer to SJ, revised

  - **Total July-arrival reservations at live Connect sites, all statuses: 4,887,531**
  - Cancelled: 888,416
  - **Non-cancelled — the denominator to quote: 3,999,115**

  Sent 1,730,647 = **43.3%** of reservations. Submitted 317,396 = **7.9%** of reservations.
  **~2,268,468 reservations at live properties we never sent to.**

  ### Where the 2.27M gap goes (live sites only)

  | Reason | Reservations | % of gap |
  |---|---|---|
  | No email AND no phone from the PMS | 684,945 | 30.2% |
  | Booked within 24h of arrival | 620,881 | 27.4% |
  | No check-in record ever created | 580,387 | 25.6% |
  | Other / unexplained | 382,255 | 16.9% |

  Two changes from the first run worth knowing about:

  - The "properties not activated" bucket (796k) is **gone by construction** — that was
    entirely non-live properties, which is exactly what this scope excludes. The gap is
    now a pure product/data funnel, which makes it a fairer thing to put in front of SJ.
  - The earlier `booked_at NULL` bucket (415k, unclassifiable) is **resolved**. Falling
    back to `fact_reservation.created_at` for lead time classifies all of them; they
    redistribute into the 24h and other buckets. No unclassifiable residue remains.

  Note the 24h bucket is not a hard wall: 1,423,066 reservations were booked inside 24h
  and we still reached 802,185 of them (56%). So it's where we lose the most, not where
  sending is impossible.

  ### Contactability ceiling (the fairer framing)

  Of 3,999,115 reservations at live properties, **2,673,540 (66.9%)** were reachable at
  all — i.e. had a check-in record and an email or phone. Of that reachable pool we sent
  to 1,730,647 = **64.7%**. Contact data is the ceiling, not send execution.

  ### Still unexplained — the one worth chasing

  **580,387 reservations at actively-sending properties never generated a check-in record.**
  All ordinary transient bookings (`reservation_kind = 'reservation'`), not group or
  multi-room masters. Candidates: mid-month activation dates, `cutoff_checkin_hours`
  config, PMS sync gaps. Not investigated — this is the largest fixable item in the gap.

  ### Caveats to carry if these numbers travel

  - `dim_hotel.is_live` is a **current** snapshot (as of 2026-08-10), not as-of-July. A
    property that went live in early August is counted live for July arrivals. Ani's
    +31 net Connect activations in July implies the distortion is small, but it exists.
  - My live-site count is 4,821 vs Ani's reported 4,770 — same drift, plus Ani's figure
    is a point-in-time end-of-July count.
  - "Reservations" is per-booking, not per-guest — one guest booking three rooms counts
    three times. True "guests we couldn't reach" is somewhat below 2.27M.

  ### Draft reply v2 (yours to edit — I have NOT sent anything)

  > Counting only properties live on Wyndham Connect, July arrivals were 4.89M
  > reservations, or 4.00M excluding cancellations. That's the denominator. Against it,
  > the 1.75M sends is 43% of reservations and the 321k submissions is 7.9%.
  >
  > So there were ~2.27M reservations at live properties we never sent to. Four reasons:
  >
  > 1. No email or phone on the reservation — 685k (30% of the gap). Nothing came across
  >    from the PMS to send to. Only 67% of reservations at live properties arrive with
  >    any contact method at all.
  >
  > 2. Booked inside 24h of arrival — 621k (27%). Same-day and walk-in business, where
  >    the send window has largely closed. Not a hard wall — we still reached 56% of that
  >    cohort — but it's where we lose most.
  >
  > 3. No check-in record ever created — 580k (26%). Ordinary transient reservations at
  >    properties that were actively sending, which never generated a check-in at all.
  >    This one I can't yet explain and want to dig into.
  >
  > 4. Other — 382k (17%).
  >
  > Put another way: of 4.00M reservations at live properties we could only reach 2.67M
  > (67%) at absolute best, and of those reachable we sent to 1.73M — 65%.
  >
  > The honest read is that the ceiling is contact data, and the biggest fixable item is (3).

  ### Suggested follow-ups (not actioned)

  - Investigate the 580k missing check-in records at live, actively-sending properties.
  - Quantify the contact-data gap by PMS / integration — 33% of reservations arriving
    with no email or phone is the structural ceiling on this whole metric.
  - Consider reporting sends against *reachable* reservations going forward.
project: null
source_id: https://mail.google.com/mail/u/0/#inbox/19fce4e9cb549c58
tags:
- morning-gtd
- gmail
time_minutes: 20
title: 'Reply to SJ Sawhney re: Wyndham July reservation totals vs sends'
updated: 2026-08-12 11:46:14.949424
waiting_on: null
waiting_since: null
working_on: false
---

On the Wyndham July update thread SJ asked: "What were the total number of reservations? (ie how many guests were we not even able to send to)?" Sent 1,753,043 / submitted 321,129 (18.3%). Denominator question is ours to answer.
https://mail.google.com/mail/u/0/#inbox/19fce4e9cb549c58