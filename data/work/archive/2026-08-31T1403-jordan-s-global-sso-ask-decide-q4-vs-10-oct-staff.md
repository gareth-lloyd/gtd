---
area: null
completed_at: 2026-08-31 22:30:53.800738
contexts:
- deep
created: 2026-08-31 14:03:35.058307
defer_until: null
due: null
energy: high
id: 2026-08-31T1403-jordan-s-global-sso-ask-decide-q4-vs-10-oct-staff
order: null
output: ''
project: 2026-08-31-ihg
source_id: null
tags: []
time_minutes: 30
title: Jordan's Global SSO ask — decide Q4 vs 10 Oct Staff App date
updated: 2026-08-31 22:30:53.800731
waiting_on: null
waiting_since: null
working_on: false
---

**Decision needed:** Jordan Sterling's Q4 timeline for global/mobile SSO vs Caitlyn Levine's ~10 Oct hard date for Staff App GA. Forum is Jordan's "Global SSO" invite (Mon 16:30 EEST, with Ricardo Moreira + Lautaro Mena). Both land in ENT-owned tables, so this is your call to make.

## Jordan's ask

The DM is two lines, 26 Aug 08:06, still unanswered:
https://canarytechnologies.slack.com/archives/D07HCMQU5FY/p1787720784110109

> "i think we need to do mobile sso (global sso) in Q4"
> "a lot of this is going to be in tables enterprise owns today"

Not a request for work — a claim on ENT's surface area plus a proposed timeline. Backed two days later by the meeting invite linking his Notion doc.

## The proposition

Notion: "Global Identities & SSO — Immutable Identity, Cross-Region Linking"
https://app.notion.com/p/3ca81468615181fcbc5af1d1a671fc2a

Problem: staff identity is derived from mutable attributes — global `auth-users` keyed `sid = hash(username:email)` — so a rename IS an identity change, cross-region duplicates collide, and SSO is regional end-to-end (`sso.Organization` is a per-region Postgres row; users keyed `(sso_organization, sso_name_id)`). Signing into a second region either fails login or creates a second unrelated account.

Proposed:
- One opaque immutable `au_` identity per person, minted once, never derived from username/email; regional Django users become *profiles* of it.
- `UserProfile.global_identity_sid` as a model default (every creation path mints it, no call-site change); backfilled.
- `auth-users` demoted to a registry `{sid, is_active, timestamps}`, not a user copy; Debezium CDC as sole writer.
- Two new global tables: `identity-credentials` (SAML: org sid + name_id -> `au_`) and `identity-profiles` (sid, region, user_id). `sso.Organization` gains `sso_organization_sid`.
- Staff OAuth tokens keyed by sid, so renames stop invalidating them. Global sign-in page across regions.

## Jordan's own scoping notes (these narrow it sharply)

- "We are NOT globalizing SSO right now. We are just pointing from global to regional. And we are picking whatever region we want."
- Ignore username/email cross-region drift for now.
- Needs a global user-profile table + pointer column from Postgres — the ENT-owned change.
- Open: global *account* table now or later; "pick the first SSO setting"?; SSO completion should return a token, not a cookie; needs GET APIs on SSO objects.

## Unresolved — raise these in the meeting

- No org registry: two regional orgs sharing one `sso_organization_sid` is undefined.
- `is_active` is global by construction, so a regional deactivation locks every profile. He flags this needs product confirmation.
- PII / data residency in the global tables.
- Registry row missing at first token use — read path fails closed.

## The collision

Caitlyn's minimum scope for Staff App GA (globalized user-profile + SSO-settings lookup) is exactly what Jordan describes. Driver is the Best Western Convention on 26 Oct (COO demos Staff App onstage); BWH needs ~2 weeks of real usage across 1,300 properties first, hence ~10 Oct.

Jordan's phase-one framing — point global -> regional, pick any region — is arguably the cheap subset that could serve 10 Oct. **That's the trade to test.**

Also unresolved: Caitlyn's proposed ownership split (UI + email/password fallback to Mobile; global lookup on user-profile/SSO-settings tables to ENT/Identity) needs your ruling before anyone can resource it. Connor deferred to you and said ENT could likely loan an engineer.

## Context

Three large SSO integrations concurrent (Hyatt, IHG, ESA); Hyatt and IHG both hitting auto-merge problems. Lautaro is separately pushing a Self-Service SSO Account Linking PRD; Connor has a prototype up for feedback.