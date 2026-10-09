---
area: null
completed_at: null
contexts: []
created: 2026-10-08 06:14:09.703203
defer_until: null
due: 2026-10-08
energy: low
id: 2026-10-08T0614-notes-for-andrea-s-presentation
order: null
output: ''
project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 5
title: Flesh out these notes for a presentation introducing onboarding scripts
updated: 2026-10-08 15:01:30.339155
waiting_on: null
waiting_since: null
working_on: true
---

Goal: an engaging, broad-technical-audience, talk to share the critical concepts of the onboarding script system.

# History:
* Grew out of a feature that reads salesforce and sets values on hotels as they get signed up
* Wyndham version: do the same thing in bulk, and add more intensive configuration
* Battled through the early days of Wyndham onboarding. Scripts became the place to store any and all learnings as we got things working
* Created a Django Admin and then a /manage UI for CS to use. 
* Lost a key person and when they left found out all the workarounds they were using to make the scripts work. They had deep Django Admin knowledge and were very independent. So they had a whole parallel set of procedures. That sparked off another round of trying to get things into scripts. 



# Why:
* Enterprise accounts have more complex lifecycles, but also more process to track them. Signed up, have training date, trained, have go-live date, going live, canceled MSA, left the brand.
  * CSMS need to be able to apply 
* Salesforce as source of truth
* Audit log. 
* Repeatable at scale
* Monitoring, error checking, UI attached
* rollout recipes
* One source of truth for what should happen: property_configuration_processes.py

# NOT JUST ONBOARDING:
* Rolling out new config with audit log
* Hotel lifecycle: offboarding, deactivating, changing brand, changing PMS

Yeah, we know, the name needs to change. One day when we have time to edit 1000 files.

# This system is fundamentally imperative
* A declarative model is a better way of expressing rules on configuration

Logical facts about the hotel:
* Coutnry, MSA, Brand, Parent brand --> config to apply
* Note this is NOT based on portfolio membership which is database state, and can get out of date.
* We have this! rules_based_configuration

* The system is currently operating in "drift detection" mode. Does this hotel diverge from the rules
* We have plans to make the system drive enterprise onboarding config changes, but it's hard to transition from the assumptions of an imperative system to purely declarative. There are 1000s of hours of learning baked in, and lots of special conditionals, loops, exceptions, error handling etc.
* And some parts of the config are INHERENTLY imperative because they are steps with dependencies:
  * Configure PMS via API calls to gateway
  * THEN, run a fetch and wait
  * THEN validate that the fetch succeeded and the hotel can be considered correctly set up
  * THEN run functions that depend on PMS access e.g. fetch rooms and images.

* We also are in the process of extending this PAST enterprise branded configs. Country -> GDPR retention rules


# Not just enterprise
* The system started for individual hotels, and individual hotels STILL use it
* Every prod hotel is activated by onboarding scripts.
* Teams should consider whether new features and broad config updates belong there. 


Sources (not all fully up to date)
* rollout recipes: https://app.notion.com/p/canarytechnologies/Rollout-Recipes-Reconfigure-Live-Hotels-at-Scale-3b98146861518122b22bc85fd86987b7?v=32081468615180f38ba9000c0362b5a5&source=copy_link

* Old rules-based design doc: https://app.notion.com/p/canarytechnologies/Rules-based-hotel-configuration-269814686151800f8812f8373d3f90e3?source=copy_link
* https://app.notion.com/p/canarytechnologies/How-Onboarding-Scripts-Should-Interface-with-Product-Pod-Domains-36181468615181f390fae19af8a097ad?v=32081468615180f38ba9000c0362b5a5&source=copy_link
* https://app.notion.com/p/canarytechnologies/Onboarding-Batch-System-Architecture-and-Key-Concepts-32081468615181f7b7e6c4ed459ad2a6?source=copy_link
Next steps for rules-based:https://app.notion.com/p/canarytechnologies/Binding-Rules-Tree-3e58146861518147b489e3fa8e8aef09?source=copy_link