---
area: null
contexts:
- react
created: 2026-05-25 04:15:51.717452
defer_until: null
due: null
energy: medium
id: 2026-05-25T0415-triage-ent-queue-5-tickets-in-triage
order: null
output: |
  ## Agent run 2026-05-25T11:55Z

  Triage notes for the 5 ENT tickets currently in Triage. No external writes
  made — recommendations only; final routing is your call.

  ### ENT-6311 — BW Missing Contact Details (prod us-west-2) — Medium prio
  - Datadog auto-filed alert. Monitor threshold is very low (>=2 events / 1h
    on `validate_membership_guest.missing_contact`). 2 events triggered it
    on 2026-05-24 16:05 UTC.
  - This is almost certainly background noise: BW enrollment requires email
    or phone, and some guest folios genuinely arrive without either. 2
    events/hr is not a spike.
  - **Recommendation:** Move out of Triage. Either:
    (a) close as "monitor noise / expected" and bump the monitor threshold
        (e.g. >=20/h or >=50/day) — long-term fix is to tune the alert; OR
    (b) drop to Low and bucket under an existing BW membership-gateway
        hygiene project.
  - Loosely related to [[project_pmsx419_bw_membership_push]] (different
    failure mode: there it's missing capability, here it's missing PII).

  ### ENT-6310 — routing-service env-aware redirect (LOGIN_HOST) — No prio
  - Well-specified by Jordan Sterling. Two-part change in `routing-service`
    + canary-kubernetes values. Blocks ENT-6295 (OAuth integration test
    against staging). Part of "Api Authentication" project.
  - This is real engineering work, not triage. Ready to be picked up.
  - **Recommendation:** Set priority Medium, leave assigned to Api
    Authentication project, move to Backlog/Todo. Reasonable for you to own
    given the existing OAuth work on this branch
    (glloyd/ent-6204-oauth-login-page) — same area, same context.

  ### ENT-6308 — Grant Meudy Araujo access to Villas at Doral — Low prio
  - Internal access request from Rachel Smoller. Admin task. SLA high-risk
    2026-05-28, breaches 2026-05-29 — needs action within ~3 days.
  - **Recommendation:** Route to oncall (already labeled "Oncall"). Do not
    self-assign — this is a standard admin grant best handled by whoever is
    on the access-request rotation. If oncall isn't picking it up, you can
    do the grant via canary-admin (user 3952213, hotel 129250001) — but
    flag to ops first; it's not yours by default.

  ### ENT-6302 — Autoclerk manual check-in not working (test lab) — No prio
  - Hotel bw-00821, confirmation 821018949. Auto-pulled reservations work;
    "force create" does not. Submitted by Melissa Fairchild from QA/test
    lab.
  - This is a real bug if the manual create flow is broken for Autoclerk —
    but it's in test lab, not customer-facing prod. Need to determine:
    (a) is this a regression in the check-in create flow, or (b) is it
    Autoclerk-specific (PMS capability/permissions), or (c) is the test
    lab PMS misconfigured?
  - **Recommendation:** Set Medium, assign to whoever owns Autoclerk
    integration / check-ins. Ask Melissa for the exact error message /
    network response from the screenshot before deep-diving — the
    attached screenshot may have it but I didn't fetch it.

  ### ENT-6298 — Four Seasons Chinese Simplified dashboard — Low prio
  - Feature request from Taylor Kirchwehm. 12 China-based FS properties
    moving off Shiji onto Canary auth/payments alongside Opera Cloud
    migration. Need zh-CN translation of dashboard, scoped to Auth +
    Payments. Target: by end of 2026.
  - This is a product/localization initiative, not a triage item. Scope is
    big (translation infrastructure + new locale + QA) and needs PM scoping
    against existing zh-Hans coverage.
  - **Recommendation:** Move out of Triage into Backlog / a Localization
    project. Loop in PM (Taylor) to confirm scope and timing. Do not start
    work — needs sizing first.

  ### Suggested batch action
  - ENT-6311: lower noise / close as monitor tuning
  - ENT-6310: → Backlog (Medium), Api Authentication project, you to own
  - ENT-6308: → Oncall queue; do not self-assign
  - ENT-6302: → Medium, Autoclerk owner; request error details from
    reporter
  - ENT-6298: → Backlog under Localization; PM to size

  All of the above are recommendations only. No Linear updates made.
project: null
source_id: linear://ent-triage-queue-2026-05-25
tags:
- morning-gtd
- linear
time_minutes: 30
title: Triage ENT queue (5 tickets in Triage)
updated: 2026-05-25 11:46:58.581442
waiting_on: null
waiting_since: null
working_on: false
---

ENT-6311 BW Missing Contact Details (prod), ENT-6310 routing-service env-aware, ENT-6308 Get User access, ENT-6302 Autoclerk check-in, ENT-6298 Four Seasons Chinese Simplified.