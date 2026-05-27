---
area: null
contexts:
- react
created: 2026-05-27 01:38:03.285731
defer_until: null
due: null
energy: medium
id: 2026-05-27T0138-reply-to-mike-bretherick-re-discover-card-mapping
order: null
output: |
  ## Agent run 2026-05-27T19:35Z (REVISION 4 — INT-8894 confirms manual recovery path; final)

  ### One-paragraph answer for Mike
  Scripted enterprise onboarding did NOT cause this. Lubbock's broken SynXis config was created manually by Sharon Hales via PMS Gateway Admin on 2026-04-01 while recovering from INT-8894, where Marta Ziaei requested a vendor switch from OHIP → SPH and accidentally deleted the entire gateway account. The manual recovery bypassed `WyndhamPMSConfigProvider` (which would have correctly written `Discover: DI` for SPH) and instead used the `SynxisConfiguration` model default — `Discover: DS` (`pms-gateway/vendors/integrations/synxis/models/configuration.py:18`). Mike fixed it on 2026-05-26 by updating the persisted dict. The wider risk is "any SynxisConfiguration created via admin rather than via the script" — not "the scripted cohort."

  ### Timeline (confirmed against INT-8894 comments + gateway admin change history)
  - **2025-12-15** — Travelodge Lubbock scripted-onboarded on OHIP via Wyndham MSA Configure-PMS (`Vendors: oracle_ohip`, script success).
  - **2026-03-31 13:57** — Marta Ziaei (Onboarding) files INT-8894: "moving to SPH on 4/1, please create SPH config. I deleted the old OHIP config." Assigned to Sharon Hales (Integrations).
  - **2026-04-01 08:55** — Sharon comments: *"happy to help here — but curious as to why this is not being completed via a script as per the usual process?"* So the team **does have a scripted path for vendor switch**; it just wasn't used here.
  - **2026-04-01 08:56** — Sharon: *"I see you did not delete the OHIP — you deleted the whole gateway account."*
  - **2026-04-01 ~09:02** — Sharon manually creates `SynxisConfiguration` + `SynxisCRSConfiguration` via PMS Gateway admin to recover, then deletes/reshapes per the 09:13 entries. This is when `Discover: DS` enters the persisted record — from the model default.
  - **2026-04-01 09:15** — Sharon: *"ready for your activation."*
  - **2026-04-01 12:49** — Marta acknowledges the deletion mistake: *"noted for next time where I need to delete the OHIP config and not the whole gateway account."*
  - **2026-05-13 07:50** — INT-8894 closed (status update).
  - **2026-05-26 06:56** — Mike Bretherick updates Payment Methods on the SynXis Configuration — the PMS-8298 fix flipping `Discover: DS` → `DI`.

  ### Root cause
  `pms-gateway/vendors/integrations/synxis/models/configuration.py:18`:
  ```python
  def default_payment_methods() -> dict[CardType, str]:
      return {CardType.AMEX: "AX", CardType.DISCOVER: "DS", CardType.MASTERCARD: "MC", CardType.VISA: "VI"}
  ```
  Manually-created `SynxisConfiguration` rows (i.e. created outside `WyndhamPMSConfigProvider`) inherit this default. For Wyndham SPH properties the right value is `DI` (as the scripted provider correctly writes at `wyndham_pms_config_provider.py:129`). The default is therefore wrong for the dominant Wyndham use case.

  ### Wider blast radius (for Mike's question)
  - **Scripted enterprise onboarding population:** **not at risk** for SPH Discover specifically — script writes `DI`. Set aside.
  - **Manually-recovered / manually-vendor-switched SPH cohort:** at risk. Any Wyndham SPH `SynxisConfiguration` created via admin (recovery after a deletion, ad-hoc vendor switch outside the scripted path, etc.) inherits `Discover: DS`. INT-8894 shows this happens in real triage workflows when something goes wrong. "Other hotels corrected in the past" referenced in the PMS-8298 thread are likely the same pattern.
  - **Detection audit:** `SynxisConfiguration` rows on Wyndham accounts where `payment_methods->>'Discover' = 'DS'`. Sample one or two to confirm they should be `DI` (the dominant Wyndham SPH expectation), then bulk-flip.

  ### Separately worth flagging (different bug, same shape — out of scope for Mike's immediate question)
  `wyndham_pms_config_provider.py:102-126` hardcodes `Discover: DS` / `MDS` for every Wyndham OHIP property. OHIP payment-method codes are per-property in Opera; one hardcoded value will be wrong for some properties. Lubbock's OHIP config wasn't the broken one here (because the account got switched to SPH), but the same problem will produce its own incidents over time. BW's provider (`best_western/pms_config_provider.py` lines 132, 183, 191, 198) replicates the pattern. Mention but don't bundle into PMS-8298 follow-up.

  ### Recommended remediation
  1. **Audit cohort** (above). Bulk-fix existing wrong SynxisConfiguration rows.
  2. **Fix the gateway model default** in `synxis/models/configuration.py:18` — either change the default to `DI` (if Wyndham SPH dominates the install base) or remove the default and require callers to supply `payment_methods` explicitly. Removing the default is safer because it forces both scripted and manual paths to be intentional.
  3. **Process**: when an account is accidentally deleted and recovered, the recovery should go through the scripted provider, not raw admin creation. Sharon's "why isn't this scripted?" comment suggests this is already the team's preference; INT-8894 is an exception that surfaced a model-default footgun.

  ### Reply drafted (NOT SENT — Mike's DM)
  ```
  Hi Mike — fully traced now, sorry for the iterations:

  The wrong `DS` on Lubbock's SynXis config did NOT come from scripted onboarding. It came from a manual recovery in INT-8894: on 2026-03-31, Marta requested an OHIP→SPH switch and accidentally deleted the whole gateway account (intending to delete just OHIP). Sharon recovered it manually on 2026-04-01 by creating a new SynxisConfiguration via PMS Gateway admin — Sharon herself flagged that this isn't the usual process ("curious as to why this is not being completed via a script as per the usual process?"). The manual creation bypassed `WyndhamPMSConfigProvider` (which correctly writes `Discover: DI` at `wyndham_pms_config_provider.py:129`) and instead picked up the `SynxisConfiguration` model default at `synxis/models/configuration.py:18`, which is `Discover: DS`. You then fixed that on 2026-05-26.

  So Sharon's "scripted enterprise onboarding" pointer was directionally right but technically off: the script is the safe path; admin-bypassing the script is what writes the wrong default. The wider at-risk cohort is "Wyndham SynxisConfiguration rows created manually via admin (recoveries, ad-hoc vendor switches) rather than via the script." Probably a small but non-zero set. The hotels "corrected in the past" you saw on the PMS-8298 thread are most likely the same pattern.

  Suggested follow-up:
  1. Audit `SynxisConfiguration` rows on Wyndham accounts where `payment_methods->>'Discover' = 'DS'`. Bulk-flip after spot-confirming.
  2. Fix the model default in `synxis/models/configuration.py:18` so future manual creations can't silently inherit the wrong value — either flip to DI or drop the default and require explicit specification.
  3. (Separately, not Lubbock's bug but worth a ticket): Wyndham + BW OHIP scripted providers hardcode `Discover: DS` for every OHIP property regardless of per-property OHIP config — will produce its own incidents over time.

  Happy to write the audit SQL and/or the model-default PR if you want me to pick it up.
  ```

  ### Exit
  working_on cleared. Reply drafted only — not sent. Awaiting user approval before posting to Mike.

  --- (earlier, partially-incorrect framings preserved below for context) ---

  ## Agent run 2026-05-27T18:55Z (revised after user supplied onboarding-history + plan-output evidence)

  ### Final diagnosis
  Lubbock has BOTH an OHIP config (created by scripted onboarding 2025-12-15, vendor `oracle_ohip`) AND a SynXis SPH config (added manually by Sharon Hales via PMS Gateway Admin on 2026-04-01 09:02). Mike's May 26 fix was on the **SynXis Configuration**, not OHIP. The wrong `Discover: DS` value on that SynXis config did not come from the scripted onboarding — the Wyndham SPH branch (`wyndham_pms_config_provider.py:129`) writes `"DI"` and has done since Feb 2024.

  It came from the **`SynxisConfiguration` model default** in `backend/pms-gateway/vendors/integrations/synxis/models/configuration.py:18`:
  ```python
  def default_payment_methods() -> dict[CardType, str]:
      return {CardType.AMEX: "AX", CardType.DISCOVER: "DS", CardType.MASTERCARD: "MC", CardType.VISA: "VI"}
  ```
  Anyone creating a `SynxisConfiguration` without explicit `payment_methods` (e.g. via Django admin) gets `DS`. Sharon's manual add on April 1 took this default. Mike's May 26 fix updated the persisted dict to `DI`.

  The Linear-ticket title symptom ("Discover card showing as CK instead of DS") fits: when the gateway-stored code didn't match what the property's SynXis actually expected, SynXis fell back to `CK` (cheque).

  ### What's actually wrong for Mike's "wider impact" question
  Two distinct issues, both real, neither one Mike's Feb-2024-window scenario:

  1. **Manual SynxisConfiguration creation inherits a default that's wrong for Wyndham SPH.**
     Any Wyndham SPH account where a `SynxisConfiguration` was created via admin (not via the Wyndham scripted onboarding) will have `Discover: DS` and silently break Discover swipes. Lubbock is one. Mike says "other hotels corrected in the past" — likely the same root cause for those.
     - **Cohort to audit:** `SynxisConfiguration` rows on Wyndham (or any non-Sabre-SPH-default) accounts where `payment_methods->>'Discover' = 'DS'`.
     - **Code fix:** either change `default_payment_methods()` to `DI` (if DI is the dominant Wyndham-SPH expectation), or remove the model default entirely and force callers to specify, so manual admin creation can't silently inherit the wrong value.

  2. **Scripted OHIP onboarding hardcodes a single Discover code for every Wyndham OHIP property.**
     `wyndham_pms_config_provider.py:102-126` writes `Discover: DS` (plus `MDS` offline) to every OHIP property. This wasn't the bug for Lubbock specifically, but per the same logic — OHIP Discover codes are configured per-property in Opera — the hardcoded `DS` is wrong wherever the property's OHIP expects `DI`. Same anti-pattern as the SynXis default, just different path. BW's provider (`best_western/pms_config_provider.py` lines 132, 183, 191, 198) replicates the pattern.

  ### Honest record of iteration
  I gave Mike two wrong answers before this one. First I said "Feb 6-26 2024 window in the SPH branch" — invalidated by the 2025-12-15 onboarding date in the script-history screenshot. Then I said "OHIP branch hardcoding, applies to every Wyndham OHIP hotel since Oct 2023" — true as a separate concern but not what broke Lubbock, since the gateway-admin change log shows the fix was on the SynXis config (created manually), not on the OHIP config. The gateway admin screenshot was needed to disambiguate.

  ### Recommended remediation (not done — for Mike / Sharon / PMS team to action)
  1. **Audit the wider SynXis cohort first**, since that's the matching mechanism to Lubbock: `SynxisConfiguration` rows on Wyndham accounts where `payment_methods->>'Discover' = 'DS'`. Bulk-flip after spot-confirmation.
  2. **Change the gateway default** in `synxis/models/configuration.py:18` — either to `DI` (if that's the right default for the dominant Wyndham SPH use case) or remove the default and require explicit specification. This prevents recurrence.
  3. **Separately, fix the scripted OHIP hardcoding** in Wyndham + BW providers so per-property codes are sourced from per-property onboarding values rather than baked into the script. This is a different bug from Lubbock's but the same shape and worth bundling.

  ### Reply drafted (NOT SENT — Mike's DM)
  ```
  Hi Mike — two iterations of wrong answer from me; cleaner picture now thanks to the gateway-admin history screenshot.

  Lubbock has two gateway configs: an OHIP one (created by the scripted Configure-PMS on 2025-12-15, vendor `oracle_ohip`) and a SynXis SPH one (added manually by Sharon via PMS Gateway Admin on 2026-04-01 09:02). Your May 26 fix was on the SynXis config, and the wrong `DS` there did NOT come from the script — the Wyndham SPH branch in `wyndham_pms_config_provider.py:129` writes `DI` and has done since Feb 2024.

  It came from the model default in `pms-gateway/vendors/integrations/synxis/models/configuration.py:18` (`default_payment_methods()` returns `Discover: DS`). When a SynxisConfiguration is created via admin without an explicit `payment_methods`, it inherits that default. Sharon's April 1 manual add picked it up; you fixed it on May 26.

  So Sharon's "scripted enterprise onboarding" pointer is half-right — same Wyndham-SPH expectation (`DI`), but the actual write path that produced the wrong value here is the model default applied during manual admin creation, not the script. The hotels "corrected in the past" most likely have the same shape (admin-created SynxisConfiguration inheriting `DS`).

  Suggested:
  1. Quick audit: `SynxisConfiguration` rows on Wyndham accounts where `payment_methods->>'Discover' = 'DS'`. That's the at-risk cohort. Bulk-flip after a spot check that they should all be DI.
  2. Code fix: change `default_payment_methods()` so future manual creations don't inherit the wrong default — either flip to DI if that's the dominant SPH expectation, or drop the default and force explicit specification.
  3. Separately: the scripted OHIP branches (Wyndham `wyndham_pms_config_provider.py:102-126` and the equivalent BW dicts) hardcode `Discover: DS` across all OHIP properties, regardless of per-property OHIP config. That's not Lubbock's bug today, but it's the same shape and will produce its own incidents over time. Worth a separate ticket.

  Happy to write the audit SQL and the model-default change if it helps.
  ```

  ### Exit
  working_on cleared. Reply drafted only — not sent. Awaiting user approval before posting.

  --- (earlier, partially-incorrect framings preserved below for context) ---

  ## Agent run 2026-05-27T18:55Z (revised after user supplied onboarding-history + plan-output evidence)

  ### Mike's question
  PMS-8298: Travelodge Lubbock — gateway had Discover mapped as `DS`, should be `DI`. Mike was told this was a side-effect of scripted enterprise onboarding and is asking whether a wider cohort needs the same fix.

  ### Earlier (wrong) hypothesis — discarded
  Initially guessed this was a finite Feb-6-to-Feb-26 2024 window where the Wyndham **SPH (SynXis)** dict briefly wrote `DS` before being corrected to `DI`. User's screenshot showed Lubbock was first scripted on **2025-12-15**, well after that window, and the user then confirmed the vendor on this hotel is **`oracle_ohip`** (Plan output: `Vendors: oracle_ohip`). So the SPH window theory does not apply to Lubbock and is not the right framing.

  ### Real bug location
  Travelodge Lubbock went down the **OPERA / OHIP branch** of `wyndham_pms_config_provider.py` (line 134 `elif self.vendor == Vendor.OPERA:`), which writes three hardcoded dicts onto the OhipConfiguration:

  ```python
  # wyndham_pms_config_provider.py:102-109
  payment_methods_ohip = {
      "JCB": "JC", "Visa": "VI", "Discover": "DS",
      "MasterCard": "MC", "Diners Club": "DC", "American Express": "AX",
  }
  # :111-118
  payment_methods_ohip__opi = {
      "JCB": "JC", "Visa": "VA", "Discover": "DS",
      "MasterCard": "MC", "Diners Club": "DC", "American Express": "AX",
  }
  # :120-126
  payment_methods_ohip__offline = {
      "Visa": "MVA", "Discover": "MDS", "MasterCard": "MMC",
      "American Express": "MAX", "Diners": "MDC",
  }
  ```

  All three are hardcoded — there is no per-property override. So **every Wyndham OHIP hotel scripted-onboarded since 2023-10-30** (when this path first landed, commit `8f19194b53`) gets `payment_methods["Discover"] = "DS"`, `opi_payment_methods["Discover"] = "DS"`, and `offline_payment_methods["Discover"] = "MDS"` written to the gateway.

  Mike's report says for Lubbock the correct value was `DI`, not `DS`. The Wyndham **SPH** branch correctly uses `DI` (line 129) which is the giveaway that `DS` was the wrong assumption for the Wyndham OHIP path too — at least for some properties. OHIP payment-method codes are configured per-property in Opera, so there is no single "correct" value vendor-wide; the script's "one hardcoded dict for every OHIP property" approach is the underlying bug.

  ### Blast radius
  - **Population at risk:** every Wyndham hotel where `pms_2__c` resolves to `Vendor.OPERA` and which was onboarded (or re-onboarded) via WYNDHAM_MSA Configure-PMS since 2023-10-30. That is the entire scripted Wyndham OHIP cohort over ~2.5 years — not a narrow window.
  - **Actually broken subset:** the hotels whose OHIP property config expects `DI` (or any value other than `DS`) for Discover. Lubbock is one; "other hotels corrected in the past" in the PMS-8298 thread are presumably others. Without an OHIP-side audit we don't know the size of this subset.
  - **Cross-brand:** BW also hardcodes `Discover: DS` for Jonas Chorum (line 132) and OHIP (line 183/191) and `MDS` for offline (line 198) in `best_western/pms_config_provider.py`. Same anti-pattern, same potential for property-specific mismatches. Worth flagging even if no BW reports yet.

  ### Recommended remediation (not done — for Mike / Sharon)
  1. **Data audit, gateway-side.** Query `OhipConfiguration` rows for Wyndham accounts: how many have `payment_methods->>'Discover' = 'DS'`? (Should be the whole scripted cohort.) Cross-reference with each property's actual OHIP Discover code (either from Opera config exports or by sampling a Discover transaction). Flip the wrong ones.
  2. **Code fix, longer-term.** Stop hardcoding per-vendor Discover codes in onboarding. Either (a) source from per-property `OnboardingValue` filled at intake, or (b) call OHIP at configuration time to discover the actual code, or (c) explicitly require a human review step before go-live so misses surface immediately.
  3. **Spot-check BW.** Same hardcoding pattern in `best_western/pms_config_provider.py` — quick check whether any BW Discover-card incidents exist would tell us whether this is a Wyndham-only problem or systemic across brands.

  This is a more serious finding than I first reported. Pure data-fix doesn't close it permanently; the script will keep writing wrong values for any new Wyndham OHIP hotel until someone changes the model.

  ### Reply drafted (NOT SENT — Mike's DM)
  ```
  Hi Mike — first answer was wrong, ignore it. Updated:

  Lubbock runs on `oracle_ohip`, so the script took the OHIP branch of `wyndham_pms_config_provider.py:134-173` and wrote three hardcoded dicts: `payment_methods` (line 102-109), `opi_payment_methods` (111-118), `offline_payment_methods` (120-126). All three set Discover = `DS` / `MDS`. There is no per-property override — every Wyndham OHIP hotel scripted-onboarded since the path was introduced on 2023-10-30 has had the same values written to its gateway config.

  Some properties' OHIP is configured to expect `DI` (Lubbock among them — and per PMS-8298 comments, others have been corrected ad hoc). The script can't know that because OHIP Discover codes are per-property in Opera. So yes — this is a wider issue than one hotel, and the data fix alone won't stop new Wyndham OHIP hotels from getting the same wrong values on next scripted onboarding.

  Two parts to a real fix:
  1. Data audit: identify Wyndham OHIP hotels where the gateway-side Discover value doesn't match what their OHIP expects, and flip them.
  2. Code change: source the per-vendor Discover (and probably the whole dict) from per-property onboarding values rather than hardcoding. Same pattern exists in BW (`best_western/pms_config_provider.py` lines 132, 183, 191, 198) — worth a spot-check on BW Discover incidents to size the risk.

  Happy to scope the data-audit query and/or write the script change if that helps. Just say where this should live — sounds like a PMS / enterprise-onboarding follow-up rather than a one-off.
  ```

  ### Exit
  working_on cleared. Did not send the Slack reply — drafted only, awaiting user approval before posting.
project: null
source_id: https://canarytechnologies.slack.com/archives/D0B72KW7ZBJ/p1779809895591949
tags:
- morning-gtd
- slack
time_minutes: 15
title: 'Reply to Mike Bretherick re: Discover-card mapping (DI vs DS) in scripted
  enterprise onboarding'
updated: 2026-05-27 13:20:15.439878
waiting_on: null
waiting_since: null
working_on: false
---

Mike resolved PMS-8298 (Travelodge Lubbock); asks if scripted enterprise onboarding had wider impact on Discover-card mapping. https://canarytechnologies.slack.com/archives/D0B72KW7ZBJ/p1779809895591949