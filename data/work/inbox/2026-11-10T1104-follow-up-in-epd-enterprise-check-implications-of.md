---
area: null
completed_at: null
contexts:
- react
created: 2026-11-10 11:04:30.658445
defer_until: null
due: null
energy: medium
id: 2026-11-10T1104-follow-up-in-epd-enterprise-check-implications-of
order: null
output: |
  ## Agent run 2026-11-10T12:53

  Nothing was posted anywhere.

  ### Headline: production US has zero of these
  Read-only counts on the production US canary DB (run 2026-11-10, with your OK):
  - check_in_portfolioextendableregistrationcard: 0 rows
  - check_in_registrationcardextension: 0 rows in any state (never used, not just archived)
  - onboarding_onboardingvalue with kind BW_USE_EXTENDABLE_REGISTRATION_CARD: 0 rows
  So in US no hotel is portfolio-managed, the setup_bw_extendable_registration_card command
  was never run with --commit there, and no BW account is flagged onto the extendable path.
  EU and AP were NOT checked (you approved US only). BW and Wyndham are mostly US, but
  one query per region would close this.

  What this changes: there are no hotels to migrate, and the portfolio_managed refusal in
  move_to_catalog blocks nobody in US. The bridge in PR #63856 would serve no live hotel.
  If EU and AP are also empty, the cheaper route is to skip the bridge and delete the
  concept now: remove the refusals and the BW extendable branch, then deprecate the tables.
  The sections below were written before the counts; the "Direction" recommendation to
  merge as a bridge only holds if EU or AP turn out to have rows, or if BW plans to turn
  the flag on soon (worth asking Andrea or Connor).

  ### Direction: where the thread stands
  Thread: https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1794235759936819
  - You (17:55): "I can check the implications, but we are leaning towards drop altogether."
  - Lea (17:58): merge Rafa's PR so portfolio hotels keep working, drop everything after
    migrating them. Still waiting on a yes from you.
  - Andrea (18:02): support it during the reg card transformation step, move away when
    onboarding writes directly to the catalog.
  These agree. Recommended answer: yes, merge PR #63856
  (https://github.com/canary-technologies-corp/canary/pull/63856, AD-8448
  https://linear.app/canary-technologies/issue/AD-8448) as a bridge, and drop the concept
  when BW onboarding writes the catalog directly. The PR is open, approved by Lea, with
  Andrea's review comments all marked non-blocking.

  ### What the feature does today (from the code)
  - The only code that creates extensions is Best Western onboarding
    (onboarding/configuration_providers/best_western/registration_card_provider.py:82), and
    only for accounts with the onboarding value BW_USE_EXTENDABLE_REGISTRATION_CARD. Other BW
    accounts take the legacy path and get an ordinary card. Six portfolio cards exist by slug:
    bw-autoclerk, bw-hotelkey, bw-jonas-chorum, bw-mews, bw-ohip, bw-vm.
  - There is no Wyndham code path. If Wyndham has a portfolio card it was made by hand in
    Django admin or the API. Unverified without prod data.
  - Each member hotel's RegistrationCard.schema is already the fully merged form (your point
    in the thread), so nothing reads the portfolio card at render time.

  ### What we lose by dropping it
  1. Central push: one edit to the portfolio card rewrites every member. Replacement is an
     onboarding re-run or a script over catalog rows.
  2. Per-hotel changes that survive a push: text overrides (BW uses this for hotel_policy),
     inserts at named insertion points (built for BW loyalty fields), hidden elements.
  3. The lock: a managed hotel cannot edit its card in the form builder
     (hotels/views/api/registration_card.py:102) and can only change the text keys the
     portfolio allows (check_in/views/registration_card_details.py:83). After the drop, BW
     hotels can edit the whole form in Flow Config unless the catalog gets its own lock.
     This is the one real capability loss; brand-standard drift would have to be caught by
     the onboarding configuration check instead.
  4. Audit events for portfolio card and extension changes.

  ### Migration impact when we drop
  - Data: no schema transform. Member cards already hold the merged form, and after #63856
    catalog members have matching catalog rows. Archiving the CURRENT RegistrationCardExtension
    rows turns is_portfolio_managed off and unlocks the hotels.
  - Order matters: change BW onboarding first. While an account still has
    BW_USE_EXTENDABLE_REGISTRATION_CARD, an onboarding re-run recreates the extension.
  - Not verified: whether the legacy BW path produces the same form as the extendable path
    for a hotel that has overrides. If not, the first onboarding re-run after the switch
    could overwrite hotel_policy text or loyalty inserts. Worth a check before the drop.
  - Code to remove afterwards: ExtendableRegistrationCardService, both models (two-table
    deprecation, migrations in their own PRs), the admin and forms, the event specs, the
    settings_agent registration_card provider branch, the i18n PATCH branch, the
    setup_bw_extendable_registration_card command, the onboarding value kind, the canary_mcp
    SQL grants, and the guards #63856 adds (require_form_not_portfolio_managed,
    require_field_not_portfolio_managed, the country-fields refusal, the Flow Config message).
  - So #63856 adds a little code that the drop later deletes. That is acceptable: without it
    managed hotels block AD-8180 (https://linear.app/canary-technologies/issue/AD-8180).

  ### Worth raising on the PR before merge (already in review comments)
  - CatalogOnboardingService.onboard_to_catalog still refuses portfolio hotels while the PR
    removes every mapping of that outcome (Andrea's comment; KeyError risk for a later caller).
  - One push is one transaction, so one member the catalog cannot represent rolls back all
    members (Andrea, non-blocking).
  - The bot's "disabled registration step blocks the whole push" concern looks fixed in the
    current diff (NO_STEP is skipped).

  ### Draft reply for the thread (not sent)
  > Checked the implications. Prod US has no portfolio extendable cards at all: 0 cards,
  > 0 extensions ever, and no BW account flagged to use them. The BW extendable path was
  > built but never switched on. I still need to confirm EU and AP.
  > If those are empty too, there is nothing to migrate and nothing for Rafa's PR to keep
  > working, so I'd rather drop the concept now than merge the bridge and delete it later:
  > remove the portfolio_managed refusals and the BW extendable branch, then deprecate the
  > two tables. The only capability we give up is the lock that stops hotels editing a
  > portfolio-owned form, and nobody is behind that lock today.
  > @Andrea / @Connor: any plan to turn the BW extendable flag on that I'm missing?

  ### Still open
  - EU and AP counts. Same query with --region eu / --region ap:
    canary prod-db query canary "SELECT (SELECT count(*) FROM check_in_portfolioextendableregistrationcard) AS cards, (SELECT count(*) FROM check_in_registrationcardextension) AS extensions_any_state, (SELECT count(*) FROM onboarding_onboardingvalue WHERE kind = 'BW_USE_EXTENDABLE_REGISTRATION_CARD') AS bw_flag_rows" --region eu
  - Whether BW intends to enable the flag (business question, not answerable from code).
project: null
source_id: https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1794239753341649?thread_ts=1794235759.936819&cid=C047K6WSUJY
tags:
- morning-gtd
- slack
time_minutes: 20
title: 'Follow up in #epd-enterprise: check implications of dropping portfolio-managed
  reg cards'
updated: 2026-11-10 13:06:17.180875
waiting_on: null
waiting_since: null
working_on: false
---

Missed yesterday: I said 'I can check the implications, but we are leaning towards drop altogether' (Wyndham/BW extendable reg cards vs the catalog). Lea then asked whether to merge Rafa's PR #63856 in the meantime and drop the concept later; Andrea answered in part. Confirm the direction and the migration impact.
https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1794239753341649?thread_ts=1794235759.936819&cid=C047K6WSUJY