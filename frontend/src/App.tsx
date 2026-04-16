import React, { useEffect, useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
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
import { contextHue, contextChipStyle, contextTintStyle } from './context-colors';

type Tab =
  | 'next'
  | 'inbox'
  | 'projects'
  | 'waiting'
  | 'someday'
  | 'reference'
  | 'trash';

const TABS: Tab[] = [
  'inbox',
  'next',
  'projects',
  'waiting',
  'someday',
  'reference',
  'trash',
];

const FILTER_TABS: Tab[] = ['next'];

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
  const [env, setEnv] = useState<string>(
    () => localStorage.getItem('gtd:env') || ''
  );
  const [tab, setTab] = useState<Tab>('next');
  const [activeProjectId, setActiveProjectId] = useState<string | null>(null);

  const [contexts, setContexts] = useState<string[]>([]);
  const [energy, setEnergy] = useState<Energy | ''>('');
  const [maxMinutes, setMaxMinutes] = useState<string>('');
  const [captureOpen, setCaptureOpen] = useState(false);

  const { data: envs } = useQuery({
    queryKey: ['envs'],
    queryFn: api.listEnvs,
  });

  const { data: config } = useQuery({
    queryKey: ['config', env],
    queryFn: () => api.getConfig(env),
    enabled: !!env,
  });

  useEffect(() => {
    if (!env && envs && envs.length > 0) setEnv(envs[0].name);
  }, [envs, env]);

  useEffect(() => {
    if (env) localStorage.setItem('gtd:env', env);
  }, [env]);

  useEffect(() => {
    setContexts([]);
    setActiveProjectId(null);
  }, [env]);

  if (!envs || envs.length === 0) return <div className="app-loading">Loading…</div>;
  if (!env) return <div className="app-loading">Choose an environment</div>;

  const showFilters = FILTER_TABS.includes(tab);

  return (
    <div className={showFilters ? 'app' : 'app no-filters'} style={contextTintStyle(contexts)}>
      <header>
        <div className="header-row">
          <h1>
            <span className="brand">gtd</span>
          </h1>
          <EnvTabs envs={envs} env={env} onChange={setEnv} />
          {tab !== 'inbox' && (
            <button
              className={captureOpen ? 'active' : ''}
              onClick={() => setCaptureOpen((v) => !v)}
            >
              {captureOpen ? 'Close capture' : '+ Capture'}
            </button>
          )}
          <div className="spacer" />
          <SyncButton />
        </div>
        {(tab === 'inbox' || captureOpen) && (
          <CaptureBar
            env={env}
            onCaptured={() => setCaptureOpen(false)}
          />
        )}
      </header>

      <nav className="side-nav">
        {TABS.map((t) => (
          <React.Fragment key={t}>
            <button
              className={tab === t && !(t === 'projects' && activeProjectId) ? 'active' : ''}
              onClick={() => {
                setTab(t);
                if (t === 'projects') setActiveProjectId(null);
              }}
            >
              {t}
            </button>
            {t === 'projects' && (
              <ProjectNavLinks
                env={env}
                activeProjectId={tab === 'projects' ? activeProjectId : null}
                onSelect={(id) => {
                  setTab('projects');
                  setActiveProjectId(id);
                }}
              />
            )}
          </React.Fragment>
        ))}
      </nav>

      <main>
        {tab === 'next' && (
          <NextActionsView
            env={env}
            contexts={contexts}
            energy={energy}
            maxMinutes={maxMinutes}
          />
        )}
        {tab === 'inbox' && <BucketView env={env} bucket="inbox" />}
        {tab === 'projects' && activeProjectId && (
          <ProjectDetailView
            env={env}
            projectId={activeProjectId}
            onBack={() => setActiveProjectId(null)}
          />
        )}
        {tab === 'projects' && !activeProjectId && (
          <ProjectsView
            env={env}
            onOpen={(id) => setActiveProjectId(id)}
          />
        )}
        {(tab === 'waiting' ||
          tab === 'someday' ||
          tab === 'reference' ||
          tab === 'trash') && <BucketView env={env} bucket={tab} />}
      </main>

      <aside className="side-filters">
        {showFilters && (
          <FilterPanel
            config={config}
            contexts={contexts}
            setContexts={setContexts}
            energy={energy}
            setEnergy={setEnergy}
            maxMinutes={maxMinutes}
            setMaxMinutes={setMaxMinutes}
          />
        )}
      </aside>
    </div>
  );
}

