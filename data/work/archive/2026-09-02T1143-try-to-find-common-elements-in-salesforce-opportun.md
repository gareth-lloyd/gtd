---
area: null
completed_at: 2026-09-02 18:51:24.640610
contexts: []
created: 2026-09-02 11:43:25.611581
defer_until: null
due: 2026-09-02
energy: low
id: 2026-09-02T1143-try-to-find-common-elements-in-salesforce-opportun
order: null
output: |
  ## Agent run 2026-09-02T11:58+01:00

  Scope: Salesforce data exploration only. Read-only SOQL via local creds (glloyd@ user), plus reading of the Canary import code. No writes anywhere. Raw pulls saved in this session's scratchpad (ihg_core_all.json, ihg_ent_noparent.json, core_under_parent.json, opp_fields.json, acc_fields.json).

  ### Blocked step (resolved in the second run below)

  ### How IHG Core properties are identified in Salesforce (common elements)
  There are two overlapping IHG populations and the Core rollout is the newer one. The reliable signals, in order of usefulness:

  1. **Opportunity name suffix, surfaced by formula field `IHG_Package_Type__c`** = `IF(CONTAINS(Name,"Core Plus"),"Core Plus", IF(CONTAINS(Name,"IHG Core"),"Core","Unclassified"))`. Every Core opp is named `<Hotel name> - IHG Core`, every Core Plus opp `<Hotel name> - IHG Core Plus` (one outlier: `... - IHG Core Plus addon`). 46 Core + 28 Core Plus opps exist org-wide today. This is the cleanest discriminator, but it is name-driven, so a rename breaks it.
  2. **`Canary_Package__c` picklist** has explicit values `Guest Management System (GMS) - IHG Core` and `... - IHG Core Plus`. Set on 65 of the 74 Core/Core Plus opps. Standard, updateable, groupable. Canary does not import it.
  3. **`Active_Products__c` multipicklist** uses IHG-specific product tokens: `Contactless Check-In - IHG Core`, `AI Guest Messaging - IHG Core`, `Digital Compendium - IHG Core`, `Dynamic Upsells - IHG Core`, `Smart Check-Out - IHG Core`, `Mobile Keys - Wallet`, and the same with ` - IHG Core Plus` plus `Digital Authorizations - IHG Core Plus`, `Digital Tipping - IHG Core Plus`, `Payment Links`. Canary already imports this string (SalesforceOpportunity.active_products), so it is the only Core-vs-Core-Plus signal Canary holds today.
  4. **`Parent_Opportunity__c` = `006Qj000007kLa5IAE`** ("IHG - Guest Messaging / GMS", account Intercontinental Hotels Group). This is what Canary keys on (PARENT_OPPORTUNITY_ID_TO_ENTERPRISE_DEPLOYMENT -> IHG_GMS_CORE). 66 of the 74 Core/Core Plus opps are under it; the other 8 are sales-led (owner = AE, stage Demo Completed, created Aug 2026) and are not yet enterprise work.
  5. **`Enterprise_Deployment__c` checkbox**: true on 46/47 Core opps, but FALSE on all Core Plus opps (bar one test). Not a reliable IHG Core selector on its own.
  6. **Account-level**: `Account.Parent_Brand_ID__c = 001f200001qQmWhAAK` (IHG), `Account.Unique_Hotel_ID__c` = 5-letter IHG hotel code (e.g. SRTSC, OSBMO; 191/201 populated) which is the natural cross-system key, `Account.Associated_Enterprise_Deployments__c` multipicklist only has an old `IHG - GMS` value (no Core value), `Account.pms_2__c` = Oracle Opera (majority) or Hotelkey.

  Fields that are NOT useful: `Enterprise_Deployment_Segment__c` is None on every Core opp (it carries "US - Cohort 1/2", "Cohort 8W" etc only for the older pilot/messaging population); `Enterprise_Deployment_Detail__c` is None; `GMS_Package_Add_Ons__c` almost always None; `Canary_App_Onboarding_Status__c` is "Needs Definition" on 274/276.

  ### Go-live schedule fields
  Standard onboarding fields are being used, and populated by the implementation team (Core: Taylor Kirchwehm; Core Plus: Max Iattoni, Caeleigh Reger, Ellen Starnes):
  - `Training_Date__c` (16/47 Core opps set), `Target_Activation_Date__c` (7 set), `Onboarding_Status__c` (Training Scheduled / Trained - Confirming Activation Date / Awaiting Handoff), `Go_Live_Date__c` (0 set so far on Core - it is back-filled after go-live on the pilot population: 128 Live there all have it).
  - So for a Core state display the schedule signal is Training_Date__c -> Target_Activation_Date__c -> Go_Live_Date__c, gated by Onboarding_Status__c. Canary imports all four (training_date, target_activation_date, go_live_date, onboarding_status).

  Candidate early batches under the IHG parent (Core opps with a training date; `hotel code | account | training | target activation | status`):
  - Batch A (trained 2026-08-31, target 2026-09-07, all "Trained - Confirming Activation Date"): SRTSC Candlewood Suites St. Robert; OSBMO HIX Osage Beach; AIKXS HIX&S Aiken; DENMD HIX Denver Central-North (Hotelkey); CBASB Staybridge Carlsbad/San Diego; OCNHI Holiday Inn Carlsbad/San Diego.
  - Batch B (training 2026-09-02, "Training Scheduled"): CHIWP voco Chicago Downtown; BEDIN HIX&S Bedford; SGHIL HIX Spring Hill FL (Hotelkey); OKCAV avid Oklahoma City Quail Springs.
  - Batch C (training 2026-09-09..09-23, "Training Scheduled"): BTRZA HIX&S Baton Rouge North (09-09); GSOHI HI Greensboro Coliseum, SDFMT Staybridge Louisville East, WDCRG Kimpton Banneker (09-14); SYRAU HI Auburn-Finger Lakes (09-16, Hotelkey); MTOEF HI Effingham (09-23).
  - 29 further Core opps under the parent have no dates yet (stage Closing / Agreement Sent). Test/placeholder accounts are mixed in: "Stacy Test Account", "Stacy Test Account 1" (SX530), "IHG Pilot Hotel" (TEST), "Canary Placeholder", "Swati Hotels, LLC".
  Core Plus is layered as a second opp on the same account: all 21 Core Plus opps under the parent sit on accounts that also have a Core opp. Only 3 have any onboarding status (2 Awaiting Handoff, 1 with target activation 2026-10-23).

  ### Where the Canary import (salesforce_onboarding_fields.py) falls short for IHG
  - `derive_onboarding_type` maps parent `006Qj000007kLa5IAE` -> `OnboardingType.IHG_GMS_CORE` for every child, so Core Plus opps are also stored as IHG_GMS_CORE. There is no parent-opp mapping for `IHG_GMS_CORE_PLUS`, so a cohort with onboarding_type ihg_gms_core_plus will never match an opportunity via `get_latest_opportunity_for_cohort_hotel`, and the "latest opp" for a Core cohort may be the Core Plus sibling (it picks max created_at among same-onboarding_type opps on the account).
  - Core Plus opps have `Enterprise_Deployment__c = false`; they are only picked up by the non-enterprise branch of `get_all_syncable_opportunities` when stage is in (Closing, Closed Won, Conference-Signed, Trial). 7 Core Plus opps at "Agreement Sent" are therefore not synced at all.
  - Neither `Canary_Package__c` nor `IHG_Package_Type__c` is imported; the only Core/Core Plus discriminator in Canary is the `active_products` string.
  - 334 older IHG opps have `Enterprise_Deployment__c = true` but NO parent opportunity (segments "US - Cohort 2" x134, "Cohort 8W" x62, "Cohort 6", "Cohort 7W", ...; 321 at stage Qualified; owner Bryan Michalis). They sync as SalesforceOpportunity rows with onboarding_type None, i.e. invisible to any IHG cohort. Most look like the messaging pilot population rather than Core, but worth confirming with the onboarding team.
  - IHG_DEPLOYMENT_PILOT / Portfolio IHG_PILOT is report-only (Slack drift), and `update_cohort_hotels` (the Wyndham per-deployment path) only supports US and EU regions.

  ### Suggested definition for the shared source of truth (data only, no UI)
  "IHG Core property" = Opportunity where `Parent_Opportunity__c = 006Qj000007kLa5IAE` AND `IHG_Package_Type__c IN ('Core','Core Plus')` (equivalently `Canary_Package__c LIKE '%IHG Core%'`), excluding known test accounts; keyed by `Account.Unique_Hotel_ID__c`; schedule from `Onboarding_Status__c`, `Training_Date__c`, `Target_Activation_Date__c`, `Go_Live_Date__c`; Core vs Core Plus from `IHG_Package_Type__c`. If the team wants Canary to be the display source, the import needs the package field and a Core Plus onboarding-type mapping.

  ## Agent run 2026-09-02T12:07+01:00 (cohort cross-check, Snowflake)

  Unblocked: the canary-snowflake MCP server process was wedged, not the SSO token. Calling the server module directly (`~/.claude/mcp/canary-snowflake/.venv/bin/python`, `server._run_query`) works in ~3s with the cached token. Canary prod is mirrored at `CANARY_RAW.CANARY` (ONBOARDING_COHORT, ONBOARDING_COHORTHOTEL, ONBOARDING_SALESFORCEOPPORTUNITY; SalesforceHotelAccount is NOT mirrored, so account ids resolve only via opportunity rows). Mirror was fresh to 2026-09-02 08:31 UTC.

  ### The three cohorts
  All three: onboarding_type ihg_gms_core, state in_progress, go_live_date empty, created by staff user id 3649236, 7 CohortHotel rows total, none yet linked to a Hotel.
  - b2a39169 "IHG GMS Core_2026-08-31" (id 46201, created 08-31 19:41): OCNHI Holiday Inn Carlsbad/San Diego.
  - d3ed663c "IHG GMS Core - SRTSC_2026-08-31" (id 46267, 08-31 20:19): SRTSC Candlewood Suites St. Robert.
  - 4af5ba2b "IHG Core GMS_2026-08-31" (id 46333, 09-01 13:39): DENMD HIX Denver Central-North, OSBMO HIX Osage Beach, AIKXS HIX&S Aiken, CBASB Staybridge Carlsbad/San Diego, plus SalesforceHotelAccount id 42439 which has NO SalesforceOpportunity rows in Canary at all (unresolvable from Snowflake; on a prod shell: `SalesforceHotelAccount.objects.get(id=42439).salesforce_account_id`). Likely an account whose only IHG opp is not syncable (Demo Completed / Agreement Sent with the enterprise checkbox off).

  So the cohorts are exactly "Batch A" from the first run: the six Core opps trained 2026-08-31 with Target_Activation_Date__c 2026-09-07 and Onboarding_Status__c "Trained - Confirming Activation Date". The Salesforce selector reproduces the cohort membership; the cohort label/date is a manual echo of Training_Date__c.

  ### Correction to the Core vs Core Plus reading
  Looking at the six accounts side by side with Canary's imported rows:
  - Every account has TWO opps under the IHG parent: `<Hotel> - IHG Core` (owner impl lead Taylor Kirchwehm, Enterprise_Deployment__c = true, carries the GMS bundle: Mobile Keys - Wallet, AI Guest Messaging, Contactless Check-In, Digital Compendium, Dynamic Upsells, Smart Check-Out) and `<Hotel> - IHG Core Plus` (impl leads Max Iattoni / Caeleigh Reger / Ellen Starnes, Enterprise_Deployment__c = false, carries only Digital Authorizations + Digital Tipping, occasionally Payment Links / AI Voice).
  - So the "Core Plus" opp is the tipping+auths add-on line, not a replacement package. A hotel's tier is: Core Plus if the account has a "- IHG Core Plus" sibling opp (18 of 41 real Core accounts under the parent today), else Core. `IHG_Package_Type__c` on the base opp always says "Core", so it identifies the base line but not the tier. The product tokens on the base opp are also relabelled "... - IHG Core Plus" for Core Plus hotels (18 base opps), which is the only tier signal Canary currently stores.
  - Schedule lives on the base "- IHG Core" opp only (training date, target activation, status). The add-on opp has its own status (Awaiting Handoff) and its own target date (OCNHI: 2026-10-23), i.e. tipping/auths go live later than GMS.

  ### Sync gaps confirmed against the mirror
  - OSBMO's add-on opp 006Nu00000lyhIPIAY (Core Plus, Agreement Sent, enterprise flag off) is absent from Canary; the other five add-on opps (stage Closing) did sync. Matches the code reading: non-enterprise opps sync only in Closing/Closed Won/Conference-Signed/Trial.
  - All synced add-on opps are stored as onboarding_type ihg_gms_core (same parent), so `get_latest_opportunity_for_cohort_hotel` will return the add-on opp for these cohorts (it is the most recently created on the account), which has no training date and a different status. Worth checking what the cohort page shows for OCNHI/CBASB.
  - Legacy rows on the same accounts (Closed Won messaging/tipping opps from 2019-2025, and "US - Cohort 2" pilot rows at stage Qualified) have onboarding_type None and are inert.
project: 2026-08-31-ihg
source_id: null
tags: []
time_minutes: 5
title: Try to find common elements in Salesforce opportunities that identify IHG Core
  GMS properties and go-live schedule
updated: 2026-09-02 18:51:24.640603
waiting_on: null
waiting_since: null
working_on: false
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