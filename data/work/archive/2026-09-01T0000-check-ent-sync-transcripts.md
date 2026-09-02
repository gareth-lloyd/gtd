---
area: null
completed_at: 2026-09-02 11:13:03.720241
contexts:
- consume
created: 2026-09-01 00:00:00
defer_until: null
due: null
energy: low
id: 2026-09-01T0000-check-ent-sync-transcripts
order: null
output: |
  ## Agent run 2026-09-01T15:34:46.350443

  Reviewed the ENT Sync Transcripts DB (https://app.notion.com/p/13c93352d06c4e88bb69af559237645c). Latest two entries below.

  ### Latest: ENT Sync — Mon 2026-08-31
  Page: https://app.notion.com/p/3cd814686151803fb6e1c42de0b6de74
  Titled "Engineering Team Standup & Sprint Review". Caveat in the page: *"missed transcribing the first half of the call"* — so this is partial.

  **Decisions**
  - **IHG roles**: proceed with the existing Canary-specific-roles setup for now rather than mapping IHG's own roles. Rationale: IHG has no visibility into Canary roles, and forcing staff to assign both an enterprise role *and* a Canary role would worsen the existing permissioning problem. Hyatt cited as precedent (they created extra roles and mapped them in — not Canary's suggestion). Plan is to gather post-rollout evidence to push IHG toward improvements, given low current engagement.
  - **RaceCards translations**: machine translation is nearly done (all fields). Team will spot-check via a spreadsheet (Lautaro's earlier approach) on Spanish + Portuguese before deciding whether crowd-sourced review is needed.
  - **Sprint pointing**: Mexico and Spain tickets set to 0 or 1 point for now.
  - **Wyndham Messages**: focus Mon/Tue, code ready by Wednesday; then back to drift detection.
  - **Manage analytics page "breakage"**: not a bug — caused by Daniel deleting old dashboards while building the new Property Insights ones.

  **Action items (as captured)**
  - Start a thread on IHG role changes; implement once Taylor Kirchwehm approves.
  - Start a thread on Windows Reminders — confirm with Annie whether to use an exclusion list instead of rolling out to every property.
  - Create a spreadsheet of RaceCards machine translations for team spot-check (ES + PT).
  - Andrea Bradshaw + Connor Swords: decide ownership of the OTA messaging integration work (Wyndham + Best Western) ahead of the September focus.
  - Lautaro Mena: wrap up Omni migration ENT-6650 (in progress) and ENT-6648 (in review); create a small ticket to update dashboard IDs (no logic changes).
  - Lautaro Mena: check the analytics page in Manage, file a Linear ticket if needed.
  - Team: decide when to enable Property Insights dashboards for a subset of customers — Daniel targeting readiness as early as next week.
  - Andrea Bradshaw: prioritize portfolio identifier backfill (overdue), portfolio typing support (selectors/helpers/initial logic), frontend cache store cleanup, plus available for IHG scripting.
  - Raise AMV UI Europe deployment status at Wednesday's sync (blocked on UI Europe deploy; Ani already sent the update to Wyndham; no follow-up email planned).

  **Other topics**
  - OTA messaging: unique OTA property identifiers now received from both Wyndham and Best Western for Expedia and Booking.com. September focus is enabling the integration and extending guest-journey messages to those channels.
  - Andrés Figueira: current-cycle tickets are small rollovers, no blockers; next up is upgrading the segmentation tax stack for winter; a 4-point HotelKey-failure ticket was deliberately scoped larger to allow design exploration on checks/messaging.
  - Team: Ryan Rogers back Tue; you (Gareth) noted as returning to assist with questions and late-stage issues.

  **Relevant to you**
  - No action item is explicitly assigned to you in this transcript. The three unowned "start a thread" items (IHG roles, Windows Reminders, RaceCards translation spreadsheet) have no named owner — worth confirming whether any are yours.
  - Two things to track this week: the Wednesday sync (AMV UI Europe deployment status) and the Property Insights enablement decision.

  ### Previous entry: 2026-08-24
  Page: https://app.notion.com/p/3c681468615180fb8f86d6ed3ea66a4c
  Despite the "ENT Sync Entry" title this is an **IHG Onboarding Sync — Pre-Testing Check-in**, not the weekly ENT sync. Highlights:
  - Registration card country logic is additive — country-specific fields layered on the default card only when missing; watch for duplicate fields (e.g. two "additional guest" controls). UK, Germany, Canada have complete definitions; others pending, so implement the common parts now and handle gaps in follow-ups.
  - Open conflict: Taylor Kirchwehm asked for the Special Request text box to be **removed**, UK spec says it should be **present**. Lautaro's newer ticket leans removal — needed confirmation from Taylor.
  - Hero image working locally after E2E testing; Core/Plus/Add-to-Portfolio plans implemented (Andrea added the portfolio data); journey messages blocked on Lautaro's template-duplication PR merge + Andrea's approval.
  - Wind Creek SSO meeting: consensus to push back/reschedule — nobody blocked.

  ### Housekeeping note
  The DB's structured columns (Attendees, Topics, Action Items, Decisions) are **empty for every row since 2026-07-13** — only that one row is filled in. Content now lives only in the embedded Notion AI meeting note. If the structured view matters (it's what makes this DB queryable/scannable), it needs backfilling or the capture process needs fixing.

  No external writes were made.
project: null
source_id: null
tags: []
time_minutes: 10
title: Check ENT sync transcripts
updated: 2026-09-02 11:13:03.720236
waiting_on: null
waiting_since: null
working_on: false
---

Review the latest ENT sync meeting transcript — action items, decisions, and topics.

https://app.notion.com/p/canarytechnologies/13c93352d06c4e88bb69af559237645c?v=5f62f3dba7234433870e5cfeb927403f&source=copy_link