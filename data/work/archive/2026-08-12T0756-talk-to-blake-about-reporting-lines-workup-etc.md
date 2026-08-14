---
area: null
completed_at: 2026-08-13 15:21:34.872763
contexts: []
created: 2026-08-12 07:56:11.503481
defer_until: null
due: 2026-08-12
energy: low
id: 2026-08-12T0756-talk-to-blake-about-reporting-lines-workup-etc
order: null
output: |
  ## SENT 2026-08-13 — message went to Blake, and he replied at length

  Gareth sent his own version (not the drafts below) — shorter, more direct, named the
  worry outright: *"I'm worried that you're managing around me rather than through me on
  Workup / MCP. I want to check that I had not shaken your confidence on this piece of
  work."* Plus the Laura-as-vehicle framing, the SJ-supersedes-development-plan
  concession, and *"I want to make sure that you push SJ's agenda for AI through me once
  I'm back."*

  ### Blake's reply — substance

  **Denies working around, specifically and credibly.** *"Definitely not intending to work
  around you or any reflection on your ability to sort of move here."* Also volunteers
  *"Laura has done a really good job."*

  **Names three lanes he's taken, all genuinely VP-only:**
  1. **Cross-team org change** — bringing Nancy along; the CSA team routing issues straight
     to on-call instead of through support (Mattie found it via workup). *"that's the exact
     problem space I want to be in to help do the organizational change across these
     boundaries."*
  2. **Security cut-through** — *"workup has to have the same workbench as a senior engineer
     at Canary, and we must move on that quickly, and I know that I can cut through all of
     the layers and actually make the decisions to force that through in a way that you,
     you just can't do as quickly."* Reason: he's the final decision maker; Bernard or Z
     would escalate to him anyway.
  3. **Budget** — *"I can push and and pull on the budgeting in a way that if I'm attached
     directly, I can move."*

  **Explains the next-step metric doc** — wrote it himself for metric clarity, drawing on
  the voice-agent mess (handle rate vs containment rate) where bad metrics made it hard to
  even discuss AI progress. Acknowledges *"the next step design could be looked at as like
  superseding sort of the development plans."* So the Laura point landed.

  **His lens:** *"how can I get AI to take more of this end to end, specifically focused on
  messaging and comms, core problem spaces."*

  **Macro mandate:** *"I've been tasked with transforming EPD to be more AI native over
  time."* Ingredients he's setting direction on: triage, bug fixing, project building
  (product → design → build).

  ### The two load-bearing lines

  1. *"It didn't even cross my mind that I could be working around you, or that it could be
     perceived as working around you… the fact that Gareth might not be the right person
     here. It totally kind of disconnected from my mind."*
     → Better than deliberate exclusion on intent, worse on salience. Not weighed and set
     aside — simply absent from the model. That is the actual problem to fix.

  2. *"I will think more on should we have you lean in harder and how, **I don't have a
     great idea there**, but I do think we should talk live. So let's make sure we find time
     when you're back to feeling good."*
     → The role question is genuinely open and he has no proposal. If Gareth arrives
     without one, the default is that nothing changes.

  ### NEW INFORMATION — Overlord is under build-vs-buy evaluation

  *"I needed to be way closer to the agent's platform we're actually building to
  understand. Do we need to invest further in the agent platform? This is like overlord and
  all of those pieces. Is this overbuilding and we should have actually just gone out to
  market and bought something? That's why I did like warp demos, etc."*

  Blake is personally evaluating whether Laura's platform should exist. He's gathering the
  answer himself because nobody has given him one. Gareth is arguably better placed than
  Laura to answer it — knows the platform and the cost model, didn't build it, so less
  conflicted. This did not appear in any prior source.

  ### The opening Blake handed over without noticing

  His stated #2 priority — give workup "the same workbench as a senior engineer", moving
  fast "through a space of like opening up" — **is the Canary MCP SQL tool.** The thing
  that makes opening it approvable is the guarded query-watcher design Gareth specced on
  10 Aug (definitive string-based blocking for sensitive queries, LLM layer for ambiguous
  review). Blake is about to spend VP capital forcing through a decision that Gareth's
  existing work is the safety case for. Most concrete reconnection point available.

  ### Status / open thread for when Gareth is back

  - Role question: **OPEN**, deferred to a live conversation.
  - Onus is on Gareth to bring the proposal. Blake explicitly has none.
  - Candidate asks, strongest first: (a) own the Overlord build-vs-buy answer;
    (b) own the guarded-access safety case that unblocks Blake's security push;
    (c) own making Blake's six-week org changes stick after he rotates off.
  - Only pre-vacation action worth taking: get the live conversation into the diary rather
    than leaving it as "when you're back to feeling good."
  - The two letter drafts below were NOT sent and are now historical.

  ---

  ## Agent run 2026-08-13 — Internal Tools block planning call, 11 Aug (Zoom VTT)

  Source: `~/Downloads/GMT20260811-143221_Recording.transcript.vtt`.
  Attendees: Blake, Stephanie Barry, Laura DeWald, Connor Swords, Asher Davidson,
  Kevin Cormier. **Gareth not present.**

  ### Outcome

  Workup is top priority for the block, all hands — but scope narrowed hard. SJ told
  Blake not to go wide; focus is messaging + Comms Core only. Order: next-step metric →
  Canary MCP takeover from Dylan → accuracy push → knowledge base → interactive
  investigations → model benchmark (last, since Sonnet held intro pricing). Blake asked
  to join the team's syncs for the next couple of weeks. User management: Blake rejected
  the trained-support-L2 plan as the #1 breach surface; Stephanie to rethink. IHG
  compendium automation is the other immediate push. SAG types approved as a small lift.
  PMS capabilities explicitly lowest priority / stretch. Cost-to-serve: Stephanie to get
  finance numbers, Blake to push AJ within 3 weeks.

  ### THIS BREAKS THE v2 LETTER'S CENTRAL ASK — do not send as drafted

  1. **The adoption ask is the thing leadership just vetoed.** v2 asks to own "pushing
     pods through Patterns and gatherers." Blake, verbatim: *"the thing that SJ doesn't
     want is us going too wide and getting sort of distracted by all the different things
     of all the different teams, and instead just laser focus on really having an impact
     on communications and, our compcore and messaging."* Org-wide staged rollout is
     deprioritised for the block. As written you'd be bidding for cancelled work.

  2. **The argument underneath it has been superseded.** v2 argues rollout is the lever
     that makes a second domain surface the PMS-shaped assumptions. Ian already did it
     solo from payments: *"he used the investigate tool on some of the triage, and out the
     back of that, realized, like, oh, a lot of this is pretty PMS-specific… he's gonna
     send over a doc."* One staff engineer, no rollout programme. Keep the insight, drop
     the mechanism.

  3. **Blake asked for a standing seat covering exactly the two weeks out:** *"if you try
     and include me on those sync cadences, I think that'd be super helpful for the next
     couple weeks, at least."* Laura: *"Yep. Do that."* The "will he go direct?" question
     is answered — he asked, and it's already agreed.

  ### MCP — the steer landed, the attribution didn't

  Internal Tools is taking Canary MCP over from Dylan/Applied AI. Confirmed on the call.
  Traces directly to the 10 Aug EMEA directors steer. Blake scoped it tight for this
  block — accuracy/triage only: *"I have the engineers take over ownership of this… rather
  than just being full dependent on applied AI. But then it becomes a tool in your tool
  chest."* The guarded-SQL architecture (string-block + LLM review) was **not mentioned in
  the room**; it lives in the Q3B doc unattributed.

  ### Perception read — resolves both ways at once

  - Asher, to Blake, in absentia: *"unfortunately, Gareth is a blocker there"* (eng design
    review cycle, PMS capabilities — the lowest-priority item, so low stakes).
  - Asher, positively: *"That was Gareth's main pushback"* (drift detection platform choice).
  - Stephanie, twice: *"Gareth has been super helpful on the plans to build out types for
    support access grants"* / *"Gareth has helped us out, so we're already partially there."*
  - **Visible fingerprints are on SAG types and PMS capabilities — not on Workup.**
    Workup credit: *"Laura's been doing a bulk of the work, which is amazing."*
    Canary Pages: *"Canary Pages is awesome. Thank you, Laura."*
    Connor's closing praise: *"Laura, Steph, and team."* Gareth unnamed.

  → The team IS getting the glory. Gareth is not in the frame for it. Both halves of the
  subtext confirmed in one call.

  ### Other

  - **User Management pillar sent back to the drawing board.** Blake: it's the *"number one
    breach surface"*, approvers get worn out above ~1/day. Stephanie: *"Let's take a step
    back and reevaluate how we're going to approach this solution."* Redirect is toward AI
    execution + concrete thresholds rather than a trained L2 human.
  - Blake wants Internal Tools *"completely unresponsible for that side of the equation"*
    on team-enablement cost — sampling / managed trigger runs so teams self-serve.
  - Direction of travel: away from Claude Code harness toward OpenRouter, when the harness
    next needs a push.
  - Kevin surfaced profanity collisions in guest-facing alphanumeric IDs; Blake asked
    Stephanie to fix within a couple of months.

  ### Next step (NOT taken — awaiting your call)

  v2 needs its "What I want" section reworked around a scope leadership actually wants.
  The obvious candidate is depth on messaging/Comms Core end-to-end rather than breadth
  across pods, but that's your judgement, not mine.

  ---

  ## Agent run 2026-08-12T15:40 — letter draft v2 (ask now needs rework, see above)

  Pulled the verbatim Aug 3 "Blake Directs" transcript
  (Granola meeting `6c96439f-69b3-48d2-b9e3-5b84c2e7b41b`) to check a claim in the first
  draft. It did not hold up, and two other things in the first draft were wrong. Draft
  rewritten. **Use v2. The 15:05 section is kept only for the evidence and links.**

  ### What the transcript actually says

  1. **Blake is NOT rewriting the investigate skill.** He is planning to.
     Verbatim: *"One thing that I'm actually doing this very second is trying to come up
     with a plan to rewrite this investigate skill"* … *"So I was trying to look at how
     would we rewrite this so that it could be more generalized"* … and he caveats the
     whole thing: *"But that's all early and not backed well. So I'm going to get to the
     bottom of that and pressure test each of those hypothesis."*

  2. **Blake pre-empted the turf concern himself, unprompted.**
     Verbatim: *"I don't think what I'm doing is interfering in any way with what internal
     tools is doing so far."* And his reason for going around them is substantive, not
     dismissive: *"you need to actually apply it somewhere else to see what gaps it has,
     like how would this not work in a messaging context or, you know, insert context here
     tipping."*
     → So the v1 bullet telling him to route the rewrite through Laura was answering a
     question he had already answered, and would have read as territorial.

  3. **You already agreed with him on that call — in the terms you now want.**
     Verbatim (you): *"I definitely agree that we need to push that I've said a couple of
     times in different places that I want to use rollout processes a lever to get to
     these to engage with that and add their own context gathering. So if you could
     unblock that from the core skill that would be awesome."*
     → A letter arguing the opposite two weeks later would contradict you on the record.
     v2 builds on this instead, and it's the strongest card in the letter.

  4. **Token cover was YOUR ask to HIM, not his to you.** (v1 had this backwards, twice.)
     Verbatim (you): *"Would be to just send a very clear message to Laura that she's got
     cover on token costs like she doesn't have to worry that she'll be on the hook…
     something holding her back from wider rollout."*
     Blake: *"Yeah."* … *"There should be economic unblocks as well as security unblocks
     that I think are another reason I want to, I want to step in."*
     → So it is a **follow-up on something he already accepted**, which is a much stronger
     position than asking fresh.

  5. **Blake is committing ~6 weeks of his own time.** Verbatim: *"I want to spend a decent
     amount of my time really in that headspace, including like, you know, pulling metrics
     myself and reading all the code… So I'm really going to try and do that for about six
     weeks. The, the whole block."* Driver is SJ direct to him: *"I really want you to be
     consistently focused on just like the adoption curve at canary… I really want you to
     resist me telling you to do other things."* Plus a *"26 million dollar gap"* and
     Wyndham call centre at *"four of 17"* activated.

  6. **Your vacation is NOT mentioned anywhere in that meeting.** Blake does not know, or
     at least it was not said. Worth deciding whether the letter is the place he finds out.

  7. **Loose end:** Blake had not received Laura's rollout-plan doc as of Aug 3 —
     you: *"I was encouraging her to put together her role out plan in a document for you"* /
     Blake: *"I haven't yet."* Unverified whether it has landed since. Cheap thing to check.

  8. **Blake already had time booked with Laura and Stephanie that same day** to discuss
     *"how to unblock them."* Going direct is established practice, not a vacation risk.

  ### Deliverable v2: draft letter to Blake (382 words)

  Full draft at `scratchpad/blake-letter.md`. Text:

  ---

  Blake — this is what I had queued for our 1:1 before the accident took it out. Rather
  than let it wait another two weeks.

  **What's been happening under the surface**

  Since May I've run Workup deliberately as Laura's vehicle. When it moved to Internal
  Tools I held the line that Julius was a resource, not a replacement — left alone she'd
  have conceded it quietly. Every 1:1 since has been the same push: publish, claim scope,
  stop asking permission. Her May calibration guidance was literally "write the six-month
  memo on what Internal Tools owns end-to-end." The judge dashboard, self-serve prompts,
  the enablement doc, Canary Pages — that's hers. And the cost nerve that had her
  self-braking is mostly gone because I kept telling her the maths was obvious.

  That's most of what I've been doing on this, and none of it shows up in a status update.

  **On you stepping in**

  You said on the 3rd you didn't think it interfered with what Internal Tools is doing.
  Agreed — and you were right about why: nobody finds the PMS-shaped assumptions until a
  second domain actually tries to use the skill. That's the same point I made back to you
  on that call, about using the rollout process as the lever to get teams engaging and
  adding their own gathering. Those are one mechanism, not two. You're generating the gaps
  from the payments end; rollout generates them everywhere else, and it's the half that
  stalls without someone pushing pods through Patterns and gatherers.

  So I'm not asking you to route around anything. I'm asking that when you're six weeks
  into this, the adoption half has an owner, that it's me, and that Internal Tools has its
  name on the result.

  **The two weeks I'm out**

  Go direct to Laura and Stephanie — you already do, and it's fine. Two things so it isn't
  lost time:

  - The Q3B plan is current as of Monday and already sequences the org-wide push, the
    Canary MCP SQL unlock and the accuracy work. Fastest way into the state of things.
  - Token cover for Laura: I raised this with you on the 3rd and you called it an economic
    unblock worth stepping in on. It hasn't reached her. One line in the channel does it.

  Gareth

  ---

  NOT SENT. Nothing posted to Slack, Notion, Linear or GitHub.

  ---

  ## Agent run 2026-08-12T15:05 — SUPERSEDED, see above

  ### Deliverable: draft letter to Blake (387 words) — DO NOT SEND, contains 3 errors

  Full draft also at `scratchpad/blake-letter.md`. Text:

  ---

  Blake — this is the conversation I had queued for our 1:1 before the accident took it
  out. Writing it down rather than letting it sit another two weeks.

  **What's been happening under the surface**

  Since May I've been running Workup deliberately as Laura's vehicle. When it moved to
  Internal Tools I held the line that Julius was a resource and not a replacement,
  because left alone she'd have quietly conceded it. Every 1:1 since has been the same
  push: publish, claim scope, stop asking permission. Her May calibration guidance was
  literally "write the six-month memo on what Internal Tools owns end-to-end." The
  visible output — the judge dashboard, self-serve prompts, the enablement doc, Canary
  Pages — is hers. The cost nerve that had her self-braking at $500/day is mostly gone
  because I kept telling her the maths was obvious.

  That is the part that never shows up in a status update, and it is most of what I've
  been doing.

  **Where that collides with your mandate**

  In a no-pressure world this is the ideal stretch assignment for her. It isn't a
  no-pressure world. SJ wants the adoption curve and the ARR gap, you've been told to
  drive it, and that outranks Laura's development plan. I'm not going to argue
  otherwise — and I don't want you having to route around me to get there.

  **The next two weeks**

  I'm out. Rather than have you rediscover the state of things:

  - Go direct to Laura and Stephanie. But land the investigate-skill rewrite as a
    contribution into their framework, with Laura owning merge and rollout. She'll move
    faster with your code than without it, and she keeps her name on it.
  - The Q3B plan is current as of Monday and already sequences the org-wide push, the
    Canary MCP SQL unlock and the accuracy work. Steer through it rather than around it.
  - On token cost: you asked me to give her explicit cover. It'll land harder from you.
    One line in the channel is enough.

  **What I want**

  A defined role in this when I'm back — specifically the adoption side: getting every
  pod through Patterns, gatherers and go-live. That's the curve SJ is actually asking
  about, it scales badly without someone driving it, and Internal Tools should have its
  name on it when it lands.

  Gareth

  ---

  NOT SENT. Nothing posted to Slack, Notion, Linear or GitHub.

  ### Evidence the letter rests on

  - **Ownership transfer + defending Laura (May 2026).** Investigation agent formally
    moved to Internal Tools/Laura on 11 May; Laura was anxious Julius was replacing her,
    you clarified he was a resource and committed to pushing back if that changed.
    (Granola: Triage agent sync 11 May; Laura 1-1.)
  - **Calibration guidance you wrote for her (5 May 2026).** Speak out across the org,
    storytelling, celebrate wins, share patterns now rather than a polished framework
    later, and "claim bigger scope via a 6-month memo on what Internal Tools will own
    end-to-end." (Bear: "Reviews calibrations".)
  - **Cost coaching.** Laura self-braking at ~$20/run / ~$500/day at 25 tickets. Your
    reframe: cheaper than a full-time contractor. Repeated to Stephanie 9 Jul.
    (Granola: Laura 1-1 9 Jul; Stephanie 1-1 9 Jul.)
  - **Directors-level steer (10 Aug EMEA directors).** Two items handed to Laura +
    Stephanie for block planning: action the handoff-rate metrics from the workup doc,
    and Canary MCP should be owned by Internal Tools. You also identified guarded SQL
    access to the Canary DB as the biggest unlock, with the query-watcher architecture
    (string-based blocking + LLM review for ambiguous queries).
  - **That steer is now in the plan.** Q3B "Canary MCP SQL Tool" — Internal Tools taking
    the MCP server over from Applied AI, guarded SQL as first investment. Lead: Laura.
    https://app.notion.com/p/3b1814686151816cb470da06f103f965
  - **Enterprise scope boundary you pushed (raised with Stephanie 5 Aug).** Generic user
    access requests belong to Internal Tools, not Enterprise. Now the Q3B "User
    Management" pillar — ~78% of the Oncall queue, body-verified across 702 tickets.
    (Bear: "Stephanie Barry 1-1", "Enterprise".)

  ### Blake's mandate — what you're squaring against

  - **SJ:** stay on the adoption curve; activating revenue earns the right to keep
    investing (~$26M ARR gap). In block planning asked "why should I care about this
    team?"
  - **Blake (3 Aug directs):** actively rewriting the investigate skill to generalise it
    off PMS-specific logic toward a generic orchestration layer with a payments angle;
    wants sub-agents used more intelligently, tool calls to humans, investigation bundled
    into Workup as a pipeline flow. Also asked *you* to give Laura explicit token-cost
    cover.
  - **Ian:** investigation quality needs to be "bolder."
  - **20 Jul directs:** Blake asked for Stephanie + Laura to quantify token cost vs
    benefit before org-wide rollout.

  ### Key docs / links

  - Workup enablement doc (updated 11 Aug) —
    https://app.notion.com/p/3b281468615181abab24cc07d8889847
  - Planning — Internal Tools — Q3B (updated 11 Aug) —
    https://app.notion.com/p/3b1814686151816cb470da06f103f965
  - Workup dashboard — https://agents.cnry.land/workup
  - Workup block priorities — https://pages.cnry.cloud/workup-block-priorities/
  - Missing-info design (Laura, in progress) — https://pages.cnry.cloud/workup-missing-info/
  - Linear: AI Workup: Canary MCP SQL Tool —
    https://linear.app/canary-technologies/project/ai-workup-canary-mcp-sql-tool-72b25204de08
  - Linear: AI Workup: Next-Step Metric —
    https://linear.app/canary-technologies/project/ai-workup-next-step-metric-ec82c135119d

  ### "What else can I put in place?" — three things, none of which are in the letter

  1. **The vacation bypass is already happening.** The EMEA block 2 walk-through
     (https://app.notion.com/p/3b981468615180eb98ddfeb3b79a23bb) records "Blake (given
     Gareth Lloyd is unavailable) to clarify hotel kit ownership decision." Precedent is
     being set now. Naming your own cover explicitly beats leaving it to default.
  2. **The Q3B plan is your best proxy while you're away.** It is current, comprehensive
     and reads as yours. Pointing Blake at it is the cheapest way to be in the loop
     without being in the room — but it needs a named owner for the two weeks, or it goes
     stale and stops being the reference.
  3. **The adoption ask has a ready-made artifact.** The Workup readiness-by-pod tracker
     already exists in the enablement doc. That is the concrete, un-hand-wavy version of
     "I own adoption" — a table with a row per pod that someone has to drive. Worth
     naming it in the conversation when you're back, because it's the piece that maps
     directly onto SJ's adoption-curve question.

  ### Caveats

  - Two follow-up research passes did not complete: a targeted Granola query on the last
    three weeks of Blake directs timed out, and Bear has **no notes** on "cnry pages
    structured reporting" or an "overlord classification system" — the only overlord
    mention is "switched to new agent on agents framework in overlord" plus the Judge app
    at 50%. If the classification-system detail matters to you, it isn't in Bear and I
    couldn't confirm it.
  - Vacation dates are not stated anywhere I could find; the letter says "the next two
    weeks" without dates. Add them if you send it.
