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

- `ItemSerializer` / `ProjectSerializer` — read-only (`to_representation`)
- `CaptureSerializer` — write: title, body, optional energy/time/contexts
- `MoveSerializer` — write: `to` bucket name
- `ProjectCreateSerializer` — write: id, title, body, outcome, area, tags
- `SnapshotRequestSerializer` — write: optional message, push flag

## Endpoints

```
GET    /api/envs/
GET    /api/envs/<env>/config/
GET    /api/envs/<env>/items/                  ?status=&contexts=&energy=&max_minutes=&project=
POST   /api/envs/<env>/items/                  capture (→inbox)
GET    /api/envs/<env>/items/<id>/
PATCH  /api/envs/<env>/items/<id>/
DELETE /api/envs/<env>/items/<id>/             soft delete (→trash)
POST   /api/envs/<env>/items/<id>/move/        {to: "next"}
POST   /api/envs/<env>/items/<id>/complete/    →archive
POST   /api/envs/<env>/items/<id>/purge/       hard delete
GET    /api/envs/<env>/projects/               ?include_inactive=true
POST   /api/envs/<env>/projects/
GET    /api/envs/<env>/projects/<id>/          includes linked actions
PATCH  /api/envs/<env>/projects/<id>/
DELETE /api/envs/<env>/projects/<id>/
POST   /api/snapshot/                          {message?, push?}
GET    /api/snapshot/status/
```
