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
| `models.py` | `Bucket` enum, `Item`/`Project`/`Template`/`EnvConfig` dataclasses |
| `storage.py` | `dump_item`/`load_item`, `dump_project`/`load_project`, `dump_template`/`load_template`, `load_env_config` |
| `repository.py` | `EnvRepository` — CRUD per env. `list_items()` excludes archive+trash by default |
| `service.py` | `GtdService` — capture, move, update, complete, delete (→trash), purge, filter_items, filter_next, list_items (with `respect_sequential`), projects, `create_project`, `reorder_project_items`, `apply_sequential_hiding` helper, `make_item_id` |
| `snapshot.py` | `snapshot()` stages+commits only `data/` paths. `snapshot_status()` reports dirty count |
| `dates.py` | `parse_human_date()` — accepts ISO strings, natural language ("next friday", "2w", "end of month"), date objects, or None |
| `recurring.py` | `spawn_recurring(repo)` — checks templates, spawns inbox items for due ones. Called before every snapshot |
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

- **Project priority**: `Project.priority` is `Literal[1,2,3,4,5] | None`
  (1 most urgent). `Project.due` is a `date | None`. Neither affects automated
  behavior — they're sorting/visibility aids consumed by the frontend.

- **Sequential projects**: `Project.sequential: bool` + `Item.order: int | None`.
  When a project is sequential, `list_items(..., respect_sequential=True)`
  keeps only the lowest-`order` item per sequential project (ties broken by
  item id). `filter_next()` passes `respect_sequential=True` by default.
  `actions_for_project()` always sorts by `(order, id)` so the project view
  shows its natural sequence. `reorder_project_items(env, project_id, [ids])`
  assigns `order: 1..N` — the API's reorder endpoint wraps this for
  drag-and-drop in the UI.

## Tests

All in `tests/`. Every test creates a tmp data root — no fixture shares
state with real `data/`. Run with `uv run pytest gtd_core/`.
