import { useQuery, useQueryClient } from "@tanstack/react-query";
import { useNavigate, useParams } from "react-router-dom";
import { api } from "./api";
import { findItemInCache } from "./ItemEdit";
import { Markdown } from "./markdown";
import { contextChipStyle } from "./context-colors";
import { fmtDate } from "./format";
import { useEnvParam } from "./useEnvParam";
import { toasts } from "./toast";

// A focused, single-item reading view: the agent log fills the screen, with
// just a compact overview of the ticket and its metadata above it. Reached via
// the 🤖 log chip on an item card. Deliberately read-only — editing lives in
// the item card / detail pane; this view is for reading agent output.
export function AgentLogView() {
  const env = useEnvParam();
  const navigate = useNavigate();
  const qc = useQueryClient();
  const { itemId = "" } = useParams<{ itemId: string }>();

  // Seed from the list cache so arriving from a card renders instantly instead
  // of flashing "Loading…"; fall back to a fetch. Mirrors DetailPanel.
  const { data: item, isLoading } = useQuery({
    queryKey: ["item", env, itemId],
    queryFn: () => api.getItem(env, itemId),
    initialData: () => findItemInCache(qc, env, itemId),
    staleTime: 30_000,
  });
  const { data: projects } = useQuery({
    queryKey: ["projects", env, false],
    queryFn: () => api.listProjects(env, false),
  });

  if (isLoading) return <div className="empty">Loading…</div>;
  if (!item) return <div className="empty">Item not found.</div>;

  const project = projects?.find((p) => p.id === item.project) ?? null;

  const copy = async () => {
    try {
      await navigator.clipboard.writeText(item.output);
      toasts.show("success", "Agent log copied");
    } catch {
      toasts.show("error", "Copy failed");
    }
  };

  return (
    <div className="agent-log-view">
      <button className="back-link" onClick={() => navigate(-1)}>
        ← Back
      </button>

      <header className="agent-log-overview">
        <h2 className="agent-log-title">{item.title}</h2>
        <div className="agent-log-meta">
          {item.status !== "next" && <span className="chip">{item.status}</span>}
          {project && <span className="chip project-chip">📁 {project.title}</span>}
          {item.project_priority != null && (
            <span className={`priority-badge p${item.project_priority}`}>
              P{item.project_priority}
            </span>
          )}
          {item.contexts.map((c) => (
            <span key={c} className="chip context-chip" style={contextChipStyle(c)}>
              @{c}
            </span>
          ))}
          {item.energy && <span className="chip">⚡{item.energy}</span>}
          {item.time_minutes != null && <span className="chip">{item.time_minutes}m</span>}
          {item.area && <span className="chip">{item.area}</span>}
          {item.due && <span className="chip">📅 {fmtDate(item.due)}</span>}
        </div>
        <div className="agent-log-dates" title={`created ${fmtDate(item.created)}`}>
          updated {fmtDate(item.updated)}
        </div>
      </header>

      <section className="agent-log-panel" data-testid="agent-log-panel">
        <div className="agent-log-panel-header">
          <span>🤖 Agent log</span>
          {item.output && (
            <button type="button" className="agent-output-copy" onClick={copy}>
              Copy
            </button>
          )}
        </div>
        <div className="agent-log-panel-body">
          {item.output ? (
            <Markdown source={item.output} />
          ) : (
            <div className="empty">No agent log yet.</div>
          )}
        </div>
      </section>
    </div>
  );
}
