import React, { useCallback, useEffect, useReducer, useState, useSyncExternalStore } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  Link,
  Navigate,
  NavLink,
  Outlet,
  Route,
  Routes,
  useLocation,
  useMatch,
  useNavigate,
  useParams,
} from "react-router-dom";
import { api, type EnvSummary, type Item } from "./api";
import { Button } from "./Button";
import { useNextFilters } from "./filters";
import { contextTintStyle } from "./context-colors";
import { ItemCard } from "./ItemCard";
import { CaptureBar, isEditableTarget, type CaptureMode } from "./CaptureBar";
import { FilterPanel } from "./FilterPanel";
import { SearchBar, SearchView } from "./SearchComponents";
import { ProjectNavLinks, ProjectsView, ProjectDetailView } from "./ProjectComponents";
import { BucketRoute, DoneView, NextActionsView } from "./ItemList";
import { TemplatesView } from "./TemplatesView";
import { SelectionProvider, useSelection } from "./SelectionContext";
import { DetailPanel } from "./DetailPanel";
import { ProcessedItemsProvider, useProcessedItems } from "./ProcessedItemsContext";
import { useEnvParam } from "./useEnvParam";
import { findItemInCache, useItemPatch } from "./ItemEdit";
import { useSpotlight } from "./spotlight";

type Section =
  | "inbox"
  | "next"
  | "projects"
  | "waiting"
  | "someday"
  | "reference"
  | "templates"
  | "done"
  | "trash";

const SECTIONS: Section[] = [
  "inbox",
  "next",
  "projects",
  "waiting",
  "someday",
  "reference",
  "templates",
  "done",
  "trash",
];

const DEFAULT_SECTION: Section = "inbox";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<RootRedirect />} />
      <Route
        path=":env"
        element={
          <ProcessedItemsProvider>
            <AppShell />
          </ProcessedItemsProvider>
        }
      >
        <Route index element={<Navigate to={DEFAULT_SECTION} replace />} />
        <Route path="inbox" element={<BucketRoute bucket="inbox" />} />
        <Route path="next" element={<NextActionsView />} />
        <Route path="waiting" element={<BucketRoute bucket="waiting" />} />
        <Route path="someday" element={<BucketRoute bucket="someday" />} />
        <Route path="reference" element={<BucketRoute bucket="reference" />} />
        <Route path="done" element={<DoneView />} />
        <Route path="trash" element={<BucketRoute bucket="trash" />} />
        <Route path="projects" element={<ProjectsView />} />
        <Route path="projects/:projectId" element={<ProjectDetailView />} />
        <Route path="templates" element={<TemplatesView />} />
        <Route path="items/:itemId" element={<ItemDetailView />} />
        <Route path="search" element={<SearchView />} />
      </Route>
    </Routes>
  );
}

function RootRedirect() {
  const { data: envs } = useQuery({ queryKey: ["envs"], queryFn: api.listEnvs });
  if (!envs) return <div className="app-loading">Loading…</div>;
  if (envs.length === 0) return <div className="app-loading">No environments configured</div>;
  const stored = localStorage.getItem("gtd:env");
  const env = stored && envs.some((e) => e.name === stored) ? stored : envs[0].name;
  return <Navigate to={`/${env}/${DEFAULT_SECTION}`} replace />;
}

