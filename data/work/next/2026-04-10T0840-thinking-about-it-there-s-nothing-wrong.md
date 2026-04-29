---
area: null
contexts:
- thinking
created: 2026-04-10 08:40:18.614217
defer_until: null
due: null
energy: medium
id: 2026-04-10T0840-thinking-about-it-there-s-nothing-wrong
order: 3
project: 2026-04-16T1348-ideas
source_id: null
tags:
- focus
time_minutes: 15
title: Write up one-level-hierarchy idea
updated: 2026-04-29 11:50:00.566318
waiting_on: null
waiting_since: null
---

Enforced one-level hierarchies are fine — sometimes the constraint is the feature.

Example: Slack threads. You can never go more than one "level deep" — thread messages can't themselves have threads. That's limiting, but the limit makes total sense: it prevents infinite nesting, keeps conversations scannable, and forces people to branch into a new channel/DM when a sub-discussion really needs its own thread.

Worth writing up as a design principle: when a one-level hierarchy is enough, enforce it rather than leaving recursion open.