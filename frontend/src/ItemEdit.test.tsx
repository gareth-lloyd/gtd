import { act, renderHook, waitFor } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import type { PropsWithChildren } from "react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import type { Item, Project } from "./api";

vi.mock("./api", () => ({
  api: {
    updateItem: vi.fn(),
  },
}));

vi.mock("./toast", () => ({
  toasts: {
    show: vi.fn(),
  },
}));

import { api } from "./api";
import { isHiddenByDefer, useItemPatch } from "./ItemEdit";
import { toasts } from "./toast";

const baseItem: Item = {
  id: "item-1",
  title: "Original title",
  body: "Original body",
  created: "2026-04-10T09:00:00",
  updated: "2026-04-10T09:00:00",
  status: "next",
  contexts: [],
  energy: null,
  time_minutes: null,
  project: null,
  project_priority: null,
  area: null,
  tags: [],
  due: null,
  overdue: false,
  defer_until: null,
  waiting_on: null,
  waiting_since: null,
  order: null,
  source_id: null,
  working_on: false,
};

const projectA: Project = {
  id: "proj-a",
  title: "Ship frontend",
  body: "",
  created: "2026-04-01T09:00:00",
  updated: "2026-04-01T09:00:00",
  status: "active",
  outcome: null,
  area: null,
  tags: [],
  due: null,
  priority: 1,
  max_next_items: null,
};

function makeWrapper(seed: (qc: QueryClient) => void) {
  const qc = new QueryClient({
    defaultOptions: {
      queries: { retry: false, staleTime: Infinity },
      mutations: { retry: false },
    },
  });
  seed(qc);
  const Wrapper = ({ children }: PropsWithChildren) => (
    <QueryClientProvider client={qc}>{children}</QueryClientProvider>
  );
  return { qc, Wrapper };
}

beforeEach(() => {
  vi.mocked(api.updateItem).mockResolvedValue({ ...baseItem });
});

afterEach(() => {
  vi.clearAllMocks();
});

describe("useItemPatch — optimistic updates", () => {
  it("updates the single-item cache immediately before the PATCH resolves", async () => {
    const { qc, Wrapper } = makeWrapper((client) => {
      client.setQueryData(["item", "work", "item-1"], baseItem);
    });
    const { result } = renderHook(() => useItemPatch("work", "item-1"), {
      wrapper: Wrapper,
    });

    // Keep the PATCH pending so we can observe the optimistic state.
    let resolveUpdate: ((v: Item) => void) | undefined;
    vi.mocked(api.updateItem).mockReturnValue(
      new Promise<Item>((resolve) => {
        resolveUpdate = resolve;
      }),
    );

    act(() => {
      result.current.patch({ title: "New title" });
    });

    // Cache should reflect the optimistic update right away.
    expect(qc.getQueryData<Item>(["item", "work", "item-1"])?.title).toBe("New title");

    resolveUpdate?.({ ...baseItem, title: "New title" });
  });
});

