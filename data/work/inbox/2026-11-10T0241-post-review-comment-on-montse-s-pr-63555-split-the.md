---
area: null
completed_at: null
contexts: []
created: &id001 2026-11-10 02:41:54.333071
defer_until: null
due: null
energy: null
id: 2026-11-10T0241-post-review-comment-on-montse-s-pr-63555-split-the
order: null
output: ''
project: null
source_id: null
tags: []
time_minutes: null
title: 'Post review comment on Montse''s PR #63555: split the hotel list out of /api/users/me'
updated: *id001
waiting_on: null
waiting_since: null
working_on: false
---

PR: https://github.com/canary-technologies-corp/canary/pull/63555 (mpladevall/users-me-only-embed-fields, "Load only the embedded hotel fields in /api/users/me")

Core learning for Montse: the PR files the edges (.only() trims columns) rather than the core. /me is the blocking bootstrap call for every dashboard; the hotel list is the one large part not needed for first render, so it should be a separate non-blocking request.

Draft comment:

Thanks for this. The `.only()` change is correct and safe, and the test pins the right invariant. I want to push on the framing though, because I think this PR files the edges of the problem rather than addressing its core.

`/api/users/me` is the bootstrap call for every dashboard, and the page cannot render until it returns. Trimming columns makes the Hotel SELECT cheaper, but the request still loads, sorts and serialises every hotel the user belongs to, and for Wyndham staff that is thousands. The page still waits for all of it.

The thing that would actually make the page load fast is to take the hotel list out of the blocking call. `/me` should return identity, permissions, flags, and the small set of things the first render needs. The full hotel list belongs in its own request that the property switcher loads lazily and that the page never waits on.

Two uses of the embed are blocking today and need a home in the split:
- The hotels app resolves the current hotel by slug from `user.hotels` and falls back to `user.hotels[0]` as the default. `/me` already receives `hotel_slug`, so it can return that one hotel's embed plus a `default_hotel`, and stop depending on the list. Note the current default is arbitrary: the Hotel query has no `order_by` and Hotel has no `Meta.ordering`.
- `socket_jwt` carries every slug. Either the socket server checks membership on subscribe and the JWT carries only `user_id`, or the socket connects after the hotel list arrives. The first is the better end state and the serializer's own TODO asks for it.

A smaller interim win if the split is too big for this ticket: the view queries CompanyHotelUser twice for the same user, then ships the resulting id list as three separate 6000-integer parameter lists (Hotel, HotelAssociationId, PortfolioHotel). Fetching the ids once and driving all three from a single subquery lets Postgres do the joins. And `hotel.pk in requester_hotel_ids` is a list scan per hotel, so quadratic, and always true in this view since both lists come from the same filter.

Happy to pair on the split if useful.