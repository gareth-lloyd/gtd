---
area: null
completed_at: 2026-08-31 14:28:18.504433
contexts: []
created: 2026-08-31 11:42:40.932029
defer_until: null
due: null
energy: low
id: 2026-08-31T1142-review-peter-s-notes
order: null
output: |
  ## Agent run 2026-08-31T13:40Z — review of Peter's 2-week update

  Source: Peter Gao DM, 2026-08-31 11:39 EEST
  https://canarytechnologies.slack.com/archives/D0B7ZNDSKQ9/p1788165572134949

  I read the update, then checked each claim against Linear (APAC team) and GitHub, and
  pulled your own prior notes on Peter/Adil/Crown from Bear. Nothing was posted anywhere.

  ### What Peter reported
  1. Adil: eFolio ticket fallout handled — his tickets moved from other pods' triage into
     APAC, assigned to Adil as a holding pattern; 1:1 covered communication style.
  2. Comms Core / Messaging pod PR reviews stalled (Mati, Chetna, Rick). Mati cites the
     two-pod merge. Peter escalated to Rachel.
  3. Swapped with In-Stay: APAC takes Shiji Infrasys POS (2nd POS after Simphony), In-Stay
     takes Knowcross. Sandbox mid-Sept, live end-Sept.
     Design doc: https://app.notion.com/p/canarytechnologies/Infrasys-POS-Integration-3ba81468615180ab82d9c3bf17d84701
  4. In-Room Compendium: live testing with Crown on room binding + reservation handling.
     Blocked waiting on Crown to confirm their MDM can reset the browser to a preset URL.
  5. eFolio project scoped/designed, kicks off tomorrow, ~2 weeks of work.
  6. Smaller releases: auto-translate fixes, en_GB + Indonesian language support.

  ### Verification — where the record disagrees with the narrative

  **a) The PR-review backlog is worse than the note implies, and it's mostly Peter's own work.**
  Peter has 7 stacked FBM PRs open since **6 Aug — 25 days**:
    #52385 https://github.com/canary-technologies-corp/canary/pull/52385
    #52386 #52387 #52389 #52390 #52391 #52425 (same date, same stack)
  The matching Linear issues (APAC-37/38/39/40/41/42/43/44/45/46/47/48/49) have all sat in
  "In Review" since 25 May. The "Support for FB Messenger" project
  (https://linear.app/canary-technologies/project/support-for-fb-messenger-5015c6ab9b51)
  has targetDate **2026-08-31 — today** and is still in status "Eng Design". It misses today.
  That is the hard number to give Rachel, and it is stronger than "reviews have fallen behind".

  Two caveats that are NOT Comms Core's fault:
    - Adil's #54483 (27 Aug, non-draft) has **no reviewer requested at all**.
      https://github.com/canary-technologies-corp/canary/pull/54483
    - Adil's #52693 was **approved by luchux and peteygao and is still open since 10 Aug**.
      https://github.com/canary-technologies-corp/canary/pull/52693 — approved-and-unmerged
      for three weeks is an author/merge-hygiene problem, not a review-capacity problem.
    - Belinda has ~20 stale Draft PRs from 8 and 26 May (Viber + an FBM stack that duplicates
      Peter's, e.g. #46250–#46306, #45002–#45014). Worth closing so the queue reads honestly.

  **b) I could not find the Adil "holding pattern" pile.**
  Peter says he moved the tickets Adil filed into other pods' triage into APAC and assigned
  them to Adil. In the APAC team, Adil is assigned only 8 issues (APAC-51/52/72/73/78/79/89/93)
  — mostly Done, plus IRC: Security and the eFolio design doc In Review. Only two APAC issues
  sit in Triage (APAC-94, assigned Peter; APAC-85, unassigned). Either the pile landed
  somewhere else or it was resolved differently. Worth one question, not an accusation.

  **c) The Infrasys commitment is not backed by the plan of record.**
  Project: https://linear.app/canary-technologies/project/fandb-infrasys-pos-integration-4772ca98dcdb
  Lead Peter, status Implementation, **targetDate 2026-09-25**. But APAC-106/107/108/109/110/
  111/112/113 are all still "To Discover / Refine", and APAC-101/102/103/105 are Backlog.
  Only APAC-98 (auth/context/errors) is Deployed and APAC-104 (room-charge target) In Progress.
  A mid-Sept sandbox deploy off a backlog that is still largely unrefined is the single
  biggest schedule risk in this update.

  **d) Knowcross was handed away but the Crown risk was not.**
  Project: https://linear.app/canary-technologies/project/compendium-wire-knowcross-into-compendium-service-request-2eb29c0ee53e
  Lead is Joanne Chevalier, target 2026-09-30 — but **APAC is still listed as a team on it**,
  and the description states plainly: "This is to unblock Crown from going live. Committed to
  deliver before end of Q3." So APAC gave away a dependency of its own customer commitment.
  Ask: has In-Stay accepted the end-Q3 date in writing, who owns the Crown go-live risk now,
  and should APAC come off the project team so the ownership is unambiguous.

  **e) Linear hygiene on Crown — you already asked for this on 29 Jul.**
    - "Crown Resorts - In-room compendium" is marked **Completed (21 Aug)**, target 28 Aug
      https://linear.app/canary-technologies/project/crown-resorts-in-room-compendium-f3608ac32b6d
      …yet APAC-93 "IRC: Security" is still In Review and live testing is actively blocked.
    - "Crown Resorts Deployment - In-room compendium" is **High priority, status Backlog,
      no start date, no target date**
      https://linear.app/canary-technologies/project/crown-resorts-deployment-in-room-compendium-3c1518fa8a76
      …despite being the project the live testing actually sits under.
    On 29 Jul you told Peter "aim to get the current cycle in Linear accurate". This is the
    follow-up, and it is the second ask rather than the first.

  **f) eFolio kicks off tomorrow with no date and no lead.**
  https://linear.app/canary-technologies/project/efolio-summarization-f82d72911238
  Status "Product Definition", **no targetDate, no lead**. APAC-72 (design doc) still In Review;
  APAC-83 "AD-6703 execution" and APAC-91 "Match Opera folio presentation" are both Icebox.
  If it genuinely starts tomorrow, it needs a lead, a target date and a move to Implementation.

  **g) Not mentioned at all: Ryan Iskandar.**
  riskandar@canarytechnologies.com was added to the APAC Linear team on **2026-08-28** and the
  Linear account itself was created that day — i.e. brand new. A new person joining the pod
  during your absence is exactly the kind of thing the update should have led with. Ask who
  they are, what they're picking up, and who is onboarding them.

  **h) Capacity collision.** Mid-Sept Infrasys sandbox + 2 weeks of eFolio + Crown live testing
  land in the same fortnight, across a pod of Peter, Adil, Belinda and one brand-new joiner,
  while Peter's own 7-PR FBM stack is still unmerged. Something in that list is going to slip;
  better to pick which one now than to discover it on 25 Sept.

  ### The Adil situation — the highest-value thing here

  This is now the fourth independent report of the same behaviour: Sudarshan (23 Jul, Bear),
  Ian Clark (18 Aug), the messaging pods, and now Peter. Your Bear note from the Sudarshan
  conversation frames it better than the current coaching does — the problem is not exploration,
  it is bounding and communicating scope: *"He actually knows the scope, but he can't hold back.
  Feedback is not don't explore — COMMUNICATE what it is."* Peter's version ("meet them half way",
  "maximally informational isn't a resolution") is a fair read but softer.

  Decision that is yours, not Peter's: does this stay peer coaching by Peter, or does it become
  something you own and document? Four reporters in six weeks is the point where the informal
  route stops being credible. Adil was raised $95k → $98k on 27 May, which argues for getting
  the expectation in writing sooner rather than later.

  Also relevant from Bear, on Peter himself: your logged concerns (20–23 Jul) are all about
  proactive communication — "I feel like I'm chasing a bit", "weirdly unsure about who he's
  talked to". This update is unprompted, structured and honest about blockers. That is a
  genuine improvement on the July pattern and is worth naming back to him explicitly.

  ### Suggested 1:1 agenda / reply (DRAFT ONLY — nothing sent)
  1. Thank him for the update and name the improvement in proactive comms.
  2. Ryan Iskandar — who, what, and who's onboarding.
  3. Infrasys: 8 tickets still in "To Discover / Refine" vs a 25 Sept target. What's the real
     critical path to a mid-Sept sandbox?
  4. Knowcross/Crown: who carries the go-live risk now, and has In-Stay signed up to end-Q3?
  5. Crown MDM: is there a date-certain from Crown, and what's the fallback if their MDM
     can't reset the browser URL?
  6. Linear accuracy — Crown projects and the eFolio project (lead + target date). Second ask.
  7. Give Rachel the number: 7 PRs, 25 days, a project target date missed today.
  8. Adil: agree explicitly whether this stays with Peter or escalates to you.
project: null
source_id: null
tags: []
time_minutes: 5
title: Review peter's notes
updated: 2026-08-31 14:28:18.504424
waiting_on: null
waiting_since: null
working_on: false
---

https://canarytechnologies.slack.com/archives/D0B7ZNDSKQ9/p1788165572134949