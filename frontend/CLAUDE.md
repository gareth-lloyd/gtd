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
