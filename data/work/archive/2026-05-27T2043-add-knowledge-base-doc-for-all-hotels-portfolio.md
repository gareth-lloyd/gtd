---
area: null
contexts: []
created: 2026-05-27 20:43:06.573228
defer_until: null
due: null
energy: low
id: 2026-05-27T2043-add-knowledge-base-doc-for-all-hotels-portfolio
order: null
output: |
  ## Agent run 2026-05-28T12:05
  Context (Slack thread C047K6WSUJY, 2026-05-27): Patrick Canny asked for a role/portfolio
  granting kiosk implementation specialists (Albert, Danny) Property Manager at ALL hotels.
  Gareth: hard no — an "all hotels" portfolio is a security problem; previously proposed and
  rejected; internal tools team is improving the temp-access flow instead. Referenced existing
  doc "Read-only and read-write Impersonation by Canary staff".

  Verified mechanism: portfolio-wide property role grants propagate the role to every hotel in
  the portfolio (CompanyHotelUser rows), so an "all hotels" portfolio = standing Property
  Manager at every live hotel. (portfolios/services/portfolio_user_management.py;
  portfolio_user_portfolio_wide_roles.py)

  Drafted a Core knowledge base doc "Why we don't create an 'all hotels' portfolio for staff
  access" (Category: Permissions, Authorization; Tags: portfolio, permissions, staff, roles,
  kiosk) covering: the recurring request, why it's a bad idea (grant propagation, defeats
  post-go-live read-only model / Dec-2023 incident, PM is high-privilege, standing grants, blast
  radius), what to do instead (impersonation + Support Access Period), and history.

  User approved creation. Created in Core knowledge base DB (collection 32081468-6151-80b2-869f-000b770dd39f).
  Page URL: https://www.notion.so/36e81468615181919e6bf955b7ee0ce3
project: null
source_id: null
tags: []
time_minutes: 5
title: add Core Knowledge base doc in Notion for all hotels portfolio. basically about
  why it's a bad idea
updated: 2026-05-28 12:06:00.000000
waiting_on: null
waiting_since: null
working_on: false
---

https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1779903203234839