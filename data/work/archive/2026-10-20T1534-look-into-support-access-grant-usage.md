---
area: null
completed_at: 2026-10-21 10:03:29.401726
contexts: []
created: 2026-10-20 15:34:43.688995
defer_until: null
due: null
energy: low
id: 2026-10-20T1534-look-into-support-access-grant-usage
order: null
output: |
  ## Agent run 2026-10-21T09:56:51

  Source: Snowflake CDC mirror CANARY_RAW.CANARY.INTERNAL_SUPPORT_SUPPORTACCESSGRANT (us region), joined to AUTH_USER and HOTELS_HOTEL. Mirror last extracted 2026-10-20 22:01 UTC, so the last ~9h of 2026-10-21 are not included. Window = created_at >= now - 30d (2026-09-21 to 2026-10-20). Feature went live 2026-06-24; 597 grants all-time.

  ### How many
  - 89 grants in 30 days, by 18 requesters, across 83 distinct hotels.
  - Per week: w/c 09-21: 10, 09-28: 14, 10-05: 36, 10-12: 21, 10-19 (partial): 8.
  - Status now: revoked 59, expired 25, active 4, pending 1. Denied: 0 (nobody has ever been denied in the window).
  - 85/89 were approved. 4 never got a decision: 3 timed out as expired (cgrijalva x2 CUSTOPS-5521/CUSTOPS-5518, edemichiel ONC-27454), 1 still pending (cgrijalva CUSTOPS-6143 at 21:53 UTC on 10-20).
  - Approval latency: median 3 min, mean 49 min, max 825 min (13.75h).
  - 58/59 "revoked" rows have no revoked_by. That is the Linear auto-close path (SupportAccessGrantService._auto_close_one sets REVOKED without revoked_by when the ticket closes), not a human revoke. Only 1 manual revoke (mziaei). Nobody revokes their own grant; access ends when the ticket is closed or the 24h TTL lapses. Median time active before auto-close is 13 min; p90 5.5h; max 22h.
  - Every grant had a ticket URL. Linear team prefix: CUSTOPS 73, ONC 8, TOOL 3, INT 3, STAFF 2.

  ### Who (requesters)
  | requester | grants | hotels | note |
  |---|---|---|---|
  | spineda | 19 | 19 | 7 under CUSTOPS-5940 (auths/pay/contract config for Proper hotels), 5 under CUSTOPS-5728 (Booking/Expedia integration) |
  | cgrijalva | 14 | 14 | almost all "SMS troubleshooting"; owns 2 of the 3 expired-undecided and the 1 pending |
  | dreplan | 11 | 11 | all user-access requests (4 under CUSTOPS-5561) |
  | agantan | 6 | 5 | role updates |
  | zmoeller | 5 | 4 | onboarding/demo access |
  | edemichiel | 5 | 5 | ONC tickets: role upgrades, modifier sets |
  | ilopez | 4 | 4 | |
  | apardo | 4 | 4 | INT tickets, implementation support |
  | creger, mziaei, jsalvacion | 3 each | | mziaei holds 3 of the 4 currently active (TOOL-889 ECHO survey pilot) |
  | aasuncion, akleczek, dquijada, rfaricy, mhu | 2 each | | |
  | dvalencia, asosa | 1 each | | |

  Approvers (decided_by): dvalencia 31, mziaei 16, agantan 10, rfaricy 6, sbarry 6, aghazarossian 4, kaustin 4, ldewald 4, cgrijalva 3, dmourad 1. No self-approvals.

  ### Reasons
  | reason | n |
  |---|---|
  | other | 32 |
  | configuration_change | 20 |
  | troubleshooting | 14 |
  | no_property_manager ("User Management") | 12 |
  | new_product_onboarding | 11 |
  | check_in_configuration | 0 |

  "other" is the largest bucket and is mostly mislabeled: of 32, ~16 are user add/remove/role changes (dreplan "Create User Access", "Existing User Access request", agantan "Update role", jsalvacion "Add CSM as Property Manager", dquijada "Remove users") that belong under no_property_manager, 5 are spineda's Booking/Expedia integration (configuration_change), and the rest are translations, branding, training, walkthroughs. Real "User Management" share is therefore ~28/89, not 12. The reason label "User Management" for no_property_manager may not read as "add/remove a user" to requesters.

  ### Types
  - grant_type: default 89, check_in_configuration 0. The CHECK_IN_CONFIGURATION type (grants PROPERTY_MANAGER + CANARY_SUPPORT roles) has never been used in the window; nobody picks the check_in_configuration reason.
  - Both types are auto_approve=False, so every grant goes through Slack approval.

  ### Observations worth a follow-up
  - Same-ticket fan-out: 11 tickets produced 2-7 grants each (one per hotel). CUSTOPS-5940 = 7 grants, CUSTOPS-5728 = 5, CUSTOPS-5907 = 5, CUSTOPS-5561 = 4. A multi-hotel request shape would cut ~25 of 89 requests.
  - One requester re-requested because they "accidentally marked the ticket as Done" (agantan CUSTOPS-5660), confirming the auto-close-on-ticket-close coupling bites in practice.
  - Approval is effectively rubber-stamp: 0 denials, median 3 min, three approvers handle 67% of decisions (dvalencia, mziaei, agantan).
  - Query script: /private/tmp/claude-501/-Users-garethlloyd-projects-canary/71bb939e-0090-417d-b7ed-1de996d46299/scratchpad/sag.py (reruns all aggregates via the canary-snowflake server module).
project: null
source_id: null
tags: []
time_minutes: 5
title: look into support access grant usage
updated: 2026-10-21 10:03:29.401713
waiting_on: null
waiting_since: null
working_on: false
---

window: 30 days
how many, who, reasons, types