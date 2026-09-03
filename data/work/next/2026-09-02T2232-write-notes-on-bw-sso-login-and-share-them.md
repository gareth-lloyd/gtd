---
area: null
completed_at: null
contexts: []
created: 2026-09-02 22:32:37.866814
defer_until: null
due: 2026-09-03
energy: low
id: 2026-09-02T2232-write-notes-on-bw-sso-login-and-share-them
order: null
output: |
    ## Agent run 2026-09-03T14:05:00

    Notes written. NOT yet shared anywhere — no Slack/Notion post made (needs your OK).

    ### Deliverables (local, unshared)
    - Markdown, ready to paste into Slack or Notion:
      `/private/tmp/claude-501/-Users-garethlloyd-projects-canary/6c72b92d-76ea-4c05-892d-6fa8625e57ef/scratchpad/bw-sso-login-notes.md`
    - Designed HTML version of the same notes (artifact publish was blocked by auto-mode, so it is file-only):
      `/private/tmp/claude-501/-Users-garethlloyd-projects-canary/6c72b92d-76ea-4c05-892d-6fa8625e57ef/scratchpad/bw-sso-login-notes.html`
      Re-run the Artifact publish in a normal-permission session to get a shareable link.

    ### 1. BW SSO sync (2 Sep) — outcomes
    Six things decided, three left open.

    Decided: V1 is US-only SSO (1,400 US properties vs 11 EU); no region picker and no
    cross-region session; two-stage identifier-first login (identifier screen, then fork to
    SSO or password); ambiguous email falls back to username; an allow-list of SSO orgs with
    exactly one entry (Best Western); password login stays global and unchanged.

    Open: whether the staff-app login is a web view (Caitlyn -> mobile team; strongly
    preferred, removes the native release dependency); the backend shape of the fork
    (Identity + Enterprise); and who builds it (Enterprise is committed to IHG, nobody
    assigned).

    Commercial framing from Connor: no revenue and no commercial commitment. SSO is the only
    way BW properties can log in, so it is a hard blocker on the staff app, which is BW's
    most-requested feature. Behind it sits housekeeping/ticketing and a race against HotelKey.
    Convention is 26 Oct in Phoenix, needs ~2 weeks of property testing first, so demo-ready
    by ~10 Oct. SJ's target is 500+ properties signed up on the day.

    Notable: Connor confirmed BW has made no ask at all here — the two-IdP split was Canary's
    own decision. That descopes the whole cross-region question for October.

    ### 2. Renan's solution — assessment
    Two artefacts are being discussed as one, and separating them is most of the decision:
    the Notion doc (durable data model: immutable `au_` sid, regional users as profiles,
    global DynamoDB identity tables, CDC as single writer) and the 31 Aug Mermaid flow
    (runtime: identifier-first page, cross-region fan-out lookup, global grants).

    Right and worth keeping: identifier-first as the primitive; looking the user up rather
    than routing on email domain; always showing the password step on a miss/timeout
    (enumeration defence); leaving the regional SAML ACS untouched (BW's IdP carries the
    hotel list and roles, so authorisation genuinely is regional); fail-closed in
    PrincipalMiddleware; and the doc's core diagnosis that a global id keyed on
    hash(username:email) is mutable and collides.

    Over-scoped for 10 Oct: the cross-region fan-out serves a case we agreed not to serve —
    with EU descoped, serving region == owning region for every BW user. The global identity
    layer (global grants, `auth_user_sid`, `global_identity_sid`, backfill, Debezium on
    hotels_userprofile) is the part carrying real schedule risk, and the doc's own open
    questions (org sid across regions, PII/data residency, global `is_active`) would block
    it. Global `is_active` is the one I'd flag hardest: a regional deactivation locking every
    profile is a behaviour change to a safety control with no product decision behind it.

    Under-specified in both: the duplicate policy is still a placeholder ("maybe pick the
    newest one"), yet it is the single rule deciding whether a BW user can log in; neither
    design contains the allow-list the sync agreed on; and neither mentions the 5,440 BW
    users with no `sso_name_id` who cannot log in today (~a quarter of BW's user rows).

    Email-domain routing is settled against, and the reasoning is recorded in the notes so it
    does not come round again: `Organization.limit_to_email_domain` exists but is a single
    domain and a restriction, not a routing index; multiple SSO orgs can share a domain; and
    BW's own `sso_name_id` values already span five domains for one org. Lauta's 3 Sep reply
    concedes the same ground by falling back to username.

    ### 3. Proposed shape
    Split V1 from V2 and stop arguing about them as one thing.

    V1 (~10 Oct): server-rendered identifier-first page in the monolith, served from
    us-west-2 in a web view; identifier resolves against the serving region's Postgres only —
    no fan-out, no global tables, no model changes, no migration; explicit allow-list of one
    org slug; existing `/sso/login/<slug>` and regional ACS untouched; non-US users fall
    through to the password step, which is what they get today anyway.

    V2 (planned now, built after): Renan's Notion model largely as written, gated on four
    answers — org identity across regions, global vs regional `is_active`, data residency for
    global tables, and a decided duplicate policy.

    The seam that makes this safe: put step 2 behind one function with the contract
    `identifier -> {region, user, method}`. V1's body is a local query; V2 swaps in the
    fan-out and duplicate policy and nothing above it changes. V1 then isn't throwaway and
    nobody has to argue about which design won.

    Resolution ladder is written out in order in the notes (7 rungs), adopting Lauta's five
    cases from #staff-app-sso for rungs 3-5.

    ### Grounded in code (worth knowing before anyone estimates)
    - `hotels/forms/forms.py` + `hotels/views/views.py`: web login is a SINGLE
      username+password form. The SSO fork only fires AFTER the password submission fails
      validation, and only when `sso_org.login_url` is set and password login is disallowed
      (`sso_user_should_redirect_to_sso_login`). So "just mirror web in a web view" is not
      free — there is no identifier-first login on web to reuse. The two-stage page is new.
    - `sso/models/organization.py`: `limit_to_email_domain` is one CharField, a restriction,
      no uniqueness across orgs. Not usable as a routing key.
    - `hotels/models/user_profile.py`: SSO users keyed on `(sso_organization, sso_name_id)`
      via a conditional unique constraint.

    ### Sources
    - Granola "BW SSO sync", 2 Sep 2026 (id 2d803c93-684a-4a44-8393-3a16531464c6)
    - Granola "Global SSO", 31 Aug 2026 (id c61b665b-2853-427c-ab82-c06eb93159f5)
    - Slack, Caitlyn's kickoff thread: https://canarytechnologies.slack.com/archives/C0AN8AQ49UG/p1787935367405959
    - Slack, Lauta's email-domain thread (your pushback): https://canarytechnologies.slack.com/archives/C0BET8YEKB4/p1788215392684259
    - Slack, Renan's Mermaid flow: https://canarytechnologies.slack.com/archives/C0BET8YEKB4/p1788203721883719
    - Notion, "Global Identities & SSO — Immutable Identity, Cross-Region Linking": https://app.notion.com/p/3ca81468615181fcbc5af1d1a671fc2a
    - Google Doc, Gemini notes for the 31 Aug Global SSO call: https://docs.google.com/document/d/1HcCYu7rdm2JEc1D1yJNzmjh9eij4xryPettHBNxycRY

    ### Not done (yours to call)
    - Sharing. Say where (which Slack channel / thread, or a Notion page) and I'll draft the
      exact message for approval before anything is posted.
project: 2026-09-01-bw-global-sso
source_id: null
tags: []
time_minutes: 5
title: 'IMPORTANT: Write notes on BW SSO login and share them. Include shape of proposed
  solution'
updated: 2026-09-03 14:05:00.000000
waiting_on: null
waiting_since: null
working_on: false
---

Call transcript in Granola: "BW SSO sync" title. Context in Slack threads:
https://canarytechnologies.slack.com/archives/C0BET8YEKB4/p1788215392684259
https://canarytechnologies.slack.com/archives/C0AN8AQ49UG/p1787935367405959

The proposed solution starting point is Renan's flow described here:

Mermaid flow + Notion doc 'Global Identities SSO: Immutable Identity, Cross-Region Linking' posted in #eng-identity, tagging me. Identifier-first login, regional fan-out lookup, global DynamoDB grants. I already pushed back in Lauta's sibling thread that email-domain routing won't generalise (multiple SSO orgs can share a domain).
https://canarytechnologies.slack.com/archives/C0BET8YEKB4/p1788203721883719


Task:
* Summarize BW SSO sync call outcomes
* Investigate how appropriate Renan's solution is.