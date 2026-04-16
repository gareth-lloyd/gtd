import React, { useEffect, useReducer, useRef, useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
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
  useSearchParams,
} from 'react-router-dom';
import {
  DndContext,
  closestCenter,
  KeyboardSensor,
  PointerSensor,
  useSensor,
  useSensors,
  type DragEndEvent,
} from '@dnd-kit/core';
import {
  arrayMove,
  SortableContext,
  sortableKeyboardCoordinates,
  useSortable,
  verticalListSortingStrategy,
} from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import {
  api,
  type Bucket,
  type Energy,
  type EnvConfig,
  type EnvSummary,
  type Item,
  type Project,
} from './api';
import { Button } from './Button';
import { useNextFilters } from './filters';
import { useSearchIndex, type SearchHit } from './search';
import { contextHue, contextChipStyle, contextTintStyle } from './context-colors';
import { ItemCard } from './ItemCard';
import { fmtDate, sortProjects } from './format';

type Section =
  | 'inbox'
  | 'next'
  | 'projects'
  | 'waiting'
  | 'someday'
  | 'reference'
  | 'trash';

const SECTIONS: Section[] = [
  'inbox',
  'next',
  'projects',
  'waiting',
  'someday',
  'reference',
  'trash',
];

const DEFAULT_SECTION: Section = 'inbox';

const ENERGY_CHOICES: (Energy | '')[] = ['', 'low', 'medium', 'high'];

const TIME_CHOICES: { label: string; value: string }[] = [
  { label: 'any', value: '' },
  { label: '5m', value: '5' },
  { label: '15m', value: '15' },
  { label: '30m', value: '30' },
  { label: '60m', value: '60' },
  { label: '2h+', value: '240' },
];

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<RootRedirect />} />
      <Route path=":env" element={<AppShell />}>
        <Route index element={<Navigate to={DEFAULT_SECTION} replace />} />
        <Route path="inbox" element={<BucketRoute bucket="inbox" />} />
        <Route path="next" element={<NextActionsView />} />
        <Route path="waiting" element={<BucketRoute bucket="waiting" />} />
        <Route path="someday" element={<BucketRoute bucket="someday" />} />
        <Route path="reference" element={<BucketRoute bucket="reference" />} />
        <Route path="trash" element={<BucketRoute bucket="trash" />} />
        <Route path="projects" element={<ProjectsView />} />
        <Route path="projects/:projectId" element={<ProjectDetailView />} />
        <Route path="items/:itemId" element={<ItemDetailView />} />
        <Route path="search" element={<SearchView />} />
      </Route>
    </Routes>
  );
}

function RootRedirect() {
  const { data: envs } = useQuery({ queryKey: ['envs'], queryFn: api.listEnvs });
  if (!envs) return <div className="app-loading">Loading…</div>;
  if (envs.length === 0) return <div className="app-loading">No environments configured</div>;
  const stored = localStorage.getItem('gtd:env');
  const env = stored && envs.some((e) => e.name === stored) ? stored : envs[0].name;
  return <Navigate to={`/${env}/${DEFAULT_SECTION}`} replace />;
}

function useEnvParam(): string {
  const { env } = useParams<{ env: string }>();
  return env!;
}

function AppShell() {
  const env = useEnvParam();
  const { contexts } = useNextFilters();
  const { pathname } = useLocation();
  const [captureOpen, setCaptureOpen] = useState(false);
  const [captureFocusTick, bumpCaptureFocus] = useReducer((x: number) => x + 1, 0);
  const [searchFocusTick, bumpSearchFocus] = useReducer((x: number) => x + 1, 0);
  const onNextPage = useMatch(':env/next') != null;
  const onInboxPage = useMatch(':env/inbox') != null;
  const projectDetailMatch = useMatch(':env/projects/:projectId');
  const currentProjectId = projectDetailMatch?.params.projectId ?? '';

  const { data: envs } = useQuery({ queryKey: ['envs'], queryFn: api.listEnvs });
  const { data: config } = useQuery({
    queryKey: ['config', env],
    queryFn: () => api.getConfig(env),
    enabled: !!env,
  });

  useEffect(() => {
    if (env) localStorage.setItem('gtd:env', env);
  }, [env]);

  useEffect(() => {
    setCaptureOpen(false);
  }, [pathname]);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.metaKey || e.ctrlKey || e.altKey) return;
      if (isEditableTarget(e.target)) return;
      if (e.key === 'c') {
        e.preventDefault();
        setCaptureOpen(true);
        bumpCaptureFocus();
      } else if (e.key === '/') {
        e.preventDefault();
        bumpSearchFocus();
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, []);

  if (!envs) return <div className="app-loading">Loading…</div>;
  if (!envs.some((e) => e.name === env)) {
    return <div className="app-loading">Unknown environment: {env}</div>;
  }

  return (
    <div
      className={onNextPage ? 'app' : 'app no-filters'}
      style={contextTintStyle(contexts)}
    >
      <header>
        <div className="header-row">
          <h1>
            <span className="brand">gtd</span>
          </h1>
          <EnvTabs envs={envs} env={env} />
          {!onInboxPage && (
            <button
              className={captureOpen ? 'active' : ''}
              onClick={() => setCaptureOpen((v) => !v)}
            >
              {captureOpen ? 'Close capture' : '+ Capture'}
            </button>
          )}
          <SearchBar env={env} focusTick={searchFocusTick} />
          <div className="spacer" />
          <SyncButton />
        </div>
        {(onInboxPage || captureOpen) && (
          <CaptureBar
            env={env}
            focusTick={captureFocusTick}
            defaultProjectId={currentProjectId}
            onCaptured={() => setCaptureOpen(false)}
          />
        )}
      </header>

      <nav className="side-nav">
        {SECTIONS.map((s) => (
          <React.Fragment key={s}>
            <NavLink
              to={s}
              end={s === 'projects'}
              className={({ isActive }) => (isActive ? 'active' : '')}
            >
              {s}
            </NavLink>
            {s === 'projects' && <ProjectNavLinks env={env} />}
          </React.Fragment>
        ))}
      </nav>

      <main>
        <Outlet />
      </main>

      <aside className="side-filters">
        {onNextPage && <FilterPanel config={config} />}
      </aside>
    </div>
  );
}