// ---- Env tabs ----

function EnvTabs({
  envs,
  env,
  onChange,
}: {
  envs: EnvSummary[];
  env: string;
  onChange: (env: string) => void;
}) {
  return (
    <div className="env-tabs">
      {envs.map((e) => (
        <button
          key={e.name}
          className={env === e.name ? 'env-tab active' : 'env-tab'}
          onClick={() => onChange(e.name)}
        >
          {e.name}
        </button>
      ))}
    </div>
  );
}

// ---- Capture bar ----

function CaptureBar({
  env,
  onCaptured,
}: {
  env: string;
  onCaptured?: () => void;
}) {
  const [title, setTitle] = useState('');
  const [notes, setNotes] = useState('');
  const qc = useQueryClient();

  const mut = useMutation({
    mutationFn: () =>
      api.captureItem(env, title.trim(), notes, {
        energy: 'low',
        time_minutes: 5,
      }),
    onSuccess: () => {
      setTitle('');
      setNotes('');
      qc.invalidateQueries({ queryKey: ['items', env] });
      qc.invalidateQueries({ queryKey: ['snapshot-status'] });
      onCaptured?.();
    },
  });

  return (
    <form
      className="capture"
      onSubmit={(e) => {
        e.preventDefault();
        if (title.trim()) mut.mutate();
      }}
    >
      <div className="capture-row">
        <input
          type="text"
          placeholder="Capture to inbox…"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          autoFocus
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
      <div className="capture-hint">
        Captured with energy=low, time=5min. Adjust later via Edit.
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

function FilterPanel({
  config,
  contexts,
  setContexts,
  energy,
  setEnergy,
  maxMinutes,
  setMaxMinutes,
}: {
  config: EnvConfig | undefined;
  contexts: string[];
  setContexts: (updater: (prev: string[]) => string[]) => void;
  energy: Energy | '';
  setEnergy: (e: Energy | '') => void;
  maxMinutes: string;
  setMaxMinutes: (s: string) => void;
}) {
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
    </div>
  );
}

// ---- Next actions view ----

function NextActionsView({
  env,
  contexts,
  energy,
  maxMinutes,
}: {
  env: string;
  contexts: string[];
  energy: Energy | '';
  maxMinutes: string;
}) {
  const params: Record<string, string> = { status: 'next' };
  if (contexts.length) params.contexts = contexts.join(',');
  if (energy) params.energy = energy;
  if (maxMinutes) params.max_minutes = maxMinutes;

  const { data: items, isLoading } = useQuery({
    queryKey: ['items', env, 'next', contexts, energy, maxMinutes],
    queryFn: () => api.listItems(env, params),
  });

  if (isLoading) return <div className="empty">Loading…</div>;
  return <ItemList env={env} items={items ?? []} showEdit />;
}

// ---- Bucket view (inbox/waiting/someday/reference/trash) ----

function BucketView({ env, bucket }: { env: string; bucket: Bucket }) {
  const { data: items, isLoading } = useQuery({
    queryKey: ['items', env, bucket],
    queryFn: () => api.listItems(env, { status: bucket }),
  });
  if (isLoading) return <div className="empty">Loading…</div>;
  return <ItemList env={env} items={items ?? []} showEdit />;
}

// ---- Projects view ----

const PRIORITY_LABELS: Record<number, string> = {
  1: 'P1 critical',
  2: 'P2 high',
  3: 'P3 medium',
  4: 'P4 low',
  5: 'P5 aspirational',
};

function sortProjects(projects: Project[]): Project[] {
  return [...projects].sort((a, b) => {
    const pa = a.priority ?? 99;
    const pb = b.priority ?? 99;
    if (pa !== pb) return pa - pb;
    if (a.due && b.due) return a.due.localeCompare(b.due);
    if (a.due) return -1;
    if (b.due) return 1;
    return a.title.localeCompare(b.title);
  });
}

function ProjectsView({
  env,
  onOpen,
}: {
  env: string;
  onOpen: (id: string) => void;
}) {
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
            <ProjectIndexRow project={p} onOpen={() => onOpen(p.id)} />
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

function ProjectIndexRow({
  project,
  onOpen,
}: {
  project: Project;
  onOpen: () => void;
}) {
  const isDone = project.status === 'complete' || project.status === 'dropped';
  return (
    <button
      type="button"
      className={`project-index-row${isDone ? ' done' : ''}`}
      onClick={onOpen}
    >
      <span className="project-index-title">{project.title}</span>
      <ProjectBadges project={project} />
      {project.due && <span className="chip">due {project.due}</span>}
      {project.outcome && (
        <span className="project-index-outcome">{project.outcome}</span>
      )}
    </button>
  );
}

function ProjectNavLinks({
  env,
  activeProjectId,
  onSelect,
}: {
  env: string;
  activeProjectId: string | null;
  onSelect: (id: string) => void;
}) {
  const { data: projects } = useQuery({
    queryKey: ['projects', env, false],
    queryFn: () => api.listProjects(env, false),
  });
  if (!projects || projects.length === 0) return null;
  return (
    <div className="side-nav-sub">
      {sortProjects(projects).map((p) => (
        <button
          key={p.id}
          className={activeProjectId === p.id ? 'sub-link active' : 'sub-link'}
          onClick={() => onSelect(p.id)}
          title={p.title}
        >
          {p.priority != null && (
            <span className={`priority-dot p${p.priority}`}>●</span>
          )}
          <span className="sub-link-title">{p.title}</span>
        </button>
      ))}
    </div>
  );
}

function ProjectDetailView({
  env,
  projectId,
  onBack,
}: {
  env: string;
  projectId: string;
  onBack: () => void;
}) {
  const qc = useQueryClient();
  const [editing, setEditing] = useState(false);
  const { data, isLoading } = useQuery({
    queryKey: ['project', env, projectId],
    queryFn: () => api.getProject(env, projectId),
  });

  const invalidate = () => {
    qc.invalidateQueries({ queryKey: ['projects', env] });
    qc.invalidateQueries({ queryKey: ['project', env, projectId] });
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
      onBack();
    },
  });

  if (isLoading || !data) return <div className="empty">Loading…</div>;

  const { project, actions } = data;
  const isDone = project.status === 'complete' || project.status === 'dropped';
  const anyPending = statusMut.isPending || deleteMut.isPending;

  return (
    <div className="project-detail">
      <button className="back-link" onClick={onBack}>
        ← All projects
      </button>
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
        {editing && <ProjectEditor env={env} project={project} />}
        <SortableActionList env={env} projectId={project.id} items={actions} />
      </div>
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
  const ids = localOrder ?? items.map((i) => i.id);
  const itemsById = new Map(items.map((i) => [i.id, i]));

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
            return <SortableItemRow key={id} env={env} item={item} />;
          })}
        </ul>
      </SortableContext>
    </DndContext>
  );
}

