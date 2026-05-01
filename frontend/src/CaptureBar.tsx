import { useEffect, useRef, useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "./api";
import { Button } from "./Button";
import { toasts } from "./toast";
import { sortProjects } from "./format";
import { invalidateProjectQueries } from "./ItemEdit";

export type CaptureMode = "regular" | "regular-top" | "ai";

const MODES: ReadonlyArray<{ value: CaptureMode; label: string; title?: string }> = [
  { value: "regular", label: "Regular" },
  {
    value: "regular-top",
    label: "Regular ↑",
    title: "Capture and float to the top of the inbox (Shift+C)",
  },
  { value: "ai", label: "AI ✦" },
];

export function isEditableTarget(target: EventTarget | null): boolean {
  if (!(target instanceof HTMLElement)) return false;
  const tag = target.tagName;
  return tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT" || target.isContentEditable;
}

export function CaptureBar({
  env,
  focusTick,
  defaultProjectId = "",
  onCaptured,
  mode,
  onModeChange,
}: {
  env: string;
  focusTick: number;
  defaultProjectId?: string;
  onCaptured?: () => void;
  mode: CaptureMode;
  onModeChange: (m: CaptureMode) => void;
}) {
  const [title, setTitle] = useState("");
  const [notes, setNotes] = useState("");
  const [projectId, setProjectId] = useState(defaultProjectId);
  const [aiText, setAiText] = useState("");
  const titleRef = useRef<HTMLInputElement>(null);
  const aiRef = useRef<HTMLTextAreaElement>(null);
  const qc = useQueryClient();

  useEffect(() => {
    setProjectId(defaultProjectId);
  }, [defaultProjectId]);

  const { data: projects } = useQuery({
    queryKey: ["projects", env, false],
    queryFn: () => api.listProjects(env, false),
  });

  const isRegular = mode === "regular" || mode === "regular-top";

  useEffect(() => {
    if (isRegular) {
      titleRef.current?.focus();
      titleRef.current?.select();
    } else {
      aiRef.current?.focus();
      aiRef.current?.select();
    }
  }, [focusTick, isRegular]);

  const invalidateAfterCapture = (assignedProjectId?: string | null) => {
    qc.invalidateQueries({ queryKey: ["items", env] });
    qc.invalidateQueries({ queryKey: ["search-corpus", env], refetchType: "none" });
    qc.invalidateQueries({ queryKey: ["snapshot-status"] });
    if (assignedProjectId) {
      invalidateProjectQueries(qc, env, assignedProjectId);
    }
  };

  const mut = useMutation({
    mutationFn: async () => {
      const item = await api.captureItem(env, title.trim(), notes, {
        energy: "low",
        time_minutes: 5,
        at_top: mode === "regular-top",
      });
      if (projectId) {
        await api.updateItem(env, item.id, { project: projectId });
        return api.moveItem(env, item.id, "next");
      }
      return item;
    },
    onSuccess: () => {
      setTitle("");
      setNotes("");
      setProjectId(defaultProjectId);
      invalidateAfterCapture(projectId);
      onCaptured?.();
    },
  });

  const aiMut = useMutation({
    mutationFn: () => api.captureItemAi(env, aiText.trim()),
    onSuccess: (result) => {
      setAiText("");
      toasts.show("success", result.summary);
      invalidateAfterCapture(result.item.project);
      onCaptured?.();
    },
  });

  const sortedProjects = projects ? sortProjects(projects) : [];
  const destination = projectId ? "next + project" : "inbox";

  const submit = () => {
    if (title.trim()) mut.mutate();
  };
  const submitAi = () => {
    if (aiText.trim()) aiMut.mutate();
  };

  const ModeToggle = (
    <div className="capture-mode chip-toggle-group">
      {MODES.map((opt) => (
        <button
          key={opt.value}
          type="button"
          className="chip-toggle"
          aria-pressed={mode === opt.value}
          onClick={() => onModeChange(opt.value)}
          title={opt.title}
        >
          {opt.label}
        </button>
      ))}
    </div>
  );

  if (mode === "ai") {
    return (
      <form
        className="capture"
        onSubmit={(e) => {
          e.preventDefault();
          submitAi();
        }}
        onKeyDown={(e) => {
          if ((e.metaKey || e.ctrlKey) && e.key === "Enter") {
            e.preventDefault();
            submitAi();
          }
        }}
      >
        {ModeToggle}
        <textarea
          ref={aiRef}
          rows={3}
          placeholder="Describe the action; AI will extract title, project, energy, dates…"
          value={aiText}
          onChange={(e) => setAiText(e.target.value)}
        />
        <div className="capture-row">
          <Button
            type="submit"
            className="primary"
            disabled={!aiText.trim()}
            busy={aiMut.isPending}
          >
            Capture with AI
          </Button>
          <div className="capture-hint">→ routed automatically · Cmd/Ctrl+Enter to submit</div>
        </div>
      </form>
    );
  }

  return (
    <form
      className="capture"
      onSubmit={(e) => {
        e.preventDefault();
        submit();
      }}
      onKeyDown={(e) => {
        if ((e.metaKey || e.ctrlKey) && e.key === "Enter") {
          e.preventDefault();
          submit();
        }
      }}
    >
      {ModeToggle}
      <div className="capture-row">
        <input
          ref={titleRef}
          type="text"
          placeholder={projectId ? "Capture to next…" : "Capture to inbox…"}
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
        <Button type="submit" className="primary" disabled={!title.trim()} busy={mut.isPending}>
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
          <select value={projectId} onChange={(e) => setProjectId(e.target.value)}>
            <option value="">— (keep in inbox)</option>
            {sortedProjects.map((p) => (
              <option key={p.id} value={p.id}>
                {p.title}
              </option>
            ))}
          </select>
        </label>
        <div className="capture-hint">
          → {destination}
          {mode === "regular-top" && !projectId ? " (top)" : ""}
          {" · energy=low · time=5min"}
        </div>
      </div>
    </form>
  );
}
