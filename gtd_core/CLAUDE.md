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
| `service.py` | `GtdService` — capture, capture_ai, move, update, complete, delete (→trash), purge, filter_items, filter_next, list_items (with `respect_next_cap`), projects, `create_project`, `reorder_project_items`, `find_project_by_title` (fuzzy match), `apply_next_item_cap` helper, `make_item_id`, `AiCaptureOutcome` dataclass |
| `ai.py` | AI capture via `claude` CLI subprocess. Builds a prompt with today's date, valid contexts/areas, project catalogue + recent actions. Parses JSON response into `AiCaptureResult`. No Anthropic API key needed — uses the user's Max plan via the CLI. |
| `snapshot.py` | `snapshot()` stages+commits only `data/` paths. `snapshot_status()` reports dirty count |
| `dates.py` | `parse_human_date()` (date granularity) and `parse_human_datetime()` (datetime granularity, used for `defer_until`) — accept ISO strings, natural language ("next friday", "2w", "end of month", "in 2 hours", "3h"), date/datetime objects, or None |
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

- **Next-actions cap**: `Project.max_next_items: int | None` + `Item.order: int | None`.
  When the cap is set, `list_items(..., respect_next_cap=True)` keeps only
  the N lowest-`order` items per capped project (ties broken by item id).
  `max_next_items=1` is the classic "one step at a time" sequential mode;
  `None` means no cap. `filter_next()` passes `respect_next_cap=True` by
  default. `actions_for_project()` always sorts by `(order, id)` so the
  project view shows its natural sequence. `reorder_project_items(env,
  project_id, [ids])` assigns `order: 1..N` — the API's reorder endpoint
  wraps this for drag-and-drop in the UI.

## Tests

All in `tests/`. Every test creates a tmp data root — no fixture shares
state with real `data/`. Run with `uv run pytest gtd_core/`.
