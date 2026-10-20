---
area: null
completed_at: null
contexts: []
created: 2026-10-19 13:57:25.112307
defer_until: null
due: null
energy: low
id: 2026-10-19T1357-check-on-best-western-staff-app-sso-covering-for-c
order: null
output: |-
  ## Agent run 2026-10-19T11:06Z

  **Summary:** On track, with two loose ends that need a push today. BW staff-app SSO logins have started again. The brand selector PR is still a draft, and Diana's 3 questions from this morning have no replies. The notifications backend PR isn't up yet. Nobody has replied to your DM to Mike and Ishwar yet.

  ### 1. Brand selector, STAFF-304
  - Linear: In Progress, assigned to Diana (https://linear.app/canary-technologies/issue/STAFF-304/staff-app-login-replace-scan-login-qr-with-an-sso-hotel-brand-selector)
  - PR #138 is still a **draft**, with no reviewers requested. Last commit was Oct 16 13:13 UTC (https://github.com/canary-technologies-corp/staff-app-react-native/pull/138). Not merged.
  - Diana's post this morning (11:44 EEST) has **0 replies** (https://canarytechnologies.slack.com/archives/C0AN8AQ49UG/p1792399469150039). Status of each open question:
    - **"Other" button:** effectively decided already. In the Oct 16 thread, Ishwar proposed cutting it and Mike agreed: "For the conference, I'm good to cut the Other workflow". Mike's reason was that mobile SSO isn't supported for smaller hotels yet, so Other comes after the conference (https://canarytechnologies.slack.com/archives/C0AN8AQ49UG/p1792141184559999). Wenjun hadn't fully agreed, and the ticket still lists Other in its requirements and acceptance criteria. Someone (Mike) needs to tell Diana "cut it" explicitly.
    - **Full-colour brand icons:** waiting on Wenjun. Diana asked on Oct 16 for every brand asset in its enabled state. No reply found.
    - **Brand list** (BW, Wyndham, Marriott, Hyatt, IHG selectable): this matches the ticket. Accor and Hilton are shown greyed out. Diana wants Mike to confirm.
  - Suggested nudge to Mike: confirm the brand list and the Other cut in Diana's thread. If any icons are still missing for the conference, ship monochrome versions.

  ### 2. Are BW logins happening again? **Yes.**
  Source: Snowflake ANALYTICS.ANALYTICS_PUBLIC.FACT_STAFF_LOGIN_EVENT (is_staff_app_login, sso_organization_slug='best-western', data current to 2026-10-19 09:31 UTC):
  - 10/03: 1 · 10/07: 1 · 10/08: 1 · *(none 10/09–10/13)* · **10/14: 2 · 10/16: 5** (each login a distinct user) · none 10/17–10/19 so far (weekend)
  - The 10/14 logins line up with the observed session with Sharan. Ishwar found that a failed app login worked after Sharan first SSO'd in mobile Safari. His theory is that BW's Okta *denies* unknown devices rather than challenging them with MFA. He asked Jason's team to check the Okta logs for user C35FC8 at 18:10:25 UTC (https://canarytechnologies.slack.com/archives/C0AN8AQ49UG/p1791917931025909). Mike said he'd follow up with Jason; Duane (BW IdP) is reachable through Jason. **No outcome from that Okta check appears in the thread yet.** It's worth asking Mike, because a deny-on-new-device policy would hit people at the conference.
  - Omni dashboard: https://canarytechnologies.omniapp.co/dashboards/607fd830

  ### 3. Default-on notifications
  - Diana plans to remove the flag so pushes go to every registered device. On Oct 16 she said the backend changes would be "on review on Monday" (today) (https://canarytechnologies.slack.com/archives/C0AN8AQ49UG/p1792170982022249?thread_ts=1790702092.262039&cid=C0AN8AQ49UG). **No canary PR from Diana is open yet** (checked GitHub at 11:06 UTC). Connor is still enabling the flag per property when Jason asks. His fallback, if this slips, is to enable the existing flag for all BW hotels.
  - Related: the app-side permission prompt, MOB-1345 PR #137, is still a draft (https://github.com/canary-technologies-corp/staff-app-react-native/pull/137).

  ### 4. BW user list for pre-create
  - Connor's plan: Jason sends first name, last name and email for every user with Canary access in their IdP. We pre-create those users on the BWH SSO org as a one-time stand-in for SCIM (https://canarytechnologies.slack.com/archives/C0AN8AQ49UG/p1792012676577299?thread_ts=1790966460.472019&cid=C0AN8AQ49UG). Connor said he was asking Jason for the list. **No reply in the thread says the list has arrived.** SCIM itself is a fast follow after the conference (Andrés).
  - Once STAFF-304 ships, the brand selector covers first-time users without pre-creation. Pre-creation would still let email-first login route to SSO.

  ### 5. Wyndham SSO on mobile (Mike's ask)
  - Mike's thread from Oct 15 (https://canarytechnologies.slack.com/archives/C0AN8AQ49UG/p1792018248856969) asks what Wyndham needs set up, and whether to open other orgs (IHG, Belinda's request) at the same time. Connor's view: open it to any SSO org once the staff app is enterprise-ready. Mike's only worry was BW login issues. Connor wanted to discuss it with you in the Oct 15 1:1. **No answer to Mike's "what needs to be set up" question appears in the thread yet.** The only SSO org with staff-app logins so far is best-western (apart from canary-sso-test). You still owe this answer, and the brand selector already includes a Wyndham tile.

  ### Other
  - Connor's handoff post has no replies (https://canarytechnologies.slack.com/archives/C0AN8AQ49UG/p1792188478260649). Your DM to Mike and Ishwar has no replies yet (https://canarytechnologies.slack.com/archives/C0C9VCZDT9V/p1792405900187209).
  - BW QA meeting is today at 12:30 ET. Caitlyn, Martin, Ron and Jessica are attending, and Caitlyn's question list is at https://app.notion.com/p/canarytechnologies/BWH-Check-In-Demo-3f281468615180f186cbfcb2130c4f91 (https://canarytechnologies.slack.com/archives/C0AQLLSLGH0/p1792160345033309?thread_ts=1792002411.095509&cid=C0AQLLSLGH0).
  - Not read: the Connor/Gareth 1:1 Notion notes.
  - No Slack, Linear or GitHub writes were made.
project: null
source_id: null
tags: []
time_minutes: 10
title: Check on Best Western Staff App SSO (covering for Connor)
updated: 2026-10-19 14:49:44.354824
waiting_on: null
waiting_since: null
working_on: false
---

Connor's #1 focus for the week. Point people are Mike Hu and Ishwar; the convention is 10/26 in Phoenix. Ron and Jessica are the route to Jason.

Check:
- Has Diana's brand-selector PR (STAFF-304) gone up for review and merged? Open questions: the "Other" button, brand icons, and the brand list.
- Are BW logins happening again? There were none after 10/8, and Jason has connected us to properties to observe logins.
- Default-on notifications change: timing (Connor asked Diana on Oct 16).
- BW user list for the pre-create/import plan. SCIM is not for the conference.
- Mike asked about Wyndham SSO on mobile for early-November testing.

Links:
- Connor's handoff to me (#epd-staff-ops): https://canarytechnologies.slack.com/archives/C0AN8AQ49UG/p1792188478260649
- Diana's brand selector, Oct 19: https://canarytechnologies.slack.com/archives/C0AN8AQ49UG/p1792399469150039
- STAFF-304: https://linear.app/canary-technologies/issue/STAFF-304/staff-app-login-replace-scan-login-qr-with-an-sso-hotel-brand-selector
- Notifications thread: https://canarytechnologies.slack.com/archives/C0AN8AQ49UG/p1792170982022249?thread_ts=1790702092.262039&cid=C0AN8AQ49UG
- My check-in DM to Mike and Ishwar: https://canarytechnologies.slack.com/archives/C0C9VCZDT9V/p1792405900187209
- BW mobile app project thread: https://canarytechnologies.slack.com/archives/C0AQLLSLGH0/p1792160345033309?thread_ts=1792002411.095509&cid=C0AQLLSLGH0
Connor's coverage post (#epd-enterprise, Oct 15): https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1792086541978799
Connor <> Gareth 1:1 notes (Oct 15): https://app.notion.com/p/canarytechnologies/Connor-Gareth-1ae8146861518002b563c3fc97fca9f3