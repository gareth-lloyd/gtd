---
area: null
completed_at: null
contexts: []
created: &id001 2026-10-14 20:07:32.072781
defer_until: null
due: null
energy: null
id: 2026-10-14T2007-file-linear-ticket-make-guest-journey-use-case-ide
order: null
output: ''
project: null
source_id: null
tags: []
time_minutes: null
title: 'File Linear ticket: make guest journey use-case identifiers unique across
  portfolios'
updated: *id001
waiting_on: null
waiting_since: null
working_on: false
---

Draft source: `/Users/garethlloyd/projects/plans/unique-use-case-identifiers-ticket-draft.md`

---

# Make guest journey use-case identifiers unique across portfolios

**Status:** draft, not filed in Linear
**Team:** Enterprise · **Related:** ENT-7726, [Guest journey messages in rules-based configuration](https://app.notion.com/p/3f9814686151813da661eb802029d0eb)

## Problem

A use-case identifier names a portfolio's content for a message. The slot the message fills is `GuestJourneyMessage.type`. Two examples show the difference:

- IHG fills the `MID_STAY_MESSAGE` slot with `mid_stay_message` in AMER and `emea_mid_stay_message` elsewhere. Each has its own template.
- Wyndham fills the `POST_CHECK_IN_MESSAGE` slot with `welcome_message` for brands without loyalty.

The enums in `onboarding/models/use_case.py` reuse the same identifier for different portfolios' content:

| Identifier | Used by |
| --- | --- |
| `post_check_out_message` | Best Western, Wyndham, IHG |
| `mid_stay_message` | Best Western, Wyndham, IHG |
| `welcome_message` | Best Western, Wyndham |

`GuestJourneyMessageGroupUseCase.use_case_identifier` stores the bare string, so a row can't say whose content it describes. This causes three problems:

- **Rebrands misreport content.** After a Wyndham to Best Western rebrand, the hotel's mid-stay message still reads as `mid_stay_message`, so it passes as Best Western's message while it holds Wyndham's content. `remove_foreign_portfolio_use_case_associations` keeps shared identifiers on purpose, so cleanup doesn't catch it.
- **Enum members from different portfolios are equal.** StrEnum members compare and hash by value. `BWGuestJourneyMessageUseCases.MID_STAY_MESSAGE == WyndhamGuestJourneyMessageUseCases.MID_STAY_MESSAGE` is `True`, and a dict keyed by the `GuestJourneyMessageUseCase` union merges them into one key.
- **One setting can't hold every portfolio's values.** The guest journey messages design may use one setting key for every portfolio. Its allowed values are then the union of all the enums, and that union can't tell the three `mid_stay_message`s apart. Reports that compare portfolios hit the same problem.

## Proposal

Prefix every identifier with its portfolio family, for example `wyndham.mid_stay_message`, and migrate the existing rows.

- The prefix names the enum's family, not `Portfolio.Identifier`. Staging portfolios (`IHG_STAGING`, `WYNDHAM_STAGING`) reuse the production enums, and demo hotels use the Best Western enum outside any Best Western portfolio.
- On rebrand, delete every association whose prefix isn't the new family. The configure plan finds the system message by `GuestJourneyMessage.type` and links it under the new family's identifier. This replaces today's deliberate rebind of shared strings.

## Scope

1. Change the enum values in `use_case.py`. Services read and write through `str(use_case)`, so `group_use_case_service.py` needs no logic change.
2. Write a data migration that rewrites `use_case_identifier` on existing `GuestJourneyMessageGroupUseCase` rows:
   - An identifier found in only one family's enum gets that family's prefix.
   - A shared identifier gets the hotel's current portfolio family.
   - A shared identifier on a hotel with no portfolio family needs a decision. Demo hotels are the known group, and their rows come from the Best Western enum.
3. Rewrite `remove_foreign_portfolio_use_case_associations` to delete by prefix. Leave hotels with no portfolio family alone.
4. Update the bare identifier strings outside the enums:
   - rollout recipes and management commands;
   - `tmp/repeatable` and `tmp/useful` scripts, e.g. `tmp/useful/deactivated_hotels_by_script_type.py` and `tmp/repeatable/ihg/tag_deprecated_mid_stay_custom_message.py`;
   - tests;
   - Snowflake or analytics queries on `use_case_identifier`.
5. Ship in three releases so a rolling deploy never runs a reader that misses rows:
   1. Readers accept both the bare and the prefixed form. Writers still write bare strings.
   2. Run the data migration, and switch writers to prefixed strings.
   3. Remove support for bare strings.

   `guest_journey_message` is one-to-one with its association. A pod that misses an existing row and tries to link the message again fails with `MessageAlreadyAssignedError`, not a duplicate row.

## Alternatives considered

- **Rename only the three shared identifiers.** This touches fewer rows, but the data still can't show which family a row belongs to. The next new identifier can collide again unless a test catches it.
- **One shared identifier per system slot.** This doesn't work. Identifiers name content, and one slot carries different content per portfolio and per region.
- **A `family` column instead of a prefix.** This gives a structured, filterable field, but it needs a schema migration PR. The unique constraint would also have to stop a hotel holding rows from two families.

## Out of scope

Addon use cases repeat the same pattern. `AddonGroupUseCase` reuses `early_check_in`, `late_check_out`, `very_late_check_out`, `pet_fee`, `rollaway_bed` and `breakfast` across portfolios. File a sibling ticket once this approach is settled.

## Acceptance criteria

- No identifier string appears in more than one family's enum. A test enforces this.
- Every existing `GuestJourneyMessageGroupUseCase` row carries a prefixed identifier.
- After a rebrand and a configure plan run, the hotel holds no associations from the old family.
- The existing tests for re-running the configure plan and for rebranding pass.