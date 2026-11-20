---
area: null
completed_at: null
contexts: []
created: 2026-11-17 11:15:52.506268
defer_until: 2026-11-23 09:00:00
due: null
energy: low
id: 2026-11-17T1115-deluna-protel-depending-on-pms-side-changes-custom
order: null
output: |
  ## Agent run 2026-11-17T13:56:51+0200

  ### Headline
  - De Luna is on **Ulyses** (Septeo), not Protel. In the 1-1 Martijn gave three separate examples: De Luna/Ulyses, Opera V5 phone numbers, and Protel (a passing remark about messages from Ian). The item title merges the first and third.
  - The De Luna/Ulyses complaint is **largely supported**, with one correction: I found no evidence that the Gateway team is waiting for Ulyses to fix the id churn. The vendor was asked in June and said no. The better-supported criticism is that the problem was handled ticket by ticket and nobody measured the outcome until EMEA did in November.
  - The Protel claim is **unverified**. Martijn has not forwarded context yet, and I could not find the messages from Ian he referred to.
  - Feedback to Ian looks appropriate, framed as outcome monitoring and ownership rather than "the team is oblivious". Draft at the bottom; nothing was sent.

  ### What Martijn said (Granola, Martijn 1-1, 17 Nov: https://notes.granola.ai/d/87c0acb6-4ecd-4ec6-8daf-d9360bb5ecf6)
  - The Gateway team does not know what the product needs. Work is bug fixing, with no look after deploy at conversion or how the integration performs.
  - Luna Hotels: the PMS creates new guest records on every save and drops the identifier, which breaks sync. He says this should have been solved months ago, the integration is a year old, and the customer escalated about a month ago.
  - He says the Gateway team's usual answer is that the PMS should fix it (he attributes this view to James too), and that for De Luna that hope is "fantasy".
  - Protel: he called it horrific because it is asynchronous, and said you can see "Protel should fix this" in messages from Ian.
  - You said you would look at the two cases (Luna and Opera V5), asked him to forward anything useful, and said you would give Ian the feedback once you were sure it was accurate. Martijn doubted the feedback would change anything.

  ### De Luna / Ulyses: what the record shows
  Timeline:
  - Nov 2025: Ulyses rollout done, PMS-6049 (https://linear.app/canary-technologies/issue/PMS-6049/rollout-to-ulyses).
  - June 2026: Marta emailed Septeo about guest ids changing. Per Montse's summary on 13 Nov, the answer was that there is no stable id and not to match unless unique. I did not read the email thread itself (integrations-epd Google Group).
  - 7 Aug 2026: De Luna reports ghost guest profiles on all properties, PMS-9898 (https://linear.app/canary-technologies/issue/PMS-9898/bugs-from-ulysses-creating-ghost-guest-profiles). Closed by Julius in 4 days.
  - 12 Aug 2026: root-cause write-up PMS-10102 (https://linear.app/canary-technologies/issue/PMS-10102/ulyses-reg-card-and-id-document-pushes-can-target-different): reg-card and ID pushes can land on different guest rows because `is_primary` is recomputed on every load from names our own writes change. Still In Progress, unassigned, no update since 21 Aug. Both fix options need cross-team agreement.
  - 19 Oct 2026: stale-companion pruning turned on (PMS-11013, https://linear.app/canary-technologies/issue/PMS-11013/check-in-asked-for-additional-adult-on-1-guest-reservation). Masked contact data handled in PMS-11291 (Deployed); follow-ups PMS-11292/11293/11294 sit in Backlog.
  - Nov 2026: EMEA (Martijn, Montse) found and are fixing the rest under the DeLuna Activation Support project (https://linear.app/canary-technologies/project/deluna-activation-support-6abce3627d9d/overview).

  Open now:
  - EMEA-839 companions not reaching the PMS (https://linear.app/canary-technologies/issue/EMEA-839/ulyses-companions-filled-in-during-online-check-in-dont-reach-the-pms): 67 failed pushes in 14 days, about 8% of Gateway guests on Ulyses accounts are leftover placeholders. Montse, In Review, PR #64997 (https://github.com/canary-technologies-corp/canary/pull/64997) waiting on Julius.
  - EMEA-860 booker name overwrites the checked-in guest (https://linear.app/canary-technologies/issue/EMEA-860/de-luna-ulyses-bookers-name-from-the-reservation-header-still): To Refine, unassigned. Martijn proposed a feature-flagged overwrite and wants the customer to confirm the flow first. Martijn named it as the next thing to pick up (https://canarytechnologies.slack.com/archives/C0AB9E7AE59/p1794909413912239).
  - ONC-28295 Booking.com phones not syncing, so the check-in WhatsApp never goes out (https://linear.app/canary-technologies/issue/ONC-28295/de-luna-ulyses-guest-phone-numbers-on-bookingcom-reservations-are-in): 191 of about 500 Booking.com arrivals completed check-in at Gran Hotel Luna de Granada. Blocked since 11 Nov waiting on an example reservation from Aksel. Workup already has a medium-confidence cause (no country fallback, so numbers without "+" are rejected; 151 rejections in 7 days). Nobody owns it.
  - EMEA-861 children and extra guests cannot be pushed (https://linear.app/canary-technologies/issue/EMEA-861/ulyses-children-and-extra-guests-added-in-online-check-in-cant-reach): 760 in 90 days, 96% children. This one is a real Ulyses limit (no create-guest call). The ticket shows Canceled since 12 Nov although Montse still cites it on 13 Nov as the tracker and planned to email Septeo. Worth checking where that is tracked now. EMEA-837 covers the misleading error message (Backlog).
  - Customer recap of the 11 Nov call (https://canarytechnologies.slack.com/archives/C098KBW5KU2/p1794484466970509): Black Friday measurement started 16 Nov and the CEO reviews check-in KPIs for the Alianza Hotelera assembly.

  ### Checking Martijn's claims
  - "Creates new records on every save, breaks sync": supported. Montse measured about 11% of Ulyses companions affected in 90 days (https://canarytechnologies.slack.com/archives/C023K54M812/p1794436976453089).
  - "Unsolved for months": supported in substance. First reported in August, the design-level fix (PMS-10102) stalled, and the remaining cases were found by EMEA in November. Not accurate to say nothing was done: PMS-9898, PMS-11013 and PMS-11291 all shipped.
  - "Gateway says the PMS should fix it": not supported for De Luna in what I read. In the 12-13 Nov thread Julius gave vendor contacts and agreed Montse's approach within about a day and a half of her first post. The friction I did find is about where logic lives, for example Julius on 13 Nov saying Gateway must represent PMS data faithfully (https://canarytechnologies.slack.com/archives/C023K54M812/p1794587868510569).
  - "Live a year / half a year": the integration rollout was Nov 2025. I did not check De Luna's product go-live dates.
  - Protel: the only recent Ian message I found is his 4 Nov note that Protel's async responses will need API design work (https://canarytechnologies.slack.com/archives/C0CEEFLB92L/p1793799131477769). That reads as the opposite of "Protel should fix it". Martijn may mean older messages, possibly in #grecotel, which I did not search.

  ### Opera V5 phone numbers (the other case)
  - Thread: https://canarytechnologies.slack.com/archives/C023K54M812/p1794395509979379. Martijn raised three tickets after an IC Berlin call on 10 Nov. Khush said the team could not pick them up before the new year. Martijn opened PR #64463 himself (https://github.com/canary-technologies-corp/canary/pull/64463).
  - Lei confirmed the gap: Gateway took the primary guest's phone from FetchBooking on the assumption it was complete, and it is not.
  - Measured gain so far is small: about 3 more usable numbers a day out of roughly 110 reservations, maybe 10 with mobile-over-landline preference; at least 20% have no mobile in the PMS at all (https://canarytechnologies.slack.com/archives/C09JC8M0XAM/p1794904023907949). So it is a real gap but a weaker example of a "core oversight" than De Luna.

  ### Suggested feedback to Ian (draft only, not sent)
  Points that hold up:
  1. Nobody watches integration outcomes per account after go-live (push failure rate, share of reservations with a usable phone, check-in completion). The De Luna gaps were found by the customer and then by EMEA querying the data. A per-integration health view would have shown them months earlier.
  2. Vendor-limit cases need an owner and a decision. Ulyses told us in June there is no stable guest id, yet PMS-10102 has sat unassigned since August.
  3. ONC-28295 is blocked on a customer example while the logs already point at a likely cause.
  4. Where normalisation logic lives (Gateway vs Canary) is unresolved and is the source of most of the friction, and it gets sharper with Guest Foundation Service.

  Draft message:
  > Ian, Martijn and I talked about De Luna (Ulyses) yesterday and I went through the tickets. Two things I think are worth your attention. First, the guest-id churn was reported in August and Septeo told us in June they have no stable id, but PMS-10102 has been unassigned since 21 Aug and the remaining cases (about 11% of companions) were found by EMEA this month. Second, we have no per-integration view of outcomes, so we learn about these from the customer. Could we talk about who owns that for Ulyses, and whether the rapid-integration work is a place to build it in? Also ONC-28295 is blocked on an example while the logs already show 151 rejected phones a week.

  ### Not done / caveats
  - Did not read the June Septeo email thread, EMEA-860 comments, or #deluna-hotels before October.
  - Did not verify any counts against the database; all figures are quoted from tickets and Slack.
  - Martijn has not forwarded context. The only DM from him since the 1-1 is the Workbench migration link.
  - Nothing was posted, sent or changed anywhere.
project: null
source_id: null
tags: []
time_minutes: 5
title: deluna protel depending on PMS-side changes, customer functions broken
updated: 2026-11-19 15:32:30.419586
waiting_on: null
waiting_since: null
working_on: false
---

notes: Martijn 1-1 17th granola
get up to speed on general picture, adn feedback to Ian if appropriate