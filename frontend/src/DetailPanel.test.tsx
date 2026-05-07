import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { MemoryRouter } from "react-router-dom";
import type { Item } from "./api";

vi.mock("./api", () => ({
  api: {
    getConfig: vi.fn().mockResolvedValue({
      name: "work",
      contexts: ["calls", "computer"],
      areas: ["engineering"],
      default_energy: "medium",
    }),
    getItem: vi.fn(),
    listProjects: vi.fn().mockResolvedValue([]),
    updateItem: vi.fn(),
    moveItem: vi.fn(),
    completeItem: vi.fn(),
    deleteItem: vi.fn(),
    purgeItem: vi.fn(),
  },
}));

import { api } from "./api";
import { DetailPanel } from "./DetailPanel";
import { SelectionProvider, useSelection } from "./SelectionContext";

const testItem: Item = {
  id: "item-1",
  title: "Test item",
  body: "",
  created: "2026-04-10T09:00:00",
  updated: "2026-04-10T09:00:00",
  status: "next",
  contexts: ["calls"],
  energy: "low",
  time_minutes: 15,
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

// Helper to select an item from outside DetailPanel
function SelectTrigger({ itemId }: { itemId: string }) {
  const { select } = useSelection();
  return (
    <button onClick={() => select(itemId)} data-testid="select-trigger">
      Select
    </button>
  );
}

function HoverTrigger({ itemId }: { itemId: string }) {
  const { setHover } = useSelection();
  return (
    <button onClick={() => setHover(itemId, 100)} data-testid="hover-trigger">
      Hover
    </button>
  );
}

function renderPanel(options: { withSelect?: string; withHover?: string } = {}) {
  const qc = new QueryClient({
    defaultOptions: { queries: { retry: false, staleTime: Infinity } },
  });
  // Seed the items list cache so findItemInCache can find items without a fetch
  qc.setQueryData(["items", "work", "next", [], "", "", false], [testItem]);
  const utils = render(
    <QueryClientProvider client={qc}>
      <MemoryRouter initialEntries={["/work/next"]}>
        <SelectionProvider>
          {options.withSelect && <SelectTrigger itemId={options.withSelect} />}
          {options.withHover && <HoverTrigger itemId={options.withHover} />}
          <DetailPanel env="work" />
        </SelectionProvider>
      </MemoryRouter>
    </QueryClientProvider>,
  );
  return { ...utils, qc };
}

beforeEach(() => {
  vi.mocked(api.getItem).mockResolvedValue(testItem);
  vi.mocked(api.updateItem).mockResolvedValue({ ...testItem });
});

afterEach(() => {
  vi.clearAllMocks();
});

describe("DetailPanel", () => {
  it("renders empty state when nothing is selected or hovered", () => {
    renderPanel();
    expect(screen.getByText("Select an item to edit")).toBeDefined();
  });

  it("shows metadata editors when an item is selected", async () => {
    const user = userEvent.setup();
    renderPanel({ withSelect: "item-1" });

    await user.click(screen.getByTestId("select-trigger"));

    // Wait for the item data to load and metadata sections to render
    await waitFor(() => {
      expect(screen.getByText("Project")).toBeDefined();
    });
    expect(screen.getByText("Contexts")).toBeDefined();
    expect(screen.getByText("Energy")).toBeDefined();
    expect(screen.getByText("Time")).toBeDefined();
    expect(screen.getByText("Area")).toBeDefined();
    expect(screen.getByText("Due")).toBeDefined();
    expect(screen.getByText("Defer until")).toBeDefined();
    expect(screen.getByText("Actions")).toBeDefined();
  });

  it("shows workflow actions when hovering", async () => {
    const user = userEvent.setup();
    renderPanel({ withHover: "item-1" });

    await user.click(screen.getByTestId("hover-trigger"));

    // Hover state shows workflow action buttons
    await waitFor(() => {
      expect(screen.getByText(/→ waiting/)).toBeDefined();
    });
    expect(screen.getByText(/→ someday/)).toBeDefined();
    expect(screen.getByText(/✓ done/)).toBeDefined();
  });

  it("selected state takes priority over hover", async () => {
    const user = userEvent.setup();
    renderPanel({ withSelect: "item-1", withHover: "item-1" });

    // First select
    await user.click(screen.getByTestId("select-trigger"));

    await waitFor(() => {
      expect(screen.getByText("Project")).toBeDefined();
    });

    // Try to hover — should be ignored since selectedId is set
    await user.click(screen.getByTestId("hover-trigger"));

    // Should still show metadata editors, not hover actions
    expect(screen.getByText("Project")).toBeDefined();
    expect(screen.getByText("Contexts")).toBeDefined();
  });

  it("renders the agent log header, collapsed, when item.output is non-empty", async () => {
    const user = userEvent.setup();
    const itemWithOutput: Item = {
      ...testItem,
      output: "## Agent run 2026-05-06\n\nReviewed PR. LGTM.",
    };
    vi.mocked(api.getItem).mockResolvedValue(itemWithOutput);

    const qc = new QueryClient({
      defaultOptions: { queries: { retry: false, staleTime: Infinity } },
    });
    qc.setQueryData(["items", "work", "next", [], "", "", false], [itemWithOutput]);
    render(
      <QueryClientProvider client={qc}>
        <MemoryRouter initialEntries={["/work/next"]}>
          <SelectionProvider>
            <SelectTrigger itemId="item-1" />
            <DetailPanel env="work" />
          </SelectionProvider>
        </MemoryRouter>
      </QueryClientProvider>,
    );
    await user.click(screen.getByTestId("select-trigger"));

    const header = await screen.findByRole("button", { name: /Agent log/ });
    expect(header).toBeDefined();
    expect(header.getAttribute("aria-expanded")).toBe("false");
    // Collapsed: body markdown should not render
    expect(screen.queryByText(/Reviewed PR/)).toBeNull();

    await user.click(header);
    expect(header.getAttribute("aria-expanded")).toBe("true");
    expect(await screen.findByText(/Reviewed PR/)).toBeDefined();
  });

  it("does not render the agent log section when item.output is empty", async () => {
    const user = userEvent.setup();
    renderPanel({ withSelect: "item-1" });
    await user.click(screen.getByTestId("select-trigger"));

    await waitFor(() => {
      expect(screen.getByText("Project")).toBeDefined();
    });
    expect(screen.queryByRole("button", { name: /Agent log/ })).toBeNull();
  });

  it("clicking a context chip triggers a PATCH", async () => {
    const user = userEvent.setup();
    renderPanel({ withSelect: "item-1" });

    await user.click(screen.getByTestId("select-trigger"));

    const computer = await screen.findByRole("button", { name: "@computer" });
    await user.click(computer);

    expect(api.updateItem).toHaveBeenCalledWith("work", "item-1", {
      contexts: ["calls", "computer"],
    });
  });
});
