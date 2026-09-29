---
area: null
completed_at: 2026-09-29 12:10:41.794980
contexts:
- consume
created: 2026-09-29 00:00:00
defer_until: null
due: null
energy: low
id: 2026-09-29T0000-check-ent-sync-transcripts
order: null
output: |-
  ## Agent run 2026-09-29T10:38:45

  Reviewed the latest entry: ENT Sync, Mon 2026-09-28
  (https://app.notion.com/p/3e9814686151806aad23c6a50358666e).
  Raw meeting note with transcript: https://app.notion.com/p/3e981468615180a8ac8aea650682bed1
  Database: https://app.notion.com/p/13c93352d06c4e88bb69af559237645c

  Present: Andrea (ran it), Ryan, Andrés, Lautaro, Tincho. Connor absent. You were not
  in the meeting and nothing was assigned to you.

  ### Worth your attention

  1. Marriott certificate expires in 12 days (about 2026-10-10) and has no clear cover.
     Lautaro raised it while arranging cover for his time out. Ryan took Kempinski, but
     the Marriott question ("do I have anyone else?") got no answer in the transcript.
     The Notion AI summary lists it as Lautaro's follow-up, which hides the gap.
  2. Golem is not working for the team. It does nothing when triggered; the guess in the
     room was monthly credits ran out. Nobody knew who owns Golem. Workup was mentioned as
     a possible replacement "not available to all teams yet". Suggested escalation was the
     Acceleration Guild or Eng Enablement channel, with no named owner for the ask.
  3. Wyndham saved card call is today (2026-09-29). Ryan is prepping from his notes and
     Tincho's design doc. Team design review sync is planned for Wed 2026-09-30.

  ### Decisions

  - Design review process: trial a new format. Everyone reads the design doc async, then a
    live sync to discuss. First use is the saved card design, Wed 2026-09-30.
  - Best Western missing-address alarm: drop the PR that excluded hotels inside the alarm.
    Use a boolean DB flag marking a hotel as intentionally missing registration fields.
    About 3 hotels affected. Why those hotels skip the fields is still unexplained.
  - Kempinski SSO: Ryan takes over from Lautaro while he is out. Currently blocked because
    the Kempinski contact is on PTO. Auth works; role mapping is undecided on their side.
  - Portfolio manage section (hotels and users): Connor approved Andrés' mockup on Fri
    2026-09-25 with minor tweaks.
  - Pyramid portfolio triage ticket: treat as likely Tipping-owned, because removing live
    tipping properties needs the tipping unwind process. Extend the SLA and agree ownership
    with Tipping.
  - Above-property dashboard dropdown (US plus EU properties): one query to the identity
    pod's DynamoDB table, not per-environment queries with an auth key. Permission gating
    and cross-environment click-through are still open.
  - IHG SSO removal: needs a ticket and approval first. Removal must also revoke the roles
    SSO granted, otherwise users keep access through username and password login.
  - Triage is the top priority for whoever is on triage (Andrés this week). Flag deadline
    conflicts to Andrea and Connor.

  ### Action items

  - Ryan: set blocked tickets to Blocked status, not only the label (label was used to
    stop the SLA clock). About 19 points in progress, many blocked.
  - Ryan: review notes and saved card design before today's Wyndham call.
  - Ryan: pull in a content gateway UI ticket.
  - Design review sync for Wednesday: owner is unclear, see caveats.
  - Lautaro: add Ryan to the Kempinski email thread and reply.
  - Lautaro: Marriott certificate renewal, see item 1 above.
  - Lautaro: finish UI fixes for the Xplore to Omni migration.
  - Andrés: create UI and service tickets for portfolio hotel/user management, then start.
  - Andrés: extend SLA on the Pyramid ticket and align with Tipping on ownership.
  - Andrés: sync with Manuel on running the hotel classification command. The Wyndham
    pilot hotel rollout has not been executed yet and is queued behind triage.
  - Andrés: wait for confirmation before deleting the S3 buckets.
  - Andrés: address review comments on the IHG Greener Stay PR. Its SLA is close to expiry.
  - Taylor Kirchwehm: create the IHG SSO removal ticket once approved.
  - Andrea: pass non-SLA triage tickets to Tincho, who has spare capacity.
  - Tincho: deploy IHG work to staging. Drift detection meeting likely slips to next sprint.
  - Unowned: ask about Golem in Acceleration Guild or Eng Enablement.

  ### Topics

  Triage, Wyndham (saved card, pilot rollout), IHG (SSO removal, Greener Stay, staging
  deploy), Best Western alarm, Content Gateway, Omni Migration, Kempinski SSO, Marriott
  certificate, portfolios and above-property dashboard, design review process, Golem.

  ### Caveats on the source

  - The transcript has no speaker labels, so attribution comes from Notion AI's summary
    and from context. Treat owners as probable.
  - Likely misattribution: the summary gives the Wednesday design review sync to Ryan.
    In the transcript the person offering to schedule it is the one who was "waiting on
    your review first", which reads as the design author, Tincho.
  - Transcription errors: "Teen Show" is Tincho, "Gollum" is Golem. "Tiffin" (S3 bucket
    owner) and "color approval" (IHG SSO removal) could not be resolved.
  - The summary omits the Greener Stay PR discussion and the open Marriott cover question.
  - The page's Summary, Decisions, Action Items, Attendees, Topics and Source Note fields
    are all empty. The same is true for the 09-21, 09-14 and 08-31 entries, so the
    ENT Sync Entry template is not being filled in. I did not edit anything in Notion.
project: null
source_id: null
tags: []
time_minutes: 10
title: Check ENT sync transcripts
updated: 2026-09-29 12:10:41.794973
waiting_on: null
waiting_since: null
working_on: false
---

Review the latest ENT sync meeting transcript — action items, decisions, and topics.

https://app.notion.com/p/canarytechnologies/13c93352d06c4e88bb69af559237645c?v=5f62f3dba7234433870e5cfeb927403f&source=copy_link