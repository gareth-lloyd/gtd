import { useMemo, useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api, type Energy, type Project } from "./api";
import {
  ChipToggleGroup,
  DatePickerRow,
  DateTimePickerRow,
  findItemInCache,
  invalidateProjectQueries,
  useItemPatch,
} from "./ItemEdit";
import { Markdown } from "./markdown";
import { contextChipStyle } from "./context-colors";
import { fmtDate, generateProjectId, sortProjects } from "./format";
import { Button } from "./Button";
import { WorkflowActions } from "./WorkflowActions";
import { useSelection } from "./SelectionContext";
import { toasts } from "./toast";

// Experiment flag: hover renders the full editor; click pins selection.
const HOVER_SHOWS_FULL_CONTROLS = true;

export function DetailPanel({ env }: { env: string }) {
  const { selectedId, hoveredId, hoveredCardTop } = useSelection();
  const activeId = selectedId ?? (HOVER_SHOWS_FULL_CONTROLS ? hoveredId : null);

  if (activeId) {
    return (
      <div className="detail-panel">
        <SelectedDetail env={env} itemId={activeId} />
      </div>
    );
  }

  return (
    <div className="detail-panel">
      {hoveredId ? (
        <HoverDetail env={env} itemId={hoveredId} topOffset={hoveredCardTop} />
      ) : (
        <div className="detail-empty">Select an item to edit</div>
      )}
    </div>
  );
}

function HoverDetail({
  env,
  itemId,
  topOffset,
}: {
  env: string;
  itemId: string;
  topOffset: number | null;
}) {
  const qc = useQueryClient();
  // Read from the existing list cache — avoids a network fetch on hover
  const item = findItemInCache(qc, env, itemId);

  if (!item) return null;

  return (
    <div
      className="hover-actions"
      style={{ top: topOffset != null ? `${topOffset}px` : undefined }}
    >
      <WorkflowActions env={env} item={item} />
    </div>
  );
}

function SelectedDetail({ env, itemId }: { env: string; itemId: string }) {
  const qc = useQueryClient();
  const { data: config } = useQuery({
    queryKey: ["config", env],
    queryFn: () => api.getConfig(env),
  });
  const { data: projects } = useQuery({
    queryKey: ["projects", env, false],
    queryFn: () => api.listProjects(env, false),
  });
  // Seed from cache so the first render is instant; fall back to fetch
  const { data: item } = useQuery({
    queryKey: ["item", env, itemId],
    queryFn: () => api.getItem(env, itemId),
    initialData: () => findItemInCache(qc, env, itemId),
    staleTime: 30_000,
  });

  const { patch } = useItemPatch(env, itemId);

  const sortedProjects = useMemo(() => (projects ? sortProjects(projects) : []), [projects]);
  const project = projects?.find((p) => p.id === item?.project) ?? null;
  const capped = project?.max_next_items != null;

  if (!item) return <div className="detail-empty">Loading…</div>;

  return (
    <div className="detail-meta">
      {item.output && <AgentLog key={item.id} output={item.output} />}
      <div className="detail-section">
        <span className="detail-label">Project</span>
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
                  <span className={`priority-badge p${p.priority}`}>P{p.priority}</span>
                )}
                {p.max_next_items != null && (
                  <span
                    className="sequential-dot"
                    title={
                      p.max_next_items === 1 ? "one at a time" : `up to ${p.max_next_items} at once`
                    }
                  >
                    ⇢
                  </span>
                )}
              </>
            ),
          }))}
        >
          <NewProjectChip env={env} onCreated={(id) => patch({ project: id })} />
        </ChipToggleGroup>
      </div>

      {capped && (
        <div className="detail-section">
          <span className="detail-label">Order</span>
          <div className="chip-toggle-group">
            <input
              type="number"
              className="order-input"
              value={item.order ?? ""}
              onChange={(e) =>
                patch({
                  order: e.target.value === "" ? null : parseInt(e.target.value, 10),
                })
              }
              placeholder="position"
            />
          </div>
        </div>
      )}

      <div className="detail-divider" />

      <div className="detail-section">
        <span className="detail-label">Contexts</span>
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
      </div>

      <div className="detail-divider" />

      <div className="detail-split">
        <div className="detail-section">
          <span className="detail-label">Energy</span>
          <ChipToggleGroup<Energy>
            mode="single"
            value={item.energy}
            onChange={(v) => patch({ energy: v })}
            options={(["low", "medium", "high"] as Energy[]).map((e) => ({
              value: e,
              label: `⚡ ${e}`,
            }))}
          />
        </div>
        <div className="detail-section">
          <span className="detail-label">Time</span>
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
      </div>

      <div className="detail-divider" />

      <div className="detail-section">
        <span className="detail-label">Area</span>
        <ChipToggleGroup<string>
          mode="single"
          value={item.area}
          onChange={(v) => patch({ area: v })}
          noneLabel="none"
          options={(config?.areas ?? []).map((a) => ({ value: a, label: a }))}
        />
      </div>

      <div className="detail-divider" />

      <div className="detail-section">
        <span className="detail-label">Due</span>
        <div className="chip-toggle-group">
          <DatePickerRow value={item.due} onChange={(v) => patch({ due: v })} />
        </div>
      </div>

      <div className="detail-section">
        <span className="detail-label">Defer until</span>
        <div className="chip-toggle-group">
          <DateTimePickerRow value={item.defer_until} onChange={(v) => patch({ defer_until: v })} />
        </div>
      </div>

      <div className="detail-divider" />

      <div className="detail-section">
        <span className="detail-label">Actions</span>
        <WorkflowActions env={env} item={item} />
      </div>

      <div className="detail-dates" title={`updated ${fmtDate(item.updated)}`}>
        created {fmtDate(item.created)}
      </div>
    </div>
  );
}