function BucketRoute({ bucket }: { bucket: Bucket }) {
  const env = useEnvParam();
  return <BucketView env={env} bucket={bucket} />;
}

// ---- Env tabs ----

function EnvTabs({ envs, env }: { envs: EnvSummary[]; env: string }) {
  return (
    <div className="env-tabs">
      {envs.map((e) => (
        <Link
          key={e.name}
          to={`/${e.name}/${DEFAULT_SECTION}`}
          className={env === e.name ? 'env-tab active' : 'env-tab'}
        >
          {e.name}
        </Link>
      ))}
    </div>
  );
}

// ---- Capture bar ----

function isEditableTarget(target: EventTarget | null): boolean {
  if (!(target instanceof HTMLElement)) return false;
  const tag = target.tagName;
  return (
    tag === 'INPUT' ||
    tag === 'TEXTAREA' ||
    tag === 'SELECT' ||
    target.isContentEditable
  );
}

function CaptureBar({
  env,
  focusTick,
  defaultProjectId = '',
  onCaptured,
}: {
  env: string;
  focusTick: number;
  defaultProjectId?: string;
  onCaptured?: () => void;
}) {
  const [title, setTitle] = useState('');
  const [notes, setNotes] = useState('');
  const [projectId, setProjectId] = useState(defaultProjectId);
  const titleRef = useRef<HTMLInputElement>(null);
  const qc = useQueryClient();

  useEffect(() => {
    setProjectId(defaultProjectId);
  }, [defaultProjectId]);

  const { data: projects } = useQuery({
    queryKey: ['projects', env, false],
    queryFn: () => api.listProjects(env, false),
  });

  useEffect(() => {
    titleRef.current?.focus();
    titleRef.current?.select();
  }, [focusTick]);

  const mut = useMutation({
    mutationFn: async () => {
      const item = await api.captureItem(env, title.trim(), notes, {
        energy: 'low',
        time_minutes: 5,
      });
      if (projectId) {
        await api.updateItem(env, item.id, { project: projectId });
        return api.moveItem(env, item.id, 'next');
      }
      return item;
    },
    onSuccess: () => {
      setTitle('');
      setNotes('');
      setProjectId(defaultProjectId);
      qc.invalidateQueries({ queryKey: ['items', env] });
      qc.invalidateQueries({ queryKey: ['search-corpus', env], refetchType: 'none' });
      qc.invalidateQueries({ queryKey: ['snapshot-status'] });
      if (projectId) {
        qc.invalidateQueries({ queryKey: ['project', env, projectId] });
        qc.invalidateQueries({ queryKey: ['projects', env] });
      }
      onCaptured?.();
    },
  });

  const sortedProjects = projects ? sortProjects(projects) : [];
  const destination = projectId ? 'next + project' : 'inbox';

  const submit = () => {
    if (title.trim()) mut.mutate();
  };

  return (
    <form
      className="capture"
      onSubmit={(e) => {
        e.preventDefault();
        submit();
      }}
      onKeyDown={(e) => {
        if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') {
          e.preventDefault();
          submit();
        }
      }}
    >
      <div className="capture-row">
        <input
          ref={titleRef}
          type="text"
          placeholder={projectId ? 'Capture to next…' : 'Capture to inbox…'}
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
        <Button
          type="submit"
          className="primary"
          disabled={!title.trim()}
          busy={mut.isPending}
        >
          Capture
        </Button>
      </div>
      <textarea
        rows={3}
        placeholder="Notes (markdown supported, optional)…"
        value={notes}
        onChange={(e) => setNotes(e.target.value)}
      />
      <div className="capture-row">
        <label className="capture-project">
          <span>Project</span>
          <select
            value={projectId}
            onChange={(e) => setProjectId(e.target.value)}
          >
            <option value="">— (keep in inbox)</option>
            {sortedProjects.map((p) => (
              <option key={p.id} value={p.id}>
                {p.title}
              </option>
            ))}
          </select>
        </label>
        <div className="capture-hint">
          → {destination} · energy=low · time=5min
        </div>
      </div>
    </form>
  );
}

