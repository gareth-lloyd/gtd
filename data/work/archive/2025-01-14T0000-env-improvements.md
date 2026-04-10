---
area: null
contexts: []
created: &id001 2025-01-14 00:00:00
defer_until: null
due: null
energy: null
id: 2025-01-14T0000-env-improvements
project: null
tags: []
time_minutes: null
title: env improvements
updated: *id001
waiting_on: null
waiting_since: null
---

https://canarytechnologies.slack.com/archives/C03P563GB4M/p1736778866223189

gsts installation through brew is no longer required:
brew remove gsts
canary cli is now updated automatically through nix. Please remove the older version: (cd ~ && which canary && rm $(which canary))
Rerun canary aws local-access-setup
Inside canary repo, canary version will always point to the latest
If you need to run canary cli outside of canary repo: nix run 'git+ssh://git@github.com/canary-technologies-corp/canary-cli' -- version
Refresh aws credentials should cache response better(with a new browser based on firefox)