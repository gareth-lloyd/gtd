# frontend

Vite + React 18 + TypeScript SPA. TanStack Query for server state.

## Key files

| File                    | Purpose                                                                                                                                                                                                                 |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `api.ts`                | Typed fetch client. All API calls go through `request<T>()`. Types for Item, Project, EnvConfig, etc.                                                                                                                   |
| `App.tsx`               | Route table + `AppShell` layout. Owns top-level keyboard shortcuts (`C`, `Shift+C`, `A`, `/`).                                                                                                                          |
| `CaptureBar.tsx`        | Capture overlay with `Regular` / `Regular ↑` / `AI ✦` mode toggle. Exports `CaptureMode` and `isEditableTarget`.                                                                                                        |
| `ItemCard.tsx`          | Dual-purpose item card (collapsed chips / expanded inline editors). Replaces the old `ItemRow` + `ItemEditor`.                                                                                                          |
| `ItemList.tsx`          | Bucket list views (NextActionsView, etc). Wires filters and pagination, drives `<ItemCard>`.                                                                                                                            |
| `ItemEdit.tsx`          | `useItemPatch` (debounced PATCH with optimistic cache updates), `ChipToggleGroup`, `DatePickerRow` (date-only), `DateTimePickerRow` (datetime — used for `defer_until`), `isScheduled`, `invalidateItemQueries` helper. |
| `DetailPanel.tsx`       | Right-side detail pane bound to selection/hover. Renders the full editor for the active item.                                                                                                                           |
| `WorkflowActions.tsx`   | Move / complete / delete buttons shared across card and detail pane.                                                                                                                                                    |
| `FilterPanel.tsx`       | Aside filter UI for `/next` — contexts, energy, time bands, no-project, overdue. Reads/writes via `useNextFilters()`.                                                                                                   |
| `ProjectComponents.tsx` | Projects list, project detail, `SortableActionList` (DnD), `ProjectBadges`.                                                                                                                                             |
| `TemplatesView.tsx`     | Read-only list of recurring templates from `GET /api/envs/<env>/templates/`.                                                                                                                                            |
| `SearchComponents.tsx`  | Header `SearchBar` dropdown + full search page. Routes `/:env/search` and `/:env/items/:itemId`.                                                                                                                        |
| `SelectionContext.tsx`  | React context for selected/hovered item id, used to drive `DetailPanel`.                                                                                                                                                |
| `useEnvParam.ts`        | Tiny hook reading `:env` from the URL — components never receive `env` as a prop at the route level.                                                                                                                    |
| `format.ts`             | Shared utilities: `fmtDate`, `sortProjects`, `slugify`, `generateProjectId`.                                                                                                                                            |
| `filters.ts`            | `useNextFilters()` — query-param-backed filter state for `/next`.                                                                                                                                                       |
| `search.ts`             | `useSearchIndex(env)` — MiniSearch index over the full corpus.                                                                                                                                                          |
| `context-colors.ts`     | Deterministic context→hue mapping (djb2 hash) and `contextChipStyle` helper.                                                                                                                                            |
| `Button.tsx`            | `<Button busy={mut.isPending}>` — spinner overlay, auto-disable. Use for every mutation-backed button.                                                                                                                  |
| `toast.tsx`             | Module-level `ToastStore` (callable outside React). `<Toaster />` subscribes to it.                                                                                                                                     |
| `main.tsx`              | React entry. `BrowserRouter` + `QueryClient` with `MutationCache.onError` → auto-toast.                                                                                                                                 |
| `test-setup.ts`         | Vitest setup — registers `@testing-library/jest-dom` matchers.                                                                                                                                                          |
| `styles.css`            | Vanilla CSS with custom properties. No Tailwind.                                                                                                                                                                        |

## Patterns

**Error handling**: global. `MutationCache.onError` and `QueryCache.onError`
in `main.tsx` call `toasts.show('error', ...)`. No per-component error state
needed.

**Loading state**: per-button via `<Button busy={mut.isPending}>`. For shared
mutations (e.g. moveMut drives → next / → waiting / → someday), use
`mut.variables === targetBucket` to show spinner only on the clicked button.
Disable siblings via a `rowBusy` flag.

**Inline editing**: `ItemCard` replaces the old `ItemRow` + `ItemEditor`.
Collapsed state shows metadata as chips with workflow actions on hover.
Clicking a card expands it: chip-toggle groups for project/contexts/energy/
time/area, date quick-pickers, borderless title input, notes textarea.
All edits auto-save via `useItemPatch` (debounced PATCH, optimistic cache
updates, rollback on error). `Cmd/Ctrl+Enter` flushes and collapses.
At most one card expanded at a time (accordion). Projects query is lifted
to the list level so 100-item lists share one subscription.

**AI capture**: `CaptureBar` has a `Regular | AI ✦` mode toggle (keyboard
`C` / `A`). AI mode sends unstructured text to `POST /items/capture-ai/`;
the backend shells out to the `claude` CLI. On success a summary toast
fires. Items with a matched project auto-move to next.

