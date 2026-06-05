---
area: null
contexts: []
created: 2026-06-03 19:47:15.449689
defer_until: null
due: null
energy: low
id: 2026-06-03T1947-do-the-due-diligence-on-tool-262-to-see-if-this-wo
order: null
output: |
  ## Agent run 2026-06-04T10:17Z — Due diligence on TOOL-262 (deal auto-labelling for Grecotel/Eurostars/De Luna)

  ### Bottom line
  v1 as written in TOOL-262 (map `parent_opportunity_id` → curated
  `PARENT_OPPORTUNITY_ID_TO_ENTERPRISE_DEPLOYMENT` dict) will label **nothing** for
  Grecotel, Eurostars, or De Luna. None of them are in the curated list, and the
  proposed `Enterprise_Deployment__c = true` fallback almost certainly won't catch them
  either. The mechanism is sound for the mandated brand rollouts it was built for
  (BW/Wyndham/IHG/Marriott) — it just doesn't reach EMEA strategic SMB chains. To cover
  the accounts that actually motivated the playbook, we need a deal-level signal that
  Sales/CS own, i.e. effectively a "strategic" flag. So: answer to Q2 is **yes, lean
  toward a flag**; answer to Q1 is **only partially / not for these accounts as-is**.

  ### Q1 — Can we actually use Salesforce this way?
  Mechanically the FK chain exists and works:
  `Hotel → SalesforceHotelAccount → SalesforceOpportunity.parent_opportunity_id`
  (`onboarding/models/salesforce_opportunity.py:29,98`). It is exactly what onboarding
  already uses (`onboarding/salesforce.py:346`, `services/types.py:101 derive_onboarding_type`).
  Two problems specific to Grecotel/Eurostars/De Luna:

  1. **The curated dict is 16 mandated enterprise rollouts only** — all BW / Wyndham /
     IHG / Aimbridge / Pyramid / Four Seasons / Marriott Vacations / Drury / TUI
     (`onboarding/services/types.py:35-52`). Zero EMEA strategic accounts. A Grecotel
     opp's `parent_opportunity_id` (if it has one) returns `None` from the dict → no label.
  2. **We store only the parent opp *ID*, never its name** (model has
     `parent_opportunity_id` but no name field). So an ID that isn't in the dict is
     opaque — you can't tell "this is Grecotel" without a separate Salesforce lookup.
     Identifying + hardcoding each EMEA parent ID is manual and doesn't scale.

  Will the data even be in the local cache? The sync SOQL
  (`services/salesforce_opportunity.py:242-265`) pulls opps where
  `Enterprise_Deployment__c = true` **OR** (`StageName IN (Closed Won/Closed Lost/
  Negotiation/Proposal) AND Account_Record_Type__c = 'Hotels'`). A live Grecotel
  property = Closed Won + Hotels record type, so its opp **would** sync *if an account
  sync has ever run for that hotel*. But:
  - `Enterprise_Deployment__c` is almost certainly **false** for these (they're not in
    the mandated-deployment program), so the ticket's proposed generic "Enterprise Deal"
    fallback label also misses them.
  - Whether a single shared **parent opportunity** even exists per EMEA chain is unknown.
    Parent/child opp structure is a Salesforce convention used for the big multi-brand
    mandated rollouts; a boutique chain or single-property deal may have no parent opp at
    all, or one parent per property. **This is the one fact I could not verify from code —
    it needs a prod/Salesforce read (see "Not yet verified" below).**

  ### Q2 — Do we need an "is strategic parent opportunity" flag on Opportunity?
  Recommend **yes** (or an equivalent Salesforce-owned signal). Rationale:
  - The curated Python dict requires an engineer to hand-add each parent ID and stores no
    name — wrong tool for a sales-driven, growing set of strategic launches. It will
    chronically lag reality (the ticket's own open question admits this).
  - There is **no deal-level strategic concept in Salesforce today**. The only existing
    flag is `Enterprise_Deployment__c` (`services/salesforce_opportunity.py:31`), which
    means "mandated enterprise rollout", not "strategic launch we're QA-gating". They are
    not the same set — the playbook's strategic accounts (Grecotel/Eurostars/De Luna/
    Danubius/Travelodge) are mostly NOT enterprise deployments.
  - There IS already a `Hotel.is_strategic_account` boolean (`hotels/models/hotel.py:525`,
    admin-editable) — but it's a manual *hotel-level* internal flag, tells you nothing
    about *which deal*, and isn't sourced from Salesforce. Useful as a coarse prioritise
    signal, not as the deal attribution TOOL-262 wants.

  A Salesforce checkbox like `Is_Strategic_Launch__c` (set by Sales/CS at deal level),
  synced down onto `SalesforceOpportunity`, would: cover EMEA accounts the dict can't,
  remove the need to hardcode IDs, and give triage a declarative "is this a strategic
  launch" signal. If we also sync the parent opp **name**, the label can be
  self-describing without a dict at all.

  ### Suggested shape for TOOL-262
  - Keep the curated-dict path for the mandated rollouts (it's correct + deterministic).
  - Add a Salesforce-sourced strategic flag (+ ideally parent/opp name) as the primary
    signal for everything else, so Grecotel/Eurostars/De Luna get labelled without code
    changes per deal. This is the bit that makes the playbook's at-risk accounts visible
    in triage, which is the whole point of the ticket.
  - Confirm the lazy-sync freshness guard still applies (account-level
    `last_salesforce_sync`, async task only — never in the webhook hot path; matches the
    ticket).

  ### Not yet verified (needs a read-only prod/Salesforce lookup — did NOT run, no approval)
  Per repo + GTD-agent safety rules I did not query staging/prod. To close the loop, run
  (read-only) for each of Grecotel / Eurostars / De Luna:
  - Does a `Hotel` exist, and does it have a `SalesforceHotelAccount` with a non-null
    `last_salesforce_sync`?
  - Do its `SalesforceOpportunity` rows have a `parent_opportunity_id`? Is it shared
    across the chain's hotels (= a real parent opp) or null/per-property?
  - Is `Enterprise_Deployment__c` / our `deployment_segment` set on any of them?
  I can draft the exact ORM/SOQL and run it if you approve hitting prod read-only, or you
  can hand it to onboarding/RevOps. The empirical answer determines whether "add their
  parent IDs to the dict" is even possible, or whether the flag is mandatory.

  ### Key references
  - `onboarding/services/types.py:13-55` — EnterpriseDeployment enum + curated dict (16 IDs)
  - `onboarding/services/salesforce_opportunity.py:242-265` — sync SOQL + filters
  - `onboarding/services/salesforce_opportunity.py:31` — `Enterprise_Deployment__c`
  - `onboarding/salesforce.py:346`, `services/types.py:101` — dict consumption
  - `onboarding/models/salesforce_opportunity.py:29,98` — FK chain + parent_opportunity_id (no name stored)
  - `hotels/models/hotel.py:525` — existing manual `is_strategic_account` hotel flag
  - `linear_agent/services/label_application.py` — where deal labels would be wired in

  ## Agent run 2026-06-04T16:30Z — Verified the limitations + drafted a ticket comment

  Re-launched to (1) verify the prior run's *assumed* limitations against the actual
  source, and (2) draft a comment for TOOL-262. All code-level limitations now confirmed
  by reading the files (not inferred):

  - **Curated dict = 16 mandated rollouts, zero EMEA** — confirmed `types.py:35-53`
    (BW / Wyndham / IHG pilot / Aimbridge / Pyramid / Four Seasons / Marriott Vacations /
    Drury / TUI). Grecotel / Eurostars / De Luna absent → dict lookup returns None.
  - **Only the parent-opp *ID* is stored, never the name** — confirmed. Model field
    `parent_opportunity_id` (`salesforce_opportunity.py:98`); sync fetches
    `Parent_Opportunity__c` (the ID) at `:322`; no parent-opp-name field exists anywhere.
  - **Sync SOQL bias** — confirmed `:255-258`: `Enterprise_Deployment__c = true` OR
    (active/closed StageName AND `Account_Record_Type__c = 'Hotels'`). EMEA live props
    ride the 2nd clause but their `Enterprise_Deployment__c` is ~certainly false, so the
    ticket's proposed generic "Enterprise Deal" fallback misses them too.
  - **`Hotel.is_strategic_account`** confirmed at `hotel.py:525` (hotel-level/manual).
  - **`apply_labels_to_issue(resolved_hotels=...)`** confirmed `label_application.py:31-33`
    — correct wiring point; hotel already in scope there.

  Still NOT verifiable from code (no SOQL/ORM MCP tool exposed; did not hit prod): whether
  Grecotel / Eurostars / De Luna actually have a single *shared* parent opportunity in
  Salesforce. If they don't, "add their parent IDs to the dict" is impossible, not just
  manual — which is exactly why the flag approach is the safer bet. Needs a read-only
  RevOps/Salesforce lookup to close.

  ### DRAFT COMMENT for TOOL-262 (NOT posted — awaiting Gareth's approval to post)

  > **Due diligence on step 2 — does this actually work for Grecotel / Eurostars / De Luna?**
  >
  > Short answer: **as specified, v1 labels nothing for these three.** Step 2 makes a few
  > assumptions that don't hold for EMEA strategic SMB chains. I verified each against the code:
  >
  > **1. "Reuse the curated deal list — no new heuristic needed for v1."**
  > `PARENT_OPPORTUNITY_ID_TO_ENTERPRISE_DEPLOYMENT` is 16 hardcoded parent-opp IDs
  > (`onboarding/services/types.py:35-53`), every one a *mandated* enterprise rollout — BW,
  > Wyndham, IHG pilot, Aimbridge/Pyramid tipping, Four Seasons, Marriott Vacations, Drury,
  > TUI. Grecotel, Eurostars and De Luna are not in it. A hotel in those chains maps its
  > opp's `parent_opportunity_id` through the dict → `None` → no deal label. So the exact
  > accounts that motivated the playbook are the ones v1 can't see.
  >
  > **2. "The local opportunity cache is already biased to significant deals."**
  > True, but biased toward a *different* set. The sync SOQL pulls opps where
  > `Enterprise_Deployment__c = true` OR (active/closed stage AND record type `Hotels`)
  > (`salesforce_opportunity.py:255-258`). A live Grecotel property does sync — via the
  > second clause — but its `Enterprise_Deployment__c` is almost certainly `false` (not in
  > the mandated-deployment program), so the proposed generic "Enterprise Deal" fallback
  > (open question #1) misses it too.
  >
  > **3. We store only the parent-opp ID, never its name.**
  > The sync fetches `Parent_Opportunity__c` (the ID) and stores it as
  > `parent_opportunity_id` — there is no parent-opp-*name* field
  > (`salesforce_opportunity.py:98, 322`). So even if a Grecotel parent opp exists, an ID
  > not in the dict is opaque; you can't tell "this is Grecotel" without a separate SF
  > lookup. Hand-adding each EMEA parent ID is the only path the dict offers, and it won't
  > scale to a growing, sales-driven set.
  >
  > **The one thing I could not verify from code** (needs a read-only Salesforce/RevOps
  > lookup): **whether each chain even has a single shared parent opportunity.** Parent/child
  > opp structure is a convention for the big mandated multi-brand rollouts; a boutique EMEA
  > chain may have no parent opp, or one parent per property. If there's no shared parent,
  > then "identify the parent IDs and add them to the dict" isn't just manual — it's
  > impossible. That's the real empirical question step 2 is asking. Concretely, for each of
  > Grecotel / Eurostars / De Luna: does a `Hotel → SalesforceHotelAccount` exist with a
  > non-null `last_salesforce_sync`; do the opps carry a `parent_opportunity_id`; is it
  > shared across the chain.
  >
  > **Recommendation: add an "is strategic" flag on the Opportunity, *alongside* the dict —
  > not replacing it.**
  >
  > Keep the curated dict exactly as-is for the mandated rollouts; it's deterministic and
  > correct for what it covers. Add a second, Salesforce-owned signal as the primary path
  > for everything else:
  >
  > - A checkbox on Opportunity (e.g. `Is_Strategic_Launch__c`) that Sales/CS set at the
  >   *deal* level. Sync it onto `SalesforceOpportunity` next to `deployment_segment` — it
  >   rides the SOQL + sync we already run, no new pipeline.
  > - Detection in `apply_labels_to_issue` becomes two coexisting rules: **(a)** map
  >   `parent_opportunity_id` through the dict as today → a specific `Deal: <brand>` label;
  >   **(b)** if *any* opp on the hotel has the strategic flag set, apply a
  >   `Deal: Strategic Launch` label even when the parent isn't in the dict. (a) wins for
  >   the named brands; (b) is the catch-all that finally covers EMEA.
  > - This removes the need to hand-add IDs, **doesn't depend on a shared parent opp
  >   existing**, and gives triage a declarative "in-flight strategic launch" filter — the
  >   actual ask. If we also sync the parent/opp name, labels can be self-describing without
  >   growing the dict.
  >
  > (There's already a manual `Hotel.is_strategic_account` boolean at
  > `hotels/models/hotel.py:525`, but it's hotel-level, internal, and not deal-attributed —
  > fine as a coarse prioritisation hint, not as the deal signal this ticket wants.)

  ### Next step (user's call)
  - Approve posting the above to TOOL-262, or edit first.
  - Separately: get RevOps/onboarding to run the read-only Salesforce lookup on the 3
    chains to settle whether a shared parent opp exists (determines dict-feasibility).

  ## Agent run 2026-06-05T09:10Z — Read the EMEA playbook; refined the comment

  Read the Notion playbook (Strategic Account Launch Playbook — EMEA, author Sebastian,
  Draft v0.1). The user's link anchored on §3 "Entry criteria". Findings that change/
  strengthen the recommendation:

  1. **"Strategic" is a leadership/Sales judgment, and it's an explicit OPEN ITEM** — not
     a Salesforce-encoded concept. §3 trigger = ARR >= $40k (placeholder) OR "deemed
     strategic by leadership", AND close-prob >= 80%, AND EMEA, AND custom-build flag.
     The table literally asks "When do we deem a customer a strategic account?" and §15
     lists the thresholds as unratified. => There is no system-of-record "strategic
     launch" signal today; an `Is_Strategic_Launch__c` checkbox on the Opportunity is the
     thing that operationalizes §3's "deemed strategic by leadership" clause. Stronger
     argument for the flag than the prior run had.
  2. **Mandated set != strategic-launch set (confirmed both ways).** Playbook accounts —
     Grecotel, Eurostars, De Luna (proof cases) + Danubius, Travelodge UK (next, §13) —
     are none of them in the 16-entry dict. The dict can't reach a single account this
     playbook exists for.
  3. **New finding: `SalesforceOpportunity.arr` is already synced (`:140`).** §3's primary
     threshold is ARR-based, so part of "is strategic" is already derivable from cache —
     but the "or deemed strategic by leadership" override still needs a human-set flag.
     ARR = useful secondary/fallback signal.
  4. **Label is launch-phase-scoped.** TOOL-262 wants "issues against an *in-flight*
     strategic launch"; the playbook is about new go-lives (≈4wk soft launch + 30d post-
     launch window, §12). A permanent boolean (or `Hotel.is_strategic_account`) over-labels
     after the launch ends. Design the signal to reflect launch phase (clear at hard-launch
     +30d, or gate on opp stage), not a forever account attribute.
  5. **Scope is clean.** Playbook §2 routes existing-customer regressions (Lugano Dante)
     to eng triage, away from this process; TOOL-262 already scopes to launch deals. No
     conflict.

  ### REVISED DRAFT COMMENT for TOOL-262 (supersedes the 16:30 draft — NOT posted)

  > **Due diligence on step 2 — does this actually work for Grecotel / Eurostars / De Luna?**
  >
  > Short answer: **as specified, v1 labels nothing for these three**, and after reading the
  > EMEA launch playbook I think the curated-dict path is structurally the wrong primary
  > signal for this ticket. Detail below; each point verified against the code.
  >
  > **Where step 2 is guessing:**
  > 1. *"Reuse the curated deal list — no new heuristic needed for v1."*
  >    `PARENT_OPPORTUNITY_ID_TO_ENTERPRISE_DEPLOYMENT` is 16 hardcoded parent-opp IDs
  >    (`onboarding/services/types.py:35-53`), every one a *mandated* enterprise rollout
  >    (BW, Wyndham, IHG pilot, Aimbridge/Pyramid tipping, Four Seasons, Marriott Vacations,
  >    Drury, TUI). Grecotel, Eurostars, De Luna — and the playbook's next launches,
  >    Danubius and Travelodge UK — are **none of them in it**. The mandated-enterprise set
  >    and the "strategic launch" set are different populations; the dict can't reach a
  >    single account this playbook exists for.
  > 2. *"The cache is already biased to significant deals."* True, but toward a different
  >    set. The sync SOQL pulls `Enterprise_Deployment__c = true` OR (active/closed stage AND
  >    record type `Hotels`) (`salesforce_opportunity.py:255-258`). EMEA live props sync via
  >    the second clause, but their `Enterprise_Deployment__c` is almost certainly `false`,
  >    so the proposed generic "Enterprise Deal" fallback (open question #1) misses them too.
  > 3. *We store only the parent-opp ID, never its name* (`:98, :322` — sync fetches
  >    `Parent_Opportunity__c`, the ID). So an ID not in the dict is opaque; you can't tell
  >    "this is Grecotel" without a separate SF lookup, and hand-adding each EMEA parent ID
  >    doesn't scale.
  > 4. **Unverifiable from code** (needs a read-only Salesforce/RevOps lookup): whether these
  >    chains even *have* a single shared parent opportunity. If they don't, "add their
  >    parent IDs to the dict" isn't manual — it's impossible. For each of Grecotel /
  >    Eurostars / De Luna: does `Hotel → SalesforceHotelAccount` exist with non-null
  >    `last_salesforce_sync`; do the opps carry a `parent_opportunity_id`; is it shared
  >    across the chain.
  >
  > **Why a flag, and why it fits the playbook.** The playbook's §3 entry criteria define a
  > strategic launch as *ARR ≥ \$40k (or simply deemed strategic by leadership), ≥80% close
  > probability, EMEA, custom-build* — and it explicitly flags "when do we deem a customer
  > strategic?" as an open question. In other words there is **no system-of-record signal
  > for "strategic launch" today**; it's a human call. `Enterprise_Deployment__c` means
  > "mandated rollout", which is a different thing. So:
  >
  > - Add an **`Is_Strategic_Launch__c` checkbox on Opportunity**, set by Sales/CS at the
  >   deal level — this is the field that operationalizes §3's "deemed strategic by
  >   leadership" clause. Sync it onto `SalesforceOpportunity` next to `deployment_segment`;
  >   it rides the SOQL + sync we already run.
  > - Detection in `apply_labels_to_issue` (`linear_agent/services/label_application.py:31`)
  >   = two coexisting rules: **(a)** map `parent_opportunity_id` through the dict → specific
  >   `Deal: <brand>` label (unchanged, deterministic, correct for the mandated rollouts);
  >   **(b)** if any opp on the hotel has the strategic flag set → `Deal: Strategic Launch`
  >   label, even when the parent isn't in the dict. (a) wins for the named brands; (b) is
  >   the catch-all that finally covers EMEA.
  > - **`SalesforceOpportunity.arr` is already synced (`:140`)**, and §3's primary threshold
  >   is ARR-based — so ARR ≥ \$40k can be a secondary/auto signal, but the "or deemed
  >   strategic by leadership" override is why the manual flag is still needed.
  > - **Make it launch-phase-scoped.** This ticket wants issues against an *in-flight* launch;
  >   the playbook scopes to new go-lives (≈4wk soft launch + 30d post-launch window). A
  >   permanent flag — or the existing manual `Hotel.is_strategic_account` (`hotel.py:525`),
  >   which is hotel-level and not deal-attributed — would keep labelling long after launch.
  >   Worth clearing the flag at hard-launch +30d, or gating the label on opp stage, so the
  >   signal means "active strategic launch", not "important account forever".
  >
  > Net: keep the dict for the mandated rollouts; add the opp-level strategic flag as the
  > primary path for everything else. That covers Grecotel/Eurostars/De Luna/Danubius/
  > Travelodge without per-deal code changes, doesn't depend on a shared parent opp existing,
  > and gives triage the declarative "in-flight strategic launch" filter that is the actual ask.

  ### Next step (user's call)
  - Approve posting the REVISED draft to TOOL-262, or edit first.
  - Optional: loop Sebastian (playbook author) — the §3 "what counts as strategic" open
    item and an `Is_Strategic_Launch__c` field are the same decision; worth resolving once.

  ## Agent run 2026-06-05T11:48Z — Corrected the framing, then POSTED

  Gareth pushed back on the "dict can't reach them" framing — correctly. I'd conflated a
  feasibility claim ("won't work") with a maintainability opinion ("doesn't scale"). The
  honest position: the dict CAN work for Grecotel etc. — it's the same mechanism the 16
  entries use — IF each chain has a single shared parent opp. That precondition is the only
  real blocker, and it's a 5-min RevOps lookup, not a design flaw. Redrafted around
  "dict is viable; flag is the scale play; one Salesforce fact decides it."

  **POSTED to TOOL-262** (approved by Gareth this session). Comment id
  `ebb38c77-6140-4db9-82eb-afa959c90a5d`, authored as Gareth, top-level thread.
  Final text = the "dict can work under one precondition / dict-vs-flag decision" version.
project: null
source_id: null
tags: []
time_minutes: 5
title: Do the "due diligence" on TOOL-262 to see if this would work for grecotel,
  Del Luna etc
updated: 2026-06-05 11:48:00.000000
waiting_on: null
waiting_since: null
working_on: false
---

* Can we actually use salesforce this way?
* Do we need an "is strategic parent opportunity" flag on opportunity? 

context: https://www.notion.so/canarytechnologies/Strategic-Account-Launch-Playbook-EMEA-Soft-Launch-QA-36781468615181b885cefd2197cd6207?source=copy_link