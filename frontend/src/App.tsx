import { useEffect, useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import {
  api,
  type Bucket,
  type Energy,
  type EnvConfig,
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

export default function App() {
  const [env, setEnv] = useState<string>(
    () => localStorage.getItem('gtd:env') || ''
  );
  const [tab, setTab] = useState<Tab>('next');

  const { data: envs } = useQuery({
    queryKey: ['envs'],
    queryFn: api.listEnvs,
  });

  useEffect(() => {
    if (!env && envs && envs.length > 0) setEnv(envs[0].name);
  }, [envs, env]);

  useEffect(() => {
    if (env) localStorage.setItem('gtd:env', env);
  }, [env]);

  if (!envs || envs.length === 0) return <div className="app">Loading…</div>;
  if (!env) return <div className="app">Choose an environment</div>;

  return (
    <div className="app">
      <header>
        <h1>gtd</h1>
        <select value={env} onChange={(e) => setEnv(e.target.value)}>
          {envs.map((e) => (
            <option key={e.name} value={e.name}>
              {e.name}
            </option>
          ))}
        </select>
        <div className="spacer" />
        <SyncButton />
      </header>

      <CaptureBar env={env} />

      <nav className="tabs">
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

      {tab === 'next' && <NextActionsView env={env} />}
      {tab === 'inbox' && <InboxView env={env} />}
      {tab === 'projects' && <ProjectsView env={env} />}
      {(tab === 'waiting' ||
        tab === 'someday' ||
        tab === 'reference' ||
        tab === 'trash') && <BucketView env={env} bucket={tab} />}
    </div>
  );
}

// ---- Capture bar ----

function CaptureBar({ env }: { env: string }) {
  const [title, setTitle] = useState('');
  const qc = useQueryClient();
  const mut = useMutation({
    mutationFn: (t: string) => api.captureItem(env, t),
    onSuccess: () => {
      setTitle('');
      qc.invalidateQueries({ queryKey: ['items', env] });
      qc.invalidateQueries({ queryKey: ['snapshot-status'] });
    },
  });

  return (
    <form
      className="capture"
      onSubmit={(e) => {
        e.preventDefault();
        if (title.trim()) mut.mutate(title.trim());
      }}
    >
      <input
        type="text"
        placeholder="Capture a new item into inbox…"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />
      <button type="submit" className="primary">
        Capture
      </button>
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

// ---- Next actions view ----

function NextActionsView({ env }: { env: string }) {
  const { data: config } = useQuery<EnvConfig>({
    queryKey: ['config', env],
    queryFn: () => api.getConfig(env),
  });
  const [contexts, setContexts] = useState<string[]>([]);
  const [energy, setEnergy] = useState<Energy | ''>('');
  const [maxMinutes, setMaxMinutes] = useState<string>('');

  const params: Record<string, string> = { status: 'next' };
  if (contexts.length) params.contexts = contexts.join(',');
  if (energy) params.energy = energy;
  if (maxMinutes) params.max_minutes = maxMinutes;

  const { data: items } = useQuery({
    queryKey: ['items', env, 'next', contexts, energy, maxMinutes],
    queryFn: () => api.listItems(env, params),
  });

  return (
    <>
      <div className="filters">
        <label>
          Contexts:
          {config?.contexts.map((c) => (
            <label key={c} style={{ display: 'inline-flex', gap: 4, marginLeft: 8 }}>
              <input
                type="checkbox"
                checked={contexts.includes(c)}
                onChange={(e) =>
                  setContexts((prev) =>
                    e.target.checked ? [...prev, c] : prev.filter((x) => x !== c)
                  )
                }
              />
              {c}
            </label>
          ))}
        </label>
        <label>
          Energy:
          <select value={energy} onChange={(e) => setEnergy(e.target.value as Energy | '')}>
            <option value="">any</option>
            <option value="low">low</option>
            <option value="medium">medium</option>
            <option value="high">high</option>
          </select>
        </label>
        <label>
          Max minutes:
          <input
            type="number"
            value={maxMinutes}
            onChange={(e) => setMaxMinutes(e.target.value)}
            style={{ width: 80 }}
          />
        </label>
      </div>
      <ItemList env={env} items={items ?? []} showEdit />
    </>
  );
}

// ---- Inbox view ----

function InboxView({ env }: { env: string }) {
  const { data: items } = useQuery({
    queryKey: ['items', env, 'inbox'],
    queryFn: () => api.listItems(env, { status: 'inbox' }),
  });
  return <ItemList env={env} items={items ?? []} showEdit />;
}

// ---- Bucket view (waiting/someday/reference) ----

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
        <div>
          {config?.contexts.map((c) => (
            <label key={c} style={{ display: 'inline-flex', gap: 4, marginRight: 8 }}>
              <input
                type="checkbox"
                checked={contexts.includes(c)}
                onChange={(e) =>
                  setContexts((prev) =>
                    e.target.checked ? [...prev, c] : prev.filter((x) => x !== c)
                  )
                }
              />
              {c}
            </label>
          ))}
        </div>
      </label>
      <div className="row">
        <label>
          Energy
          <select value={energy} onChange={(e) => setEnergy(e.target.value as Energy | '')}>
            <option value="">–</option>
            <option value="low">low</option>
            <option value="medium">medium</option>
            <option value="high">high</option>
          </select>
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
          <select value={area} onChange={(e) => setArea(e.target.value)}>
            <option value="">–</option>
            {config?.areas.map((a) => (
              <option key={a} value={a}>
                {a}
              </option>
            ))}
          </select>
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
        Notes
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
