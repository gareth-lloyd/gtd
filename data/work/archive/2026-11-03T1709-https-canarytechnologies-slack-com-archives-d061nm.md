---
area: null
completed_at: 2026-11-04 16:13:08.491353
contexts: []
created: 2026-11-03 17:09:11.568242
defer_until: null
due: null
energy: low
id: 2026-11-03T1709-https-canarytechnologies-slack-com-archives-d061nm
order: null
output: |
  ## Agent run 2026-11-03T17:40:00+02:00

  **Ask (Andrea, DM 2026-11-03 https://canarytechnologies.slack.com/archives/D061NMRMFB3/p1793716233606339):** push AP to add Malay support for APAC-210 (https://linear.app/canary-technologies/issue/APAC-210/support-malay-as-a-hotel-language-for-gj-messages), or decide whether ENT owns it. Marta re-pinged Andrea on the ticket today asking for a Wyndham timeline; now 10 sites asking.

  ### TL;DR
  - Ownership was already settled on 2026-10-08: you told Connor "APAC is ideal" / "Agree no gatekeeping" and Connor said ENT would script the Malay GJ messages (group DM https://canarytechnologies.slack.com/archives/C0B1Y5K9AMC/p1791469547676669). Nothing has changed to reverse that. Recommend: **APAC owns the locale, ENT owns the Wyndham-provider fix.**
  - APAC has stalled, not refused: Peter Gao asked Belinda in #epd-apac-engineers on 2026-10-21 whether to slot it ASAP or wait, and the thread has no reply (https://canarytechnologies.slack.com/archives/C0BJKKPLJAY/p1792570678027869). Ticket is still Triage, unassigned. That thread is the place to push.
  - The work is smaller than the ticket thread implies. Malay (`ms`) is already registered on the backend; only the Django `LANGUAGES` entry, the frontend language map, and the generated locale files are missing. Finnish precedent: two PRs by mdekkernet, 6 days apart.
  - ENT has its own bug here regardless: the Wyndham onboarding provider provisions `ms` as the *default* guest language for Malaysian hotels even though the frontend cannot render it. That is why ENT-7792 (hotel 60886 cannot save GJ templates) is Blocked and why MSG-6845 had to flip the default back to `en` by hand.

  ### What is actually missing (verified in repo)
  Already present for `ms`: `shared/guest/languages.py` (ISO639Languages.MALAY), `canary/schemas/validators.py` (LANGUAGE_CODE literal + SUPPORTED_LANGUAGES, so GJ messaging accepts it), `Hotel.supported_languages` choices, chat auto-translation choices. Wyndham GJ provider lists `ms` in the 24h and 72h check-in available-language sets.
  Missing: `canary/settings/base.py` LANGUAGES entry; `frontend/packages/shared/constants/languages.ts` (no `ms` at all, which is why the admin picker does not show it, per Dmitry on ENT-7792); no `backend/canary/canary/locale/ms/` and no `ms.json` in any frontend app. The repo has `make translate-add-lang LANG=ms` for the backfill. Dashboard/staff language (`DASHBOARD_LANGUAGES`, `language_middleware.SUPPORTED_LANGUAGES`) is optional and not needed for the Wyndham ask.
  Process doc: Notion "Language Translation System", Adding a New Language section (https://app.notion.com/p/3258146861518012b381e02f14f53790).
  Precedent: #59767 backend registration (+224 lines) https://github.com/canary-technologies-corp/canary/pull/59767 and #60541 Finnish locale (+38.8k generated lines) https://github.com/canary-technologies-corp/canary/pull/60541. For Malay, most of #59767 is already done.

  ### ENT-side cause
  `onboarding/configuration_providers/wyndham/wyndham_supported_languages_provider.py` maps Malaysia default -> `ms` (and Singapore additional -> `ms`). You removed unsupported defaults in ENT-3589 (June 2025), then PR #50249 "Reconcile Wyndham default and supported languages by country" (abrad, merged 2026-07-15, https://github.com/canary-technologies-corp/canary/pull/50249) rewrote the table from the Wyndham CSV and reintroduced `ms`. The #50249 note promised a backfill command for already-live hotels; I found no such commit. Hotel 60886 was onboarded 2026-09-28 with `ms` as default (Dmitry's analysis on ENT-7792 https://linear.app/canary-technologies/issue/ENT-7792/guest-journey-template-issue; Agustin's fix on MSG-6845 https://linear.app/canary-technologies/issue/MSG-6845/add-guest-facing-languages-for-the-orion-kuala-lumpur-60886).
  Decision for you: either (a) ship a small ENT PR making Malaysia default `en` with `ms` as additional (stops new Malaysian onboardings breaking the GJ editor) or (b) leave it and lean on APAC shipping the locale within ~2 weeks. (a) is the safe default if APAC cannot commit a date this week.

  ### Not done / blocked
  - Tried to count live hotels already carrying `ms` (EU/AP/US) with `canary prod-db query`; the permission classifier blocked it. Marta's number (10 sites) is the best figure available.
  - No messages sent, no Linear comments posted. Drafts below.

  ### Drafts (not sent)
  1. Reply to Andrea (DM):
  > Already decided with Connor on 8 Oct that APAC owns it, and I still think that is right: the backend registration for `ms` is already in place, so it is really the frontend map + `make translate-add-lang LANG=ms` (the Finnish PR shape). Peter asked Belinda on 21 Oct whether to prioritise and never got an answer, so I'll push there. Separately, our Wyndham provider provisions `ms` as the Malaysia default, which is what broke 60886's GJ editor (ENT-7792). I'd like ENT to flip that to en-default until the locale ships. OK with you?

  2. Push in #epd-apac-engineers, reply to Peter's thread https://canarytechnologies.slack.com/archives/C0BJKKPLJAY/p1792570678027869 (cc Belinda, Adil):
  > Bumping this one. Wyndham now has 10 Malaysian sites asking and are chasing for a date on APAC-210. Scope is smaller than it looks: `ms` is already registered in validators/ISO639Languages, so it's the `LANGUAGES` setting, `languages.ts`, and `make translate-add-lang LANG=ms`, same shape as the Finnish PRs (#59767, #60541). Could you slot it this cycle and put a target date on the ticket so CS can tell Wyndham? ENT will script the Wyndham GJ messages in Malay and fix our onboarding provider in parallel.

  3. Linear comment on APAC-210 answering Marta:
  > APAC team owns this; ENT will handle the Wyndham onboarding side (our provider currently sets Malay as default for Malaysian hotels before the UI supports it, which is what broke 60886). Backend registration for Malay already exists, so remaining work is the frontend/locale pass. @pgao / @ashaikh to confirm a target date.
project: null
source_id: null
tags: []
time_minutes: 5
title: https://canarytechnologies.slack.com/archives/D061NMRMFB3/p1793716233606339
updated: 2026-11-04 16:13:08.491347
waiting_on: null
waiting_since: null
working_on: false
---