---
area: null
contexts: []
created: &id001 2025-03-31 00:00:00
defer_until: null
due: null
energy: null
id: 2025-03-31T0000-ticket-allow-plans-providers-to-define-m
project: null
tags: []
time_minutes: null
title: 'Ticket: allow plans/providers to define must-have, should-have config. Provides
  the basis of a check for hotels ready to go-live.'
updated: *id001
waiting_on: null
waiting_since: null
---

Extend the idea of config providers providing actual config. 
I.e. Wyndham enable msa provider would constuct a config, then the plan would use that to apply values. 
Refactor enable msa step to be more like strategy pattern.
then could have a check step to verify everything is applied. 

OR:
"Hotel is configured" method, which could be run on all hotels