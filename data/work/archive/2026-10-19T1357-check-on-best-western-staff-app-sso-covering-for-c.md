---
area: null
completed_at: 2026-10-21 12:20:29.207933
contexts: []
created: 2026-10-19 13:57:25.112307
defer_until: null
due: 2026-10-20
energy: low
id: 2026-10-19T1357-check-on-best-western-staff-app-sso-covering-for-c
order: 1
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
  ## Agent run 2026-10-20T11:38Z

  > Follow-up asked: "Check status today"

  **Summary:** Good day. Three of the five threads moved: the brand selector PR is out of draft and waiting on a pod-staff-ops review, Diana has seven push-notification PRs up in canary with CI green and Mike has told Ron "enabled for everyone in the next couple days", and Mike and Ishwar both replied to your DM. Two things want you today: Mike asked you a direct question about other brands on mobile at 01:26 EEST, and Ishwar wants a reply to his "who owns BW" answer. No new BW logins since 10/16, and still no Okta log outcome from Jason.

  ### 1. Brand selector, STAFF-304: ready for review, not merged
  - PR #138 left draft on Oct 19 at 19:19 UTC. Reviewer requested is the **Pod: Staff Ops** team only; no reviews yet, decision REVIEW_REQUIRED, CI green (https://github.com/canary-technologies-corp/staff-app-react-native/pull/138). Linear is now **In Review** (https://linear.app/canary-technologies/issue/STAFF-304/staff-app-login-replace-scan-login-qr-with-an-sso-hotel-brand-selector).
  - All three of Diana's questions are closed. Mike replied in her thread: "No Other button for now. Wenjun to send icons (may have already sent). Correct brands" (https://canarytechnologies.slack.com/archives/C0AN8AQ49UG/p1792399469150039).
  - Other path removed in the last commit ("Take the Other email path out of the brand selector"). Diana's Linear comment asks for the Other requirement and acceptance criterion to be re-scoped to a follow-up; nobody has done that yet. Real brand logos landed; she flags the Hyatt asset is the *World of Hyatt* wordmark, not the plain HYATT mark.
  - Nudge: someone in pod-staff-ops (Rafa, James, Ishwar) needs to pick up the review today if this is shipping before 10/26, and it still needs a store build after merge.

  ### 2. BW logins: no new ones since 10/16
  - Snowflake FACT_STAFF_LOGIN_EVENT, best-western, staff app: 10/14: 2, 10/16: 5, nothing 10/17 to 10/20 so far. Same picture as yesterday.
  - Jason's reply to Mike (quoted by Ishwar in the DM): "I've not had any luck getting logs for this user, but I've talked to a few hotels who have been able to log in successfully." So the Okta deny-on-new-device theory is **unconfirmed and unlikely to be confirmed by BW** (https://canarytechnologies.slack.com/archives/C0C9VCZDT9V/p1792425095057999).
  - Mike's read: "possible it was a transient issue. Jason noted he hasn't had any new reports" (https://canarytechnologies.slack.com/archives/C0C9VCZDT9V/p1792444918036709). Ishwar offered to check our logs for misses and push Jason to get hotels testing more; Mike asked "do we have logs on our end?" and Ishwar said he hasn't checked yet. **Nobody has looked at our side yet.** Cheap win: ask Ishwar to pull identity-service / Groundcover logs for failed BW SSO attempts since 10/8.
  - Ownership answered: Ishwar said "Mike and me. Mike is point on comms and I am cc'd" and asked Mike to cc you on replies to Jason (https://canarytechnologies.slack.com/archives/C0C9VCZDT9V/p1792435921974229). You reacted with a prayer emoji; no further reply from you.

  ### 3. Default-on notifications: PRs are up, CI green, no reviews yet
  Diana opened seven canary PRs on Oct 19 and 20. The one that answers Connor's question is STAFF-326:
  - #60664 STAFF-326: stop gating staff pushes on the hotel push flag. Base master, +38/-98, CI green, reviewers Pod: Messaging, Rafa, James, in15. No reviews (https://github.com/canary-technologies-corp/canary/pull/60664). The PR body says the flag is the **guest** opt-in, and four staff send paths were wrongly reading it. That is the whole "staff never got the message" failure.
  - #60686 STAFF-328: hotel slug on every staff push payload, +6/-1, master (https://github.com/canary-technologies-corp/canary/pull/60686)
  - #60680 STAFF-327: drop subscriptions for deregistered devices, master (https://github.com/canary-technologies-corp/canary/pull/60680)
  - #60688 STAFF-329: metrics and log events on the push send path, **stacked on #60664**, +404/-10 (https://github.com/canary-technologies-corp/canary/pull/60688)
  - #60695 STAFF-330: delete duplicate staff subscriptions, master (https://github.com/canary-technologies-corp/canary/pull/60695)
  - #60721 STAFF-332: registration becomes a device handover, stacked on STAFF-330, no reviewers yet (https://github.com/canary-technologies-corp/canary/pull/60721)
  - #60722 STAFF-331: unique device_sid on StaffSubscription, stacked on STAFF-332, **2 CI failures**, no reviewers (https://github.com/canary-technologies-corp/canary/pull/60722)
  - You were not requested on any of them, though you offered on Oct 19. Diana said "PRs are gonna go for review later" in Ron's thread at 00:00 EEST today (https://canarytechnologies.slack.com/archives/C0AN8AQ49UG/p1792435191298319). The minimum set for the conference is #60664 plus #60686.
  - Ron: Jason gave the **green light to enable notifications across all BW hotels**. Mike told him "they're being enabled for everyone, work should be done in the next couple days". Connor's fallback (flip the existing flag for all BW hotels) is no longer needed if #60664 merges this week, but it remains the one-line safety net if review slips.
  - Scope decision settled: Diana asked whether pushes should go only for the selected hotel. James leaned keep-all, Wenjun voted selected-only, **Mike decided keep-all** ("staff are shared across hotels"), and Diana confirmed the payload will carry the hotel slug via #60686 (https://canarytechnologies.slack.com/archives/C0AN8AQ49UG/p1792416405741329). The app-side routing on tap is implied follow-up work; no ticket seen for it.
  - App-side permission prompt PR #137 is still a draft (https://github.com/canary-technologies-corp/staff-app-react-native/pull/137).

  ### 4. BW user list for pre-create: no movement
  - No reply in Connor's SCIM thread since Oct 15 (https://canarytechnologies.slack.com/archives/C0AN8AQ49UG/p1792012676577299?thread_ts=1790966460.472019&cid=C0AN8AQ49UG). No Slack mention of SCIM or a user list from Jason since 10/17. Connor's 1:1 notes list "BW user export / import plan, list of all users" and "SCIM don't rush it, not for conference".
  - With Other cut and the brand selector going in, pre-creation only buys email-first routing for first-timers. Worth one ask to Mike whether Jason ever sent the list, then let it drop if not.

  ### 5. Wyndham and other brands on mobile: Mike is waiting on you
  - You replied Oct 19: "quick config change", same caveats as BW, native SSO is US-only. Mike followed up at 01:26 EEST today: "if we linked to the SSO page on mobile, would it work out of the box or would those other brands (IHG, Hyatt, Marriott) need extra configuration to work on mobile too?" (https://canarytechnologies.slack.com/archives/C0AN8AQ49UG/p1792448760833769). **Unanswered.**
  - Draft answer from the code (not posted): there are two paths. The email-first lookup in `hotels/services/login_lookup.py` only routes to SSO when the org slug is in the `SSO_LOGIN_ALLOW_LIST` setting, so each new brand is one config change there (prod value lives in the k8s config, not checked). The brand-selector path is `/sso/login/<slug>` and, per Diana's PR body, is not gated by that list: it needs only an enabled Organization with issuer, SSO URL and certificate, and JIT-provisions the user. So Wyndham, IHG, Hyatt and Marriott tiles would open their IdP today. The real gating is non-technical: each brand's IdP must be fine with staff signing in from a phone, native SSO is US-only, and we have not tested any org but BW. Recommend keeping tiles for untested brands greyed out until a test login per brand, which is a one-line change in the brand grid config.

  ### Other
  - Mike told Ron notifications are coming; Ron is satisfied. Caitlyn's BW QA meeting happened yesterday; no notes posted in #best-western-mobile-app-project since (channel empty after 10/18).
  - Connor's #epd-enterprise coverage post still has no replies.
  - 1:1 notes (Oct 15) read this time. Relevant lines: BW SSO is "number one thing to focus on next week"; QR code won't be the conference method; selector launches with BW only selectable ("not final design"). The shipped grid makes five brands selectable, which goes beyond that note; see point 5.
  - No Slack, Linear, GitHub or Notion writes were made.
project: 2026-09-08-mobile
source_id: null
tags: []
time_minutes: 10
title: Check on Best Western Staff App SSO (covering for Connor)
updated: 2026-10-21 12:20:29.207928
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