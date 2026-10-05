---
area: null
completed_at: 2026-10-05 11:04:40.499613
contexts: []
created: 2026-10-01 11:03:40.084410
defer_until: null
due: null
energy: low
id: 2026-10-01T1103-quote-detail-should-be-able-to-book-before-sent-to
order: null
output: |
  ## Agent run 2026-10-01

  **Short answer:** the gate is deliberate but not a product decision — it was the
  cheapest fix for a bug on 2026-06-11, and the legacy app had no such rule.
  Lifting it is a small, well-contained change (recommended shape below).

  ### Where the gate lives (both layers)
  - Frontend: `frontend/src/features/quotations/QuotationDetailLayout.tsx:96`
    `canBook = canWrite && quotation.status === "sent"`. Comment above it:
    "Booking requires the guest to have actually received the quote (sent)."
    Pinned by `QuotationDetailLayout.test.tsx:330` ("row Book is disabled on a draft
    quote and enabled once sent").
  - Backend: `POST /quotations/{id}:convert` (`views/quotation.py:245-316`) calls
    `Quotation.accept()`, whose transition table (`reservations/enums.py:146-162`)
    only allows SENT -> ACCEPTED. DRAFT convert -> 409 `invalid_transition`. Pinned by
    `test_convert_draft_quotation_409s` (`tests/test_api_quotations.py:3159`).

  ### Why it exists
  - Commit 5194ff8d (2026-06-11) "guard quotation lifecycle against post-send
    mutation". The bug: `:convert` used to skip `accept()` for any non-SENT status
    but still create the booking, so converting a DRAFT produced a live booking with
    the quote stuck in DRAFT and the enquiry never CONVERTED. The fix chose
    "require SENT" rather than "allow DRAFT -> ACCEPTED". FE gate landed the same
    day (2be2ec2f). No entry in `decisions.md`; no ticket argues for it.
  - Legacy ResSystem: no equivalent. `VillaQuotationMaster` has no status/sent
    column at all; a booking is created with a QuotationNo with no "sent" check.
    So this is a rebuild-only limitation.

  ### What silently relies on SENT having happened first (must be handled if lifted)
  1. Zoho push (GAP-100): `_push_transition_to_zoho` (`models/quotation.py:48-67`)
     only pushes when prev status == SENT, because send is the only path that
     creates the CRM Quote. A raw DRAFT -> ACCEPTED would never push the quote to
     Zoho (booking push still fires; Limitless' Flow tolerates a missing quote,
     but the CRM would be missing the quote record permanently).
  2. Enquiry status: send flips the enquiry to QUOTE_SENT; accept flips to CONVERTED
     only if allowed. NEW -> CONVERTED is NOT in the enquiry table (`enums.py:30-37`),
     so a DRAFT -> ACCEPTED on a fresh enquiry would leave the enquiry at NEW.
  3. Audit trail: the "quote sent" EnquiryEvent (send_path smtp/manual) would never
     be written for a quote booked straight from draft.
  4. `expires_at` is set at send (+90d) — irrelevant once accepted. `terms_version`
     is set at quote creation, not send — fine.

  ### Current workaround
  "Mark manually sent" (`POST :mark-manually-sent`) then Book. Two clicks; all
  bookkeeping above happens correctly.

  ### Recommended fix (small)
  Keep the state machine; make Book from DRAFT do the manual-send step implicitly.
  Rationale: a phone/in-person booking still means the guest received the quote
  (verbally), so `send_path=manual` is semantically honest and every downstream
  hook (Zoho quote push, enquiry QUOTE_SENT -> CONVERTED, audit event) keeps
  working with zero changes to the transition tables.
  - Backend: in `:convert`, if `quotation.status == DRAFT`, call
    `quotation_transmission.record_quote_sent(quotation, send_path=SEND_PATH_MANUAL,
    actor=request.user)` inside the same `transaction.atomic()` before `accept()`.
    Flip `test_convert_draft_quotation_409s` into a positive test asserting
    booking created + quote ACCEPTED + enquiry CONVERTED + manual send audit event.
    EXPIRED/CANCELLED stay 409.
  - Frontend: `canBook = canWrite && (status === "draft" || status === "sent")`
    (i.e. `canBook = canWrite && quoteEditable`), update the test at line 330,
    and optionally note in the Convert dialog that booking a draft will also mark
    it as sent.
  Alternative (not recommended): add DRAFT -> ACCEPTED to the table and special-case
  the Zoho push + enquiry NEW -> CONVERTED; more moving parts for the same outcome.

  Estimated effort: ~1-2h incl. tests. No `decisions.md` change needed, but worth a
  one-line note there that "Book from draft implies manual send".

  ## Agent run 2026-10-01 (follow-up)

  Filed as **BUG-050** at `django_res_design/todo/bug-050-quote-book-blocked-until-sent.md`
  (INDEX row + scoreboard recount: 60 open), committed on main as f16ef565.
  Numbered 050 because a concurrent session was filing BUG-049 (security-deposit
  track card) at the same time; that session's uncommitted work was left untouched.
project: 2026-05-25-villa-collective
source_id: null
tags: []
time_minutes: 5
title: Quote detail. Should be able to Book before 'sent to guest'
updated: 2026-10-05 11:04:40.499589
waiting_on: null
waiting_since: null
working_on: false
---

Not sure why this limitation exists