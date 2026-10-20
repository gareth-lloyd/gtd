---
area: null
completed_at: 2026-10-19 16:32:40.448776
contexts:
- react
created: 2026-10-19 10:47:41.804550
defer_until: null
due: 2026-10-19
energy: medium
id: 2026-10-19T1047-answer-zendesk-bri-kapellas-can-we-disable-credit
order: null
output: |
  ## Agent run 2026-10-19T13:05

  Thread: https://canarytechnologies.slack.com/archives/C03V5P4B48P/p1792190561632889?thread_ts=1792190561.632889&cid=C03V5P4B48P
  Zendesk #211260: https://canarysupport.zendesk.com/agent/tickets/211260
  Bri asked Taylor (2026-10-17) whether IHG check-in credit-card sync can be disabled, or if scripts would overwrite it. The hotel user (lancp) asked: "Is there a way that we can have these not automatically sync to our PMS?"
  Taylor already replied: "no that is a standard setting. curious why they want it turned off." The thread has had no reply since. Nothing was sent.

  ### What the code says
  - Check-in has no setting that turns off only the card. The card goes to the PMS when `integration_auto_post_to_pms` is on AND `credit_card_step != DISABLED` (hotels/utils/pms_gateway_config_checks.py:249-306). The raw-vs-token override only changes how the card is sent, not whether it is sent.
  - The only levers:
    1. `integration_auto_post_to_pms = False` stops ALL check-in posting to the PMS, not just cards: reg card data, email, phone, passport, DOB, nationality, notes, UDF, ID submitted, check-in time.
    2. `credit_card_step = DISABLED` stops collecting the card at check-in altogether. That is a product change, not a sync change.
  - Will it be overwritten? Yes for (1):
    - It is pinned in the rules registry as FINAL True for both IHG GMS Core (enterprise_ihg/configs/ihg_gms_core.py:47) and IHG Pilot (enterprise_ihg/configs/ihg_pilot.py:43).
    - The IHG Enable MSA Products onboarding step hard-sets it back to True every time it runs (onboarding/configuration_providers/ihg/gms_core_ihg_enable_msa_products_provider.py:65; the pilot version is enable_msa_products_provider.py:60).
    - The daily drift cron (rules_based_configuration/management/commands/cron_detect_drift.py) does NOT write. It would flag the hotel as drifted and post a Slack alert.
  - (2) `credit_card_step` is not in the IHG registry or the IHG enable-products provider, so I found nothing that resets it. That is unverified for the other IHG providers beyond a grep of onboarding/configuration_providers/ihg/.
  - If they mean card posting on authorizations rather than check-in, it is a separate setting. `hotel.authorization_configuration.v2_do_not_post_cards_to_pms` is FINAL False for IHG Pilot live (ihg_pilot.py:138), so the same answer applies.

  ### Draft reply (NOT sent; for Gareth to post in the thread if wanted)
  > Adding to Taylor's answer: check-in has no "don't sync cards" setting. Cards go to the PMS as part of check-in auto-post, which is a FINAL IHG brand standard. Turning it off would also stop reg card details (email, phone, ID, etc.) from posting, and IHG onboarding re-runs plus drift monitoring would turn it back on or flag it. The only other option is to remove the card step from check-in completely, which would stop collecting the card at all. What problem is the hotel trying to solve: duplicate cards on the folio, the wrong payment slot, PCI concerns? There may be a better fix.

  Open question: what is the hotel's actual problem? The Zendesk ticket isn't readable from here, and no hotel ID is in the thread.
project: 2026-08-31-ihg
source_id: https://canarytechnologies.slack.com/archives/C03V5P4B48P/p1792190561632889?thread_ts=1792190561.632889&cid=C03V5P4B48P
tags:
- morning-gtd
- slack
- from-awareness
time_minutes: 15
title: 'Answer Zendesk/Bri Kapellas: can we disable credit-card sync for IHG check-in,
  or will scripts overwrite it?'
updated: 2026-10-19 16:32:40.448768
waiting_on: null
waiting_since: null
working_on: false
---

From morning awareness (Slack highlights).
https://canarytechnologies.slack.com/archives/C03V5P4B48P/p1792190561632889?thread_ts=1792190561.632889&cid=C03V5P4B48P