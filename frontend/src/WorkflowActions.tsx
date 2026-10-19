import { useMutation, useQueryClient } from "@tanstack/react-query";
import { api, type AgentTarget, type Bucket, type Item } from "./api";
import { Button } from "./Button";
import { invalidateItemQueries, invalidateItemQueriesPreservingInbox } from "./ItemEdit";
import { MergeButton } from "./MergeButton";
import { GrabRow } from "./GrabBags";
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
  const invalidate = (outcome?: Bucket) => {
    if (inInboxProcessing && processed) {
      invalidateItemQueriesPreservingInbox(qc, env, item.id);
      processed.markProcessed(item.id, outcome);
    } else {
      invalidateItemQueries(qc, env, item.id);
    }
    select(null); // Clear selection so the user can move to the next item.
  };

  const moveMut = useMutation<Item, Error, Bucket>({
    mutationFn: (to) => api.moveItem(env, item.id, to),
    onSuccess: (_updated, to) => invalidate(to),
  });
  const completeMut = useMutation({
    mutationFn: () => api.completeItem(env, item.id),
    onSuccess: () => invalidate("archive"),
  });
  // Marked done during this inbox session: the row is greyed out (and the
  // detail pane may already show it as archived), but uncomplete stays
  // available and puts it straight back into the inbox.
  const doneInThisSession = processed?.processedOutcome(item.id) === "archive";
  // Outside that flow we don't know where the item came from: a project
  // action belongs in next, anything else goes back to inbox for triage.
  const uncompleteTo: Bucket = doneInThisSession || !item.project ? "inbox" : "next";
  const uncompleteMut = useMutation<Item, Error, void>({
    mutationFn: () => api.moveItem(env, item.id, uncompleteTo),
    onSuccess: (updated) => {
      if (doneInThisSession && processed) {
        invalidateItemQueriesPreservingInbox(qc, env, item.id);
        qc.setQueriesData<Item[]>(
          {
            predicate: (q) =>
              q.queryKey[0] === "items" && q.queryKey[1] === env && q.queryKey[2] === "inbox",
          },
          (list) => list?.map((i) => (i.id === updated.id ? updated : i)),
        );
        processed.unmarkProcessed(item.id);
      } else {
        invalidateItemQueries(qc, env, item.id);
      }
    },
  });
  const deleteMut = useMutation({
    mutationFn: () => api.deleteItem(env, item.id),
    onSuccess: () => invalidate("trash"),
  });
  const purgeMut = useMutation({
    mutationFn: () => api.purgeItem(env, item.id),
    onSuccess: () => invalidate(),
  });
  const launchMut = useMutation<void, Error, AgentTarget>({
    mutationFn: (target) => api.launchAgent(env, item.id, target),
  });
  const isLaunching = (target: AgentTarget) =>
    launchMut.isPending && launchMut.variables === target;

  // Once an item has been processed in this inbox session the row stays
  // visible but the server-side state has moved on; lock the buttons so an
  // accidental second click doesn't chain another mutation against stale
  // status. The row is still visible / inspectable; the user navigates
  // away (or reloads) to drop it.
  const alreadyProcessed = processed?.isProcessed(item.id) ?? false;
  const mutating =
    moveMut.isPending ||
    uncompleteMut.isPending ||
    completeMut.isPending ||
    deleteMut.isPending ||
    purgeMut.isPending ||
    launchMut.isPending;
  const busy = alreadyProcessed || mutating;

  const isMoving = (to: Bucket) => moveMut.isPending && moveMut.variables === to;

  const inTrash = item.status === "trash";
  const isArchive = item.status === "archive";

  return (
    <>
      <div className="item-actions" onClick={(e) => e.stopPropagation()}>
        {inTrash ? (
          <>
            <Button
              onClick={() => moveMut.mutate("inbox")}
              busy={isMoving("inbox")}
              disabled={busy}
            >
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
        ) : isArchive || doneInThisSession ? (
          <>
            <Button
              onClick={() => uncompleteMut.mutate()}
              busy={uncompleteMut.isPending}
              disabled={mutating}
              title={`Reopen this item in ${uncompleteTo}`}
            >
              ↺ uncomplete
            </Button>
            <Button
              onClick={() => moveMut.mutate("reference")}
              busy={isMoving("reference")}
              disabled={busy}
              title="File this completed item as reference"
            >
              → reference
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
            {(["next", "waiting", "someday", "reference"] as const).map((b) =>
              item.status === b ? (
                <Button key={b} aria-pressed disabled title={`Currently in ${b}`}>
                  {b}
                </Button>
              ) : (
                <Button
                  key={b}
                  onClick={() => moveMut.mutate(b)}
                  busy={isMoving(b)}
                  disabled={busy}
                  title={
                    b === "reference"
                      ? "File as reference — also marks the item complete"
                      : undefined
                  }
                >
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
              onClick={() => launchMut.mutate("iterm")}
              busy={isLaunching("iterm")}
              disabled={busy}
              title="Launch a Claude Code session in iTerm with this item as the prompt"
            >
              🤖 agent
            </Button>
            <Button
              onClick={() => launchMut.mutate("desktop")}
              busy={isLaunching("desktop")}
              disabled={busy}
              title="Open a Claude Code session in the Claude desktop app with this item as the prompt"
            >
              🖥️ desktop agent
            </Button>
            <MergeButton env={env} item={item} />
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
      <GrabRow env={env} item={item} />
    </>
  );
}
