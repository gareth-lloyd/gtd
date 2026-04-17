import { useEffect, useRef, useState } from 'react';
import ReactMarkdown, { type Components } from 'react-markdown';
import remarkGfm from 'remark-gfm';

const markdownComponents: Components = {
  a: ({ node: _node, ...props }) => (
    <a {...props} target="_blank" rel="noopener noreferrer" />
  ),
};
import type { Item, Project } from './api';
import { useItemPatch } from './ItemEdit';
import { contextChipStyle } from './context-colors';
import { useSelection } from './SelectionContext';

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
  const cardRef = useRef<HTMLDivElement>(null);

  const onMouseEnter = () => {
    if (!cardRef.current) return;
    const scrollContainer = cardRef.current.closest('.content-area');
    if (!scrollContainer) return;
    const cardRect = cardRef.current.getBoundingClientRect();
    const containerRect = scrollContainer.getBoundingClientRect();
    const topOffset = cardRect.top - containerRect.top + scrollContainer.scrollTop;
    setHover(item.id, topOffset);
  };

  const className = [
    'item',
    selected ? 'selected' : '',
    hovered && !selected ? 'hovered' : '',
  ]
    .filter(Boolean)
    .join(' ');

  return (
    <div
      ref={cardRef}
      className={className}
      onClick={(e) => {
        if (selected) return;
        if ((e.target as HTMLElement).closest('.item-actions')) return;
        select(item.id);
      }}
      onMouseEnter={onMouseEnter}
    >
      {selected ? (
        <SelectedInListCard env={env} item={item} />
      ) : (
        <CollapsedCard item={item} projects={projects} />
      )}
    </div>
  );
}

function CollapsedCard({
  item,
  projects,
}: {
  item: Item;
  projects: Project[] | undefined;
}) {
  const project = projects?.find((p) => p.id === item.project) ?? null;

  return (
    <>
      <div className="item-title">{item.title}</div>
      {item.body && (
        <div className="item-body">
          <ReactMarkdown remarkPlugins={[remarkGfm]} components={markdownComponents}>
            {item.body}
          </ReactMarkdown>
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
      </div>
    </>
  );
}

function SelectedInListCard({
  env,
  item,
}: {
  env: string;
  item: Item;
}) {
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
  }, [item.id]);

  const saveAndDeselect = (e: React.KeyboardEvent) => {
    if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') {
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
    </div>
  );
}
