# gtd_api

Thin DRF translation layer. No domain logic lives here.

## Rule

If a view method does more than **parse request → call GtdService → serialize
response**, the logic belongs in `gtd_core/service.py`, not here.

## Pattern

Function-based views with `@api_view`, not ViewSets. Each view:
1. Calls `_service()` to get a `GtdService` instance (bound to `settings.GTD_DATA_ROOT`)
2. Validates input via a DRF `Serializer` (for writes)
3. Calls the appropriate service method
4. Returns `Response` with serialized output or error dict + status code

Errors from the service layer (`ValueError`, `KeyError`) are caught and
translated to 400/404 responses. The frontend's global `MutationCache.onError`
handler surfaces these as toast notifications automatically.

## Serializers

- `ItemSerializer` / `ProjectSerializer` — read-only (`to_representation`).
  Items expose `order`; projects expose `priority`, `due`, `max_next_items`
- `CaptureSerializer` — write: title, body, optional energy/time/contexts
- `CaptureAiSerializer` — write: `text` (unstructured input for AI extraction)
- `MoveSerializer` — write: `to` bucket name
- `ItemPatchSerializer` — write: any mutable item field. Fields only appear
  in `validated_data` when the client sent them, so PATCH semantics are clean
- `ProjectCreateSerializer` — write: id, title, body, outcome, area, tags,
  due, priority (1-5), max_next_items (int ≥ 1 or null), working_dir
- `ProjectPatchSerializer` — write: same field set as Create minus id
- `ProjectReorderSerializer` — write: `item_ids: list[str]`
- `SnapshotRequestSerializer` — write: optional message, push flag

All PATCH endpoints go through a serializer — raw `request.data` is never
passed to `setattr`. Unknown fields are silently dropped.

## Endpoints

```
GET    /api/envs/
GET    /api/envs/<env>/config/
GET    /api/envs/<env>/items/                    ?status=&contexts=&energy=&max_minutes=&project=&show_all=
POST   /api/envs/<env>/items/                    capture (→inbox)
POST   /api/envs/<env>/items/capture-ai/        AI capture (→inbox or →next+project)
GET    /api/envs/<env>/items/done/               ?page=1&page_size=50 — paginated archive+trash
GET    /api/envs/<env>/items/<id>/
PATCH  /api/envs/<env>/items/<id>/
DELETE /api/envs/<env>/items/<id>/               soft delete (→trash)
POST   /api/envs/<env>/items/<id>/move/          {to: "next"}
POST   /api/envs/<env>/items/<id>/complete/      →archive
POST   /api/envs/<env>/items/<id>/purge/         hard delete
GET    /api/envs/<env>/projects/                 ?include_inactive=true
POST   /api/envs/<env>/projects/
GET    /api/envs/<env>/projects/<id>/            ?include_deferred= — actions hide deferred items by default
PATCH  /api/envs/<env>/projects/<id>/
DELETE /api/envs/<env>/projects/<id>/
POST   /api/envs/<env>/projects/<id>/reorder/    {item_ids: [...]} — assigns order 1..N
GET    /api/envs/<env>/templates/                recurring templates list
POST   /api/snapshot/                            {message?, push?}
GET    /api/snapshot/status/
```

### Next-actions cap per project

`GET /items/?status=next` automatically caps each project's visible items
to `max_next_items` (when set). `max_next_items: 1` reproduces the classic
"sequential" behaviour — only the lowest-`order` incomplete item surfaces.
Higher values (e.g. `3`) surface the N lowest-`order` items. `null`
(default) means no cap. Pass `?show_all=true` to bypass capping entirely
(useful during a weekly review). Projects without a cap and items without
a project are unaffected.
