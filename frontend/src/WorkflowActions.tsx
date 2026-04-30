import { useMutation, useQueryClient } from '@tanstack/react-query';
import { api, type Bucket, type Item } from './api';
import { Button } from './Button';
import { invalidateItemQueries } from './ItemEdit';
import { useSelection } from './SelectionContext';

export function WorkflowActions({
  env,
  item,
}: {
  env: string;
  item: Item;
}) {
  const qc = useQueryClient();
  const { select } = useSelection();
  const invalidate = () => {
    invalidateItemQueries(qc, env, item.id);
    select(null); // Clear selection when item moves/completes/deletes
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

  const busy =
    moveMut.isPending ||
    completeMut.isPending ||
    deleteMut.isPending ||
    purgeMut.isPending;

  const isMoving = (to: Bucket) =>
    moveMut.isPending && moveMut.variables === to;

  const inTrash = item.status === 'trash';
  const isArchive = item.status === 'archive';

  return (
    <div
      className="item-actions"
      onClick={(e) => e.stopPropagation()}
    >
      {inTrash ? (
        <>
          <Button
            onClick={() => moveMut.mutate('inbox')}
            busy={isMoving('inbox')}
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
      ) : isArchive ? (
        <>
          <Button
            onClick={() => moveMut.mutate('next')}
            busy={isMoving('next')}
            disabled={busy}
          >
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
          {(['next', 'waiting', 'someday'] as const)
            .filter((b) => item.status !== b)
            .map((b) => (
              <Button
                key={b}
                onClick={() => moveMut.mutate(b)}
                busy={isMoving(b)}
                disabled={busy}
              >
                → {b}
              </Button>
            ))}
          <Button
            onClick={() => completeMut.mutate()}
            busy={completeMut.isPending}
            disabled={busy}
          >
            ✓ done
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
