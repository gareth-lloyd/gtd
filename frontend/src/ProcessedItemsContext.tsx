import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import { useLocation } from "react-router-dom";

type Ctx = {
  isProcessed: (id: string) => boolean;
  markProcessed: (id: string) => void;
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
  const [processedIds, setProcessedIds] = useState<Set<string>>(new Set());

  // Reset the processed set whenever we leave the inbox route OR switch envs
  // (e.g. /work/inbox -> /home/inbox), so stale IDs can't grey out an
  // unrelated item with a coincidentally-matching id in the new view.
  useEffect(() => {
    setProcessedIds(new Set());
  }, [env, active]);

  const markProcessed = useCallback((id: string) => {
    setProcessedIds((prev) => {
      if (prev.has(id)) return prev;
      const next = new Set(prev);
      next.add(id);
      return next;
    });
  }, []);

  const value = useMemo<Ctx>(
    () => ({
      isProcessed: (id: string) => processedIds.has(id),
      markProcessed,
      processedCount: processedIds.size,
      active,
    }),
    [processedIds, markProcessed, active],
  );

  return <ProcessedItemsContext.Provider value={value}>{children}</ProcessedItemsContext.Provider>;
}

export function useProcessedItems(): Ctx | null {
  return useContext(ProcessedItemsContext);
}
