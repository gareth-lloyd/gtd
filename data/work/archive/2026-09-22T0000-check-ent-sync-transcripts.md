---
area: null
completed_at: 2026-09-22 13:41:04.247042
contexts:
- consume
created: 2026-09-22 00:00:00
defer_until: null
due: 2026-09-22
energy: low
id: 2026-09-22T0000-check-ent-sync-transcripts
order: null
output: |
  ## Agent run 2026-09-22

  Latest ENT sync entry: 2026-09-21 (https://app.notion.com/p/3e28146861518074b8adc0eb7805277a).
  The Summary / Decisions / Action Items sections on the page are empty; the Notion AI meeting summary and cleaned transcript are populated. Previous entry 2026-09-14 (https://app.notion.com/p/3db8146861518043956be55c04e0149c) reviewed for carry-overs.

  ### Items touching Gareth
  - Transcript summary says "Gareth Lloyd's PR related to the SLA/hotel key configuration ticket needs review". In the raw transcript Ryan actually says "there's a Golem PR that's related that needs to be reviewed. So I'm doing that as well" - the summariser likely attributed the Golem PR to you. Ryan also said "let me know... I did some initial work on this, so if there's anything I can help with or make sure we're not duplicating". Worth confirming with Ryan whether the Golem PR is one you launched, and whether you have overlapping work.
    - SLA ticket "#7576" resolves in Linear to INT-11164 "Can't post ccs from auths to PMS" (BW Plus Winter Haven, HotelKey, moved to Integrations, back in Triage) https://linear.app/canary-technologies/issue/INT-11164/cant-post-ccs-from-auths-to-pms
    - Ryan's fix PR #57203 "Flag tokenize auth strategy with no payment gateway" is already APPROVED (https://github.com/canary-technologies-corp/canary/pull/57203). Ryan was assigned the ticket in the meeting.
    - I could not identify a separate open Golem PR for this ticket via gh search; not resolved.
  - Peer reviews due Friday 2026-09-25 - Connor reminded everyone to start.
  - Review buddies: pairings unchanged for now; rotation expected once Lautaro returns.

  ### Decisions
  - Wyndham segmentation migration pilot plan: run on OHIP sandbox / a UAT property first, Wyndham verifies (~couple of days), then a small set of real pilot properties. No production green light from Wyndham yet. Connor to give them a heads-up when UAT update is ready.
  - Andrés keeps his current review buddy; rotation deferred.
  - Two department models (hotel tipping departments vs the ticketing app's new model with no Django admin): team agreed it is a problem but "not in our realm", ENT is only enabling product permissions on departments. Connor offered backing if needed.
  - S3 bucket security ticket (platform security group; HTTPS restrictions + retention lifecycle on ENT-owned buckets): a team member volunteered to take it (name not captured in transcript).

  ### Action items (all owners)
  - Connor: email Sonia today about Content Gateway rollout timeline, CC team. Give Wyndham heads-up when UAT sites ready for segmentation pilot.
  - Ryan: continue INT-11164 / hotel key configuration; backfill config may be needed after "migrate to hotel key configuration values" PRs merge; also starting "list all properties globally" and expanding department permissions to include product.
  - Tincho: eng design for tracking acknowledgement of risk detection settings (ready today/tomorrow, team to review, possible group discussion later in week); risk detection backend + frontend PRs posted in team channel with video; IHG Mexican RefCars fields fix PR needs a quick approval so it can be tested in the afternoon.
  - Andrés: Wyndham segmentation monitoring tickets, then pilot this week; Wyndham SSO issue for a couple of accounts (related to a prior triage ticket); confirm pilot readiness on Slack and sync with Manuel; keep Manu in the loop.
  - Lautaro (or whoever is on translations): Icelandic translations PR incl. registration cards and upsell translations; Omni migration PRs outstanding.
  - Andrea: Content Gateway end-to-end validated (5-6 entries, images work), ready to roll out on approval; two open Managed Context tickets to look at.

  ### Topics
  Content Gateway, Wyndham segmentation migration, Risk detection / drift UI, IHG Mexican RefCars fix, Translations & Omni migration, Hotel key configuration & department model, S3 bucket security, Review buddies, Peer reviews.

  ### Carry-overs from 2026-09-14 not mentioned on 2026-09-21
  - IHG new countries (Thailand, Iceland, Jordan) check-in requirements - Iceland translations now underway, no update on Thailand/Jordan.
  - Best Western OTA messaging issue investigation (Ryan).
  - Salesforce Wyndham site ID reconciliation script verification (Ryan).
  - GroundCover monitors draft PR second opinion.
  - Drift detection: Loom video (done, video was shared), approved-drifts spike ticket, filter-by-app, coordinate with Tommy Slater.

  Notes: the DB rows for both entries have empty Action Items / Decisions / Topics properties. No external writes made.
project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 10
title: Check ENT sync transcripts
updated: 2026-09-22 13:41:04.247038
waiting_on: null
waiting_since: null
working_on: false
---

Review the latest ENT sync meeting transcript — action items, decisions, and topics.

https://app.notion.com/p/canarytechnologies/13c93352d06c4e88bb69af559237645c?v=5f62f3dba7234433870e5cfeb927403f&source=copy_link