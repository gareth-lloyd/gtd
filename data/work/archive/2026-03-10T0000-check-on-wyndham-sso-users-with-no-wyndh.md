---
area: null
contexts: []
created: &id001 2026-03-10 00:00:00
defer_until: null
due: null
energy: null
id: 2026-03-10T0000-check-on-wyndham-sso-users-with-no-wyndh
project: null
tags: []
time_minutes: null
title: check on wyndham sso users with no wyndham htels. Scope for Lauta?
updated: *id001
waiting_on: null
waiting_since: null
---

us = UserProfile.objects.filter(sso_organization=49).exclude(user__companyhoteluser__hotel__sso_organization=49).exclude(user__companyhoteluser=None)