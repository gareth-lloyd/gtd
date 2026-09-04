---
area: null
completed_at: 2026-09-03 14:11:14.729598
contexts:
- react
created: 2026-09-03 11:20:28.663158
defer_until: null
due: null
energy: low
id: 2026-09-03T1120-answer-andrea-on-basic-brand-vs-enterprise-validat
order: null
output: |
  ## Agent run 2026-09-03T14:13 — investigated; draft reply ready, NOT sent

  **Andrea's ask:** "very basic brand v enterprise validation? ie a marriott hotel should never be ihg"
  https://canarytechnologies.slack.com/archives/C0B1Y5K9AMC/p1788373457946269

  ### Where the contradiction comes from

  Not our backend. It is a **hotel-code namespace collision in Salesforce**.

  `Account.Unique_Hotel_ID__c` is a single shared column holding whichever brand property code
  applies. It is not unique across brands and structurally cannot be: IHG Inn Codes and Marriott
  MARSHA codes use the same shape (3-letter IATA city code + 2-char property suffix).

  The two accounts behind the #ihg thread:

  | SF Account | Unique_Hotel_ID__c | Marsha | Parent Brand | Created |
  | --- | --- | --- | --- | --- |
  | [Courtyard by Marriott Thomasville Downtown](https://canarytechnologies.lightning.force.com/lightning/r/Account/001Du000004liSlIAI/view) `001Du000004liSlIAI` | TLHCT | TLHCT | Marriott | 2023-10-11 |
  | [Hotel Indigo Tallahassee - Collegetown, an IHG Hotel](https://canarytechnologies.lightning.force.com/lightning/r/Account/001Qj0000080TUGIA2/view) `001Qj0000080TUGIA2` | TLHCT | — | IHG | 2024-02-01 |

  Chain of events: Jeremy McCauley (Park Place Hosp Group) signed up via Marketo passing
  `IHG_Inn_Code__c: TLHCT` + Company "Hotel Indigo Tallahassee Collegetown"
  (Rick's field dump: https://canarytechnologies.slack.com/archives/C0BJPFZKQ9W/p1788364978811499).
  The lead→account match ran on `Unique_Hotel_ID__c` with **no brand qualifier**, hit the older
  Marriott record, and the onboarding lead assignment fired as
  "Courtyard by Marriott Thomasville Downtown - IHG Core".

  Already remediated by hand — both IHG opps now sit on the Indigo account
  (`006Nu00000mIn0DIAS` IHG Core, `006Nu00000mKqIBIA0` IHG Core Plus). Stacy: "we are going to
  tighten up the flow so it only pulls IHG"
  (https://canarytechnologies.slack.com/archives/C0BJPFZKQ9W/p1788377047288559).
  Rick separately fixed a Marketo "do not sync" that suppressed the Core Plus package fields.

  Threads:
  - #ihg — https://canarytechnologies.slack.com/archives/C03V5P4B48P/p1788373232118349
  - #ihg-q3-deployment — https://canarytechnologies.slack.com/archives/C0BJPFZKQ9W/p1788359955817149

  ### This is systemic, not a one-off

  Snowflake, `analytics.analytics_public.sfdc_account`, `type='Hotel'` with a non-empty
  `Unique_Hotel_ID__c` — 42,410 distinct codes:

  - **2,327** codes sit on more than one account
  - **2,130** codes span more than one **parent brand** (~5% of the namespace)
  - **974** of those involve IHG: 414 Hilton|IHG, **361 IHG|Marriott**, 176 three-way
    Hilton|IHG|Marriott, 20 IHG|unset, 3 Hilton|IHG|unset

  Other live IHG↔Marriott collisions: ABQTW (Staybridge Albuquerque Airport / TownePlace
  Albuquerque Old Town), ATLAP (Holiday Inn Atlanta Airport North / Atlanta Airport Marriott),
  AMSAA (Holiday Inn Arena Towers / Courtyard Amsterdam Arena Atlas), AGSDT, ALBCO, ATLBH…

  So Taylor is right that this is not a cleanup job — a bare code match is genuinely ambiguous
  about 1 time in 20.


  ### Collisions resolvable by adding a `Parent_Brand__c` filter (from SF data)

  Source: Snowflake `analytics.analytics_public.sfdc_account`, `type='Hotel'`, non-empty
  `Unique_Hotel_ID__c` — 42,410 distinct codes across 44,931 accounts.
  (`parent_brand_shorthand__c` holds the literal string `'None'` for unset, not NULL — treated as unset.)

  **Per target brand — would `code + Parent_Brand = X` return exactly one account?**

  | Target brand | Distinct codes | Codes that collide | Resolved by brand filter | Still ambiguous | % resolved |
  | --- | ---: | ---: | ---: | ---: | ---: |
  | Hilton | 6,129 | 1,433 | 1,415 | 18 | 98.7% |
  | Marriott | 10,645 | 1,379 | 1,344 | 35 | 97.5% |
  | **IHG** | **7,047** | **1,053** | **966** | **87** | **91.7%** |
  | Wyndham | 8,079 | 336 | 318 | 18 | 94.6% |
  | Best Western | 4,046 | 354 | 321 | 33 | 90.7% |
  | Hyatt | 38 | 3 | 3 | 0 | 100% |
  | (brand unset) | 1,645 | 63 | 59 | 4 | 93.7% |
  | Choice | 7,087 | 15 | 1 | 14 | 6.7% |

  Choice is the outlier because its codes (`NC505`, `GA694`) collide *within* Choice, not across brands.

  **Which brand pairs the filter separates** — 2,059 codes / 4,291 accounts where each brand has
  exactly one account, so the filter fully disambiguates:

  | Colliding brands | Codes | Accounts |
  | --- | ---: | ---: |
  | Hilton + Marriott | 796 | 1,592 |
  | Hilton + IHG | 411 | 822 |
  | **IHG + Marriott** | **359** | **718** |
  | Best Western + Wyndham | 317 | 634 |
  | Hilton + IHG + Marriott | 173 | 519 |
  | Hyatt + Marriott | 2 | 4 |
  | Choice + Hyatt | 1 | 2 |

  **Whole namespace, by whether a brand filter helps:**

  | Category | Codes | Accounts |
  | --- | ---: | ---: |
  | No collision | 40,083 | 40,083 |
  | **Cross-brand, 1 account per brand — filter FULLY resolves** | **2,059** | **4,291** |
  | Cross-brand, >1 account inside a brand — partially resolves | 12 | 39 |
  | Cross-brand, an unset-brand account also shares the code | 3 | 9 |
  | Collides only with unset-brand account(s) | 60 | 120 |
  | **Same-brand duplicate — filter does NOT help** | **193** | **389** |

  **The split that matters for Stacy's cleanup ask.** Of IHG's 1,053 colliding codes:
  - **966 are a code change** — add the brand predicate, zero data work.
  - **87 are genuine duplicate account records** — the same hotel entered twice. Examples:
    `AKLCN` voco Auckland City Centre ×2 (`001Qj00000Ty4emIAB`, `001Qj00000g9MXyIAM`);
    `AUHBY` Yas Plaza Bay ×2; `AUHYI` Crowne Plaza Abu Dhabi Yas Island ×2;
    `BERPB` Garner Hotel Berlin Ku'Damm ×2; `AUSAP` Candlewood Suites Austin Airport ×2;
    `AXEIN` real Hotel Indigo Old Town Alexandria vs an "IHG Demo Account" (`001Qj00000tDyoIIAS`).

    **87 codes is the right scope to hand the marketing database team — not the 2,000+.**

  **Worked examples (all real, all currently live):**

  | Code | IHG account | Colliding account(s) |
  | --- | --- | --- |
  | TLHCT | Hotel Indigo Tallahassee - Collegetown | Courtyard by Marriott Thomasville Downtown *(the reported one)* |
  | ABQTW | Staybridge Suites Albuquerque Airport | TownePlace Suites Albuquerque Old Town |
  | ATLAP | Holiday Inn & Suites Atlanta Airport North | Atlanta Airport Marriott + Homewood Suites Alpharetta |
  | AMSAA | Holiday Inn Arena Towers | Courtyard Amsterdam Arena Atlas |
  | ALBCO | voco James Newbury Hudson Valley | SpringHill Suites Albany Latham-Colonie |
  | AGSDT | Holiday Inn Express Augusta Downtown | Tribute Portfolio Augusta + DoubleTree Augusta |

  ### Answer to Andrea: yes, and it's cheap

  Taylor's instinct (`Parent Brand = IHG`) is the right predicate and the data backs it: among the
  **44,931** hotel accounts that carry a `Unique_Hotel_ID__c`, **99.4% have `Parent_Brand__c`
  populated** (270 nulls). Fill rate across *all* 711,995 hotel accounts is only 19%, but that's
  dominated by uncoded prospect records you'd never match against.

  Better still — brand-specific columns already exist on Account (`Marriott_Marsha_Code__c`,
  `Radisson_Property_Code__c`, `LHW_Hotel_ID__c`). **There is no IHG-specific column.** That is the
  actual gap. An `IHG_Inn_Code__c` on Account, mirroring the field Marketo already passes, makes
  the match unambiguous with no brand predicate needed.

  Canary's backend already models this correctly — `HotelAssociationId` namespaces by `id_type`,
  so `ihg_inn_code` and `marriott_marsha_code` are separate rows, unique per (hotel, id_type):
  `backend/canary/hotels/models/hotel_association_id.py:61-68`. The collision is a Salesforce
  data-model problem, not a Canary one.

  ### If we make it a standing check, ~190 accounts fail today

  `Associated_Enterprise_Deployments__c` label vs `Parent_Brand__c`:

  - `IHG - GMS`: 119 accounts, **all 119 IHG — clean**
  - `Best Western - GMS`: 3,906 BW + **95 non-BW** (25 Choice, 9 Marriott, 7 IHG, 6 Hilton,
    2 Hyatt, 1 Red Roof, 45 unset)
  - Wyndham Connect labels (all variants): ~5,700 Wyndham + **~97 non-Wyndham** (40 Choice,
    8 IHG, 5 BW, 5 Hilton, 3 Marriott, 1 Radisson, ~35 unset)

  Those BW/Wyndham mismatches don't reach portfolios today (those deployments still discover via
  the parent-opportunity path), but they are exactly what bites when they migrate to the label path.

  ### Relation to my PR #45154

  https://github.com/canary-technologies-corp/canary/pull/45154 (`gareth-lloyd/ent-5974`)

  - Discovery keys on `Associated_Enterprise_Deployments__c` (SOQL `INCLUDES`) and
    `Enterprise_Deployment_Segment__c` — **not** hotel codes, so the TLHCT collision can't fool it
    directly.
  - But `get_account_ids_for_enterprise_deployment` in
    `backend/canary/onboarding/services/salesforce_onboarding_fields.py` has **no
    `Parent_Brand__c` predicate** — it inherits whatever the label says. A mislabelled Marriott
    account would go straight into the IHG portfolio. Adding `AND Parent_Brand__c = <IHG id>`, or
    asserting post-fetch and Slacking the mismatch, is a small natural add; both IHG portfolios are
    still in `REPORT_ONLY_PORTFOLIOS` so it surfaces as drift, not breakage.
  - Precedent exists at a different layer: `backend/canary/onboarding/checks/brand_portfolio_membership.py`
    already compares `parent_brand_id` against `limit_to_parent_brand` for onboarding script batches.
  - **Separate finding worth raising:** the Hotel Indigo account has **no**
    `Associated_Enterprise_Deployments__c` value at all. This newly-signed IHG Core hotel would not
    be discovered by the label path — another instance of the "untagged accounts" gap called out in
    the PR description (109 → now 119 tagged).

  ### Draft reply to Andrea — NOT SENT, needs your approval

  > Yes, and we should. Root cause on that Courtyard is a code collision, not bad data entry:
  > `Unique_Hotel_ID__c` is one shared column across all brands, and IHG Inn Codes and Marriott
  > MARSHA codes have the same 5-char shape, so they collide. TLHCT is simultaneously the MARSHA
  > code for Courtyard Thomasville Downtown and the Inn Code for Hotel Indigo Tallahassee
  > Collegetown. The Marketo→SFDC match ran on the code with no brand qualifier and picked the
  > older (Marriott) record.
  >
  > It's not rare — 2,130 codes in SFDC span more than one parent brand, 361 of those are
  > IHG↔Marriott specifically. So ~5% of the namespace is ambiguous on a bare code match.
  >
  > Cheapest fix is Taylor's: qualify the match with `Parent_Brand__c`. 99.4% of accounts that
  > carry a hotel code have parent brand populated, so it resolves essentially all of them. The
  > durable fix is an `IHG_Inn_Code__c` field on Account — we already have
  > `Marriott_Marsha_Code__c` and `Radisson_Property_Code__c`, IHG is the one missing.
  >
  > On the enterprise-deployment side I can add the same assertion in the portfolio sync. Worth
  > knowing: `IHG - GMS` is clean today (119/119 IHG), but `Best Western - GMS` has 95 non-BW
  > accounts tagged and the Wyndham Connect labels have ~97 non-Wyndham. So the check would fire
  > ~190 times on day one — mostly latent, but real.

  ### Open questions for you

  1. Send the reply as drafted, or trim it?
  2. Add the `Parent_Brand__c` guard to PR #45154 now, or split into a follow-up? (PR is already
     large and the guard is behaviour-changing on discovery.)
  3. The ~190 BW/Wyndham label mismatches — worth a Linear ticket for RevOps, or just mention in
     the thread?
project: null
source_id: https://canarytechnologies.slack.com/archives/C0B1Y5K9AMC/p1788373457946269
tags:
- morning-gtd
- slack
time_minutes: 15
title: Answer Andrea on basic brand-vs-enterprise validation
updated: 2026-09-03 14:13:35.142126
waiting_on: null
waiting_since: null
working_on: false
---

She asks whether we can validate that a Marriott hotel is never assigned to IHG. Prompted by the #ihg thread where a Courtyard by Marriott opp came through as IHG Core. Relates to my open PR #45154 on IHG portfolio attribution.
https://canarytechnologies.slack.com/archives/C0B1Y5K9AMC/p1788373457946269

Look at the hotels referenced.

Where is the contradition from? https://canarytechnologies.slack.com/archives/C03V5P4B48P/p1788373232118349