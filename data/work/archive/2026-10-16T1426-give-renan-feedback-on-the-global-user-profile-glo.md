---
area: null
completed_at: 2026-10-16 15:42:35.714733
contexts:
- deep
created: 2026-10-16 14:26:49.295338
defer_until: null
due: 2026-10-16
energy: high
id: 2026-10-16T1426-give-renan-feedback-on-the-global-user-profile-glo
order: null
output: |
  ## Agent run 2026-10-16T14:45
  Read the doc (https://app.notion.com/p/canarytechnologies/Global-User-Profile-Global-SSO-3f381468615180939704fd689cd53eb0, last edited Oct 14) and all 13 open comments. Andrea Bradshaw left 5 (wording, user-side problem framing, portfolio regionality). Jsterling left 8, and they are substantive. Renan's ask: https://canarytechnologies.slack.com/archives/D09S6HC42H0/p1792079314491039 (no replies yet). NOTHING POSTED. The draft below is for you to edit and send.

  Code facts checked (backend/canary):
  - `UserProfile.uuid` already exists (hotels/models, `UUIDField(default=uuid4, unique=True)`). This backs jsterling's point that a model-default sid would just be a second regional id.
  - `sso_name_id` can be edited in admin and in hotels/forms/forms.py:528. `sso.Organization.name_id_format` allows emailAddress, unspecified and transient. So the SAML "subject" is not guaranteed to be stable.

  ### Draft Slack reply to Renan
  Hey Renan, read it plus the comments. The direction is right: an opaque sid, no PII in global tables, resolve to regional Postgres. Jsterling's comments already push on the biggest decision. Here's what I'd add, roughly in priority order:

  1. **Settle when the sid is minted, then rewrite Proposed Solution around it.** The doc says "model default on every create path". Jsterling says "assign on global lookup, SSO only". Those are different designs. I'd go with jsterling's, plus one rule: login never waits on the global write. Keep the sid nullable. JIT creates the regional profile, then the profile is linked to a sid (found or minted). If identity-service or replication is slow, the person still logs in and we reconcile async. That takes the SPOF-vs-collision trade-off off the login path. A single writer region for *new* credential claims becomes acceptable, because an outage only delays linking.

  2. **One merge mechanism for both duplicate sources.** You get duplicates from replication races, which are rare (the same subject's first login in two regions within ~2s). You also get them from existing cross-region accounts at backfill, which are common, e.g. Best Western. The doc lists "one sid per person at backfill" as an alternative with no verdict. Whatever you pick, existing dupes need the same merge as race dupes. On jsterling's "latest write wins, rewrite Postgres": rewriting the sid recreates the rename bug, because tokens and grants minted against the losing sid stop resolving. Suggest the losing sid becomes an alias (`status=merged`, `merged_into=<winner>`) and resolution follows it. That gives the `status` column a real job.

  3. **Check that the first release actually fixes Best Western.** BW has two IdPs (US and EU). Linking keys on `(sso_organization_sid, subject)`, so the two BW orgs only share a credential space if we deliberately give them the same `sso_organization_sid` and both IdPs send the same subject for a person. With persistent or transient NameIDs that usually isn't true across IdPs. Worth confirming BW's NameID format and whether subjects match. If they don't, the headline demand isn't met by "link on arrival" and needs an explicit merge rule (admin action, or matching on a verified attribute).

  4. **The subject is mutable too.** `sso_name_id` can be edited in admin, and email-format NameIDs change when the email changes. A rename at the IdP then misses the credential, mints a new sid, and creates a duplicate. That's the rename problem again, one layer down. The credential table needs an "update the credential for sid X" path, and the doc should say what happens on a miss for a user who already has a regional profile with a sid. (Re jsterling's "1 credential per profile": fine for v1, but IdP migrations and SSO+email users argue for not baking 1:1 into the key.)

  5. **Security section, top risk: cross-customer linking.** Linking trusts `sso_organization_sid`. If two different customers' orgs ever share that value through an admin mistake or a bad backfill, one customer's IdP can log into another customer's user. Assigning it should be a controlled, audited operation, ideally checked against IdP entity ID or issuer. Also spell out deprovisioning. A sid token resolves in any region with a profile, so deactivation has to be checked per regional profile (`is_active`) on every resolution, and the doc should say whether deactivating in one region does anything to the others.

  6. **Say explicitly that authorization stays regional.** Hotel memberships, permissions and portfolio grants stay on the regional user. A global identity is not global access. That answers Andrea's portfolio thread for this project and keeps portfolio regionality out of scope (jsterling's `portfolio_identifier` → global table idea is a separate project).

  7. **Scope and structure:**
     - Fill in Out of scope: cross-region sessions and property switching, email/password users, portfolio regionality, auth-users retirement timing.
     - Drop the "One sign-in, every property" goal, as jsterling said.
     - Fine to drop `user-profile-regions` for v1 if nothing reads it yet, but call it deferred, not unnecessary (see #8).
     - Fill in Vocabulary. "Profile" means both the regional `UserProfile` model and the global user-profile identity, and naming is wobbling (`global_identity_sid` vs `global_profile_sid`).
     - Give each Alternative a one-line "rejected because".

  8. **Spell out a cross-region request, end to end.** As I read it: a bearer token points at identity `{user_profile, S1}`; the edge routes by hotel slug; identity-service in that region signs a token carrying S1; that region's middleware looks up `UserProfile` by S1 and runs the normal regional permission check. Three gaps show up:
     - **Replication lag on tokens.** A token issued in the US may not reach the EU replica for 1–2s, so an immediate EU call can 401. Revocation has the same lag: a revoked token keeps working in other regions until replication catches up. State the expected window and whether it's acceptable.
     - **Deactivation.** If the EU profile is deactivated but the US one isn't, the same token is rejected in one region and accepted in the other. Is that intended, or should deactivation spread through the global `status`?
     - **Hotel discovery.** The token works for any slug the client already knows, but nothing tells the client which hotels across all regions the person can reach. A hotel switcher would have to ask every region, or read a sid → regions index. That index is `user-profile-regions`. Fine to defer, but Global Web will need it or something like it.

  Happy to talk through any of it live.

  ### Optional: matching Notion inline comments (not posted)
  If you'd rather put this on the doc, the natural anchors are:
  - #1 on "generated as a model default on every creation path", as a reply to jsterling.
  - #2 on the Risks merge-strategy thread.
  - #3 on the Best Western demand bullet.
  - #4 on the user-profile-credentials thread.
  - #5 on "What implications does this project have on security and data privacy?"
  - #6 on Andrea's portfolio thread.
  - #8 on the "Edge. The signed identity token carries the sid" bullet; hotel discovery as a reply on jsterling's user-profile-regions thread.

  ### Reference: a request to two regions with one credential (my reading of the doc; [inferred] = not stated in the doc)
  Applies to bearer tokens through the global api host (Staff App, Global Web). Browser sessions stay regional.

  Setup: the person has a profile in each region, created by SSO JIT on first login there, or by an admin:
    US Postgres: UserProfile(user 123, sid S1) + US hotel memberships
    EU Postgres: UserProfile(user 456, sid S1) + EU hotel memberships

  Step 1, get the credential once (Staff App OAuth, US):
    SSO login in the US → user 123 (S1) → OAuth login page mints a grant for identity {user_profile, S1}
    → code → access token T. oauth-grants and auth-tokens are DynamoDB global tables, replicated to EU and AP.

  Step 2, request to a US hotel with Bearer T:
    a. routing-service: slug → us-west-2
    b. Istio auth plugin → identity-service (US): T → identity S1 → signed identity token {sid: S1}
    c. US middleware: UserProfile where sid = S1 → user 123
    d. normal regional permission check → 200

  Step 3, same T to an EU hotel:
    same steps; the EU identity-service reads replicated T [inferred lag];
    EU middleware: sid S1 → user 456; permission check against EU memberships.
    The client never picks a region. Each region turns S1 into its own local user, and authorization stays regional.

  What goes wrong, and where:
    - No EU profile for S1 → rejected (the doc says fail closed)
    - EU profile deactivated, US active → EU rejected, US works; the doc doesn't say if deactivation should spread [gap]
    - No membership at that hotel → 403, as today
    - Token issued seconds ago, first call goes to another region → possible 401 until replication [inferred]
    - Revoked token → still accepted elsewhere until replication [inferred]
    - S1 merged into S2 → fails unless the losing sid acts as an alias

  Today the same steps use username:email, so an EU call works only if the EU user has the same username and email, and a rename breaks every token.
project: 2026-04-16T1210-unblock-team
source_id: https://canarytechnologies.slack.com/archives/D09S6HC42H0/p1792079314491039
tags:
- morning-gtd
- slack
time_minutes: 45
title: Give Renan feedback on the Global User Profile / Global SSO doc
updated: 2026-10-16 15:42:35.714728
waiting_on: null
waiting_since: null
working_on: false
---

Renan asked for early feedback before he gets into implementation and rollout details. I said 'I hope to get to this tomorrow' (Oct 15), so it is due today.
https://app.notion.com/p/canarytechnologies/Global-User-Profile-Global-SSO-3f381468615180939704fd689cd53eb0
https://canarytechnologies.slack.com/archives/D09S6HC42H0/p1792079314491039