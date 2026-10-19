import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import { useLocation } from "react-router-dom";
import type { Bucket } from "./api";

type Ctx = {
  isProcessed: (id: string) => boolean;
  // `outcome` is the bucket the item was moved to (when known), so a row
  // that was marked done can offer an "uncomplete" back into the inbox.
  markProcessed: (id: string, outcome?: Bucket) => void;
  unmarkProcessed: (id: string) => void;
  processedOutcome: (id: string) => Bucket | undefined;
  // Number of items processed in this session — used by the sidebar count
  // to stay consistent with the visibly-greyed rows.
  processedCount: number;
  // Whether the current route is the inbox view. Consumers (WorkflowActions,
  // useItemPatch) use this to decide whether to grey-out / preserve the
  // inbox cache instead of invalidating it.
  active: boolean;
};

const ProcessedItemsContext = createContext<Ctx | null>(null);

// Returns [env, isInbox] for paths shaped like /:env/inbox(/...|?...).
// Returns [null, false] otherwise.
function parseInboxPath(pathname: string): [string | null, boolean] {
  const parts = pathname.split("/").filter(Boolean);
  if (parts.length < 2 || parts[1] !== "inbox") return [null, false];
  return [parts[0], true];
}

export function ProcessedItemsProvider({ children }: { children: React.ReactNode }) {
  const { pathname } = useLocation();
  const [env, active] = parseInboxPath(pathname);
  const [processedIds, setProcessedIds] = useState<Map<string, Bucket | undefined>>(new Map());

  // Reset the processed set whenever we leave the inbox route OR switch envs
  // (e.g. /work/inbox -> /home/inbox), so stale IDs can't grey out an
  // unrelated item with a coincidentally-matching id in the new view.
  useEffect(() => {
    setProcessedIds(new Map());
  }, [env, active]);

  const markProcessed = useCallback((id: string, outcome?: Bucket) => {
    setProcessedIds((prev) => {
      if (prev.has(id) && prev.get(id) === outcome) return prev;
      const next = new Map(prev);
      next.set(id, outcome);
      return next;
    });
  }, []);

  const unmarkProcessed = useCallback((id: string) => {
    setProcessedIds((prev) => {
      if (!prev.has(id)) return prev;
      const next = new Map(prev);
      next.delete(id);
      return next;
    });
  }, []);

  const value = useMemo<Ctx>(
    () => ({
      isProcessed: (id: string) => processedIds.has(id),
      markProcessed,
      unmarkProcessed,
      processedOutcome: (id: string) => processedIds.get(id),
      processedCount: processedIds.size,
      active,
    }),
    [processedIds, markProcessed, unmarkProcessed, active],
  );

  return <ProcessedItemsContext.Provider value={value}>{children}</ProcessedItemsContext.Provider>;
}

export function useProcessedItems(): Ctx | null {
  return useContext(ProcessedItemsContext);
}
