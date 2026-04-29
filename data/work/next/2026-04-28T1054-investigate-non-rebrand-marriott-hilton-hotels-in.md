---
area: null
contexts:
- computer
created: 2026-04-28 10:54:36.125291
defer_until: null
due: null
energy: medium
id: 2026-04-28T1054-investigate-non-rebrand-marriott-hilton-hotels-in
order: null
project: 2026-04-16T1351-ship
source_id: https://canarytechnologies.slack.com/archives/C08P0M47GPQ/p1776987315383679
tags:
- morning-gtd
- slack
time_minutes: 30
title: Investigate non-rebrand Marriott/Hilton hotels in BW portfolio
updated: 2026-04-28 11:07:15.945421
waiting_on: null
waiting_since: null
---

Melissa Fairchild flagged a Marriott (hotel/1828) and a Hilton (hotel/129261806) sitting in the Best Western portfolio with no scripting history — appeared because property asked who Jason Pitard was. Figure out how they got there and clean up.

Deep-dive findings — already in flight, not net-new work for me:
- Cleanup is done: Connor removed both hotels from the BW portfolio on 2026-04-25 (per Slack thread). Melissa thanked him 2026-04-27.
- Investigation ticket exists: ENT-6015 "Investigate how non-BW hotels entered portfolio" — assigned to Connor, status=Backlog, priority=Low. https://linear.app/canary-technologies/issue/ENT-6015/investigate-how-non-bw-hotels-entered-portfolio
- This task is now a watch-only: optionally support Connor's investigation (e.g. PortfolioHotel history for hotel_ids 1828 / 129261806) when he picks it up. Otherwise can be moved to someday/trash since the immediate cleanup is done and ownership is clear.

Links:
- Slack: https://canarytechnologies.slack.com/archives/C08P0M47GPQ/p1776987315383679?thread_ts=1776987315.383679&cid=C08P0M47GPQ
- Hotel 1828 (Marriott): https://www.canarytechnologies.com/canary-admin/hotels/hotel/1828/change/
- Hotel 129261806 (Hilton Garden Inn — Salt Lake City Airport): https://www.canarytechnologies.com/canary-admin/hotels/hotel/129261806/change/
- ENT-6015: https://linear.app/canary-technologies/issue/ENT-6015/investigate-how-non-bw-hotels-entered-portfolio