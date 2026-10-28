---
area: null
completed_at: null
contexts:
- deep
created: 2026-10-26 12:54:53.679994
defer_until: 2026-10-29 09:00:00
due: null
energy: high
id: 2026-10-26T1254-review-renan-moreira-s-global-user-profile-global
order: null
output: |-
  ## Agent run 2026-10-26

  Read the doc (last edited 2026-10-23 13:10), all 15 comment threads, the Slack DM, and Global Web (https://app.notion.com/p/3c6814686151805b8a11f952998b7a6d). **Nothing was posted.** The draft comments are below for you to post if you agree.

  Doc: https://app.notion.com/p/canarytechnologies/Global-User-Profile-Global-SSO-3f381468615180939704fd689cd53eb0
  Slack DM: https://canarytechnologies.slack.com/archives/D09S6HC42H0/p1792764674195549. His last message (10-23) was "No rush, I'll leave on vacation starting next week". He's away this week, so the comments will wait until he's back. Posting them today still keeps your Monday promise.

  ### Your earlier comments (10-16) are all addressed
  - Merge regional IdPs? Renan says no: `sso_organization_sid` joins the regions, and the design works whether an org has one IdP or several. https://app.notion.com/p/3f381468615180939704fd689cd53eb0?d=3fb81468615180bdab8c001cbf397dac
  - Cross-region hotel discovery: deferred on purpose; they'll add a sid→regions index if fan-out is too slow. https://app.notion.com/p/3f381468615180939704fd689cd53eb0?d=3fb814686151801e8188001c053ddb47
  - Step-by-step example flows: added as "Login flow across regions" (US then EU, 8 steps). Good.

  ### Other open threads (no need to repeat these)
  - Jev's points were folded in: global `sso_organization_sid`, the collision/merge strategy, and a profile sid instead of a regional uuid. His credential-table naming thread (one credential per profile, phone later) is still open with a question from Renan.
  - Andrea: portfolio grants added to Out of scope. Her diagram-cutoff thread is still open ("Is it better now?").
  - Security, Aleksandra, 10-23: four inline comments plus a page-level summary.
    - SAML subjects are scoped to the IdP, so the same subject from two IdPs isn't proof of the same person.
    - The refresh race lets a token be issued after the merge revocation sweep.
    - Deactivation scope, plus revoking and cutting off legacy tokens.
    - A keyed hash is still personal data under GDPR, so residency and deletion are needed in phase 1.
    - These are the heaviest open items.

  ### New review points (draft comments)

  **1. The Global Web goal is overstated; biggest point.** Goals says "Global Web is unblocked." But Global Web's definition of done is "all users logged in to the Canary website have a public api auth token", issued to a `user_profile` identity, and it also needs impersonation identities built from `user_profile` (its "MUST be of type todo" note). This doc's first release is SSO-only, and the OAuth mint "refuses rather than falling back" for null sids. So password and email users, who are most website users, still can't get a `user_profile` identity. Either reword the goal to "unblocked for SSO users", or name the phase that covers password users and make Global Web depend on that phase.
  > Draft comment (on "Global Web is unblocked"): Global Web's DoD is a public-API token for *every* website user, as a user_profile identity, plus impersonation identities built from user_profile. With phase 1 SSO-only and the mint refusing null sids, most website users stay blocked. Can we either scope this goal to SSO users or name the phase that unblocks Global Web?

  **2. Check that "the OAuth mint refuses otherwise" is scoped to the allow-list.** Implementation says: "The OAuth mint uses the user profile identity when the sid is set and refuses otherwise". Read literally, every password user's Staff App OAuth login breaks on deploy. That contradicts "Backwards compatibility: None", and `staff_login` / `oauth_grant_issuance_service` mint `staff_user` today for everyone. I assume Renan means "refuse only for allow-listed orgs whose user has no sid; everyone else keeps `staff_user`".
  > Draft comment: Is the refusal only for allow-listed orgs? As written, password users (null sid) can no longer get Staff App tokens, which contradicts "no backwards-compatibility breaking changes".

  **3. Consider a deterministic first mint to remove the collision machinery.** The repair task (at 10s and 1m), the daily reconcile, the merged state and token revocation all exist because two regions can mint different sids during the replication lag. The refresh race Security flagged also comes from that path. Alternative: on a credential miss, mint `sid = HMAC(global_key, sso_organization_sid + subject)` instead of a random value. Both regions compute the same sid independently, the writes are idempotent, and nothing needs merging. The sid is computed only once, at first registration, and stored. After that it never changes, even if the subject changes later, so the "never derived from mutable fields" goal still holds. The doc already plans a keyed hash of the subject for the credential key, so this is close to free. If a subject is reassigned to a new person, the admin path gives them a fresh random sid. Main trade-off: the HMAC key must be global and stable for minting.
  > Draft comment (on Risks / Repair): Could the first mint be deterministic, e.g. HMAC(key, org_sid + subject)? Then concurrent first logins in two regions write the same sid, and the repair task, reconcile, merged state and the post-merge token race all go away. It's computed once and stored, so later subject or attribute changes don't affect it.

  **4. Does the core use case (Best Western) actually link?** Linking needs both regional IdPs to send the same subject for the same person. Security made the same point. BW has separate US and EU IdPs. If their NameID is a persistent opaque ID, each IdP generates its own and nothing links, so the demand-center goal fails. If it's an email, linking works, but the subject is then mutable and reassignable. The doc lists "confirm Best Western's NameID format" as an ENT task during rollout. It should be checked before build, because it decides whether phase 1 delivers anything for the customer that motivated it. (I didn't query prod SSO org config: CLAUDE.md says no prod access without an explicit ask. I can look it up read-only via the Sallyport canary MCP tools if you want.)
  > Draft comment (on Demand center / BW): Have we confirmed that BW's US and EU IdPs send the same NameID for the same person? If it's persistent or transient, nothing links and the main goal fails for BW. Worth checking before build, not during rollout.

  **5. Reassigned subjects now cross regions.** If an IdP reuses a subject (for example a rehired or recycled email), a first login in a new region gets a registry hit. The new person is then linked to the departed person's sid, and that sid's tokens resolve in every region where it has a profile. Within one region this happens today, because the local lookup reuses the old user. The registry spreads it to every region. Suggest: refuse to link to a sid whose profiles are all inactive, or require the sid to have an active profile somewhere. This ties into Security's deactivation question.

  **6. Backfill vs the rejected alternative.** Alternatives lists "One sid per person at backfill: group existing accounts across regions before minting" as not chosen. But a backfill run one region at a time through lookup-or-register would link BW's existing US+EU duplicates anyway (the second region gets hits). Which is intended? If existing duplicates are not linked, say so and say how they get linked later. More broadly, the Alternatives section lists four options with no reason for rejecting any of them. One line each against the three stated criteria would help.

  **7. Smaller items**
  - Repair wording: "marks the losing profile merged and revokes its tokens". The regional profile isn't merged; it gets the winning sid. The losing `user-profiles` registry row is what gets marked merged. Clarify which, and say what an identity on the losing sid sees afterwards (401 and re-login?).
  - Staging is single-region, so linking and collisions are first exercised in prod (with the internal test org). Could the collision drill run against a local or staging setup with two DynamoDB replica regions first?
  - Out of scope still says "⚠️ Not finished yet", and Vocabulary is still "TBD". The doc uses "profile", "identity", "user profile identity", "sid" and "global_identity_sid" interchangeably, so the glossary would help.
  - Leftover text: "generated ...ation path" / "immutable ...first save" are anchors from older wording. Jev's thread on the old regional-uuid approach (https://app.notion.com/p/3f381468615180939704fd689cd53eb0?d=3f981468615180d4bf02001c2fe8539f) can probably be resolved now.

  ### Overall
  The direction is right and the doc has improved a lot since 10-16. I wouldn't approve yet:
  - **Must fix:** #1 (the goal overstates what phase 1 delivers for Global Web) and #2 (possible breakage for password users).
  - **Must answer first:** #4 (whether BW links at all) and Security's four comments.
  - **Strongest design suggestion:** #3, which would also close Security's merge and refresh race.

  Suggested Slack reply, not sent (DM to Renan):
  > Left my review comments on Global User Profile. Main ones are about the Global Web goal vs SSO-only phase 1, the null-sid mint refusal, and an idea for a deterministic first mint that removes the collision repair. Enjoy the vacation, no rush!

  ## Agent run 2026-10-27: doc summary + example flows

  Re-checked on 10-27. The doc is unchanged since 2026-10-23 13:10. There are still 15 comment threads, none new since Security's on 10-23, and none of the 10-26 drafts have been posted. The review above still stands.

  ### Summary
  The doc gives every hotel staff member one permanent, opaque global ID (`sid`), stored on each of their per-region user accounts. Logins and tokens then keep working when a username or email changes, and across regions. The first release covers SSO users only.
  - **The problem today:**
    - Each region keeps its own users, and nothing global links them.
    - The global handles that exist are hashes of `username:email`, so a rename breaks tokens and orphans the old record.
    - Best Western's US and EU sign-in systems give one person two accounts.
    - Staff App SSO is US-only because of this.
  - **Who's asking for it:** Best Western (SSO-only staff who want the Staff App), and Global Web, which lists this as a hard dependency.
  - **New ID on each regional account:** `UserProfile.global_identity_sid`. It is set once and never changed, except by the duplicate repair.
  - **New global ID for customer organizations:** `sso_organization_sid`, which ENT sets to the same value in every region for the same customer.
  - **Global registry in identity-service:**
    - `user-profiles` holds just the ID.
    - `user-profile-credentials` maps (organization ID + hashed SSO identifier) to the person's ID.
    - Names, emails and passwords stay in each region's own database.
  - **Login flow:** when an SSO login finds no local account, the region asks the registry. A hit reuses the person's ID; a miss creates a new one. Later logins never call the registry.
  - **Tokens:** tokens and app access grants reference the ID through a new `user_profile` identity type. Each request looks the ID up in that region's database and fails if there's no local account.
  - **Retires the old table:** the old `auth-users` table and the pipeline that copies data into it are removed.
  - **Risks it names:**
    - Two regions creating two IDs for one person before they sync. Repaired at 10s and 1m, plus a daily check.
    - A registry outage, where new SSO logins fail with an error page and a kill switch restores today's behaviour.
    - A wrong organization ID, which only ENT can set.
    - Different SSO identifiers across sign-in systems, which give the person two IDs.
  - **Rollout:** six steps (IDs and columns, registry, lookup on SSO login, tokens by ID, repair and backfill, rollout by organization). Off by default with a per-organization opt-in list and a kill switch. Staging first, then an internal test organization set up in two regions, with Best Western last. Each organization runs a clean week before the next. Needs ENT, Security and Platform.
  - **Not in scope:** permissions on portfolios across regions. Password and email users come in later phases.
  - **Unfinished:** Vocabulary is TBD and Out of scope is marked unfinished.

  ### Example flows
  The doc already walks through "first login in the US, later in the EU". These flows cover the other paths. **[doc]** means the doc says it; **[gap]** means the doc is silent or ambiguous, and I've stated my reading.

  **A. Returning user, every login after the first (the common path)**
  Maria (Best Western, EU) already has an EU account with `sid=up_123`.
  1. The Staff App starts SSO and the EU sign-in endpoint validates the response from her company's sign-in system. **[doc]**
  2. Her local account is found by organization + SSO identifier, already carrying `up_123`. Nothing global is called. **[doc]**
  3. The app access token is issued to identity `{type: user_profile, reference: up_123}`. **[doc]**
  4. On each API call: bearer → identity → `up_123` → EU account, then check that it's active. Only the region's own database is read. **[doc]**

  Point: after the first login, nothing global is on the request path. This is why the doc calls the load "near zero".

  **B. Rename**
  Maria's email changes from maria@bw-old.com to maria@bw.com.
  1. Her next SSO login updates `auth_user.email` through just-in-time provisioning, as today.
  2. Today this would change the `username:email` hash, so her Staff App tokens stop resolving and she is signed out.
  3. With the new design, her token references `up_123`, which hasn't changed, so the token keeps resolving. **[doc]**
  4. **[gap]** This only holds if her SSO identifier is not the email. If her company sends email as the identifier, step 1's lookup by organization + identifier misses. She then looks like a new person: the registry misses and a new account with a new ID is created. The rename fix only works for companies whose identifier is a stable, opaque ID. (Ties to review point 4.)

  **C. One token, used against a hotel in another region**
  Maria holds a token for `up_123` and has accounts in both the US and EU.
  1. The app calls the global API for a US hotel. Global routing sends it to the US region by hotel slug. **[doc]**
  2. The signed identity token carries `up_123`, so the US region looks up its own account with that ID, and the request works without a second login. **[doc]**
  3. If she had no US account, the request fails rather than falling back. **[doc]**
  4. **[gap]** Nothing tells the app which regions or hotels she has. It has to ask each region (your earlier comment; deferred by Renan).

  **D. Two regions create two IDs for one person (collision and repair)**
  Jo's first logins hit the US and EU within the ~1–2s it takes the regions to sync.
  1. Both regions find no local account, and both registry lookups miss because neither write has reached the other region yet. **[doc]**
  2. The US creates `up_A` and the EU creates `up_B`, each creating an account and issuing tokens. **[doc]**
  3. The credential tables sync, and the later write wins, say `up_B`. **[doc]**
  4. At 10s or 1m, the US repair task re-reads the credential row, sees `up_B`, rewrites the US account's ID from `up_A` to `up_B`, marks `up_A` merged and revokes `up_A`'s tokens. Jo signs in once more in the US. **[doc]**
  5. **[gap]** Security's race: a token refresh already in progress on `up_A` can issue a new token after the revocation. The merged state has to block issuance and authentication, not just revoke tokens once.
  6. Under the alternative from review point 3 (ID computed from organization + SSO identifier), both regions would compute the same ID in step 2. Steps 3–5 disappear.

  **E. Registry down, new user**
  1. Sam's first login in the EU finds no local account and calls the registry, which times out. **[doc]**
  2. The login fails with an error page, and no account is created. **[doc]**
  3. Existing users like Maria (flow A) are unaffected because they never call the registry. **[doc]**
  4. For a prolonged outage, ops can drop the organization from the opt-in list or use the kill switch, and today's sign-in behaviour returns. **[doc]**

  **F. Password user logs into the Staff App (no ID)**
  Alex, a password user at a hotel that isn't using SSO, has no ID set.
  1. Alex logs in with a password, and the app access token is issued.
  2. **[gap]** The doc says the token issuer "uses the user profile identity when the sid is set and refuses otherwise". Read literally, Alex's login now fails, a regression for every password user. My reading is that the intent is: refuse only for opted-in SSO organizations, and everyone else keeps today's `staff_user` identity keyed by `username:email`. That would also mean Alex gets none of the rename protection, and isn't covered by the Global Web dependency (review points 1 and 2).

  **G. Backfill of existing duplicates**
  Best Western staff who already have both a US account and an EU account.
  1. The backfill runs in the US first: each SSO account looks up or registers its credential and gets a new ID. **[doc]**
  2. The backfill then runs in the EU: the same organization ID + SSO identifier gives a registry hit, so the EU account receives the US ID. **[gap]** This links existing duplicates automatically, yet the doc lists "One sid per person at backfill" as a rejected alternative (review point 6). It also depends on both of Best Western's sign-in systems sending the same identifier (review point 4).
project: null
source_id: https://canarytechnologies.slack.com/archives/D09S6HC42H0/p1792764674195549
tags:
- morning-gtd
- slack
time_minutes: 45
title: Review Renan Moreira's Global User Profile / Global SSO doc (promised Monday)
updated: 2026-10-28 15:54:07.775189
waiting_on: null
waiting_since: null
working_on: false
---

On 10-23 Renan asked for another review and I said 'Is Monday ok?'. He said no rush, but he's on vacation from next week.
https://app.notion.com/p/canarytechnologies/Global-User-Profile-Global-SSO-3f381468615180939704fd689cd53eb0
https://canarytechnologies.slack.com/archives/D09S6HC42H0/p1792764674195549