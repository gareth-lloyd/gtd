---
area: null
completed_at: null
contexts:
- react
created: 2026-11-13 09:54:27.931484
defer_until: null
due: null
energy: medium
id: 2026-11-13T0954-review-pr-64913-stay-5961-add-set-guest-sign-in-co
order: null
output: |
  ## Agent run 2026-11-13T10:08

  Reviewed PR #64913 (https://github.com/canary-technologies-corp/canary/pull/64913) by reading the diff and the code it calls. Nothing posted to GitHub.

  **Verdict: no blocking defects in the command. Approve once the base PR is green, with two rollout questions for Ishwar.**

  ### What I checked
  - Diff: 2 new files, `hotels/management/commands/set_guest_sign_in.py` (134 lines) and its test (183 lines).
  - `Hotel.save()` and every `post_save`/`pre_save` receiver on Hotel, to see what a per-hotel save triggers.
  - CI: `make test-backend` passes on this PR. I did not run the tests locally.
  - The stack: #64907 field/migration (https://github.com/canary-technologies-corp/canary/pull/64907), #64911 backend gate (https://github.com/canary-technologies-corp/canary/pull/64911), #64912 frontend (https://github.com/canary-technologies-corp/canary/pull/64912). Ticket STAY-5961 (https://linear.app/canary-technologies/issue/STAY-5961/disable-anonymous-reservation-lookup-everywhere-except-paired-devices) has no comments.

  ### Holds up
  - Dry run by default, `--state` required, targets mutually exclusive, blank or unknown targets fail before any write.
  - `save(update_fields=["has_guest_sign_in"])` per hotel is right: the field is in `CONFIG_FIELDS`, so the config-change event fires with source `management_command` (tested). It writes no other column.
  - The v3 flow reseed receiver is skipped, because `has_guest_sign_in` is not in `_HOTEL_RESEED_FIELDS`. The remaining per-save cost is a `HotelSlug` lookup, two `exists()` checks, and `ensure_default_addons_exist` for add-on hotels.
  - Idempotent: a re-run only touches hotels still on the old value. One failing hotel does not stop the rest, and the command exits non-zero with the failed ids split into `written` / `not_written` / `unknown`.

  ### Questions worth raising (rollout, not code)
  1. **Coverage gap for an incident fix.** The field defaults to on (#64907), and `--all-live-hotels` skips non-live, inactive and demo hotels. A hotel created or taken live after the run has anonymous lookup on again. If SEC-1762 wants lookup off everywhere, the plan needs either a default flip or a repeat run. Ask which is intended.
  2. **Ordering and regions.** #64911 says not to turn a hotel off until the backend and frontend PRs are live in that hotel's region. The command has no guard for this, and it must be run once per region (US, EU, AP).

  ### Minor, non-blocking
  - A full `Hotel.save()` across every live hotel can create missing default add-ons, room upgrade tiers and available forms as a side effect. The author defended this in the PR body and it matches the repo rule. The dry run does not exercise `save()`, so a small portfolio commit before `--all-live-hotels` is worth suggesting.
  - `sum(len(hotel_ids) for hotel_ids in error_hotel_ids.values())` reuses the outer name `hotel_ids`. It works, but a rename would read better.
  - `--management-company` is a case-insensitive prefix match with no minimum length, so `--management-company a --commit` hits every company starting with "a". The matched-companies log only helps if the operator runs the dry run first.
  - `--portfolio wyndham` does not cover `wyndham_emea`, `wyndham_latam` or `wyndham_seapr`, which are separate identifiers. This is documented, but the operator needs one run per identifier.
  - The `unknown` outcome branch has no test (stated in the PR).
  - "1 hotels raised an error" in the error message.

  ### CI and merge state
  - `Backend linters` fails on two sub-checks: `check-generate-setting-types` (`rules_based_configuration/types/setting_keys.py` is stale) and `check-mcp-sql-grants` (`canary_mcp_ro.json`/`.sql` out of date). Run: https://github.com/canary-technologies-corp/canary/actions/runs/43383383349/job/131746098517. This PR adds only a command and a test, so the cause is almost certainly the new field in base PR #64907, which also fails `Backend linters`. I did not open the base PR's log to confirm.
  - Base PR #64907 also fails `make test-backend` and `Birdline policy`. I did not investigate those. This PR cannot land until the base does.
  - No reviews on either PR yet.

  ### Draft review comment (not posted)
  > Command looks good to me: dry run by default, per-hotel save so the config-change event fires, and failures are reported without stopping the run. Two rollout questions before this is used for SEC-1762:
  > 1. The field defaults to on and `--all-live-hotels` skips non-live/inactive/demo hotels, so a hotel that goes live after the run has lookup on again. Is the plan to flip the default afterwards, or to re-run?
  > 2. Can the runbook say explicitly: only after #64911 and #64912 are live in the region, once per region, and a small portfolio with `--commit` before `--all-live-hotels` (the dry run does not exercise `Hotel.save()` hooks)?
  >
  > Nits: the `hotel_ids` name is reused in the `error_count` generator; `--management-company` accepts a one-character prefix.
  >
  > The lint failure (stale `setting_keys.py` and MCP SQL grants) looks inherited from #64907 and needs regenerating there.
project: null
source_id: https://github.com/canary-technologies-corp/canary/pull/64913
tags:
- morning-gtd
- github
time_minutes: 15
title: 'Review PR #64913: [STAY-5961] Add set_guest_sign_in command'
updated: 2026-11-13 10:08:22.000000
waiting_on: null
waiting_since: null
working_on: false
---

SEC-1762 incident fix. Author in15 (Ishwar), branch in15/guest-sign-in-toggle-command.
https://github.com/canary-technologies-corp/canary/pull/64913