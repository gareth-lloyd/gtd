---
area: null
contexts:
- react
created: 2026-05-13 11:28:24.422613
defer_until: null
due: null
energy: medium
id: 2026-05-13T1128-respond-on-ent-6165-property-still-not-showing-on
order: null
output: '## Agent run 2026-05-13T13:05:00Z


  **Investigation summary:**


  - Hotel 13749 (Hampton Inn Carson City) IS in portfolio 2080 (Intermountain Management)
  — PortfolioHotel #115631 exists.

  - The AP dashboard "Hotel Name" dropdown is populated by Explo reading from Snowflake
  (CDC sync), NOT from Canary''s DB directly.

  - Connor''s fix for ENT-6154 (Guldsmeden portfolio) was confirmed working on May
  12 10:14.

  - Rachel reported at 19:14 same day that Intermountain Management portfolio STILL
  doesn''t show the hotel.

  - Root cause is likely Explo-side: either Connor''s fix was portfolio-specific (Guldsmeden
  only), or the Snowflake/CDC sync for this portfolio hasn''t caught up, or the Explo
  dashboard queries need manual update for Intermountain Management.


  **Draft Linear comment (needs approval before posting):**


  > @connor Rachel is reporting this is still broken for the Intermountain Management
  portfolio (uuid `adadcfb5-8945-4291-bdcb-b4e269d38ee8`). The PortfolioHotel record
  exists, so this is Explo/Snowflake-side. Could the fix from ENT-6154 have been specific
  to the Guldsmeden portfolio? Can you check whether the Explo queries for Intermountain
  Management need the same treatment?


  **Status:** needs your approval to post the above comment, or you can handle directly.

  '
project: null
source_id: https://linear.app/canary-technologies/issue/ENT-6165/add-property-to-above-property-dashboard
tags:
- morning-gtd
- linear
time_minutes: 20
title: 'Respond on ENT-6165: property still not showing on portfolio'
updated: 2026-05-13 14:11:13.747955
waiting_on: null
waiting_since: null
working_on: false
---

rsmoller flagged: property is still not visible on portfolio (Deployed state, but reported missing). https://linear.app/canary-technologies/issue/ENT-6165/add-property-to-above-property-dashboard