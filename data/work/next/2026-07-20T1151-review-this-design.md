---
area: engineering
contexts: []
created: 2026-07-20 11:51:15.898540
defer_until: null
due: 2026-07-21
energy: medium
id: 2026-07-20T1151-review-this-design
order: null
output: |
  ## Agent run 2026-07-21T12:46:00

  **What this is:** Martijn Dekker's draft eng design for the **Canary GDPR Obfuscation Service** (EMEA-354).
  - Slack: https://canarytechnologies.slack.com/archives/C0AB9E7AE59/p1784537452382449
  - Notion design: https://app.notion.com/p/canarytechnologies/Canary-Obfuscation-Service-3a2814686151815ea78bc317e5a426a8
  - Linear ticket: https://linear.app/canary-technologies/issue/EMEA-354/gdpr-eng-design-obfuscation-service-framework
  - Project: https://linear.app/canary-technologies/project/gdpr-user-input-data-anonymisation-ef83a5a80e32/overview

  **TL;DR:** Solid, well-scoped design. Port the pms-gateway `gdpr/` framework into Canary, add an
  irreversible-overwrite toolkit (`ObfuscatableModel` + `obfuscatable_field` + worker), and three triggers
  (scheduled sweep / follow PMS-gateway sync / on-demand DSAR). Recommendations lean simple and are mostly
  right. I verified the load-bearing claims against the codebase — they hold, with one field-name snag.

  ### Verified against the code
  - `backend/pms-gateway/gdpr/` exists and `ObfuscatableModel`/`obfuscatable_field` are already in use on
    `reservations/models/guest_information.py` — the "port an existing working framework" premise is real.
  - `check_in.Configuration` has `id_retention_days` (`security/services/identity_document_purge_service.py`),
    so a sibling `pii_retention_days` fits the established pattern. `pii_retention_days` does **not** exist yet.
  - Rule engine `OverridePolicy.FINAL` + general-rules + startup checks all exist and are used (enterprise_ihg,
    enterprise_best_western). The "legal floor CS can't drop below" mechanism is sound and already precedented.

  ### Concerns worth raising on the doc (ranked)
  1. **`hotel.country` vs `hotel.country_code` (correctness bug in §6.4).** The prose says the sweep "reads the
     floor straight from `_PII_RETENTION_FLOOR` keyed on `hotel.country`". `hotel.country` is a free-text
     `CharField(max_length=255)` (`hotels/models/hotel.py:544`) — unreliable ("USA"/"US"/"United States").
     The **canonical** field is `hotel.country_code` (a `Country` enum, `hotel.py:514`), and the rule engine
     already resolves on it (`rules_based_configuration/services/hotel_attributes.py:57` →
     `country=hotel.country_code`; matched in `conformity.py:155`). Two follow-ons: (a) the `_PII_RETENTION_FLOOR`
     dict keys ("FR","DE") must match the `Country` enum serialization, not free text; (b) define the fallback
     when `country_code` is null/unknown — it must **fail safe** (longest retention / explicit default), never skip.
  2. **§6.4 describes two competing sources of truth for the floor.** One path is the rule engine general rule
     (`OverridePolicy.FINAL` writes the resolved `pii_retention_days`); the other is the sweep reading
     `_PII_RETENTION_FLOOR` directly. Pick one. If the rule engine already resolves + enforces the value, the
     sweep should read the *resolved* `pii_retention_days`, not re-derive from the dict — re-deriving duplicates
     the source of truth and is exactly where the country-field bug in (1) creeps back in.
  3. **DSAR subject matching is weak for an irreversible op (§4 example, §11 Q3).** `get_subject_queryset`
     matches `guest_email=subject.email OR guest_name=subject.full_name`. Over-match → you irreversibly erase a
     *different* guest with the same name (no undo). Under-match → incomplete legal erasure (variant email, name
     formatting, encrypted-field equality). A DSAR needs a stronger identity-resolution story than free-text
     equality; this is the riskiest correctness surface in the design and deserves its own section.
  4. **No safety rail on the irreversible scheduled sweep (§6.3).** Recommendation B gives the nightly sweep the
     lightweight path (no dry-run). Given a bad country→floor mapping could mass-destroy *recent* data with no
     recovery, add a bounded rail even without full dry-run: a per-run row-count ceiling / anomaly guard, or a
     canary first-run. Cheap insurance against a config typo becoming an irreversible incident.
  5. **Free-text-value PII isn't addressed (§2 JSON_KEY_SCRUB, §8 audit payloads).** Key-based JSON scrub only
     redacts *known keys*. Chat messages, form free-text, "notes" fields carry PII in the *values* (a guest
     types a passport number into a comment). That's the hardest slice and the doc defers chat/forms to later
     surfaces — fine, but the framework should acknowledge value-level PII is out of scope for key-scrub and say
     how those surfaces will handle it.
  6. **Idempotency under partial failure — confirm all strategies are safe to re-run.** Worker scrambles fields
     then stamps `obfuscated_at`; a crash between them leaves `obfuscated_at IS NULL`, so the row is re-swept.
     Hex-overwrite and JSON-scrub are idempotent; `IMAGE_BLOB_DELETE` re-deleting an already-gone S3 object
     should be a no-op — worth stating the transaction boundary and that every strategy tolerates retry.
  7. **Default contradiction.** §6.4 says a default "active on every hotel"; §10 says v1 ships "a single
     turned-off default". And `PiiPurgeStrategy` defaults to `SCHEDULED` (on). Reconcile — is v1 sweeping or not?

  Strengths worth keeping: `obfuscated_at IS NULL` first-writer-wins idempotency is clean; reusing the existing
  ID-doc purge cron + gateway framework is the right call; the per-surface adapter (due-rows / subject-rows) is
  a tidy seam; out-of-scope list (§10) is disciplined; the rule-engine legal-floor-that-CS-can't-undercut is elegant.

  ### Recommended reviewers (from git ownership of each touched surface)
  - **PMS-Gateway GDPR framework (the code being ported)** — **Ryan Rogers**, **Ramiro Nieto** (top authors of
    `pms-gateway/gdpr/`). They'll catch divergence from the reference impl and know the primitives' sharp edges.
  - **Rules-based configuration / Conformity (riskiest coupling: floors via FINAL + startup check)** —
    **Dana Levine** (spans both `check_in` config *and* `rules_based_configuration` — strongest single
    cross-cutting reviewer here) and **rmoreira-bit**.
  - **Identity-document purge cron this mirrors (+ EMEA-356 surface)** — **Federico Mazzoni-Durán**, **Patrick Canny**.
  - **Reservation ingestion / the Trigger-2 sync hook** — **Renne Rocha**.
  - **Chat & messaging (EMEA-360, the free-text-value PII surface)** — **Jonathan Sandoval**.
  - **Legal/Privacy stakeholder** — the "irreversible overwrite = GDPR no longer applies" claim and DSAR
    completeness are legal positions, not just eng. Get sign-off from whoever owns the GDPR project legally.

  ### Kiosk? — Yes.
  Kiosk is an explicit v1 surface (EMEA-357; §6.2 lists it under Canary-native PII), plus unlinked/abandoned
  kiosk sessions are their own ticket (EMEA-362). Recommend **Federico Mazzoni-Durán** — he's *both* a top
  `kiosk/` author and a top author of the identity-doc purge service, so he covers kiosk + the ID-doc pattern in
  one reviewer. **Matt Jeffery** is the alternate kiosk owner.

  ### Suggested next step (not taken — needs your go-ahead)
  I did not post anything to Slack/Notion/Linear. If you want, I can draft a Slack thread reply to Martijn
  surfacing points 1–3 (country_code, single-source-of-truth, DSAR matching) and tagging the reviewers above —
  say the word and I'll show you the exact text before sending.
project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 15
title: review this design, and recommend other reviewers. Kiosk?
updated: 2026-07-21 14:53:06.554870
waiting_on: null
waiting_since: null
working_on: true
---

https://canarytechnologies.slack.com/archives/C0AB9E7AE59/p1784537452382449