**State**: TanStack Query for all server state. URL (path + query params)
for navigation and filters — see Routing below. Local `useState` for
transient UI only (expanded card, capture form toggle).
`localStorage` mirrors the current env so `/` can redirect on next visit.

## Routing

`react-router-dom` v6 (`BrowserRouter`). URL is the source of truth for
section, env, project detail, and filters.

```
/                              → redirects to /<last-env>/inbox
/:env                          → redirects to /:env/inbox
/:env/inbox
/:env/next?contexts=calls,computer&energy=low&max_minutes=15
/:env/waiting | /someday | /reference | /trash
/:env/projects
/:env/projects/:projectId
```

- `App` declares the route table; `AppShell` is the layout (header, nav,
  filters aside, `<Outlet/>`). Nav uses `<NavLink>` — `isActive` handles
  the highlight automatically.
- `useEnvParam()` reads `:env` from the URL; components never receive
  `env` as a prop at the route level (they still drill it into children
  that need it, e.g. `ItemCard`).
- `useNextFilters()` (in `filters.ts`) exposes `{contexts, energy,
maxMinutes}` + setters, backed by `useSearchParams`. Setters use
  `{ replace: true }` so filter toggles don't spam browser history.
  Empty values are dropped from the URL.
- Filters only render on `/:env/next` (detected via `useMatch`). The
  URL query keeps them but other sections don't read them.
- Tests: `renderApp()` wraps `<App/>` in `<MemoryRouter initialEntries=
{['/work/next']}>`.

## Search

`react-router-dom` routes: `/:env/search?q=…` (full results) and
`/:env/items/:itemId` (single-item view). Header `<SearchBar/>` renders
a live dropdown with top 8 hits; `/` shortcut focuses it (skipped when
typing in an input). Enter on the input (or clicking "See all N") goes
to the full search page.

Index is built client-side with `minisearch`. `useSearchIndex(env)` in
`search.ts` fetches the corpus via `api.listSearchCorpus(env)`
(`include_archive=true&include_trash=true` + inactive projects). Index
is memoised on the raw data and shared across dropdown + search page
via TanStack Query (60 s staleTime, `['search-corpus', env]` key).
Fields/boosts and the `prefix:true, fuzzy:0.15, combineWith:'AND'`
search options live in `search.ts` — adjust ranking there.

## Drag-and-drop

`@dnd-kit/core` + `@dnd-kit/sortable` for project action reordering. Only
`SortableActionList` (used inside `ProjectDetailView`) mounts the DnD
context — the main next-actions list is plain. Pointer sensor has a 5px
activation distance so clicking the handle doesn't accidentally start a
drag. Drop is optimistic: `localOrder` overrides `items` immediately, then
`api.reorderProjectItems` syncs; on error we drop the override and rely on
the global toast.

## Project priority colors

P1 red, P2 orange, P3 yellow, P4 blue, P5 gray. Classes are
`.priority-badge.p1` … `.priority-badge.p5` in `styles.css`.
`.sequential-badge` (purple) marks projects with a `max_next_items` cap
set. Projects sort by `(priority ?? 99, due, title)` in `ProjectsView`.

## Build

```sh
npm run build    # tsc + vite build → dist/
npm run dev      # vite dev server on :5173, proxies /api to :8000
```

`dist/` is served by Django via WhiteNoise at `/static/`. Vite `base` is
`/static/` so built assets reference `/static/assets/...`.

## Lint / format

Configured in `eslint.config.js` (flat config) and `.prettierrc.json`.
ESLint uses the established React Hooks rules (`rules-of-hooks`,
`exhaustive-deps`) plus typescript-eslint recommended. The newer v7
"react-compiler-friendly" rules are deliberately not enabled.

```sh
npm run lint        # eslint --max-warnings=0 (cached)
npm run lint:fix    # eslint --fix
npm run format      # prettier --write
npm run format:check
npm run typecheck   # tsc --noEmit
```

The repo-root `./scripts/lint.sh` runs all of these plus the Python
equivalents in fail-fast order. Both fire automatically via
`pre-commit` on `git commit`.

## E2E (Playwright)

`e2e/*.spec.ts` — Playwright specs. `playwright.config.ts` runs a
throwaway Django server against `e2e/.tmp/data/` (globalSetup seeds
`config.yml` + bucket dirs, the auto `autoReset` fixture in
`fixtures.ts` wipes item files before every test).

AI capture is stubbed via the `GTD_AI_STUB_RESPONSE` env var set by the
Playwright `webServer` config (see `gtd_core/ai.py`).

Run from project root via `./scripts/e2e.sh`, or `npm run e2e:ui` here
for interactive mode. `npm test` (vitest) and `npm run e2e` are disjoint:
vitest matches `src/**/*.test.{ts,tsx}`, Playwright matches
`e2e/*.spec.ts`.

## CSS conventions

CSS custom properties defined in `:root` of `styles.css`. Key tokens:
`--accent`, `--border`, `--card`, `--muted`, `--danger`, `--radius`.
No component-scoped CSS — everything is global class-based.