// ---- Sync button ----

function SyncButton() {
  const qc = useQueryClient();
  const { data } = useQuery({
    queryKey: ['snapshot-status'],
    queryFn: api.snapshotStatus,
    refetchInterval: 10_000,
  });
  const snap = useMutation({
    mutationFn: (message?: string) => api.snapshot(message),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['snapshot-status'] }),
  });

  const count = data?.dirty_count ?? 0;

  return (
    <div className="sync">
      <span className={count > 0 ? 'count dirty' : 'count'}>
        {count === 0 ? 'clean' : `${count} dirty`}
      </span>
      <Button
        onClick={() => {
          const msg = prompt('Snapshot message (optional):') || undefined;
          snap.mutate(msg);
        }}
        disabled={count === 0}
        busy={snap.isPending}
      >
        Sync
      </Button>
    </div>
  );
}

// ---- Filter panel ----

function FilterPanel({ config }: { config: EnvConfig | undefined }) {
  const {
    contexts,
    energy,
    maxMinutes,
    noProject,
    setContexts,
    setEnergy,
    setMaxMinutes,
    setNoProject,
  } = useNextFilters();
  return (
    <div className="filter-panel">
      <div className="filter-section">
        <h3>Contexts</h3>
        {config?.contexts.map((c) => (
          <label
            key={c}
            className="check-row"
            style={{ borderLeft: `3px solid hsl(${contextHue(c)}, 55%, 65%)` }}
          >
            <input
              type="checkbox"
              checked={contexts.includes(c)}
              onChange={(e) =>
                setContexts((prev) =>
                  e.target.checked ? [...prev, c] : prev.filter((x) => x !== c)
                )
              }
            />
            <span>@{c}</span>
          </label>
        ))}
        {contexts.length > 0 && (
          <button
            type="button"
            className="clear-link"
            onClick={() => setContexts(() => [])}
          >
            clear
          </button>
        )}
      </div>

      <div className="filter-section">
        <h3>Energy</h3>
        <div className="btn-group">
          {ENERGY_CHOICES.map((e) => (
            <button
              type="button"
              key={e || 'any'}
              className={energy === e ? 'active' : ''}
              onClick={() => setEnergy(e)}
            >
              {e || 'any'}
            </button>
          ))}
        </div>
      </div>

      <div className="filter-section">
        <h3>Max time</h3>
        <div className="btn-group">
          {TIME_CHOICES.map((t) => (
            <button
              type="button"
              key={t.label}
              className={maxMinutes === t.value ? 'active' : ''}
              onClick={() => setMaxMinutes(t.value)}
            >
              {t.label}
            </button>
          ))}
        </div>
      </div>

      <div className="filter-section">
        <h3>Project</h3>
        <label className="check-row">
          <input
            type="checkbox"
            checked={noProject}
            onChange={(e) => setNoProject(e.target.checked)}
          />
          <span>No project</span>
        </label>
      </div>
    </div>
  );
}

// ---- Next actions view ----

function NextActionsView() {
  const env = useEnvParam();
  const { contexts, energy, maxMinutes, noProject } = useNextFilters();
  const params: Record<string, string> = { status: 'next' };
  if (contexts.length) params.contexts = contexts.join(',');
  if (energy) params.energy = energy;
  if (maxMinutes) params.max_minutes = maxMinutes;
  if (noProject) params.no_project = 'true';

  const { data: items, isLoading } = useQuery({
    queryKey: ['items', env, 'next', contexts, energy, maxMinutes, noProject],
    queryFn: () => api.listItems(env, params),
  });

  if (isLoading) return <div className="empty">Loading…</div>;
  return <ItemList env={env} items={items ?? []} />;
}

// ---- Bucket view (inbox/waiting/someday/reference/trash) ----

