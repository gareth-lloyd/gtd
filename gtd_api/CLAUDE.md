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
  Items expose `order`; projects expose `priority`, `due`, `sequential`
- `CaptureSerializer` — write: title, body, optional energy/time/contexts
- `MoveSerializer` — write: `to` bucket name
- `ItemPatchSerializer` — write: any mutable item field. Fields only appear
  in `validated_data` when the client sent them, so PATCH semantics are clean
- `ProjectCreateSerializer` — write: id, title, body, outcome, area, tags,
  due, priority (1-5), sequential
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
GET    /api/envs/<env>/items/<id>/
PATCH  /api/envs/<env>/items/<id>/
DELETE /api/envs/<env>/items/<id>/               soft delete (→trash)
POST   /api/envs/<env>/items/<id>/move/          {to: "next"}
POST   /api/envs/<env>/items/<id>/complete/      →archive
POST   /api/envs/<env>/items/<id>/purge/         hard delete
GET    /api/envs/<env>/projects/                 ?include_inactive=true
POST   /api/envs/<env>/projects/
GET    /api/envs/<env>/projects/<id>/            includes linked actions (sorted by order)
PATCH  /api/envs/<env>/projects/<id>/
DELETE /api/envs/<env>/projects/<id>/
POST   /api/envs/<env>/projects/<id>/reorder/    {item_ids: [...]} — assigns order 1..N
POST   /api/snapshot/                            {message?, push?}
GET    /api/snapshot/status/
```

### Sequential project filtering

`GET /items/?status=next` automatically hides later-in-sequence items from
projects where `sequential: true`. Only the lowest-`order` incomplete item
per sequential project appears. Pass `?show_all=true` to bypass this (useful
during a weekly review). Non-sequential projects and items without a project
are unaffected.
