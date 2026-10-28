---
area: null
completed_at: 2026-10-27 13:22:41.741977
contexts:
- consume
created: 2026-10-27 00:00:00
defer_until: null
due: null
energy: low
id: 2026-10-27T0000-check-ent-sync-transcripts
order: null
output: |
  ## Agent run 2026-10-27T08:32:06

  **Heads-up: the transcripts DB is stale.** Latest row is the 2026-10-05 ENT Sync (https://app.notion.com/p/3f0814686151800bb49fe9a48c5e8f87). There are no rows for Oct 12/19/26, and a Notion search for ENT Sync pages created after Oct 6 found none. Either the meetings weren't recorded or the transcript-capture automation stopped. Also, since Jul 13 the DB properties (Action Items/Decisions/Topics/Attendees/Source Note) are empty on every row; the content lives only in the page body's Notion AI summary.

  ### Oct 5 ENT Sync — action items
  - Tincho: review Ryan's rollout-recipe PR (BW hotel exclusions); flagged it may affect other properties. Ryan reworks per feedback.
  - Lautaro + Andrés: SCIM effort estimate by Wed (Oct 7). BW wants SCIM before their convention (~3 wks out, i.e. ~Oct 26). Decide go/no-go that day or the next. Keep the MVP slim; GDPR question open.
  - Andrea: re-reply to Marriott thread / chase Taylor on SSO cert rotation (cert expired Oct 10; Connor offered to escalate to Brian).
  - Connor: with Daniel + Lautaro, enable Property Insights dashboards for non-enterprise hotels (excl. Wyndham/BW/IHG); test portfolio behaviour first; get a GrowthBook walkthrough; record a video plus an in-app announcement.
  - Connor: intro Andrea to Nathan (PM offer out, enterprise/guest-facing, ex-JetBlue). Ryan suggests the Wyndham Barclays card project as his onboarding.
  - Ryan: schedule a 30-min design review for the Barclays card project.
  - Someone (unassigned): reshare the weekend-incident retro doc in the main channel.
  - Andrés: share the Wyndham OHIP-error fix PR with the PMS Gateway team.
  - Lautaro: reply to Kempinski to finish SSO enablement.
  - Andrea: Eng All Hands slides on config scripts, rollouts and drift detection (week of Oct 12).
  - Team: focused retro on sprint points / Linear workflow.

  ### Decisions / consensus
  - Encode BW hotel exceptions in the rollout recipe instead of relying on tribal knowledge; long term, drift detection should catch this kind of misconfiguration.
  - Sprint points: leadership isn't worried about 30–40+ pt loads (mostly tickets blocked in review/rollout). Don't zero out points mid-sprint.

  ### Other topics
  - Lautaro: finishing the Explo→Omni migration (errors for non-migrated overrides, Notion doc of pending ones).
  - Andrea: IHG script issues (wrong SF ID for a Canadian hotel, unconfigured FreedomPay gateway); onboarding values missing when the core script ran; WhatsApp error fix; ISG core opportunity detection; global hotel list header design.
  - Andrés: Salesforce-data segmentation layer; portfolio-mgmt app PRs with Laura; missed a weekend SLA.
  - Drift-detection UI owner (unnamed) is slightly behind because of the incident; spike ready, UI PR soon.
  - Andrea and Connor out the weekend of Oct 19.

  ### Relevant to you
  Nothing assigned to you. Two items touch your area: the rollout-recipe exclusions and drift detection, both adjacent to ENT-7726 binding rules (plan: ~/.claude/plans/zippy-soaring-metcalfe.md). Worth checking whether the BW-exclusion PR conflicts with the conventions/binding-rules design. Possible follow-up: ask in the ENT channel whether ENT Sync transcripts stopped being captured after Oct 5 (I did not post anything).
project: null
source_id: null
tags: []
time_minutes: 10
title: Check ENT sync transcripts
updated: 2026-10-27 13:22:41.741959
waiting_on: null
waiting_since: null
working_on: false
---

Review the latest ENT sync meeting transcript — action items, decisions, and topics.

https://app.notion.com/p/canarytechnologies/13c93352d06c4e88bb69af559237645c?v=5f62f3dba7234433870e5cfeb927403f&source=copy_link