function BucketView({ env, bucket }: { env: string; bucket: Bucket }) {
  const [params, setParams] = useSearchParams();
  const includeDeferred =
    bucket === 'inbox' && params.get('include_deferred') === 'true';

  const listParams: Record<string, string> = { status: bucket };
  if (includeDeferred) listParams.include_deferred = 'true';

  const { data: items, isLoading } = useQuery({
    queryKey: ['items', env, bucket, includeDeferred],
    queryFn: () => api.listItems(env, listParams),
  });

  return (
    <>
      {bucket === 'inbox' && (
        <div className="bucket-toolbar">
          <label className="toggle">
            <input
              type="checkbox"
              checked={includeDeferred}
              onChange={(e) => {
                const next = new URLSearchParams(params);
                if (e.target.checked) next.set('include_deferred', 'true');
                else next.delete('include_deferred');
                setParams(next, { replace: true });
              }}
            />
            Show deferred
          </label>
        </div>
      )}
      {isLoading ? (
        <div className="empty">Loading…</div>
      ) : (
        <ItemList env={env} items={items ?? []} />
      )}
    </>
  );
}

// ---- Projects view ----

const PRIORITY_LABELS: Record<number, string> = {
  1: 'P1 critical',
  2: 'P2 high',
  3: 'P3 medium',
  4: 'P4 low',
  5: 'P5 aspirational',
};

function ProjectsView() {
  const env = useEnvParam();
  const [showFinished, setShowFinished] = useState(false);
  const { data: projects, isLoading } = useQuery({
    queryKey: ['projects', env, showFinished],
    queryFn: () => api.listProjects(env, showFinished),
  });

  if (isLoading) return <div className="empty">Loading…</div>;

  const sorted = sortProjects(projects ?? []);

  return (
    <>
      <div className="projects-toolbar">
        <NewProjectForm env={env} />
        <label className="toggle">
          <input
            type="checkbox"
            checked={showFinished}
            onChange={(e) => setShowFinished(e.target.checked)}
          />
          Show finished
        </label>
      </div>
      {sorted.length === 0 && <div className="empty">No projects yet.</div>}
      <ul className="project-index">
        {sorted.map((p) => (
          <li key={p.id}>
            <ProjectIndexRow project={p} />
          </li>
        ))}
      </ul>
    </>
  );
}

function ProjectBadges({ project }: { project: Project }) {
  return (
    <>
      {project.priority != null && (
        <span className={`priority-badge p${project.priority}`}>
          P{project.priority}
        </span>
      )}
      {project.sequential && (
        <span className="sequential-badge" title="Sequential — one step at a time">
          ↓ sequential
        </span>
      )}
      {project.status !== 'active' && (
        <span className="project-status">{project.status}</span>
      )}
    </>
  );
}

function ProjectIndexRow({ project }: { project: Project }) {
  const isDone = project.status === 'complete' || project.status === 'dropped';
  return (
    <Link
      to={project.id}
      className={`project-index-row${isDone ? ' done' : ''}`}
    >
      <span className="project-index-title">{project.title}</span>
      <ProjectBadges project={project} />
      {project.due && <span className="chip">due {project.due}</span>}
      {project.outcome && (
        <span className="project-index-outcome">{project.outcome}</span>
      )}
    </Link>
  );
}

function ProjectNavLinks({ env }: { env: string }) {
  const { data: projects } = useQuery({
    queryKey: ['projects', env, false],
    queryFn: () => api.listProjects(env, false),
  });
  if (!projects || projects.length === 0) return null;
  return (
    <div className="side-nav-sub">
      {sortProjects(projects).map((p) => (
        <NavLink
          key={p.id}
          to={`projects/${p.id}`}
          className={({ isActive }) => (isActive ? 'sub-link active' : 'sub-link')}
          title={p.title}
        >
          {p.priority != null && (
            <span className={`priority-dot p${p.priority}`}>●</span>
          )}
          <span className="sub-link-title">{p.title}</span>
        </NavLink>
      ))}
    </div>
  );
}

