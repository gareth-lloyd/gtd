import React, { useMemo, useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Link, NavLink, useNavigate, useParams, useSearchParams } from "react-router-dom";
import {
  DndContext,
  closestCenter,
  KeyboardSensor,
  PointerSensor,
  useSensor,
  useSensors,
  type DragEndEvent,
} from "@dnd-kit/core";
import {
  arrayMove,
  SortableContext,
  sortableKeyboardCoordinates,
  useSortable,
  verticalListSortingStrategy,
} from "@dnd-kit/sortable";
import { CSS } from "@dnd-kit/utilities";
import { api, type Item, type Project } from "./api";
import { Button } from "./Button";
import { ItemCard } from "./ItemCard";
import { fmtMinutes, generateProjectId, sortProjects } from "./format";
import { invalidateProjectQueries, isHiddenByDefer } from "./ItemEdit";
import { useEnvParam } from "./useEnvParam";

type EnergyKey = "low" | "medium" | "high" | "unset";

export interface ProjectStats {
  totalMinutes: number;
  totalCount: number;
  byEnergy: Record<EnergyKey, { count: number; minutes: number }>;
}

export function computeProjectStats(actions: Item[]): ProjectStats {
  const byEnergy: ProjectStats["byEnergy"] = {
    low: { count: 0, minutes: 0 },
    medium: { count: 0, minutes: 0 },
    high: { count: 0, minutes: 0 },
    unset: { count: 0, minutes: 0 },
  };
  let totalMinutes = 0;
  for (const a of actions) {
    const m = a.time_minutes ?? 0;
    totalMinutes += m;
    const k: EnergyKey = a.energy ?? "unset";
    byEnergy[k].count += 1;
    byEnergy[k].minutes += m;
  }
  return { totalMinutes, totalCount: actions.length, byEnergy };
}

export const PRIORITY_LABELS: Record<number, string> = {
  1: "P1 critical",
  2: "P2 high",
  3: "P3 medium",
  4: "P4 low",
  5: "P5 aspirational",
};

export function ProjectBadges({ project }: { project: Project }) {
  return (
    <>
      {project.priority != null && (
        <span className={`priority-badge p${project.priority}`}>P{project.priority}</span>
      )}
      {project.max_next_items != null && (
        <span
          className="sequential-badge"
          title={
            project.max_next_items === 1
              ? "Only the first ordered step appears on the next list"
              : `Up to ${project.max_next_items} ordered steps appear on the next list`
          }
        >
          {project.max_next_items === 1 ? "↓ 1-at-a-time" : `↓ up to ${project.max_next_items}`}
        </span>
      )}
      {project.status !== "active" && <span className="project-status">{project.status}</span>}
    </>
  );
}

function ProjectIndexRow({ project }: { project: Project }) {
  const isDone = project.status === "complete" || project.status === "dropped";
  return (
    <Link to={project.id} className={`project-index-row${isDone ? " done" : ""}`}>
      <span className="project-index-title">{project.title}</span>
      <ProjectBadges project={project} />
      {project.due && <span className="chip">due {project.due}</span>}
      {project.outcome && <span className="project-index-outcome">{project.outcome}</span>}
    </Link>
  );
}

export function ProjectNavLinks({ env }: { env: string }) {
  const { data: projects } = useQuery({
    queryKey: ["projects", env, false],
    queryFn: () => api.listProjects(env, false),
  });
  if (!projects || projects.length === 0) return null;
  return (
    <div className="side-nav-sub">
      {sortProjects(projects).map((p) => (
        <NavLink
          key={p.id}
          to={`projects/${p.id}`}
          className={({ isActive }) => (isActive ? "sub-link active" : "sub-link")}
          title={p.title}
        >
          {p.priority != null && <span className={`priority-dot p${p.priority}`}>●</span>}
          <span className="sub-link-title">{p.title}</span>
        </NavLink>
      ))}
    </div>
  );
}

