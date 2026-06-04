---
area: null
contexts: []
created: 2026-06-03 16:43:09.728584
defer_until: null
due: null
energy: low
id: 2026-06-03T1643-review-andrea-s-bw-reg-card-ticket
order: null
output: |
  ## Agent run 2026-06-03T13:47Z

  ### Short answer
  The "destructive" concern is essentially CORRECT — but not because the code
  change loses data. It's correct because the remaining step (provisioning the
  portfolio card via `setup_bw_extendable_registration_card`) has a blast radius
  far wider than "add a HotelKey card," and the wording "destructive" is a fair
  caution against running that command in prod.

  ### Important caveat on "Andres's comment"
  I could not find a literal written comment from Andres saying "destructive":
  - ENT-6288 has ZERO comments (Linear).
  - The closely-related migration ticket ENT-5438 has only a Gareth comment.
  - There is no PR for ENT-6288's own branch.
  - On the PR that actually shipped this change (#46402, see below), Andrés
    Figueira APPROVED with no comment body.
  So the "destructive" note appears to be a verbal/Slack remark I can't see. I
  evaluated the substance of the claim against the code rather than his exact words.
  If you have the literal text, worth a second pass — but the technical verdict below
  should hold regardless.

  ### State of play (matters a lot)
  ENT-6288 is effectively a DUPLICATE of ENT-6320. ENT-6320 / PR #46402 (megolem,
  merged to master 2026-05-27) already added `Vendor.HOTEL_KEY` (slug `bw-hotelkey`,
  template BW_MSA_TEMPLATE) to VENDOR_CONFIG — that's step 1 of the ENT-6288 spec,
  already done and deployed. The dict addition itself is purely additive and SAFE.
  No migration, no command run, and no tests shipped with that PR.

  ### Why the remaining step is the "destructive" one
  All that's left is provisioning the `PortfolioExtendableRegistrationCard` rows,
  i.e. running `onboarding/management/commands/setup_bw_extendable_registration_card.py`.
  That command is NOT scoped to the new HotelKey card. It iterates the ENTIRE
  VENDOR_CONFIG (now 6 entries) and, for the 5 pre-existing slugs, takes the UPDATE
  path -> `ExtendableRegistrationCardService.update_portfolio_extendable_registration_card`
  (check_in/services/extendable_registration_card.py:47). That method CASCADES: for
  every hotel RegistrationCard with a CURRENT extension of each card, it regenerates
  the combined schema, runs `full_clean()` + `save()`, and writes an event log
  (lines 63-93). So running it to "just add HotelKey" actually re-writes the base
  schema of all live BW extendable cards and re-saves every extended hotel's reg card.

  ### Fairness / nuance (so we don't overclaim)
  - Hotel customizations are NOT lost: they live in `extension.extension` and are
    recombined on top of the regenerated base. So custom fields survive.
  - BUT the base-template portion is overwritten with whatever BW_MSA_TEMPLATE /
    BW_MEWS_TEMPLATE / BW_OHIP_TEMPLATE etc. say in code TODAY. If those have drifted
    from what's live in prod, every extended hotel silently gets the new base on the
    next run. That's the real "destructive" risk — a silent, unscoped schema push.
  - The whole cascade runs in one `transaction.atomic`, so one hotel failing
    `full_clean()` rolls back everything and blocks provisioning the HotelKey card.
  - Net: intent = "add 1 card"; effect = "re-touch all extended BW hotels." That
    mismatch is exactly why "destructive" is a reasonable label.

  ### Recommendation
  1. Treat ENT-6288 as a duplicate of ENT-6320; re-scope it to "safely provision the
     bw-hotelkey portfolio card" or close as dup.
  2. Do NOT run `setup_bw_extendable_registration_card` as-is in prod. Provision only
     the missing card: either a create-only data migration that inserts the single
     bw-hotelkey PortfolioExtendableRegistrationCard, or change the command so existing
     slugs are skipped (create-only, no update/cascade). The ticket's own "Open
     questions" already leans toward (b) a data migration — that's the right call.
  3. If we ever DO want to re-sync the existing 5 cards, do it deliberately and
     separately, after confirming the in-code templates match production.

  ### Files referenced
  - backend/canary/onboarding/management/commands/setup_bw_extendable_registration_card.py (iterates all VENDOR_CONFIG; update path lines 86-117)
  - backend/canary/check_in/services/extendable_registration_card.py:47-102 (cascading update)
  - backend/canary/onboarding/configuration_providers/best_western/registration_card_provider.py (VENDOR_CONFIG, HOTEL_KEY already present)
  - ENT-6320 / PR #46402 (already merged the dict change)
project: null
source_id: null
tags: []
time_minutes: 5
title: REview Andrea's BW reg card ticket
updated: 2026-06-03 16:59:51.241037
waiting_on: null
waiting_since: null
working_on: false
---

"destructive"
https://linear.app/canary-technologies/issue/ENT-6288/add-a-registration-card-configured-for-hotelkey-in-best-western-reg

Is andres's comment correct?