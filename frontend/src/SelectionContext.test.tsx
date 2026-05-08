import { describe, it, expect } from "vitest";
import { render, act } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { useEffect, useRef } from "react";
import { ROUTER_FUTURE } from "./routerConfig";
import { SelectionProvider, useSelection } from "./SelectionContext";

type Snapshot = ReturnType<typeof useSelection>;

function harness() {
  const ref: { current: Snapshot | null } = { current: null };
  function Probe({ ids }: { ids: string[] }) {
    const sel = useSelection();
    ref.current = sel;
    const { setNavigableIds } = sel;
    const idsRef = useRef(ids);
    idsRef.current = ids;
    useEffect(() => {
      setNavigableIds(idsRef.current);
    }, [setNavigableIds]);
    return null;
  }
  return { ref, Probe };
}

function renderProvider(ids: string[]) {
  const { ref, Probe } = harness();
  render(
    <MemoryRouter initialEntries={["/work/next"]} future={ROUTER_FUTURE}>
      <SelectionProvider>
        <Probe ids={ids} />
      </SelectionProvider>
    </MemoryRouter>,
  );
  return ref;
}

describe("SelectionContext state machine", () => {
  it("select(id) sets selectedId and clears editingId", () => {
    const ref = renderProvider(["a", "b", "c"]);
    act(() => ref.current!.edit("a"));
    expect(ref.current!.selectedId).toBe("a");
    expect(ref.current!.editingId).toBe("a");
    act(() => ref.current!.select("b"));
    expect(ref.current!.selectedId).toBe("b");
    expect(ref.current!.editingId).toBeNull();
  });

  it("select(id) on the same id toggles selection off", () => {
    const ref = renderProvider(["a"]);
    act(() => ref.current!.select("a"));
    expect(ref.current!.selectedId).toBe("a");
    act(() => ref.current!.select("a"));
    expect(ref.current!.selectedId).toBeNull();
  });

  it("edit(id) sets both selectedId and editingId", () => {
    const ref = renderProvider(["a", "b"]);
    act(() => ref.current!.edit("a"));
    expect(ref.current!.selectedId).toBe("a");
    expect(ref.current!.editingId).toBe("a");
  });

  it("stopEditing() clears editingId and keeps selectedId", () => {
    const ref = renderProvider(["a"]);
    act(() => ref.current!.edit("a"));
    act(() => ref.current!.stopEditing());
    expect(ref.current!.selectedId).toBe("a");
    expect(ref.current!.editingId).toBeNull();
  });
});

describe("SelectionContext navigation", () => {
  it("selectNext from idle picks the first id", () => {
    const ref = renderProvider(["a", "b", "c"]);
    act(() => ref.current!.selectNext());
    expect(ref.current!.selectedId).toBe("a");
  });

  it("selectPrev from idle picks the last id", () => {
    const ref = renderProvider(["a", "b", "c"]);
    act(() => ref.current!.selectPrev());
    expect(ref.current!.selectedId).toBe("c");
  });

  it("selectNext walks forward and clamps at end", () => {
    const ref = renderProvider(["a", "b", "c"]);
    act(() => ref.current!.select("a"));
    act(() => ref.current!.selectNext());
    expect(ref.current!.selectedId).toBe("b");
    act(() => ref.current!.selectNext());
    expect(ref.current!.selectedId).toBe("c");
    act(() => ref.current!.selectNext());
    expect(ref.current!.selectedId).toBe("c");
  });

  it("selectPrev walks backward and clamps at start", () => {
    const ref = renderProvider(["a", "b", "c"]);
    act(() => ref.current!.select("c"));
    act(() => ref.current!.selectPrev());
    expect(ref.current!.selectedId).toBe("b");
    act(() => ref.current!.selectPrev());
    expect(ref.current!.selectedId).toBe("a");
    act(() => ref.current!.selectPrev());
    expect(ref.current!.selectedId).toBe("a");
  });

  it("selectNext clears editingId so navigation never drags edit mode along", () => {
    const ref = renderProvider(["a", "b"]);
    act(() => ref.current!.edit("a"));
    expect(ref.current!.editingId).toBe("a");
    act(() => ref.current!.selectNext());
    expect(ref.current!.selectedId).toBe("b");
    expect(ref.current!.editingId).toBeNull();
  });

  it("selectNext on an empty list is a no-op", () => {
    const ref = renderProvider([]);
    act(() => ref.current!.selectNext());
    expect(ref.current!.selectedId).toBeNull();
  });

  it("selectNext on a single-item list selects then no-ops", () => {
    const ref = renderProvider(["a"]);
    act(() => ref.current!.selectNext());
    expect(ref.current!.selectedId).toBe("a");
    act(() => ref.current!.selectNext());
    expect(ref.current!.selectedId).toBe("a");
  });
});

describe("SelectionContext Escape ladder", () => {
  it("Escape outside any input deselects when selected (not editing)", () => {
    const ref = renderProvider(["a"]);
    act(() => ref.current!.select("a"));
    act(() => {
      window.dispatchEvent(new KeyboardEvent("keydown", { key: "Escape" }));
    });
    expect(ref.current!.selectedId).toBeNull();
  });

  it("Escape outside any input stops editing first, leaves selection", () => {
    const ref = renderProvider(["a"]);
    act(() => ref.current!.edit("a"));
    act(() => {
      window.dispatchEvent(new KeyboardEvent("keydown", { key: "Escape" }));
    });
    expect(ref.current!.selectedId).toBe("a");
    expect(ref.current!.editingId).toBeNull();
  });

  it("Escape with focus in an input blurs the input but leaves selection", () => {
    const ref = renderProvider(["a"]);
    act(() => ref.current!.edit("a"));
    const input = document.createElement("input");
    document.body.appendChild(input);
    input.focus();
    expect(document.activeElement).toBe(input);
    try {
      act(() => {
        // KeyboardEvent listeners read document.activeElement, not target.
        window.dispatchEvent(new KeyboardEvent("keydown", { key: "Escape" }));
      });
      expect(document.activeElement).not.toBe(input);
      expect(ref.current!.selectedId).toBe("a");
      expect(ref.current!.editingId).toBe("a");
    } finally {
      input.remove();
    }
  });
});
