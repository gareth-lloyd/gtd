import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { MemoryRouter } from "react-router-dom";
import type { Item } from "./api";
import { ROUTER_FUTURE } from "./routerConfig";

vi.mock("./api", () => ({
  api: {
    moveItem: vi.fn(),
    completeItem: vi.fn(),
    deleteItem: vi.fn(),
    purgeItem: vi.fn(),
    launchAgent: vi.fn(),
  },
}));

import { api } from "./api";
import { SelectionProvider } from "./SelectionContext";
import { WorkflowActions } from "./WorkflowActions";
import { ProcessedItemsProvider, useProcessedItems } from "./ProcessedItemsContext";

const nextItem: Item = {
  id: "item-1",
  title: "Write release notes",
  body: "",
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
  output: "",
};

function renderActions(item: Item) {
  const qc = new QueryClient({
    defaultOptions: {
      queries: { retry: false, staleTime: Infinity },
      mutations: { retry: false },
    },
  });
  const utils = render(
    <QueryClientProvider client={qc}>
      <MemoryRouter initialEntries={["/work/next"]} future={ROUTER_FUTURE}>
        <SelectionProvider>
          <WorkflowActions env="work" item={item} />
        </SelectionProvider>
      </MemoryRouter>
    </QueryClientProvider>,
  );
  return { ...utils, qc };
}

beforeEach(() => {
  vi.mocked(api.moveItem).mockResolvedValue({ ...nextItem });
  vi.mocked(api.completeItem).mockResolvedValue({ ...nextItem, status: "archive" });
  vi.mocked(api.deleteItem).mockResolvedValue({ ...nextItem, status: "trash" });
  vi.mocked(api.purgeItem).mockResolvedValue(undefined as unknown as void);
  vi.mocked(api.launchAgent).mockResolvedValue(undefined as unknown as void);
});

afterEach(() => {
  vi.clearAllMocks();
});

describe("WorkflowActions — next bucket", () => {
  it("renders move buttons for waiting and someday, and the current bucket as a selected (non-move) chip", () => {
    renderActions(nextItem);
    expect(screen.getByRole("button", { name: /→ waiting/ })).toBeDefined();
    expect(screen.getByRole("button", { name: /→ someday/ })).toBeDefined();
    // Current bucket is next — shown as a selected, non-actionable button
    // (no arrow prefix, since it's the current state, not a move target).
    expect(screen.queryByRole("button", { name: /→ next$/ })).toBeNull();
    const current = screen.getByRole("button", { name: /^next$/ });
    expect(current).toHaveAttribute("aria-pressed", "true");
    expect(current).toHaveProperty("disabled", true);
  });

  it("clicking the selected current-bucket button does not call moveItem", async () => {
    const user = userEvent.setup();
    renderActions(nextItem);
    await user.click(screen.getByRole("button", { name: /^next$/ }));
    await new Promise((resolve) => setTimeout(resolve, 0));
    expect(api.moveItem).not.toHaveBeenCalled();
  });

  it('clicking "→ waiting" calls moveItem with waiting', async () => {
    const user = userEvent.setup();
    renderActions(nextItem);
    await user.click(screen.getByRole("button", { name: /→ waiting/ }));
    await waitFor(() => {
      expect(api.moveItem).toHaveBeenCalledWith("work", "item-1", "waiting");
    });
  });

  it('clicking "→ someday" calls moveItem with someday', async () => {
    const user = userEvent.setup();
    renderActions(nextItem);
    await user.click(screen.getByRole("button", { name: /→ someday/ }));
    await waitFor(() => {
      expect(api.moveItem).toHaveBeenCalledWith("work", "item-1", "someday");
    });
  });

  it('clicking "→ reference" calls moveItem with reference', async () => {
    const user = userEvent.setup();
    renderActions(nextItem);
    await user.click(screen.getByRole("button", { name: /→ reference/ }));
    await waitFor(() => {
      expect(api.moveItem).toHaveBeenCalledWith("work", "item-1", "reference");
    });
  });

  it('clicking "✓ done" calls completeItem', async () => {
    const user = userEvent.setup();
    renderActions(nextItem);
    await user.click(screen.getByRole("button", { name: /✓ done/ }));
    await waitFor(() => {
      expect(api.completeItem).toHaveBeenCalledWith("work", "item-1");
    });
  });

  it('clicking "🤖 agent" calls launchAgent with the iterm target', async () => {
    const user = userEvent.setup();
    renderActions(nextItem);
    await user.click(screen.getByRole("button", { name: /🤖 agent/ }));
    await waitFor(() => {
      expect(api.launchAgent).toHaveBeenCalledWith("work", "item-1", "iterm");
    });
  });

  it('clicking "🖥️ desktop agent" calls launchAgent with the desktop target', async () => {
    const user = userEvent.setup();
    renderActions(nextItem);
    await user.click(screen.getByRole("button", { name: /desktop agent/ }));
    await waitFor(() => {
      expect(api.launchAgent).toHaveBeenCalledWith("work", "item-1", "desktop");
    });
  });

  it('clicking "Delete" soft-deletes (deleteItem)', async () => {
    const user = userEvent.setup();
    renderActions(nextItem);
    await user.click(screen.getByRole("button", { name: /^Delete$/ }));
    await waitFor(() => {
      expect(api.deleteItem).toHaveBeenCalledWith("work", "item-1");
    });
    // Soft-delete should NOT call purge.
    expect(api.purgeItem).not.toHaveBeenCalled();
  });
});

