---
area: null
completed_at: null
contexts: []
created: 2026-09-30 10:04:13.888752
defer_until: null
due: null
energy: low
id: 2026-09-30T1004-respond-to-comments-on-binding-tree-design
order: 5
output: |
  ## Agent run 2026-09-30T14:05:00+01:00

  Drafted replies to the three open comments on the Binding Rules Tree design (https://app.notion.com/p/canarytechnologies/Binding-Rules-Tree-3e58146861518147b489e3fa8e8aef09). Nothing posted to Notion; paste each reply into its thread.

  Commenters: jhart = Joshua Hart (two comments), abradshaw = Andrea Bradshaw (one comment).

  Grounding I checked in the code before drafting:
  - HotelAttributes gets brand_id / parent_brand_id / management_company_id from Salesforce (OnboardingService.get_salesforce_account_categories) and caches them in StoredHotelAttributes; country comes from hotel.country_code, never Salesforce (rules_based_configuration/services/hotel_attributes.py:19-58).
  - Gap that Josh's Salesforce question exposes: fetch_hotel_attributes_for_hotel raises ValueError("Hotel does not have a Salesforce Account ID.") when a hotel has no StoredHotelAttributes row and no sfdc_account_id (hotel_attributes.py:29-30). Such a hotel cannot resolve any tree today, binding or brand.
  - Gateway capabilities already exist as PaymentGatewayCapability (TOKENIZE, AUTHORIZE_CARD, CHARGE_CARD, HOSTED_REDIRECT, ...) in payment_gateways/constants.py:36-58, fetched per gateway config via PaymentGatewayApi.get_gateway_capabilities. hotels/utils/pms_gateway_config_checks.py:71-130 already hand-codes the Nexi-shaped check ("gateway can tokenize but cannot place holds -> set disable_authorization_charge on these form templates") as a report-only admin check.
  - Surcharge law enforcement: SurchargeService._validate_location_based_surcharge (payment_gateways/services/surcharge.py:48-93) validates only US state caps (US_STATE_RULES) at write time; the surcharge policy is a Surcharge model with portfolio fallback, not a Configuration column. The engine has no state dimension (GroupAttributes: countries, canary_region only).

  ---

  ### Reply 1: Josh Hart, inline on "One subpackage per authority (law/, pms/, platform/)"
  Thread: https://app.notion.com/p/3e58146861518147b489e3fa8e8aef09?d=3ea81468615180c9ac99001c22f81d07&pvs=42#3e58146861518020a424d2f85f364e9f

  > Yes, and it fits the design as written rather than needing a new mechanism. A gateway rule is the PMS case with a different dimension: a fourth authority `GATEWAY_CAPABILITY` under `binding/gateway/` (Payments in CODEOWNERS), scoped by `gateway_capabilities_absent`, sourced from `PaymentGatewayApi.get_gateway_capabilities` (the same `PaymentGatewayCapability` set `pms_gateway_config_checks.py` already reads). Nexi becomes: `GroupAttributes(gateway_capabilities_absent={TOKENIZE})` defining each tokenization-triggering setting as `BINDING` `False`, authority `GATEWAY_CAPABILITY`, explanation "gateway cannot tokenize". That gives us what the admin-page check does not: drift on every hotel, a seed value at onboarding, and an E003 boot failure if a brand tree turns one of those features on.
  >
  > Three things it needs first, which is why I'd keep it out of releases 1-3 and treat it like `binding/pms/`:
  > 1. A dimension on `GroupAttributes` / `HotelAttributes`. Brand comes from Salesforce and is cached in `StoredHotelAttributes`; gateway capabilities are a remote call, so they'd be cached the same way and refreshed on gateway-config change.
  > 2. A definition of "the hotel's gateway": authorization, check-in and payment links can each point at a different `payment_gateway_config_id`. Probably the rule scopes per use (`authorization_gateway_capabilities_absent`), not per hotel.
  > 3. Keys. Some of the quirks are on per-template rows (`FormTemplate.disable_authorization_charge`), not hotel `Configuration` columns, and the engine only keys the latter. Those need a reader, like retention in section 10, or a hotel-level key that the template inherits.
  >
  > Could you list the gateway quirks that are impossibilities (the gateway cannot do it, so the setting must be off) versus preferences (it works but we'd rather not)? The first list is `binding/gateway/`; the second is a default in the fallback tree. I'll add the `gateway/` line to the layout and a row to the open questions with you as owner.

  ---

  ### Reply 2: Josh Hart, page-level comment (surcharging law, Salesforce as source of truth, ESA)
  Thread: https://app.notion.com/p/3e58146861518147b489e3fa8e8aef09?d=56081468615182da82cd03ee5c99e885&pvs=42

  > Thanks. Three parts.
  >
  > **Gateways**: answered on the inline thread; short version is a fourth authority scoped by gateway capability, after the dimension exists.
  >
  > **Surcharge law**: that is `LAW` authority scoped by country, so it belongs in `binding/law/surcharge.py` with Legal reviewing, and the Australia ban is the first rule: `AU_SURCHARGE` defines the surcharge keys as `Equals(NO_SURCHARGE)` (or `Empty()`), explanation naming the regulation. Two reasons not to move the payments enforcement into the tree yet, both the same shape as retention (section 10): the policy is a `Surcharge` row with portfolio fallback, not a `Configuration` column, so it needs a registered reader for the effective value; and `_validate_location_based_surcharge` is state-scoped (US_STATE_RULES) and the engine has no state dimension. So the proposal is: the tree owns "what the law says" and drift reports against it for every hotel including independents; `SurchargeService` keeps the write-time validation until a `pre_save` on the reader can replace it. If you can point me at where the "surcharging removed from Australian hotels" work is tracked, I'll add it as release 2's third rule candidate and you as the reviewer for the `law/surcharge.py` payload.
  >
  > **Salesforce**: no. Salesforce supplies only brand, parent brand and management company, cached in `StoredHotelAttributes`; the binding tree never scopes by any of those. Country comes from `hotel.country_code` and PMS/gateway capabilities from the integration config. So the 40 disconnected ESA hotels get every law rule regardless of what Salesforce knows about them; what they miss is the ESA brand tree, which is today's problem and unchanged by this design. Reconciliation matters for brand rules, not binding ones.
  >
  > Your question did expose a real gap, though: `fetch_hotel_attributes_for_hotel` raises if a hotel has no stored attributes and no `sfdc_account_id`, so a hotel with no Salesforce account at all cannot resolve any tree today. "Independents covered" needs that path to build country-only attributes without Salesforce. I'll add that to section 8 and a third count to section 13 (hotels with no `StoredHotelAttributes` and no `sfdc_account_id`).

  ---

  ### Reply 3: Andrea Bradshaw, inline on "Reading 'all binding rules that touch Spain' is one grep SPAIN ... at a shell"
  Thread: https://app.notion.com/p/3e58146861518147b489e3fa8e8aef09?d=3ea81468615180579d96001c96758cde&pvs=42#3e5814686151804c9d9fc25cdb05c2d1

  > Agreed, and the sentence oversells the grep. `grep SPAIN` only finds rules that name Spain; the EU rule names `EUROPEAN_UNION` from `scopes.py`. The programmatic read is the one that answers your question: `binding_rules_for_country(Country.SPAIN)` resolves the tree for synthetic attributes with country=Spain, so it returns every rule whose scope contains Spain (`EU_ID`, `EEA` retention caps, anything Schengen-wide) with the Spanish exception applied per key, so for `id_step` you see `ES_ID`'s set, not `EU_ID`'s. I'll reword it to:
  >
  > "Reading 'all binding rules that touch Spain' is `ConformityService.binding_rules_for_country(Country.SPAIN)` at a shell: every rule whose scope contains Spain, including EU- and EEA-wide sets from `scopes.py`, with Spain's exceptions applied per key. `grep SPAIN` finds only the exceptions."
  >
  > and add a Spain row to the section 8 table showing `EU_ID` plus `ES_ID` resolving together.

  ---

  Doc edits implied by the replies (not made; the design page is in review and each is a judgment call):
  1. Layout: add `gateway/` as a fourth subpackage and `GATEWAY_CAPABILITY` as a fourth authority, marked "after the gateway dimension lands", with Payments in CODEOWNERS.
  2. Open questions: rows for Josh (gateway impossibilities vs defaults; surcharge law tracking), and a Legal row for the Australia surcharge ban.
  3. Section 8 / 13: attribute fetch must not require Salesforce; third blast-radius count (no StoredHotelAttributes and no sfdc_account_id).
  4. Reword the `grep SPAIN` sentence per reply 3; add a Spain row to the section 8 table.
  5. Rollout table, release 2: add `AU_SURCHARGE` as a candidate once the surcharge reader exists.
  ## Agent run 2026-09-30T15:10:00+01:00

  Follow-up asked: "The response to andrea names edits to make. Get ready to make these with my sign off"

  Prepared, not applied. Nothing written to Notion. Two edits to the design page (https://app.notion.com/p/canarytechnologies/Binding-Rules-Tree-3e58146861518147b489e3fa8e8aef09), ready to apply with `notion-update-page` `update_content` on your "yes".

  Context: you already posted the short reply on Andrea's thread at 11:21 today ("Agreed, and the sentence oversells the grep ... I'll reword it."), so the reword is a public commitment. Thread: https://app.notion.com/p/3e58146861518147b489e3fa8e8aef09?d=3ea81468615180579d96001c96758cde&pvs=42#3e5814686151804c9d9fc25cdb05c2d1

  ### Edit 1: reword the grep sentence (section "Layout and ownership", the paragraph starting "Import order matters")

  Current text:
  > Reading "all binding rules that touch Spain" is one `grep SPAIN` in one directory, or `ConformityService.binding_rules_for_country(Country.SPAIN)` at a shell.

  Proposed text:
  > Reading "all binding rules that touch Spain" is `ConformityService.binding_rules_for_country(Country.SPAIN)` at a shell: every rule whose scope contains Spain, including the EU- and EEA-wide sets from `scopes.py`, with Spain's exceptions applied per key (so the ID key shows `ES_ID`'s set, not `EU_ID`'s). `grep SPAIN` finds only the exceptions.

  Caveat: Andrea's inline thread is anchored to this sentence. Replacing the text will likely unanchor the thread (it stays in the comments sidebar, no longer highlighted). Suggest resolving the thread after the edit lands.

  ### Edit 2: add an "Independent, Spain" row to the section 8 table ("Runtime resolution and seeding"), directly after "Independent, Germany"

  | Hotel | Brand tree | Binding tree | `get_setting_value(ID)` | `hotel_conforms` checks |
  |---|---|---|---|---|
  | Independent, Spain | no tree | `EU_ID` (Spain in `EUROPEAN_UNION`) and `ES_ID` nested under it; `ES_ID` replaces `EU_ID`'s define for the ID key only, every other EU-wide key falls through unchanged | nothing for the ID key (`ES_ID` has no `default`); `binding_rules_for_country(SPAIN)` lists both groups, `ES_ID` winning on the ID key | stored `in` `ES_ID`'s set: `{REQUIRED, REQUIRED_WITH_OCR, OPTIONAL, OPTIONAL_WITH_OCR}` |

  The existing "Wyndham, Spain" row stays; it shows the boot conflict, this row shows the EU-plus-exception resolution Andrea asked to see.

  ### Two things the row surfaced, for your call before applying

  1. `ES_ID` carries no `default=` in the section 5 code sample, so an independent Spanish hotel gets nothing seeded for the ID key while an independent German hotel gets `OPTIONAL`. If that is unintended, add `default=OPTIONAL` to `ES_ID` (it is in both sets) and the row's fourth cell becomes "`OPTIONAL` seeded (`ES_ID` default)". I have written the row for the design as it stands.
  2. The design's only EU-wide rule is `EU_ID`, and Spain overrides it, so no example key actually demonstrates "an EU rule still applies to Spain unchanged". The row says so in words ("every other EU-wide key falls through unchanged"). A concrete second EU-wide key (e.g. an EEA retention cap) would make the point better but would be new design content, not a wording fix.

  Exact `old_str` / `new_str` payloads are in the scratchpad at /private/tmp/claude-501/-Users-garethlloyd-projects-canary/27c9879c-1001-429d-9030-6c7903ac41ed/scratchpad/edits.md. Both anchors are unique on the page (checked). If Notion rejects the plain-text `old_str` for edit 1 because of the inline-comment span markup, I will retry with the span-wrapped form from the fetch output.

  ## Agent run 2026-09-30T15:40:00+01:00

  Follow-up asked: "Apply" (sign-off on the two edits above).

  Applied both edits to the design page (https://app.notion.com/p/canarytechnologies/Binding-Rules-Tree-3e58146861518147b489e3fa8e8aef09) and re-fetched to verify:
  1. "Layout and ownership": the grep sentence now reads "Reading 'all binding rules that touch Spain' is `ConformityService.binding_rules_for_country(Country.SPAIN)` at a shell: every rule whose scope contains Spain, including the EU- and EEA-wide sets from `scopes.py`, with Spain's exceptions applied per key (so the ID key shows `ES_ID`'s set, not `EU_ID`'s). `grep SPAIN` finds only the exceptions." The old "one `grep SPAIN` in one directory" wording is gone.
  2. Section 8 table ("Runtime resolution and seeding"): "Independent, Spain" row inserted after "Independent, Germany", exactly as proposed.

  Andrea's inline thread stayed anchored to the reworded sentence (the first plain-text attempt failed to match because of the comment span markup; the span-wrapped retry kept the anchor). Thread: https://app.notion.com/p/3e58146861518147b489e3fa8e8aef09?d=3ea81468615180579d96001c96758cde&pvs=42#3e5814686151804c9d9fc25cdb05c2d1

  Not done, your call:
  - Resolve Andrea's thread, or reply on it that the reword and the row are in.
  - Decide whether `ES_ID` should carry `default=OPTIONAL` (the new row currently says nothing is seeded for the ID key). If yes, the section 5 code sample and the row's fourth cell both change.
  - Josh's two threads still have no reply posted; drafts are in the first run above.
project: 2026-04-16T1319-rules-based-config
source_id: null
tags: []
time_minutes: 5
title: respond to comments on binding tree design
updated: 2026-10-06 12:48:18.250173
waiting_on: null
waiting_since: null
working_on: false
---

draft replies: 
https://app.notion.com/p/canarytechnologies/Binding-Rules-Tree-3e58146861518147b489e3fa8e8aef09?source=copy_link