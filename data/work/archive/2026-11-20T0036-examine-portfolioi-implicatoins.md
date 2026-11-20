---
area: null
completed_at: 2026-11-20 14:15:22.158423
contexts: []
created: 2026-11-20 00:36:09.666742
defer_until: null
due: null
energy: low
id: 2026-11-20T0036-examine-portfolioi-implicatoins
order: null
output: |
  ## Agent run 2026-11-20T13:10

  Thread: https://canarytechnologies.slack.com/archives/C0C4KBFL9KR/p1795125404930359 (#project-operator, Dylan's multi-property MCP access for Noble House). Read-only research; nothing was posted or changed.

  ### How "portfolio" access works in the MCP today

  - The Noble House tenant is one Snowflake role, `MCP_TENANT_NOBLE_HOUSE_ROLE`, paired with 16 hard-coded hotel ids in terragrunt (`snowflake/production/us-west-2/mcp/control/terragrunt.hcl`, canary-terragrunt PR #1663, https://github.com/canary-technologies-corp/canary-terragrunt/pull/1663). A comment says the rows "mirror Canary portfolio 5809". Nothing enforces that.
  - Users reach a tenant through a hard-coded user-id map, `TENANTS_BY_USER_ID` in `backend/canary/public_mcp/tenants.py` (canary PR #65997, https://github.com/canary-technologies-corp/canary/pull/65997), plus an `MCPAccessGrant` row.
  - So the Canary Portfolio model plays no part at runtime. Neither `PortfolioHotel` nor `PortfolioManagedUser` nor the user's hotel memberships is consulted.

  ### What I checked against live data (Snowflake ANALYTICS_PUBLIC, 2026-11-20)

  - The registry and portfolio 5809 agree today: 16 of 16 hotels, no extras either way.
  - Portfolio 5809 has zero portfolio users in `DIM_PORTFOLIO_USER`. Steven's access comes from being a hotel user at 18 properties, not from the portfolio.
  - 7 of the 16 hotels are also in "Pebblebrook Hotel Trust" (portfolio 4588, 44 hotels), and in four personal sub-portfolios under it (David Danieli's, David Craig's, Jeff Randall's, Kari Carr's). Hotel ids: 2642, 2681, 4289, 129283520, 129283586, 129283588, 129283590.
  - La Mer (129255701) is in no portfolio at all.

  ### Implications

  1. Drift is silent, and the risky direction is removal. If a hotel leaves Noble House (sold, management contract ends), `PortfolioService.remove_hotel` updates Canary, but the Noble House role keeps reading that hotel's guest messages, payments and reservations until someone edits terragrunt. A hotel added to the portfolio just reads empty, which is safe. Dylan already named the parity problem; the asymmetry is the part worth saying out loud.

  2. A hotel belongs to several portfolios, so "the hotel's portfolio" is not one thing. The 7 Pebblebrook hotels are the live example: operator (Noble House) and owner (Pebblebrook) both group them. The registry handles this mechanically (a hotel can pair with several roles), but each pairing hands a different company the full warehouse view of the hotel. Who consents, the hotel, the operator or the owner, is undecided. This is the same question Dylan asked at the end of the thread, one level up.

  3. Portfolios are not an authorization boundary in Canary, so "just sync the registry from PortfolioHotel" is not a safe fix on its own. Portfolio types include ad hoc and personal groupings ("Jeff Randall's Portfolio"), and some types are customer-creatable (`hotels/models/portfolio_type_rules.py`). If membership drove warehouse access, adding a hotel to a portfolio would become a data grant. Any sync would need to be limited to specific portfolio types and probably an explicit opt-in per portfolio. I did not check which types 5809 holds.

  4. Access is per tenant, not per user. Everyone mapped to the Noble House role sees all 16 hotels, whatever their Canary hotel memberships or role permissions are. Fine for Steven, a corporate user. It breaks for the next Noble House user who is, say, a GM at one property, or whose Canary role hides payments or messages. It also means offboarding is manual: removing Steven's hotel access in Canary does not touch his MCP access; only deleting the `MCPAccessGrant` or the map entry does. (I did not verify whether deactivating the user blocks the OAuth path.)

  5. The reverse gap is visible to the customer. Steven has 18 hotels in Canary and 16 in the MCP; Corazon Cabo and the parent record read as empty, with no error. Expect "why is hotel X missing" questions.

  6. `dim_portfolio` is exposed unfiltered except by hotel (`transform/models/mcp_public/mcp_dim_portfolio.sql` in canary-dagster is `select *`). The Noble House tenant can therefore read every portfolio its hotels belong to, including "Pebblebrook Hotel Trust" and the four named individuals' portfolios. Low severity, since they likely know their owner, but it is another customer's structure and people's names, and at brand scale it would show which management companies and owners sit behind each hotel. Small fix: filter that view to the tenant's own portfolio, or drop the name columns.

  7. Region. The registry, the user-id map and portfolio ids are all per region (us-west-2 only). A portfolio spanning regions has different ids per region, linked only by `portfolio_identifier`. Portfolio 5809 has an identifier ("Noble House Portfolio"); Pebblebrook has none. Not a problem for this pilot.

  ### My read

  For a two-customer pilot this is fine as built, and Dylan's call not to invest in scaling yet is reasonable. The one thing I would act on now is item 6 (cheap). Items 1 to 4 are what should be on the table before a third portfolio tenant, and in particular before any brand or ownership-group tenant, where items 2 and 3 stop being theoretical. If this graduates, the natural shape is user-scoped access derived from the hotels a user can already see in Canary, rather than a tenant-per-portfolio role, with the portfolio only used as a convenience filter.

  ### Possible follow-ups (not done, your call)

  - Reply in the thread with items 1, 2 and 6. Nothing drafted or sent.
  - A ticket for the `dim_portfolio` exposure (item 6).
project: null
source_id: null
tags: []
time_minutes: 5
title: examine portfolioi implicatoins
updated: 2026-11-20 14:15:22.158413
waiting_on: null
waiting_since: null
working_on: false
---

https://canarytechnologies.slack.com/archives/C0C4KBFL9KR/p1795125404930359