describe("WorkflowActions — inbox bucket", () => {
  it("offers next/waiting/someday as move options", () => {
    renderActions({ ...nextItem, status: "inbox" });
    expect(screen.getByRole("button", { name: /→ next/ })).toBeDefined();
    expect(screen.getByRole("button", { name: /→ waiting/ })).toBeDefined();
    expect(screen.getByRole("button", { name: /→ someday/ })).toBeDefined();
  });

  it("marks the item processed (instead of fully invalidating) when moved inside an inbox-processing context", async () => {
    const user = userEvent.setup();
    const inboxItem = { ...nextItem, status: "inbox" as const };
    const qc = new QueryClient({
      defaultOptions: {
        queries: { retry: false, staleTime: Infinity },
        mutations: { retry: false },
      },
    });
    // Seed the inbox list cache so we can verify it is NOT cleared.
    qc.setQueryData(["items", "work", "inbox", false], [inboxItem]);

    let captured: ReturnType<typeof useProcessedItems> = null;
    function CaptureCtx() {
      captured = useProcessedItems();
      return null;
    }

    render(
      <QueryClientProvider client={qc}>
        <MemoryRouter initialEntries={["/work/inbox"]} future={ROUTER_FUTURE}>
          <SelectionProvider>
            <ProcessedItemsProvider>
              <CaptureCtx />
              <WorkflowActions env="work" item={inboxItem} />
            </ProcessedItemsProvider>
          </SelectionProvider>
        </MemoryRouter>
      </QueryClientProvider>,
    );

    await user.click(screen.getByRole("button", { name: /→ next/ }));

    await waitFor(() => {
      expect(captured?.isProcessed("item-1")).toBe(true);
    });
    // Inbox list cache should still contain the item — the list is preserved
    // so the row can render greyed out instead of disappearing.
    const cached = qc.getQueryData<Item[]>(["items", "work", "inbox", false]);
    expect(cached?.map((i) => i.id)).toContain("item-1");
  });
});

