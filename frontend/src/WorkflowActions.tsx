import { useMutation, useQueryClient } from "@tanstack/react-query";
import { api, type Bucket, type Item } from "./api";
import { Button } from "./Button";
import { invalidateItemQueries, invalidateItemQueriesPreservingInbox } from "./ItemEdit";
import { useSelection } from "./SelectionContext";
import { useProcessedItems } from "./ProcessedItemsContext";

export function WorkflowActions({ env, item }: { env: string; item: Item }) {
  const qc = useQueryClient();
  const { select } = useSelection();
  const processed = useProcessedItems();
  // On the inbox route, treat the action as an inbox-processing step: grey
  // the item out locally rather than letting the inbox list refetch remove
  // it. The user can keep scanning the rest of the inbox without items
  // vanishing under their cursor.
  const inInboxProcessing = processed?.active === true && item.status === "inbox";
  const invalidate = () => {
    if (inInboxProcessing && processed) {
      invalidateItemQueriesPreservingInbox(qc, env, item.id);
      processed.markProcessed(item.id);
    } else {
      invalidateItemQueries(qc, env, item.id);
    }
    select(null); // Clear selection so the user can move to the next item.
  };

  const moveMut = useMutation<Item, Error, Bucket>({
    mutationFn: (to) => api.moveItem(env, item.id, to),
    onSuccess: invalidate,
  });
  const completeMut = useMutation({
    mutationFn: () => api.completeItem(env, item.id),
    onSuccess: invalidate,
  });
  const deleteMut = useMutation({
    mutationFn: () => api.deleteItem(env, item.id),
    onSuccess: invalidate,
  });
  const purgeMut = useMutation({
    mutationFn: () => api.purgeItem(env, item.id),
    onSuccess: invalidate,
  });
  const launchMut = useMutation({
    mutationFn: () => api.launchAgent(env, item.id),
  });

  // Once an item has been processed in this inbox session the row stays
  // visible but the server-side state has moved on; lock the buttons so an
  // accidental second click doesn't chain another mutation against stale
  // status. The row is still visible / inspectable; the user navigates
  // away (or reloads) to drop it.
  const alreadyProcessed = processed?.isProcessed(item.id) ?? false;
  const busy =
    alreadyProcessed ||
    moveMut.isPending ||
    completeMut.isPending ||
    deleteMut.isPending ||
    purgeMut.isPending ||
    launchMut.isPending;

  const isMoving = (to: Bucket) => moveMut.isPending && moveMut.variables === to;

  const inTrash = item.status === "trash";
  const isArchive = item.status === "archive";

  return (
    <div className="item-actions" onClick={(e) => e.stopPropagation()}>
      {inTrash ? (
        <>
          <Button onClick={() => moveMut.mutate("inbox")} busy={isMoving("inbox")} disabled={busy}>
            ↺ restore
          </Button>
          <Button
            className="danger"
            onClick={() => {
              if (confirm(`Permanently delete "${item.title}"?`)) purgeMut.mutate();
            }}
            busy={purgeMut.isPending}
            disabled={busy}
          >
            Purge
          </Button>
        </>
      ) : isArchive ? (
        <>
          <Button onClick={() => moveMut.mutate("next")} busy={isMoving("next")} disabled={busy}>
            ↺ uncomplete
          </Button>
          <Button
            className="danger"
            onClick={() => deleteMut.mutate()}
            busy={deleteMut.isPending}
            disabled={busy}
          >
            Delete
          </Button>
        </>
      ) : (
        <>
          {(["next", "waiting", "someday"] as const).map((b) =>
            item.status === b ? (
              <Button key={b} aria-pressed disabled title={`Currently in ${b}`}>
                {b}
              </Button>
            ) : (
              <Button key={b} onClick={() => moveMut.mutate(b)} busy={isMoving(b)} disabled={busy}>
                → {b}
              </Button>
            ),
          )}
          <Button
            data-completing={completeMut.isPending ? "true" : undefined}
            onClick={() => completeMut.mutate()}
            busy={completeMut.isPending}
            disabled={busy}
          >
            ✓ done
          </Button>
          <Button
            onClick={() => launchMut.mutate()}
            busy={launchMut.isPending}
            disabled={busy}
            title="Launch a Claude Code session in iTerm with this item as the prompt"
          >
            🤖 agent
          </Button>
          <Button
            className="danger"
            onClick={() => deleteMut.mutate()}
            busy={deleteMut.isPending}
            disabled={busy}
          >
            Delete
          </Button>
        </>
      )}
    </div>
  );
}