function ProjectDetailView() {
  const env = useEnvParam();
  const { projectId = '' } = useParams<{ projectId: string }>();
  const navigate = useNavigate();
  const qc = useQueryClient();
  const [editing, setEditing] = useState(false);
  const { data, isLoading } = useQuery({
    queryKey: ['project', env, projectId],
    queryFn: () => api.getProject(env, projectId),
  });

  const invalidate = () => {
    qc.invalidateQueries({ queryKey: ['projects', env] });
    qc.invalidateQueries({ queryKey: ['project', env, projectId] });
    qc.invalidateQueries({ queryKey: ['search-corpus', env], refetchType: 'none' });
    qc.invalidateQueries({ queryKey: ['snapshot-status'] });
  };

  const statusMut = useMutation<Project, Error, string>({
    mutationFn: (status) => api.updateProject(env, projectId, { status }),
    onSuccess: invalidate,
  });

  const deleteMut = useMutation({
    mutationFn: () => api.deleteProject(env, projectId),
    onSuccess: () => {
      invalidate();
      navigate('..');
    },
  });

  if (isLoading || !data) return <div className="empty">Loading…</div>;

  const { project, actions } = data;
  const isDone = project.status === 'complete' || project.status === 'dropped';
  const anyPending = statusMut.isPending || deleteMut.isPending;

  return (
    <div className="project-detail">
      <Link className="back-link" to="..">
        ← All projects
      </Link>
      <div className={`project-card${isDone ? ' done' : ''}`}>
        <h2>
          {project.title}
          <ProjectBadges project={project} />
        </h2>
        <div className="project-meta">
          {project.outcome && <span className="outcome">{project.outcome}</span>}
          {project.due && <span className="chip">due {project.due}</span>}
          {project.area && <span className="chip">{project.area}</span>}
          <span className="chip">
            {actions.length} action{actions.length !== 1 ? 's' : ''}
          </span>
          <span className="chip dates" title={`created ${fmtDate(project.created)}`}>
            updated {fmtDate(project.updated)}
          </span>
        </div>
        <div className="project-actions">
          {project.status !== 'complete' && (
            <Button
              onClick={() => statusMut.mutate('complete')}
              busy={statusMut.isPending && statusMut.variables === 'complete'}
              disabled={anyPending}
            >
              ✓ Complete
            </Button>
          )}
          {project.status !== 'active' && (
            <Button
              onClick={() => statusMut.mutate('active')}
              busy={statusMut.isPending && statusMut.variables === 'active'}
              disabled={anyPending}
            >
              ↺ Reopen
            </Button>
          )}
          {project.status === 'active' && (
            <Button
              onClick={() => statusMut.mutate('on_hold')}
              busy={statusMut.isPending && statusMut.variables === 'on_hold'}
              disabled={anyPending}
            >
              ⏸ Hold
            </Button>
          )}
          <button onClick={() => setEditing(!editing)} disabled={anyPending}>
            {editing ? 'Close' : 'Edit'}
          </button>
          <Button
            className="danger"
            onClick={() => {
              if (
                confirm(
                  `Delete project "${project.title}"? Actions linked to it will not be deleted.`
                )
              ) {
                deleteMut.mutate();
              }
            }}
            busy={deleteMut.isPending}
            disabled={anyPending}
          >
            Delete
          </Button>
        </div>
        {editing && (
          <ProjectEditor
            env={env}
            project={project}
            onClose={() => setEditing(false)}
          />
        )}
        <SortableActionList env={env} projectId={project.id} items={actions} />
      </div>
    </div>
  );
}

// ---- Search ----

const SEARCH_CAP = 200;
const DROPDOWN_LIMIT = 8;

function hitLink(env: string, hit: SearchHit): string {
  return hit.kind === 'item'
    ? `/${env}/items/${hit.item.id}`
    : `/${env}/projects/${hit.project.id}`;
}

function HitRow({
  hit,
  selected,
  onClick,
}: {
  hit: SearchHit;
  selected?: boolean;
  onClick?: () => void;
}) {
  if (hit.kind === 'item') {
    const item = hit.item;
    return (
      <div
        className={selected ? 'search-hit selected' : 'search-hit'}
        onClick={onClick}
      >
        <span className="hit-kind">item</span>
        <span className="hit-title">{item.title}</span>
        <span className="hit-meta">
          <span className="chip">{item.status}</span>
          {item.contexts.slice(0, 3).map((c) => (
            <span key={c} className="chip context-chip" style={contextChipStyle(c)}>
              @{c}
            </span>
          ))}
        </span>
      </div>
    );
  }
  const project = hit.project;
  return (
    <div
      className={selected ? 'search-hit selected' : 'search-hit'}
      onClick={onClick}
    >
      <span className="hit-kind">project</span>
      <span className="hit-title">{project.title}</span>
      <span className="hit-meta">
        <ProjectBadges project={project} />
        {project.outcome && (
          <span className="hit-snippet">{project.outcome}</span>
        )}
      </span>
    </div>
  );
}

