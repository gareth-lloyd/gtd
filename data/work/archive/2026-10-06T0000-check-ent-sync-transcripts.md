---
area: null
completed_at: 2026-10-06 09:42:13.459403
contexts:
- consume
created: 2026-10-06 00:00:00
defer_until: null
due: null
energy: low
id: 2026-10-06T0000-check-ent-sync-transcripts
order: null
output: |-
  ## Agent run 2026-10-06T09:31:55+0300

  Latest entry: ENT Sync, Mon 2026-10-05 (https://app.notion.com/p/3f0814686151800bb49fe9a48c5e8f87).
  Source: the Notion AI summary plus the raw transcript on that page. The transcript has no speaker
  labels, so owners below are from the AI summary, checked against context where I could. Ones I
  could not confirm are marked "(inferred)".

  ### Touches you directly
  - IHG Core opportunity detection: Andrea said you found that the scripts may not be identifying
    IHG Core opportunities correctly (transcribed as "ISG core"), probably after Salesforce-side
    changes. She is tweaking the scripts. She described the two of you as checking the health of
    hotels that went through the configuration scripts, and deciding later whether that becomes an
    Omni dashboard (would need extra data in Omni).
  - New enterprise PM (Nathan): Connor said he is discussing with Blake, Andrea and you where Nathan
    sits in the org, and separately what PM ownership of scripting looks like, since Nathan is a weak
    fit for backend-heavy work. Offer goes out this week, not yet accepted.
  - Eng All Hands next week: Andrea is presenting configuration scripts, rollouts and drift
    detection, aiming to get other teams using rollouts for enterprise backfills. She may ping
    people for slides.

  ### Time-sensitive
  - Marriott SSO certificate expires Sat 2026-10-10. Rotation is not scheduled; waiting on
    Marriott's IAM team. Andrea: "It's probably going to break all of their logins." Andrea is
    re-replying on the email thread and pinging Taylor (at Marriott HQ in Bethesda on Monday).
    Connor offered to escalate to Brian.
  - SCIM for Best Western: BW has agreed to use SCIM, and their convention is 3 weeks out
    (~2026-10-26). Go/no-go on shipping before the convention was wanted Mon/Tue. Lautaro and Andrés
    owe an effort estimate Wed 2026-10-07. Lautaro's read: MVP is a few extra endpoints that update
    users. Open question: GDPR (raised by Laura on the PRD). Connor wants the slimmest MVP.
    Risk I noticed, not raised in the meeting: Lautaro's baby is due any day, and he wrote the SCIM
    design; Andrés had not read it yet.

  ### Decisions
  - Enable Property Insights dashboards for all non-enterprise hotels (everyone except Wyndham,
    Best Western, IHG), planned for Monday via GrowthBook, pending a portfolio-behaviour test.
  - Extend an offer to Nathan (PM, enterprise). Ex-agency, product lead on JetBlue's in-flight
    experience, New York based. Wyndham Barclays is the likely onboarding project.
  - Lautaro to take nothing beyond Explo-to-Omni and SCIM.
  - Hotel exclusions belong in the rollout recipe code, not in people's heads.
  - Sprint points: no change. Leadership is not concerned about 30-40 point boards; do not zero out
    points on tickets in review. Topic goes to a focused retro.

  ### Action items
  - Tincho: review Ryan's rollout recipe PR. Likely PR #58858, [ENT-7734] "Make BW guest journey
    re-runs safe for excluded hotels" (https://github.com/canary-technologies-corp/canary/pull/58858).
    Tincho thinks the change as written may affect other properties.
  - Ryan: rework that PR (he agreed it was implemented wrong); schedule a 30-minute design review
    for the Barclays card project this week.
  - Lautaro + Andrés: SCIM effort estimate by Wed 2026-10-07.
  - Andrea: re-reply on the Marriott thread and chase Taylor; All Hands slides; finish first pass of
    the eng design for the global hotel list header.
  - Connor: sync with Daniel and Lautaro on the Property Insights release, including a GrowthBook
    walkthrough so he can do it alone; record a video and app-cue announcement; connect Andrea with
    Nathan.
  - Andrés: share the Wyndham OHIP fix PR with the PMS Gateway team. Likely one of his two drafts:
    #59087 "Expose Opera payment-method flags through PMS Gateway"
    (https://github.com/canary-technologies-corp/canary/pull/59087) or #59068 "Check Opera token
    acceptance before Wyndham go-live sets tokenize"
    (https://github.com/canary-technologies-corp/canary/pull/59068).
  - Lautaro: reply to Kempinski to finish SSO enablement; write a Notion doc of pending Explo
    migrations.
  - Tincho (inferred): reshare the weekend incident retro doc in the main channel.
  - Team: focused retro on sprint points / Linear workflow.

  ### Topics
  - BW rollout recipe bug: Ryan ran the guest journey messaging plan across all BW hotels using the
    rollout recipe. The recipe included hotels that were meant to be excluded, so their messages
    were altered and hotels reported it. Root cause: the exclusions lived only in tribal knowledge.
    Wish stated: drift detection should catch this eventually.
  - Weekend incident: someone had to log on Sunday to approve a PR (Tincho, inferred). Retro doc
    exists with learnings.
  - Updates: Lautaro on the last Explo-to-Omni step (un-migrated overrides show a "not migrated"
    error dashboard); European SSO enablement mostly done, Tincho doing the US side. Ryan closed
    many stale blocked tickets, is on Content Gateway UI. Andrea on IHG script issues (wrong
    Salesforce ID for a Canadian hotel, FreedomPay gateway not configured; Golem working again),
    WhatsApp message errors fix. Andrés on a segmentation layer that uses Salesforce data without a
    real Salesforce account, portfolio manage app PRs with Laura, and a missed weekend SLA (ticket
    arrived from on-call out of hours). Tincho (the summary's "unnamed team member") slightly
    behind on drift detection UI, has a spike, PR soon.
  - Availability: Andrea and Connor both out "the weekend of the 19th of October". The 19th is a
    Monday, so the exact days are unclear.

  ### Housekeeping
  - The database row properties (Attendees, Topics, Action Items, Decisions, Source Note) and the
    page's Summary/Decisions/Action Items headings are empty for this entry and for the 09-14,
    09-21 and 09-28 entries; only the embedded meeting note is filled. I changed nothing in Notion.
project: null
source_id: null
tags: []
time_minutes: 10
title: Check ENT sync transcripts
updated: 2026-10-06 09:42:13.459398
waiting_on: null
waiting_since: null
working_on: false
---

Review the latest ENT sync meeting transcript — action items, decisions, and topics.

https://app.notion.com/p/canarytechnologies/13c93352d06c4e88bb69af559237645c?v=5f62f3dba7234433870e5cfeb927403f&source=copy_link