---
area: null
completed_at: null
contexts:
- react
created: 2026-08-31 06:55:56.247733
defer_until: null
due: 2026-08-31
energy: medium
id: 2026-08-31T0655-answer-the-zendesk-one-click-sso-url-question-on-e
order: null
output: |
  ## Agent run 2026-08-31T15:05:00

  Researched the code and full ticket/Slack history. Nothing posted anywhere — draft comment below awaiting your approval.

  ### 1. The prefix Nensy asked about is correct

  Confirmed against `backend/canary/internal_support/services/zendesk_remote.py` (REGION_HOSTS):
  - US `https://www.canarytechnologies.com`
  - EU `https://eu.canarytechnologies.com`
  - APAC `https://ap.canarytechnologies.com`  ← note `ap.`, not `apac.` (the `apac.` in an old ENT-4162 comment is wrong)

  Path is `/sso/idp/zendesk?return_to=<encoded>`, registered at `backend/canary/sso/urls.py:18` -> `sso.views.views.zendesk_jwt` (`backend/canary/sso/views/views.py:487`). The EU/APAC links Nensy posted in Slack on 19 Aug are correctly formed — I reproduced them byte-for-byte.

  ### 2. Encoding rules

  `zendesk_jwt` does exactly ONE `urllib.parse.unquote()` on `return_to`, then re-quotes it into the Zendesk form action (`sso/templates/zendesk_jwt.html`). So:
  - Percent-encode the target URL **exactly once, with nothing safe**: `:`→`%3A`, `/`→`%2F`, `?`→`%3F`, `=`→`%3D`, `&`→`%26`, `#`→`%23`, space→`%20`.
  - Never double-encode. A `%25` in the link means it was encoded twice; the single unquote leaves it still-encoded and Zendesk errors.
  - Never leave it raw. A raw URL survives *today* for simple article slugs (unquote is a no-op) but truncates the moment the target has its own `?`, `&` or `#`. Encode-once is the only safe rule.

  Generator: `python3 -c "import urllib.parse,sys;print('https://eu.canarytechnologies.com/sso/idp/zendesk?return_to='+urllib.parse.quote(sys.argv[1],safe=''))" '<article url>'`
  Or in a browser console: `encodeURIComponent(url)`.

  ### 3. The better answer: in-product links shouldn't be regional at all

  The dashboard is served from the user's own region hostname, so a **relative** `/sso/idp/zendesk?return_to=...` is region-correct by construction — no detection, no three variants. That's exactly what ENT-4162 / PR #31057 (https://github.com/canary-technologies-corp/canary/pull/31057) did for the profile-menu FAQ link (`frontend/packages/shared/components/HeaderDropdownProfile.vue:246,411`), and why that one works today for EU/APAC.

  **Guille does not need to make the URL dynamic per region.** The Front Desk Upsells link he's stuck on is one line:
  `frontend/adminland/src/views/IntegrationsSettings/frontDeskUpsells.ts:5` — `ORACLE_OHIP_SETUP_GUIDE_URL` is a bare `https://canarysupport.zendesk.com/...` URL. Change it to the relative trampoline form and it works in all three regions. (Rendered with `target="_blank"` at `FrontDeskUpsellsSettings.vue:118` — fine with a relative href. Two spec files assert the current string and would need updating.)

  Same bare-URL bug exists at `frontend/adminland/src/views/POSGatewaySettings/POSGatewaySettings.vue:49` (Micros Simphony guide), so this deserves a sweep for bare `canarysupport.zendesk.com` hrefs, not a one-off fix.

  Absolute `eu.`/`ap.` prefixes are only genuinely needed **outside** the product — Zendesk macros, emails, AppCues, Slack — where there's no host context. That's the residual manual burden for Support.

  ### 4. Is "temporarily public" acceptable? — Yes, and I'd argue for permanent

  - The article is an OHIP flex-link setup guide: no customer data, no credentials, nothing commercially sensitive. The gate buys nothing and costs a support round-trip for every non-US customer.
  - The gate isn't a security control anyway — any signed-in Canary user from any hotel can already read it.
  - Real risk of "temporary": it silently becomes permanent and nobody revisits. If we do it, pair it with shipping the relative-link change, then decide deliberately whether to re-gate.
  - Content policy is Blake's/Support's call, not engineering's — but engineering has no objection.

  ### 5. On Nensy's bigger ask (single link with region picker)

  Already designed in ENT-4162 — Lautaro's `/sso/router` proposal with a cross-region session check. I would not build it: it leans on cross-subdomain credentialed fetches that I tested inconclusively at the time (`SESSION_COOKIE_DOMAIN` would need changing to `.canarytechnologies.com`), and it only helps the out-of-product case. Cheaper 80%: relative links in-product (~free) + a documented 3-line region table for Support macros. If we later want one external link, a static three-button region chooser beats auto-detection.

  ### Not verified (flagging honestly)

  - I have **not** tested cold as a logged-out EU user. The `@login_required` → region login → MFA → back-to-trampoline chain is the part most likely to drop the `next` param. Jerome and Isaac both confirmed the EU link worked for them on 19 Aug (Slack thread), but they may already have had sessions. Worth one incognito test before we declare it solved.
  - I have **not** checked the Zendesk-side config: what the remote login URL is currently set to, or whether the EU/APAC *brands* created in ENT-4162/ENT-4824 are live or vestigial. That's Zendesk admin, not the repo.

  ### Draft Linear comment (NOT POSTED — needs your approval)

  > **On the URL format — yes, that prefix is right.**
  > `https://eu.canarytechnologies.com/sso/idp/zendesk?return_to=<encoded>` and `https://ap.canarytechnologies.com/sso/idp/zendesk?return_to=<encoded>` (note `ap.`, not `apac.`). US is `https://www.canarytechnologies.com`. The links Nensy posted in Slack are correctly formed.
  >
  > **Encoding rule:** percent-encode the article URL exactly once, escaping everything including `/` and `:` (`encodeURIComponent(url)` in a browser console does it). Don't double-encode — if you see `%25` in the link it's been encoded twice and will fail. Don't leave it raw either; that happens to work for plain article slugs but breaks as soon as the target URL has its own `?`, `&` or `#`.
  >
  > **But for in-product links we shouldn't be building regional URLs at all.** The dashboard is already served from the user's own region, so a relative `/sso/idp/zendesk?return_to=...` is region-correct automatically — that's what we did in ENT-4162 for the profile-menu FAQ link, and it's why that one works for EU/APAC today. @gaguirre — you don't need to make the Front Desk Upsells link dynamic per region. It's a one-line change in `frontDeskUpsells.ts` to wrap the existing Zendesk URL in the relative trampoline path. The same bare-URL issue exists on the POS Gateway settings page, so I'd sweep for these rather than fix one.
  >
  > Regional absolute prefixes are only needed outside the product (Zendesk macros, emails, AppCues), where there's no host to be relative to.
  >
  > **On going temporarily public:** no objection from engineering, and honestly I'd consider making it permanent. It's a setup guide with no customer data or credentials, and the gate isn't a security control — every signed-in Canary user can already read it. The only risk is that "temporary" quietly becomes forever, so if we open it up let's also ship the relative-link fix and then re-gate (or not) as a deliberate decision.
  >
  > **One thing still untested:** nobody has confirmed the flow cold, from a logged-out EU browser. Jerome and Isaac confirmed the links work but may have had live sessions. Could someone try the EU link in an incognito window and confirm they land on the article after logging in? That's the step most likely to drop the redirect.
  >
  > **On a single region-picker link** (Nensy's broader ask): we designed this in ENT-4162 as `/sso/router` with a cross-region session check. I'd not build it — it depends on cross-subdomain cookie behaviour I couldn't get a clean result on, and it only helps the out-of-product case. If we want one external link later, a static three-button region chooser is the simpler version.

  ### Suggested next steps

  1. Get the incognito EU test done (Support can do this in minutes) — that's the real unknown.
  2. One-line PR: relative trampoline URL in `frontDeskUpsells.ts` (+ `POSGatewaySettings.vue`, + two spec updates). ~15 min.
  3. Tell Blake the public-page fallback is fine by engineering, so his Tuesday deadline is de-risked either way.
project: 2026-04-16T1210-unblock-team
source_id: https://linear.app/canary-technologies/issue/ENT-7027
tags:
- morning-gtd
- linear
time_minutes: 20
title: Answer the Zendesk one-click SSO URL question on ENT-7027 before Blake's EoD
  Tuesday fallback
updated: 2026-08-31 14:39:10.093510
waiting_on: null
waiting_since: null
working_on: true
---

Blake, 28 Aug: if not resolved by EoD Tuesday they will make the help centre page PUBLIC temporarily until SSO is solved. Now assigned to kcormier, but Nensy's @glloyd question on the eu./ap. sso/idp/zendesk?return_to= link format is still unanswered. Weigh in on the format and on whether temporarily public is acceptable.
https://linear.app/canary-technologies/issue/ENT-7027