function AgentLog({ output }: { output: string }) {
  const [expanded, setExpanded] = useState(false);
  const copy = async () => {
    try {
      await navigator.clipboard.writeText(output);
      toasts.show("success", "Agent log copied");
    } catch {
      toasts.show("error", "Copy failed");
    }
  };
  return (
    <div className="agent-output">
      <div className="agent-output-header-row">
        <button
          type="button"
          className="agent-output-header"
          aria-expanded={expanded}
          onClick={() => setExpanded((v) => !v)}
        >
          <span aria-hidden>{expanded ? "▾" : "▸"}</span> 🤖 Agent log
        </button>
        <button
          type="button"
          className="agent-output-copy"
          aria-label="Copy agent log to clipboard"
          onClick={copy}
        >
          Copy
        </button>
      </div>
      {expanded && (
        <div className="agent-output-body">
          <Markdown source={output} />
        </div>
      )}
    </div>
  );
}

function NewProjectChip({
  env,
  onCreated,
}: {
  env: string;
  onCreated: (projectId: string) => void;
}) {
  const [open, setOpen] = useState(false);
  const [title, setTitle] = useState("");
  const qc = useQueryClient();

  const mut = useMutation({
    mutationFn: () => {
      const trimmed = title.trim();
      return api.createProject(env, { id: generateProjectId(trimmed), title: trimmed });
    },
    onSuccess: (project: Project) => {
      invalidateProjectQueries(qc, env);
      setTitle("");
      setOpen(false);
      onCreated(project.id);
    },
  });

  const submit = () => {
    if (title.trim()) mut.mutate();
  };

  if (!open) {
    return (
      <button type="button" className="chip-toggle new-project" onClick={() => setOpen(true)}>
        + new project
      </button>
    );
  }

  return (
    <span className="new-project-inline">
      <input
        autoFocus
        value={title}
        placeholder="project title"
        onChange={(e) => setTitle(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            e.preventDefault();
            submit();
          } else if (e.key === "Escape") {
            e.preventDefault();
            setTitle("");
            setOpen(false);
          }
        }}
        disabled={mut.isPending}
      />
      <Button type="button" onClick={submit} busy={mut.isPending} disabled={!title.trim()}>
        Create
      </Button>
    </span>
  );
}