function SearchBar({ env, focusTick }: { env: string; focusTick: number }) {
  const navigate = useNavigate();
  const inputRef = useRef<HTMLInputElement>(null);
  const [query, setQuery] = useState('');
  const [focused, setFocused] = useState(false);
  const [selected, setSelected] = useState(0);
  const [everFocused, setEverFocused] = useState(false);
  const { index, isLoading } = useSearchIndex(env, { enabled: everFocused });

  useEffect(() => {
    if (focusTick === 0) return;
    inputRef.current?.focus();
    inputRef.current?.select();
  }, [focusTick]);

  useEffect(() => {
    setSelected(0);
  }, [query]);

  const allHits = useMemoSearch(index, query, SEARCH_CAP);
  const hits = allHits.slice(0, DROPDOWN_LIMIT);
  const total = allHits.length;
  const hasQuery = query.trim().length > 0;
  const showDropdown = focused && hasQuery;

  function activate(hit: SearchHit) {
    setFocused(false);
    setQuery('');
    navigate(hitLink(env, hit));
  }

  function seeAll() {
    setFocused(false);
    navigate(`/${env}/search?q=${encodeURIComponent(query.trim())}`);
  }

  function onKeyDown(e: React.KeyboardEvent<HTMLInputElement>) {
    if (e.key === 'Escape') {
      setQuery('');
      inputRef.current?.blur();
      return;
    }
    if (!hasQuery) return;
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      setSelected((s) => Math.min(s + 1, hits.length));
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setSelected((s) => Math.max(s - 1, 0));
    } else if (e.key === 'Enter') {
      e.preventDefault();
      if (selected < hits.length) activate(hits[selected]);
      else seeAll();
    }
  }

  return (
    <div className="search-bar">
      <input
        ref={inputRef}
        type="search"
        placeholder="Search… (/)"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onFocus={() => {
          setFocused(true);
          setEverFocused(true);
        }}
        onBlur={() => {
          setTimeout(() => setFocused(false), 100);
        }}
        onKeyDown={onKeyDown}
      />
      {showDropdown && (
        <div className="search-dropdown">
          {isLoading && !index && (
            <div className="search-empty">Building index…</div>
          )}
          {index && hits.length === 0 && (
            <div className="search-empty">No matches.</div>
          )}
          {hits.map((hit, i) => (
            <div
              key={`${hit.kind}:${hit.id}`}
              onMouseDown={(e) => e.preventDefault()}
              onClick={() => activate(hit)}
              onMouseEnter={() => setSelected(i)}
            >
              <HitRow hit={hit} selected={i === selected} />
            </div>
          ))}
          {total > hits.length && (
            <div
              className={
                selected === hits.length
                  ? 'search-see-all selected'
                  : 'search-see-all'
              }
              onMouseDown={(e) => e.preventDefault()}
              onClick={seeAll}
              onMouseEnter={() => setSelected(hits.length)}
            >
              See all {total} results →
            </div>
          )}
        </div>
      )}
    </div>
  );
}

function useMemoSearch(
  index: ReturnType<typeof useSearchIndex>['index'],
  query: string,
  limit: number,
): SearchHit[] {
  const trimmed = query.trim();
  return React.useMemo(() => {
    if (!index || !trimmed) return [];
    return index.search(trimmed, limit);
  }, [index, trimmed, limit]);
}

function SearchView() {
  const env = useEnvParam();
  const [params, setParams] = useSearchParams();
  const q = params.get('q') ?? '';
  const { index, isLoading } = useSearchIndex(env);
  const hits = useMemoSearch(index, q, SEARCH_CAP);

  const items = hits.filter((h) => h.kind === 'item');
  const projects = hits.filter((h) => h.kind === 'project');

  return (
    <div className="search-view">
      <input
        type="search"
        className="search-view-input"
        placeholder="Search…"
        value={q}
        onChange={(e) => {
          const next = new URLSearchParams(params);
          if (e.target.value) next.set('q', e.target.value);
          else next.delete('q');
          setParams(next, { replace: true });
        }}
        autoFocus
      />
      {!q.trim() && <div className="empty">Type to search.</div>}
      {q.trim() && isLoading && !index && (
        <div className="empty">Building index…</div>
      )}
      {q.trim() && index && hits.length === 0 && (
        <div className="empty">No matches.</div>
      )}
      {projects.length > 0 && (
        <>
          <h3 className="search-group-title">Projects ({projects.length})</h3>
          <ul className="search-results">
            {projects.map((hit) => (
              <li key={hit.id}>
                <Link to={hitLink(env, hit)} className="search-result-link">
                  <HitRow hit={hit} />
                </Link>
              </li>
            ))}
          </ul>
        </>
      )}
      {items.length > 0 && (
        <>
          <h3 className="search-group-title">Items ({items.length})</h3>
          <ul className="search-results">
            {items.map((hit) => (
              <li key={hit.id}>
                <Link to={hitLink(env, hit)} className="search-result-link">
                  <HitRow hit={hit} />
                </Link>
              </li>
            ))}
          </ul>
          {hits.length === SEARCH_CAP && (
            <div className="empty">
              Showing first {SEARCH_CAP} — refine your search.
            </div>
          )}
        </>
      )}
    </div>
  );
}

// ---- Item detail ----

function ItemDetailView() {
  const env = useEnvParam();
  const navigate = useNavigate();
  const { itemId = '' } = useParams<{ itemId: string }>();
  const [expanded, setExpanded] = useState(true);
  const { data: item, isLoading } = useQuery({
    queryKey: ['item', env, itemId],
    queryFn: () => api.getItem(env, itemId),
  });
  const { data: projects } = useQuery({
    queryKey: ['projects', env, false],
    queryFn: () => api.listProjects(env, false),
  });

  if (isLoading) return <div className="empty">Loading…</div>;
  if (!item) return <div className="empty">Item not found.</div>;

  return (
    <div className="item-detail">
      <button className="back-link" onClick={() => navigate(-1)}>
        ← Back
      </button>
      <ul className="item-list">
        <li>
          <ItemCard
            env={env}
            item={item}
            projects={projects}
            expanded={expanded}
            onExpand={() => setExpanded(true)}
            onCollapse={() => setExpanded(false)}
          />
        </li>
      </ul>
    </div>
  );
}

