import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import type { GrabBag, Item } from "./api";

vi.mock("./api", () => ({
  api: {
    listGrabBags: vi.fn(),
    createGrabBag: vi.fn(),
    grabItem: vi.fn(),
    getGrabBag: vi.fn(),
    emptyGrabBag: vi.fn(),
    listProjects: vi.fn(),
  },
}));

import { api } from "./api";
import { GrabBagDetailView, GrabBagNavLinks, GrabBagsView, GrabButton } from "./GrabBags";
import { SelectionProvider } from "./SelectionContext";

function makeItem(id: string, title: string): Item {
  return {
    id,
    title,
    body: "",
    created: "2026-10-14T09:00:00",
    updated: "2026-10-14T09:00:00",
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
    completed_at: null,
    output: "",
  };
}

function bag(id: string, name: string, overrides: Partial<GrabBag> = {}): GrabBag {
  return {
    id,
    name,
    created: "2026-10-14T09:00:00",
    updated: "2026-10-14T09:00:00",
    item_count: 1,
    ...overrides,
  };
}

const item = makeItem("item-1", "Call Bob");

function renderAt(path: string, ui: React.ReactNode, routePath = "/:env/*") {
  const qc = new QueryClient({
    defaultOptions: { queries: { retry: false }, mutations: { retry: false } },
  });
  return render(
    <QueryClientProvider client={qc}>
      <MemoryRouter initialEntries={[path]}>
        <SelectionProvider>
          <Routes>
            <Route path={routePath} element={ui} />
            <Route path="/:env/grab-bags" element={<div>bags index</div>} />
          </Routes>
        </SelectionProvider>
      </MemoryRouter>
    </QueryClientProvider>,
  );
}

beforeEach(() => {
  vi.mocked(api.listGrabBags).mockResolvedValue([bag("b1", "Offsite"), bag("b2", "Calls")]);
  vi.mocked(api.listProjects).mockResolvedValue([]);
  vi.mocked(api.grabItem).mockResolvedValue(bag("b1", "Offsite", { item_count: 2 }));
  vi.mocked(api.createGrabBag).mockResolvedValue(bag("b3", "New one"));
  vi.mocked(api.emptyGrabBag).mockResolvedValue(undefined as unknown as void);
});

afterEach(() => {
  vi.restoreAllMocks();
  vi.clearAllMocks();
});

describe("GrabButton", () => {
  it("lists existing bags and grabs into the one clicked", async () => {
    const user = userEvent.setup();
    renderAt("/work/next", <GrabButton env="work" item={item} />);
    await user.click(screen.getByRole("button", { name: /grab/i }));
    const dialog = await screen.findByRole("dialog", { name: /grab/i });
    await user.click(await screen.findByRole("button", { name: "Offsite" }));
    await waitFor(() => expect(api.grabItem).toHaveBeenCalledWith("work", "b1", "item-1"));
    await waitFor(() => expect(dialog).not.toBeInTheDocument());
  });

  it("creates a new bag by name containing the item", async () => {
    const user = userEvent.setup();
    renderAt("/work/next", <GrabButton env="work" item={item} />);
    await user.click(screen.getByRole("button", { name: /grab/i }));
    await user.type(await screen.findByPlaceholderText(/new grab bag/i), "New one{Enter}");
    await waitFor(() =>
      expect(api.createGrabBag).toHaveBeenCalledWith("work", "New one", "item-1"),
    );
  });

  it("does not create a bag with a blank name", async () => {
    const user = userEvent.setup();
    renderAt("/work/next", <GrabButton env="work" item={item} />);
    await user.click(screen.getByRole("button", { name: /grab/i }));
    await user.type(await screen.findByPlaceholderText(/new grab bag/i), "   {Enter}");
    expect(api.createGrabBag).not.toHaveBeenCalled();
  });
});

describe("GrabBagNavLinks", () => {
  it("shows at most the three most recent bags", async () => {
    vi.mocked(api.listGrabBags).mockResolvedValue([
      bag("b1", "One"),
      bag("b2", "Two"),
      bag("b3", "Three"),
      bag("b4", "Four"),
    ]);
    renderAt("/work/next", <GrabBagNavLinks env="work" />);
    expect(await screen.findByRole("link", { name: /One/ })).toHaveAttribute(
      "href",
      "/work/grab-bags/b1",
    );
    expect(screen.getByRole("link", { name: /Three/ })).toBeInTheDocument();
    expect(screen.queryByRole("link", { name: /Four/ })).not.toBeInTheDocument();
  });
});

describe("GrabBagsView", () => {
  it("lists every bag with its age and size", async () => {
    renderAt("/work/grab-bags-all", <GrabBagsView />);
    expect(await screen.findByRole("link", { name: /Offsite/ })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /Calls/ })).toBeInTheDocument();
    expect(screen.getAllByText(/1 item/)).toHaveLength(2);
  });
});

describe("GrabBagDetailView", () => {
  beforeEach(() => {
    vi.mocked(api.getGrabBag).mockResolvedValue({
      bag: bag("b1", "Offsite"),
      items: [item],
    });
  });

  it("shows the bag's name, age and items", async () => {
    renderAt("/work/grab-bags/b1", <GrabBagDetailView />, "/:env/grab-bags/:bagId");
    expect(await screen.findByRole("heading", { name: "Offsite" })).toBeInTheDocument();
    expect(screen.getByText(/created .* ago|created just now/i)).toBeInTheDocument();
    expect(screen.getByText("Call Bob")).toBeInTheDocument();
  });

  it("Empty deletes the bag after confirmation and returns to the list", async () => {
    vi.spyOn(window, "confirm").mockReturnValue(true);
    const user = userEvent.setup();
    renderAt("/work/grab-bags/b1", <GrabBagDetailView />, "/:env/grab-bags/:bagId");
    await user.click(await screen.findByRole("button", { name: /empty/i }));
    await waitFor(() => expect(api.emptyGrabBag).toHaveBeenCalledWith("work", "b1"));
    expect(await screen.findByText("bags index")).toBeInTheDocument();
  });

  it("Empty does nothing if not confirmed", async () => {
    vi.spyOn(window, "confirm").mockReturnValue(false);
    const user = userEvent.setup();
    renderAt("/work/grab-bags/b1", <GrabBagDetailView />, "/:env/grab-bags/:bagId");
    await user.click(await screen.findByRole("button", { name: /empty/i }));
    expect(api.emptyGrabBag).not.toHaveBeenCalled();
  });
});

describe("findItemInCache", () => {
  it("finds items held only in a grab bag detail cache", async () => {
    const { findItemInCache } = await import("./ItemEdit");
    const qc = new QueryClient();
    qc.setQueryData(["grab-bags", "work"], [bag("b1", "Offsite")]);
    qc.setQueryData(["grab-bags", "work", "b1"], { bag: bag("b1", "Offsite"), items: [item] });
    expect(findItemInCache(qc, "work", "item-1")).toEqual(item);
  });
});
