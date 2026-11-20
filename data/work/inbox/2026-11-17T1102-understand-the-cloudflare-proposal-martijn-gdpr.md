---
area: null
completed_at: null
contexts: []
created: 2026-11-17 11:02:10.908471
defer_until: 2026-11-23 09:00:00
due: null
energy: low
id: 2026-11-17T1102-understand-the-cloudflare-proposal-martijn-gdpr
order: null
output: |-
  ## Agent run 2026-11-17T13:56

  Sources: Notion design doc "Workbench migration" (https://app.notion.com/p/41a814686151808e97faed27cfc3eeee) and its 8 comment threads; Martijn 1-1s of 17 Nov (https://notes.granola.ai/d/87c0acb6-4ecd-4ec6-8daf-d9360bb5ecf6), 10 Nov (https://notes.granola.ai/d/4827ab5d-ada4-40b7-a438-ae8463471a57), 3 Nov (https://notes.granola.ai/d/516aa837-6953-43f6-a8d7-5a37e6c6412e), 28 Oct (https://notes.granola.ai/d/3b3ba576-f39d-4586-93ae-2d59d11f4349); EMEA standup 9 Nov (https://notes.granola.ai/d/bd66f1eb-b9db-4c5f-bc44-f17ee693774a). Read-only, nothing posted anywhere.

  ### In one paragraph

  The doc is Marta's (author and project owner, created 16 Nov, status TODO), not Martijn's; Martijn is the only commenter so far. It proposes moving Kiosk Workbench off Supabase + Vercel onto Cloudflare (Workers for frontend and backend, Cloudflare Access for sign-in) with Postgres kept on AWS. It is a draft with most decisions open: how the app reaches Postgres, how far to split data by region, and whether Workbench should hold guest PII at all. Knative on Kubernetes, which Martijn described to you this morning as the second path, is not in the doc yet.

  ### Why migrate (doc's reasons)

  - Supabase and Vercel are outside what Platform and Security maintain or monitor.
  - Workbench reaches Canary with one static API key held outside our infrastructure; that key covers all three regions.
  - Guest PII is copied into it: first and last names, plus VCC card holder name, last four and expiry.
  - Data residency: EU and AP hotel guest data sits in one US database.
  - Everything is internet-reachable unless someone locks it; the target is sign-in by default.
  - It should become the template for future services outside the monolith (BirdBrain etc.), which is the framing you and Martijn agreed on 3 Nov.

  ### What Workbench is today

  Vue app on Vercel; the browser queries one Supabase Postgres directly through PostgREST; much business logic lives in database functions and triggers; row-level security on every table; about 3,300 Postgres-only tests; 38 Supabase backend functions (EasyPost, Mailgun, Slack, Stripe, syncs); scheduled jobs copy hotels, reservations, kiosk sessions and VCC records from all three Canary regions. It also runs the global hardware store, used by an external warehouse company.

  ### Decisions in the doc

  1. **Database: D1 vs Postgres.** Marta rules out D1 (SQLite): no RLS, no functions/triggers, no row locking, tests cannot run, PostgREST does not work. The rest of the doc assumes Postgres on AWS.
  2. **Database access: keep PostgREST (A) vs own API on Workers via Hyperdrive (B).**
     - A is least work: self-host PostgREST as a container in a private network, plus a small "bridge" that turns the Cloudflare Access token into one PostgREST accepts. Depends on Platform allowing it.
     - B means roughly 184 frontend queries in 60 files, about 130 new endpoints and 138 backend queries rewritten (Marta's Claude estimate, in the comments). RLS stays, but every endpoint has to tell the database which user it acts for; one that forgets runs without the rules.
  3. **Backend functions to Workers.** Judged modest: only the wrapper changes. Limits to check: 30s after response, 15 min for scheduled/queued, 128 MB, no disk (PDF building).
  4. **Regions.** Store data is global and not divisible. Reservation data must be per region. Options: (A) three separate Workbenches, which changes the product; (B) only reservation data in three regional databases, the cleanest split; (C) hotel data per region too, about 10 frontend places affected.
  5. **Sign-in.** Cloudflare Access (Okta for staff, emailed code for the warehouse) replaces the Supabase login. Needs the bridge, our own user table with the same IDs, and access level decided by email domain instead of sign-in method.
  6. **Rollout.** Build beside Supabase, test on a copy of production, cut over in an announced window. No simple rollback once the store reopens.

  ### The GDPR-relevant parts

  - Cloudflare cannot pin scheduled or queued Workers to a region; request-driven Workers only with Regional Services, an Enterprise add-on; file storage location is guaranteed for EU and US only, not AP. So regional databases alone do not give regional processing.
  - Doc question 2 is the big lever: if Workbench stops copying guest PII, or deletes it after about a month, the regional split is not needed at all. The doc says the PII does not look strictly necessary for the features.
  - Doc question 3: the all-region static API key is a problem the migration does not fix by itself.
  - Doc question 1 asks whether "Platform maintains Cloudflare and AWS" is enough justification alone.

  ### Martijn's position (his doc comments, 16 Nov, plus the 17 Nov 1-1)

  - Against self-hosting PostgREST: "How would we deploy this? EC2? Seems very complex & expensive to run on AWS", and rewriting queries is cheaper than running complex infrastructure. Marta partly agreed, noting the cost is testing, not writing.
  - Wants Knative listed with the reason it is excluded, and a Postgres-on-Aurora column in the D1 table.
  - AWS has only Production and Staging accounts; an internal tool could sit in Staging but that is a bigger security risk. Wants pros/cons expanded.
  - Regional Services "seems like a good investment", wants to raise it with Platform.
  - Suggests Better-Auth instead of a hand-built user table.
  - Adds that Vercel and Supabase have had security incidents (links in the comment thread).
  - In the 1-1 he framed two paths: Workers (cheap, fast, but platform-specific APIs and a rewrite) vs Knative on Kubernetes (already Platform-supported, Postgres-native, easier since the app is just containerised). He leans Workers, as you did: a rewrite behind the Cloudflare firewall beats the same code in a more exposed environment, and since it is internal he told Marta vibe-coding the rewrite is acceptable. Marta is to produce proofs of concept with pros and cons and socialise it across teams; she is in discussion with Platform now.

  ### Gaps I noticed (my reading, not in the doc)

  - The doc and the 1-1 disagree on what the options are: the doc compares Cloudflare+Postgres vs Cloudflare+D1, the 1-1 compared Workers vs Knative. Knative is where residency is easiest (run in-region), so leaving it out weakens the GDPR comparison.
  - Where the AWS Postgres lives is unspecified (which account, Aurora or not, one per region or not). The regional options depend on it.
  - CI test jobs in Workbench are currently switched off (Marta's comment cites a commit "Disable CI test jobs and deploy without the test gate"). Option B's large rewrite with no test gate is the main delivery risk.
  - Dropping or expiring guest PII (question 2) could ship on the current stack before any migration and would remove most of the residency exposure early. This fits your 3 Nov concern that the platform work must not become a reason to delay fixing the existing violation.
  - Ownership: on 3 Nov your view was EMEA coordinates and the Kiosk team does the engineering. Since 9 Nov Marta leads it as an EMEA cycle item (estimated 8), with Elena Brown from Kiosk helping on data migration. The doc does not say who owns Workbench afterwards.
  - Nothing on retention, deletion or erasure requests for the copied data, nor on Supabase/Vercel as sub-processors in the interim.

  ### Timing

  Block planning session is tomorrow, 18 Nov; Martijn plans to raise PII/GDPR sprawl there (example: new OpenSearch store with PMS Gateway data created without obfuscation). This doc is the context for that.
project: null
source_id: null
tags: []
time_minutes: 5
title: understand the cloudflare proposal martijn gdpr
updated: 2026-11-19 15:32:26.896439
waiting_on: null
waiting_since: null
working_on: false
---

https://app.notion.com/p/canarytechnologies/Workbench-migration-41a814686151808e97faed27cfc3eeee?source=copy_link

+ recent granola 1-1 notes