import { useEffect, useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
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

type Tab =
  | 'next'
  | 'inbox'
  | 'projects'
  | 'waiting'
  | 'someday'
  | 'reference'
  | 'trash';

const TABS: Tab[] = [
  'next',
  'inbox',
  'projects',
  'waiting',
  'someday',
  'reference',
  'trash',
];

const FILTER_TABS: Tab[] = ['next'];

const ENERGY_CHOICES: (Energy | '')[] = ['', 'low', 'medium', 'high'];

// ---- Context colors (deterministic from name) ----

function contextHue(name: string): number {
  let h = 0;
  for (let i = 0; i < name.length; i++) h = (h + name.charCodeAt(i) * 37) % 360;
  return h;
}

function contextChipStyle(name: string): React.CSSProperties {
  const h = contextHue(name);
  return {
    backgroundColor: `hsl(${h}, 60%, 90%)`,
    color: `hsl(${h}, 50%, 30%)`,
  };
}

function contextTintStyle(selected: string[]): React.CSSProperties | undefined {
  if (selected.length === 0) return undefined;
  const avg = selected.reduce((sum, c) => sum + contextHue(c), 0) / selected.length;
  return { backgroundColor: `hsl(${avg}, 25%, 97%)` };
}

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

  const [contexts, setContexts] = useState<string[]>([]);
  const [energy, setEnergy] = useState<Energy | ''>('');
  const [maxMinutes, setMaxMinutes] = useState<string>('');

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
  }, [env]);

  if (!envs || envs.length === 0) return <div className="app-loading">Loading…</div>;
  if (!env) return <div className="app-loading">Choose an environment</div>;

  const showFilters = FILTER_TABS.includes(tab);

  return (
    <div className={showFilters ? 'app' : 'app no-filters'} style={contextTintStyle(contexts)}>
      <header>
        <h1>
          <span className="brand">gtd</span>
        </h1>
        <EnvTabs envs={envs} env={env} onChange={setEnv} />
        <div className="spacer" />
        <SyncButton />
      </header>

      <nav className="side-nav">
        {TABS.map((t) => (
          <button
            key={t}
            className={tab === t ? 'active' : ''}
            onClick={() => setTab(t)}
          >
            {t}
          </button>
        ))}
      </nav>

      <main>
        <CaptureBar env={env} />
        {tab === 'next' && (
          <NextActionsView
            env={env}
            contexts={contexts}
            energy={energy}
            maxMinutes={maxMinutes}
          />
        )}
        {tab === 'inbox' && <BucketView env={env} bucket="inbox" />}
        {tab === 'projects' && <ProjectsView env={env} />}
        {(tab === 'waiting' ||
          tab === 'someday' ||
          tab === 'reference' ||
          tab === 'trash') && <BucketView env={env} bucket={tab} />}
      </main>

      {showFilters && (
        <aside className="side-filters">
          <FilterPanel
            config={config}
            contexts={contexts}
            setContexts={setContexts}
            energy={energy}
            setEnergy={setEnergy}
            maxMinutes={maxMinutes}
            setMaxMinutes={setMaxMinutes}
          />
        </aside>
      )}
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

function CaptureBar({ env }: { env: string }) {
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

function ProjectsView({ env }: { env: string }) {
  const [showFinished, setShowFinished] = useState(false);
  const { data: projects, isLoading } = useQuery({
    queryKey: ['projects', env, showFinished],
    queryFn: () => api.listProjects(env, showFinished),
  });
  const [expanded, setExpanded] = useState<string | null>(null);

  if (isLoading) return <div className="empty">Loading…</div>;

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
      {projects?.length === 0 && <div className="empty">No projects yet.</div>}
      {projects?.map((p) => (
        <ProjectCard
          key={p.id}
          env={env}
          project={p}
          expanded={expanded === p.id}
          onToggle={() => setExpanded(expanded === p.id ? null : p.id)}
        />
      ))}
    </>
  );
}

function NewProjectForm({ env }: { env: string }) {
  const qc = useQueryClient();
  const [open, setOpen] = useState(false);
  const [id, setId] = useState('');
  const [title, setTitle] = useState('');
  const [outcome, setOutcome] = useState('');
  const mut = useMutation({
    mutationFn: () => api.createProject(env, { id, title, outcome }),
    onSuccess: () => {
      setOpen(false);
      setId('');
      setTitle('');
      setOutcome('');
      qc.invalidateQueries({ queryKey: ['projects', env] });
      qc.invalidateQueries({ queryKey: ['snapshot-status'] });
    },
  });

  if (!open) return <button onClick={() => setOpen(true)}>+ New project</button>;

  return (
    <div className="editor">
      <div className="row">
        <label>
          ID
          <input
            type="text"
            value={id}
            onChange={(e) => setId(e.target.value)}
            placeholder="2026-04-10-my-project"
          />
        </label>
        <label>
          Title
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />
        </label>
      </div>
      <label>
        Outcome (what "done" looks like)
        <input
          type="text"
          value={outcome}
          onChange={(e) => setOutcome(e.target.value)}
        />
      </label>
      <div className="row">
        <Button
          className="primary"
          onClick={() => mut.mutate()}
          disabled={!id || !title}
          busy={mut.isPending}
        >
          Create
        </Button>
        <button onClick={() => setOpen(false)}>Cancel</button>
      </div>
    </div>
  );
}

function ProjectCard({
  env,
  project,
  expanded,
  onToggle,
}: {
  env: string;
  project: Project;
  expanded: boolean;
  onToggle: () => void;
}) {
  const qc = useQueryClient();
  const { data } = useQuery({
    queryKey: ['project', env, project.id],
    queryFn: () => api.getProject(env, project.id),
    enabled: expanded,
  });

  const invalidate = () => {
    qc.invalidateQueries({ queryKey: ['projects', env] });
    qc.invalidateQueries({ queryKey: ['project', env, project.id] });
    qc.invalidateQueries({ queryKey: ['snapshot-status'] });
  };

  const statusMut = useMutation<Project, Error, string>({
    mutationFn: (status) => api.updateProject(env, project.id, { status }),
    onSuccess: invalidate,
  });

  const deleteMut = useMutation({
    mutationFn: () => api.deleteProject(env, project.id),
    onSuccess: invalidate,
  });

  const isDone = project.status === 'complete' || project.status === 'dropped';
  const anyPending = statusMut.isPending || deleteMut.isPending;

  return (
    <div className={isDone ? 'project-card done' : 'project-card'}>
      <h3 onClick={onToggle} style={{ cursor: 'pointer' }}>
        {expanded ? '▼' : '▶'} {project.title}
        {project.status !== 'active' && (
          <span className="project-status">{project.status}</span>
        )}
      </h3>
      {project.outcome && <div className="outcome">{project.outcome}</div>}
      <div className="project-actions">
        {project.status !== 'complete' && (
          <Button
            onClick={() => statusMut.mutate('complete')}
            busy={statusMut.isPending && statusMut.variables === 'complete'}
            disabled={anyPending}
          >
            ✓ Mark complete
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
            ⏸ Put on hold
          </Button>
        )}
        <Button
          className="danger"
          onClick={() => {
            if (confirm(`Delete project "${project.title}"? Actions linked to it will not be deleted.`)) {
              deleteMut.mutate();
            }
          }}
          busy={deleteMut.isPending}
          disabled={anyPending}
        >
          Delete
        </Button>
      </div>
      {expanded && data && (
        <ItemList env={env} items={data.actions} showEdit={false} />
      )}
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
    qc.invalidateQueries({ queryKey: ['project', env] });
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

  const rowBusy =
    moveMut.isPending ||
    completeMut.isPending ||
    deleteMut.isPending ||
    purgeMut.isPending;

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
            {item.status !== 'next' && !isArchive && (
              <Button
                onClick={() => moveMut.mutate('next')}
                busy={isMoving('next')}
                disabled={rowBusy}
              >
                → next
              </Button>
            )}
            {item.status !== 'waiting' && !isArchive && (
              <Button
                onClick={() => moveMut.mutate('waiting')}
                busy={isMoving('waiting')}
                disabled={rowBusy}
              >
                → waiting
              </Button>
            )}
            {item.status !== 'someday' && !isArchive && (
              <Button
                onClick={() => moveMut.mutate('someday')}
                busy={isMoving('someday')}
                disabled={rowBusy}
              >
                → someday
              </Button>
            )}
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
      {editing && <ItemEditor env={env} item={item} />}
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
          Due
          <input
            type="text"
            value={due}
            onChange={(e) => setDue(e.target.value)}
            placeholder="e.g. next friday, 2w, end of month"
          />
        </label>
        <label>
          Defer until
          <input
            type="text"
            value={deferUntil}
            onChange={(e) => setDeferUntil(e.target.value)}
            placeholder="e.g. tomorrow, 3d, Apr 30"
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
