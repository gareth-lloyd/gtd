---
area: null
completed_at: 2026-09-01 15:13:04.743065
contexts:
- react
created: 2026-09-01 11:53:02.853659
defer_until: null
due: null
energy: medium
id: 2026-09-01T1153-reply-to-ramiro-re-support-access-grant-levels-and
order: null
output: |
  ## Agent run 2026-09-01 14:50:58.628975

  **Verdict: I agree with you, and the evidence backs it.** Ramiro's own diff and PR body
  undercut his own "let's not rush it" framing. Three load-bearing points, all verified
  against `origin/master`:

  ### 1. The interim does not unblock the actual ask
  The doc's concrete CS/IM need is PMS registration-card field mapping. That is gated on
  `Permission.CHECK_IN_HAS_REGISTRATION_CARD_SETTINGS_ACCESS`, which appears in exactly one
  role - `PROPERTY_MANAGER` (`backend/canary/permissions/constants/default_role.py:92` on
  master). `CANARY_SUPPORT` carries only `CHECK_IN_HAS_ADVANCED_CONFIGURATION_ACCESS`
  (`default_role.py:143`). Ramiro states this himself under "What the narrow grant gives
  up". So the narrow reason reaches flow config and stops short of the named requirement.

  ### 2. The "hard and slow" mechanism is the dict he already wrote
  `_DEFAULT_ROLE_BY_REASON` in his diff *is* the type -> roles map from the design doc,
  keyed on `reason` instead of a `grant_type` field. `DECISION_TTL` / `ACCESS_TTL` are
  module constants ten lines above it and become a per-type lookup identically. Permissions
  + lifetime - the two biggest levers in the doc - are constants in code, same diff size,
  same single migration. His spike is the proof the mechanism is cheap.

  ### 3. Keying behaviour on `reason` has a real later cost
  Confirmed on master: `reason` drives nothing today. Every non-test reference is display
  or validation - Slack DM label (`support_access_grant_slack.py:180,273`), admin
  (`admin.py:169`), API echo + `Reason.values` membership check
  (`views/support_access_grant.py:78,160`). Steph's Notion comment (2026-08-20) says keep
  it that way: "reason is a way to provide additional context to the approver."
  Making it load-bearing means the requester self-selects their permission level by picking
  a label, with no server-side tie to need; and a second migration + backfill to unpick when
  `grant_type` lands.

  ### 4. His worry is already answered by the doc's own sequencing
  Steph's "Breaking out the work" section ships the mechanism with a **default type carrying
  today's exact behaviour** (PM, 24h, 3-day window, two-person rule on). Every existing grant
  maps to it, nothing changes on deploy. So engineering lands ahead of the product answers.
  The one genuinely blocking answer - what the check-in type can do - blocks his interim
  equally hard.

  ### Where Ramiro is right (concede these, they are free wins)
  - **AD-8308**: `defaultRole.canary_support` is missing from every adminland locale file, so
    hotel staff would see a raw i18n key in their user list. Shipped bug, fix now.
  - **`delete_update_role.py`** does not reject internal roles server-side. Also already
    shipped; the doc already says it should not sequence behind this design.
  - His permission-gate verification (why composing `PROPERTY_STAFF` is wrong: it would add
    `MESSAGES_CAN_MESSAGE_INDIVIDUAL_GUEST` + `TEAM_CHAT_HAS_PRODUCT_ACCESS`, letting a
    support user message real guests and read internal team chat) is the best answer anyone
    has produced to the one blocking product question. **Lift it into the doc.**
  - Note the invariant in `permissions/tests/test_default_roles.py` asserts
    `DEFAULT_ROLE_PERMISSIONS[CANARY_SUPPORT] == PERMISSIONS_BY_STRENGTH[CANARY_ONLY]`
    exactly - so "widening it is three lines plus one test assertion" also erodes that
    invariant's meaning. Worth naming if he pushes.

  ### Fallback if check-in V3 truly cannot wait
  Do the interim on a `grant_type` field with two values from day one, not on `reason`.
  Same size PR, nothing to unpick later.

  ---

  ## Draft Slack reply (NOT SENT - needs your approval)

  Destination: thread reply to rami in #C0A0S3SLDC5,
  https://canarytechnologies.slack.com/archives/C0A0S3SLDC5/p1788207716014489

  > Thanks for digging in properly - the verification work in the spike is the valuable part
  > and I want it either way. But I don't think the interim buys what it is meant to buy, and
  > I don't think the thing you are worried about is as expensive as it looks.
  >
  > *The interim does not unblock the actual ask.* The concrete need in the doc is PMS
  > registration-card field mapping. That is gated on
  > `CHECK_IN_HAS_REGISTRATION_CARD_SETTINGS_ACCESS`, which lives only on `PROPERTY_MANAGER` -
  > your own PR says so. So the narrow grant gets a support user into flow config and stops
  > short of the thing CS actually asked for. If they still need PM for the mapping, we have
  > shipped a reason nobody picks.
  >
  > *The mechanism is the dict you already wrote.* `_DEFAULT_ROLE_BY_REASON` is the
  > type -> roles map from the doc; you keyed it on `reason` instead of a `grant_type` field.
  > `DECISION_TTL` / `ACCESS_TTL` sit ten lines above it and become a per-type lookup the same
  > way. That is the whole permissions-and-lifetime lever, it is constants in code, and it is
  > the same size and the same one migration as your diff.
  >
  > *Keying it on `reason` costs us later.* Today `reason` drives nothing - it is approver
  > context, and Steph's comment says keep it that way. Make it load-bearing and (a) the
  > requester picks their own permission level by picking a label, with no server-side tie to
  > what they need, (b) we take a second migration and a backfill to unpick it when
  > `grant_type` lands, (c) the next narrowed reason that wants a different TTL or approver
  > pool sends us back to building `grant_type` anyway.
  >
  > *Your worry is already handled by the sequencing.* Steph's breakdown ships the mechanism
  > with a default type carrying today's exact behaviour - PM, 24h, 3-day window, two-person
  > rule on. Every existing grant maps to it, nothing changes on deploy. We are not rushing
  > the role definitions: we build the levers and wait on exactly one product answer, what the
  > check-in type can do. That answer blocks your interim just as hard.
  >
  > Where you are straight-up right, and I would take now regardless:
  > • AD-8308 - `defaultRole.canary_support` missing from the adminland locales, so hotel staff
  > see a raw i18n key. Real bug in shipped code.
  > • `delete_update_role.py` not rejecting internal roles server-side. Also shipped, also
  > should not wait for this design.
  > • Your permission-gate analysis is the best answer we have to the one blocking product
  > question. Can we lift it into the doc as the proposed permission set for the check-in type?
  >
  > And if check-in V3 genuinely cannot wait - give me the date and I will fold - then let's do
  > the interim on `grant_type` with two values from day one rather than on `reason`. Same size
  > PR, nothing to unpick.

  ### Links
  - Slack thread: https://canarytechnologies.slack.com/archives/C0A0S3SLDC5/p1788207716014489
  - PR #54887: https://github.com/canary-technologies-corp/canary/pull/54887
  - TOOL-542: https://linear.app/canary-technologies/issue/TOOL-542/eng-design-support-access-grant-types
  - Notion doc: https://app.notion.com/p/canarytechnologies/Different-levels-of-Support-Access-Grant-3b48146861518198ac27c246cb4baf07

  ---

  ## Agent run 2026-09-01 14:54:24.144328 - revised draft (kinder, shorter)

  Supersedes the draft above. Same destination: thread reply to rami in #C0A0S3SLDC5,
  https://canarytechnologies.slack.com/archives/C0A0S3SLDC5/p1788207716014489
  NOT SENT - needs approval.

  > Hey - thanks for reading it properly and actually building something, that's the most
  > useful kind of pushback. And you're right that we shouldn't rush the role definitions.
  >
  > Two things pull me toward going straight at the mechanism though.
  >
  > First, I'm not sure the narrow grant reaches what CS is asking for. The concrete need in
  > the doc is the PMS registration-card field mapping, and that's gated on
  > `CHECK_IN_HAS_REGISTRATION_CARD_SETTINGS_ACCESS`, which only `PROPERTY_MANAGER` carries -
  > you flagged this yourself in the PR. So we might ship a reason people try once and then
  > fall back to a normal PM grant anyway.
  >
  > Second, your PR is what convinced me the mechanism is smaller than it looks.
  > `_DEFAULT_ROLE_BY_REASON` is essentially the type -> roles map from the doc, just keyed on
  > `reason`. The TTLs are constants ten lines up and go the same way. That's most of it, in
  > code, one migration. The bit I'd rather avoid is making `reason` load-bearing, since we'd
  > have to unpick it when `grant_type` lands.
  >
  > On the rushing worry - Steph's breakdown has the mechanism shipping with a default type
  > that is exactly today's behaviour (PM, 24h, two-person rule), so every existing grant maps
  > to it and nothing changes on deploy. We'd build the levers and still wait on the one
  > product answer, what the check-in type can actually do. Your version needs that answer too.
  >
  > The things you found I'd take regardless: AD-8308 (hotel staff seeing
  > `defaultRole.canary_support` as a raw key) and `delete_update_role.py` not rejecting
  > internal roles server-side are both live bugs. And your permission-gate analysis is
  > genuinely the best answer we have to the blocking product question - can we put it in the
  > doc as the proposed permission set for the check-in type?
  >
  > And if check-in V3 can't wait, say the word and I'll fold - I'd just key the interim on
  > `grant_type` from day one so there's nothing to unpick later.

  ---

  ## Agent run 2026-09-01 15:01:32.965779 - re-emphasised draft (CURRENT)

  Supersedes both drafts above. Re-weighted per Gareth: lead on "new permissions are not
  going on PROPERTY_MANAGER", then make the case for grant_type alongside reason.
  Destination: thread reply to rami in #C0A0S3SLDC5,
  https://canarytechnologies.slack.com/archives/C0A0S3SLDC5/p1788207716014489
  NOT SENT - needs approval.

  > Hey - thanks for reading it properly and building something to argue with, that's the most
  > useful kind of pushback.
  >
  > I think the thing that decides it is this: the new check-in capabilities are deliberately
  > not going on the Property Manager default role. That isn't just a preference in the doc,
  > it's already shipped - `CHECK_IN_HAS_ADVANCED_CONFIGURATION_ACCESS` is
  > `PermissionStrength.CANARY_ONLY`, it lives only on `CANARY_SUPPORT`, and
  > `test_default_roles.py` asserts that no hotel-facing role can hold a `CANARY_ONLY`
  > permission. So a grant that hardcodes `PROPERTY_MANAGER` structurally cannot confer any of
  > them, now or later. Deriving the role from something on the grant isn't a refactor we're
  > choosing, it's forced by that decision - and your PR is exactly that derivation. Which is
  > why I don't think it's the big scary piece: it's the dict you already wrote.
  >
  > And it'll keep happening. The registration-card field mapping is a PM permission today;
  > the moment CS needs it without the rest of PM, it becomes another internal permission, and
  > again the hardcoded grant can't reach it.
  >
  > On `reason` vs `grant_type` - I'd keep both, because they answer different questions:
  > • `reason` is *why* the requester wants access. Approver context, human, will accrete over
  > time as CS meets new situations, cheap to add.
  > • `grant_type` is *what* the grant confers - permissions, TTL, approval path. A security
  > control: small, closed, reviewed when it changes.
  >
  > They aren't 1:1 either - `no_property_manager` and `new_product_onboarding` both want the
  > full PM grant. If we merge them, every new reason CS wants becomes a permissions change,
  > and "what could this grant do?" is only answerable by knowing what the map said on the day.
  > Steph's comment says keep `reason` and grow the options, which I agree with - I just don't
  > want it carrying the permissions as well.
  >
  > On the rushing worry: the mechanism ships with a default type that is exactly today's
  > behaviour, so every existing grant maps to it and nothing changes on deploy. We build the
  > levers and still wait on the one product answer, what the check-in type can actually do -
  > which your version needs too.
  >
  > Things you found that I'd take regardless: AD-8308, and `delete_update_role.py` not
  > rejecting internal roles server-side - both live bugs. And your permission-gate analysis is
  > the best answer we have to that blocking question. Can we lift it into the doc as the
  > proposed permission set for the check-in type?
  >
  > If check-in V3 can't wait, say so and I'll fold - I'd just key it on `grant_type` from day
  > one so there's nothing to unpick later.

  ---

  ## Agent run 2026-09-01 15:04:16.952290 - short draft (CURRENT, on clipboard)

  Supersedes all drafts above. Half length, same two emphases.
  Destination: thread reply to rami in #C0A0S3SLDC5,
  https://canarytechnologies.slack.com/archives/C0A0S3SLDC5/p1788207716014489
  NOT SENT - needs approval. Copied to clipboard 2026-09-01.

  > Thanks for reading it properly and building something to argue with - most useful kind of pushback.
  >
  > The thing that decides it for me: the new check-in capabilities are deliberately not going on Property Manager, and that's already shipped - `CHECK_IN_HAS_ADVANCED_CONFIGURATION_ACCESS` is `CANARY_ONLY`, lives only on `CANARY_SUPPORT`, and `test_default_roles.py` asserts no hotel-facing role can hold a `CANARY_ONLY` permission. So a grant hardcoding `PROPERTY_MANAGER` structurally can't confer any of them, now or later. Deriving the role from the grant isn't a refactor we're choosing, it's forced - and your PR is that derivation. Which is why I don't think it's the scary piece: it's the dict you already wrote.
  >
  > On `reason` vs `grant_type`, I'd keep both - they answer different questions. `reason` is why the requester wants access: approver context, human, accretes as CS meets new situations. `grant_type` is what the grant confers: permissions, TTL, approval path - small, closed, reviewed when it changes. They're not 1:1 either; `no_property_manager` and `new_product_onboarding` both want the full PM grant. Merge them and every new reason becomes a permissions change.
  >
  > The mechanism ships with a default type that's exactly today's behaviour, so nothing changes on deploy - we're not rushing the role definitions, we're waiting on the same one product answer your version needs.
  >
  > AD-8308 and `delete_update_role.py` I'd take now regardless. And can we lift your permission-gate analysis into the doc as the proposed permission set? If check-in V3 can't wait, say so and I'll fold.
project: null
source_id: https://canarytechnologies.slack.com/archives/C0A0S3SLDC5/p1788207716014489
tags:
- morning-gtd
- slack
time_minutes: 20
title: 'Reply to Ramiro re: Support Access Grant levels and draft PR #54887'
updated: 2026-09-01 15:13:04.743056
waiting_on: null
waiting_since: null
working_on: false
---

Ramiro read the 'Different levels of Support Access Grant' Notion doc and disagrees with the approach: proposes a narrow new SAG reason granting DefaultPropertyRole.CANARY_SUPPORT to unblock check-in v3 setup on live hotels, rather than rushing a full replacement of the hardcoded Property Manager grant. Asks 'Wdyt?'. Draft PR: https://github.com/canary-technologies-corp/canary/pull/54887
https://canarytechnologies.slack.com/archives/C0A0S3SLDC5/p1788207716014489

https://app.notion.com/p/canarytechnologies/Different-levels-of-Support-Access-Grant-3b48146861518198ac27c246cb4baf07

My view: he's over thinking. The changes are simple and easy to manage as constants in code. If you agree, back me up.