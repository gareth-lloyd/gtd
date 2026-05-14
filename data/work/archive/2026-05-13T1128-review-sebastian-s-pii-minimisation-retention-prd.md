---
area: null
contexts:
- deep
created: 2026-05-13 11:28:24.627380
defer_until: null
due: null
energy: high
id: 2026-05-13T1128-review-sebastian-s-pii-minimisation-retention-prd
order: null
output: '## Agent run 2026-05-13T09:20:00Z


  Reviewed V2 of Sebastian''s PII Minimisation & Retention PRD (Notion: 35d814686151815a96cfcf07ae7edc35).
  Cross-referenced against actual codebase: identity_document_purge_service.py, CheckInConfiguration
  retention fields, EventableModel/Event payload storage, PMS Gateway ObfuscatableModel,
  and safe_backfill_iterator. Overall the PRD is well-structured, V2 improvements
  (two-track split, incorporated feedback, elevated Snowflake) are solid. Below are
  substantive review comments organized by priority.


  ### High — things that will bite if not addressed before engineering starts


  **1. Event payload PII is harder than a line item**

  The PRD correctly flags that "obfuscation pass must walk event payloads." But the
  `Event.payload` is a freeform JSONField — there''s no schema governing what''s inside.
  Each EventSpec defines its own payload structure via dataclass→dict serialization.
  Walking these payloads to find and obfuscate PII means either (a) enumerating every
  EventSpec that captures guest data and building per-spec obfuscation logic, or (b)
  doing a brute-force field-name scan across JSON keys. Neither is trivial. This deserves
  its own line item in the estimate — it''s probably 2-3 days on its own, and it''s
  easy to miss fields.


  **2. Comprehensive field inventory is missing**

  The PRD says "name, email, phone, address, DOB, signature, ID doc images, OCR''d
  ID fields, selfie" but doesn''t map these to specific Django models and fields.
  The existing ID doc purge explicitly enumerates `IDENTITY_DOCUMENT_FIELDS` on CheckIn
  and `ADDITIONAL_GUEST_IDENTITY_DOCUMENT_FIELDS` on AdditionalGuestDetails. The new
  PII purge needs the same treatment — which fields on Reservation, CheckIn, AdditionalGuestDetails,
  KioskSession, RegistrationCard, Guest (if applicable), and any other model? This
  inventory is a prerequisite for estimation accuracy and should be an appendix to
  the PRD.


  **3. "Hours after submission" anchor — UX risk**

  This is new in V2 and is the most aggressive trigger. If PII is purged hours after
  submission, what happens when:

  - Guest returns to edit their registration card?

  - Hotel staff need to verify guest identity at front desk?

  - A partially-completed check-in flow resumes?

  The PRD doesn''t address these UX edge cases. "Hours after submission" of _what_
  — the initial reg card? The full pre-check-in completion? This needs tighter definition
  or it''ll create support chaos.


  **4. Snowflake as "core flow" — scope creep signal**

  V2 elevates Snowflake from a Phase 2 downstream audit to "must be part of core GDPR
  flow." But the PRD doesn''t specify _how_ obfuscation propagates to Snowflake. Does
  Canary use CDC streams? ETL batch jobs? Fivetran? If the CDC pipeline carries raw
  column values, then obfuscating in Canary DB should automatically propagate. But
  if there''s a snapshot/ETL that runs independently, it needs its own purge logic.
  This could be the long pole and needs investigation before committing to "core flow"
  scope.


  **5. Guest-facing experience post-obfuscation**

  Not addressed: if a guest clicks their check-in link after PII has been obfuscated,
  what do they see? An error? A blank form? "Your data has been removed"? This matters
  especially for the "hours after submission" anchor where the guest may still expect
  to interact with their submission.


  ### Medium — should be addressed but won''t block engineering kickoff


  **6. AI chat / messaging history**

  Guest PII likely exists in AI chat conversation history and stored message templates
  (SMS/email with guest name interpolation). Are these in scope? If not, they should
  be called out explicitly in "Out of Scope" so there''s no ambiguity.


  **7. Authorization forms**

  Payment authorization forms contain guest PII (name, sometimes address). Are these
  in scope for obfuscation or handled separately? Given authorizations have their
  own retention requirements (chargebacks can come 120+ days later), they likely need
  different treatment. Worth calling out.


  **8. Monitoring / alerting gap**

  The existing ID doc purge has retry logic via cron task (`retry_pending_identity_document_purges`).
  The PRD should specify equivalent observability for the new PII purge: dashboard
  for purge lag, alerts for failure rates, SLA for time-from-trigger-to-obfuscation.
  "Verifiable via audit" is listed as a success metric but no tooling is specified.


  **9. Estimate for Track 1A feels tight**

  ~2 weeks total for core obfuscation + retention config + dashboard, given:

  - Field inventory across multiple models

  - Event payload walking (see #1)

  - Signature S3 replacement (needs PruneService integration)

  - Three retention anchors with different clocks

  - Edge cases (partial check-ins, additional guests)

  - Testing

  I''d budget 3 weeks to be safe, especially if event payloads are in scope.


  **10. Re-ingestion blocking (Track 2A) — "Option 1 vs Option 2" framing**

  Option 1 (purge everything after full pre-check-in) at 2 weeks vs Option 2 (field-level
  mapping) at 2 months. The PRD should make a recommendation, not just list options.
  Option 1 is clearly the right starting point — it''s simpler and addresses the Danubius
  requirement. Option 2 is an optimization that can come later if needed. State this.


  ### Low — polish / nice-to-have


  **11. Existing two-phase purge pattern**

  The ID doc purge uses mark-then-delete (id_marked_for_purge_at → async S3 → id_purged_at).
  The PRD should explicitly say whether the new PII purge follows the same pattern
  — I assume yes for signatures (S3 objects) but database field obfuscation could
  be single-phase. Clarifying this up front avoids design ambiguity.


  **12. Backfill rate limiting**

  When an EMEA property first enables retention and has thousands of historical reservations
  past the retention window, the purge job shouldn''t hammer the database. The `safe_backfill_iterator`
  pattern with batching handles this, but it''s worth a sentence in the PRD acknowledging
  the backfill-on-first-enable scenario.


  **13. V1→V2 joinability deferral is the right call**

  The decision to defer cross-property pseudonymous joinability avoids significant
  cryptographic complexity (per-group keying, salt rotation) for a requirement nobody
  is currently asking for. Good call.


  ### Open questions I''d want answered before starting


  - Q1 (Legal) is genuinely blocking — obfuscation vs deletion changes the entire
  architecture

  - Q7 (CX workflow) is the real rollout gate, agree it''s blocking

  - Q9 (Martijn on PMS Gateway) — also blocking for Track 2A

  - NEW: Who owns the Snowflake data pipeline and what''s the propagation mechanism?

  - NEW: Is AI chat conversation history in scope?

  - NEW: What''s the guest-facing UX post-obfuscation?


  ### Bottom line

  Strong PRD. V2 is a meaningful improvement over V1. The two-track structure is clean.
  Main gaps are: field inventory, event payload complexity underestimated, guest-facing
  UX unaddressed, and Snowflake propagation mechanism undefined. Ready for engineering
  design once Legal answers Q1 and the field inventory is complete.

  '
project: null
source_id: https://canarytechnologies.slack.com/archives/C0AB9E7AE59/p1778592214733509
tags:
- morning-gtd
- slack
time_minutes: 45
title: Review Sebastian's PII Minimisation/Retention PRD (Notion)
updated: 2026-05-13 13:41:56.102878
waiting_on: null
waiting_since: null
working_on: false
---

Sebastian @-mentioned me with the PII PRD link in #epd-emea-engineers. Foundational for Danubius GDPR. https://canarytechnologies.slack.com/archives/C0AB9E7AE59/p1778592214733509