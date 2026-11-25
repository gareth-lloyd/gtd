---
area: null
completed_at: 2026-11-24 15:36:19.855546
contexts:
- react
created: 2026-11-24 10:55:42.787048
defer_until: null
due: null
energy: medium
id: 2026-11-24T1055-answer-ani-in-wyndham-mobile-app-project-where-to
order: null
output: |-
  ## Agent run 2026-11-24T15:25:51

  Nothing sent. Draft reply below; no prod queries run.

  ### Finding
  There is no list page, and there cannot be a simple one: the app is default-on per hotel with off switches, not an enabled list.
  - Since MOB-1543/1544 (PRs https://github.com/canary-technologies-corp/canary/pull/64008, https://github.com/canary-technologies-corp/canary/pull/64010) each hotel can have an SDK Configuration row (`sdk_configuration` table; master `enabled` plus per-module flags such as `check_in_enabled`). A hotel with no row has every module on (`sdk/selectors`, `SdkConfigurationSelector.get_enabled_modules`).
  - Check-in shows in the app only when SDK `enabled` and `check_in_enabled` are on (or no row) AND `check_in_configuration.has_check_in_mobile` is true (`sdk/services/sdk_response.py`).
  - The one place a non-engineer can see it is per hotel: Django admin > Hotel > "SDK Configuration" inline (`hotels/admin/hotel.py`). This is what Francisco meant by "feature flags are already in the django admin". No list view or filter exists.
  - Connor's ask (ENT ticket for the flag to flip at go-live) looks already done: MOB-1545 (https://github.com/canary-technologies-corp/canary/pull/64024) makes the go-live plan and Set Live set `enabled`, `check_in_enabled`, `check_out_enabled` and `has_check_in_mobile` to true, and the build turn them off (`onboarding/plans/go_live_plan.py`, `onboarding/services/opportunity_go_live.py`). Worth confirming with Francisco that the Wyndham go-live script ENT runs goes through that path.
  - Backfill for hotels already in onboarding: MOB-1546 (https://github.com/canary-technologies-corp/canary/pull/64051, merged 2026-11-16), command `onetime_disable_sdk_for_not_live_wyndham_hotels`. NOT VERIFIED whether it has been run with `--commit` in prod. Diana's "when we enable the SDK FF" in the thread suggests some part may still be pending; ask Francisco.
  - Diana's real question (which hotels have a required checkbox group) does not need the app list. Query the registration form config of all Wyndham hotels for a required `checkbox_group` element; then narrow by the flags above if wanted. Ani expects a handful. The SDK fix is merged (MOB-1636 iOS https://linear.app/canary-technologies/issue/MOB-1636, MOB-1646 Android https://linear.app/canary-technologies/issue/MOB-1646) but old app builds stay affected.

  ### Draft reply (thread https://canarytechnologies.slack.com/archives/C0A4EN8SJLA/p1795456418061779?thread_ts=1795443631.993749&cid=C0A4EN8SJLA)
  > @Ani no list page, sorry. The app is on by default for every Wyndham hotel on Canary and we switch it off per hotel, so there is no "enabled" list to show. You can see one hotel at a time in Django admin: Hotel > SDK Configuration (blank or all ticked = on), and check-in also needs "has check in mobile" on the check-in configuration. For anything bulk, the SmartSheet of active Wyndhams is a fair proxy for what guests can reach.
  > @Diana you don't need the app list for this. I can query the reg forms of all Wyndham hotels for a required checkbox group and post the slugs, which also catches hotels with no SDK check-ins yet.
  > @Connor I think the go-live flag is already handled: MOB-1545 has the go-live plan / Set Live turn the SDK flags and has_check_in_mobile on, and the build turn them off. @Francisco can you confirm that covers the Wyndham go-live script, and whether the MOB-1546 backfill has been run?

  ### Open for you
  - Send, edit or drop the draft.
  - If you want the required-checkbox-group hotel list, say so and I will run it read-only against prod (needs your OK; card schemas are not in Snowflake).
project: null
source_id: https://canarytechnologies.slack.com/archives/C0A4EN8SJLA/p1795456418061779?thread_ts=1795443631.993749&cid=C0A4EN8SJLA
tags:
- morning-gtd
- slack
time_minutes: 15
title: 'Answer Ani in #wyndham-mobile-app-project: where to see Wyndham app-enabled
  properties'
updated: 2026-11-24 15:36:19.855539
waiting_on: null
waiting_since: null
working_on: false
---

Ani asked me/Andrea/Connor for an easy place to see which Wyndham properties are enabled in the app (SDK check-ins rejected on required checkbox-group fields: wyndham-01051 had 92 rejections last week, plus 50087, 24994). Andrea/Caitlyn replied there is no list (enabled Wyndham-side, ~all US hotels); Connor also wants an ENT ticket for the SDK flag to flip in the Wyndham go-live script. No reply from me.
https://canarytechnologies.slack.com/archives/C0A4EN8SJLA/p1795456418061779?thread_ts=1795443631.993749&cid=C0A4EN8SJLA