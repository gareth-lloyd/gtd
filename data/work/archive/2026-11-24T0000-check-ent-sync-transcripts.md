---
area: null
completed_at: 2026-11-24 15:23:43.794307
contexts:
- consume
created: 2026-11-24 00:00:00
defer_until: null
due: null
energy: low
id: 2026-11-24T0000-check-ent-sync-transcripts
order: null
output: |-
  ## Agent run 2026-11-24T15:27+02:00

  Latest ENT sync: Mon 2026-11-23, "ENT Sync Entry" (https://app.notion.com/p/421814686151806f8e1dfe26b8a8d50d). Short standup, 4 speakers, Andrea running it. Read the Notion AI summary and the full transcript. The DB properties (Attendees, Topics, Action Items, Decisions) and the page's Summary / Decisions / Cleaned Transcript sections are all empty — only the AI summary and raw transcript exist.

  ### One thing waiting on you
  - Andrea did a second pass of the cross-region eng design and is waiting on final feedback from you and Jordan Sterling before sharing it with the team. No doc link was given in the meeting. No GTD item covers this yet (the inbox item about Jordan's doc is a different doc).

  ### Action items
  - Andrea: share the cross-region eng design with the team once your and Jordan's feedback is in.
  - Welcome Amenity / country settings engineer (unnamed in transcript): re-check the AutoKey property where reservations are not fetching. Canary side looks fine after re-running fetch reservations and validate TMS; suspected AutoKey-side misconfiguration; Taylor Kirchwehm is asking on her side (came from her question in the deploy channel).
  - Luan: keep testing the ~6 new countries' settings async on staging; a group session gets scheduled for anything needing the team.
  - Get Taylor Kirchwehm's sign-off on how country settings look (no owner stated).

  ### Decisions
  - No formal decisions. Closest: Andrés's original per-channel booking gateway PR will be closed, not merged — the real fix shipped separately using Andrea's design. The ticket stays open until the Wyndham-wide rollout.

  ### Topics
  - Per-channel booking gateway, Wyndham (Andrés): monitoring 5–6 pilot hotels. No production QR booking received yet, so unconfirmed in prod; manual tests with Manu and a couple of hotels passed. Rollout to all Wyndham waits on one real QR reservation.
  - Skimm (Andrés): addressing review comments, no blockers.
  - Wyndham Barclays instant credit (Ryan): UI flow tested end to end — posts into Barclays' environment, application completes, returns to Canary. Barclays' docs have wrong field names; Barclays said to leave it, so Canary code adapts. Ryan mentioned an unspecified remaining issue he is still working out. Related row in the same DB: 2026-11-19 "Wyndham Connect-Barclays Instant Credit (IC) Meeting Series" (https://app.notion.com/41d81468615181479931c813b4b4fd2c), not reviewed here.
  - Triage (Ryan): on triage this week; Andrés took 2 of Ryan's on-call days (Thanksgiving).
  - Welcome Amenity + Catalog PRs (unnamed engineer): self-reviewed, plan is merge to the feature branch and test on staging; now testing locally by running onboarding on a property to mimic an AM test.
  - Country settings (same engineer): staging deploy was blocked by a failing migration, now fixed and deployed.
  - Pre-meeting aside: Ryan has a customer call to set up SSO because the internal ask to collect a few things from them never happened. Customer not named.

  ### Caveats
  - Speakers are unlabelled (A–D). Andrés, Ryan and Andrea are identifiable from context; the fourth is not named (Notion calls them "Third Speaker").
  - Other recent rows not reviewed: 2026-11-16 ENT Sync Entry (https://app.notion.com/41a8146861518063b349d59aa5b7f7e8), 2026-11-16 IHG Loyalty Amenity Sync (https://app.notion.com/41a81468615180fdb8eae1f69026b0c4).
  - This item file was already in archive/ with completed_at set when the run started (not in inbox/ as the launch prompt said). I left it where it was.
project: null
source_id: null
tags: []
time_minutes: 10
title: Check ENT sync transcripts
updated: 2026-11-24 15:24:26.896203
waiting_on: null
waiting_since: null
working_on: false
---

Review the latest ENT sync meeting transcript — action items, decisions, and topics.

https://app.notion.com/p/canarytechnologies/13c93352d06c4e88bb69af559237645c?v=5f62f3dba7234433870e5cfeb927403f&source=copy_link