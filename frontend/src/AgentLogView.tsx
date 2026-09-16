import { useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useNavigate, useParams } from "react-router-dom";
import { api, type AgentTarget } from "./api";
import { AutoGrowTextarea } from "./AutoGrowTextarea";
import { Button } from "./Button";
import { findItemInCache, invalidateItemQueries } from "./ItemEdit";
import { Markdown } from "./markdown";
import { contextChipStyle } from "./context-colors";
import { fmtDate } from "./format";
import { useEnvParam } from "./useEnvParam";
import { toasts } from "./toast";

// A focused, single-item reading view: the agent log fills the screen, with
// just a compact overview of the ticket and its metadata above it. Reached via
// the 🤖 log chip on an item card. Item fields are read-only here — editing
// lives in the item card / detail pane. The one thing you can *do* from this
// view is hand the agent its next piece of work (see NextAgentWork).
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

      <NextAgentWork env={env} itemId={item.id} />

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

// The "next agent task" flow: after reading a run's output, type the
// follow-up and launch a fresh session. The server builds a prompt from the
// item *plus* its existing `output:` *plus* this text, so the new agent picks
// up where the last one left off. The text is not saved on the item — the
// agent is told to quote it at the top of its own `## Agent run` section, so
// the log itself records what was asked.
function NextAgentWork({ env, itemId }: { env: string; itemId: string }) {
  const qc = useQueryClient();
  const [text, setText] = useState("");
  const task = text.trim();

  const launchMut = useMutation<void, Error, AgentTarget>({
    mutationFn: (target) => api.launchAgent(env, itemId, target, task),
    onSuccess: () => {
      setText("");
      toasts.show("success", "Agent launched");
      // Launching pins working_on; refresh so the header/lists reflect it.
      invalidateItemQueries(qc, env, itemId);
    },
    onError: (e) => toasts.show("error", e.message || "Launch failed"),
  });
  const isLaunching = (target: AgentTarget) =>
    launchMut.isPending && launchMut.variables === target;
  const disabled = !task || launchMut.isPending;

  const onKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && (e.metaKey || e.ctrlKey) && task && !launchMut.isPending) {
      e.preventDefault();
      launchMut.mutate("iterm");
    }
  };

  return (
    <section className="next-agent-work" data-testid="next-agent-work">
      <label className="next-agent-work-label" htmlFor="next-agent-work-input">
        ▶ Next agent work
      </label>
      <AutoGrowTextarea
        id="next-agent-work-input"
        className="next-agent-work-input"
        value={text}
        onChange={(e) => setText(e.target.value)}
        onKeyDown={onKeyDown}
        placeholder="What should the next agent session do? It will see the log below. ⌘↵ launches in iTerm."
        minRows={2}
        maxHeightRem={16}
      />
      <div className="next-agent-work-actions">
        <Button
          onClick={() => launchMut.mutate("iterm")}
          busy={isLaunching("iterm")}
          disabled={disabled}
          title="Launch a Claude Code session in iTerm with the log and this follow-up as the prompt"
        >
          🤖 agent
        </Button>
        <Button
          onClick={() => launchMut.mutate("desktop")}
          busy={isLaunching("desktop")}
          disabled={disabled}
          title="Open a Claude Code session in the Claude desktop app with the log and this follow-up as the prompt"
        >
          🖥️ desktop agent
        </Button>
      </div>
    </section>
  );
}