export function ProjectsView() {
  const env = useEnvParam();
  const [showFinished, setShowFinished] = useState(false);
  const { data: projects, isLoading } = useQuery({
    queryKey: ["projects", env, showFinished],
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

function ProjectStatsRow({ stats }: { stats: ProjectStats }) {
  const energyOrder: EnergyKey[] = ["high", "medium", "low"];
  return (
    <div className="project-stats">
      {stats.totalMinutes > 0 && (
        <span className="chip stat-total">⏱ {fmtMinutes(stats.totalMinutes)} total</span>
      )}
      {energyOrder.map((k) =>
        stats.byEnergy[k].count > 0 ? (
          <span key={k} className={`chip stat-energy stat-energy-${k}`}>
            ⚡ {k} · {fmtMinutes(stats.byEnergy[k].minutes)}
            <span className="stat-count"> ({stats.byEnergy[k].count})</span>
          </span>
        ) : null,
      )}
      {stats.byEnergy.unset.count > 0 && (
        <span className="chip stat-energy stat-energy-unset">
          no energy · {stats.byEnergy.unset.count}
        </span>
      )}
    </div>
  );
}

export function ProjectDetailView() {
  const env = useEnvParam();
  const { projectId = "" } = useParams<{ projectId: string }>();
  const navigate = useNavigate();
  const qc = useQueryClient();
  const [editing, setEditing] = useState(false);
  const [params, setParams] = useSearchParams();
  const includeDeferred = params.get("include_deferred") === "true";
  // Always fetch the full action list — drag-to-reorder needs every item so
  // hidden deferred items keep their slots. The checkbox toggles a render-time
  // filter, not the API call.
  // Always fetch the full action list — drag-reorder needs hidden items to
  // preserve their slots. The "Show deferred" toggle is a render-time filter.
  const { data, isLoading } = useQuery({
    queryKey: ["project", env, projectId, "full"],
    queryFn: () => api.getProject(env, projectId, true),
  });

  const invalidate = () => invalidateProjectQueries(qc, env, projectId);

  const statusMut = useMutation<Project, Error, string>({
    mutationFn: (status) => api.updateProject(env, projectId, { status }),
    onSuccess: invalidate,
  });

  const deleteMut = useMutation({
    mutationFn: () => api.deleteProject(env, projectId),
    onSuccess: () => {
      invalidate();
      navigate("..");
    },
  });

  const stats = useMemo(() => (data ? computeProjectStats(data.actions) : null), [data]);

  if (isLoading || !data || !stats) return <div className="empty">Loading…</div>;

  const { project, actions } = data;
  const visibleActions = includeDeferred ? actions : actions.filter((a) => !isHiddenByDefer(a));
  const deferredHidden = actions.length - visibleActions.length;
  const isDone = project.status === "complete" || project.status === "dropped";
  const anyPending = statusMut.isPending || deleteMut.isPending;

  return (
    <div className={`project-detail${isDone ? " done" : ""}`}>
      <header className="project-header">
        <h2>{project.title}</h2>
        <div className="project-badges-row">
          <ProjectBadges project={project} />
        </div>
      </header>
      {actions.length > 0 && <ProjectStatsRow stats={stats} />}
      {(project.outcome || project.due || project.area) && (
        <div className="project-meta">
          {project.outcome && <span className="outcome">{project.outcome}</span>}
          {project.due && <span className="chip">due {project.due}</span>}
          {project.area && <span className="chip">{project.area}</span>}
        </div>
      )}
      <div className="project-actions">
        {project.status !== "complete" && (
          <Button
            onClick={() => statusMut.mutate("complete")}
            busy={statusMut.isPending && statusMut.variables === "complete"}
            disabled={anyPending}
          >
            ✓ Complete
          </Button>
        )}
        {project.status !== "active" && (
          <Button
            onClick={() => statusMut.mutate("active")}
            busy={statusMut.isPending && statusMut.variables === "active"}
            disabled={anyPending}
          >
            ↺ Reopen
          </Button>
        )}
        {project.status === "active" && (
          <Button
            onClick={() => statusMut.mutate("on_hold")}
            busy={statusMut.isPending && statusMut.variables === "on_hold"}
            disabled={anyPending}
          >
            ⏸ Hold
          </Button>
        )}
        <button className="quiet" onClick={() => setEditing(!editing)} disabled={anyPending}>
          {editing ? "Close" : "Edit"}
        </button>
        <Button
          className="quiet danger"
          onClick={() => {
            if (
              confirm(
                `Delete project "${project.title}"? Actions linked to it will not be deleted.`,
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
      {editing && <ProjectEditor env={env} project={project} onClose={() => setEditing(false)} />}
      {(deferredHidden > 0 || includeDeferred) && (
        <div className="bucket-toolbar">
          <label className="toggle">
            <input
              type="checkbox"
              checked={includeDeferred}
              onChange={(e) => {
                const next = new URLSearchParams(params);
                if (e.target.checked) next.set("include_deferred", "true");
                else next.delete("include_deferred");
                setParams(next, { replace: true });
              }}
            />
            Show deferred
          </label>
        </div>
      )}
      <SortableActionList
        env={env}
        projectId={project.id}
        items={visibleActions}
        allItems={actions}
      />
    </div>
  );
}

/**
 * Walk the current full order, substituting `newVisible` into the slots
 * currently occupied by visible items. Hidden items keep their absolute slot —
 * visible items move around them.
 */
export function computeReorderedFullIds(
  currentFull: string[],
  visibleSet: Set<string>,
  newVisible: string[],
): string[] {
  let cursor = 0;
  return currentFull.map((id) => (visibleSet.has(id) ? newVisible[cursor++] : id));
}

export function SortableActionList({
  env,
  projectId,
  items,
  allItems,
}: {
  env: string;
  projectId: string;
  items: Item[];
  /**
   * Full action list including any items hidden from rendering (e.g. deferred
   * items when "Show deferred" is off). Reorder operates on this list so
   * hidden items keep their slots and `order` values stay collision-free.
   * Defaults to `items` for callers that don't filter.
   */
  allItems?: Item[];
}) {
  const fullItems = allItems ?? items;
  const qc = useQueryClient();
  const [localFullOrder, setLocalFullOrder] = useState<string[] | null>(null);
  // Lists are small (≤ ~50 items) and the parent re-renders on every action
  // edit, so memoizing these buys nothing — the deps change reference each pass.
  const visibleSet = new Set(items.map((i) => i.id));
  const visibleIds = localFullOrder
    ? localFullOrder.filter((id) => visibleSet.has(id))
    : items.map((i) => i.id);
  const itemsById = new Map(items.map((i) => [i.id, i]));
  const { data: projects } = useQuery({
    queryKey: ["projects", env, false],
    queryFn: () => api.listProjects(env, false),
  });

  const sensors = useSensors(
    useSensor(PointerSensor, { activationConstraint: { distance: 5 } }),
    useSensor(KeyboardSensor, { coordinateGetter: sortableKeyboardCoordinates }),
  );

  const reorderMut = useMutation({
    mutationFn: (itemIds: string[]) => api.reorderProjectItems(env, projectId, itemIds),
    onSuccess: () => {
      setLocalFullOrder(null);
      invalidateProjectQueries(qc, env, projectId);
      qc.invalidateQueries({ queryKey: ["items", env] });
    },
    onError: () => {
      setLocalFullOrder(null);
    },
  });

  if (items.length === 0) return <div className="empty">Nothing here.</div>;

  function onDragEnd(event: DragEndEvent) {
    const { active, over } = event;
    if (!over || active.id === over.id) return;
    const oldIndex = visibleIds.indexOf(String(active.id));
    const newIndex = visibleIds.indexOf(String(over.id));
    if (oldIndex < 0 || newIndex < 0) return;
    const newVisible = arrayMove(visibleIds, oldIndex, newIndex);
    const currentFull = localFullOrder ?? fullItems.map((i) => i.id);
    const newFull = computeReorderedFullIds(currentFull, visibleSet, newVisible);
    setLocalFullOrder(newFull);
    reorderMut.mutate(newFull);
  }

  return (
    <DndContext sensors={sensors} collisionDetection={closestCenter} onDragEnd={onDragEnd}>
      <SortableContext items={visibleIds} strategy={verticalListSortingStrategy}>
        <ul className="item-list sortable">
          {visibleIds.map((id) => {
            const item = itemsById.get(id);
            if (!item) return null;
            return <SortableItemRow key={id} env={env} item={item} projects={projects} />;
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
}: {
  env: string;
  item: Item;
  projects: Project[] | undefined;
}) {
  const { attributes, listeners, setNodeRef, transform, transition, isDragging } = useSortable({
    id: item.id,
  });
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
          <ItemCard env={env} item={item} projects={projects} />
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
  const [outcome, setOutcome] = useState(project.outcome ?? "");
  const [due, setDue] = useState(project.due ?? "");
  const [priority, setPriority] = useState<string>(project.priority?.toString() ?? "");
  const [maxNextItems, setMaxNextItems] = useState<number | null>(project.max_next_items);
  const [workingDir, setWorkingDir] = useState(project.working_dir ?? "");
  const [body, setBody] = useState(project.body);

  const mut = useMutation({
    mutationFn: () =>
      api.updateProject(env, project.id, {
        title,
        outcome: outcome || null,
        due: due || null,
        priority: priority ? parseInt(priority, 10) : null,
        max_next_items: maxNextItems,
        working_dir: workingDir.trim() || null,
        body,
      }),
    onSuccess: () => {
      invalidateProjectQueries(qc, env, project.id);
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
          <input type="date" value={due} onChange={(e) => setDue(e.target.value)} />
        </label>
        <label>
          Priority
          <select value={priority} onChange={(e) => setPriority(e.target.value)}>
            <option value="">—</option>
            {[1, 2, 3, 4, 5].map((n) => (
              <option key={n} value={n}>
                {PRIORITY_LABELS[n]}
              </option>
            ))}
          </select>
        </label>
      </div>
      <MaxNextItemsField value={maxNextItems} onChange={setMaxNextItems} />
      <label>
        Working directory
        <input
          type="text"
          value={workingDir}
          placeholder="~/projects/foo — where agent sessions launch"
          onChange={(e) => setWorkingDir(e.target.value)}
        />
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

function NewProjectForm({ env }: { env: string }) {
  const qc = useQueryClient();
  const [open, setOpen] = useState(false);
  const [title, setTitle] = useState("");
  const [outcome, setOutcome] = useState("");
  const [due, setDue] = useState("");
  const [priority, setPriority] = useState<string>("");
  const [maxNextItems, setMaxNextItems] = useState<number | null>(null);
  const [workingDir, setWorkingDir] = useState("");

  const mut = useMutation({
    mutationFn: () =>
      api.createProject(env, {
        id: generateProjectId(title),
        title: title.trim(),
        outcome: outcome || undefined,
        due: due || undefined,
        priority: priority ? parseInt(priority, 10) : undefined,
        max_next_items: maxNextItems,
        working_dir: workingDir.trim() || undefined,
      }),
    onSuccess: () => {
      setOpen(false);
      setTitle("");
      setOutcome("");
      setDue("");
      setPriority("");
      setMaxNextItems(null);
      setWorkingDir("");
      invalidateProjectQueries(qc, env);
    },
  });

  if (!open) return <button onClick={() => setOpen(true)}>+ New project</button>;

  return (
    <div className="editor">
      <label>
        Title
        <input type="text" value={title} onChange={(e) => setTitle(e.target.value)} autoFocus />
      </label>
      <label>
        Outcome (what "done" looks like)
        <input type="text" value={outcome} onChange={(e) => setOutcome(e.target.value)} />
      </label>
      <div className="row">
        <label>
          Due
          <input type="date" value={due} onChange={(e) => setDue(e.target.value)} />
        </label>
        <label>
          Priority
          <select value={priority} onChange={(e) => setPriority(e.target.value)}>
            <option value="">—</option>
            {[1, 2, 3, 4, 5].map((n) => (
              <option key={n} value={n}>
                {PRIORITY_LABELS[n]}
              </option>
            ))}
          </select>
        </label>
      </div>
      <MaxNextItemsField value={maxNextItems} onChange={setMaxNextItems} />
      <label>
        Working directory
        <input
          type="text"
          value={workingDir}
          placeholder="~/projects/foo — where agent sessions launch"
          onChange={(e) => setWorkingDir(e.target.value)}
        />
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

function MaxNextItemsField({
  value,
  onChange,
}: {
  value: number | null;
  onChange: (v: number | null) => void;
}) {
  const capped = value != null;
  return (
    <label className="toggle-row">
      <input
        type="checkbox"
        checked={capped}
        onChange={(e) => onChange(e.target.checked ? 1 : null)}
      />
      <span>Cap next-actions —</span>
      <input
        type="number"
        min={1}
        value={value ?? ""}
        placeholder="∞"
        disabled={!capped}
        onChange={(e) => {
          const parsed = parseInt(e.target.value, 10);
          onChange(Number.isFinite(parsed) && parsed >= 1 ? parsed : null);
        }}
        style={{ width: "4rem" }}
      />
      <span>ordered step(s) visible at once</span>
    </label>
  );
}
