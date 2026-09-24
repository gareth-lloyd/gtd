import { useEffect, useRef, useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { api, type Item } from "./api";
import { Button } from "./Button";
import { invalidateItemQueries } from "./ItemEdit";
import { useSearchIndex } from "./search";
import { toasts } from "./toast";

const RESULT_LIMIT = 20;

/**
 * "merge other": pick a second item via search and fold it into `item`.
 * The current item keeps its project and bucket; the picked item's content
 * is merged in by the AI and the picked item is moved to trash.
 */
export function MergeButton({ env, item }: { env: string; item: Item }) {
  const [open, setOpen] = useState(false);
  const qc = useQueryClient();

  const mut = useMutation<Item, Error, Item>({
    mutationFn: (source) => api.mergeItem(env, item.id, source.id),
    onSuccess: (merged, source) => {
      invalidateItemQueries(qc, env, item.id);
      invalidateItemQueries(qc, env, source.id);
      setOpen(false);
      toasts.show("success", `Merged "${source.title}" into "${merged.title}" — original trashed`);
    },
  });

  function pick(source: Item) {
    const ok = confirm(
      `Merge "${source.title}" into "${item.title}"?\n\n` +
        `"${source.title}" will be moved to trash once merged.`,
    );
    if (ok) mut.mutate(source);
  }

  return (
    <>
      <Button
        onClick={() => setOpen(true)}
        busy={mut.isPending}
        title="Search for another item and merge its content into this one"
      >
        ⇄ merge other
      </Button>
      {open && (
        <MergePicker
          env={env}
          currentId={item.id}
          busy={mut.isPending}
          onPick={pick}
          onClose={() => setOpen(false)}
        />
      )}
    </>
  );
}

function MergePicker({
  env,
  currentId,
  busy,
  onPick,
  onClose,
}: {
  env: string;
  currentId: string;
  busy: boolean;
  onPick: (source: Item) => void;
  onClose: () => void;
}) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [query, setQuery] = useState("");
  const { index, isLoading } = useSearchIndex(env, { enabled: true });

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const hasQuery = query.trim().length > 0;
  const hits = index
    ? index
        .search(query, RESULT_LIMIT + 1)
        .filter((h) => h.kind === "item" && h.id !== currentId)
        .slice(0, RESULT_LIMIT)
        .map((h) => (h.kind === "item" ? h.item : null))
        .filter((i): i is Item => i !== null)
    : [];

  return (
    <div
      className="capture-overlay"
      onClick={onClose}
      onKeyDown={(e) => {
        if (e.key === "Escape") {
          e.stopPropagation();
          onClose();
        }
      }}
    >
      <div
        className="capture merge-picker"
        role="dialog"
        aria-label="Merge another item into this one"
        onClick={(e) => e.stopPropagation()}
      >
        <input
          ref={inputRef}
          type="search"
          placeholder="Search for the item to merge in…"
          value={query}
          disabled={busy}
          onChange={(e) => setQuery(e.target.value)}
        />
        <div className="merge-picker-results">
          {isLoading && !index && <div className="search-empty">Building index…</div>}
          {index && !hasQuery && (
            <div className="search-empty">Type to search. The picked item will be trashed.</div>
          )}
          {index && hasQuery && hits.length === 0 && (
            <div className="search-empty">No matches.</div>
          )}
          {hits.map((hit) => (
            <div
              key={hit.id}
              className="search-hit"
              role="button"
              tabIndex={0}
              onClick={() => !busy && onPick(hit)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !busy) onPick(hit);
              }}
            >
              <span className="hit-title">{hit.title}</span>
              <span className="hit-meta">
                <span className="chip">{hit.status}</span>
                {hit.project && <span className="chip project-chip">📁 {hit.project}</span>}
              </span>
            </div>
          ))}
        </div>
        <div className="capture-hint">
          Esc to cancel · the current item keeps its project and bucket
        </div>
      </div>
    </div>
  );
}
