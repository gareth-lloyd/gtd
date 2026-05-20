---
area: null
contexts:
- consume
created: 2026-05-20 11:34:33.488935
defer_until: null
due: null
energy: low
id: 2026-05-20T1134-read-recap-dianna-kertz-ihg-domain-follow-up-notes
order: null
output: "## Agent run 2026-05-20T08:49:06Z\n\nRead Dianna Kertz's May 19 recap of
  the May 7 IHG discovery meeting on\nhosting the Canary guest experience under an
  IHG-branded domain.\n\n**Subject:** \"Follow Up Notes & Action Items - Discovery
  Discussion Hosting\nCanary Experience on IHG domain\" (sent 2026-05-19 by dkertz@;
  To: Monica\nBryson, Abner Contreras, Armando Barboza-Ojeda, Catherine Carson, Chanda\nCheung,
  Daniel Endara, Priyanka Jahr (IHG) + Blake Sullivan, Brendon\nVanLandingham, Caitlyn
  Levine, Conor Swords, Vidur Sachdeva, Zach Lee,\nGareth (Canary). Attachment: Custom_Domain_Pre-Setup.pdf.\n\n###
  What was discussed\nGoal: serve Canary's digital check-in/out under an IHG domain
  to lift\nguest trust (Priyanka cited hotels/owners/tech-committee feedback that\nguests
  engage more when the experience feels authentically IHG).\nThree options were walked
  through:\n1. **Subdomain** (e.g. checkin.ihg.com) — Canary's proven enterprise\n
  \  pattern. IHG sets CNAME + DCB DNS records, Canary issues SSL and\n   white-labels
  with IHG branding. Already in production at multiple\n   major hotel brands.\n2.
  **API-based** — Canary's mobile-SDK APIs (docs.canarytechnologies.com)\n   could
  in theory power a custom IHG-built front end, but that surface\n   has only been
  used inside the mobile SDK, no customer has built a\n   standalone web experience
  on it, and Canary doesn't recommend or\n   support it. No web-facing API docs outside
  the SDK context.\n3. **Web component / iframe** — IHG's web team raised embedding
  inside\n   www.ihg.com keeping IHG chrome. Canary has no web component / iframe\n
  \  offering, and IHG's own discovery flagged iframe security concerns.\n\n### Canary's
  recommendation\n**Subdomain route.** Stated reasons in the email:\n- Solves the
  trust problem (IHG URL visible in SMS/email and browser bar).\n- Proven and fast:
  lift is just DNS (CNAME + DCB for SSL); Canary handles\n  app setup, branding, ongoing
  maintenance.\n- Keeps IHG on Canary's product roadmap automatically — every DGX\n
  \ improvement reaches IHG guests with zero IHG dev work.\n- Alternatives carry significant
  risk/cost: API path means IHG owns\n  building/testing/maintaining a new front end,
  re-implementing on every\n  Canary release, losing Canary's A/B testing, and gating
  IHG guests'\n  access to new features on IHG's own dev capacity.\n\n### Action items
  (from the email)\n| Owner | Action |\n|---|---|\n| **Caitlyn Levine (Canary)** |
  Send a sample web experience (SMS or email trigger) to Monica so IHG can see the
  current branded check-in/out flow firsthand. |\n| **Monica / IHG team** | Share
  Canary's SDK docs with Abner and Juan for reference. |\n| **Monica / IHG team**
  | Evaluate the pathways internally; coordinate with DGX stakeholders (Priyanka,
  Catherine, Chanda) to align on a direction. |\n\nDianna offered to set up a deeper
  technical walkthrough with IHG IT/DNS\nwhenever they're ready to move forward.\n\n###
  What this means for me (Gareth)\n- No direct action assigned to me. The next move
  is on Caitlyn (sample)\n  and Monica's team (internal evaluation + DGX alignment).\n-
  Worth tracking that the recommendation matches what was already\n  captured in the
  \"IHG enterprise notes\" Bear note (5 May 2026): custom\n  subdomain CNAME, 63 customers
  already live on that pattern. The\n  \"Custom SDK\" misread from earlier IHG threads
  has now been reframed\n  cleanly — API path is explicitly called out as unsupported
  for web.\n- Watch for: (a) whether IHG accepts the subdomain framing or pushes\n
  \ back toward embed/API; (b) whether the engineering side gets pulled\n  in for
  the technical walkthrough with IHG IT/DNS, which would\n  likely route through me
  / Blake.\n\nNo code or external action taken. Status not changed; handing back.\n"
project: null
source_id: https://mail.google.com/mail/u/0/#inbox/19e418e3f5340bf3
tags:
- morning-gtd
- gmail
- from-awareness
time_minutes: 10
title: 'Read recap: Dianna Kertz IHG domain follow-up notes & action items'
updated: 2026-05-20 14:44:58.826375
waiting_on: null
waiting_since: null
working_on: false
---

May 7 meeting recap with IHG on hosting Canary experience under IHG-branded domain. Recommends subdomain (checkin.ihg.com). Action items on Caitlyn (sample experience) and IHG team (evaluate pathways). https://mail.google.com/mail/u/0/#inbox/19e418e3f5340bf3