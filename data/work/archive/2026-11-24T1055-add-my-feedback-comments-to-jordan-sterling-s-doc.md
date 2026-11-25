---
area: null
completed_at: 2026-11-24 15:27:26
contexts:
- react
created: 2026-11-24 10:55:42.970319
defer_until: null
due: null
energy: low
id: 2026-11-24T1055-add-my-feedback-comments-to-jordan-sterling-s-doc
order: null
output: |
  ## Agent run 2026-11-24T13:27:03Z

  Posted your DM feedback as three inline comments on Jordan's Notion doc "Public Api Scopes"
  (https://app.notion.com/p/41881468615180dd9367fb44b7247e03). You approved the exact text in session.
  Source DM: https://canarytechnologies.slack.com/archives/D07HCMQU5FY/p1795449557582949

  1. On the first paragraph under "Problem statement" ("An api application can call every route..."):
     "If this is for a Product Manager audience as well as a technical one, can you add a few
     user-facing use cases near the top so they know what they're looking at? I think it would
     frame the doc as a whole nicely."
     https://app.notion.com/p/41881468615180dd9367fb44b7247e03?d=4228146861518154b220001c7a8f4bc1

  2. On "Why not make canary-guest? Should this just be canary ?":
     "My instinct is to keep canary-guest as its own group. Three reasons: (1) the same product
     can have a guest side and a staff side; (2) umbrella scopes are per-group, so a single group
     doesn't capture the kinds of access we'd want to grant in practice; (3) guest endpoints have
     different trust levels. If guest turns out to be first-party only, I'd shrink the guest scope
     list rather than merge the groups."
     https://app.notion.com/p/41881468615180dd9367fb44b7247e03?d=42281468615181408aa0001cc8c18cbf

  3. On "All our guest apis just call underlying Canary apis, we can gate them at the underlying level.":
     "I don't think gating at the underlying API works: the scope check happens at the gateway,
     and the monolith can't tell a guest app from a staff app."
     https://app.notion.com/p/41881468615180dd9367fb44b7247e03?d=42281468615181e5bea9001ce75305a0

  All three create calls returned success. I did not re-fetch the page to check where each anchor
  landed, and the comment links above are built from the returned discussion ids, not copied from Notion.

  Not done: no Slack reply to Jordan saying the comments are in.
  Draft if you want one: "Added them to the doc as inline comments."
project: null
source_id: https://canarytechnologies.slack.com/archives/D07HCMQU5FY/p1795454478070019
tags:
- morning-gtd
- slack
time_minutes: 15
title: Add my feedback comments to Jordan Sterling's doc
updated: 2026-11-24 15:31:56.730141
waiting_on: null
waiting_since: null
working_on: false
---

Jordan: "can you add these comments to the doc. this is great feedback" (my DM feedback: PM-facing use cases; keep canary guest as its own scope group).
https://canarytechnologies.slack.com/archives/D07HCMQU5FY/p1795454478070019