import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import { useLocation } from "react-router-dom";

interface HoverState {
  id: string;
  top: number | null;
}

interface SelectionState {
  selectedId: string | null;
  hoveredId: string | null;
  hoveredCardTop: number | null;
  select: (id: string | null) => void;
  setHover: (id: string | null, topOffset?: number) => void;
  clearHover: () => void;
}

const SelectionCtx = createContext<SelectionState>({
  selectedId: null,
  hoveredId: null,
  hoveredCardTop: null,
  select: () => {},
  setHover: () => {},
  clearHover: () => {},
});

export function useSelection() {
  return useContext(SelectionCtx);
}

export function SelectionProvider({ children }: { children: ReactNode }) {
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [hover, setHoverState] = useState<HoverState | null>(null);
  const { pathname } = useLocation();

  // Clear on navigation
  useEffect(() => {
    setSelectedId(null);
    setHoverState(null);
  }, [pathname]);

  // Escape to deselect
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key !== "Escape") return;
      if (!selectedId) return;
      const active = document.activeElement;
      if (active) {
        const inCapture = active.closest(".capture");
        const inSearch = active.closest(".search-bar");
        if (inCapture || inSearch) return;
      }
      setSelectedId(null);
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [selectedId]);

  const select = useCallback((id: string | null) => {
    setSelectedId((prev) => (prev === id ? null : id));
  }, []);

  const setHover = useCallback(
    (id: string | null, topOffset?: number) => {
      if (selectedId) return;
      setHoverState(id ? { id, top: topOffset ?? null } : null);
    },
    [selectedId],
  );

  const clearHover = useCallback(() => {
    setHoverState(null);
  }, []);

  const value = useMemo(
    () => ({
      selectedId,
      hoveredId: hover?.id ?? null,
      hoveredCardTop: hover?.top ?? null,
      select,
      setHover,
      clearHover,
    }),
    [selectedId, hover, select, setHover, clearHover],
  );

  return <SelectionCtx.Provider value={value}>{children}</SelectionCtx.Provider>;
}
