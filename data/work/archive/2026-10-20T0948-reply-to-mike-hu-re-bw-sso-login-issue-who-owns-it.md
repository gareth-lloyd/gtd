---
area: null
completed_at: 2026-10-20 15:59:19.046365
contexts:
- react
created: 2026-10-20 09:48:30.093878
defer_until: null
due: 2026-10-20
energy: low
id: 2026-10-20T0948-reply-to-mike-hu-re-bw-sso-login-issue-who-owns-it
order: 3
output: |
  ## Agent run 2026-10-20 14:53:17.369821

  ### Answer to "who owns it"
  Ishwar already answered in the DM: Mike is point on comms with Jason, Ishwar is cc'd, and Gareth should be cc'd on replies to Jason (https://canarytechnologies.slack.com/archives/C0C9VCZDT9V/p1792435921974229). Connor's handoff note names Gareth as the check-in owner for the BWH SSO sign-in workstream while Connor is OOO (https://canarytechnologies.slack.com/archives/C0AN8AQ49UG/p1792188478260649). So the open question is not ownership but whether Mike's "many logins since 10/08" actually closes the issue. It does not.

  ### Recent logins (Snowflake CANARY_RAW, auth_user last_login CDC history)
  Jason Pitard has three accounts. The SSO-linked one is `bwjasonpitard` (user 3747696, BW SSO org 313), not `bestwesternjasonpitard`:
  - `bwjasonpitard` (3747696): 328 logins since Jan 2026, 36 since 10/01, 15 since 10/08, latest 2026-10-19 20:58 UTC. Logging in daily.
  - `bestwesternjasonpitard` (4137887, org 247, created 2026-06-15): 2 logins ever, none since 10/01.
  - `jason pitard` (3727261, no sso_name_id): 6 logins ever, none since 10/01.

  BW-wide (all users with sso_organization in 247/313): ~2,300 distinct users and ~3,300 logins per weekday, flat from 09/28 through 10/19. No dip at or after 10/08. That is web plus mobile combined, so it is dominated by web. Mike's Omni dashboard observation is consistent with this and says nothing about the staff app on its own. On 10/13 Connor said the same dashboard showed no successful staff-app SSO logins since 10/08 (https://canarytechnologies.slack.com/archives/C0AN8AQ49UG/p1791917931025909). Mike should confirm his chart is filtered to mobile before we call it transient.

  The three users BWH reported with "Cannot Log In" (Mike, 10/13: https://canarytechnologies.slack.com/archives/C0AN8AQ49UG/p1791929992089649):
  - Sharan Bhakta, `bwsharanbhakta` (4214350, name_id C35FC8@bwhhotel.com): 17 logins since 10/08, latest 2026-10-19 13:34 UTC. Working now, but only after the Safari-first workaround Ishwar observed on 10/14 (https://canarytechnologies.slack.com/archives/C0AN8AQ49UG/p1792011110066819).
  - Stephanie Self, active account is `bwstephanieboteler` (3779582, name_id 06E37K@bwhhotel.com): 1 login since 10/08, at 2026-10-19 22:45 UTC. The older `StephanieSelf` account (3564962) is inactive, last login 2025-03-03.
  - Erin Levionnois: the reported email maps only to `ErinLevi` (3644477), inactive since 2025-02-12, sso_name_id null. She has no active BW SSO account under that email, so she would fail on web too. Not a mobile bug.

  Ishwar's 10/13 log read (https://canarytechnologies.slack.com/archives/C0AN8AQ49UG/p1791919878990119): 3 mobile SSO successes vs 9 non-completions, all iPhone. Private-relay theory was weakened by Sharan (no relay, still failed). Current working theory is BWH Okta denying unknown devices instead of challenging. Nobody has disproved it, and Jason has not returned Okta logs for C35FC8 at 2026-10-14 18:10:25 UTC.

  Could not verify: sso_diagnostic_log and sso_organization are not mirrored to Snowflake (not authorized), and the staff-app SSO flow lives in staff-app-react-native, so I could not split mobile from web logins myself. Groundcover's SAML relay-state logs for the last 3h show only web return URLs.

  ### Draft reply to Mike (group DM C0C9VCZDT9V) -- NOT SENT, needs your OK
  > Thanks Mike. One caution on the dashboard: BW does ~2.3k distinct SSO logins a day and that was flat through 10/08, so "many logins since 10/08" is what we'd see even if the staff app were fully broken. Is the Omni chart filtered to staff-app logins? Connor read the same dashboard on 10/13 as "nothing on mobile since 10/8".
  >
  > On the three users Jason sent: Sharan is logging in daily now, but only after the Safari-first workaround Ishwar saw live. Stephanie logged in once last night. Erin's email maps to an account that's been inactive since Feb 2025, so she'd fail on web too and isn't a mobile case.
  >
  > I'd not call it transient yet. Two asks for Jason when you reply (cc me): (1) Okta logs for user C35FC8 at 18:10:25 UTC on 10/14 and whether their policy denies or challenges unknown devices, which is Ishwar's open question; (2) which email Erin actually signs in with on web.

  ### Suggested next steps
  - Ask Mike to confirm the Omni dashboard filter (link in his message: https://canarytechnologies.omniapp.co/dashboards/607fd830).
  - Ask Ishwar to rerun his mobile success/non-completion count for 10/14 to 10/19, since that is the only mobile-specific signal we have.
  - Keep the Okta-logs ask to Jason open; Duane Hebert (duane.hebert@bwh.com) is BWH's IdP contact, via Jason per Connor.

  ## Agent run 2026-10-20 15:08:31.421686 -- Groundcover sweep of BW staff-app SSO, 10/09 to 10/20

  ### How the staff app login is visible in our logs
  The staff app does an SP-initiated SAML flow: GET /sso/login/best-western with next=/login/oauth/?application_sid=app_d4pygdgmfyfhqqjqwyfwv8kkf6yy6f&redirect_uri=canarystaff://sso (PKCE). Log event `sso_login.return_to_link` with return_to containing "canarystaff" is a mobile start; `saml_acs.redirect_to_relay_state` with relay_state containing "canarystaff" is a mobile completion; `oauth_grant.authorization_code_exchanged` is the app getting its token. Web BW logins are all IdP-initiated from hotelsso.bwhhotelgroup.com and never carry a RelayState, so the two are cleanly separable. gcQL used:
  - starts: `event:sso_login.return_to_link return_to:*canarystaff* path:*best-western* | fields _time, ip`
  - completions: `event:saml_acs.redirect_to_relay_state relay_state:*canarystaff* path:*best-western* | fields _time, ip`
  - failures on our side: `CTX_sso_organization_slug:best-western event:saml_acs* -event:saml_acs.saml_response` (24h windows; 5-day windows time out)

  ### Mobile funnel, UTC days (testers on 46.25.77.13 excluded)
  | day | app starts | completed SAML | token exchanged | notes |
  | 10/09-10/11 | 0 | 0 | 0 | |
  | 10/12 | 6 | 0 | 0 | 5 retries in 8 min from Apple Private Relay egress (New Orleans), plus Sharan 50.235.217.146 at 18:23Z |
  | 10/13 | 1 | 0 | 0 | Private Relay egress again (same /52) |
  | 10/14 | 3 | 2 | 2 | 199.59.119.56 ok; Sharan 18:10:25Z no return, 18:14:33Z ok after Safari login |
  | 10/15 | 4 | 0 | 0 | 68.226.154.17 (Cox residential) retried 4x in 8 min, never returned |
  | 10/16 | 5 | 5 | 5 | users 4107276 (hotel 44469), 3785493 (44486), 3767268 (27073), 4235302 (27073), 3986705 (05561) |
  | 10/17-10/18 | 0 | 0 | 0 | |
  | 10/19 | 1 | 0 | 0 | 104.28.191.43 at 19:00:20Z (Cloudflare range, not Private Relay), never returned |
  | 10/20 to 12:40Z | 0 | 0 | 0 | |

  Roughly 12 real-user attempt sessions since 10/12: 7 succeeded, 5 never came back from BWH's IdP. Not transient: the most recent failure is 10/19 19:00 UTC, and 10/15 was a clean 0-for-4.

  ### What fails and where
  - Every failure is the same shape: we redirect the user to BWH's IdP and the IdP never POSTs back to /sso/saml/acs/best-western. Nothing fails on our side. BW SAML errors for the whole 5 days: 2 validation_error, 1 assertion_expired, 7 unknown_sso_hotel_value warnings. No idp_rejected responses for BW (those were IHG and Marriott).
  - The OAuth/PKCE token step is clean for real users: every one of the 7 completions exchanged its code within 1s. The 21 code-exchange misses in the week are all from AWS 2600:1f14 addresses in 7-reason bursts, i.e. an integration test, not users.
  - Private Relay: 6 of 6 starts from Apple Private Relay egress (verified against https://mask-api.icloud.com/egress-ip-ranges.csv) never returned, and 0 of 7 successes used it. So Ishwar's theory holds as a sufficient cause, but Sharan (10/12, 10/14), the Cox user (10/15) and the 10/19 user failed without it. Likely two IdP policies: an Okta network-zone deny for anonymizing proxies, plus the new-device deny Ishwar suspected.
  - Sharan's trace confirms the device theory: first app attempt 18:10:25Z no return; Safari login to hotelsso.bwhhotelgroup.com; second app attempt 18:14:33Z returned in 12s.

  ### Revised draft reply to Mike (group DM C0C9VCZDT9V) -- NOT SENT, needs your OK
  > Thanks Mike. I pulled our logs for the staff app specifically (we can separate app logins from web by the canarystaff:// return URL). Since 10/12 about 12 users have tried SSO in the app: 7 got in, 5 never came back from BWH's IdP. The last failure was yesterday 19:00 UTC, and 10/15 was 0 for 4, so I wouldn't call it transient. The ~2.3k BW logins a day on the dashboard are web and were flat through all of this.
  >
  > Nothing fails on our side. Every failure is the same: we hand off to hotelsso.bwhhotelgroup.com and the IdP never posts back. Two patterns in who fails: (1) every attempt from an iPhone with iCloud Private Relay on (6 of 6, checked against Apple's egress list) never returned, and none of the successes used it; (2) Sharan, and two others, failed without Private Relay, and Sharan's succeeded 4 minutes later once he had a Safari session with the IdP.
  >
  > Asks for Jason/Duane when you reply (cc me): (a) the Okta deny reason for user C35FC8 at 18:10:25 UTC on 10/14; (b) whether their sign-on policy denies anonymizing proxies / Private Relay rather than challenging; (c) whether unknown devices are denied vs MFA-challenged. On the three names Jason sent: Sharan is now logging in daily, Stephanie once last night, and Erin's email maps to an account inactive since Feb 2025 so she'd fail on web too.

  ### Methodology (repro in Groundcover, logs signal, cluster prod-main-us-west-2)
  The staff app logs in via SP-initiated SAML whose `next` URL contains `canarystaff://sso`; web BW logins are IdP-initiated and carry no RelayState, so the two separate cleanly. Count mobile starts with `event:sso_login.return_to_link return_to:*canarystaff* path:*best-western* | fields _time, ip`, completions with `event:saml_acs.redirect_to_relay_state relay_state:*canarystaff* path:*best-western* | fields _time, ip`, and token issuance with `event:oauth_grant.authorization_code_exchanged | fields _time, ip`. Run each as a 24h window; wider windows time out. Exclude internal testers by IP. Match start and completion rows on ip within ~60s; a start with no completion means the IdP never posted back. Check failing IPs against https://mask-api.icloud.com/egress-ip-ranges.csv for Private Relay.

  ## Agent run 2026-10-20 15:52:11.526433 -- Is Mike's Omni dashboard methodology sound?

  I cannot open Omni from here, so this reconstructs the chart from its source: analytics_public.fact_events, created_at in the past 7 days (Mike's link: https://canarytechnologies.omniapp.co/dashboards/607fd830).

  ### What the source table can and cannot show
  - The login event is `HOTEL_STAFF_USER.HotelStaffUser__login`; payload has source, username, sso_name_id, sso_organization_slug. A staff-app SSO login writes two rows a few hundred ms apart: one with source null (from the SAML ACS, web browser sheet) and one with source "mobile_app" (when the app finishes OAuth). `fact_staff_login_event` derives is_staff_app_login from that source. So source = mobile_app is a correct count of successful app logins.
  - Best Western, source = mobile_app, per day: 10/07 1, 10/08 1, 10/09-10/13 0, 10/14 2, 10/15 0, 10/16 5, 10/17-10/20 0. This matches my Groundcover SAML-completion counts day for day, which cross-validates both.
  - Best Western, source null (web): ~3,000 logins / ~2,150 users every weekday, flat.
  - A failed app attempt writes nothing to fact_events. The IdP never posts back, so no login event is ever created. The table has successes only, no denominator.

  ### Verdict
  Mike's conclusion ("many logins after 10/08, possibly transient") is not supported either way:
  - If the chart is filtered to the staff app, "many" is 7 logins on two days (2 on 10/14, 5 on 10/16) and zero on each of the last four days, during which one BW user tried on 10/19 and failed. Connor read the same dashboard on 10/13 as "nothing since 10/8", which is exactly what source = mobile_app shows for 10/09-10/13.
  - If the chart is not filtered by source, it is counting ~3k/day web logins, which were flat through the whole incident and say nothing about the app.
  - Either way the chart cannot show failures, so it cannot distinguish "fixed" from "nobody is trying". Groundcover gives the denominator: since 10/12, 20 app starts from ~12 users, 7 successes, 5 user-sessions that never returned (10/12 x2, 10/13, 10/15, 10/19).

  Usernames behind the 10/16 app successes (all SSO): bwraghuvirchavda (hotel 4145), bwjcstone (129239066), bwchristinemuller (129234267), bwelizibethjohnson (129234267), bwtufugasingh (129273525). 10/14: Sharan (bwsharanbhakta) plus one from 199.59.119.56.

  Suggested line for Mike: "The dashboard counts successful app logins only (source = mobile_app); a failed attempt never creates a login event because BWH's IdP never returns the user to us. It shows 7 successes since 10/08, all on 10/14 and 10/16, and none in the last four days."
  ## Agent run 2026-10-20 22:05:03.116803 -- Private Relay hypothesis: evidence for and against

  Verdict: REJECT "BWH Okta blocks iCloud Private Relay". Relay is incidental; the failing step is the interactive Okta sign-in inside the app's auth sheet on a device with no existing Okta session.

  Method: paired each staff-app SSO start (event sso_login.return_to_link, return_to *canarystaff*) with the app's own call 1s earlier (path /api-gateway/v1/oauth/lookup, event request_started), which carries the device's real IP and user agent because Private Relay only proxies Safari traffic. Then checked Best Western SAML successes (saml_acs.saml_response, path *best-western*) for Apple egress addresses (is_ipv6(ip) per 12h window; Snowflake FACT_EVENTS LIKE on relay prefixes, then verified every hit against mask-api.icloud.com/egress-ip-ranges.csv with python ipaddress).

  Against (decisive):
  - 16 confirmed Private Relay web logins to BW since 10/01 (12 iPhone Safari, 4 Mac Safari, 10 users: bwkoushikkaria x4, bwmeredithrainville x2, bwsachitsharma x2, bwcassandraescobedo, bwyoginbhakta, bwnickwoelk, bwasantigenna, bwrakeshshura, bwchristinenunes, bwjasmincastrosantibanez). Okta accepted all of them.
  - 10/17 04:13Z bwsachitsharma, iPhone iOS 18.7 via relay (Jacksonville egress): SP-initiated /sso/login/best-western -> hotelsso -> ACS success in 6s. Same flow shape as the app.
  - The 6 relay failures (10/12 16:05-16:13Z, 10/13 14:26Z) are ONE device: app calls from 66.210.236.34 (Cox business line, CanaryStaff/41 iOS 18.6) each 1s before the relay-IP browser start. n=1, not 6.
  - 10/19 104.28.191.43 is a tester, not a BW user: it hit best-western, marriott, hyatt, ihg, wyndham within 20s; not on Apple's list.
  - Neither Cox device (66.210.236.34, 68.226.154.17) has any login event since 10/01, web or app; cannot name them from our data.

  For (weak): the one relay user never got in; relay plausibly trips Okta behaviour detection (new IP/geo) for an already-unknown device. Not sufficient on its own.

  Timing of the 7 app successes, start -> SAML return: 10s, 11s, 13s, 18s, 15s, 38s, 7s. Sharan 10/14: app start 18:10:25Z no return; Safari logins to hotelsso at 18:13:16Z and 18:13:45Z; app start 18:14:33Z -> return 18:14:45Z. The app's auth sheet reuses Safari's Okta session; the failure is the interactive Okta login inside the sheet. Failing devices retried 4-6 times within minutes (consistent with an Okta-side stall/error each time, not abandonment).

  hotelsso.bwhhotelgroup.com confirmed Okta (assets from oktacdn.com).

  Next steps to raise confidence:
  1. BWH Okta System Log (Duane via Jason): bwsharanbhakta/C35FC8 10/14 18:10:25-18:14:45Z; unknown users 10/12 16:05-16:14Z from 66.210.236.34 or 2a04:4e41:2e03:3000::/52; 10/15 01:06-01:14Z from 68.226.154.17. Look for policy.evaluate_sign_on DENY, MFA/Okta Verify/FastPass challenge events, or no events at all (= never reached Okta).
  2. Repro on an iPhone with NO Okta session (clear hotelsso cookies in Safari): open the staff app, sign in, screenshot the sheet after credentials. Repeat with Private Relay off. One screenshot resolves this.
  3. Mobile team: does the staff app open the auth session ephemeral (prefersEphemeralWebBrowserSession)? Does Okta Verify / FastPass app-switch work from inside ASWebAuthenticationSession?
  4. Canary side: emit a client diagnostic when the auth sheet is dismissed/cancelled, so failures are visible without pairing IPs by hand.

  Draft reply to Mike updated accordingly; NOT SENT. Item was archived by the user before this run; related live item: data/work/next/2026-10-19T1357-check-on-best-western-staff-app-sso-covering-for-c.md (not modified).

project: 2026-09-08-mobile
source_id: https://canarytechnologies.slack.com/archives/C0C9VCZDT9V/p1792444918036709
tags:
- morning-gtd
- slack
time_minutes: 10
title: 'Reply to Mike Hu re: BW SSO login issue — who owns it on our side'
updated: 2026-10-20 22:05:03.116803
waiting_on: null
waiting_since: null
working_on: false
---

Group DM (Mike, Ishwar). I asked who owns sorting out the BW situation; Mike replied many logins since 10/08, maybe transient, Jason has no new reports. Best Western, key account.
https://canarytechnologies.slack.com/archives/C0C9VCZDT9V/p1792444918036709

Relevant user: bestwesternjasonpitard
sso_name_id: Jason.Pitard@bestwestern.com

Look for recent logins