---
area: null
completed_at: 2026-11-19 18:31:45.224301
contexts:
- react
created: 2026-11-18 11:11:54.453525
defer_until: null
due: null
energy: medium
id: 2026-11-18T1111-answer-montse-in-worldhotels-approve-cs-permission
order: null
output: |
  ## Agent run 2026-11-18T12:33 (nothing sent, no code changed)

  Thread: https://canarytechnologies.slack.com/archives/C07BX379GQK/p1794940847103919?thread_ts=1794238334.673929&cid=C07BX379GQK

  ### Recommendation
  Do not approve a CS-wide permission change. Keep the gateway configs with Integrations (Ted is already
  doing Auburndale), and if that becomes a bottleneck for the Thanksgiving (Nov 26) push, add Jessica to the
  csa-integrations Google group instead.

  ### Why
  - The ask is bigger than "add the missing Shift4 section". In code, the CS group has NO payment gateway
    grants at all: `_CS_PERMISSION_SET_MODEL_GRANTS` (backend/canary/canary_staff/services/canary_staff_service.py:100-357)
    contains no `payment_gateways.*` entry. Only Integrations / CSA Integrations (lines 860-951, incl.
    `shift4config` at 925) and Support (`gatewayconfig` view+change only, line 1171) have any.
  - So whatever lets Jessica open Add Gateway Config and see some vendor sections does not come from the CS
    set. Likely leftover per-user permissions: the sync only ever adds (`user_permissions.add`, line 1402),
    never removes, and it preserves non-Google Django groups (line 1378). NOT verified: I did not read prod.
    Joshua's "drift" guess fits, but it is drift on her user, not a gap in the CS spec.
  - "Fixing" it in code therefore means newly granting all of CS add/change on `gatewayconfig` plus
    `shift4config` (and `freedompayconfig`, since HotelKey takes either). That lets every CSM create and
    repoint tokenizing/charging gateways for any hotel. That is the kind of change the "notify Blake first"
    comment is there for.
  - Permission is not what blocks Auburndale today. The blocker is the Shift4 auth token: the one supplied
    had expired, HotelKey says they cannot generate a new one, and Ted replied (Nov 17) with the property
    guide showing they can issue one for Canary as vendor without disruption. Jessica already agreed
    (Nov 16) to route the config through Integrations.
  - csa-integrations already exists for this: it maps to the full Integrations permission set (line 1242).
    Per person, no code change or deploy, reversible. Downside: it is the whole Integrations set, much
    broader than Shift4.

  ### Draft reply (in thread, to Montse) — not sent
  > Thanks Montse. I'd rather not widen CS permissions for this one. CS doesn't have any payment gateway
  > config access in the permission spec today (only Integrations and CSA Integrations do), so this would be
  > a new grant for all of CS to create and repoint gateways, not just a missing Shift4 section. I'd want
  > Blake in on that.
  > For the WorldHotels push: Ted is already setting up Auburndale, and the blocker there is the Shift4
  > token, not access. Let's keep the configs going through Integrations. If that turns into a bottleneck
  > for the rest of the sites, adding Jessica to csa-integrations gets her the access without a code change.
  > Happy to OK that if Ted and Josh are fine with it.

  ### Other things noticed
  - Jessica pasted the Shift4 auth token in the channel (reply 19, Nov 16). Ted says it had already
    expired, so low risk, but credentials should not go in Slack for the remaining sites.
  - If you do want the code change instead: add `payment_gateways.gatewayconfig`, `gatewayconfigtag`,
    `shift4config`, `freedompayconfig` (view/change/add) to `_CS_PERMISSION_SET_MODEL_GRANTS`. Granted
    permission pks are cached 24h per group (line 1355) and apply at next login sync.
  - To confirm where Jessica's current access comes from, check her user's direct permissions and groups
    in prod canary-admin (auth.user) — I did not query prod.
project: null
source_id: https://canarytechnologies.slack.com/archives/C07BX379GQK/p1794940847103919?thread_ts=1794238334.673929&cid=C07BX379GQK
tags:
- morning-gtd
- slack
time_minutes: 15
title: 'Answer Montse in #worldhotels: approve CS permission for Shift4 gateway config?'
updated: 2026-11-19 18:31:45.224282
waiting_on: null
waiting_since: null
working_on: false
---

Jessica Cervantes can't see the Shift4 section on Add Gateway Config (BW Auburndale 10352, WorldHotels HotelKey payment setup, target: all WH auths sites by Thanksgiving). Montse: Blake usually signs off permission changes, but in his absence my OK might be enough. Open 1 day, no reply from me.
https://canarytechnologies.slack.com/archives/C07BX379GQK/p1794940847103919?thread_ts=1794238334.673929&cid=C07BX379GQK