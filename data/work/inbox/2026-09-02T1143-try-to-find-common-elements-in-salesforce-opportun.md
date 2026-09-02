---
area: null
completed_at: null
contexts: []
created: 2026-09-02 11:43:25.611581
defer_until: null
due: null
energy: low
id: 2026-09-02T1143-try-to-find-common-elements-in-salesforce-opportun
order: null
output: ''
project: null
source_id: null
tags: []
time_minutes: 5
title: Try to find common elements in Salesforce opportunities that identify IHG Core
  GMS properties and go-live schedule
updated: 2026-09-02 11:43:29.994255
waiting_on: null
waiting_since: null
working_on: true
---

ULtimate task: build a shared source of truth including for peopel with no access to salesforce. Some kind of state display that can be shared and agreed upon. 

First part: identify the salesforce data. 

Precedent: Wyndham data is imported into CohortHotels, SalesforceHotelAccounts etc by onboarding/services/salesforce_onboarding_fields.py

that shoudl give guidance on how we think about opportunity fields. 

there's IHG import work in there, but might not be doing its full job. 

Do not progress to designing the eventual state display UI. LImit to Salesforce data exploration. 

Hopefully the standard fields on opportunity are used. 

Starting point: These cohorts on prod:
https://www.canarytechnologies.com/manage/onboarding/cohorts/b2a39169-c201-4379-8167-03c4ec3fe5cf
https://www.canarytechnologies.com/manage/onboarding/cohorts/d3ed663c-026c-4ffd-ba16-725a97a8ec3a
https://www.canarytechnologies.com/manage/onboarding/cohorts/4af5ba2b-516d-48a3-a9ce-bb4bf43d3afd

These are recent early batches. Identify hotels. Find the corresponding SF accounts/opportunities. Inspect

You can use /debug_in_shell process

salesforce credentials are up to date locally to run API calls.