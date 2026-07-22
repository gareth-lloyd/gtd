---
area: null
contexts: []
created: 2026-07-21 12:05:23.120983
defer_until: null
due: null
energy: low
id: 2026-07-21T1205-find-guest-profile-prd-from-kevin-li
order: null
output: |
  ## Agent run 2026-07-21T14:53

  **Found it — the "guest profile" PRD:**

  - **PRD: Guest Profiles** — https://app.notion.com/p/27681468615180f8a62eed8ae716b758
    - Best match. A full product requirements doc to let returning guests store
      personal info, ID, payment, and preferences in a secure Guest Profile for
      one-click / faster check-in.
    - Last edited ~2026-05-13 (~2 months ago).

  **Caveat on authorship:** Kevin Li's name is NOT in the page's metadata/properties,
  so I could not directly confirm he authored it. He shows up as a Canary product
  leader in adjacent search results, but treat "authored by Kevin Li" as unverified —
  worth a quick confirm with him or by checking the page's edit history.

  **Companion working docs (same feature):**
  - Guest Profiles / Guest Profiles (1) — https://app.notion.com/p/33e81468615180f6a3b5f12673d5182d
    (most recently edited 2026-07-16). Use the PRD above as canonical.

  **Key contents / decisions in the PRD:**
  - Unique identifier = Email + Name + hotel/brand; profiles stored at hotel level
    (brand/group level only with explicit buy-in).
  - Hotel/brand owns the data (controller); consent + MFA required at creation;
    profiles do NOT cross US/EU/APAC environment boundaries; no auto-linking of past
    reservations without explicit guest action.
  - MVP = guest-facing flow only, one brand/group, basic info + auto-fill + opt-in;
    staff UI and loyalty integrations are Phase 2+.

  **Open / TBD:** monetization, privacy/security, compliance (PCI, regional), and
  whether to integrate with PMS profiles. GTM proposed as a Capella-style pilot.

  Source: Notion (via notion-context skill).

  ## Agent run 2026-07-21T15:18 — GDPR review of the Guest Profiles PRD

  Reviewed **PRD: Guest Profiles** (https://app.notion.com/p/27681468615180f8a62eed8ae716b758)
  through a GDPR lens, using the **EMEA GDPR Program vs Guest Memory Strategy —
  Alignment Map** (https://app.notion.com/p/39e814686151814d95cde39f7a0d5caf) as the
  compliance frame. That map already did a lot of the legal legwork (Cooley/Tanya Chib
  counsel notes 2026-05-13, https://app.notion.com/p/38a81468615180b29833f805abe423ed;
  PII Minimisation & Retention PRD, https://app.notion.com/p/35d814686151815a96cfcf07ae7edc35).

  **Bottom line:** the PRD's instincts are right (opt-in + consent + MFA, hotel is
  controller, no auto-linking without consent, no cross-environment transfer). But every
  GDPR-load-bearing section is still "TBD," and the product's *durable, aggregating,
  monetisable* profile is on a direct collision course with the EMEA purge program that
  ships **July 23 -> Aug 28**. The compliance framing needs to be settled *before* that
  framework's anchors/exemptions are frozen, not after.

  ### The headline conflict (read this first)
  The EMEA program is building irreversible, **reservation-anchored** PII purge (name,
  email, phone, address, DOB, ID, signature overwritten X days after departure/check-in).
  A Guest Profile is by definition **durable and reused across stays** — and post-stay
  rebooking (sending to guests with no active reservation) is already committed on the
  roadmap. A reservation-anchored purge and a persistent profile cannot both be true for
  the same guest record. The map's current stance is "exclude EMEA from guest profiles
  entirely," but Cooley already said **opt-in profiles are GDPR-compliant, intra-portfolio
  reuse is fine with consent, ~3yr retention + reminder email is the recommended pattern.**
  So the profile is legal — but the PRD must define its own retention clock and a
  **distill-before-purge** hook, or the purge service will erase the very data the profile
  depends on. There is an open Cooley action to "review guest profiles when more details
  are available" — the PRD is that detail; book the follow-up.

  ### Findings by GDPR principle (roughly prioritised)

  1. **Lawful basis / purpose limitation (Art 5(1)(b), 6) — biggest gap.** The PRD bundles
     three very different purposes under one opt-in: (a) faster check-in autofill
     (contract/consent), (b) in-stay personalisation & upsells, (c) explicit **monetisation
     / re-targeting / targeted loyalty campaigns** ("Goals" + "Monetization" sections).
     (b) and (c) are secondary purposes that need their own **granular, separately-toggled**
     consent — a single "save my details for faster check-in?" prompt cannot lawfully cover
     marketing/retargeting. Fix: separate consent toggles; don't gate check-in on accepting
     marketing.

  2. **Special-category data (Art 9).** Profiles store **allergies / dietary needs** =
     health data, and ID documents reveal nationality. Art 9 requires *explicit* consent
     and heightened handling; the PRD never flags this. Cooley confirmed allergy data is
     permissible *with consent* — so make that consent explicit and separable.

  3. **Storage limitation / retention (Art 5(1)(e)) — currently absent.** "Data storage and
     deletion procedures? … we continue to operate the way we do." No retention period is
     defined for the profile. Adopt Cooley's **~3 years after last guest activity + reminder
     email** pattern, and reserve the config now (map's ask: a `profile_retention_*` sibling
     with a **"months after last activity"** anchor — the program only has reservation-bound
     anchors today). Reserving it pre-Jul-23 is trivial; retrofitting after the purge service
     ships is a migration + policy renegotiation.

  4. **Right to erasure & withdrawal of consent (Art 7(3), 17).** Deletion today = "guest
     asks the hotel, hotel asks Canary" — manual, no SLA, no self-service. Art 7(3) requires
     withdrawal to be **as easy as giving** consent, and Art 17 requires action without undue
     delay (~1 month). At minimum define an SLA'd process and a consent-withdrawal path;
     ideally the "Profile Management (guest can opt out/delete)" item moves out of Future.

  5. **Consent/suppression carve-out (Art 21 / ePrivacy / TCPA) — cross-cutting risk.** This
     is the map's point 2 and it bites profiles directly: if a profile or the purge overwrites
     phone/email, a prior **STOP/opt-out** state can be severed from the guest, so a later
     rebooking invite goes to someone who opted out. Opt-out/consent-provenance must live in
     a **non-obfuscatable store keyed by phone/email+channel+property**, exempt from profile
     merges and purges. Objections bind indefinitely; suppress, don't delete.

  6. **Profiling / automated decisions (Art 22) — the "watch list" feature is the sharpest
     edge.** Future scope lists **inclusion/exclusion lists, flagging "bad actors," and
     "Canary would be able to identify these bad actors."** Cross-hotel denial-of-service
     flags are exactly Art 22 automated decisions with legal/significant effect, plus serious
     **accuracy (Art 5(1)(d))** and fairness exposure — and they blow past Cooley's caveat
     that a PIA is minimal *only if profiling affects experience quality*. Keep this well
     out of the guest-profile lawful-basis story, or treat it as a separate, heavily-gated
     workstream.

  7. **Data minimisation & third-party data (Art 5(1)(c), 6).** Profiles store reg-card data,
     ID, CC, **all reservations + metadata, prior message threads, add-ons, loyalty, notes,
     and "linked profiles (accompanying guests)."** Companion/accompanying guests never went
     through the consent flow — capturing them as linked profiles processes third parties'
     data without a basis. Justify each field against purpose; drop or separately-base
     companion linkage and stored message bodies.

  8. **Controller / processor posture (Art 28) — drifting.** PRD correctly says the hotel is
     controller and Canary the processor. But (a) the map flags that Canary centrally setting
     retention defaults is the "manufactured-instruction" pattern that undermines processor
     protection, and (b) the PRD muses about eventually storing profiles "at a Canary level…
     we also become a consumer brand… changes the data ownership model." Monetisation +
     Canary-level profiles would make **Canary a controller** and require re-papered DPAs.
     Keep it hotel/portfolio-controller for now; record hotel retention *elections* rather
     than imposing defaults.

  9. **DPIA (Art 35) — required, not "TBD."** Large-scale profiling + special-category data
     + potential exclusion lists = a DPIA is almost certainly mandatory. "Privacy/security:
     TBD, Compliance: TBD" is the single biggest documentation gap. Commission the DPIA as
     part of MVP scoping and take it to Cooley.

  10. **Cross-border (Ch V) — looks fine, verify.** "Guest profiles will not cross environment
      boundaries (US/EU/APAC)" is the right call; confirm no support/ops access reaches EU
      data from outside the region.

  ### What's already good (keep)
  - Opt-in + consent + MFA at creation; hotel as controller.
  - Explicit "do **not** auto-link previous reservations on name/email/phone match without
    consent" — directly serves accuracy (Art 5(1)(d)) and avoids mis-identification.
  - No cross-environment transfer; hotel-level (not Canary-wide) default storage.

  ### Recommended next steps
  1. Before **Jul 23**, get the profile into the EMEA framework conversation with Martijn
     Dekker (program owner): reserve a `profile_retention` sibling config + "months since
     last activity" anchor, a distill-before-purge hook, and the consent/suppression carve-out.
  2. Replace every "TBD" in the PRD's Privacy/Compliance/Deletion sections with concrete
     positions: lawful basis per purpose, Art 9 explicit consent, retention (~3yr+reminder),
     erasure SLA, DPIA commitment.
  3. Split the marketing/monetisation/retargeting and watch-list/exclusion features into
     separately-based (or separately-gated) workstreams — do not let them ride the check-in
     consent.
  4. Draft the profile spec (tiers, granular consent, retention) and book the standing Cooley
     follow-up to convert their in-principle "profiles are compliant" into a signed-off design.

  Source: Notion (Guest Profiles PRD + EMEA GDPR Alignment Map). Legal points attributed to
  the Cooley/Tanya Chib counsel notes as summarised in the Alignment Map — confirm verbatim
  with the source before quoting to counsel.
project: null
source_id: null
tags: []
time_minutes: 5
title: Review the guest profiles document thorugh a GDPR lens
updated: 2026-07-21 15:18:00.000000
waiting_on: null
waiting_since: null
working_on: false
---

https://app.notion.com/p/canarytechnologies/EMEA-GDPR-Program-vs-Guest-Memory-Strategy-Alignment-Map-39e814686151814d95cde39f7a0d5caf?source=copy_link&utm_content=39e81468-6151-814d-95cd-e39f7a0d5caf&utm_campaign=T4PJH2UQL&n=slack&n=slack_link_unfurl&pvs=6