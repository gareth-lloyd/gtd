import { useState } from "react";
import { Link } from "react-router-dom";
import type { Item, Project } from "./api";
import { useItemPatch } from "./ItemEdit";
import { contextChipStyle } from "./context-colors";
import { Markdown } from "./markdown";
import { useSelection } from "./SelectionContext";
import { useSpotlight } from "./spotlight";
import { useProcessedItems } from "./ProcessedItemsContext";
import { ItemLinks } from "./ItemLinks";
import { ClippedBlock } from "./ClippedBlock";
import { AutoGrowTextarea } from "./AutoGrowTextarea";

const SESSION_START_MS = Date.now();
const FRESH_WINDOW_MS = 2000;

const COLLAPSED_BODY_MAX_REM = 14;
const EDITOR_BODY_MAX_REM = 24;

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
  const processed = useProcessedItems();
  const isProcessed = processed?.isProcessed(item.id) ?? false;
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
    isProcessed ? "processed" : "",
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
        // Markdown-body anchors don't stop propagation themselves; the
        // other interactive children (`.item-actions`, `.working-on-toggle`,
        // `.spotlight-toggle`) already do.
        if ((e.target as HTMLElement).closest("a")) return;
        if (selected) edit(item.id);
        else select(item.id);
      }}
      onMouseEnter={onMouseEnter}
    >
      {editing ? (
        <InlineEditor key={item.id} env={env} item={item} />
      ) : (
        <CollapsedCard env={env} item={item} projects={projects} />
      )}
    </div>
  );
}

function SpotlightToggle({ id }: { id: string }) {
  const { spotlightId, setSpotlight } = useSpotlight();
  const { select } = useSelection();
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
          select(id);
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
          <Link
            to={`/${env}/items/${item.id}/agent`}
            className="chip chip-link"
            title="Open the agent log in a focused reading view"
            onClick={(e) => e.stopPropagation()}
          >
            🤖 log
          </Link>
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

function InlineEditor({ env, item }: { env: string; item: Item }) {
  const { stopEditing } = useSelection();
  const { patch, flush } = useItemPatch(env, item.id);

  const [localTitle, setLocalTitle] = useState(item.title);
  const [localBody, setLocalBody] = useState(item.body);

  const saveAndStopEditing = (e: React.KeyboardEvent) => {
    if ((e.metaKey || e.ctrlKey) && e.key === "Enter") {
      e.preventDefault();
      void flush();
      stopEditing();
    }
  };

  return (
    <div className="item-inline-editor" data-editing>
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