project: 2026-08-05-strategy
source_id: null
tags: []
time_minutes: 5
title: 'Task: "letter" to blake about Workup (new name for the investigation agent
  work) and my role under him managing laura. How to play the next few weeks.'
updated: 2026-08-13 15:21:34.872749
waiting_on: null
waiting_since: null
working_on: false
---

goal: constructive communication, not more than 400 words. For Blake's eyes only. Sell the real work I've been doing behind the scenes to develop laura and internal tools team, while recognizing that he has been tasked with driving this work forward by company leadership. 

Subtext: I don't want a perception I've been doing nothing. I don't want to be out of the loop. I want me and internal tools team under laura to get some glory. I want a role going forward. 

Tools: Granola transcripts. Notion design and discussion docs. Bear notes search for my own notes of meetings/conclusions. 

My Rough notes indicating my thoughts:

I had planned to raise this in our meeting, to figure out how to square his direction from leadership with my role: Blake VP eng > Me eng director > Laura eng lead of internal tools team (with PM Stephanie Barry)

This didn't happen (he knows why - i was in an accident)

context: In an ideal world with no external pressure, this would be hte perfect exercise for Laura to address review feedback directly, work cross org and drive things forward with energy. I.e. it's basically made for her to do what she needs to do for career progression.

To that end, all my 1-1 conversations with her in the last few months have been me encouraging her to do thought leadership and build momentum. She's responded well. Her approach leans a bit too heavily on doc output, (e.g. the cnry pages structured reporting) but I'm seeing progress in spite of her natural caution. She's in the right meetings. She's done cool stuff like adding a classification system for workup output to overlord (I think that's where it is) 

The directino from leadership changes this, I see that, and they are more important than Laura's personal development goals. Let's strategize how to take this forward. 

Awkward truth: I'm out on vacation next two weeks. Will blake go direct to her and stephanie?

What else can I put in place to achieve my goals?