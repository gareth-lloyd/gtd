import { useEffect, useMemo, useRef, useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { api, type Bucket, type Energy, type Item, type Project } from './api';
import { Button } from './Button';
import {
  ChipToggleGroup,
  DatePickerRow,
  invalidateItemQueries,
  useItemPatch,
} from './ItemEdit';
import { contextChipStyle } from './context-colors';
import { fmtDate, sortProjects } from './format';

export function ItemCard({
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
  const cardRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!expanded) return;
    const onMouseDown = (e: MouseEvent) => {
      if (cardRef.current && !cardRef.current.contains(e.target as Node)) {
        onCollapse();
      }
    };
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onCollapse();
    };
    document.addEventListener('mousedown', onMouseDown);
    document.addEventListener('keydown', onKey);
    return () => {
      document.removeEventListener('mousedown', onMouseDown);
      document.removeEventListener('keydown', onKey);
    };
  }, [expanded, onCollapse]);

  return (
    <div
      ref={cardRef}
      className={`item${expanded ? ' expanded' : ''}`}
      onClick={(e) => {
        if (expanded) return;
        if ((e.target as HTMLElement).closest('.item-actions')) return;
        onExpand();
      }}
    >
      {expanded ? (
        <ExpandedCard env={env} item={item} projects={projects} onCollapse={onCollapse} />
      ) : (
        <CollapsedCard env={env} item={item} projects={projects} />
      )}
    </div>
  );
}

function CollapsedCard({
  env,
  item,
  projects,
}: {
  env: string;
  item: Item;
  projects: Project[] | undefined;
}) {
  const project = projects?.find((p) => p.id === item.project) ?? null;

  return (
    <>
      <div className="item-title">{item.title}</div>
      {item.body && (
        <div className="item-body">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>{item.body}</ReactMarkdown>
        </div>
      )}
      <div className="item-meta">
        {item.status !== 'next' && <span className="chip">{item.status}</span>}
        {project && <span className="chip project-chip">📁 {project.title}</span>}
        {item.project_priority != null && (
          <span className={`priority-badge p${item.project_priority}`}>
            P{item.project_priority}
          </span>
        )}
        {item.order != null && <span className="chip">#{item.order}</span>}
        {item.contexts.map((c) => (
          <span key={c} className="chip context-chip" style={contextChipStyle(c)}>
            @{c}
          </span>
        ))}
        {item.energy && <span className="chip">⚡{item.energy}</span>}
        {item.time_minutes != null && (
          <span className="chip">{item.time_minutes}m</span>
        )}
        {item.area && <span className="chip">{item.area}</span>}
        {item.due && <span className="chip">due {item.due}</span>}
        {item.defer_until && <span className="chip">defer {item.defer_until}</span>}
        <span className="chip dates" title={`created ${fmtDate(item.created)}`}>
          updated {fmtDate(item.updated)}
        </span>
      </div>
      <WorkflowActions env={env} item={item} variant="on-hover" />
    </>
  );
}

function ExpandedCard({
  env,
  item,
  projects,
  onCollapse,
}: {
  env: string;
  item: Item;
  projects: Project[] | undefined;
  onCollapse: () => void;
}) {
  const { data: config } = useQuery({
    queryKey: ['config', env],
    queryFn: () => api.getConfig(env),
  });
  const { patch, flush } = useItemPatch(env, item.id);

  const [localTitle, setLocalTitle] = useState(item.title);
  const [localBody, setLocalBody] = useState(item.body);
  const lastItemIdRef = useRef(item.id);
  useEffect(() => {
    if (lastItemIdRef.current !== item.id) {
      setLocalTitle(item.title);
      setLocalBody(item.body);
      lastItemIdRef.current = item.id;
    }
  }, [item.id]);

  const project = projects?.find((p) => p.id === item.project) ?? null;
  const sequential = project?.sequential ?? false;
  const sortedProjects = useMemo(
    () => (projects ? sortProjects(projects) : []),
    [projects]
  );

  const saveAndCollapse = (e: React.KeyboardEvent) => {
    if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') {
      e.preventDefault();
      void flush();
      onCollapse();
    }
  };

  return (
    <div className="item-expanded">
      <input
        className="title-input"
        value={localTitle}
        onChange={(e) => {
          setLocalTitle(e.target.value);
          patch({ title: e.target.value }, { debounce: 500 });
        }}
        onKeyDown={saveAndCollapse}
        placeholder="Title"
        autoFocus
      />

      <ChipToggleGroup<string>
        mode="single"
        value={item.project}
        onChange={(v) => patch({ project: v })}
        noneLabel="📁 none"
        options={sortedProjects.map((p) => ({
          value: p.id,
          label: (
            <>
              📁 {p.title}
              {p.priority != null && (
                <span className={`priority-badge p${p.priority}`}>
                  P{p.priority}
                </span>
              )}
              {p.sequential && (
                <span className="sequential-dot" title="sequential">⇢</span>
              )}
            </>
          ),
        }))}
      />

      {sequential && (
        <div className="chip-toggle-group">
          <span className="row-hint">order</span>
          <input
            type="number"
            className="order-input"
            value={item.order ?? ''}
            onChange={(e) =>
              patch({
                order: e.target.value === '' ? null : parseInt(e.target.value, 10),
              })
            }
            placeholder="position"
          />
        </div>
      )}

      <ChipToggleGroup<string>
        mode="multi"
        value={item.contexts}
        onChange={(v) => patch({ contexts: v })}
        options={(config?.contexts ?? []).map((c) => ({
          value: c,
          label: `@${c}`,
        }))}
        styleForSelected={(v) => contextChipStyle(v)}
      />

      <div className="chip-toggle-group split-row">
        <ChipToggleGroup<Energy>
          mode="single"
          value={item.energy}
          onChange={(v) => patch({ energy: v })}
          options={(['low', 'medium', 'high'] as Energy[]).map((e) => ({
            value: e,
            label: `⚡ ${e}`,
          }))}
        />
        <ChipToggleGroup<string>
          mode="single"
          value={item.time_minutes != null ? String(item.time_minutes) : null}
          onChange={(v) => patch({ time_minutes: v == null ? null : parseInt(v, 10) })}
          options={[5, 15, 30, 60].map((n) => ({
            value: String(n),
            label: `${n}m`,
          }))}
        />
      </div>

      <ChipToggleGroup<string>
        mode="single"
        value={item.area}
        onChange={(v) => patch({ area: v })}
        noneLabel="area: none"
        options={(config?.areas ?? []).map((a) => ({ value: a, label: a }))}
      />

      <div className="chip-toggle-group">
        <span className="row-hint">due</span>
        <DatePickerRow
          value={item.due}
          onChange={(v) => patch({ due: v })}
        />
      </div>

      <div className="chip-toggle-group">
        <span className="row-hint">defer</span>
        <DatePickerRow
          value={item.defer_until}
          onChange={(v) => patch({ defer_until: v })}
        />
      </div>

      <textarea
        className="body-input"
        rows={4}
        value={localBody}
        onChange={(e) => {
          setLocalBody(e.target.value);
          patch({ body: e.target.value }, { debounce: 500 });
        }}
        onKeyDown={saveAndCollapse}
        placeholder="Notes (markdown)…"
      />

      <WorkflowActions env={env} item={item} variant="expanded" />
    </div>
  );
}

