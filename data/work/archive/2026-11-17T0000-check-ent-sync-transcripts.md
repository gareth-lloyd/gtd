---
area: null
completed_at: 2026-11-17 13:54:54.704390
contexts:
- consume
created: 2026-11-17 00:00:00
defer_until: null
due: null
energy: low
id: 2026-11-17T0000-check-ent-sync-transcripts
order: null
output: |
  ## Agent run 2026-11-17T13:54

  Latest ENT sync: **ENT Sync Entry, Mon 2026-11-16** (https://app.notion.com/p/41a8146861518063b349d59aa5b7f7e8). Read the Notion AI summary and the full transcript. The page's own Summary / Decisions / Action Items sections are empty; only the AI summary and raw transcript exist. You were not a speaker. Speakers are unlabelled (A-E) in the transcript; I mapped them from context as A = Connor, B = Andrea, C = Ryan, D = Andrés, E = Tincho. Treat owner names below as my inference where the summary left them blank.

  Other new entries in the same database since the previous ENT sync (2026-11-02), not reviewed here: IHG Loyalty Amenity Sync 2026-11-16 (https://app.notion.com/p/41a81468615180fdb8eae1f69026b0c4), Wyndham Automated Activation Workflows 2026-11-11 (https://app.notion.com/p/4158146861518083b612efdfd0b765fd), ENT 2026Q4B pitches 2026-11-09 (https://app.notion.com/p/41381468615180bab875de4054d8a9b0), Wyndham Drift Detection & Audit Workflow Sync 2026-11-06 (https://app.notion.com/p/410814686151803382d5c8c529a48141).

  ### Touches you
  - **Tincho owes you a PR review** and planned to do it the afternoon of 11-16, behind triage. The PR was not named. Nothing was assigned to you.

  ### Decisions
  - Internal ENT sync on Mon 2026-11-30 gets moved; the Wyndham meeting keeps the slot (Connor moves it).
  - IHG loyalty welcome amenity (upsell -> check-in flow step): do not over-engineer for older IHG mobile app versions and do not degrade web for the app. Accepted outcome is that some app users will not see the new flow until they update. Not final: depended on Andrea's sync with Leandro that afternoon and on Caitlin agreeing to the gap.
  - Create a triage ticket for the Wyndham configuration script change (flag values), since all Wyndham hotels are being migrated (Connor).
  - Per-channel gateway rollout plan: ship, test on a staging hotel with Manu, then all Wyndham hotels; existing hotels handled by backfill plus onboarding script update rather than hand-edited values.

  ### Action items
  - Connor: add the video link to the IHG auto-enrollment invite (Mon 11-23); send the PRD with IHG API docs to Ryan and Andrea; move the 11-30 internal sync; create the Wyndham config script triage ticket.
  - Ryan, Andrea: read the IHG API docs on the PRD before 11-23. (The Notion summary says Ryan and Andrés; the transcript says Ryan and Andrea were the ones added to the meeting.)
  - Andrea: sync with Leandro on whether the upsell must stay for older app versions and whether Instinct-team filtering is needed; get numbers or sign-off from Caitlin; review Marta's doc on the Wyndham site ID format change; finish first pass of the cross-region property dropdown design doc; send the follow-up dashboard flash PR via eng enablement.
  - Andrés: ship per-channel gateway, test with Manu, roll out, backfill and update onboarding scripts; post the managed portfolios SSO UI to Just Hatched after deploy; send the SCIM doc to Wyndham (targeted 11-16); solve rate limiting during Okta's initial sync (idea: a flag to bypass temporarily).
  - Tincho: finish triage items; review your PR; re-read the IHG scripting Slack thread and progress his open IHG scripting PR; check the IHG blocked countries Notion page and queue more countries for Luan to QA this week (Fiji for sure).
  - Ryan: keep working ENT-7909 (Microsoft SSO, questions back with the customer); close the Barclays dependency ticket once Arrivals/Departures reaches 100% (90% now, expected end of week); send the channel a list of PRs needing review.
  - World Hotels SSO image: the Notion summary says Ryan provides it. The transcript reads the other way: Ryan is waiting on it and someone else (probably Connor) said they would get it to him that day.

  ### Topics
  - **IHG auto-enrollment**: API docs received from IHG. Mon 11-23 meeting is with IHG business teams about the experience, not technical. Connor hopes it fits the existing pattern used for other brands. Discovery will land on this team.
  - **AVM / Synxis Property Hub**: SPH is about 2/3 of Wyndham, OHIP about 1/3. Commercial terms likely moving from a flat per-hotel fee to per-API-call. AVM will open the integration to non-Wyndham hotels, described as the biggest blocker to voice expansion today. Owned by Ian and PMS gateway; no direct ENT development expected.
  - **Mobile versioning**: with more mobile apps, frontend/backend changes no longer reach every client at once. Raised as a concern for all of EPD, no owner or follow-up assigned.
  - **Wyndham site ID format change**: Wyndham is changing site IDs (longer or different format); Marta has a doc, Andrea is checking impact.
  - **SCIM for Wyndham**: Andrés can test locally against Okta. Okta does an initial sync, so no import needed on our side. Demo this Friday (11-20).
  - **Voice config**: Andrea reviewing Stephen's PRs for SRS config and Wyndham Connect vs voice vs shell properties for portfolio-wide calls.
  - **Weekend incident**: mostly settled, comms sent, Connor following up with Blake on 11-16.
  - **Block planning** is Connor's main focus this week across pods.
  - Side note: Ryan is asking eng enablement to make Birdline show PR review requirements on the PR itself.

  ### Possible follow-ups for you (my suggestions, not from the meeting)
  - If the PR review from Tincho has not arrived, nudge him; he was swamped with triage.
  - The Wyndham site ID format change may matter to anything keyed on site ID (e.g. sso_hotel_id lookups). Worth a glance at Marta's doc if Andrea's check does not cover your areas.
  - The mobile versioning concern overlaps with the Wyndham SDK gating work (MOB-1470, X-SDK-Platform header).
project: null
source_id: null
tags: []
time_minutes: 10
title: Check ENT sync transcripts
updated: 2026-11-17 13:55:32.742137
waiting_on: null
waiting_since: null
working_on: false
---

Review the latest ENT sync meeting transcript — action items, decisions, and topics.

https://app.notion.com/p/canarytechnologies/13c93352d06c4e88bb69af559237645c?v=5f62f3dba7234433870e5cfeb927403f&source=copy_link