function AppShell() {
  const env = useEnvParam();
  const { contexts } = useNextFilters();
  const { pathname } = useLocation();
  const [captureOpen, setCaptureOpen] = useState(false);
  const [captureMode, setCaptureMode] = useState<CaptureMode>("regular");
  const [captureFocusTick, bumpCaptureFocus] = useReducer((x: number) => x + 1, 0);
  const [searchFocusTick, bumpSearchFocus] = useReducer((x: number) => x + 1, 0);
  const onNextPage = useMatch(":env/next") != null;
  const projectDetailMatch = useMatch(":env/projects/:projectId");
  const currentProjectId = projectDetailMatch?.params.projectId ?? "";

  const { data: envs } = useQuery({ queryKey: ["envs"], queryFn: api.listEnvs });
  const { data: config } = useQuery({
    queryKey: ["config", env],
    queryFn: () => api.getConfig(env),
    enabled: !!env,
  });
  // Shares cache key with BucketView's default (non-deferred) inbox fetch.
  const { data: inboxItems } = useQuery({
    queryKey: ["items", env, "inbox", false],
    queryFn: () => api.listItems(env, { status: "inbox" }),
    enabled: !!env,
  });
  // While the user is processing the inbox, the cached list intentionally
  // still contains rows that have been moved/completed/deleted (they render
  // greyed out). Subtract those from the badge so the count matches what
  // the user sees as "still to do".
  const processed = useProcessedItems();
  const inboxCount = Math.max(0, (inboxItems?.length ?? 0) - (processed?.processedCount ?? 0));

  useEffect(() => {
    if (env) localStorage.setItem("gtd:env", env);
  }, [env]);

  useEffect(() => {
    setCaptureOpen(false);
  }, [pathname]);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape" && captureOpen) {
        setCaptureOpen(false);
        return;
      }
      if (e.metaKey || e.ctrlKey || e.altKey) return;
      if (isEditableTarget(e.target)) return;
      if (e.shiftKey && e.key.toLowerCase() !== "c") return;
      if (e.key === "c" || e.key === "C") {
        e.preventDefault();
        setCaptureMode(e.shiftKey ? "regular-top" : "regular");
        setCaptureOpen(true);
        bumpCaptureFocus();
      } else if (e.key === "a") {
        e.preventDefault();
        setCaptureMode("ai");
        setCaptureOpen(true);
        bumpCaptureFocus();
      } else if (e.key === "/") {
        e.preventDefault();
        bumpSearchFocus();
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [captureOpen]);

  if (!envs) return <div className="app-loading">Loading…</div>;
  if (!envs.some((e) => e.name === env)) {
    return <div className="app-loading">Unknown environment: {env}</div>;
  }

  return (
    <SelectionProvider>
      <div className={onNextPage ? "app" : "app no-filters"} style={contextTintStyle(contexts)}>
        <header>
          <div className="header-row">
            <h1>
              <span className="brand">gtd</span>
            </h1>
            <EnvTabs envs={envs} env={env} />
            <button
              className={captureOpen ? "active" : ""}
              onClick={() => setCaptureOpen((v) => !v)}
            >
              {captureOpen ? "Close capture" : "+ Capture"}
            </button>
            <SpotlightWorkingOnButton env={env} />
            <SearchBar env={env} focusTick={searchFocusTick} />
            <div className="spacer" />
            <SyncButton />
          </div>
        </header>

        {captureOpen && (
          <div
            className="capture-overlay"
            onClick={(e) => {
              if (e.target === e.currentTarget) setCaptureOpen(false);
            }}
          >
            <CaptureBar
              env={env}
              focusTick={captureFocusTick}
              defaultProjectId={currentProjectId}
              onCaptured={() => setCaptureOpen(false)}
              mode={captureMode}
              onModeChange={setCaptureMode}
            />
          </div>
        )}

        <nav className="side-nav">
          {SECTIONS.map((s) => (
            <React.Fragment key={s}>
              <NavLink
                to={s}
                end={s === "projects"}
                className={({ isActive }) => (isActive ? "active" : "")}
              >
                {s}
                {s === "inbox" && inboxCount > 0 && (
                  <span className="side-nav-count"> ({inboxCount})</span>
                )}
              </NavLink>
              {s === "projects" && <ProjectNavLinks env={env} />}
            </React.Fragment>
          ))}
        </nav>

        {onNextPage && (
          <aside className="side-filters">
            <FilterPanel config={config} />
          </aside>
        )}

        <ContentArea env={env} />
      </div>
      <WorkingOnShortcut env={env} />
      <KeyboardNavShortcut />
    </SelectionProvider>
  );
}

function ContentArea({ env }: { env: string }) {
  const { clearHover } = useSelection();
  return (
    <div className="content-area" onMouseLeave={clearHover}>
      <main onScroll={clearHover}>
        <Outlet />
      </main>
      <DetailPanel env={env} />
    </div>
  );
}

// Subscribe to the React Query cache so we can surface a working-on entry
// point without firing our own dedicated /items?status=next request — that
// would either drift from NextActionsView's filter-aware key (silent
// duplicate fetches under filters) or pin the cache to a fragile key shape.
// useSyncExternalStore (not useEffect+setState) — synchronous cache fires
// during another component's render would otherwise trigger React's
// "setState during render of another component" warning.
function useWorkingOnId(env: string): string | null {
  const qc = useQueryClient();
  const subscribe = useCallback((cb: () => void) => qc.getQueryCache().subscribe(cb), [qc]);
  const getSnapshot = useCallback(() => {
    const lists = qc.getQueriesData<Item[]>({ queryKey: ["items", env] });
    for (const [, data] of lists) {
      const found = data?.find((i) => i.working_on);
      if (found) return found.id;
    }
    return null;
  }, [qc, env]);
  return useSyncExternalStore(subscribe, getSnapshot);
}

