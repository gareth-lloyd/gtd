---
area: null
completed_at: null
contexts: []
created: 2026-08-07 13:42:11.505680
defer_until: null
due: null
energy: low
id: 2026-08-07T1342-assess-lauta-s-comment-that-auth-api-work-needs-to
order: null
output: |
  ## Agent run 2026-08-07T10:45Z

  **Verdict: the framing is right, the target is wrong. Nothing in the Public API design
  needs to change. One thing in it does need an answer, and it isn't the thing he asked about.**

  ### What the comments actually say

  Lautaro posted two comments on 2026-08-06, both replying to your 2026-06-15 nudge to frame
  the PRD against the global identity work.

  1. On the PRD, in your page thread
     (https://app.notion.com/p/37c81468615181ab9522d4f7c131046d?d=651814686151828cb8ae034f485240b5):
     "I think there is no overlap here (other than the choice of the word Identity for different
     entities) but for the solution on this proposal to work we may need a few changes on their solution."
  2. On the Canary Public API design doc, anchored to the Identity-table callout
     (https://app.notion.com/p/2f48146861518016980fe487bdcc1ddc?d=3b481468615180b29d5c001c036fb639),
     asking Jordan Sterling to review: *"one session should be able to hold several authenticated
     accounts at the same time, today each session maps to one identity, and each identity to one
     account. Can the Canary Public API be built in a way that supporting several accounts per
     session later is simple, or is it too much overhead?"*

  PRD: https://app.notion.com/p/37c81468615181ab9522d4f7c131046d (Lautaro, idea-stage, not committed)
  Design doc: https://app.notion.com/p/2ef8146861518080bcc3dfce8a33759c (Jordan Sterling, Platform, IN REVIEW)

  ### Assessment

  **The Identity table is invariant under his PRD — he's right that there's no overlap, and he
  should stop there.** Identity is unique on `(type, reference)` with a deterministic sid
  (`IdentitySid.hash_of(type, reference)`, `backend/canary/api_gateway/services/identity_service.py:100`),
  and the staff-user reference is `username:email` (`StaffUserReference`, same file). So an identity
  row is *per account*. Nothing in that table caps how many identity rows one human owns. It is a
  name-resolution service; a person with 3 accounts already has 3 identities today, correctly.

  **The 1:1 he wants relaxed is in middleware, not in the Public API.** `BasePrincipalMiddleware.resolve()`
  (`backend/shared/shared/request_framework/principal_middleware.py:44`) returns exactly one `Principal`
  per request, and canary's `resolve_session()` (`backend/canary/canary/middlewares/principal.py:73`)
  returns one `UserPrincipal` off `request.user`. That is the cookie path in the monolith. It is
  entirely separate from the token path the design doc specifies.

  **The token path should stay 1:1 and he should not ask for it to change.** `AuthToken.identity` and
  `oauth_grants.identity_sid` bind one credential to one identity to one account. That is correct and
  worth defending: a machine credential must not carry a human's whole account set, or every partner
  integration inherits the blast radius of cross-brand access. His own GitHub analogy works this way —
  a token is scoped, and org SSO enforcement is applied per-org at check time, not by fanning the token
  out. So the honest answer to "is it too much overhead" is **zero, because the answer is do nothing**.
  Asking Jordan for a change here risks getting a worse design than leaving it alone.

  ### The one real ask he has on Jordan's design — and he didn't make it

  The OAuth authorize leg. Per the OAuth section of the design doc (step 3), the login page creates the
  `oauth_grant` and *sets the staff user `identity`* at login time. If a human has several accounts, the
  login page cannot know which identity to bind without asking. That needs an **account chooser on the
  shared login page**, and it is a flow/UX question, not a data-model one — cheap now, awkward once
  partners have integrated against the current redirect contract.

  He already knows this: PRD §8 says "The shared login page (also used by OAuth) may need an account
  chooser." He then wrote a comment asking for something else. Worth pointing him at his own paragraph.

  ### Two couplings he has not named, both cheap to state now

  1. **Don't move email off the account.** PRD §4 proposes "moving name and some contact fields up" to
     the new person entity. The staff-user identity sid is a deterministic, unsalted hash of
     `username:email`. If email stops being account-scoped, two accounts of the same person can collide
     on `UNIQUE(type, reference)` and hash to the *same* identity sid — silently merging two accounts'
     audit trails. Constraint to write down today: the staff-user reference must stay derived from an
     account-scoped field. Username is fine, email alone is not. One line now, a data migration later.
  2. **EE-1495 raises the stakes on account linking.** Identity sids are derivable, not merely
     non-secret, and the monolith was resolving a client-supplied `Bearer id_...` into a principal
     (see the note at `backend/canary/canary/middlewares/principal.py:35-38`). Django now verifies a
     signed edge token, but per Bernard Pietraga's 2026-07-31 comment on the design doc, ok-api-v5 and
     the task_management gatekeeper still resolve internal_service identities from the raw bearer.
     "One authentication unlocks several accounts" multiplies what a derived sid is worth. This is
     exactly the concern Andrea Bradshaw flagged as her main one on the PRD.

  ### Vocabulary

  He acknowledges the collision and then keeps using "Identity" for the human. Two Identity entities in
  adjacent in-review designs will cost more reviewer time than a rename costs him. The PRD prose already
  says "the person" throughout — **rename the entity to Person**.

  ### Suggested reply to Lautaro (NOT posted — needs your words + approval)

  Substance to convey, in your own voice:
  - Agree there's no overlap; the Identity table doesn't need to change and neither does the token path.
  - Don't ask Jordan to make auth tokens/OAuth grants multi-account — 1 credential : 1 account is right,
    and it's what GitHub does too.
  - The real ask on his design is the account chooser on the shared login page before the grant binds
    an identity. That's your §8 — make it the actual question.
  - Add the constraint that the staff-user identity reference stays account-scoped, so contact fields
    moving up to Person doesn't collide identity sids.
  - Rename the PRD entity to Person.

  Say the word and I'll draft the exact comment text for you to edit and approve before anything is posted.

  ### Verified / not verified

  Verified against code in this repo: identity sid derivation and uniqueness, staff-user reference shape,
  single-principal-per-request in both the shared and canary middlewares. Read in full: the PRD, all 4 of
  its discussions, Lautaro's comment on the identity-table page, and the identity / auth-token / OAuth /
  interservice sections of the Public API design doc. Not read in full: the rest of that design doc
  (global routing, Istio/WASM, device attestation) and the "June 2026 Service Architecture Gaps" page you
  linked, which now renders blank. No tests run, no code changed, nothing posted anywhere.
project: 2026-04-16T1351-ship
source_id: null
tags: []
time_minutes: 5
title: Assess Lauta's comment that auth api work needs to change
updated: 2026-08-07 13:47:10.000000
waiting_on: null
waiting_since: null
working_on: false
---

https://app.notion.com/p/PRD-Decoupling-Authentication-from-User-Accounts-One-Identity-Multiple-Accounts-37c81468615181ab9522d4f7c131046d?d=651814686151828cb8ae034f485240b5&source=copy_link

Read linked comment. 
REad referenced comment on other doc
review docs to assess