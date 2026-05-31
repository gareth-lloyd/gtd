---
area: null
contexts: []
created: 2026-05-29 11:13:19.685694
defer_until: null
due: null
energy: low
id: 2026-05-29T1113-role-on-property-contacts-should-be-a-dropdown
order: null
output: |
  ## Agent run 2026-05-29T09:04:17Z

  ### Root cause
  Frontend/backend mismatch. The backend constrains `role` to a fixed enum, but
  the frontend renders it as a free-text input — so any value that isn't one of
  the 5 enum members fails server-side validation with a DRF 400
  ("<value>" is not a valid choice. The valid choices are: owner, manager,
  agent, housekeeper, owners_rep).

  ### Backend (already correct — do NOT change)
  - Enum: `accounts/enums.py:47` `ContactRole(TextChoices)` — values:
    `owner` / `manager` / `agent` / `housekeeper` / `owners_rep`
    (labels: Owner, Manager, Agent, Housekeeper, Owner's representative).
  - Field: `properties/models/contacts.py:27-30` —
    `role = CharField(max_length=24, choices=ContactRole.choices)`.
  - Serializer: `properties/serializers/contact_assignment.py` — plain
    ModelSerializer, inherits the choices validation (no custom validator).
  - The choices are NOT exposed via any API/options endpoint today.

  ### Frontend (this is what needs fixing)
  - `frontend/src/features/properties/components/AssignmentFormDialog.tsx:145-157`
    renders role as a free-text `<Input {...form.register("role")} />`.
  - Zod schema is too permissive: `frontend/src/features/properties/schemas.ts:520-526`
    has `role: z.string().trim().max(120).optional()` (max 120, no enum check —
    note backend max_length is only 24).
  - Display: `frontend/src/features/properties/tabs/PeopleTab.tsx:354` shows the
    raw value with `_`→space + capitalize.

  ### Recommended fix (small, FE-only)
  1. Swap the free-text `<Input>` in AssignmentFormDialog.tsx for the existing
     `<Select>` (`src/components/ui/select.tsx`) — already used by sibling
     dialogs in `properties/components/` (SeasonFormDialog, RoomFormDialog, etc.),
     so the pattern is established.
  2. Hardcode the 5 options to mirror `ContactRole` (value -> label):
     owner→Owner, manager→Manager, agent→Agent, housekeeper→Housekeeper,
     owners_rep→Owner's representative. (No options endpoint exists; a tiny
     shared FE constant is fine. Optionally add a backend choices endpoint later
     to keep them in sync, but that's gold-plating for now.)
  3. Tighten the Zod schema to `z.enum([...])` with the 5 values (and drop the
     stale max(120)) so invalid roles are caught client-side.
  4. i18n role keys already exist (en/properties.json `role_label`,
     `role_placeholder`); the placeholder ("e.g. owner, cleaner") becomes a
     Select placeholder/empty option, and per-role labels may want new keys.

  ### Effort / risk
  ~30–45 min, frontend-only, low risk. No DB/migration changes. Add/adjust a
  component test for the dialog. Watch the enum drift: 5th value is stored as
  `owners_rep` but legacy migration maps role IDs 1-5 (data_migration/loaders/
  reservations.py:27) — existing data is already enum-clean, so no backfill needed.
project: 2026-05-25-villa-collective
source_id: null
tags: []
time_minutes: 5
title: Role on property contacts should be a dropdown
updated: 2026-05-29 09:04:17.000000
waiting_on: null
waiting_since: null
working_on: false
---

currently free text and raising errors because of invalid choices.