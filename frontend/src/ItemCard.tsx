import { useEffect, useLayoutEffect, useRef, useState } from "react";
import type { Item, Project } from "./api";
import { useItemPatch } from "./ItemEdit";
import { contextChipStyle } from "./context-colors";
import { Markdown } from "./markdown";
import { useSelection } from "./SelectionContext";
import { useSpotlight } from "./spotlight";

const SESSION_START_MS = Date.now();
const FRESH_WINDOW_MS = 2000;

const COLLAPSED_BODY_MAX_REM = 14;
const EDITOR_BODY_MAX_REM = 24;
const REM_PX = 16;

export function ItemCard({
  env,
  item,
  projects,
}: {
  env: string;
  item: Item;
  projects: Project[] | undefined;
}) {
  const { selectedId, editingId, hoveredId, select, edit, setHover } = useSelection();
  const selected = selectedId === item.id;
  const editing = editingId === item.id;
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
    editing ? "editing" : "",
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
      data-item-id={item.id}
      data-fresh={isFresh ? "true" : undefined}
      onClick={(e) => {
        if (editing) return;
        if ((e.target as HTMLElement).closest(".item-actions")) return;
        if ((e.target as HTMLElement).closest("a")) return;
        if ((e.target as HTMLElement).closest(".working-on-toggle")) return;
        if ((e.target as HTMLElement).closest(".spotlight-toggle")) return;
        if (selected) edit(item.id);
        else select(item.id);
      }}
      onMouseEnter={onMouseEnter}
    >
      {editing ? (
        <SelectedInListCard env={env} item={item} />
      ) : (
        <CollapsedCard env={env} item={item} projects={projects} />
      )}
    </div>
  );
}

function SpotlightToggle({ id }: { id: string }) {
  const { spotlightId, setSpotlight } = useSpotlight();
  const { edit } = useSelection();
  const active = spotlightId === id;
  return (
    <button
      type="button"
      className={`spotlight-toggle${active ? " active" : ""}`}
      aria-pressed={active}
      aria-label={active ? "Exit spotlight" : "Focus on this item"}
      title={active ? "Exit spotlight" : "Focus on this item"}
      onClick={(e) => {
        e.stopPropagation();
        if (active) {
          setSpotlight(null);
        } else {
          setSpotlight(id);
          edit(id);
        }
      }}
    >
      <span aria-hidden>{active ? "✕" : "◎"}</span>
    </button>
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
        <SpotlightToggle id={item.id} />
      </div>
      {item.body && (
        <ClippedBlock
          maxHeightRem={COLLAPSED_BODY_MAX_REM}
          contentClassName="item-body"
          contentKey={item.body}
        >
          <Markdown source={item.body} />
        </ClippedBlock>
      )}
      <ItemLinks body={item.body} />
      <div className="item-meta">
        {item.output && (
          <span className="chip" title="Agent log present — expand to read">
            🤖 log
          </span>
        )}
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
  const { stopEditing } = useSelection();
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

  const saveAndStopEditing = (e: React.KeyboardEvent) => {
    if ((e.metaKey || e.ctrlKey) && e.key === "Enter") {
      e.preventDefault();
      void flush();
      stopEditing();
    }
  };

  return (
    <div className="item-selected-in-list" data-editing>
      <input
        className="title-input"
        value={localTitle}
        onChange={(e) => {
          setLocalTitle(e.target.value);
          patch({ title: e.target.value }, { debounce: 500 });
        }}
        onKeyDown={saveAndStopEditing}
        placeholder="Title"
        autoFocus
      />
      <AutoGrowTextarea
        className="body-input"
        value={localBody}
        onChange={(e) => {
          setLocalBody(e.target.value);
          patch({ body: e.target.value }, { debounce: 500 });
        }}
        onKeyDown={saveAndStopEditing}
        placeholder="Notes (markdown)…"
        minRows={4}
        maxHeightRem={EDITOR_BODY_MAX_REM}
      />
      <ItemLinks body={localBody} />
    </div>
  );
}

function ShowAllButton({ onExpand }: { onExpand: () => void }) {
  return (
    <button
      type="button"
      className="clipped-block-expand"
      onClick={(e) => {
        e.stopPropagation();
        onExpand();
      }}
    >
      Show all ↓
    </button>
  );
}

function ClippedBlock({
  maxHeightRem,
  contentClassName,
  contentKey,
  children,
}: {
  maxHeightRem: number;
  contentClassName?: string;
  /** Stable string used as the measurement effect's dependency, so we don't
   * remeasure on every parent re-render that constructs new `children`. */
  contentKey?: string;
  children: React.ReactNode;
}) {
  const ref = useRef<HTMLDivElement>(null);
  const [expanded, setExpanded] = useState(false);
  const [clipped, setClipped] = useState(false);

  useLayoutEffect(() => {
    const el = ref.current;
    if (!el) return;
    setClipped(el.scrollHeight > maxHeightRem * REM_PX + 1);
  }, [contentKey, maxHeightRem]);

  const innerClass = ["clipped-block-content", contentClassName].filter(Boolean).join(" ");
  return (
    <div className="clipped-block">
      <div
        ref={ref}
        className={innerClass}
        style={expanded ? undefined : { maxHeight: `${maxHeightRem}rem`, overflow: "hidden" }}
      >
        {children}
      </div>
      {clipped && !expanded && <ShowAllButton onExpand={() => setExpanded(true)} />}
    </div>
  );
}

function AutoGrowTextarea({
  className,
  value,
  onChange,
  onKeyDown,
  placeholder,
  minRows,
  maxHeightRem,
}: {
  className?: string;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLTextAreaElement>) => void;
  onKeyDown?: (e: React.KeyboardEvent<HTMLTextAreaElement>) => void;
  placeholder?: string;
  minRows: number;
  maxHeightRem: number;
}) {
  const ref = useRef<HTMLTextAreaElement>(null);
  const [expanded, setExpanded] = useState(false);
  const [clipped, setClipped] = useState(false);

  useLayoutEffect(() => {
    const el = ref.current;
    if (!el) return;
    // Reset height so shrinking works, then set to natural content height.
    el.style.height = "auto";
    const maxPx = maxHeightRem * REM_PX;
    const natural = el.scrollHeight;
    if (!expanded && natural > maxPx) {
      el.style.height = `${maxPx}px`;
      setClipped(true);
    } else {
      el.style.height = `${natural}px`;
      setClipped(false);
    }
  }, [value, expanded, maxHeightRem]);

  return (
    <div className="autogrow-wrap">
      <textarea
        ref={ref}
        className={`${className ?? ""} autogrow-textarea`.trim()}
        rows={minRows}
        value={value}
        onChange={onChange}
        onKeyDown={onKeyDown}
        placeholder={placeholder}
      />
      {clipped && !expanded && <ShowAllButton onExpand={() => setExpanded(true)} />}
    </div>
  );
}
