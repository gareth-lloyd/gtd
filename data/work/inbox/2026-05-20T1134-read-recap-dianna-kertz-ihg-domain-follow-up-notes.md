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
output: |
  ## Agent run 2026-05-20T08:49:06Z

  Read Dianna Kertz's May 19 recap of the May 7 IHG discovery meeting on
  hosting the Canary guest experience under an IHG-branded domain.

  **Subject:** "Follow Up Notes & Action Items - Discovery Discussion Hosting
  Canary Experience on IHG domain" (sent 2026-05-19 by dkertz@; To: Monica
  Bryson, Abner Contreras, Armando Barboza-Ojeda, Catherine Carson, Chanda
  Cheung, Daniel Endara, Priyanka Jahr (IHG) + Blake Sullivan, Brendon
  VanLandingham, Caitlyn Levine, Conor Swords, Vidur Sachdeva, Zach Lee,
  Gareth (Canary). Attachment: Custom_Domain_Pre-Setup.pdf.

  ### What was discussed
  Goal: serve Canary's digital check-in/out under an IHG domain to lift
  guest trust (Priyanka cited hotels/owners/tech-committee feedback that
  guests engage more when the experience feels authentically IHG).
  Three options were walked through:
  1. **Subdomain** (e.g. checkin.ihg.com) — Canary's proven enterprise
     pattern. IHG sets CNAME + DCB DNS records, Canary issues SSL and
     white-labels with IHG branding. Already in production at multiple
     major hotel brands.
  2. **API-based** — Canary's mobile-SDK APIs (docs.canarytechnologies.com)
     could in theory power a custom IHG-built front end, but that surface
     has only been used inside the mobile SDK, no customer has built a
     standalone web experience on it, and Canary doesn't recommend or
     support it. No web-facing API docs outside the SDK context.
  3. **Web component / iframe** — IHG's web team raised embedding inside
     www.ihg.com keeping IHG chrome. Canary has no web component / iframe
     offering, and IHG's own discovery flagged iframe security concerns.

  ### Canary's recommendation
  **Subdomain route.** Stated reasons in the email:
  - Solves the trust problem (IHG URL visible in SMS/email and browser bar).
  - Proven and fast: lift is just DNS (CNAME + DCB for SSL); Canary handles
    app setup, branding, ongoing maintenance.
  - Keeps IHG on Canary's product roadmap automatically — every DGX
    improvement reaches IHG guests with zero IHG dev work.
  - Alternatives carry significant risk/cost: API path means IHG owns
    building/testing/maintaining a new front end, re-implementing on every
    Canary release, losing Canary's A/B testing, and gating IHG guests'
    access to new features on IHG's own dev capacity.

  ### Action items (from the email)
  | Owner | Action |
  |---|---|
  | **Caitlyn Levine (Canary)** | Send a sample web experience (SMS or email trigger) to Monica so IHG can see the current branded check-in/out flow firsthand. |
  | **Monica / IHG team** | Share Canary's SDK docs with Abner and Juan for reference. |
  | **Monica / IHG team** | Evaluate the pathways internally; coordinate with DGX stakeholders (Priyanka, Catherine, Chanda) to align on a direction. |

  Dianna offered to set up a deeper technical walkthrough with IHG IT/DNS
  whenever they're ready to move forward.

  ### What this means for me (Gareth)
  - No direct action assigned to me. The next move is on Caitlyn (sample)
    and Monica's team (internal evaluation + DGX alignment).
  - Worth tracking that the recommendation matches what was already
    captured in the "IHG enterprise notes" Bear note (5 May 2026): custom
    subdomain CNAME, 63 customers already live on that pattern. The
    "Custom SDK" misread from earlier IHG threads has now been reframed
    cleanly — API path is explicitly called out as unsupported for web.
  - Watch for: (a) whether IHG accepts the subdomain framing or pushes
    back toward embed/API; (b) whether the engineering side gets pulled
    in for the technical walkthrough with IHG IT/DNS, which would
    likely route through me / Blake.

  No code or external action taken. Status not changed; handing back.
project: null
source_id: https://mail.google.com/mail/u/0/#inbox/19e418e3f5340bf3
tags:
- morning-gtd
- gmail
- from-awareness
time_minutes: 10
title: 'Read recap: Dianna Kertz IHG domain follow-up notes & action items'
updated: 2026-05-20T08:49:06.599469Z
waiting_on: null
waiting_since: null
working_on: false
---

May 7 meeting recap with IHG on hosting Canary experience under IHG-branded domain. Recommends subdomain (checkin.ihg.com). Action items on Caitlyn (sample experience) and IHG team (evaluate pathways). https://mail.google.com/mail/u/0/#inbox/19e418e3f5340bf3