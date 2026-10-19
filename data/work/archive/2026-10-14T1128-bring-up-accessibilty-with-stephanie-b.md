---
area: null
completed_at: 2026-10-16 15:42:50.345407
contexts: []
created: 2026-10-14 11:28:38.334227
defer_until: null
due: 2026-10-15
energy: low
id: 2026-10-14T1128-bring-up-accessibilty-with-stephanie-b
order: null
output: |
  ## Agent run 2026-10-15T14:57:40

  Prep notes for the Stephanie 1:1 (Oct 15). Sources: Slack, Linear, Granola, and
  the related GTD items (Diana follow-ups #2, Blake Monday ownership item).

  ### Where things stand (what I found)

  Web (guest web app: check-in and compendium). This is the live track.
  - Stephanie took the web VPAT over from Amanda (announced by Daga, Oct 6):
    https://canarytechnologies.slack.com/archives/C09D2A5LYN9/p1791272627600559?thread_ts=1791272376.107829&cid=C09D2A5LYN9
  - Linear project "Guest A11y Remediation", lead Stephanie, target Nov 13:
    https://linear.app/canary-technologies/project/guest-a11y-remediation-ab518d16668b
    - 42 issues. 12 Done (mostly Amanda's), about 22 In Review, 2 In Progress, 3 Backlog.
    - Nearly all In Review items are assigned to Stephanie, including 5 Urgent ones
      (EE-2129, EE-2243, EE-2132, EE-2112, EE-2142) and EE-2212, the Google Wallet button name.
    - The project summary says the findings come from an "Aug 2026 Essentia11y audit",
      not Level Access. Ask which findings Level Access will retest.
  - Nov 14 is Amanda's conservative VPAT estimate for guest web
    (Amanda in #rfp-accor-digitalkey, Sep 25; Z's WCAG thread:
    https://canarytechnologies.slack.com/archives/C0AHEMNMWMN/p1790357353808039). Jean-Charles says Nov 14 is not in the Accor contract.
    It is an internal target, to keep and to flag early if it slips.
  - Daga's flag (Oct 6): as of then, nothing had been submitted to Level Access, and the
    retest/VPAT may take more than a month after submission. Nov 14 is tight.
  - Blake's fallback: a remediation-status document by Nov 15 if the VPAT isn't ready.
  - Blake's closing steer in that thread: fix all web check-in and compendium issues first.
    Mobile can follow.

  Mobile SDK (our team)
  - Accor now wants in-app NFC: an "Add to Wallet" button inside Accor's own app, no BLE.
    Accor does the MFA and renders the UI, and the wallet button and sheet are native
    Apple/Google controls. Blake (after talking to Mehul): "no mobile SDK UI". Diana:
    the SDK only becomes our audit surface if we ship the button component ourselves.
  - Diana has paused mobile accessibility, citing Accor's small scope.
  - Counterpoint from the Granola notes: the Level Access retest takes 30+ days, so
    deprioritising it creates enterprise risk. IHG may need AA (earlier notes said AA was
    a prerequisite for IHG using the SDK, at roughly 1 week of engineering plus 3 weeks of
    certification). https://notes.granola.ai/d/6e3be9bf-2577-457d-927a-318f20699685 ,
    https://notes.granola.ai/d/5bc6a835-e3a9-4c2f-b7fe-d01293a11c74 ,
    https://notes.granola.ai/d/d0de2936-cdf1-44f8-a66a-8c3413970e56
  - Stephanie already shipped a mobile SDK accessibility linter (agent-based, iOS and
    Android, advisory CI with a ratchet) that could serve as the "SDK guardrails":
    https://linear.app/canary-technologies/project/mobile-accessibility-linter-69a0d7f5a13a

  Kiosk: separate track, not part of Nov 14 (per JC). Linear "LevelAccess Accessibility",
  lead Matthew Jeffery, Planned, many unassigned AD and KSK tickets:
  https://linear.app/canary-technologies/project/levelaccess-accessibility-64991f3ab1ea

  Contract: per the Blake inbox item, the Level Access contract runs to March 2027.
  I couldn't confirm what it covers (retest count, which surfaces).

  ### Questions to ask Stephanie

  1. Web VPAT: has anything gone to Level Access yet? When is the submission, and what's
     their stated turnaround? Is Nov 13/14 still realistic?
  2. About 22 tickets are In Review, all hers. Who's reviewing them? Is review the bottleneck,
     and does she need reviewers from Mobile or EE?
  3. Will Critical/High all be closed, or is "Partially Supports" plus a remediation doc the
     realistic outcome? Should we start Blake's Nov 15 fallback doc now?
  4. Audit source: Essentia11y (Aug) vs Level Access. Does Level Access retest against the
     Essentia11y findings or its own audit? Which surfaces and how many retests does the
     contract (to Mar 2027) include? Is there an SDK audit already?
  5. Accor mobile scope: anything changed this week now the physical team runs Accor?
     Is the SDK still headless (no button component from us)? Is MFA fully on Accor's side?
  6. Mobile SDK backlog: given the 30+ day retest lead time and IHG, would she start the
     SDK fixes now or wait? Rough size? Is the mobile linter baseline a usable backlog?
  7. Capacity: she now owns web VPAT, Accor web, and was the mobile linter lead. What's
     she dropping? Is Z still co-running Level Access, and where does Amanda fit now?

  ### What to carry to Blake on Monday (Oct 19)

  The facts from 1, 4, and 6, so you can confirm your steer on mobile: start the SDK
  backlog now because of the lead time, or keep Diana's pause.

  ### Caveats

  - Ticket statuses are as of the Linear read today. I didn't open individual tickets or PRs.
  - The Granola points come from a Granola AI summary, which can misattribute speakers.
    Check the transcripts before citing who said what.
  - IHG's AA requirement comes from older meeting notes. I found no current IHG ticket or
    Slack thread confirming it.
  - Nothing was written to any external service.

  ## Agent run 2026-10-16T15:44:18

  > Follow-up asked: "eli10"

  The prior run, explained simply. No new research; every fact comes from the run above.

  ### The big idea
  Some people use phones and websites in different ways. Some can't see well, some
  can't use a mouse, and some use a screen reader that reads the page out loud.
  "Accessibility" means building our stuff so it works for them too. Big customers
  like Accor want proof that it does. That proof is a report card called a VPAT.
  A company called Level Access checks our work and helps write the report card.

  ### There are three things to check

  1. The website guests use (check-in and the hotel guide). This is the urgent one.
     - Stephanie is now in charge of it. She took it over from Amanda.
     - There's a list of 42 things to fix. 12 are done, and about 22 are fixed but
       waiting for someone to check the fix. Almost all of those 22 belong to Stephanie.
     - The goal is to have the report card by mid-November (Nov 13/14). That date is our
       own goal, not a promise in Accor's contract. Still, we should say early if it slips.
     - The catch: once we hand the work to Level Access, their check can take more than
       a month. On Oct 6 nothing had been handed over yet, so mid-November is tight.
     - The backup plan (Blake's): if the report card isn't ready, send a "here's what
       we've fixed and what's left" document by Nov 15.
     - Blake says fix the website first. The phone stuff can wait.

  2. The phone toolkit (the mobile SDK, our team's part).
     - Accor now wants an "Add to Wallet" button inside their own app. Accor builds the
       screens, and the button itself is made by Apple and Google, not by us.
     - So we may have nothing on screen to check. Diana has paused this work for now.
     - The worry: if another customer (maybe IHG) needs it later, the 30+ day checking
       wait means starting late hurts. IHG needing it comes from older notes, so it's
       unconfirmed.
     - Bonus: Stephanie already built a tool that spots accessibility problems in the
       phone code automatically. It could become our to-do list if we start.

  3. The hotel lobby kiosk. This is a separate track that Matthew leads. It isn't part of
     the November deadline.

  ### What to ask Stephanie (short version)
  1. Have we handed the website to Level Access yet? Is mid-November still realistic?
  2. Who is checking her ~22 finished fixes? Does she need helpers?
  3. Will everything important get fixed, or should we start the backup document now?
  4. Is Level Access checking against the August audit (by a different company,
     Essentia11y) or its own? What does our deal with them cover? It runs to March 2027.
  5. Has Accor's phone plan changed? Are we really building no buttons?
  6. Should we start the phone fixes now because the checking takes so long, or wait?
  7. She's doing a lot. What's she dropping? Is Z still helping?

  ### Why it matters for Monday (Oct 19)
  You'll tell Blake whether to start the phone fixes now or keep them paused. Questions
  1, 4 and 6 give you the facts for that call.
project: 2026-09-08-mobile
source_id: null
tags: []
time_minutes: 5
title: Prep accessibility notes before stephanie 1-1
updated: 2026-10-16 15:46:00.000000
waiting_on: null
waiting_since: null
working_on: false
---