function slugify(text: string): string {
  return text.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 50) || 'untitled';
}

function NewProjectForm({ env }: { env: string }) {
  const qc = useQueryClient();
  const [open, setOpen] = useState(false);
  const [title, setTitle] = useState('');
  const [outcome, setOutcome] = useState('');
  const [due, setDue] = useState('');
  const [priority, setPriority] = useState<string>('');
  const [sequential, setSequential] = useState(false);

  const generatedId = title.trim()
    ? `${new Date().toISOString().slice(0, 10)}-${slugify(title)}`
    : '';

  const mut = useMutation({
    mutationFn: () =>
      api.createProject(env, {
        id: generatedId,
        title: title.trim(),
        outcome: outcome || undefined,
        due: due || undefined,
        priority: priority ? parseInt(priority, 10) : undefined,
        sequential,
      }),
    onSuccess: () => {
      setOpen(false);
      setTitle('');
      setOutcome('');
      setDue('');
      setPriority('');
      setSequential(false);
      qc.invalidateQueries({ queryKey: ['projects', env] });
      qc.invalidateQueries({ queryKey: ['search-corpus', env], refetchType: 'none' });
      qc.invalidateQueries({ queryKey: ['snapshot-status'] });
    },
  });

  if (!open) return <button onClick={() => setOpen(true)}>+ New project</button>;

  return (
    <div className="editor">
      <label>
        Title
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          autoFocus
        />
      </label>
      <label>
        Outcome (what "done" looks like)
        <input
          type="text"
          value={outcome}
          onChange={(e) => setOutcome(e.target.value)}
        />
      </label>
      <div className="row">
        <label>
          Due
          <input
            type="date"
            value={due}
            onChange={(e) => setDue(e.target.value)}
          />
        </label>
        <label>
          Priority
          <select value={priority} onChange={(e) => setPriority(e.target.value)}>
            <option value="">—</option>
            {[1, 2, 3, 4, 5].map((n) => (
              <option key={n} value={n}>{PRIORITY_LABELS[n]}</option>
            ))}
          </select>
        </label>
      </div>
      <label className="toggle-row">
        <input
          type="checkbox"
          checked={sequential}
          onChange={(e) => setSequential(e.target.checked)}
        />
        <span>Sequential — do one step at a time (hides later steps from next list)</span>
      </label>
      <div className="row">
        <Button
          className="primary"
          onClick={() => mut.mutate()}
          disabled={!title.trim()}
          busy={mut.isPending}
        >
          Create
        </Button>
        <button onClick={() => setOpen(false)}>Cancel</button>
      </div>
    </div>
  );
}

function SortableActionList({
  env,
  projectId,
  items,
}: {
  env: string;
  projectId: string;
  items: Item[];
}) {
  const qc = useQueryClient();
  // Local ordering override — starts with the server's order but updates
  // optimistically on drop so the UI doesn't wait for the round trip.
  const [localOrder, setLocalOrder] = useState<string[] | null>(null);
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const ids = localOrder ?? items.map((i) => i.id);
  const itemsById = new Map(items.map((i) => [i.id, i]));
  const { data: projects } = useQuery({
    queryKey: ['projects', env, false],
    queryFn: () => api.listProjects(env, false),
  });

  const sensors = useSensors(
    useSensor(PointerSensor, { activationConstraint: { distance: 5 } }),
    useSensor(KeyboardSensor, { coordinateGetter: sortableKeyboardCoordinates })
  );

  const reorderMut = useMutation({
    mutationFn: (itemIds: string[]) =>
      api.reorderProjectItems(env, projectId, itemIds),
    onSuccess: () => {
      setLocalOrder(null);
      qc.invalidateQueries({ queryKey: ['project', env, projectId] });
      qc.invalidateQueries({ queryKey: ['items', env] });
      qc.invalidateQueries({ queryKey: ['search-corpus', env], refetchType: 'none' });
      qc.invalidateQueries({ queryKey: ['snapshot-status'] });
    },
    onError: () => {
      // Roll back the optimistic order on failure; the global toast handler
      // already surfaces the error message.
      setLocalOrder(null);
    },
  });

  if (items.length === 0) return <div className="empty">Nothing here.</div>;

  function onDragEnd(event: DragEndEvent) {
    const { active, over } = event;
    if (!over || active.id === over.id) return;
    const oldIndex = ids.indexOf(String(active.id));
    const newIndex = ids.indexOf(String(over.id));
    if (oldIndex < 0 || newIndex < 0) return;
    const next = arrayMove(ids, oldIndex, newIndex);
    setLocalOrder(next);
    reorderMut.mutate(next);
  }

  return (
    <DndContext sensors={sensors} collisionDetection={closestCenter} onDragEnd={onDragEnd}>
      <SortableContext items={ids} strategy={verticalListSortingStrategy}>
        <ul className="item-list sortable">
          {ids.map((id) => {
            const item = itemsById.get(id);
            if (!item) return null;
            return (
              <SortableItemRow
                key={id}
                env={env}
                item={item}
                projects={projects}
                expanded={expandedId === id}
                onExpand={() => setExpandedId(id)}
                onCollapse={() =>
                  setExpandedId((cur) => (cur === id ? null : cur))
                }
              />
            );
          })}
        </ul>
      </SortableContext>
    </DndContext>
  );
}

