---
area: null
contexts: []
created: 2026-07-01 01:05:37.435411
defer_until: null
due: null
energy: low
id: 2026-07-01T0105-image-naming-per-ben-email
order: 7
output: |-
  ## Agent run 2026-07-29T14:45

  Captured as **GAP-084 — SEO image naming + alt tags** in the villacollective design todo tier:
  - Ticket: `django_res_design/todo/gap-084-image-seo-naming-alt-tags.md`
  - Index row added to `django_res_design/todo/INDEX.md` (after GAP-083, which another capture claimed earlier today — hence 084, not 083)
  - Both files left **uncommitted** on main for your review (alongside the also-uncommitted GAP-083 capture)

  Ticket contents, grounded in the as-built code:
  - Ask: `{country}-{region}-{villa}-{n}` (e.g. greece-corfu-villa-melissonia-2) for BOTH stored filename and alt tag pushed to WP; motivation is SEO, and per Ben the **alt tag is the higher-value half** (filters into images already on WP without re-import; renamed files need a WP remove-and-reimport, "may or may not be worth the effort").
  - Current state: `PropertyImage` has no `alt_text` field; `upload_to="properties/%Y/%m/"` keeps browser filenames; all ~12.3k legacy images are GUID-named (exactly the res2 behaviour Ben dislikes). Building blocks exist: Property.name + Region.slug + Country via `properties/models/geo.py`.
  - Key gap flagged: **no res3→WP image path exists at all** (WP integration is inbound enquiries only; outbound is Zoho Flow). Ticket is gated on the open question "how do villa images reach WP today?" — needs an ask to Ben/Nick.
  - Sketch: pure slug-derivation function, `alt_text` column with derived default + staff override, rename-on-upload via `upload_to` callable, legacy objects NOT renamed in v1 (S3 copy+delete over 13k objects only if WP re-imports); coordinate with GAP-082 (Zoho villa push) so its payload can carry image URL + alt.

  Suggested next actions (yours to file): ask Ben/Nick how images reach WP today; decide whether GAP-082's villa payload grows an images array.

  Update (user-approved): committed as 8326bb7 on local main (bundled with the parallel GAP-083 capture — shared INDEX.md hunk). Unpushed.
project: 2026-05-25-villa-collective
source_id: null
tags: []
time_minutes: 5
title: 'Capture as gap todo: image naming per ben email'
updated: 2026-07-29 14:45:06.172387
waiting_on: null
waiting_since: null
working_on: false
---

Something we’ve noticed from res 2 is how it’s named/renamed the images after they’ve been uploaded.
Would it be possible to create a naming structure for the images within res 3, both for the file name and the alt tag that pushes through to WP? 
Ideally, piecing together the labels for the villa name, country and region. Potentially something like (greece-corfu-villa-melissonia-2//3/4/5/6). 

Thanks in advance

Ben Wood | mojo media
T - 0208 054 3268 I M - 0791 959 1288
W - www.mojomedia.co.uk | E - ben@mojomedia.co.uk


email-sig.png


Gareth Lloyd <glloyd@gmail.com>
Thu, Jun 25, 2:24 PM
to Ben, Nick

Definitely possible. 

Can you expand a bit more on the motivation? Is it just organization or for referencing images from elsewhere?

Ben - mojo media
Thu, Jun 25, 3:17 PM
to me, Nick

Main focus is SEO, with the images being named to the villa in question, there’s a benefit with organic reach, it’s not a game-changer, but it’s another tick in the box from an SEO perspective, in particular the alt tag part of it as that should filter into the images already loaded onto WP.

Worst case from a naming perspective and getting WP to use the updated filenames we would need to remove and import all the properties images again, which may or may not be worth the effort
Thanks