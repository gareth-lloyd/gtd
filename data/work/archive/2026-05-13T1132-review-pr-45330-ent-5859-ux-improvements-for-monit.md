---
area: null
contexts:
- react
created: 2026-05-13 11:32:58.619974
defer_until: null
due: null
energy: medium
id: 2026-05-13T1132-review-pr-45330-ent-5859-ux-improvements-for-monit
order: null
output: "## Agent run 2026-05-13T14:30Z — review of PR #45330\n\n### Summary\nSmall,
  well-scoped change. Author: Martin Rodriguez. +113/-11 across one backend\nservice,
  one backend view, one frontend component, one frontend API binding,\nplus two new
  unit tests. Refresh button no longer requires a selected cohort;\n`onboarding_type`
  becomes optional on the refresh endpoint and on\n`MonitoredHotelStateService.get_states_for_hotels`
  (omitting it returns the\nfull latest-run check results unfiltered).\n\n### Verdict\nApprove
  with one substantive UX concern and a few cleanup nits. Nothing here\nis a blocker,
  but the UX concern (#1) undercuts the headline goal of the PR.\n\n### Concerns\n\n1.
  **Headline timestamp updates while check results stay stale** (UX, worth raising)\n
  \  - After refresh, `lastUpdatedOverride` makes the \"Last updated\" line jump to\n
  \    the new time immediately (or `new Date()` fallback). But the `check_results`\n
  \    rendered beneath it come from `props.monitoredState`, which is sourced\n     from
  the parent's `useMonitoredHotelStatesQuery` (CohortHotelsTable.vue:336).\n     That
  query is not re-fetched after refresh.\n   - `MonitoredCheckResultsDetail.vue:28`
  declares `emit(\"refreshed\")` and\n     fires it on success, but `grep -rn \"@refreshed\"`
  in\n     `frontend/manage/src/views/Cohorts/` returns no listeners. The emit is
  dead.\n   - Net effect: clicking Refresh now shows a fresh-looking timestamp on
  top\n     of the same old check results. Arguably more misleading than the prior\n
  \    behavior (where the timestamp also didn't update without reload, but at\n     least
  the staleness was consistent).\n   - Suggest one of:\n     (a) Have `CohortHotelDetail`/`CohortHotelsTable`
  listen on `@refreshed`\n         and call the relevant `refreshQuery()` from the
  monitoring queries\n         map; or\n     (b) Use the POST response payload more
  fully — Martin already returns\n         the state with `check_results` from the
  backend; the component could\n         expose the refreshed state up to the parent
  (or render from it\n         locally) instead of just pulling `updated_at`.\n\n2.
  **Type cast hack reveals an existing typing bug in the bridge mutation**\n   - `MonitoredCheckResultsDetail.vue`
  post-change does\n     `refreshed as unknown as MonitoredHotelState | undefined`.\n
  \  - Root cause: `useRefreshMonitoredHotelStatesMutation`\n     (`MonitoredHotelStates.ts:62-82`)
  types the axios call as\n     `{ data: MonitoredHotelState[] }` and returns `response.data.data`
  (a list).\n     But the backend POST returns `{ data: state_response }` (singular
  —\n     `monitored_hotel_states.py:114`), and the bridge `stateResponseSchema` is\n
  \    built with `isList: false`. The mutation's response type is therefore\n     wrong
  at both the axios layer and the return value.\n   - Cleaner fix (small): change
  `axios.post<{ data: MonitoredHotelState[] }>`\n     → `axios.post<{ data: MonitoredHotelState
  }>` and drop the cast at the\n     call site. Same scope, one fewer comment-explaining-the-hack.\n\n3.
  **Unreachable guard in `handleRefresh`**\n   - The button is rendered with `v-if=\"salesforceAccountId\"`.
  The early-return\n     guard inside `handleRefresh` checks the same thing. Not a
  bug — just\n     defensive code that can never fire. Fine to leave.\n\n4. **`GetArguments.onboarding_type`
  still required on the GET endpoint**\n   - Intentional, because all current GET
  callers (CohortHotelsTable's\n     per-onboarding-type queries) always have one.
  Worth noting for future:\n     if you ever want a \"show me everything\" GET, you'll
  need to mirror the\n     optional treatment here too. Not an action item for this
  PR.\n\n### Things that look good\n- The `watch(() => props.monitoredState?.updated_at,
  ...)` to clear\n  `lastUpdatedOverride` on cohort switch is the right call — prevents
  a stale\n  override leaking across selections.\n- `YYYY-MM-DD HH:MM:SS UTC` formatting
  from the ISO string is a clean\n  replacement for `toLocaleString()` and removes
  timezone confusion. Server\n  returns aware ISO timestamps via Django `auto_now`
  so `new Date(raw).toISOString()`\n  is safe.\n- Backend `check_result_filters` dict-based
  filter assembly is straightforward\n  and reads well.\n- `monitor_expected_onboarding`
  already took only `salesforce_account_id`\n  (no `onboarding_type`), so making the
  post-run query unfiltered is\n  consistent with how the run-side already works.\n-
  Two new tests cover both branches of `get_states_for_hotels`. Good\n  discipline
  for a small behavior change.\n\n### Action\nDrafted observations only. Did not post
  any comment to the PR. If you'd like\nme to consolidate into a single GitHub review
  comment, say the word and I'll\ndraft the text for your approval before sending.\n"
project: 2026-04-16T1210-unblock-team
source_id: https://github.com/canary-technologies-corp/canary/pull/45330
tags:
- morning-gtd
- github
- from-awareness
time_minutes: 20
title: 'Review PR #45330: ENT-5859 UX improvements for monitoring check results'
updated: 2026-05-13 14:29:55.632831
waiting_on: null
waiting_since: null
working_on: false
---

Martin (pod-enterprise). Refresh button no longer requires selected cohort; backend onboarding_type changes. https://github.com/canary-technologies-corp/canary/pull/45330