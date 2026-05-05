import { useEffect, useRef, useState } from "react";
import ReactMarkdown, { type Components } from "react-markdown";
import remarkGfm from "remark-gfm";

const SESSION_START_MS = Date.now();
const FRESH_WINDOW_MS = 2000;

const markdownComponents: Components = {
  a: ({ node: _node, ...props }) => <a {...props} target="_blank" rel="noopener noreferrer" />,
};
import type { Item, Project } from "./api";
import { useItemPatch } from "./ItemEdit";
import { contextChipStyle } from "./context-colors";
import { useSelection } from "./SelectionContext";

export function ItemCard({
  env,
  item,
  projects,
}: {
  env: string;
  item: Item;
  projects: Project[] | undefined;
}) {
  const { selectedId, hoveredId, select, setHover } = useSelection();
  const selected = selectedId === item.id;
  const hovered = hoveredId === item.id;

  const onMouseEnter = (e: React.MouseEvent<HTMLDivElement>) => {
    const el = e.currentTarget;
    const scrollContainer = el.closest("main");
    if (!scrollContainer) return;
    const cardRect = el.getBoundingClientRect();
    const containerRect = scrollContainer.getBoundingClientRect();
    const topOffset = cardRect.top - containerRect.top;
    setHover(item.id, topOffset);
  };

  const className = [
    "item",
    selected ? "selected" : "",
    hovered && !selected ? "hovered" : "",
    item.working_on ? "working-on" : "",
  ]
    .filter(Boolean)
    .join(" ");

  const createdMs = new Date(item.created).getTime();
  const isFresh = createdMs > SESSION_START_MS && Date.now() - createdMs < FRESH_WINDOW_MS;

  return (
    <div
      className={className}
      data-fresh={isFresh ? "true" : undefined}
      onClick={(e) => {
        if (selected) return;
        if ((e.target as HTMLElement).closest(".item-actions")) return;
        if ((e.target as HTMLElement).closest("a")) return;
        if ((e.target as HTMLElement).closest(".working-on-toggle")) return;
        select(item.id);
      }}
      onMouseEnter={onMouseEnter}
    >
      {selected ? (
        <SelectedInListCard env={env} item={item} />
      ) : (
        <CollapsedCard env={env} item={item} projects={projects} />
      )}
    </div>
  );
}

function WorkingOnToggle({ env, item }: { env: string; item: Item }) {
  const { patch } = useItemPatch(env, item.id);
  const active = item.working_on;
  return (
    <button
      type="button"
      className={`working-on-toggle${active ? " active" : ""}`}
      aria-pressed={active}
      aria-label={active ? "Unpin working on" : "Mark as working on"}
      title={active ? "Working on this — click to unpin" : "Mark as working on"}
      onClick={(e) => {
        e.stopPropagation();
        patch({ working_on: !active }, { debounce: 200 });
      }}
    >
      <span aria-hidden>📌</span>
    </button>
  );
}

function formatUrl(url: string): string {
  try {
    const u = new URL(url);
    const path = u.pathname.replace(/\/$/, "");
    if (!path || path === "/") return u.hostname;
    const segments = path.split("/").filter(Boolean);
    const short =
      segments.length <= 2
        ? segments.join("/")
        : `${segments[0]}/…/${segments[segments.length - 1]}`;
    return `${u.hostname}/${short}`;
  } catch {
    return url.length > 40 ? url.slice(0, 37) + "…" : url;
  }
}

const URL_RE = /https?:\/\/[^\s)<>]+/g;

function extractUrls(text: string): string[] {
  const matches = text.match(URL_RE);
  if (!matches) return [];
  // Deduplicate preserving order
  return [...new Set(matches)];
}

function ItemLinks({ body }: { body: string }) {
  const urls = body ? extractUrls(body) : [];
  if (urls.length === 0) return null;
  return (
    <div className="item-links">
      {urls.map((url) => (
        <a
          key={url}
          href={url}
          target="_blank"
          rel="noopener noreferrer"
          className="link-chip"
          title={url}
        >
          {formatUrl(url)}
        </a>
      ))}
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
      <div className="item-title-row">
        <WorkingOnToggle env={env} item={item} />
        <div className="item-title">{item.title}</div>
      </div>
      {item.body && (
        <div className="item-body">
          <ReactMarkdown remarkPlugins={[remarkGfm]} components={markdownComponents}>
            {item.body}
          </ReactMarkdown>
        </div>
      )}
      <ItemLinks body={item.body} />
      <div className="item-meta">
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
        {item.due && (
          <span className={`chip${item.overdue ? " chip-overdue" : ""}`}>due {item.due}</span>
        )}
        {item.defer_until && (
          <span className="chip">defer {formatDeferChip(item.defer_until)}</span>
        )}
      </div>
    </>
  );
}

function formatDeferChip(iso: string): string {
  const m = iso.match(/^(\d{4}-\d{2}-\d{2})T(\d{2}):(\d{2})/);
  if (!m) return iso;
  const [, date, hh, mm] = m;
  if (hh === "00" && mm === "00") return date;
  return `${date} ${hh}:${mm}`;
}

function SelectedInListCard({ env, item }: { env: string; item: Item }) {
  const { select } = useSelection();
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
    // Only reset on id change. Including title/body would clobber in-flight edits.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [item.id]);

  const saveAndDeselect = (e: React.KeyboardEvent) => {
    if ((e.metaKey || e.ctrlKey) && e.key === "Enter") {
      e.preventDefault();
      void flush();
      select(null);
    }
  };

  return (
    <div className="item-selected-in-list">
      <input
        className="title-input"
        value={localTitle}
        onChange={(e) => {
          setLocalTitle(e.target.value);
          patch({ title: e.target.value }, { debounce: 500 });
        }}
        onKeyDown={saveAndDeselect}
        placeholder="Title"
        autoFocus
      />
      <textarea
        className="body-input"
        rows={4}
        value={localBody}
        onChange={(e) => {
          setLocalBody(e.target.value);
          patch({ body: e.target.value }, { debounce: 500 });
        }}
        onKeyDown={saveAndDeselect}
        placeholder="Notes (markdown)…"
      />
      <ItemLinks body={localBody} />
    </div>
  );
}
