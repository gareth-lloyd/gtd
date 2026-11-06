---
area: null
completed_at: 2026-11-05 17:46:58.961563
contexts: []
created: 2026-11-04 21:27:38.105302
defer_until: null
due: null
energy: low
id: 2026-11-04T2127-how-often-is-last-name-look-up-used-legitimately-i
order: null
output: |
  ## Agent run 2026-11-05T16:30+02:00

  **Short answer:** last name + stay dates is a minority sign-in path but not a fringe one: on a clean day it produces about 950-1,000 successful guest sign-ins across ~300 hotels, which is ~6% of all successful guest reservation lookups and ~15% of web (non-SDK) ones. Confirmation-number lookups do ~14,000 successes/day across ~3,300 hotels. First+last+dates (the stricter mode Nico agreed with Capella) is effectively unused today (1 request on Nov 4, a 422), because it sits behind the HAS_TABLET_QR_ENHANCED_SEARCH flag.

  **Caveat on the source:** I could not find a Granola transcript with "Z" on Nov 3 or 4. The only Nov 3/4 mention of Z is in the Martijn 1-1 (https://notes.granola.ai/d/516aa837-6953-43f6-a8d7-5a37e6c6412e), about the Kiosk Workbench shadow IT, not last name lookup. Bear has nothing on this topic or on Z. The security context below is reconstructed from Slack, Linear and Groundcover; if the Z conversation is in another meeting, tell me the title and I will fold it in.

  ### The security problem(s)

  1. **Capella / Patina Osaka (Compendium sign-in).** An internal auditor signed into another guest's booking because both shared a last name and the auditor typed the other guest's dates. Capella suspended F&B ordering, their Group IT Director called last name + stay dates "too hackable" on a public site, and on Nov 4 asked us to disable it. Thread (40 replies): https://canarytechnologies.slack.com/archives/C094CRQHZD5/p1792557557900819. Outcome on the Nov 4 call: Capella's IT Director (Gary) accepted Nico's proposal of First Name + Last Name + Stay Dates; nothing needed for IPTV/QR. Ishwar cc'd.
  2. **Active enumeration against the same endpoint on Nov 4.** See numbers below. This is the part I think needs attention.

  ### Groundcover numbers (prod, endpoint GET /guest_api/reservations/<hotel_slug>, url_name guest_guest_reservations_api, request_finished events)

  Clean days:

  | Day (UTC) | Name+dates 200 | Name+dates 404 | Name+dates 409 (multi-match) | Confirmation 200 (SDK / web) | Confirmation 404 |
  |---|---|---|---|---|---|
  | Nov 2 | 996 | 730 | 97 | 14,118 (8,533 / 5,585) | 1,379 |
  | Nov 3 | 952 | 935 | 106 | 14,125 (8,677 / 5,448) | 1,649 |

  - Name+dates traffic is 100% web (client_source empty); the Wyndham/IHG SDK only uses confirmation numbers.
  - Nov 3 breadth: name+dates successes came from 306 hotels / 677 IPs; confirmation successes from 3,339 hotels / 5,684 IPs.
  - Name+dates success rate is ~50% (vs ~90% for confirmation number), i.e. guests mistype dates a lot, which is also the Capella failure mode.

  Nov 4 (attack day), name+dates only: 429 x 18,308, 404 x 5,625, 200 x 1,116, 409 x 106.

  - Phase 1, single IP 45.12.62.224, UA "Mozilla/5.0": ~300 last names x several arrival dates against bavarian-inn-lodge (8,407 x 429), flying-flags-rv-resort-campground64 (8,401), daytona-grande-oceanfront-resort (1,500). The SEC-881 per-IP limiter (300/hr) held.
  - Phase 2, same operator, UA curl/8.22.0, 08:20-10:48 UTC, through ~2,960 rotating IPs (about one request per IP): 3,153 requests at Bavarian Inn, 1,810 at Flying Flags. The per-IP limiter is irrelevant here. Result: 150 successful reservation reads at Bavarian Inn Lodge (148 distinct IPs, arrival dates Oct 10-19; the hotel's baseline is 3/day) and 15 at Flying Flags. The 45-day post-departure window (RESERVATION_ACCESSIBLE_AFTER_DEPATURE_DAYS) is what makes past-date enumeration pay.
  - Only trace of it in our systems: WAF S4 alert on 45.12.62.224 in #eng-alerts-groundcover-security at 11:31 EET, auto-resolved, no human reply: https://canarytechnologies.slack.com/archives/C0AQ970QDTP/p1793784674478639. No Linear SEC ticket for Nov 4. The security monitors ("Reservation lookup probing from one IP", "limiter blocked an IP", Greg Wilson closing them) are per-IP, and SEC-1515 from Nov 3 is still in Triage: https://linear.app/canary-technologies/issue/SEC-1515.
  - Nov 5 to 14:00 UTC: no 429s, 377 ok / 394 not found. Attack has stopped for now.

  Relevant code/PRs: per-IP limiter on this view is SEC-881 #59670 (Alina, Oct 8); SEC-763 #56463 closed the ?source=kiosk bypass; SEC-818 #60422 added failure-based blocking and probe events but only for the reservation_external_api slug route, not this name+dates route.

  ### What this implies

  - Killing last name + stay dates globally would break ~1,000 sign-ins/day at ~300 hotels (15% of web sign-ins). Per-hotel opt-out (Capella style) or forcing first name via the existing flag is cheap; a global switch is not.
  - Per-IP rate limiting does not stop the distributed version. Candidates: per-hotel failure velocity, per-(hotel, last_name) velocity, shrink the 45-day window for name+dates lookups, or require first name everywhere.
  - Nothing was posted anywhere. Suggest flagging the Nov 4 distributed run to Greg Wilson / Alina Glumova (security) so it gets a SEC ticket; I can draft that message if you want.
  ## Agent run 2026-11-05T17:05+02:00 (follow-up: are we aware of the Nov 4 attack?)

  **Verdict: no evidence anyone has noticed it.** Searched Linear (SEC team, all teams, keywords: bavarian, flying flags, enumeration, probing, guest lookup, reservation lookup) and Slack (#eng-security, #eng-alerts-security, #epd-alerts-security, #eng-alerts-groundcover-security, hotel names, the attacker IP, attack/scraping/brute-force keywords, Greg Wilson's and Alina Glumova's messages since Nov 3). Nothing human references it.

  What the systems did:

  - The Security team's "Reservation lookup" monitors (probing from one IP / failures across multiple IPs / limiter blocked an IP / limiter unavailable, per region) stayed Normal all day on Nov 4 in us-west-2. The multi-IP one is designed for exactly this ("one hotel, 100+ failed lookups from 5+ IPs in 30 min", SEC-1616 https://linear.app/canary-technologies/issue/SEC-1616), but it and the SEC-818 probe events only instrument the slug-based route in reservation_external_view.py. The name+dates route (guest_guest_reservations_api) emits no probe events, so Bavarian Inn's 2,967 failures from 2,798 IPs were invisible to it. That is a monitoring gap, not a tuning problem.
  - The only alert was the generic WAF "Hotel IP approaching default rate limit" for 45.12.62.224 at 11:31 EET (https://canarytechnologies.slack.com/archives/C0AQ970QDTP/p1793784674478639), auto-resolved 14 minutes later, no reply. The channel is otherwise 50+ unanswered renotifications of an unrelated WAF alert, so a real signal there would be easy to miss.
  - No Linear ticket was auto-created for Nov 4 (the Groundcover-to-Linear integration created the Nov 1 and Nov 3 batches of per-IP tickets, which Greg Wilson closed; SEC-1515/SEC-1583/SEC-1616 from Nov 3 are still in Triage with only the bot "alert resolved" comment).
  - Timeline for reference: single-IP phase 09:18 to 10:13 UTC (18,308 x 429 from the per-IP limiter), rotating-IP curl phase 08:20 to 10:48 UTC (bypassed the limiter, ~165 reservations read).

  Also resolved: "Z" is Z Lee (Director of Engineering, Platform, zlee@). Your 1-1 with Z was Nov 4 around 21:00 EET (DM at 20:51 moving it 15 min), and this item was created at 21:27, so that is the conversation. Granola has no recording of it beyond a 239-character fragment titled "New note" (https://notes.granola.ai/d/73ec2207-4ea7-4dec-8713-2faa202ae5a1).

  Related but separate: STAY-5782 "Compendium lookup logs the guest last name in plain text" (Nov 2, Canceled, Ishwar) is the same route; the request logs I queried do carry query.last_name in clear.

  Still nothing posted anywhere. Suggested next step is a message to Greg Wilson and Alina Glumova (or Z, as platform owner of the monitors) with the Nov 4 numbers and the route gap; happy to draft it.
  Notion write-up (private draft, created 2026-11-05 on request): https://app.notion.com/p/40f8146861518139b3f6d6259563a878
project: null
source_id: null
tags: []
time_minutes: 5
title: How often is last name look up used legitimately in the context of the security
  problems
updated: 2026-11-05 17:46:58.961552
waiting_on: null
waiting_since: null
working_on: false
---

See transcript with Z granola yesterday

groundcover high level numbers