function SpotlightWorkingOnButton({ env }: { env: string }) {
  const { spotlightId, setSpotlight } = useSpotlight();
  const workingOnId = useWorkingOnId(env);
  if (!workingOnId || workingOnId === spotlightId) return null;
  return (
    <button
      type="button"
      className="spotlight-working-on"
      title="Focus on the item you're currently working on"
      onClick={() => setSpotlight(workingOnId)}
    >
      🎯 Focus working item
    </button>
  );
}

// j/k/ArrowDown/ArrowUp/Enter — keyboard navigation between item cards.
// Lives inside SelectionProvider so it can read/drive selection. Renders nothing.
function KeyboardNavShortcut() {
  const { selectedId, editingId, selectNext, selectPrev, edit } = useSelection();
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.metaKey || e.ctrlKey || e.altKey || e.shiftKey) return;
      if (isEditableTarget(e.target)) return;
      if (e.key === "j" || e.key === "ArrowDown") {
        e.preventDefault();
        selectNext();
      } else if (e.key === "k" || e.key === "ArrowUp") {
        e.preventDefault();
        selectPrev();
      } else if (e.key === "Enter") {
        if (!selectedId || editingId) return;
        e.preventDefault();
        edit(selectedId);
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [selectedId, editingId, selectNext, selectPrev, edit]);

  // Scroll the selected card into view when selection moves.
  useEffect(() => {
    if (!selectedId) return;
    const el = document.querySelector(`[data-item-id="${CSS.escape(selectedId)}"]`);
    el?.scrollIntoView({ block: "nearest" });
  }, [selectedId]);

  return null;
}

// Lives inside SelectionProvider so it can read selectedId. Renders nothing.
function WorkingOnShortcut({ env }: { env: string }) {
  const { selectedId } = useSelection();
  const qc = useQueryClient();
  const { patch } = useItemPatch(env, selectedId ?? "");
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key.toLowerCase() !== "f") return;
      if (e.metaKey || e.ctrlKey || e.altKey || e.shiftKey) return;
      if (isEditableTarget(e.target)) return;
      if (!selectedId) return;
      const item = findItemInCache(qc, env, selectedId);
      if (!item) return;
      e.preventDefault();
      patch({ working_on: !item.working_on });
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [env, selectedId, qc, patch]);
  return null;
}

// ---- Env tabs ----

function EnvTabs({ envs, env }: { envs: EnvSummary[]; env: string }) {
  return (
    <div className="env-tabs">
      {envs.map((e) => (
        <Link
          key={e.name}
          to={`/${e.name}/${DEFAULT_SECTION}`}
          className={env === e.name ? "env-tab active" : "env-tab"}
        >
          {e.name}
        </Link>
      ))}
    </div>
  );
}

// ---- Sync button ----

function SyncButton() {
  const qc = useQueryClient();
  const { data } = useQuery({
    queryKey: ["snapshot-status"],
    queryFn: api.snapshotStatus,
    refetchInterval: 10_000,
  });
  const snap = useMutation({
    mutationFn: () => api.snapshot(),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["snapshot-status"] }),
  });

  const count = data?.dirty_count ?? 0;
  const unloadable = data?.unloadable_files ?? [];

  return (
    <div className="sync">
      {unloadable.length > 0 && (
        <span
          className="count dirty"
          title={`Unloadable files (won't appear in lists):\n${unloadable.join("\n")}`}
        >
          ⚠ {unloadable.length} unloadable
        </span>
      )}
      <span className={count > 0 ? "count dirty" : "count"}>
        {count === 0 ? "clean" : `${count} dirty`}
      </span>
      <Button onClick={() => snap.mutate()} disabled={count === 0} busy={snap.isPending}>
        Sync
      </Button>
    </div>
  );
}

// ---- Item detail ----

function ItemDetailView() {
  const env = useEnvParam();
  const navigate = useNavigate();
  const { itemId = "" } = useParams<{ itemId: string }>();
  const { select } = useSelection();
  const { data: item, isLoading } = useQuery({
    queryKey: ["item", env, itemId],
    queryFn: () => api.getItem(env, itemId),
  });
  const { data: projects } = useQuery({
    queryKey: ["projects", env, false],
    queryFn: () => api.listProjects(env, false),
  });

  // Pre-select the item on mount
  useEffect(() => {
    if (itemId) select(itemId);
  }, [itemId, select]);

  if (isLoading) return <div className="empty">Loading…</div>;
  if (!item) return <div className="empty">Item not found.</div>;

  return (
    <div className="item-detail">
      <button className="back-link" onClick={() => navigate(-1)}>
        ← Back
      </button>
      <ul className="item-list">
        <li>
          <ItemCard env={env} item={item} projects={projects} />
        </li>
      </ul>
    </div>
  );
}
