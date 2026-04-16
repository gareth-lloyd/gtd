# frontend

Vite + React 18 + TypeScript SPA. TanStack Query for server state.

## Key files

| File | Purpose |
|------|---------|
| `api.ts` | Typed fetch client. All API calls go through `request<T>()`. Types for Item, Project, EnvConfig, etc. |
| `App.tsx` | All pages and components in one file. Three-column CSS grid layout. |
| `Button.tsx` | `<Button busy={mut.isPending}>` — spinner overlay, auto-disable. Use for every mutation-backed button. |
| `toast.tsx` | Module-level `ToastStore` (callable outside React). `<Toaster />` subscribes to it. |
| `main.tsx` | React entry. `QueryClient` with `MutationCache.onError` → auto-toast. |
| `styles.css` | Vanilla CSS with custom properties. No Tailwind. |

## Patterns

**Error handling**: global. `MutationCache.onError` and `QueryCache.onError`
in `main.tsx` call `toasts.show('error', ...)`. No per-component error state
needed (ItemEditor removed its local error handling when this was added).

**Loading state**: per-button via `<Button busy={mut.isPending}>`. For shared
mutations (e.g. moveMut drives → next / → waiting / → someday), use
`mut.variables === targetBucket` to show spinner only on the clicked button.
Disable siblings via a `rowBusy` flag.

**State**: TanStack Query for all server state. Local `useState` for UI-only
state (filter selections, expanded panels). `localStorage` for env persistence.

**Drag-and-drop**: `@dnd-kit/core` + `@dnd-kit/sortable` for project action
reordering. Only `SortableActionList` (used inside expanded `ProjectCard`)
mounts the DnD context — the main next-actions list is plain. Pointer sensor
has a 5px activation distance so clicking the handle doesn't accidentally
start a drag. Drop is optimistic: `localOrder` overrides `items` immediately,
then `api.reorderProjectItems` syncs; on error we drop the override and rely
on the global toast.

**Project priority colors**: P1 red, P2 orange, P3 yellow, P4 blue, P5 gray.
Classes are `.priority-badge.p1` … `.priority-badge.p5` in `styles.css`.
`.sequential-badge` (purple) marks sequential projects. Projects sort by
`(priority ?? 99, due, title)` in `ProjectsView`.

## Build

```sh
npm run build    # tsc + vite build → dist/
npm run dev      # vite dev server on :5173, proxies /api to :8000
```

`dist/` is served by Django via WhiteNoise at `/static/`. Vite `base` is
`/static/` so built assets reference `/static/assets/...`.

## CSS conventions

CSS custom properties defined in `:root` of `styles.css`. Key tokens:
`--accent`, `--border`, `--card`, `--muted`, `--danger`, `--radius`.
No component-scoped CSS — everything is global class-based.