function SortableItemRow({
  env,
  item,
  projects,
  expanded,
  onExpand,
  onCollapse,
}: {
  env: string;
  item: Item;
  projects: Project[] | undefined;
  expanded: boolean;
  onExpand: () => void;
  onCollapse: () => void;
}) {
  const { attributes, listeners, setNodeRef, transform, transition, isDragging } =
    useSortable({ id: item.id });
  const style: React.CSSProperties = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0.5 : 1,
  };
  return (
    <li ref={setNodeRef} style={style}>
      <div className="item-with-handle">
        <button
          type="button"
          className="drag-handle"
          aria-label="Drag to reorder"
          {...attributes}
          {...listeners}
        >
          ⋮⋮
        </button>
        <div className="item-with-handle-body">
          <ItemCard
            env={env}
            item={item}
            projects={projects}
            expanded={expanded}
            onExpand={onExpand}
            onCollapse={onCollapse}
          />
        </div>
      </div>
    </li>
  );
}

function ProjectEditor({
  env,
  project,
  onClose,
}: {
  env: string;
  project: Project;
  onClose?: () => void;
}) {
  const qc = useQueryClient();
  const [title, setTitle] = useState(project.title);
  const [outcome, setOutcome] = useState(project.outcome ?? '');
  const [due, setDue] = useState(project.due ?? '');
  const [priority, setPriority] = useState<string>(
    project.priority?.toString() ?? ''
  );
  const [sequential, setSequential] = useState(project.sequential);
  const [body, setBody] = useState(project.body);

  const mut = useMutation({
    mutationFn: () =>
      api.updateProject(env, project.id, {
        title,
        outcome: outcome || null,
        due: due || null,
        priority: priority ? parseInt(priority, 10) : null,
        sequential,
        body,
      }),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['projects', env] });
      qc.invalidateQueries({ queryKey: ['project', env, project.id] });
      qc.invalidateQueries({ queryKey: ['search-corpus', env], refetchType: 'none' });
      qc.invalidateQueries({ queryKey: ['snapshot-status'] });
      onClose?.();
    },
  });

  return (
    <div className="editor">
      <label>
        Title
        <input type="text" value={title} onChange={(e) => setTitle(e.target.value)} />
      </label>
      <label>
        Outcome
        <input type="text" value={outcome} onChange={(e) => setOutcome(e.target.value)} />
      </label>
      <div className="row">
        <label>
          Due
          <input
            type="date"
            value={due}
            onChange={(e) => setDue(e.target.value)}
          />
        </label>
        <label>
          Priority
          <select value={priority} onChange={(e) => setPriority(e.target.value)}>
            <option value="">—</option>
            {[1, 2, 3, 4, 5].map((n) => (
              <option key={n} value={n}>{PRIORITY_LABELS[n]}</option>
            ))}
          </select>
        </label>
      </div>
      <label className="toggle-row">
        <input
          type="checkbox"
          checked={sequential}
          onChange={(e) => setSequential(e.target.checked)}
        />
        <span>Sequential — only the first ordered step shows on the next list</span>
      </label>
      <label>
        Notes
        <textarea rows={3} value={body} onChange={(e) => setBody(e.target.value)} />
      </label>
      <Button className="primary" onClick={() => mut.mutate()} busy={mut.isPending}>
        Save
      </Button>
    </div>
  );
}

// ---- Item list ----

function ItemList({ env, items }: { env: string; items: Item[] }) {
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const { data: projects } = useQuery({
    queryKey: ['projects', env, false],
    queryFn: () => api.listProjects(env, false),
  });
  if (items.length === 0) return <div className="empty">Nothing here.</div>;
  return (
    <ul className="item-list">
      {items.map((item) => (
        <li key={item.id}>
          <ItemCard
            env={env}
            item={item}
            projects={projects}
            expanded={expandedId === item.id}
            onExpand={() => setExpandedId(item.id)}
            onCollapse={() =>
              setExpandedId((id) => (id === item.id ? null : id))
            }
          />
        </li>
      ))}
    </ul>
  );
}

