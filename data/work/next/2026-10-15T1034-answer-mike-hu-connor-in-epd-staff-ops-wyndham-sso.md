---
area: null
completed_at: null
contexts:
- react
created: 2026-10-15 10:34:12.347444
defer_until: null
due: 2026-10-15
energy: medium
id: 2026-10-15T1034-answer-mike-hu-connor-in-epd-staff-ops-wyndham-sso
order: null
output: |-
  ## Agent run 2026-10-15T12:52:45.914449

  ### Thread (#epd-staff-ops, 14 Oct, https://canarytechnologies.slack.com/archives/C0AN8AQ49UG/p1792018248856969)
  - Mike: Wyndham is close to testing (~early Nov), so plan Wyndham SSO on the Staff App now. Asks what setup Wyndham needs and whether to open other orgs at the same time (IHG, Belinda's APAC request). Attached Wenjun's concept of an SSO org picker showing major brands, aimed at the BW conference.
  - Connor: if Staff App is enterprise-ready, open it to all SSO orgs. Wants to cover it in your 1:1 today. Asked Mike whether Staff App is GA-ready for enterprise.
  - Mike: the only worry is the open BW SSO login issues. Connor has no concerns either. Belinda cc'd taykirch.
  - You haven't replied.

  ### Answer to "what's needed for Wyndham": mostly config (code verified)
  - The gate is `LoginLookupService.route()` in backend/canary/hotels/services/login_lookup.py:43. It sends a user to SSO only if their `userprofile.sso_organization.slug` is in `settings.SSO_LOGIN_ALLOW_LIST` and the org can run SAML (`is_enabled`, `issuer_id`, `sso_url` and a certificate, lines 67-69).
  - `SSO_LOGIN_ALLOW_LIST` is a JSON env var (canary/settings/base.py:2082). Prod values aren't in the repo. Per James Lovatt it currently holds `bestwestern` (BW Lab), `best-western` (BW Prod) and `canary-sso-test` (https://canarytechnologies.slack.com/archives/C0AN8AQ49UG/p1790159717134059). Adding an org is "1 line of config + a deploy" (James, https://canarytechnologies.slack.com/archives/C0AN8AQ49UG/p1789734467360399).
  - Slugs: `wyndham` (onboarding/services/vendor/wyndham_definitions.py:28), `ihg` (onboarding/configuration_providers/ihg/ihg_remove_hotel_from_parent_brand_provider.py:19), `best-western`.
  - The mobile login path has no BW-specific code. It's generic SP-initiated SAML: `/sso/login/<slug>` with `next` as RelayState, back to the OAuth view, then a redirect to `canarystaff://sso`. The app SID config (`STAFF_APP_APPLICATION_SIDS`) doesn't depend on the org.
  - Nothing new should be needed on Wyndham's IdP, because the ACS URL is unchanged. It does need to support SP-initiated login and preserve RelayState. That's the one thing to test before relying on it. If the IdP drops RelayState, the user lands on web /login, not back in the app.
  - Recent PRs: #55813 (lookup and allow-list), #55814 (skip consent), #57156 (authorize-challenge), #57777 (SSO+password for orgs that allow both), #56878 (username or email).

  ### Caveats for the 1:1
  1. **US region only.** Native-app SSO works only in the US region. IHG APAC needs a global rollout: STAFF-251 (was APAC-144), Backlog, unassigned (https://linear.app/canary-technologies/issue/STAFF-251/roll-out-staff-app-sso-globally). Wyndham is US, so it's fine. IHG is fine only for US hotels.
  2. **First login has to happen on the web.** The lookup only recognises users who already have an SSO-linked profile. Unknown identifiers get the password route. Renan confirmed users must log in on web first, which is why the QR code flow exists. SCIM pre-creation (Andrés) won't make the BW convention (https://canarytechnologies.slack.com/archives/C0AN8AQ49UG/p1791921453850249). This is the real reason for Wenjun's org picker. Connor pushed back on a picker ("we should know based on email"). That only holds once users exist, via a prior web login or SCIM, or with domain-based routing, which doesn't exist today. Worth settling with Connor.
  3. **IHG accepts both SSO and password** (org 347 allows both). #57777 returns SSO_OR_PASSWORD for orgs like this, so allow-listing `ihg` shouldn't lock out password users. It would start offering SSO to IHG users who have SSO profiles.
  4. **Users in more than one allow-listed org get USERNAME_REQUIRED.** This becomes more likely as more orgs are added to the list.
  5. **BW SSO login issues are still open** (https://canarytechnologies.slack.com/archives/C0AN8AQ49UG/p1791917931025909). These are Mike's GA blocker. Ishwar found 3 of 12 iPhone attempts succeeded. Canary logs show no "Cannot Log In" error, so it looks like BW's Okta denying. One user succeeded after first logging into hotelsso.bwhhotelgroup.com in Safari, which suggests BW's Okta denies unknown devices when it should challenge with MFA. Mike is following up with Jason (and Duane, BW's IdP owner). That's a BW-side Okta policy problem, not ours. Check with Wyndham early whether their IdP has device/MFA policies that could hit the same issue.
  6. **Push notifications** are gated per hotel by `Hotel.enable_push_notifications`, independent of SSO (your 30 Sep finding). Wyndham hotels will need it turned on too.

  ### Suggested reply (draft only, NOT sent)
  > For Wyndham it's mostly config: adding the `wyndham` slug to the SSO allow-list plus a deploy, with no BW-specific code in the path. Before we commit to dates I'd check three things: (1) Wyndham's IdP handles SP-initiated login and passes RelayState through, so a quick test login with a Wyndham test user; (2) first-time users still need a prior web login, the QR flow or SCIM, since we only route to SSO users we already know; (3) native SSO is US-only, so IHG APAC depends on STAFF-251. IHG US could be allow-listed at the same time (they keep password login too). Happy to go through it with Connor in our 1:1.

  Nothing was posted to Slack or Linear.

  ## Agent run 2026-10-16T13:24:30

  Merged `2026-10-05T2347-up-to-speed-on-bw-sso` ("up to speed on BW sso", project 2026-04-16T1210-unblock-team, due 2026-10-14, energy low, 5 min, no notes) into this item. It's now in trash/ and can be restored from there.
  - Kept the current title. It already covers BW SSO readiness.
  - The other item had no body, so its title is kept as a line in the body: "Also: get up to speed on BW SSO".
  - Kept this item's own scalars (due 2026-10-15, energy medium, 15 min) and project (2026-09-08-mobile). The other item had no contexts or tags.
project: 2026-09-08-mobile
source_id: https://canarytechnologies.slack.com/archives/C0AN8AQ49UG/p1792018516101899?thread_ts=1792018248.856969&cid=C0AN8AQ49UG
tags:
- morning-gtd
- slack
time_minutes: 15
title: 'read summary: background context including BW SSO in staff app readiness (code)'
updated: 2026-10-16 13:24:30.000000
waiting_on: null
waiting_since: null
working_on: true
---

Mike asks what's needed to set up Wyndham (and maybe IHG) SSO orgs on Staff App mobile; Connor wants to cover it in 1:1 today. Open since yesterday, no reply from me.
https://canarytechnologies.slack.com/archives/C0AN8AQ49UG/p1792018516101899?thread_ts=1792018248.856969&cid=C0AN8AQ49UG

Also: get up to speed on BW SSO (merged from "up to speed on BW sso").