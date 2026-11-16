---
area: null
completed_at: null
contexts:
- react
created: 2026-11-16 10:10:20.261883
defer_until: null
due: null
energy: medium
id: 2026-11-16T1010-reply-to-peter-gao-re-upsell-categories-apac-177-w
order: null
output: |
  ## Agent run 2026-11-16T14:35

  Nothing was sent. The draft reply to Peter is at the bottom, for you to edit and send.

  ### Position
  Back single-item-with-options (Nico's proposal) as the direction, on the condition that it gets a named owner and a block to land in. APAC should offer to build it against an In-Stay PRD. If In-Stay cannot commit to that, shipping the already-built categories as a time-boxed trial becomes the reasonable ask.

  Peter's planned next step, aligning with Nico on timeline and then asking to ship behind a flag, does not fit the disagreement. Nico turned down the flag and A/B idea on 11 Nov and objects to categories existing at all.

  ### Why options beats categories for the stated problem
  - Belinda's data: APAC lists are longer, and the top half of a list takes about two thirds of sales in every region. Position and length are what cost money. Categories add headers without removing items, so the list gets longer.
  - The lists are long because of variations, not variety: early check-in at 10am vs 12pm, 60 vs 90 minute massages, half-day vs full-day excursions. Each is one decision for the guest.
  - Nico's example is Elite Suites Patong going from 214 items to 13. A 13-item list hardly needs categories.
  - Categories carry unresolved costs raised in the #epd-in-stay thread and by Nico: they break the upsell agent's 1-1 ordering (Luciano), may show empty sections (Luciano), overlap with Compendium sections (Joanne), and leave out Room Upgrades, Extend Your Stay and the other upsell surfaces.

  ### Where Nico's case is weaker than he presents it
  - Options is an idea, not a plan. It has no ticket, PRD or owner, and it is a bigger build than categories: pricing, PMS posting codes per variation, the upsell agent.
  - In-Stay has form here. Categories had a PRD and prototype in Dec 2025, then no bandwidth, then cancellation. APAC customers have asked for a year, and "we'll do something better" could end the same way.
  - Customers asked for categories by name. The Luxe Nomad wants rooms separated from ski rentals, which is about organisation rather than length. Options does not obviously answer that, though it may matter less once lists are short.
  - "Stuck maintaining it forever" is about expectations more than code. The schema change is one table and a nullable foreign key. The real cost is taking it away from hotels that have configured it, which a declared trial only partly covers.

  ### Why the A/B is only a fallback
  - It has been asked for and refused once already (Peter 11 Nov 11:12 EET, Nico 11 Nov 15:54 EET).
  - A handful of APAC hotels may not produce enough upsell volume to show a difference either way. I have seen no numbers to judge that.
  - If it does run, the terms should be agreed with Nico up front: which hotels, how long, what result counts, and the removal date.

  ### History
  The miss is not only the missing PRD. APAC started without going back to Nico after his position had changed.
  - Dec 2025: In-Stay wrote a PRD and prototype for categories (STAY-2192, https://linear.app/canary-technologies/issue/STAY-2192).
  - 6 Apr 2026, Nico on STAY-2192: categories are "definitely something we want to do", no In-Stay bandwidth in Q2, and "If you'd like to explore having the APAC pod pick this up, I'd be happy to collaborate on that!"
  - Aug 2026: Nico told Bonnie there was no timeline and no plan. Oct 2026: STAY-2192 cancelled, In-Stay project paused. Both are from Belinda's summary in #project-upsellcats; I did not verify them.
  - 28 Sep 2026: Belinda created APAC-177. 23 Oct: the triage agent recommended the STAY team.
  - 9 Nov: Peter announced the PRs in #epd-in-stay. Nico: "where is this coming from? Product needs to be at the very least looped in".

  ### Current state
  - APAC-177 (https://linear.app/canary-technologies/issue/APAC-177/upsells-group-upsells-into-categories-on-the-guest-page) is Blocked since 11 Nov.
  - PR #63162 (https://github.com/canary-technologies-corp/canary/pull/63162), the migration, is approved by Luciano and still open. It could be merged by accident and should stay parked.
  - PR #63163 (https://github.com/canary-technologies-corp/canary/pull/63163), the feature (+2455, 56 files), has changes requested by Luciano pending the product discussion.
  - #project-upsellcats (https://canarytechnologies.slack.com/archives/C0CGF8J5SV8) has been silent since Nico's options proposal on 11 Nov 17:39 EET. Nobody has replied to it.
  - Belinda is out 19 to 24 Nov, so Wednesday 18 Nov is the practical deadline for putting something concrete to In-Stay.
  - Demand keeps arriving: Fullerton Sydney, Hard Rock Bali, Mandai Rainforest, Niseko (request comments) and Sugar Marina (APAC-177 comment, 9 Nov).

  ### Draft reply to Peter (not sent)
  Destination: DM with Peter, https://canarytechnologies.slack.com/archives/D0B7ZNDSKQ9

  > Hey Peter, read through all of it. Here's where I've landed:
  >
  > 1. I don't think this is only a missing PRD on our side. In-Stay had a PRD and prototype for categories from last December, and in April Nico offered to collaborate if the APAC pod picked it up. He then cancelled it in October and has since turned against categories altogether. The real miss was not checking back with him before starting.
  >
  > 2. I wouldn't take a timeline question to Nico. He already answered the feature flag / A/B idea on the 11th, and the disagreement is whether categories should exist at all. His last message proposes merging variations into one upsell item (Elite Suites Patong 214 → 13), and nobody has replied to it yet.
  >
  > 3. On the merits I think he's mostly right about the problem. Belinda's numbers say list length and position are what cost sales, and categories don't shorten the list. Collapsing variations does. Where I think he's weak is delivery: it's an idea with no ticket, PRD or owner, and categories went the same way last time.
  >
  > 4. So what I'd put to Nico and Belinda: we back the options approach if it gets an owner and a block, and APAC offers to build it against an In-Stay PRD. If In-Stay can't commit to that, then shipping what you've already built as a time-boxed trial is a fair ask, with hotels, duration and removal date agreed up front.
  >
  > Meanwhile please keep both PRs parked, including the migration even though it's approved. This is a product call between Belinda and Nico/Becca and I'd rather you weren't in the middle of it. Belinda is out from the 19th, so it needs to get to them before Wednesday. Happy to join a call if that helps.
  >
  > I know that's not what you want to hear after building the whole thing. The work isn't wasted either way: it's the fallback, and it's what got this decision moving after a year.

  ### Before you send
  - Point 4 moves the next step onto Belinda. You may want to talk to her first, since she has argued for the trial and this asks her to lead with Nico's proposal.
  - The draft commits APAC time to building options. Check that against Block 2 capacity (KakaoTalk, StayPlease, the upsell facelift) before offering it.
  - The upsell facelift Peter raised for Block 2 could be the vehicle for options, with the PRD and In-Stay sign-off agreed at the 10 Nov standup (https://notes.granola.ai/d/dfe37f9b-421e-4cfb-89df-99e573c78848).

  ### Sources and limits
  - Read: Peter's DM (https://canarytechnologies.slack.com/archives/D0B7ZNDSKQ9/p1794814151649569), product request #453 (https://app.notion.com/p/594dd7befae34391a89ac55cba529ee3), APAC-177 and STAY-2192 with comments, the #epd-in-stay thread (https://canarytechnologies.slack.com/archives/C08FKQG5MKL/p1794191726879399), all of #project-upsellcats, both PRs' descriptions and reviews, the 10 Nov standup notes.
  - Not read: Nico's screenshot behind the 214 to 13 figure, Belinda's underlying numbers, the cancelled In-Stay PRD (https://app.notion.com/p/31e81468615181e8b908e82a48bf7343), the two Looms, the PR diffs.
project: null
source_id: https://canarytechnologies.slack.com/archives/D0B7ZNDSKQ9/p1794814151649569
tags:
- morning-gtd
- slack
time_minutes: 30
title: 'Reply to Peter Gao re: upsell categories (APAC-177) with no PRD and the In-Stay
  impasse'
updated: 2026-11-16 14:35:36.361795
waiting_on: null
waiting_since: null
working_on: false
---

Peter sent the product request, APAC-177, the #epd-in-stay announcement and #project-upsellcats; APAC wants to ship behind a flag for A/B and own maintenance, pending Nico's timeline. I said I'd read it all and build my own context (1 holding reply, today).
https://canarytechnologies.slack.com/archives/D0B7ZNDSKQ9/p1794814151649569
