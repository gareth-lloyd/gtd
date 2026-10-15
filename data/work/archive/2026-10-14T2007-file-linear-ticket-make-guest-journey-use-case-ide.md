---
area: null
completed_at: 2026-10-15 13:02:43.002685
contexts: []
created: 2026-10-14 20:07:32.072781
defer_until: null
due: null
energy: null
id: 2026-10-14T2007-file-linear-ticket-make-guest-journey-use-case-ide
order: null
output: |-
  ## Agent run 2026-10-15 13:00:15.070839

  NOT FILED. Gareth asked for a redraft to review before creation.
  Redraft: /private/tmp/claude-501/-Users-garethlloyd-projects-canary/be0b57d7-68b6-4eae-9601-b51901b66f4a/scratchpad/ticket-body.md (session scratchpad; copy it if needed)
  Planned create: team Enterprise, title "Make guest journey use-case identifiers unique across portfolios", unassigned, relatedTo ENT-7726 (https://linear.app/canary-technologies/issue/ENT-7726/implement-binding-rules-tree-prototype).

  Duplicate check: none. Closest is ENT-5310, canceled (https://linear.app/canary-technologies/issue/ENT-5310/address-wyndham-check-in-message-use-case-overlap-with-migration-step).

  Claims checked against code:
  - Shared identifiers table: correct (use_case.py). Addon overlap list: correct.
  - Rebrand claim needed softening: the configure plan finds the message by use case and then overwrites its content (configure_guest_journey_messages.py ~1531-1583), so wrong content only persists until a new-family plan rewrites that message.
  - The configure plan already falls back to fetch_root_message_by_type when the use-case lookup misses (~1342-1350), so deleting foreign associations then re-linking under the prefix works for system messages.
  - Demo hotels use the BW enum (demo_guest_journey_messages_provider.py:50). Staging portfolios reuse the prod enums, so the prefix belongs to the enum, not Portfolio.Identifier.
  - remove_foreign_portfolio_use_case_associations already computes "other enums minus current". With unique values the subtraction does nothing, so the fix is a simplification plus a docstring update.
  - set_guest_journey_message_for_use_case raises MessageAlreadyAssignedError rather than duplicating (guest_journey_message is OneToOne). A wrong-form read during the rollout fails loudly.

  Edits to your version: "data migration" vs "management command" reconciled to the command; import-time check replaces the separate "test enforces" criterion; release sequence kept as one line with an example; restored the one-line list of bare strings outside the enums (tmp scripts, tests, Snowflake).

  ## Agent run 2026-10-15 13:03:09.551539

  FILED: ENT-7901 (https://linear.app/canary-technologies/issue/ENT-7901/make-guest-journey-use-case-identifiers-unique-across-portfolios). Enterprise team, Triage, Low priority, unassigned, related to ENT-7726. Opens with a note that this is a potential future footgun the current code works around, and a candidate for a later fix. The body is the reviewed redraft from the previous run.
project: null
source_id: null
tags: []
time_minutes: null
title: 'File Linear ticket: make guest journey use-case identifiers unique across
  portfolios'
updated: 2026-10-15 13:03:09.551539
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

By editing the StrEnum definitions, prefix every identifier with its portfolio family, for example `wyndham.mid_stay_message`, and migrate the existing rows.

- The prefix names the enum's brand MSA - 'wyndham' for the Wyndham StrEnum
- Create a one-off migration management command to select all use-case instances by hotel portfolio and identifier and convert them to the new values.
- Institute a runtime check in the same file which asserts the length of the combined strenums is the same as the sum of the individual enums
## Scope

1. Change the enum values in `use_case.py`. Services read and write through `str(use_case)`, so `group_use_case_service.py` needs no logic change.
2. Write a data migration that rewrites `use_case_identifier` on existing `GuestJourneyMessageGroupUseCase` rows:
   - An identifier found in only one family's enum gets that family's prefix.
   - A shared identifier gets the hotel's current portfolio family.
   - A shared identifier on a hotel with no portfolio family needs a decision. Demo hotels are the known group, and their rows come from the Best Western enum.
3. Fix `remove_foreign_portfolio_use_case_associations` to delete using the correct enum values. 
5. design a safe releases sequence to avoid gaps where the wrong enum values are used to filter / create during onboarding scripts. 


## Out of scope

Addon use cases repeat the same pattern. `AddonGroupUseCase` reuses `early_check_in`, `late_check_out`, `very_late_check_out`, `pet_fee`, `rollaway_bed` and `breakfast` across portfolios. File a sibling ticket once this approach is settled.

## Acceptance criteria

- No identifier string appears in more than one family's enum. A test enforces this.
- Every existing `GuestJourneyMessageGroupUseCase` row carries a prefixed identifier.
- After a rebrand and a configure plan run, the hotel holds no associations from the old family.
- The existing tests for re-running the configure plan and for rebranding pass.