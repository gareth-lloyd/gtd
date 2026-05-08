import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState,
  type ReactNode,
} from "react";
import { useLocation } from "react-router-dom";
import { isEditableTarget } from "./CaptureBar";

interface HoverState {
  id: string;
  top: number | null;
}

interface SelectionState {
  selectedId: string | null;
  editingId: string | null;
  hoveredId: string | null;
  hoveredCardTop: number | null;
  navigableIds: string[];
  select: (id: string | null) => void;
  edit: (id: string | null) => void;
  stopEditing: () => void;
  selectNext: () => void;
  selectPrev: () => void;
  setNavigableIds: (ids: string[]) => void;
  setHover: (id: string | null, topOffset?: number) => void;
  clearHover: () => void;
}

const SelectionCtx = createContext<SelectionState>({
  selectedId: null,
  editingId: null,
  hoveredId: null,
  hoveredCardTop: null,
  navigableIds: [],
  select: () => {},
  edit: () => {},
  stopEditing: () => {},
  selectNext: () => {},
  selectPrev: () => {},
  setNavigableIds: () => {},
  setHover: () => {},
  clearHover: () => {},
});

export function useSelection() {
  return useContext(SelectionCtx);
}

export function SelectionProvider({ children }: { children: ReactNode }) {
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [navigableIds, setNavigableIdsState] = useState<string[]>([]);
  const [hover, setHoverState] = useState<HoverState | null>(null);
  const { pathname } = useLocation();

  // Clear on navigation
  useEffect(() => {
    setSelectedId(null);
    setEditingId(null);
    setHoverState(null);
  }, [pathname]);

  const select = useCallback((id: string | null) => {
    setSelectedId((prev) => {
      const next = prev === id ? null : id;
      if (next !== prev) setEditingId(null);
      return next;
    });
  }, []);

  const edit = useCallback((id: string | null) => {
    setSelectedId(id);
    setEditingId(id);
  }, []);

  const stopEditing = useCallback(() => {
    setEditingId(null);
  }, []);

  // Read latest state via refs so the callback identities stay stable.
  const selectedIdRef = useRef(selectedId);
  selectedIdRef.current = selectedId;
  const navigableIdsRef = useRef(navigableIds);
  navigableIdsRef.current = navigableIds;

  const stepSelection = useCallback((delta: 1 | -1) => {
    const ids = navigableIdsRef.current;
    if (ids.length === 0) return;
    const current = selectedIdRef.current;
    const idx = current ? ids.indexOf(current) : -1;
    let nextIdx: number;
    if (idx === -1) {
      nextIdx = delta === 1 ? 0 : ids.length - 1;
    } else {
      nextIdx = Math.max(0, Math.min(ids.length - 1, idx + delta));
    }
    if (idx !== -1 && nextIdx === idx) return;
    setSelectedId(ids[nextIdx]);
    setEditingId(null);
  }, []);

  const selectNext = useCallback(() => stepSelection(1), [stepSelection]);
  const selectPrev = useCallback(() => stepSelection(-1), [stepSelection]);

  const setNavigableIds = useCallback((ids: string[]) => {
    setNavigableIdsState((prev) => {
      if (prev.length === ids.length && prev.every((id, i) => id === ids[i])) return prev;
      return ids;
    });
  }, []);

  // Escape ladder. Inside the active editor → stop editing in one keystroke
  // (the input unmounts with the editor, no separate blur step). Inside any
  // other input (capture bar, search) → blur but preserve selection. Outside
  // any input → stop editing if editing, else deselect.
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key !== "Escape") return;
      const active = document.activeElement;
      const inEditor = active instanceof Element && active.closest("[data-editing]");
      if (isEditableTarget(active) && !inEditor) {
        if (active instanceof HTMLElement) active.blur();
        return;
      }
      if (editingId) {
        setEditingId(null);
        return;
      }
      if (selectedId) {
        setSelectedId(null);
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [selectedId, editingId]);

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
      editingId,
      hoveredId: hover?.id ?? null,
      hoveredCardTop: hover?.top ?? null,
      navigableIds,
      select,
      edit,
      stopEditing,
      selectNext,
      selectPrev,
      setNavigableIds,
      setHover,
      clearHover,
    }),
    [
      selectedId,
      editingId,
      hover,
      navigableIds,
      select,
      edit,
      stopEditing,
      selectNext,
      selectPrev,
      setNavigableIds,
      setHover,
      clearHover,
    ],
  );

  return <SelectionCtx.Provider value={value}>{children}</SelectionCtx.Provider>;
}