describe("WorkflowActions — archive bucket", () => {
  it("hides bucket-move and complete buttons but offers filing to reference (item is already done)", () => {
    renderActions({ ...nextItem, status: "archive" });
    // No re-bucketing to next/waiting/someday, and no re-completing.
    expect(screen.queryByRole("button", { name: /→ waiting/ })).toBeNull();
    expect(screen.queryByRole("button", { name: /→ someday/ })).toBeNull();
    expect(screen.queryByRole("button", { name: /✓ done/ })).toBeNull();
    // A completed item can still be filed as reference or uncompleted.
    expect(screen.getByRole("button", { name: /→ reference/ })).toBeDefined();
    expect(screen.getByRole("button", { name: /↺ uncomplete/ })).toBeDefined();
    // Still offers soft delete.
    expect(screen.getByRole("button", { name: /^Delete$/ })).toBeDefined();
  });

  it('clicking "→ reference" on a completed item calls moveItem with reference', async () => {
    const user = userEvent.setup();
    renderActions({ ...nextItem, status: "archive" });
    await user.click(screen.getByRole("button", { name: /→ reference/ }));
    await waitFor(() => {
      expect(api.moveItem).toHaveBeenCalledWith("work", "item-1", "reference");
    });
  });
});

describe("WorkflowActions — trash bucket", () => {
  it("shows restore and purge (not the normal actions)", () => {
    renderActions({ ...nextItem, status: "trash" });
    expect(screen.getByRole("button", { name: /↺ restore/ })).toBeDefined();
    expect(screen.getByRole("button", { name: /Purge/ })).toBeDefined();
    expect(screen.queryByRole("button", { name: /→ waiting/ })).toBeNull();
    expect(screen.queryByRole("button", { name: /✓ done/ })).toBeNull();
  });

  it("restore calls moveItem with inbox", async () => {
    const user = userEvent.setup();
    renderActions({ ...nextItem, status: "trash" });
    await user.click(screen.getByRole("button", { name: /↺ restore/ }));
    await waitFor(() => {
      expect(api.moveItem).toHaveBeenCalledWith("work", "item-1", "inbox");
    });
  });

  it("purge calls purgeItem after confirm", async () => {
    const user = userEvent.setup();
    const confirmSpy = vi.spyOn(window, "confirm").mockReturnValue(true);
    renderActions({ ...nextItem, status: "trash" });
    await user.click(screen.getByRole("button", { name: /Purge/ }));
    await waitFor(() => {
      expect(api.purgeItem).toHaveBeenCalledWith("work", "item-1");
    });
    confirmSpy.mockRestore();
  });

  it("purge does nothing when the user cancels the confirm prompt", async () => {
    const user = userEvent.setup();
    const confirmSpy = vi.spyOn(window, "confirm").mockReturnValue(false);
    renderActions({ ...nextItem, status: "trash" });
    await user.click(screen.getByRole("button", { name: /Purge/ }));
    // Give any pending promise queues a tick to drain before asserting.
    await new Promise((resolve) => setTimeout(resolve, 0));
    expect(api.purgeItem).not.toHaveBeenCalled();
    confirmSpy.mockRestore();
  });
});

describe("WorkflowActions — busy state disables siblings", () => {
  it("disables all buttons while a mutation is pending", async () => {
    const user = userEvent.setup();
    // Never-resolving promise keeps the mutation in the pending state.
    let resolveMove: ((v: Item) => void) | undefined;
    vi.mocked(api.moveItem).mockReturnValue(
      new Promise<Item>((resolve) => {
        resolveMove = resolve;
      }),
    );
    renderActions(nextItem);
    await user.click(screen.getByRole("button", { name: /→ waiting/ }));

    // All buttons should be disabled while pending.
    await waitFor(() => {
      const deleteBtn = screen.getByRole("button", { name: /^Delete$/ });
      expect(deleteBtn).toHaveProperty("disabled", true);
    });
    const somedayBtn = screen.getByRole("button", { name: /→ someday/ });
    expect(somedayBtn).toHaveProperty("disabled", true);
    const doneBtn = screen.getByRole("button", { name: /✓ done/ });
    expect(doneBtn).toHaveProperty("disabled", true);

    // Resolve the pending promise so we don't leak.
    resolveMove?.({ ...nextItem });
  });
});
