# gtd_core

Standalone Python domain library. Zero Django/HTTP knowledge. Importable from
scripts, notebooks, and CLI sessions.

## Layer stack

```
service.py      High-level operations (capture, move, filter, projects)
    ↓
repository.py   Per-environment CRUD (list/get/save/move/delete)
    ↓
storage.py      Raw file IO (frontmatter serialize/deserialize)
```

The API layer (`gtd_api`) only talks to `GtdService`. Never skip layers.

## Key files

| File | Purpose |
|------|---------|
| `models.py` | `Bucket` enum, `Item`/`Project`/`EnvConfig` dataclasses |
| `storage.py` | `dump_item`/`load_item`, `dump_project`/`load_project`, `load_env_config` |
| `repository.py` | `EnvRepository` — CRUD per env. `list_items()` excludes archive+trash by default |
| `service.py` | `GtdService` — capture, move, update, complete, delete (→trash), purge, filter_items, filter_next, projects |
| `snapshot.py` | `snapshot()` stages+commits only `data/` paths. `snapshot_status()` reports dirty count |
| `importer_nirvana.py` | CSV import from Nirvana GTD app. Case-insensitive context matching |

## Conventions

- **Status not in frontmatter**: `load_item(path, bucket)` receives bucket
  as an argument. `dump_item()` never writes a `status:` key.

- **Injectable clock**: `GtdService(root, now=lambda: fixed_datetime)` for
  deterministic tests. Production uses `datetime.now`.

- **Collision-safe IDs**: `YYYY-MM-DDTHHMM-slug` with `-N` suffix on
  collision. See `service.slugify()` and `importer_nirvana.gen_id()`.

- **Validation at service layer**: contexts checked against `config.yml`,
  immutable fields (`id`, `created`) rejected in patches, status changes
  only via `move()`.

## Tests

All in `tests/`. Every test creates a tmp data root — no fixture shares
state with real `data/`. Run with `uv run pytest gtd_core/`.
