---
area: null
completed_at: null
contexts: []
created: 2026-08-05 14:32:21.010177
defer_until: null
due: null
energy: low
id: 2026-08-05T1432-absorb-this-notion-doc-on-above-property-routing
order: 8
output: |
  ## Agent run 2026-08-06T14:23

  Absorbed **"Discovery: Above-Property Webchat Routing"**
  (https://app.notion.com/p/2fd81468615180579117d9009afa566e) — parent page: Messaging
  (https://app.notion.com/p/91aa9acb8a7f466084ec1d4c6fe1845b). Research dated 2026-02-04.

  ### The doc's argument in one line
  OTAs are property-centric (one inbox per property, no routing); brands are central-first
  (one pool + configurable routing rules). Chain hotels on OTAs get N fragmented inboxes.
  Canary today looks like the OTA model, and the doc argues we should build the brand model.

  ### Evidence base
  - Primary research is a single discovery call: Emil Rasmussen, E-Commerce Manager,
    Guldsmeden Hotels, 2026-02-02 — Gong: https://us-66902.app.gong.io/call?id=6880326139653024547
  - Emil's three asks, which are in tension and worth pulling apart:
    1. one pool for everything (Canary + Expedia + Booking + Instagram/Facebook)
    2. system-decides-next-message triage by SLA (booking Qs = 2h, check-in Qs = 1h)
    3. BUT per-property override — Berlin (Lulu) and Oslo are answered by the property's own
       receptionist, not the central booking dept; and the "central team" is really 5 people
       who each own a hotel, so he wants routing to a *person's* inbox where possible and
       the general pool only as fallback.
    That last point is the real requirement: it's not "central vs property", it's
    "route to the right owner, fall back to general".
  - Secondary/desk research only for Hilton (Kipsu, 7k+ properties, 10.5M conversations 2023)
    and Marriott (Salesforce). No vendor calls.

  ### The doc's proposed V1 (it explicitly asks engineering to confirm)
  Open question in the doc: *"For an above property webchat, do we agree that P1 to P3 are
  the main V1 milestones?"*
  P1 staff multi-hotel access -> P2 cross-property thread visibility -> P3 routing rules
  config -> P4 routing engine -> P5 guest context linking.

  ### Open comments on the doc (all unresolved, all 2026-02-10)
  - **Miguel Santana** on "central-first architectures": "got a 'dummies' description of this?"
    -> the doc needs a plain-English framing paragraph.
  - **Miguel Santana** on Emil's SLA-triage quote: *"Figuring out routing ourselves or 'smart
    routing' might be a herculean task where we could potentially make a lot of mistakes. Kind
    of feels like we're building the equivalent of other AI tools that aggregate your inbox and
    prioritize them."* -> this is the sharpest challenge in the doc and is unanswered.
  - **Sudarshan Muralidhar** on Hilton: "wow so its one inbox for 7k hotels?"

  ### Codebase reality-check (I verified the doc's "Current Canary Data Model" table)
  The doc's data-model section is **directionally right but overstates the schema problem**:
  - CONFIRMED: `Thread.hotel = FK(Hotel, CASCADE)` — `backend/canary/chat/models/thread.py:59`.
    Every index/constraint leads with `hotel`; `Thread.phone` is a OneToOne to a hotel-scoped
    `Phone`, so a guest number gets a separate thread per hotel by construction.
  - CONFIRMED: `MessageEscalation.hotel` FK — `chat/models/message_escalation.py:24`.
  - **WRONG as stated**: "Phone -> Hotel is 1-to-1". It's many phones per hotel, unique on
    `(hotel, phone_number)` — `guest/models/phone.py:44,56`. The same number is N rows, one per
    hotel. Guest identity is genuinely duplicated per property; this is the one place a real
    schema change is needed.
  - **MISLEADING**: "Staff access is per hotel". `CompanyHotelUser` is already an M2M join
    (`hotels/models/company_hotel_user.py:19-42`); `unique_together` only blocks dupes. On top
    of that we already have `PortfolioHotel`, `PortfolioManagedUser`, and
    `PortfolioWidePropertyRoleGrant` (`permissions/models/portfolio_wide_property_role_grant.py`)
    which grants a role across every hotel in a portfolio, enforced by `PortfolioUserGatekeeper`.
    **So P1 is largely already done.** The gap is that messaging *queries* never use it —
    zero non-test hits for `Thread.objects.filter(hotel__in=...)`.
  - **Precedent that undercuts P2's difficulty**: portfolio-scoped cross-hotel search already
    ships for Voice — `backend/canary/voice/views/portfolio_call_search.py` plus the
    `PortfolioResource` / `AuthorizePortfolio` primitives in `portfolios/request_framework/`.
    P2 is a copy of that shape, not new architecture.
  - The Above Property frontend shell already exists (`frontend/hotels/src/views/AboveProperty/`
    — Analytics, Calls, PMSIntegrations, PaymentIntegrations, PortfolioManagement). No Inbox tab.
  - Routing/assignment that already exists and the doc doesn't mention:
    - `GuestAssignment` — OneToOne on **Guest**, user XOR department
      (`guest/models/guest_assignment.py:12-37`); the inbox already filters by it. There is no
      `Thread.assigned_to`.
    - `EscalationRoutingTopic` — LLM matches a topic to a recipient **email** list
      (`chat/models/escalation_routing_topic.py`). This is already a primitive form of the
      routing engine (P4), scoped under a per-hotel escalation.
    - Brand-level webchat exists but is a fake-out: `WebchatConfiguration.deployment_level`
      = HOTEL|BRAND with `brand_properties` as a **JSON blob**, not FKs
      (`chat/models/webchat_configuration.py:140-166`). The property picker
      (`chat/views/api_external_chat.py:205-226`) just hands the guest a slug to jump into that
      property's own widget — guest-side selection, not staff-side routing.

  ### What I'd take into the team conversation
  1. **Re-sequence the milestones.** P1 is mostly built (M2M + portfolio grants). The honest V1
     is: expose a portfolio-scoped thread query mirroring `portfolio_call_search.py`, and add an
     Inbox tab to the existing AboveProperty shell. That is a much smaller V1 than the doc implies.
  2. **Miguel's "herculean task" comment is the decision that actually needs making** and is still
     open. Emil's own words point away from smart routing: he wants deterministic
     property->owner mapping with a general fallback. Deterministic rules (P3) deliver most of
     the value; SLA-based "press next" triage (P4) is the speculative part. Worth explicitly
     cutting P4 from V1 rather than leaving it as "the engine".
  3. **The doc's real blind spot is guest identity.** `Phone`'s `(hotel, phone_number)` unique key
     means "same guest across 3 properties = 3 identities" is a schema problem, not the "nice
     enrichment" P5 is described as. If we ever want one pool, this bites.
  4. **Scope trap:** Emil's ask includes Expedia, Booking.com, Instagram and Facebook in the pool.
     The doc quotes it but never scopes it out. Someone should say out loud whether V1 is
     Canary-webchat-only.
  5. **n=1.** The whole property-level-configurability requirement rests on one call with one
     mid-size European group. Before committing to per-hotel routing config, worth checking it
     against another multi-property customer.

  No external writes made. Nothing posted to Notion — the three open comments are still
  unanswered; if you want to reply to Miguel's routing challenge, that's yours to write.
project: 2026-08-05-strategy
source_id: null
tags: []
time_minutes: 5
title: Absorb this notion doc on above property routing
updated: 2026-08-12 13:47:45.733149
waiting_on: null
waiting_since: null
working_on: false
---

https://app.notion.com/p/canarytechnologies/Discovery-Above-Property-Webchat-Routing-2fd81468615180579117d9009afa566e?source=copy_link