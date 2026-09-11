---
area: null
completed_at: 2026-09-10 15:00:25.539736
contexts:
- react
created: 2026-09-10 09:12:48.847285
defer_until: null
due: null
energy: medium
id: 2026-09-10T0912-review-pr-55083-dissolve-ihg-core-plus-plan-subcla
order: null
output: |-
  ## Agent run 2026-09-10T11:25:41

  Reviewed PR #55083 (https://github.com/canary-technologies-corp/canary/pull/55083), ticket ENT-7438 (https://linear.app/canary-technologies/issue/ENT-7438). Head c82063d3f6d, based on current master. Nothing posted to GitHub or Linear.

  **Verdict: approve with comments.** Nothing blocking. #1 is the one I'd want fixed, or explicitly accepted, before merge.

  ### Checked and safe
  - Old plan names saved on existing batches: the runner (onboarding_batch.py:928) turns each name into a plan class and keeps only classes the stage wires. So a saved `IHGGmsCorePlusDeactivateTippingPlan` becomes DeactivateTippingPlan, which Core Plus no longer wires, and is dropped. It does not run without its old guard. The old go-live name becomes TippingGoLivePlan with the country-keyed providers.
  - Dropping the deactivate plan from Core Plus base config: the PR's claim holds. For a hotel not yet live, deactivate only reset flags that ConfigureTippingPlan puts back (setup_hotel sets has_tipping; tip providers set can_be_tipped=False). `Configuration.save()` forces can_be_tipped off when the hotel has no tipping, so the one state deactivate could have mattered for can't happen.
  - The nine other tipping types: their CONFIGURE_TIPPING stage runs Deactivate, then Configure, then Department, so the new "already live" guards don't block Wyndham-style re-templating. All nine TippingGoLivePlan wirings got DefaultTippingGoLiveProvider; none are left with no provider.
  - The ENSURE_MARRIOTT_DEPARTMENTS rollout (rollouts.py:428) runs DepartmentPlan on live tipping hotels. It is NOT affected: rollouts call `execute_rollout`, which goes straight to the provider and never reaches `execute`.
  - `can_be_tipped` defaults to False and every tip provider sets it False, so the go-live guard won't skip a hotel's first go-live.
  - Health service mapping old names to base plans: harmless (only used to check for missed plans).
  - CI: `make test-backend`, lint and migration checks pass. `review-bot` fails only because no one from its reviewer group [rrgrs, lmenaolivares, andresfigueira, martinrodriguezcanary] has approved yet; not a code problem. Playwright E2E shard 4/4 fails but is non-blocking; not investigated (backend-only PR). I did not run tests locally.

  ### Comments to raise
  1. **(should) Core Plus hotels with no tips Configuration now crash at go-live with a raw `NotFound`.** The old subclass returned "No tipping configuration" for these. The Core Plus script shipped 2026-08-20 (#53676) but tipping was only wired in on 2026-08-25 (#53898), so hotels base-configured in between have no Configuration. `NotFound` is also not an ExpectedOnboardingPlanError; the onboarding CLAUDE.md asks plans to use `raise_expected_error`, and `ERROR_TIPPING_CONFIGURATION_DOES_NOT_EXIST` already exists (DepartmentPlan uses it). Suggest a check for a Configuration before `set_can_be_tipped` that raises the expected error: still fails the run, but with a message operators can act on. Ask Andrea whether any Core Plus hotels were base-configured between 08-20 and 08-25.
  2. **(question) DEFAULT onboarding type base config.** property_configuration_processes.py ~L3145 wires DepartmentPlan with the management-company department providers (Aimbridge, Crestline, Marriott, Pyramid, Raymond, Buffalo, Stonebridge), with no deactivate before it. Re-running base config on a hotel already live on tipping now skips both creating departments and the provider's own step (MarriottDepartmentProvider deletes unused departments there). The PR's heads-up mentions this. Worth a quick yes from whoever owns management-company/Marriott tipping that re-running base config to add departments is not something ops does; the rollout is the supported way.
  3. **(nit) TippingGoLivePlan quietly succeeds with no provider.** The docstring says swallowing a missing config "would report success and leave the hotel not live", and the new "No config provider" branch does exactly that. Anyone who later wires TippingGoLivePlan with `config_provider=None` gets a quiet success instead of a failure. Suggest a log line on that branch and a sentence in the docstring.
  4. **(nit)** `TippingGoLiveConfig`: `tippable_department_kinds=None` means "every department" and then `tippable_custom_names_en` is ignored. The type allows a combination that means nothing. Say so in the docstring, or use an explicit flag.
  5. **(nit)** `update_batch_plan_names`: sending an old and a new name together (["IHGGmsCorePlusDepartmentPlan", "DepartmentPlan"]) saves "DepartmentPlan" twice. Dedupe, keeping order.
  6. **(housekeeping)** The ENT-7438 description is out of date: it still describes the `should_skip` hook and `preserve_live_tipping` config flags the PR dropped. Worth asking Andrea to update it.

  ### Draft GitHub review (NOT posted; say the word and I'll post it as a COMMENT/APPROVE review)
  > Nice cleanup: plans/ is brand-free again, and the "no provider = no-op" + intrinsic already-live guards read much simpler than the skip-hook iterations. I checked that saved old names can't bring back an unguarded DeactivateTippingPlan (the runner filters by stage class), and that the Marriott department rollout is unaffected (execute_rollout never reaches execute). A few comments:
  > 1. `tipping_go_live_plan.py`: a Core Plus hotel in a tipping country with no tips Configuration now gets a raw `NotFound` from `set_can_be_tipped`; the old subclass returned "No tipping configuration". Hotels base-configured between #53676 (08-20) and #53898 (08-25) would hit this. Could you check for a Configuration first and `raise_expected_error(ERROR_TIPPING_CONFIGURATION_DOES_NOT_EXIST)`, so it fails with a message operators can act on?
  > 2. DEFAULT base config wires DepartmentPlan with the management-company providers and no deactivate before it, so re-running on a live tipping hotel now skips the provider step as well (e.g. Marriott's unused-department cleanup). Fine by me if ops never re-runs base config on live hotels; just confirming that's intended.
  > 3. Nit: the "No config provider" branch quietly reports success; maybe log it, and update the docstring, which still says swallowing would leave the hotel not live.
  > 4. Nit: `update_batch_plan_names` can save duplicates if old and new names are both sent.
project: null
source_id: https://github.com/canary-technologies-corp/canary/pull/55083
tags:
- morning-gtd
- github
time_minutes: 30
title: 'Review PR #55083: Dissolve IHG Core Plus plan subclasses into config-driven
  tipping plans'
updated: 2026-09-10 15:00:25.539730
waiting_on: null
waiting_since: null
working_on: false
---

Author abrad, branch abradshaw/ENT-7438/dissolve-brand-plan-subclasses. Andrea: 'after a whole lot of back and forth, the tipping refactor is ready for review'.
https://github.com/canary-technologies-corp/canary/pull/55083