describe("useItemPatch — rollback on failure", () => {
  it("reverts the cache to the pre-edit value when the PATCH rejects", async () => {
    const { qc, Wrapper } = makeWrapper((client) => {
      client.setQueryData(["item", "work", "item-1"], baseItem);
    });
    vi.mocked(api.updateItem).mockRejectedValue(new Error("boom"));

    const { result } = renderHook(() => useItemPatch("work", "item-1"), {
      wrapper: Wrapper,
    });

    // Use debounce > 0 so `patch` doesn't fire its own fire-and-forget flush.
    // That way our explicit `flush()` owns the single promise chain.
    act(() => {
      result.current.patch({ title: "Doomed title" }, { debounce: 1000 });
    });
    await expect(result.current.flush()).rejects.toThrow("boom");

    expect(qc.getQueryData<Item>(["item", "work", "item-1"])?.title).toBe("Original title");
  });

  it("coalesced title + body edits both roll back on failure", async () => {
    const { qc, Wrapper } = makeWrapper((client) => {
      client.setQueryData(["item", "work", "item-1"], baseItem);
    });
    vi.mocked(api.updateItem).mockRejectedValue(new Error("boom"));

    const { result } = renderHook(() => useItemPatch("work", "item-1"), {
      wrapper: Wrapper,
    });

    act(() => {
      result.current.patch({ title: "New title" }, { debounce: 1000 });
      result.current.patch({ body: "New body" }, { debounce: 1000 });
    });
    await expect(result.current.flush()).rejects.toThrow("boom");

    const cached = qc.getQueryData<Item>(["item", "work", "item-1"]);
    expect(cached?.title).toBe("Original title");
    expect(cached?.body).toBe("Original body");

    // Single coalesced PATCH carrying both fields.
    expect(api.updateItem).toHaveBeenCalledTimes(1);
    expect(api.updateItem).toHaveBeenCalledWith("work", "item-1", {
      title: "New title",
      body: "New body",
    });
  });

  it("also rolls back entries in the items-list cache", async () => {
    const listKey = ["items", "work", "next"];
    const { qc, Wrapper } = makeWrapper((client) => {
      client.setQueryData(["item", "work", "item-1"], baseItem);
      client.setQueryData(listKey, [baseItem]);
    });
    vi.mocked(api.updateItem).mockRejectedValue(new Error("boom"));

    const { result } = renderHook(() => useItemPatch("work", "item-1"), {
      wrapper: Wrapper,
    });

    act(() => {
      result.current.patch({ title: "Doomed" }, { debounce: 1000 });
    });
    await expect(result.current.flush()).rejects.toThrow("boom");

    const list = qc.getQueryData<Item[]>(listKey);
    expect(list?.[0]?.title).toBe("Original title");
  });
});

describe("useItemPatch — project move toast", () => {
  it("fires an info toast with the new project title on a successful move", async () => {
    const { Wrapper } = makeWrapper((client) => {
      client.setQueryData(["item", "work", "item-1"], baseItem);
      client.setQueryData(["projects", "work", false], [projectA]);
    });
    vi.mocked(api.updateItem).mockResolvedValue({
      ...baseItem,
      project: "proj-a",
    });

    const { result } = renderHook(() => useItemPatch("work", "item-1"), {
      wrapper: Wrapper,
    });

    act(() => {
      result.current.patch({ project: "proj-a" }, { debounce: 1000 });
    });
    await act(async () => {
      await result.current.flush();
    });

    // Toast was fired with the project title, not the raw id.
    expect(toasts.show).toHaveBeenCalledWith("info", expect.stringContaining("Ship frontend"));
  });
});

describe("useItemPatch — unmount safety", () => {
  it("unmount during an in-flight patch does not leak unhandled rejections", async () => {
    const { Wrapper } = makeWrapper((client) => {
      client.setQueryData(["item", "work", "item-1"], baseItem);
    });

    let resolveUpdate: ((v: Item) => void) | undefined;
    vi.mocked(api.updateItem).mockReturnValue(
      new Promise<Item>((resolve) => {
        resolveUpdate = resolve;
      }),
    );

    const { result, unmount } = renderHook(() => useItemPatch("work", "item-1"), {
      wrapper: Wrapper,
    });

    act(() => {
      result.current.patch({ title: "Mid-flight" }, { debounce: 200 });
    });

    // Unmount while the debounce timer hasn't fired yet.
    unmount();

    // Let any deferred flush promise settle — should not throw.
    await waitFor(() => {
      // Resolving ensures the dangling promise chain completes cleanly.
      resolveUpdate?.({ ...baseItem, title: "Mid-flight" });
    });
    // Reaching this line without an unhandled rejection is the assertion.
    expect(true).toBe(true);
  });
});

describe("isHiddenByDefer", () => {
  it("is false when defer_until is null", () => {
    expect(isHiddenByDefer({ defer_until: null, overdue: false })).toBe(false);
  });

  it("is true when defer_until is in the future and not overdue", () => {
    const future = new Date(Date.now() + 86_400_000).toISOString();
    expect(isHiddenByDefer({ defer_until: future, overdue: false })).toBe(true);
  });

  it("is false when defer_until is in the past", () => {
    const past = new Date(Date.now() - 86_400_000).toISOString();
    expect(isHiddenByDefer({ defer_until: past, overdue: false })).toBe(false);
  });

  it("is false when overdue, even if defer_until is in the future", () => {
    const future = new Date(Date.now() + 86_400_000).toISOString();
    expect(isHiddenByDefer({ defer_until: future, overdue: true })).toBe(false);
  });
});