function WorkflowActions({
  env,
  item,
  variant,
}: {
  env: string;
  item: Item;
  variant: 'on-hover' | 'expanded';
}) {
  const qc = useQueryClient();
  const invalidate = () => invalidateItemQueries(qc, env, item.id, item.project);

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

  const busy =
    moveMut.isPending ||
    completeMut.isPending ||
    deleteMut.isPending ||
    purgeMut.isPending;

  const isMoving = (to: Bucket) =>
    moveMut.isPending && moveMut.variables === to;

  const inTrash = item.status === 'trash';
  const isArchive = item.status === 'archive';

  return (
    <div
      className={`item-actions ${variant === 'on-hover' ? 'on-hover' : 'expanded-actions'}`}
      onClick={(e) => e.stopPropagation()}
    >
      {inTrash ? (
        <>
          <Button
            onClick={() => moveMut.mutate('inbox')}
            busy={isMoving('inbox')}
            disabled={busy}
          >
            ↺ restore
          </Button>
          <Button
            className="danger"
            onClick={() => {
              if (confirm(`Permanently delete "${item.title}"?`)) purgeMut.mutate();
            }}
            busy={purgeMut.isPending}
            disabled={busy}
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
                disabled={busy}
              >
                → {b}
              </Button>
            ))}
          {!isArchive && (
            <Button
              onClick={() => completeMut.mutate()}
              busy={completeMut.isPending}
              disabled={busy}
            >
              ✓ done
            </Button>
          )}
          <Button
            className="danger"
            onClick={() => deleteMut.mutate()}
            busy={deleteMut.isPending}
            disabled={busy}
          >
            Delete
          </Button>
        </>
      )}
    </div>
  );
}