function SortableItemRow({ env, item }: { env: string; item: Item }) {
  const { attributes, listeners, setNodeRef, transform, transition, isDragging } =
    useSortable({ id: item.id });
  const [editing, setEditing] = useState(false);
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
          <ItemRow
            env={env}
            item={item}
            editing={editing}
            onEdit={() => setEditing(!editing)}
            showEdit
          />
        </div>
      </div>
    </li>
  );
}

function ProjectEditor({ env, project }: { env: string; project: Project }) {
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
      qc.invalidateQueries({ queryKey: ['snapshot-status'] });
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

// ---- Item list + editor ----

function ItemList({
  env,
  items,
  showEdit,
}: {
  env: string;
  items: Item[];
  showEdit: boolean;
}) {
  const [editing, setEditing] = useState<string | null>(null);
  if (items.length === 0) return <div className="empty">Nothing here.</div>;
  return (
    <ul className="item-list">
      {items.map((item) => (
        <li key={item.id}>
          <ItemRow
            env={env}
            item={item}
            editing={editing === item.id}
            onEdit={() => setEditing(editing === item.id ? null : item.id)}
            showEdit={showEdit}
          />
        </li>
      ))}
    </ul>
  );
}

function ItemRow({
  env,
  item,
  editing,
  onEdit,
  showEdit,
}: {
  env: string;
  item: Item;
  editing: boolean;
  onEdit: () => void;
  showEdit: boolean;
}) {
  const qc = useQueryClient();
  const invalidate = () => {
    qc.invalidateQueries({ queryKey: ['items', env] });
    qc.invalidateQueries({ queryKey: ['snapshot-status'] });
    qc.invalidateQueries({ queryKey: ['projects', env] });
    if (item.project) {
      qc.invalidateQueries({ queryKey: ['project', env, item.project] });
    }
  };

  const moveMut = useMutation<Item, Error, Bucket>({
    mutationFn: (to) => api.moveItem(env, item.id, to),
    onSuccess: invalidate,
  });
  const completeMut = useMutation({
    mutationFn: () => api.completeItem(env, item.id),
    onSuccess: invalidate,
  });
  const deleteMut = useMutation({
    mutationFn: () => api.deleteItem(env, item.id),
    onSuccess: invalidate,
  });
  const purgeMut = useMutation({
    mutationFn: () => api.purgeItem(env, item.id),
    onSuccess: invalidate,
  });
  const assignProjectMut = useMutation<Item, Error, string>({
    mutationFn: async (projectId) => {
      const updated = await api.updateItem(env, item.id, { project: projectId });
      if (item.status === 'inbox') {
        return api.moveItem(env, item.id, 'next');
      }
      return updated;
    },
    onSuccess: invalidate,
  });

  const rowBusy =
    moveMut.isPending ||
    completeMut.isPending ||
    deleteMut.isPending ||
    purgeMut.isPending ||
    assignProjectMut.isPending;

  const isMoving = (to: Bucket) =>
    moveMut.isPending && moveMut.variables === to;

  const inTrash = item.status === 'trash';
  const isArchive = item.status === 'archive';

  return (
    <div className="item">
      <div className="item-title">{item.title}</div>
      {item.body && (
        <div className="item-body">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>{item.body}</ReactMarkdown>
        </div>
      )}
      <div className="item-meta">
        {item.status !== 'next' && <span className="chip">{item.status}</span>}
        {item.order != null && <span className="chip">#{item.order}</span>}
        {item.contexts.map((c) => (
          <span key={c} className="chip context-chip" style={contextChipStyle(c)}>
            @{c}
          </span>
        ))}
        {item.energy && <span className="chip">⚡{item.energy}</span>}
        {item.time_minutes != null && <span className="chip">{item.time_minutes}m</span>}
        {item.area && <span className="chip">{item.area}</span>}
        {item.due && <span className="chip">due {item.due}</span>}
        {item.defer_until && <span className="chip">defer {item.defer_until}</span>}
        <span className="chip dates" title={`created ${fmtDate(item.created)}`}>
          updated {fmtDate(item.updated)}
        </span>
      </div>
      <div className="item-actions">
        {inTrash ? (
          <>
            <Button
              onClick={() => moveMut.mutate('inbox')}
              busy={isMoving('inbox')}
              disabled={rowBusy}
            >
              ↺ restore
            </Button>
            <Button
              className="danger"
              onClick={() => {
                if (confirm(`Permanently delete "${item.title}"?`)) purgeMut.mutate();
              }}
              busy={purgeMut.isPending}
              disabled={rowBusy}
            >
              Purge
            </Button>
          </>
        ) : (
          <>
            {(['next', 'waiting', 'someday'] as const)
              .filter((b) => item.status !== b && !isArchive)
              .map((b) => (
                <Button
                  key={b}
                  onClick={() => moveMut.mutate(b)}
                  busy={isMoving(b)}
                  disabled={rowBusy}
                >
                  → {b}
                </Button>
              ))}
            {!isArchive && (
              <Button
                onClick={() => completeMut.mutate()}
                busy={completeMut.isPending}
                disabled={rowBusy}
              >
                ✓ done
              </Button>
            )}
            {showEdit && (
              <button onClick={onEdit} disabled={rowBusy}>
                {editing ? 'Close' : 'Edit'}
              </button>
            )}
            <Button
              className="danger"
              onClick={() => deleteMut.mutate()}
              busy={deleteMut.isPending}
              disabled={rowBusy}
            >
              Delete
            </Button>
          </>
        )}
      </div>
      {!inTrash && !isArchive && (
        <ProjectAssignRow
          env={env}
          currentProjectId={item.project}
          onAssign={(projectId) => assignProjectMut.mutate(projectId)}
          busyProjectId={
            assignProjectMut.isPending ? (assignProjectMut.variables ?? null) : null
          }
          disabled={rowBusy}
        />
      )}
      {editing && <ItemEditor env={env} item={item} />}
    </div>
  );
}

function ProjectAssignRow({
  env,
  currentProjectId,
  onAssign,
  busyProjectId,
  disabled,
}: {
  env: string;
  currentProjectId: string | null;
  onAssign: (projectId: string) => void;
  busyProjectId: string | null;
  disabled: boolean;
}) {
  const { data: projects } = useQuery({
    queryKey: ['projects', env, false],
    queryFn: () => api.listProjects(env, false),
  });
  if (!projects || projects.length === 0) return null;
  return (
    <div className="item-actions project-assign">
      {sortProjects(projects).map((p) => (
        <Button
          key={p.id}
          className={currentProjectId === p.id ? 'active' : ''}
          onClick={() => onAssign(p.id)}
          busy={busyProjectId === p.id}
          disabled={disabled}
        >
          → {p.title}
        </Button>
      ))}
    </div>
  );
}

function fmtDate(iso: string): string {
  if (!iso) return '';
  return iso.slice(0, 10);
}

function ItemEditor({ env, item }: { env: string; item: Item }) {
  const qc = useQueryClient();
  const { data: config } = useQuery({
    queryKey: ['config', env],
    queryFn: () => api.getConfig(env),
  });
  const [title, setTitle] = useState(item.title);
  const [contexts, setContexts] = useState<string[]>(item.contexts);
  const [energy, setEnergy] = useState<Energy | ''>(item.energy ?? '');
  const [timeMinutes, setTimeMinutes] = useState<string>(
    item.time_minutes?.toString() ?? ''
  );
  const [area, setArea] = useState<string>(item.area ?? '');
  const [project, setProject] = useState<string>(item.project ?? '');
  const [due, setDue] = useState<string>(item.due ?? '');
  const [deferUntil, setDeferUntil] = useState<string>(item.defer_until ?? '');
  const [order, setOrder] = useState<string>(item.order?.toString() ?? '');
  const [body, setBody] = useState<string>(item.body);

  const mut = useMutation({
    mutationFn: () =>
      api.updateItem(env, item.id, {
        title,
        body,
        contexts,
        energy: energy || null,
        time_minutes: timeMinutes ? parseInt(timeMinutes, 10) : null,
        area: area || null,
        project: project || null,
        due: due || null,
        defer_until: deferUntil || null,
        order: order ? parseInt(order, 10) : null,
      }),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['items', env] });
      qc.invalidateQueries({ queryKey: ['snapshot-status'] });
    },
  });

  return (
    <div className="editor">
      <label>
        Title
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
      </label>
      <label>
        Contexts
        <div className="chip-row">
          {config?.contexts.map((c) => (
            <label key={c} className="chip-check" style={contextChipStyle(c)}>
              <input
                type="checkbox"
                checked={contexts.includes(c)}
                onChange={(e) =>
                  setContexts((prev) =>
                    e.target.checked ? [...prev, c] : prev.filter((x) => x !== c)
                  )
                }
              />
              @{c}
            </label>
          ))}
        </div>
      </label>
      <div className="row">
        <label>
          Energy
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
        </label>
        <label>
          Time (min)
          <input
            type="number"
            value={timeMinutes}
            onChange={(e) => setTimeMinutes(e.target.value)}
          />
        </label>
        <label>
          Area
          <input
            type="text"
            value={area}
            onChange={(e) => setArea(e.target.value)}
            list={`areas-${env}`}
          />
          <datalist id={`areas-${env}`}>
            {config?.areas.map((a) => (
              <option key={a} value={a} />
            ))}
          </datalist>
        </label>
      </div>
      <div className="row">
        <label>
          Project ID
          <input
            type="text"
            value={project}
            onChange={(e) => setProject(e.target.value)}
            placeholder="optional"
          />
        </label>
        <label>
          Order
          <input
            type="number"
            value={order}
            onChange={(e) => setOrder(e.target.value)}
            placeholder="within project"
          />
        </label>
      </div>
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
          Defer until
          <input
            type="date"
            value={deferUntil}
            onChange={(e) => setDeferUntil(e.target.value)}
          />
        </label>
      </div>
      <label>
        Notes (markdown)
        <textarea
          rows={4}
          value={body}
          onChange={(e) => setBody(e.target.value)}
        />
      </label>
      <Button className="primary" onClick={() => mut.mutate()} busy={mut.isPending}>
        Save
      </Button>
    </div>
  );
}
