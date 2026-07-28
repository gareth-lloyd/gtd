---
area: null
contexts:
- react
created: 2026-07-28 09:53:44.090104
defer_until: null
due: 2026-07-28
energy: medium
id: 2026-07-28T0953-weigh-in-on-check-in-configuration-location-debate
order: null
output: |
  ## Agent run 2026-07-28T13:20:00+03:00

  Read the full #tmp-check-in-configuration-location history and all threads
  (https://canarytechnologies.slack.com/archives/C0BKDAG8FMY). Drafted a weigh-in
  reply below — NOT posted; needs your explicit approval (or edit + post yourself).

  ### State of the debate

  - **July 8–9 round** (thread
    https://canarytechnologies.slack.com/archives/C0BKDAG8FMY/p1783509542515049):
    consensus was reached on your proposal — shared builder codebase, hotel-staff
    subset in adminland, CS superset in /manage. Vibhor: "lets take this path …
    minimizing overhead … keeping the security concerns at bay."
  - **July 23 round**: Wenjun relayed SJ/Blake's view that ALL config belongs in
    adminland and /manage must not become "django admin v2"; CS edits should
    "express clear intent." Discussion re-converged on /manage anyway (Vibhor:
    reg-card PMS field mapping is CS-only power, so impersonation "is not really
    impersonation"; Stephanie proposed embedding in /manage/properties; Vibhor
    "aligned"; Lea keeping it feature-flagged behind a navbar link pending designs).
  - **July 27 (Stephanie's async summary,
    https://canarytechnologies.slack.com/archives/C0BKDAG8FMY/p1785182639028309)**:
    group still diverging after she talked to Wenjun + Laura. Option A: CS in
    /manage, clients in adminland. Option B: everyone in adminland; CS sees richer
    view; pre-live edits via training user; post-live via Support Access Period
    (temp user + impersonation). She names the sticking point: we conflate
    impersonate-to-view with impersonate-to-edit.
  - **Open question from Andrea** (unanswered,
    https://canarytechnologies.slack.com/archives/C0BKDAG8FMY/p1785182774894709):
    how often does CS reconfigure LIVE hotels? Vibhor earlier: "not often but that
    is just anecdotal, i dont have data."
  - **Vibhor's saved mention**
    (https://canarytechnologies.slack.com/archives/C0BKDAG8FMY/p1784666772775569):
    Wenjun notes Canary-only features already exist in prod hotel dashboards —
    i.e. the staff-gated-dashboard pattern you called "a smell" already has
    precedent.
  - Andrea's security principle (no blanket Canary write access to any hotel) has
    a +1 and your "critical, must hold in all outcomes" replies; both camps accept
    it.

  ### Key insight for the weigh-in

  The two options share the builder codebase either way; the real disagreements
  are (1) which shell renders the CS superset and (2) how CS access is gated —
  and (2) is separable: Support Access Grants can gate /manage editing directly
  (grant = Blake's "clear intent"), with edits made and audited as the real staff
  member, no synthetic temp user. Option B re-imports impersonation-for-editing
  under a new name and puts CS-only powers in the hotel dashboard — the exact
  legacy pattern behind past security incidents / SOC 2 concerns. Rarity of
  post-live reconfig (per Vibhor) supports grant friction being acceptable.

  ### Draft Slack reply (to channel C0BKDAG8FMY — awaiting your approval)

  Catching up on this — thanks Stephanie, that's a clear summary. My take:

  The two options are closer than they look. We all agree on one shared builder
  codebase with hotel staff seeing a subset. The real questions are (1) which
  shell renders the CS superset view, and (2) how CS access is gated — and they're
  separable.

  On (2) first, because I think it dissolves most of the disagreement: a Support
  Access Grant is itself the "clear intent" Blake wants — it doesn't have to imply
  impersonation. We can extend the grant machinery to gate the /manage builder:
  editing a live hotel there requires an active grant for that hotel, and every
  edit is then made and audited as the actual Canary staff member. That satisfies
  Andrea's no-blanket-access requirement (which I think everyone accepts as
  non-negotiable) and Wenjun/Blake's clear-intent requirement, without the
  temp-user dance.

  On (1): the everyone-in-adminland option means CS-only capabilities (e.g. PMS
  reg-card field mapping) render inside the hotel dashboard, gated on being Canary
  staff, and are edited while impersonating a synthetic support user. Three
  problems:
  • It isn't impersonation — no hotel user has these powers. It's a CS role
  wearing a hotel-user costume, which is exactly the conflation Stephanie called
  out.
  • The audit trail attributes changes to a temporary synthetic user rather than
  the person who made them.
  • Staff-gated features inside the hotel dashboard is the legacy pattern that led
  to real security incidents and SOC 2 findings. Some such features still exist
  (Wenjun's point), but they're what we've been retiring, not a precedent to build
  on.

  On "manage must not become django admin v2": agreed with the underlying concern,
  but django admin v2 means unaudited, ungated, raw model editing. A
  product-designed builder sharing the exact same components as the adminland
  view, with writes gated by support access grants, is the opposite of that.
  "Manage as status hub only" is a fine aspiration, but as a hard rule it forces
  the CS superset into the hotel dashboard, which is worse on both security and
  auditability.

  On Andrea's frequency question: Vibhor's read is that post-live reconfiguration
  is rare (no hard data). That supports the grant model — rare enough that grant
  friction is acceptable, and too risky to justify always-on access.

  So my recommendation:
  • One shared builder codebase (already agreed)
  • Hotel-staff subset in adminland
  • CS superset in /manage, edits made as the actual staff member
  • Editing a live hotel in /manage requires an active Support Access Grant for
  that hotel
  • Impersonation reserved strictly for "see what this user sees" — never for
  editing
  • Pre-live, onboarding CS keeps its current access; grants kick in at go-live

  ### Next step

  Say "post it" (or edit first) and I'll send it to the channel; happy to also
  trim it into shorter separate messages if you prefer your usual burst style.
project: 2026-04-16T1210-unblock-team
source_id: https://canarytechnologies.slack.com/archives/C0BKDAG8FMY/p1784666772775569
tags:
- morning-gtd
- slack
time_minutes: 5
title: Weigh in on check-in configuration location debate (#tmp-check-in-configuration-location)
updated: 2026-07-28 14:08:44.548827
waiting_on: null
waiting_since: null
working_on: false
---

Stephanie laid out the /manage-vs-adminland split async last night (group still diverging; impersonation-for-editing conflation is the sticking point); Andrea asked how often CS actually reconfigures live hotels. Vibhor's saved mention (Canary-only features on prod hotels) is part of this.
https://canarytechnologies.slack.com/archives/C0BKDAG8FMY/p1784666772775569