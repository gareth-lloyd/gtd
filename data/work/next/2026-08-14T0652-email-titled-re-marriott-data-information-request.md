---
area: null
completed_at: null
contexts: []
created: 2026-08-14 06:52:20.330206
defer_until: null
due: null
energy: low
id: 2026-08-14T0652-email-titled-re-marriott-data-information-request
order: null
output: |
  ## Agent run 2026-08-14 06:57 (local)

  **Bottom line: no reply owed by you. You were CC'd for visibility only, and the
  work moved off email into Slack + the GDPR workstream within a day. The one
  thing worth checking is whether the Marriott one-pager actually went out — it
  was due Aug 12/13 and today is Aug 14.**

  ### The email
  Thread: "Re: Marriott data information request - STG Oxford street churn risk"
  (Gmail thread 19fd78f7b94527f2, last message Blake VanLandingham 2026-08-06).

  Chain: Alex Reid (Regional Director, EMEA) flagged that STG Oxford Street —
  ~£130K ARR, live on Upsells / Messaging / Kiosk / Digital Check-in / Check-out /
  AI Webchat — is transitioning to Marriott management and will churn unless
  Canary satisfies Marriott's security review. Marriott's Brandon (senior
  director) will consider a one-time exception if Canary can state, **per
  product**, which PMS fields it pulls and how the data is retained. Kiosk is
  already Marriott-approved; the ask is to show GMS handles data the same way.

  Blake's closing message assigned Dana Levine + Vibhor Sachdeva three checks
  (obfuscation running? reg cards redacted like other Marriott Kiosk properties?
  no integrations outside the PMS one?) and said **"I'll start a Slack thread as
  well."** That's why the email has no replies — it was never the venue.

  ### Where it actually went: Slack #marriott
  https://canarytechnologies.slack.com/archives/C094W051U68/p1786027980519949
  (Blake, 2026-08-06 17:53 EEST — **59 replies**, last 2026-08-07 23:21 EEST)

  The three validation checks all came back **negative**. Vibhor's tl;dr in-thread:
  1. PMS Gateway redaction was implemented but is **not working as expected**.
  2. On the Canary side **no redaction is happening on guest information** — reg
     cards still contain full guest details. Dana pulled STG reg cards from
     January and found PII still present. Vibhor found the same on Moxy
     Piccadilly (the supposed reference property) for May reservations.
  3. Logs/traces redaction still outstanding. Bernard Pietraga: his
     `PII_REDACTION_PROPERTY_ALLOWLIST` mechanism is **Groundcover/Sentry log
     redaction only** — no hotel onboarded to it, and it does not affect what's
     stored in the DB. Groundcover **traces still contain PII** (eBPF
     kernel-level collection, separate problem).

  Martijn Dekker: registration-card obfuscation was then ~2 weeks out. Vibhor's
  conclusion was that Martijn's GDPR workstream achieves the same result and
  needed expediting, with resourcing moved if necessary. Martijn booked a
  Dana/Vibhor/Martijn meeting for Monday (Aug 10).

  ### What happened after (Notion)
  - **Marriott STG GDPR** (meeting 2026-08-10) —
    https://app.notion.com/p/3b8814686151807abf00d1978a856b3e
    Decision: rather than re-send the ~V10 doc given to Marriott for Kiosk
    approval (which "contains statements not fully accurate in code today"),
    Bernard authors a **new plain-language target-state one-pager** covering, per
    product: data entry points, anonymisation/obfuscation, retention (hot logs,
    audit logs, archive), who can access retained data, configurable defaults.
    Marriott also wants 730-day audit log retention / 60-day hot logs. Explicitly
    noted as reusable for other enterprise brands (IHG). Property history: St.
    Giles → Criterion mid-pilot → now Marriott; seen internally as a "Trojan
    horse" for proving Canary works inside Marriott's security protocols.
  - **GDPR Weekly - Aug 12** —
    https://app.notion.com/p/3ba81468615180b384fbd6f6056b2549
    "Top priority this week is getting the Marriott one-pager out the door."
    **Alex Reid sends it, with Vibhor** — short email + attached PDF — "today or
    tomorrow" (i.e. Aug 12–13). Blake's formal sign-off deemed not critical.
    Bernard to double-check the data-accuracy table. Guest-messaging section to be
    reframed as "messaging is not an entry point for sensitive data; PII there is
    voluntary and unsolicited", with a timeline for extending the anonymisation
    engine to messaging threads on the 7-day anchor.

  ### Engineering thread status
  - **PMS-9895** "Guests are being created with PII set to `__redacted__` on
    upcoming reservations" —
    https://linear.app/canary-technologies/issue/PMS-9895/guests-are-being-created-with-pii-set-to-redacted-on-upcoming
    **Done** 2026-08-13, assignee Julius Seporaitis. (Bounced back to Triage
    Aug 13 03:53 then re-closed Aug 13 10:22 — worth a glance if you care whether
    the re-close was a real fix or an admin tidy-up.)
  - Related and still open-ish in the same cluster: PMS-9863 (obfuscation sweep
    erases reservation-less guests), PMS-9791 (un-obfuscate on new future
    reservation), PMS-9787 (PMS syncs re-introduce PII on obfuscated guests).
  - Per the Aug 12 weekly, Henry has obfuscation MRs open for check-in, reg card
    and additional guest; a known bug has PMS Gateway updates un-obfuscating
    previously obfuscated check-in objects.

  ### What next — options for you
  1. **Do nothing / archive.** Defensible. You were cc'd for visibility, the
     validation work completed, ownership is clearly with Alex Reid + Vibhor, and
     the deliverable is a commercial/privacy document, not an engineering one.
  2. **One-line nudge (recommended if you want to close the loop).** Ask in
     #marriott or to Vibhor whether the one-pager went out — it was due Aug 12/13
     and I found no sent mail from Alex Reid in the last 5 days on your account
     (though you would only see it if cc'd, so this is weak evidence, not proof).
  3. **Engineering angle, if you want one.** The Aug 12 weekly flagged that
     international-vs-local anonymisation scheduling has **no owning team** (Amir
     pod vs APAC pod unresolved; Annie's team ~1 month out) and needs a PRD from
     Sebastian Cahill + James Saram. That's the actual unassigned work in this
     area, and it's adjacent to your EMEA/country-code work.

  ### Caveats
  - No writes made anywhere — Gmail, Slack, Notion and Linear were read-only.
  - I could not confirm the one-pager was sent; absence of evidence in your
    mailbox is not proof it didn't go.
  - Slack thread content is quoted as written by participants; I did not
    independently verify the redaction claims against the code.
project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 5
title: 'Email titled: "Re: Marriott data information request - STG Oxford street churn
  risk"'
updated: 2026-08-14 06:58:16.005656
waiting_on: null
waiting_since: null
working_on: false
---

* Notion or Slack search for relevance
* Email has no replies. What next?