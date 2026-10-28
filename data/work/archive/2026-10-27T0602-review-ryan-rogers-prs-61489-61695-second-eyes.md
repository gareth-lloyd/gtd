---
area: null
completed_at: 2026-10-27 13:34:08.004508
contexts:
- react
created: 2026-10-27 06:02:51.227629
defer_until: null
due: null
energy: medium
id: 2026-10-27T0602-review-ryan-rogers-prs-61489-61695-second-eyes
order: null
output: |
  ## Agent run 2026-10-27T08:36:04

  **State.** #61695 (https://github.com/canary-technologies-corp/canary/pull/61695, the base PR) has no reviews yet and its CI is green. #61489 (https://github.com/canary-technologies-corp/canary/pull/61489, the Wyndham wiring) has patrickcanny's approval. Andrea left 9 inline notes on it yesterday (made with Claude), and Ryan answered or fixed all of them. One is deferred to a follow-up: a country-policy injection key to replace the prop. Andrea said in Slack she'd look at both today (https://canarytechnologies.slack.com/archives/C0B1MN8F869/p1793050504737189). On #61489, only "Evaluate auto-approval policies" fails, which is expected for a PR that needs human review.

  **What it does.** Wyndham country dropdowns list CN, HK, MO and TW as "<region>, Greater China". Before, they showed one "Greater China" entry and hid TW/HK/MO. Only labels change. The stored value is still the ISO code, so no data or PMS changes. The policy is `getSplitRegions(hotel)`, which checks for the WYNDHAM or WYNDHAM_STAGING portfolio. Components read it from the injected hotel, or from a `splitRegions` prop in kiosk and payment links.

  **What I checked (read the code; did not run it).**
  - Every app that provides HOTEL_INJECTION_KEY (check-in, guest, guest-experience, hotels, authorizations, adminland) gets a hotel type that carries `portfolio_identifiers`. Kiosk uses `GuestHotelSchema`, which already had them. For authorizations, all four store paths (form, generic link, contract/sales booking, payment link) now go through `HotelWithPortfoliosSchemaExternal`. `hasPortfolio` returns false when the field is missing, so a path I missed would fail safe to no split rather than throw.
  - All 6 kiosk `CanarySelectCountry` fields and `PaymentForm` pass the prop. `AuthorizationPaymentMethods` gets the policy through the inject. Kiosk renders no schemaform `Country`.
  - The backend schema split is sound. Wallet, voice and hotel_device still nest the base `HotelSchemaExternal`, so none of those pay the extra Portfolio query. There is a test that non-public portfolios stay out.

  **Points worth raising (none blocking):**
  1. *Native-select findability (product).* Schemaform `Country` is a plain `<select>` with no search. In English, China now sorts under **M** ("Mainland China, Greater China"). A guest who scrolls or types "C" to find China won't find it there. `CanarySelectCountry` is fine, because `plainName` stays a search term. Ryan already switched to per-label sorting and said he'd check with Ani. This is the concrete case to put to Ani.
  2. *Latent crash in `getGreaterChinaNames` (#61695).* `message(key)` returns `messages[key] ?? englishMessages[key]` but is typed `string`. If an English key ever goes missing or is mistyped, a label becomes `undefined` and the final `.sort((a, b) => a.name.localeCompare(b.name))` throws. That would take down the whole dropdown, not just one label. A final `?? key` fallback, or a test that all four keys exist in en.json, would close it.
  3. *Not tried in a browser.* The PR says so. Worth one pass on a live branch or staging with a Wyndham hotel before merge: a guest check-in reg card, a kiosk identity step, and a staff check-in details view.
  4. *Unverified:* I did not check backend-rendered places that print a country name, such as reg card PDFs or exports. They will presumably still say "Taiwan", not "Taiwan, Greater China". That's worth a one-line confirmation that it's acceptable to Wyndham.
  5. Adminland now splits too, because it provides the hotel, except `CompendiumPropertyInfo.vue`. Andrea already raised that.

  **Suggested action.** Andrea is covering the full review, so a second review isn't needed. If you want to add something, point 2 is the one code change worth asking for on #61695, and point 1 is the product question for Ani. Nothing was posted anywhere. Draft comment for #61695 if you want it (not sent):
  > `getGreaterChinaNames`: `message()` is typed `string` but can return `undefined` if a key is missing from en.json too, and then the sort's `localeCompare` throws and the whole list fails to load. Could it fall back to the key, or could a test pin the four keys in en.json?
project: null
source_id: https://canarytechnologies.slack.com/archives/C0B1MN8F869/p1793050504737189?thread_ts=1793050504.737189&cid=C0B1MN8F869
tags:
- morning-gtd
- slack
- from-awareness
time_minutes: 20
title: 'Review Ryan Rogers PRs #61489/#61695 (second eyes)'
updated: 2026-10-27 13:34:08.004499
waiting_on: null
waiting_since: null
working_on: false
---

Ryan wants a second reviewer on #61489, a feature he's not familiar with, and split out a base PR, #61695. Andrea said she'd look today.
https://github.com/canary-technologies-corp/canary/pull/61695
https://github.com/canary-technologies-corp/canary/pull/61489
https://canarytechnologies.slack.com/archives/C0B1MN8F869/p1793050504737189?thread_ts=1793050504.737189&cid=C0B1MN8F869