---
area: null
completed_at: 2026-09-23 16:27:18.438078
contexts: []
created: 2026-09-23 11:18:53.143846
defer_until: null
due: 2026-09-23
energy: low
id: 2026-09-23T1118-get-ready-for-mobile-block-planning-review-team-pr
order: null
output: |
  ## Agent run 2026-09-23T11:45:00+03:00

  ### The meeting
  - **Q3 Block 2 Review: Mobile & Staff Ops** — today 2026-09-23, 17:00–17:45 EEST, Zoom https://canarytechnologies.zoom.us/j/8535381621 (organizer ssawhney; 18 attendees incl. SJ, Blake, Caitlyn Levine, Mike Hu, Diana, James Lovatt, Jason Flax, Eric Mossman, Bree Sullivan, Romi Khanna, Francisco Prieto, Marshall, Wenjun, Connor Swords).
  - Also today 11:00: Diana <> Gareth 1-1 (right before this; good slot to align with Diana on her stance).
  - You asked Zam to add you on 2026-09-16 (https://canarytechnologies.slack.com/archives/D07ULB6QYDU/p1789558248023449) — "Diana is the new eng lead for mobile, and I'm her manager".
  - Format per EPD "Planning in 6-week Blocks" (https://app.notion.com/p/32781468615180dcae20f2147cdc2472): forward-looking only, little/no recap; SJ + Blake review the prioritized project list in the Linear Block Planning View (https://linear.app/canary-technologies/view/block-planning-view-785d612a6154); expectation is ~1–2h prep to make Linear current and "a clear stance on the goals". Bear notes say pods present as "Large build / small build / misc" and SJ comments on whether leads "think about the pod".

  ### Q4 Block A (label `26Q4A`) — Mobile team (MOB) proposed projects
  All 8 created overnight 2026-09-23 ~04:00 UTC (likely Caitlyn), **none have a lead**, none have milestones, most have one-line descriptions:
  | Project | Status | Pri | Dates | Note |
  |---|---|---|---|---|
  | Refine Custom Views (https://linear.app/canary-technologies/project/refine-custom-views-fa381bd4daec) | Implementation | High | Sep 25–Oct 9 | BWH uses custom views; all flows in progress, BLE not started. MOB-1220 says "fully custom UI not viable". |
  | Push Notifications in Staff App (https://linear.app/canary-technologies/project/push-notifications-in-staff-app-dfa08e2dd663) | Ready for Eng | High | Sep 25–Oct 9 | Built but "not working as expected"; investigate + fix. |
  | Add Team Chat to Staff App (https://linear.app/canary-technologies/project/add-team-chat-to-staff-app-1ffe6f80885a) | Product Definition | Med | Sep 25–Oct 16 | DUPLICATES P-MOB-2248 "Staff App: Add Team Chat" (Eng Design, Sep 14–Oct 7) and P-STAFF-1717 "Internal team messaging". Needs dedupe. |
  | Apple Pay / Google Pay in Tipping flow (https://linear.app/canary-technologies/project/add-apple-pay-and-google-pay-to-the-tipping-flow-71585a9e6312) | Product Definition | Med | Oct 9–30 | Wyndham app. Depends on Payments team (P-PAY-2365 GooglePay platform, P-PAY-2301 ApplePay web merchant are both 26Q4A). |
  | Add Loyalty Gifts Page to Check-In SDK (https://linear.app/canary-technologies/project/add-loyalty-gifts-page-to-check-in-sdk-1ca2107af9c9) | Backlog | High | Oct 29–Nov 12 | IHG requested for their ~November SDK pickup. Closest thing to a hard commitment. |
  | Add BLE to the Wyndham SDK (https://linear.app/canary-technologies/project/add-ble-to-the-wyndham-sdk-dbfff7296d85) | Backlog | Med | Oct 16–30 | BLE SDK built; test beyond Salto, add to Wyndham app, physical-lock testing. Overlaps P-MOB-2249 BLE Enhancements (Sep 10–Oct 1, Backlog). |
  | Messaging SDK Enhancements (https://linear.app/canary-technologies/project/messaging-sdk-enhancements-ae9f0be2777c) | Backlog | Med | Oct 16–30 | Attachments + membership-level threads; backend done. |
  | Accessibility Certification (https://linear.app/canary-technologies/project/accesibility-certification-bf6a697c4ffe) | Backlog | Med | Oct 23–Nov 6 | "This supports Accor" — one line only. Bear: Diana note today mentions Accor accessibility cert (Amanda). |

  ### Staff Ops (Mike Hu) proposed projects — shared in #epd-staff-app 2026-09-22
  https://canarytechnologies.slack.com/archives/C0AN8AQ49UG/p1790024401447729 — "still need to be refined and sequenced… I don't expect us to get to all of this. Overarching goal: as many ticketing/housekeeping pilots onboarded in Q4."
  - Mobile logins for staff (https://linear.app/canary-technologies/project/mobile-logins-for-staff-ba106f130da4) — Backlog, Oct 2–Dec 31. OTP/PIN login for back-office staff without work email; SSO brands (BWH, IHG). Diana + James are already doing the email-disambiguation/username fix this week for BWH corporate (Jason Pitard) — see thread https://canarytechnologies.slack.com/archives/C0AN8AQ49UG/p1789564692168629.
  - Housekeeping: Post-MVP (https://linear.app/canary-technologies/project/housekeeping-post-mvp-efda7639335b) — Backlog, Sep 30–Dec 31. Northstar = adopted properties; themes: support pilots (must), expand PMS coverage, AI auto-assign, rushes/traces.
  - Ticketing: Post-MVP (https://linear.app/canary-technologies/project/ticketing-post-mvp-0a7b71833505) — Backlog, Oct 1–Dec 31. Support pilots (must), preventative maintenance, connect messaging/voice/compendium to tickets, AI ticket creation.
  - Not labelled 26Q4A; none have milestones. Members include Diana, James, Sofya (QA), Marshall, Wenjun.

  ### Linear hygiene issues to raise / fix before the call (Linear should be "current")
  - **Q3 Block 2 MOB projects are all stale and unclosed**: Wyndham In-Stay Experience (Testing, target Aug 14, lead Diana); Android Support for Staff App (Implementation, target Aug 31); Best Western SDK Support (Product Definition, target Aug 26); Staff App: Add Housekeeping (Eng Design, target Sep 11); Staff App: Observability & Monitoring (Product Def, target Sep 18); Phase 2 Foundational Services (Backlog, Sep 7–Oct 12); QA: Wyndham Mobile Testing (Testing, Urgent, target Sep 3). Decide: complete, cancel, or roll into a 26Q4A project.
  - Older "Planned" projects with past dates and leads who may no longer own them (Jason Flax ×6, Bree Sullivan ×3, Eric Mossman ×3): Guest App Onboarding Flow, Guest App Core Flows, Lock Provider SDK Deployment, IHG Incode ID Verification (iOS/Android), IHG Wallet Key UI (iOS/Android), Langham messaging ×2. Guest App Release Readiness (Diana, Oct 26–Nov 6) and Guest App: App Store Submission (Bree, Nov 19–Dec 28) fall in/after this block but are not labelled 26Q4A — are they still planned?
  - OpenKey → Canary Key App migration (3 projects, Backlog/Implementation, dates Jun–Dec) — Bear note from Diana today lists "Physical access / OpenKey" as a topic; not in the 26Q4A list.
  - Only 6 MOB issues are in a started state; 2 of them (MOB-10, MOB-108, Jason Flax) untouched since Feb/Apr.
  - No lead on any of the 8 new MOB projects — Diana should probably be lead or delegate explicitly.

  ### Suggested stance / questions for the call
  1. Capacity: 8 MOB projects + 3 Staff Ops projects for ~6 weeks, plus Staff App pilots support (ticketing/housekeeping) and BWH corporate UAT. What is the cutline? Team Chat and Apple/Google Pay look like the obvious deferrals; Loyalty Gifts (IHG, Nov) and Push Notifications (pilot-blocking) look like must-dos.
  2. Who owns the staff app mobile work — MOB or Staff Ops? Team Chat, Push Notifications, Mobile logins, Housekeeping mobile all straddle both teams. Agree one pod per project (Notion rule: "every project belongs to exactly one pod").
  3. Dedupe: Team Chat (P-MOB-2420 vs P-MOB-2248 vs P-STAFF-1717); BLE (P-MOB-2423 vs P-MOB-2249).
  4. Commitments: which of these are in the Commitment Tracker (https://app.notion.com/p/8154c139d3e74c87b2a5d49d0cdef37c)? IHG loyalty gifts SDK (Nov), BWH custom views, Accor accessibility cert, Wyndham tipping.
  5. Observability: staff app has no Sentry (James, 2026-09-16 thread) — P-MOB-2245 Staff App Observability is stale; worth a small-build slot given pilots are starting.
  6. Related context: Atrium ownership discussion (Internal Tools / Security next block) — https://canarytechnologies.slack.com/archives/C0C2LP70Z4N/p1789669058735549.

  ### Not verified
  - Who created the 8 MOB projects (Linear MCP doesn't expose creator); assumed Caitlyn.
  - Whether Jason Flax / Bree / Eric are still on the mobile team; they are on today's invite.
  - Bear search returned snippets only; team/lead attributions there are partial.
project: 2026-09-08-mobile
source_id: null
tags: []
time_minutes: 5
title: get ready for mobile block planning - review team projects
updated: 2026-09-23 16:27:18.438068
waiting_on: null
waiting_since: null
working_on: false
---

Caitlyn shared the MOB board filtered to 26Q4A for the planning session. Her roadmap shortlist (Sep 16 DM): 1 enterprise support IHG/Wyndham/BWH, 2 OpenKey, 3 Custom Views (BWH), 4 Team Chat in Staff App, 5 SDK for Langham; only 1-5 likely fit.
https://canarytechnologies.slack.com/archives/C0C3NCG0LS1/p1790137083925609