---
area: null
completed_at: null
contexts: []
created: 2026-10-01 10:21:52.327093
defer_until: null
due: null
energy: low
id: 2026-10-01T1021-usability-of-property-finance-screen
order: null
output: |
  ## Agent run 2026-10-01T10:30 (local)

  **Fixed and committed on main:** `11ba6fb3` — fix(frontend): property finance save no longer nulls non-null text fields.

  **Root cause (frontend only, backend is fine):**
  - The Finance form (`frontend/src/features/properties/tabs/SettingsTab.tsx`) runs `blankToNull` on submit, mapping every `""` to `null`.
  - `notes`, `tax_number` and `commission_note` are `TextField(blank=True)` on `PropertyFinance` (not `null=True`), so DRF rejects `null` with "This field may not be null." The sibling Settings form never hit this because its text field (`min_nights_rental_note`) is `null=True`.
  - `commission_note` has no input on the screen but was still in the write schema/defaults, so it was sent as `null` on every save — hence "always".
  - `tax_number` had the same latent bug (only hidden when a tax number is filled in).

  **Change:**
  - Removed `commission_note` from `propertyFinanceWriteInputSchema` and `financeDefaults` — PATCH no longer touches it (read-only on this screen, as requested).
  - `blankToNull` takes an optional keep-blank set; the Finance form keeps `notes` and `tax_number` as `""` while nullable decimals/FKs/choices still clear to `null`.
  - Regression test in `SettingsTab.test.tsx`: clearing Finance notes PATCHes `notes: ""`, `tax_number: ""`, no `commission_note` key, and `security_deposit_amount: null`.

  **Quality gate:** properties vitest suite 560/561 passing; tsc, eslint, prettier clean; pre-commit hooks passed.
  - Pre-existing unrelated failure (also fails on clean main before this commit): `RateWorkbenchPage.test.tsx` › "opens the period dialog prefilled with the day after the latest period and creates" — "Unable to find an element with the text: Autumn". Looks date-dependent; not touched here.

  **Not done / for you to decide:**
  - Backend left as-is: the API correctly treats `""` as empty for these columns. If you'd rather the API also tolerate `null` for blank-only text fields, that's a small serializer coercion in `properties/serializers/finance.py` — say so and I'll add it.
  - Not pushed.
project: 2026-05-25-villa-collective
source_id: null
tags: []
time_minutes: 5
title: Usability of Property finance screen
updated: 2026-10-01 10:29:44.755173
waiting_on: null
waiting_since: null
working_on: false
---

Saving always outputs: 
{
    "code": "validation_error",
    "detail": "Validation failed",
    "field_errors": {
        "commission_note": [
            "This field may not be null."
        ],
        "notes": [
            "This field may not be null."
        ]
    }
}

Notes should not be required. Commission note is not editable adn should not be required.