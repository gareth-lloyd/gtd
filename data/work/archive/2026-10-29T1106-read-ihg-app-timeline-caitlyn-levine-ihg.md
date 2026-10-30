---
area: null
completed_at: 2026-10-29 14:37:10.966015
contexts:
- react
created: 2026-10-29 11:06:10.449903
defer_until: null
due: null
energy: low
id: 2026-10-29T1106-read-ihg-app-timeline-caitlyn-levine-ihg
order: null
output: |
  ## Agent run 2026-10-29T13:40
  **The timeline** (from the screenshot Gareth pasted in; Caitlyn's post: https://canarytechnologies.slack.com/archives/C03V5P4B48P/p1793196934524439). You aren't tagged; it went to Luan, a subteam, and Connor.
  | Date | Milestone | Owner |
  |---|---|---|
  | Tue Nov 3 | iOS + Android dev complete (MOB-1364, MOB-1365). Loyalty sends the welcome amenity images by then, so they're in QA | Canary Mobile |
  | Wed Nov 4 – Mon Nov 9 | Internal QA, 4 days: iOS, Android, IHG flavor regression. IHG provides an early branch | Canary QA |
  | Tue Nov 10 | SDK version handed to IHG | Canary Mobile |
  | Wed Nov 11 – Thu Nov 12 | IHG sprint starts; they branch with the new version | IHG app team |
  | ~Fri Nov 12 – Fri Nov 24 | Joint testing, 1 week. IHG's analytics work may land before the branch is released, so we may not get access straight away | Canary + IHG |
  | Nov 25 – Dec 2 | IHG release prep (includes Thanksgiving) | IHG |
  | Thu Dec 3 | Release | IHG |

  Notes:
  - The joint-testing weekdays are wrong for 2026: Nov 12 is a Thursday and Nov 24 is a Tuesday; the Fridays are Nov 13 and Nov 27. The span is also about 12 days, not "1 week". Worth asking Caitlyn which end is right. It matters because the Dec 3 date depends on testing finishing, and Caitlyn's Dec ~20 fallback applies if testing overruns.
  - Canary has no backend milestone on the chart. All the work is in Mobile/QA. The only outside dependency before QA is Loyalty's images by Nov 3.
  - Release is Dec 3, the same as Caitlyn's in-app target in the mobile check-in thread below.
  Thread: Luan said "That sounds good to me"; Dianna cc'd Conor G for his weekly update slides. No questions or asks.

  **Context from the related thread you started** (https://canarytechnologies.slack.com/archives/C03V5P4B48P/p1791457530248069), about mobile check-in messages:
  - Caitlyn (https://canarytechnologies.slack.com/archives/C03V5P4B48P/p1793210520419289?thread_ts=1791457530.248069&cid=C03V5P4B48P): IHG will wait for the separate **Welcome Amenity step** before rolling the app out at scale. In-app target: **Dec 3**, or about **Dec 20** if IHG's testing runs past the planned sprint. The plan is to move all IHG GMS hotels onto the app after that.
  - Taylor proposed, and Caitlyn agreed: before full rollout, only **5 or fewer properties** get the 2-CTA check-in message (switched over by hand). All others stay on standard check-in messaging, so there's no need to run several GJ templates or a per-hotel indicator.
  - Open: Caitlyn asked Taylor whether he's telling IHG. Taylor hasn't been in the mobile-launch talks. He says IHG doesn't realise the app is controlled by the same Canary dashboard settings. Your questions there (who runs the mobile rollout, onboarding values) didn't get a clear owner. Caitlyn said IHG decides which hotels get mobile; Chanda tracks it in a spreadsheet; Connor wants IHG to own it and send it in the property file.
  - Welcome Amenity designs were signed off on 10/21. Copy changes go in via ENT config scripts (Caitlyn's 10/21 post to David Champeil/vibhor in #ihg; I didn't get its permalink).

  Nothing needed from you unless you want to chase who owns the mobile rollout.
project: null
source_id: https://canarytechnologies.slack.com/archives/C03V5P4B48P/p1793196934524439?thread_ts=1793196934.524439&cid=C03V5P4B48P
tags:
- morning-gtd
- slack
- from-awareness
time_minutes: 10
title: 'Read: IHG app timeline (Caitlyn Levine, #ihg)'
updated: 2026-10-29 14:45:00
waiting_on: null
waiting_since: null
working_on: false
---

Caitlyn shared the IHG app timeline for the next few weeks in #ihg.
https://canarytechnologies.slack.com/archives/C03V5P4B48P/p1793196934524439?thread_ts=1793196934.524439&cid=C03V5P4B48P