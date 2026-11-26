---
area: null
completed_at: 2026-11-25 15:47:04.057117
contexts: []
created: 2026-11-17 11:15:52.506268
defer_until: null
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

  ## Agent run 2026-11-25T15:09:25+0200

  Follow-up asked: "Summarize"

  This is a summary of the 17 Nov run above. Nothing was re-checked, so ticket states and counts are as of 17 Nov.

  ### Summary
  - **The title is wrong on the PMS.** De Luna is on Ulyses (Septeo), not Protel. Martijn gave three separate examples in the 1-1: De Luna/Ulyses, Opera V5 phone numbers, and a passing remark about Protel.
  - **Martijn's De Luna complaint mostly holds.** Ulyses changes guest ids on save, which breaks sync for about 11% of companions. It was first reported in August, the design-level fix (PMS-10102, https://linear.app/canary-technologies/issue/PMS-10102/ulyses-reg-card-and-id-document-pushes-can-target-different) has sat unassigned since 21 Aug, and EMEA found the remaining cases in November.
  - **One of his claims does not hold.** I found no sign that Gateway is waiting for Ulyses to fix it. Septeo said in June there is no stable id, and Julius engaged with Montse's approach within a day and a half. Three fixes did ship (PMS-9898, PMS-11013, PMS-11291).
  - **The better-supported criticism** is that the problem was handled ticket by ticket and nobody measured outcomes per integration, so the customer and EMEA found the gaps.
  - **Protel is unverified.** The only Ian message I found (4 Nov, https://canarytechnologies.slack.com/archives/C0CEEFLB92L/p1793799131477769) says Protel's async responses need API design work on our side, which is the opposite of "Protel should fix it". Martijn had not forwarded anything.
  - **Opera V5 phones is a real but small gap:** about 3 more usable numbers a day out of roughly 110 reservations. It is a weaker example than De Luna.

  ### Open on De Luna as of 17 Nov
  - EMEA-839 companions not reaching the PMS: In Review, PR #64997 (https://github.com/canary-technologies-corp/canary/pull/64997) waiting on Julius.
  - EMEA-860 booker name overwrites the checked-in guest: To Refine, unassigned (https://linear.app/canary-technologies/issue/EMEA-860/de-luna-ulyses-bookers-name-from-the-reservation-header-still).
  - ONC-28295 Booking.com phones rejected, so the check-in WhatsApp never goes out: blocked on a customer example, no owner, although the logs already point at a likely cause (https://linear.app/canary-technologies/issue/ONC-28295/de-luna-ulyses-guest-phone-numbers-on-bookingcom-reservations-are-in).
  - EMEA-861 children and extra guests cannot be pushed: a real Ulyses limit; the ticket shows Canceled, so where it is tracked is unclear.
  - The customer's Black Friday measurement started 16 Nov and their CEO reviews check-in KPIs.

  ### Feedback to Ian
  Appropriate, framed as ownership and outcome monitoring rather than "the team is oblivious". Four points: no per-integration outcome view after go-live; vendor-limit cases need an owner and a decision (PMS-10102); ONC-28295 is blocked unnecessarily; where normalisation logic lives (Gateway vs Canary) is unresolved. The draft message is in the 17 Nov run above. It has not been sent, and it says "yesterday", so reword before sending.

  ### Still unknown
  - Whether the open tickets moved since 17 Nov (not re-checked in this run).
  - What Martijn meant about Protel, and De Luna's product go-live dates.
  - All counts are quoted from tickets and Slack, none verified against the database.

  ### Correction, 2026-11-25 (EMEA-839 re-checked)
  EMEA-839 is not waiting on anyone. Julius approved PR #64997 on 17 Nov at 09:46 UTC, it merged and deployed to production the same afternoon, and the ticket has been Deployed since 17 Nov 15:26 UTC. A follow-up, PR #65509 (https://github.com/canary-technologies-corp/canary/pull/65509), is also attached, and Montse posted a video on 18 Nov of the prune working on the Ulyses sandbox hotel in EU prod (https://tv.canary-engineering.com/watch/38da0441-7697-4799-b535-1ef9b45143d4). The "In Review, waiting on Julius" line above was already out of date a few hours after the 17 Nov run.

  ## Agent run 2026-11-25T15:20:15+0200

  Follow-up asked: "review other sources to update picture"

  Sources re-read: Linear (the tickets below, the DeLuna Activation Support project, all Ulyses tickets updated since 10 Nov), GitHub PRs, Slack (#deluna-hotels, #epd-pms-gateway, #epd-emea-engineers, Martijn's DMs), Granola (EMEA block 19 Nov, EMEA standup 23 Nov; summaries only, transcripts not read).

  ### Headline
  - Three of the four De Luna items that were open on 17 Nov are now fixed and live. The fourth (children and extra guests) still has no ticket and no owner.
  - The Gateway team did two of the fixes themselves in the last week, so the draft message to Ian from 17 Nov is out of date. One of its three points is now wrong and should be dropped.
  - Two points still hold: PMS-10102 is untouched since 21 Aug, and nobody has posted any outcome numbers for De Luna.
  - New customer reports keep arriving: one new Ulyses data ticket (23 Nov, in Triage) and several messaging and voice asks.

  ### What changed since 17 Nov
  - **EMEA-839 dead companion cards: fixed.** PR #64997 and follow-up PR #65509 (https://github.com/canary-technologies-corp/canary/pull/65509) merged 17 Nov. Montse then ran a one-time cleanup on 19 Nov that removed 446 cards across 260 upcoming check-ins, 357 of them at Gran Hotel Luna de Granada (https://canarytechnologies.slack.com/archives/C0AB9E7AE59/p1795092610311319).
  - **EMEA-860 booker name on the main guest: fixed.** PR #65731 (https://github.com/canary-technologies-corp/canary/pull/65731) merged 23 Nov. The flag `check-in-primary-guest-name-from-id` is on for the seven De Luna hotels on Ulyses. Montse could not test it in prod and asked Aksel whether Laura should retest.
  - **ONC-28295 phones not syncing: fixed by Gateway, ticket still shows Blocked and unassigned.** Juan Balian found the cause under PMS-11951 (https://linear.app/canary-technologies/issue/PMS-11951/apartamentos-luna-suites-granada-deluna-eu-mcqd-phone-numbers-not): reception types the phone on the reservation holder and our load only read the guest record. PR #66161 (https://github.com/canary-technologies-corp/canary/pull/66161) has been live in the EU since 24 Nov 21:32 UTC, and a re-fetch on 25 Nov updated 648 reservations at Gran Hotel Luna de Granada. One case is still open: the holder phone is not used when the guest name differs from the holder name.
  - **The Workup hypothesis I quoted on 17 Nov was wrong for these cases.** The "151 rejected phones a week, no country fallback" cause did not explain the PMS-11951 examples; both phones had a "+" prefix.
  - **Ulyses masked contact data: closed out by Gateway.** Septeo exempts Canary from masking. Khush verified no account gets masked data (PMS-11987) and removed the guard (PMS-11988, PR #66351). PMS-11292/11293/11294 were cancelled as no longer needed.
  - **Opera V5 phones:** PR #64463 merged 16 Nov. Per the 23 Nov standup summary, Martijn is still working on making the IC Berlin mobile number primary.

  ### Still open
  - **PMS-10102** (https://linear.app/canary-technologies/issue/PMS-10102/ulyses-reg-card-and-id-document-pushes-can-target-different): In Progress, unassigned, no comment and no update since 21 Aug.
  - **Children and extra guests cannot reach Ulyses:** EMEA-861 is still Canceled with no comments, and I found no replacement ticket. This was the largest share of the failures Montse measured (760 hand-added companions in 90 days, 96% children).
  - **AD-11064** (https://linear.app/canary-technologies/issue/AD-11064/guest-check-in-data-missing-from-ulyses-pms-across-properties), raised 23 Nov, Triage, unassigned: De Luna reports missing fields in the PMS at Boutique Granada Centro and Almagra. Workup points at a config rollout that never reached Almagra (document issue date hidden there) plus a code gap (state/province is never sent for companions).
  - **PMS-11590** Hotel Terrassa Confort reg card not pushed to Ulyses: in Triage since 3 Nov.
  - **PMS-12084** (https://linear.app/canary-technologies/issue/PMS-12084): Septeo turns on an IP allowlist for the Ulyses API on Monday 30 Nov. Khush is collecting our egress IPs to send by Friday 27 Nov (https://canarytechnologies.slack.com/archives/C06MU2WUFSP/p1795604177813679). If that slips, every Ulyses call is blocked.
  - **Non-PMS asks in #deluna-hotels on 25 Nov:** EMEA-913 Booking.com auto-messages cut the guest's message out of the AI's context (https://linear.app/canary-technologies/issue/EMEA-913/bookingcom-auto-messages-cut-the-guests-message-out-of-the-ais-context), Black Friday promo prices not reflected in Canary, and Martijn asking voice for supervised transfers because calls hang up after two minutes.
  - **No outcome numbers.** The customer's Black Friday measurement started 16 Nov. I found no check-in completion or push-failure figures posted since the fixes went live.

  ### Wider context
  - EMEA block review, 19 Nov (https://notes.granola.ai/d/4cd22fbe-5e84-4604-94ff-98e4525740af): De Luna is listed as 6 properties, $45.2K ARR, CEO escalated directly, with EMEA now handling its tickets. The same meeting set a posture shift: raise the bar for GMS and PMS-depth work and favour the comms suite. The summary puts PMS connectivity at about 35% of R&D effort.
  - EMEA standup, 23 Nov (https://notes.granola.ai/d/8f0621aa-8627-4102-bfdb-e1f4e617ad67): the summary says Martijn found Booking.com customers not receiving messages at IC properties on Holidex, apparently undetected for about a year. That is a second example of the "nobody watches outcomes" problem, outside Ulyses. I have not checked it against the transcript.
  - Martijn has still not forwarded anything on Protel. His DMs since 17 Nov are about Workbench and the comms-product audit. On 23 Nov he wrote that he does not want EMEA to stand in the way of other teams taking ownership, and that he and James are focusing on the vision change.

  ### What this does to the feedback to Ian
  - **Drop the ONC-28295 point.** Gateway picked it up and fixed it within five days of PMS-11951 being raised, and my stated cause was wrong.
  - **Soften "Gateway does not act".** In the last week Gateway shipped the phone fix, closed out masking, and is handling the IP allowlist ahead of the deadline.
  - **Keep two points.** PMS-10102 has had no owner for three months. Nobody measures outcomes per integration, and the Holidex Booking.com finding is a second case if it holds up.
  - **Add one question.** Who decides what happens for children and extra guests on Ulyses, now that EMEA-861 is cancelled with nothing in its place?
  - Given the 19 Nov posture shift and Martijn's 23 Nov message, the feedback may now fit better as input to the "who owns PMS depth" discussion than as a note about De Luna. That is my reading, not something anyone said.

  Revised draft (not sent):
  > Ian, I went through the De Luna (Ulyses) tickets after talking to Martijn. Most of it is now fixed, including Juan's holder-phone fix this week, thanks for that. Two things are left that I think need an owner. PMS-10102 (reg-card and ID pushes landing on different guest rows) has been unassigned since 21 Aug. And children or extra guests added at check-in still cannot reach Ulyses; EMEA-861 was cancelled and nothing replaced it. Separately, we only found these because the customer and EMEA went looking. Is there a place for a per-integration outcome view (push failure rate, share of reservations with a usable phone) in the rapid-integration work?

  ### Not done / caveats
  - Granola figures and claims come from the summaries, not the transcripts.
  - Did not read the Septeo email Khush forwarded to Martijn on 16 Nov, or the June email thread.
  - Did not verify any counts against the database or Groundcover.
  - Did not check whether the IP list was actually sent to Septeo.
  - Nothing was posted, sent or changed anywhere.
project: null
source_id: null
tags: []
time_minutes: 5
title: deluna protel depending on PMS-side changes, customer functions broken
updated: 2026-11-25 15:47:04.057098
waiting_on: null
waiting_since: null
working_on: false
---

notes: Martijn 1-1 17th granola
get up to speed on general picture, adn feedback to Ian if appropriate