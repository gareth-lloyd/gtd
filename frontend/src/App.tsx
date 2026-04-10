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
    // Reset filters when switching envs (contexts list differs)
    setContexts([]);
  }, [env]);

  if (!envs || envs.length === 0) return <div className="app-loading">Loading…</div>;
  if (!env) return <div className="app-loading">Choose an environment</div>;

  const showFilters = FILTER_TABS.includes(tab);

  return (
    <div className={showFilters ? 'app' : 'app no-filters'}>
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
  const [expanded, setExpanded] = useState(false);
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
      setExpanded(false);
      qc.invalidateQueries({ queryKey: ['items', env] });
      qc.invalidateQueries({ queryKey: ['snapshot-status'] });
    },
  });

  return (
    <form
      className={expanded ? 'capture expanded' : 'capture'}
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
        <button
          type="button"
          className="expand"
          onClick={() => setExpanded(!expanded)}
          title={expanded ? 'Hide notes' : 'Add notes'}
        >
          {expanded ? '▲' : '▼'}
        </button>
        <button type="submit" className="primary" disabled={!title.trim()}>
          Capture
        </button>
      </div>
      {expanded && (
        <>
          <textarea
            rows={4}
            placeholder="Notes (markdown supported)…"
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
          />
          <div className="capture-hint">
            Captured with energy=low, time=5min. Adjust later via Edit.
          </div>
        </>
      )}
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
      <button
        onClick={() => {
          const msg = prompt('Snapshot message (optional):') || undefined;
          snap.mutate(msg);
        }}
        disabled={count === 0 || snap.isPending}
      >
        Sync
      </button>
    </div>
  );
}

// ---- Filter panel ----

const ENERGY_CHOICES: (Energy | '')[] = ['', 'low', 'medium', 'high'];

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
          <label key={c} className="check-row">
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
        <h3>Time (max min)</h3>
        <input
          type="number"
          value={maxMinutes}
          onChange={(e) => setMaxMinutes(e.target.value)}
          placeholder="any"
          min={0}
        />
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

  const { data: items } = useQuery({
    queryKey: ['items', env, 'next', contexts, energy, maxMinutes],
    queryFn: () => api.listItems(env, params),
  });

  return <ItemList env={env} items={items ?? []} showEdit />;
}

// ---- Bucket view (inbox/waiting/someday/reference/trash) ----

function BucketView({ env, bucket }: { env: string; bucket: Bucket }) {
  const { data: items } = useQuery({
    queryKey: ['items', env, bucket],
    queryFn: () => api.listItems(env, { status: bucket }),
  });
  return <ItemList env={env} items={items ?? []} showEdit />;
}

// ---- Projects view ----

function ProjectsView({ env }: { env: string }) {
  const { data: projects } = useQuery({
    queryKey: ['projects', env],
    queryFn: () => api.listProjects(env),
  });
  const [expanded, setExpanded] = useState<string | null>(null);

  return (
    <>
      <NewProjectForm env={env} />
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
        <button className="primary" onClick={() => mut.mutate()} disabled={!id || !title}>
          Create
        </button>
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
  const { data } = useQuery({
    queryKey: ['project', env, project.id],
    queryFn: () => api.getProject(env, project.id),
    enabled: expanded,
  });

  return (
    <div className="project-card">
      <h3 onClick={onToggle} style={{ cursor: 'pointer' }}>
        {expanded ? '▼' : '▶'} {project.title}
      </h3>
      {project.outcome && <div className="outcome">{project.outcome}</div>}
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
  };
  const moveMut = useMutation({
    mutationFn: (to: Bucket) => api.moveItem(env, item.id, to),
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
          <span key={c} className="chip">
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
            <button onClick={() => moveMut.mutate('inbox')}>↺ restore</button>
            <button
              className="danger"
              onClick={() => {
                if (confirm(`Permanently delete "${item.title}"?`)) purgeMut.mutate();
              }}
            >
              Purge
            </button>
          </>
        ) : (
          <>
            {item.status !== 'next' && !isArchive && (
              <button onClick={() => moveMut.mutate('next')}>→ next</button>
            )}
            {item.status !== 'waiting' && !isArchive && (
              <button onClick={() => moveMut.mutate('waiting')}>→ waiting</button>
            )}
            {item.status !== 'someday' && !isArchive && (
              <button onClick={() => moveMut.mutate('someday')}>→ someday</button>
            )}
            {!isArchive && <button onClick={() => completeMut.mutate()}>✓ done</button>}
            {showEdit && <button onClick={onEdit}>{editing ? 'Close' : 'Edit'}</button>}
            <button className="danger" onClick={() => deleteMut.mutate()}>
              Delete
            </button>
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
  const [error, setError] = useState<string | null>(null);

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
      setError(null);
      qc.invalidateQueries({ queryKey: ['items', env] });
      qc.invalidateQueries({ queryKey: ['snapshot-status'] });
    },
    onError: (e: Error) => setError(e.message),
  });

  return (
    <div className="editor">
      {error && <div className="error">{error}</div>}
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
            <label key={c} className="chip-check">
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
      <button className="primary" onClick={() => mut.mutate()} disabled={mut.isPending}>
        Save
      </button>
    </div>
  );
}
