---
area: null
completed_at: 2026-11-12 10:55:46.340509
contexts:
- react
created: 2026-11-12 08:59:20.749146
defer_until: null
due: null
energy: medium
id: 2026-11-12T0859-close-out-the-slug-structure-question-in-the-sec-1
order: null
output: |
  ## Agent run 2026-11-12T09:12

  Nothing posted. A thread reply is drafted below and needs your go-ahead to send.

  ### State of the thread
  - Gameplan thread (https://canarytechnologies.slack.com/archives/C0CFU7HBZEK/p1794343355996419?thread_ts=1794343355.996419&cid=C0CFU7HBZEK) has 2 replies, both about customer comms (Z, Connor). Nothing from you, which is why the fetcher keeps flagging it.
  - The conclusion is already in the channel, just not in this thread:
    - 10 Nov 21:54 GMT, top level: "hotel slug aliases don't get us anywhere. There's no benefit, not even security by obscurity." (https://canarytechnologies.slack.com/archives/C0CFU7HBZEK/p1794347678227809)
    - 10 Nov 22:40 GMT, in another thread: "Slugs are not secrets." (https://canarytechnologies.slack.com/archives/C0CFU7HBZEK/p1794350436555579?thread_ts=1794345936.636049&cid=C0CFU7HBZEK)
    - 10 Nov 22:07 GMT, top level: SEC-1785 posted as the fix for the enumeration endpoint (https://canarytechnologies.slack.com/archives/C0CFU7HBZEK/p1794348450339859)
  - DM with Connor, 10 Nov 22:04 GMT: "We should not change slugs", "it doesn't gain us anything", "we need to be less shit at exposing them, but even then, they should not be considered secrets." Connor: "cool aligned" (https://canarytechnologies.slack.com/archives/D08BG88NY2K/p1794348288065259)

  ### Ticket status (checked 2026-11-12)
  - SEC-1785 (https://linear.app/canary-technologies/issue/SEC-1785) Detect and slow hotel-slug guessing on check_in_hotel: In Progress, assigned to Gregory Wilson
  - SDM-5339 (https://linear.app/canary-technologies/issue/SDM-5339) Reduce information exposure from the unauthenticated v2 hotel endpoint: Todo, unassigned

  ### Draft reply for the gameplan thread
  Destination: #incident-reservation-lookup-sec-1762, thread_ts 1794343355.996419

  > Closing out item 4: we should not change the slug structure.
  >
  > • It buys us nothing. Old slugs are already out there (urlscan, old guest links, our own marketing site), and we can't retire them without breaking the mobile app integrations, Wyndham wifi and every link we've ever sent. New obscure aliases alongside the old ones add no security at all.
  > • Slugs are not secrets and shouldn't be treated as one. The fix is that a slug alone must never be enough to reach guest data, which is what item 1 (require confirmation number) does.
  > • What we should fix is how easy they are to enumerate. That's SEC-1785 (https://linear.app/canary-technologies/issue/SEC-1785), in progress with Greg, plus SDM-5339 (https://linear.app/canary-technologies/issue/SDM-5339) to cut what the unauthenticated hotel endpoint returns.
  >
  > Connor and I are aligned on this. Calling item 4 done unless anyone disagrees.

  ### Notes
  - The mobile app / Wyndham wifi breakage reasons come from Connor's side of the DM ("so much external coordination and things are gonna break"), not from anything I verified in code.
  - SDM-5339 has no owner. Drop that line from the reply if you would rather not point at an unassigned ticket.
project: null
source_id: https://canarytechnologies.slack.com/archives/C0CFU7HBZEK/p1794343355996419?thread_ts=1794343355.996419&cid=C0CFU7HBZEK
tags:
- morning-gtd
- slack
- resurfaced
time_minutes: 10
title: Close out the slug-structure question in the SEC-1762 gameplan (#incident-reservation-lookup-sec-1762)
updated: 2026-11-12 10:55:46.340500
waiting_on: null
waiting_since: null
working_on: false
---

Resurfaced: archived 2026-11-11 as `2026-11-11T0738-catch-up-on-sec-1762-overnight-and-review-the-lock`, but the fetcher still shows it unanswered.

Connor's gameplan item 4 (lower prio) is mine: "Understand if we should change our slug structure and the impact". I told Connor in DM we should not change slugs; post the conclusion in the channel. Open 1 day, no reply from me in thread.
https://canarytechnologies.slack.com/archives/C0CFU7HBZEK/p1794343355996419?thread_ts=1794343355.996419&cid=C0CFU7HBZEK