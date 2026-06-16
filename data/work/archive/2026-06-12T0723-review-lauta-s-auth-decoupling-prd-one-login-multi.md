---
area: null
contexts:
- react
created: 2026-06-12 07:23:20.770370
defer_until: null
due: null
energy: medium
id: 2026-06-12T0723-review-lauta-s-auth-decoupling-prd-one-login-multi
order: null
output: |
  ## Agent run 2026-06-15T13:05Z — Review of Lauta's auth-decoupling PRD

  **Doc:** PRD: Decoupling Authentication from User Accounts (One Login, Multiple Account Profiles)
  https://www.notion.so/canarytechnologies/PRD-Decoupling-Authentication-from-User-Accounts-One-Login-Multiple-Account-Profiles-37c81468615181ab9522d4f7c131046d
  **Slack thread:** https://canarytechnologies.slack.com/archives/C0B1MN8F869/p1781201347454999?thread_ts=1781201279.225359&cid=C0B1MN8F869
  **Author:** Lautaro Mena. Explicitly framed as an *idea/exploration, not a committed project*. He asked Andrea, Connor and me for eyes. Andrea suggested looping in Laura (has prior thoughts); Connor said he'd read it. No deadline, no commitment requested.

  ### What it asks for (the actual decision)
  Two questions only (§9): (1) does the problem framing resonate — will this keep recurring/compounding? (2) is there a principled objection to the direction, so we can file it away instead of re-deriving "no" each time. NOT "should we build this."

  ### Trigger tickets — both real, both declined
  - ENT-6474 (Marjaree Forbes): GM, 6 properties / 3 brands (2 IHG, 2 Wyndham, 2 BW), already has 3 separate Canary accounts, wants one above-property view. **Canceled** 2026-06-11. https://linear.app/canary-technologies/issue/ENT-6474
  - ENT-6484 (merge user access): mgmt-group contact, 4 hotels across 4 brands (BW/Wyndham/Hilton/Choice). **Canceled** 2026-06-11 — "we are not able to merge user accounts from different enterprise customers." https://linear.app/canary-technologies/issue/ENT-6484
  Both filed the same week, both canceled correctly. Confirms his "recurring and compounding" framing.

  ### Technical accuracy — I verified the load-bearing claims against the canary backend. They hold up:
  - **One account per (SSO org, SAML name_id)** — TRUE. `unique_sso_user_per_org` constraint in hotels/models/user_profile.py:130-135.
  - **Merge machinery explicitly forbids cross-org merges** — TRUE. `InvalidTargetDifferentSSOOrganization` + check in sso/services/manual_user_merge.py:80,229-232.
  - **Session holds exactly one authenticated user; impersonation is the precedent** — TRUE. Impersonation is a middleware identity *swap* (request.user / request.impersonator) in impersonation/middleware.py:56-62, not a true multi-user session. So it proves "we can carry alternate identity context in a session," but it is NOT a drop-in for "N simultaneously-authenticated profiles with per-method freshness." The PRD's "commensurate testing burden" caveat is the honest read.
  - **No ForceAuthn / step-up; SLO configured but unimplemented** — TRUE/PARTIAL, exactly as he states. slo_url/slo_binding exist on the Organization SAML config but the SLS endpoint is commented out and there's no logout route. Per-org auth policies (acceptable methods + freshness + step-up re-auth) build on machinery that genuinely does not exist yet — this is the biggest hidden cost and he flags it.
  - **Hotel/portfolio access recorded per-organization** — TRUE. company_hotel_user and portfolio_user both carry sso_organization. This is what makes the proposed "keep accounts as-is, link above them" option clean: access grants don't move.

  ### My assessment
  Strong document. Problem is real and structurally recurring (multi-brand franchising is the US norm; every new SSO mandate fragments more humans). The framing — auth and account are *fused* and "the person" isn't an entity we model — is the correct diagnosis, not just a feature gap. The "safe by construction / orgs get *more* control, not less" point is the right way to disarm the obvious security objection, and §3's rejection of the naive workaround (gating Wyndham access behind IHG's IdP) is exactly right. The recommended option (new Person/auth entity *above* untouched existing accounts, verified link) is the low-risk shape and preserves audit semantics ("her Wyndham account did X"). I'd endorse the direction at the idea level.

  ### Pushback / things I'd raise with Lauta (none are blockers — this is idea-stage):
  1. **Auth-freshness/step-up is the real iceberg, undersized in §7.** "Per-org authentication policy" needs ForceAuthn in our SAML usage, a re-auth round-trip flow, and session state tracking method+freshness per profile — all net-new core auth-path work. If we ever scope this, I'd carve auth policies into a *separate, later* slice and ship plain account-linking + profile-switching first (he already sequences it this way in §7 — I'd make that separation even harder, because slice 1 delivers most of the ticket value without touching the SAML freshness machinery).
  2. **"AI makes this cheaper" caveat (§7) — I'd soften it.** True for migration scaffolding/test coverage/mechanical breadth, but the expensive part here is *design correctness on the auth path* (account-takeover surface, session fixation), which AI accelerates least and where mistakes are most expensive. Don't let that line invite under-budgeting the design phase.
  3. **Verified linking = account-takeover vector.** He flags it (§7/§8.1) but I'd want the design phase to treat the linking/unlink/audit flow as the security centerpiece, not a sub-bullet. Who can initiate a link, what proof, what's the unlink/abuse path, what does support tooling see.
  4. **Coordinate with ENT-6491 (SCIM) and SLO now, on paper.** §8.2 is right that deprovisioning/blocklists/SLO must hit exactly one profile incl. in live sessions. Worth a half-page of "how these two designs reinforce each other" before either proceeds, so we don't build conflicting session models.
  5. **Portfolio-analytics tie-in is the commercial wedge — lean into it.** The cross-org above-property view (the real "prize" he names) is what makes this a revenue story, not just a CS-cost story. (Relevant to my current worktree-portfolio-analytics work — the analytics surface is exactly what these multi-brand owners would buy.) Worth making the §5 "foundation for cross-org views" point more prominent for the audience deciding whether to invest.
  6. **Minor:** call it a "discovery brief" / "problem brief," not a PRD (he's unsure himself in Slack) — there's no committed product to require a PRD, and the framing as exploration is a feature.

  ### Suggested next step (for Gareth to action — NOT done by agent)
  Reply in-thread / comment on the doc with: endorse the problem framing + direction; no principled objection; flag that auth-freshness/step-up is the cost iceberg and should be a separable later slice; suggest pairing the design with ENT-6491 (SCIM) and adding Laura per Andrea's suggestion. NO Slack/Notion/Linear writes were made by the agent — drafts only, awaiting your go-ahead if you want me to post.
project: null
source_id: https://canarytechnologies.slack.com/archives/C0B1MN8F869/p1781201347454999?thread_ts=1781201279.225359&cid=C0B1MN8F869
tags:
- morning-gtd
- slack
time_minutes: 20
title: Review Lauta's auth-decoupling PRD (one login, multiple account profiles)
updated: 2026-06-15 14:45:57.224811
waiting_on: null
waiting_since: null
working_on: false
---

Lauta asked Andrea/Connor/me directly to review his draft addressing recurring tickets (ENT-6474, ENT-6484).
Doc: https://www.notion.so/canarytechnologies/PRD-Decoupling-Authentication-from-User-Accounts-One-Login-Multiple-Account-Profiles-37c81468615181ab9522d4f7c131046d
Thread: https://canarytechnologies.slack.com/archives/C0B1MN8F869/p1781201347454999?thread_ts=1781201279.225359&cid=C0B1MN8F869