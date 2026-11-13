---
area: null
completed_at: null
contexts:
- consume
created: 2026-11-13 09:54:28.765473
defer_until: null
due: null
energy: medium
id: 2026-11-13T0954-reply-on-sec-1688-review-alina-s-reservation-looku
order: null
output: |
  ## Agent run 2026-11-13T10:07:57

  Nothing was posted. Below: what the doc says, what I checked, and a draft reply for you to send.

  ### Where things stand

  - Doc: "Reservation lookup: caller trust and enumeration controls" (https://app.notion.com/p/4158146861518134b381cd57d561701d). Status is still Draft, every reviewer row says "name TBD", and it has no comments yet. Enterprise is a required reviewer (API gateway identity token).
  - SEC-1688 (https://linear.app/canary-technologies/issue/SEC-1688) moved to In Review on 2026-11-12 with one comment from Alina, the doc link.
  - The doc does not design the per-hotel failure budget. It lists SEC-1688 as one of three undecided options for confirmation guessing and puts that risk under "Left open". SEC-1762 (https://linear.app/canary-technologies/issue/SEC-1762) still names SEC-1688 as the durable fix.

  ### What the doc proposes

  1. Django decides the caller once, from a same-hotel device cookie or a verified identity token. The `X-Canary-Source` header and `IDENTITY_TOKEN_MODE` stop counting.
  2. A verified app without a paired device must send a confirmation number.
  3. Partner fields (door codes, wallet tokens, key contacts, nationality) go only to verified apps; otherwise they stay in the response as null.
  4. One decision record per lookup, with a keyed-hash reservation reference.
  5. The per-IP limiter uses the address the gateway saw. On `/v1` it currently counts the gateway pod for about 72% of lookups.
  6. The Cloudflare rule covers `/v1` and drops the `?source=kiosk` exemption.

  ### Checked against the code at the doc's commit (797f79b)

  - Confirmed: both the lookup and the by-uuid GET choose partner fields with `resolve_client(request).app`, which reads the raw header in every mode (`backend/canary/guest/views/guest_reservations_view.py` L398 and L711, `backend/canary/canary/client_source.py` L54-62).
  - Confirmed: `edge_application_sid` accepts the header below enforce (`backend/canary/api_gateway/services/api_identity_token.py` L306-326). The lookup's trust check already uses it, so in production (enforce, per the doc) the lookup rule already ignores a forged header. The live production gap is the partner-field decision.
  - Confirmed: a paired device skips the per-IP limiter entirely and keeps surname-plus-dates search.
  - Not checked: the Istio, Cloudflare and Groundcover claims (other repos and logs), and whether apps are scoped to hotels anywhere.

  ### Review points, most important first

  1. The by-uuid GET has to be in scope. The doc makes it a non-goal, but it makes the same header decision and the lookup returns the uuid. If a gateway stops stripping the header, an attacker does a five-field lookup, gets redacted fields plus the uuid, then calls the by-uuid GET with a forged header and gets the door codes. The "forged header: Closed" row and the goal "whatever the edge config says" are not met until both sites change. It is the same one-line change in the same file.
  2. SEC-1688 is not answered. The ticket's original shape is also out of date: anonymous callers now send all five fields, so there is no name-and-dates step-up left for them. A budget still fits in two places:
     - Paired devices: surname plus dates, no per-IP limit. A stolen kiosk cookie is an unmetered SEC-1762 search at that hotel. The doc counts 306 such lookups a day across the fleet, so a per-device budget is cheap.
     - App confirmation guessing: Alina's objection (failures under-count when guesses hit) is fair. Her own "exposure breadth" alert counts the right thing, distinct reservations per hotel per app per 30 minutes. It could be the enforcement counter, with a step-up to name and dates rather than a block. Whether the SDKs and partner servers have name and dates to send is unverified.
  3. "`IDENTITY_TOKEN_MODE` plays no part" hides a dependency. `verified_request_claims` returns None when verification keys are not configured, so in any such environment every app turns anonymous: null mobile keys and five fields required. R0 covers production only. Also unstated: the token must be an `api_identity` token carrying `app_sid`; a verified token without one resolves to no application.
  4. Alert thresholds of three times a hotel's p99 do not work for a hotel with three lookups a day. They need an absolute floor. The 4 Nov actor (about one request per IP across 2,960 IPs, 1,200 failures an hour at one hotel) should be the named test case.
  5. Small: the summary says confirmation guessing "is how SEC-1762 beat the per-IP limit". SEC-1762 was surname plus dates; IP rotation beat the limit. The doc also uses a 14-day p99 in one place and a 7-day p99 in another.

  ### Draft reply for SEC-1688 (not posted)

  Thanks Alina, I read it this morning. The caller-trust half is right: decide who is calling once from verified facts, and stop the partner-field decision reading the raw header. Four things before it goes to wider review.

  1. The by-uuid GET needs to be in scope. It makes the same `resolve_client(request).app` decision (`guest_reservations_view.py` L398) and the lookup hands back the uuid. If a gateway stops stripping the header, a five-field lookup followed by a by-uuid GET with a forged header returns the door codes. I don't think the forged-header row is "Closed" until both sites change, and it is the same one-line change.

  2. This ticket's question is still open, so I'd hold it out of In Review. The original shape is out of date, since anonymous callers now send all five fields. I see two places a budget still applies. Paired devices keep surname plus dates and skip the per-IP limiter, so a stolen kiosk cookie is an unmetered search at that hotel; at about 306 lookups a day a per-device budget is cheap. For app confirmation guessing, you're right that failures under-count. Your exposure-breadth alert counts the right thing (distinct reservations per hotel per app per 30 minutes). Could that be the enforcement counter, stepping up to name and dates rather than blocking? We'd need to confirm the SDKs and partner servers can send them.

  3. "`IDENTITY_TOKEN_MODE` plays no part" needs its dependency written down. `verified_request_claims` returns None when verification keys aren't configured, so in any environment without them every app becomes anonymous. R0 covers production; staging, live branches and local SDK development need listing too. Worth stating as well that the token must be `api_identity` with an `app_sid`.

  4. Three times p99 won't work as a threshold for a hotel with three lookups a day; it needs an absolute floor. I'd name the 4 Nov actor (about one request per IP across 2,960 IPs, 1,200 failures an hour at one hotel) as the case the per-hotel 404 alert must fire on.

  One small fix: the summary says confirmation guessing is how SEC-1762 beat the per-IP limit. It was surname plus dates.

  ### Decisions for you

  - Send the reply on Linear, or put points 1 to 4 as comments on the Notion doc (the doc asks reviewers to comment there), or both. I have posted neither.
  - Whether to name yourself or someone else in the Enterprise reviewer row.
project: null
source_id: https://linear.app/canary-technologies/issue/SEC-1688/design-per-hotel-failure-budget-on-name-and-dates-lookups-that-steps#comment-0200a7f8
tags:
- morning-gtd
- linear
time_minutes: 30
title: 'Reply on SEC-1688: review Alina''s reservation-lookup design doc'
updated: 2026-11-13 10:07:57.355033
waiting_on: null
waiting_since: null
working_on: false
---

Alina posted the design doc on the ticket I filed (now In Review): "Reservation lookup caller trust and enumeration controls".
https://app.notion.com/p/canarytechnologies/Reservation-lookup-caller-trust-and-enumeration-controls-4158146861518134b381cd57d561701d
https://linear.app/canary-technologies/issue/SEC-1688/design-per-hotel-failure-budget-on-name-and-dates-lookups-that-steps