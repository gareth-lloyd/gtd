---
area: engineering
completed_at: 2026-11-04 20:02:37.063884
contexts:
- deep
created: 2026-11-04 19:21:56.197984
defer_until: null
due: null
energy: high
id: 2026-11-04T1921-claude-made-that-discovery-so-easy-just-then-worth
order: null
output: |
  ## Agent run 2026-11-04T19:43:00+02:00

  Done: ranked the slow dashboard routes from Groundcover, broke each down by component from production spans, traced every repeated query to code (file:line), drafted the #engineering post. NOT posted to Slack: draft is at /private/tmp/claude-501/-Users-garethlloyd-projects-canary/cb5a6146-a46a-4c02-b154-504274a2a4fb/scratchpad/slack_draft.md and needs your yes (suggest replying in the discovery thread https://canarytechnologies.slack.com/archives/C019TQLQDJP/p1793811389605919?thread_ts=1793808707.680909&cid=C019TQLQDJP). Full notes: scratchpad/groundcover_notes.md and scratchpad/code_findings.md (same dir).

  ### Method
  - Groundcover eBPF APM collapses routes to wildcards (GET /api/*/*), so route-level numbers come from Datadog `django.request` spans (`source:Datadog`, `http_route`), queried in six 3h business-hours windows (Oct 21, 23, 28, 30, Nov 3, 4, 16-19 UTC); traces must be queried in <=3h chunks so this is a sample, not a 2-week aggregate. Rankings were stable across all six windows.
  - Per-route component breakdown: child spans joined by `trace_id:in(...)`, grouped by span type and by the SQL text in the `resource` field, giving queries-per-request and the exact repeated statements.
  - Code tracing by six read-only Explore agents given the SQL evidence; I spot-checked every headline file:line.

  ### First-render blocking calls (from frontend/hotels/src App.vue `isReady` + hotelStore.initialize)
  Only four requests gate the route render: `/api/users/me` p50 0.14s, `/api/hotels/{slug}` p50 0.5s p95 1.4s (8s on device-heavy hotels), `/api/companies/{slug}` 0.05s, `/api/users?hotel=` 0.13s (p95 0.8s). `hotels/{slug}` is the only slow one; PR #63267 (https://github.com/canary-technologies-corp/canary/pull/63267) removes hotel_devices from the payload. `chat/threads` and `unread_counts` do not block (confirmed in code: Sidebar2/useNavBadges mount after isReady; nothing awaits them).

  ### Findings table (p50/p95 from the six windows; SQL/req from spans)
  | # | Endpoint | p50 / p95 | req/3h | SQL/req | Where the time goes | The mistake (file:line) | Fix |
  |---|---|---|---|---|---|---|---|
  | 1 | GET /api/chat/threads | 1.1-1.5s / 3.8-5.3s | 4000-5600 | 167 (1.0s DB) + 50 redis + ~0.8s Python | guest by id x23, check_in x14, check_out x14, phone x13, outbound_sms x20, assignment x9, membership x7, SELECT 1 x19 | chat/services/thread.py:329-336 `find_conversation_reservation` and :228-233 `find_sender_guest` fallback run a fresh `Reservation.objects.filter(primary_guest__in=...)` per thread, discarding the reservations already prefetched on each guest by `with_active_guests_queryset` (:1457-1468) with check_in/check_out/phone/assignment/membership; chat/schemas/message_schema.py:172-173 `.exists()`+`.last()` on outbound_smss per last message; threads.py:290-294 Prefetch("messages") loads every message of every thread on the page | rank prefetched `g.get_reservation()` in Python (get_active_reservation already takes a list, guest/services/reservation.py:1739); Prefetch outbound_smss to_attr; select_related last_message__message_feedback |
  | 2 | GET /api/chat/search | 1.2-3.3s / 39-75s | ~190 | 15, but one statement = 12.5s avg | single UNION query | chat/services/search.py:137-390: OR of tsquery + leading-wildcard LIKE (`__contains` on phone columns :227-232) across six LEFT JOINed tables, isnull-OR hotel filters :208-217, UNION (not ALL) :363-371 with a guest branch that scans every reservation at the hotel :312-351, DISTINCT ON :277-293 + ORDER BY before LIMIT 11; docstring :147-205 already admits it | resolve matching guest/thread ids per table with indexed queries (guest GIN, confirmation number exact, check_in GIN, phone digits exact), then fetch by id |
  | 3 | GET /api/contracts | 2.1-2.7s / 5.8-8.7s | ~75 | 377 (2.2s DB) + 59 jinja compiles | ~29 queries per contract | contracts/models/contract_models_search_combiner.py:61-65 refetches `Contract.objects.filter(url__in=...)` with only `prefetch_related("authform")`, discarding the view's annotated qs (api_views.py:682-726); ContractSelector methods build fresh querysets (contract_selector.py:248-286); `_make_contract_link_email` (contracts/schemas/contract.py:224-256) called twice per contract and compiles 2 templates each via `from_string` with no cache (shared/utilities/utilities.py:103-117); `get_guest_facing_domain` per contract and per signer (contract_selector.py:73-74,166). Bonus bug: api_views.py:691 `Count("signers")` lacks `filter=Q(signers__deleted_at=None)` unlike :683-697, so contracts with a soft-deleted signer never satisfy signed==count and the completed/countersigned/pending folder (:529,541,575-582) and SIGNATURE_DUE/PAYMENT_DUE/COMPLETED workflow (:612,621,631) filters misclassify them | eager-load in the combiner (select_related hotel__authorization_configuration, created_by, hellosign_contract; Prefetch signers/operation_logs/internal_notes); read prefetched signers in schema/selectors; compute link email once; lru_cache compiled templates; add the deleted filter |
  | 4 | GET /api/ticket_gateway/recommended_tickets | 0.5-1.4s / 6.8-21s | ~55 | 890 (3.3s DB) | alice_facility x1070, alice_service_request x535, facility_service x535, hotsos x300 each, knowcross x300 each | ticket_gateway/services/recommended_ticket_service.py:87 unbounded (no status filter, no limit; approved/auto-created rows never soft-delete); GenericForeignKey resolved per row via DynamicSchemaField (recommended_ticket_schema.py:53-69, canary/fields/dynamic_schema_field.py:23-37); ticket_gateway/alice/schemas/alice_facility_service_schema.py:55 and :68 `AliceFacility.objects.get` twice per row; knowcross_call_description_schema.py:37-45 category lookup by external_id per row | filter created_ticket__isnull=True + limit; `GenericPrefetch("vendor_ticket", [...select_related per vendor])` (Django 5.2); `obj.facility`; bulk category map |
  | 5 | GET /api/hotels/{slug}/wallets | 0.82-1.01s / 3.0-3.9s | ~60 | 215 (1.07s DB) | per wallet: hotelslug+hotel x26, tips_configuration x25, wallettermsaccept x25, payouts_configuration x25, hotelwalletprofile-by-wallet x25, hotel IN x25, SELECT 1 x53 | WalletProfileSchema.payout_vendor (wallets/schemas/wallet_profile.py:30,42) -> tips/selectors/tips.py:472-474 `wallet.hotelwalletprofile_set.prefetch_related("hotel").order_by("hotel__created_at").first()` (prefetch on a forward FK = extra IN query) -> :463 `get_config_by_hotel_slug(hotel.slug_name)` re-fetches the Hotel it was handed via hotels/selectors/hotel.py:48 -> :69 tips_configuration (:66 `@no_readonly_database`, goes to the writer) -> :464 payout_config lazy FK; has_completed_setup -> wallets/selectors/wallet.py:97 `wallet_terms_accepts.latest()` ignores prefetch | Subquery annotations on the main qs (wallets/services/wallet.py:845-883): payout vendor via hotel__tip_configuration__payout_config__vendor, latest terms kind; smaller: tips.py:463 `Configuration.objects.select_related("payout_config").get(hotel=hotel)` |
  | 6 | GET /api/hotels/{slug}/departments | 0.16-0.20s / 2.2-2.8s | 800-1300 | 105 (0.43s DB) | same chain per staff member x10 + shortlink x14 | same as 5 via hotels/schemas/department.py:39-47 staff qs; hotels/selectors/department.py:30 and schemas/department.py:46 lack tip_link__short_link | share one annotated selector with wallets; select_related tip_link__short_link |
  | 7 | GET /api/authorizations | 0.31-0.41s / 1.8-2.1s | ~1000 | 76 (0.69s DB) | COUNT(*) over UNION 1.4s (search) / 2.2s (no search); page query 0.6s; per row latest attempt x12, companyhoteluser exists x12, payment method+card+stripe x4 | authorization/views/api_views.py:426-427 stock `Paginator` over `AuthorizationCombiner` -> `__len__` :971-972 `auth_data.count()` over the union (:957-969) just for num_pages (frontend uses total: Authorizations.vue:381,639); authorization_dashboard.py:244 `get_ach_process_status` -> authform/services/form.py:1858-1887 latest attempt + full payment method fetch even for card auths; :188 `is_conferma_authorization` -> vendor_service.py:24-40 CompanyHotelUser exists per row | limit+1 / has_next with cached or approximate total; batch latest attempts (Subquery) like charged_payments :83-92; skip PM fetch unless ACH; one Conferma-user query per page |
  | 8 | GET /api/hotels/{slug}/check_ins/search | 0.35-0.41s / 6.5-11s | ~100 | 63 (2.9s DB) | COUNT(*) with tsquery 3.5s avg; page 0.2s; per row configs/bookingintent/purchaseorder/phone | check_in/views/check_in_dashboard.py:400 explicit `check_ins.count()` (frontend shows "N results", CheckInSearch.vue:191; hasNext derived from total, PagePaginationManager.ts:92-96); :382 only `select_related("check_in_action")`, skipping the relations/annotations block the sibling CheckInDashboardView sets up at :159-199 for the same schema (schema comment at check_in_dashboard.py:125 claims the view prefetches) | shared relations helper applied to the page slice; limit+1 or capped count; point check_in.hotel at the loaded hotel |
  | 9 | GET /api/chat/messages | 0.26-0.34s / 1.9-2.4s | 1600-2900 | 61 (0.54s DB) | main query 0.19s on its own; aimessagedraft x10, outbound_sms x14, auth_user x4, userprofile x4 | chat/services/thread.py:870-888 select_related includes `thread__hotel__chat_configuration` (hundreds of identical columns x26 rows) + 10 notification FKs but not `user`, `sent_ai_draft`, `message_feedback`; message_schema.py:294-296 reverse 1:1 sent_ai_draft per row; :167-173 outbound_smss exists+last; chat_user.py photo_url -> user.userprofile | drop the hotel/config join (set m.thread = thread); add select_related sent_ai_draft, message_feedback, user__userprofile; Prefetch outbound_smss to_attr |
  | 10 | cross-cutting SELECT 1 | - | - | 20-50/req on threads/wallets (12k per 20 min on threads alone) | connection health checks | canary/utilities/readonly_database.py:40-41 `close_if_unusable_or_obsolete()` on every `@readonly_database` entry; Django 5.2 resets health_check_done there and CONN_HEALTH_CHECKS=True (settings/base.py:457) forces SELECT 1 before the next query; nested decorators on per-row selectors (e.g. guest/selectors/guest.py:45, tips.py:460/59, hotel.py:118/45) | skip the close call when already inside a readonly context (prev_value == db_override) |

  ### Not ORM (PMS latency), excluded from the table
  - `GET /api/hotels/{slug}/gateway-reservations` p50 2.9-3.3s: guest/views/gateway_reservations_view.py:72 `search_reservation_from_gateway` (gateway GET /reservations/ 2.7s median).
  - `GET /api/reservations/{uuid}?refresh` p50 2.4-3.4s: guest/views/reservations_view.py:222-230 gateway refresh (single-reservation fetch 6-25s).
  - `GET /api/hotels/{slug}/reservations/{uuid}?resync` p95 4.3-5.9s on ~45% of requests: reservation_details_view.py:198-207.
  - `e_folio` p50 0.7-1.0s: gateway folio fetch. `chat/messages/translate` p50 1.5-1.9s: external translation. `purchase_orders/{uuid}` PATCH 1.4-2.0s: outbound + fanout + email.
  - `threads/{id}` is mostly PATCH (1.24s, FanoutPublish 0.33s/req); GET is 0.22s.

  ### Soft-delete findings (beyond the table)
  - contracts api_views.py:691 Count("signers") bug above (functional, not just perf).
  - chat/threads prefetches tickets/recommended_tickets via related managers on soft-delete models (threads.py:295-297), filtered in Python later; CheckOut is SoftDeleteModel without base_manager_name so `reservation.check_out` can return a deleted checkout.
  - recommended_tickets: forward FK/GFK lookups bypass the alive-only manager while explicit `.objects.get` filters alive; inconsistent.

  ### Caveats
  - Per-row attributions are from reading code against production span data; nothing was executed. Each fix PR needs a query-count assertion.
  - p50/p95 are per-window, not a true 2-week aggregate.
  - Three subagent-flagged items I did not verify: GenericPrefetch soft-delete semantics; whether the Upper(email) indexes lack text_pattern_ops; exact SELECT 1 attribution.

  ### Links
  - Discovery thread: https://canarytechnologies.slack.com/archives/C019TQLQDJP/p1793811389605919?thread_ts=1793808707.680909&cid=C019TQLQDJP
  - DM with Andy: https://canarytechnologies.slack.com/archives/D04NZUZN1H8/p1793812625020609?thread_ts=1793812417.946739&cid=D04NZUZN1H8
  - hotels/{slug} fix: https://github.com/canary-technologies-corp/canary/pull/63267
project: null
source_id: null
tags: []
time_minutes: 120
title: Profile the top ~10 slowest dashboard API endpoints with Claude, same as the
  hotel_devices N+1 discovery
updated: 2026-11-04 20:02:37.063879
waiting_on: null
waiting_since: null
working_on: false
---

## Next action
Pull the top ~10 slowest dashboard-blocking API endpoints from Groundcover (p50 and p95 by route, last 2 weeks), then run the same Claude profiling pass on each that found the `hotel_devices` N+1 in `serialize_hotel`: trace where the time goes per component, name the ORM mistake, and post a per-endpoint findings table to #engineering.

## Why
On 2026-11-04 sj asked in #engineering why the dashboard takes 10s to load. Andy said the first-page-load API requests are known-slow but risky to change; I asked whether to give someone a week to JFDI, sj said yes ("can you JFDI please").

Claude found the `/api/hotels/{slug}` cause in ~30 min: `HotelDeviceSchema` does two queries per device (no `select_related` on `kiosk_details` / `device_placement`) and the related manager includes soft-deleted devices (806 rows on canary-test-hotel, 795 on statler, 357 on bowie-house). PR for that is incoming.

Andy: "I wish we could somehow have `knip` but for our whole stack!" I suggested repeating the same discovery process on the worst endpoints; Andy agreed it's a good idea.

## Known candidates from the thread
- `/api/.../threads` — consistently slow at the median, not blocking (Mati, Dmitry)
- unread-count endpoint — ~500ms on statler, not blocking (Mati)
- `/api/hotels/{slug}` — in flight already

## Links
- Discovery thread (#engineering): https://canarytechnologies.slack.com/archives/C019TQLQDJP/p1793811389605919?thread_ts=1793808707.680909&cid=C019TQLQDJP
- DM with Andy where idea was floated: https://canarytechnologies.slack.com/archives/D04NZUZN1H8/p1793812625020609?thread_ts=1793812417.946739&cid=D04NZUZN1H8