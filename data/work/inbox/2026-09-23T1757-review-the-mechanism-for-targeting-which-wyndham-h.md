---
area: null
completed_at: null
contexts: []
created: &id001 2026-09-23 17:57:54.554029
defer_until: null
due: null
energy: null
id: 2026-09-23T1757-review-the-mechanism-for-targeting-which-wyndham-h
order: null
output: ''
project: null
source_id: null
tags: []
time_minutes: null
title: Review the mechanism for targeting which Wyndham hotels get the in-stay / mobile
  check-in flows
updated: *id001
waiting_on: null
waiting_since: null
working_on: false
---

From #epd-mobile thread "All good with Wyndham :)" (Sept 21-23), cc'd by Caitlyn Levine.
https://canarytechnologies.slack.com/archives/C09M5GRJPL2/p1790171519216139?thread_ts=1790006579.628339&cid=C09M5GRJPL2

Proposed mechanism (Eric): once PR 56743 (AD-8391) merges, guest payload sends has_check_in_mobile = config flag AND hotel.has_check_in. Wyndham app checks hasCheckInMobile != false, so unset = button shown by default. Wyndham then controls rollout per property by setting has_mobile_check_in true only where they want it live.

Things to sanity-check:
- Default-on semantics (unset -> visible) for a slow rollout
- Caveat: with product off, check_in is still null on guest reservations, already-checked-in guests lose state
- Who owns the per-property config: Wyndham side vs Canary side
- PR 56743 open, approved, not merged; only non-blocking E2E failures