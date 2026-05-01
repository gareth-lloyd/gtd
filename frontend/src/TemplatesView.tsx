import { useQuery } from "@tanstack/react-query";
import { api, type Project, type Template } from "./api";
import { contextChipStyle } from "./context-colors";
import { useEnvParam } from "./useEnvParam";

export function TemplatesView() {
  const env = useEnvParam();
  const { data: templates, isLoading } = useQuery({
    queryKey: ["templates", env],
    queryFn: () => api.listTemplates(env),
  });
  const { data: projects } = useQuery({
    queryKey: ["projects", env, true],
    queryFn: () => api.listProjects(env, true),
  });

  if (isLoading) return <div className="empty">Loading…</div>;

  const list = templates ?? [];
  if (list.length === 0) {
    return (
      <div className="empty">
        No recurring templates yet. Add one under <code>data/{env}/templates/</code> and it will
        appear here.
      </div>
    );
  }

  const sorted = [...list].sort((a, b) => {
    const ad = a.next_due ?? "zzz";
    const bd = b.next_due ?? "zzz";
    if (ad === bd) return a.title.localeCompare(b.title);
    return ad < bd ? -1 : 1;
  });

  const projectsById = new Map((projects ?? []).map((p) => [p.id, p]));

  return (
    <ul className="template-list">
      {sorted.map((t) => (
        <li key={t.id}>
          <TemplateRow
            template={t}
            project={t.project ? (projectsById.get(t.project) ?? null) : null}
          />
        </li>
      ))}
    </ul>
  );
}

function TemplateRow({ template, project }: { template: Template; project: Project | null }) {
  const dueSoon = template.next_due === "now";
  return (
    <div className={`template-row${dueSoon ? " due-now" : ""}`}>
      <div className="template-header">
        <span className="template-title">{template.title}</span>
        <span className="recurrence-badge">↻ {template.recurrence}</span>
        <span className="template-due">
          {dueSoon
            ? "due now"
            : template.next_due
              ? `next ${template.next_due}`
              : "schedule unknown"}
        </span>
      </div>
      {template.body && <div className="template-body">{template.body}</div>}
      <div className="template-meta">
        {project && <span className="chip project-chip">📁 {project.title}</span>}
        {template.contexts.map((c) => (
          <span key={c} className="chip context-chip" style={contextChipStyle(c)}>
            @{c}
          </span>
        ))}
        {template.energy && <span className="chip">⚡{template.energy}</span>}
        {template.time_minutes != null && <span className="chip">{template.time_minutes}m</span>}
        {template.area && <span className="chip">{template.area}</span>}
        <span className="chip last-spawned">
          {template.last_spawned ? `last spawned ${template.last_spawned}` : "never spawned"}
        </span>
      </div>
    </div>
  );
}
