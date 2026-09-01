---
area: null
completed_at: 2026-08-31 12:49:09.511590
contexts:
- react
created: 2026-08-14 07:10:44.619732
defer_until: null
due: 2026-08-14
energy: high
id: 2026-08-14T0710-decide-with-andrea-django-admin-v0-vs-manage-app-s
order: null
output: |
  ## Agent run 2026-08-14T04:20Z

  **Headline: the decision as framed is stale. Both options lost. A third one
  (customer-facing self-serve) won between Aug 7 and Aug 11, work has started,
  and you and Andrea have already half-ratified it in DM. What's left is not a
  choice — it's closing three loose ends.**

  ### What actually happened after the Aug 7 thread

  - **Aug 10** — Lautaro DM'd you two Loom pitches for the management section
    (https://www.loom.com/share/1f13435fb783491b851ce379ee1c2f33 and
    https://www.loom.com/share/64ecadf78bc64cefa4e89fd2b3fd63cf). You have not
    replied. DM: https://canarytechnologies.slack.com/archives/D08QQ2UP92A/p1786341604449259
  - **Aug 11** — Lautaro marked the Manage-app PRD **Rejected — superseded** and
    wrote a new one: [PRD: Self-service SSO integration](https://app.notion.com/p/3b981468615181969bfde3f7ae9c7264)
    (old one, kept for history: https://app.notion.com/p/382814686151819ea24de669c6d33ea9).
    New shape: customers configure their own SSO from the above-property
    dashboard; Canary staff use *the same screens* via a support access grant
    (SAG); only cross-tenant operations stay internal.
  - **Aug 13** — first PRs up, awaiting review:
    [#53218 ENT-7160](https://github.com/canary-technologies-corp/canary/pull/53218) (286/-17)
    and [#53219 ENT-7167](https://github.com/canary-technologies-corp/canary/pull/53219) (63/-1),
    posted in #epd-enterprise-engineers as "the first PR needed for the self
    service section for sso"
    (https://canarytechnologies.slack.com/archives/C0B1MN8F869/p1786654452642179).
  - **Aug 13** — Andrea, in your DM: *"as long as we are ok pushing back, I'd
    like to see how far Lauta could get in a week or two. Still some hand
    holding at the end, but all in the name of learning."* You replied *"It's a
    good outcome to have self serve at last"* and handed her the call.
    (https://canarytechnologies.slack.com/archives/D061NMRMFB3/p1786638566793079)
  - **Aug 13** — the intended self-serve pilot died. Andrea raised
    [ENT-7130 La Jolla Beach & Tennis Club](https://linear.app/canary-technologies/issue/ENT-7130/enable-microsoft-entra-sso-for-la-jolla-beach-and-tennis-club-and)
    in the group DM with Connor; Connor: *"No, we are not going to help with this
    one"* and *"I'm going to tell Sales to stop offering this."*
    (https://canarytechnologies.slack.com/archives/C0B1Y5K9AMC/p1786638074757459)

  So: Django-admin v0 is dead, the internal Manage section is demoted, demand is
  being throttled at the sales end, and Andrea has already said "give Lauta a
  week or two." Nothing needs deciding between you two on the original question.

  ### The Linear reality — and the one thing worth pushing back on

  [Project: Self service SSO org management](https://linear.app/canary-technologies/project/self-service-sso-org-management-2df14b58fe5e)
  — lead Lautaro, Enterprise, label `2026 Q3 Block 2`, target **2026-09-30**.
  Milestones and points as scoped today:

  | Milestone | Tickets | Points | State |
  |---|---|---|---|
  | Make SSO-Roles not required | 6 | 7 | 18% — 2 in review, 2 in progress |
  | APD SSO section (the customer product) | 10 | 15 | 0% — all Todo/Backlog |
  | SAG for APD | **0** | **0** | **unscoped** |
  | Internal SSO tools (Manage) | 6 | 7 | 0% — all Backlog, **last in line** |
  | Phase out SSO-Roles | 1 | 4 | 0% (acknowledged tech debt) |
  | Enable Pilot Portfolios | 1 (ENT-7130) | — | pilot just declined |

  **~33 points, ~7 weeks to target, one engineer.** Lautaro's "2 weeks" offer on
  Aug 7 was for the *Manage* version; the plan he's now executing is roughly 3x
  that. Andrea's "1 vs 4 weeks" framing from the thread resolves as: it's 4+,
  and the relief we wanted arrives at the *end*, not the start.

  Concretely, the thing that gets engineering out of the triage queue is either
  **SAG for APD** (2.3 — zero tickets, undefined) or **Internal SSO tools
  (Manage)** (2.5 — 7 points, all backlog, scheduled last). Until one lands,
  every SSO setup still needs Lautaro personally. That is exactly the burden the
  Aug 7 thread was trying to remove, and the current sequencing defers it
  longest.

  ### Does the near-term queue justify a stopgap? No.

  Live SSO setup work in ENT right now is thin, which is what makes dropping the
  Django-admin v0 safe:
  - [ENT-7069 SSO for Extended Stay](https://linear.app/canary-technologies/issue/ENT-7069/sso-for-extended-stay) — Todo, Tincho, 2 pts
  - [ENT-6898 SSO OKTA for Delaware North](https://linear.app/canary-technologies/issue/ENT-6898/sso-okta-for-delaware-north) — Blocked since 16 Jul
  - ENT-7130 La Jolla — being declined
  Historic run rate is roughly 1–2 setups/month (Langham, Highway West, Heritage,
  Hyatt roles) plus a steady trickle of login/identity troubleshooting tickets.
  Not enough volume to fund a throwaway admin UI.

  ### Recommendation — three loose ends, ~10 minutes total

  1. **Close the Aug 7 thread.** Lautaro is nominally still waiting on you and
     Andrea; he's already shipping the superseding plan. One line in-thread —
     "agreed, dropping the Django-admin v0, self-serve is the path" — removes
     the ambiguity. (I have NOT posted anything.)
     Thread: https://canarytechnologies.slack.com/archives/C0B1MN8F869/p1786101647522999
  2. **Ask Andrea to fix the checkpoint.** Her "a week or two" has no date and no
     pass/fail. Suggest: **Fri 28 Aug**, and the bar is "a Canary staffer set up
     one SSO org end-to-end without Lautaro touching the database." That test
     forces SAG-for-APD (or the Manage internal tools) to get scoped rather than
     drifting to the back of a 33-point project.
  3. **Push on sequencing, not on surface.** The argument to make is *order*, not
     Django-vs-Manage: pull `Internal SSO tools (Manage)` (ENT-6962, 6965, 6967,
     7163, 7170, 7174 — 7 pts) or SAG-for-APD forward, ahead of the polish end of
     the APD section. Lautaro's own point on Aug 7 — the backend is the same
     whatever the surface — is the argument for doing the assignment services now
     and the customer screens after.

  Also worth knowing: the pilot is gone, so there is currently **no customer
  lined up to validate the self-serve path**. Worth one line to Andrea — "who's
  the new pilot?" — before the two-week clock starts running on something with
  no user at the end of it.

  ### Your own prior thinking (Bear notes) — mostly *supports* the supersede

  - **SAG-first was already your stated direction.** Stephanie Barry 1-1,
    5 Aug 2026: Canary-only features get built "in adminland" using the SAG
    mechanism, permission-gated "to signal intent to roll out powers to hotel
    users eventually" — with an action item that reads *"Lauta's proposals
    should be adapted for SAGs"*, plus a PRD to draft for typed SAGs. Lautaro's
    §2.3 "SAG for APD" is exactly that. So the new PRD isn't drift; it's your
    own position, arriving. That strengthens the case for ratifying it — and
    makes the fact that SAG-for-APD has **zero tickets** the single most
    important gap to close, since it's both his dependency and your pending PRD.
  - **The handover target is the Integrations team, and you've already written
    it down.** Lauta's review: *"the long term aim of the SSO work is to
    transition it to integrations team… enterprise team handles the
    infrastructure but not every integration."* Block planning (5 Aug): *"Ent
    should not be owning small SSO integrations"* and *"Ent should not be owning
    generic user access requests — internal tools better placed to interface
    with support."* Worth restating to Andrea: the goal isn't "self-serve" per
    se, it's getting ENT out of per-integration work.
  - **Andrea's own data backs the burden case**: of 47 user access requests,
    only 14 were for the big-three enterprises and 33 were smaller/one-off —
    ~1 FTE-week per 6 weeks. Useful number if the "is this worth a week or two"
    question comes up again.
  - **Capacity is the live risk, not surface choice.** Recurring notes on
    Lautaro: overloaded and reactive ("too many things at once… SSO UI,
    Stephanie default roles, procrastinating"), your own review advice to
    *"narrow your scope… work on one thing at a time"*, and Blake's flag that he
    holds concentrated team knowledge that should be shared for resilience.
    That argues against running a Django-admin stopgap in parallel, and *for*
    tightening the project to one ordered track.
  - **Gap:** no note anywhere adjudicates Django-admin vs Manage-section vs
    above-property self-serve as three options. The Aug 5 adminland/SAG entry is
    the closest thing to a prior, and it points at admin-first *with* eventual
    customer exposure — which is what the new PRD does.

  **No external writes were made.** Nothing posted to Slack, Linear, Notion or
  GitHub.
project: 2026-04-16T1210-unblock-team
source_id: https://canarytechnologies.slack.com/archives/C0B1MN8F869/p1786109251898469?thread_ts=1786101647.522999&cid=C0B1MN8F869
tags:
- morning-gtd
- slack
time_minutes: 15
title: 'Decide with Andrea: Django-admin v0 vs manage-app section for SSO integration
  tooling'
updated: 2026-08-31 12:49:09.511582
waiting_on: null
waiting_since: null
working_on: false
---

Lautaro pushed back on the Django-admin v0 and offered to ship the manage-app version in ~2 weeks. Andrea's view: manage app eases handover and points at above-property; Django admin fixes it for us sooner. The decision is mine + Andrea's and Lautaro is waiting.
https://canarytechnologies.slack.com/archives/C0B1MN8F869/p1786109251898469?thread_ts=1786101647.522999&cid=C0B1MN8F869