---
area: null
completed_at: 2026-11-19 15:34:35.907449
contexts:
- react
created: 2026-11-19 10:06:56.131503
defer_until: null
due: null
energy: low
id: 2026-11-19T1006-reply-to-andrea-re-cross-region-property-switcher
order: null
output: |
  ## Agent run 2026-11-19T12:46

  Nothing sent. Draft reply below for you to post.

  **What I found**

  - Andrea answered her own question two messages later: "Actually, now that I'm talking out loud, I'm wondering if it is even necessary" and then "(removing it)" (https://canarytechnologies.slack.com/archives/D061NMRMFB3/p1795038600013559). So the reply is a confirmation, not a decision.
  - The flag is already gone from the doc (https://app.notion.com/p/3eb81468615181748039ddbe4a6272ee, last edited 2026-11-18 22:04 UTC). The composable now gates on the GrowthBook flag alone (`usesGlobalList = isEnabled`).
  - `has_portfolio_wide_grant` does not exist anywhere in the canary repo, so it was only ever a proposed field.
  - I could not see the old doc version, so what the flag did is my inference: a boolean on the user or portfolio payload that told the frontend whether to use the global list.
  - On that reading it was not a real security risk. Each region decides server-side which hotels the account sees (`HotelAccessPolicy` on its own memberships), so a client-side boolean grants nothing. The cost was a redundant field that exposes grant state and invites someone to treat it as an authorization check later.
  - It is also unnecessary: the doc now says users with hand-picked hotels get the new list too, filtered to their own memberships.
  - The doc has 11 open comment threads, the ones I saw posted 2026-11-19 03:47-03:51 UTC by one reviewer (probably Jordan, not verified). Topics: `canary_region` on every regional object, search needing a search index rather than more list filters, and adding `sso_hotel_id` to the hotel object.

  **Draft reply** (DM to Andrea, in reply to https://canarytechnologies.slack.com/archives/D061NMRMFB3/p1795038510630479)

  > Agree with removing it. I don't think it was a real security risk, since each region still decides server-side what the account can see and the flag would only have been a UI hint. But it isn't needed either: the list already returns only the hotels the account's memberships allow, so a hand-picked user just gets a shorter list. One less thing for Identity to question.
  >
  > Thanks for getting it to Jordan. I'll read it again properly once his feedback has landed.
project: null
source_id: https://canarytechnologies.slack.com/archives/D061NMRMFB3/p1795038510630479
tags:
- morning-gtd
- slack
time_minutes: 10
title: 'Reply to Andrea re: cross-region property switcher proposal and has_portfolio_wide_grant'
updated: 2026-11-19 15:34:35.907444
waiting_on: null
waiting_since: null
working_on: false
---

She shared the proposal with Jordan for Identity feedback (not urgent to re-read). She asks whether has_portfolio_wide_grant is a security risk and is leaning to remove it.
https://canarytechnologies.slack.com/archives/D061NMRMFB3/p1795038510630479