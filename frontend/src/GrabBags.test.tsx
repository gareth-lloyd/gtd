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
import {
  GrabBagDetailView,
  GrabBagNavLinks,
  GrabBagsNavSection,
  GrabBagsView,
  GrabRow,
  isSetAside,
  sortBagItems,
} from "./GrabBags";
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
    item_ids: [],
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
  vi.mocked(api.createGrabBag).mockResolvedValue(bag("b3", "New one", { item_count: 0 }));
  vi.mocked(api.emptyGrabBag).mockResolvedValue(undefined as unknown as void);
});

afterEach(() => {
  vi.restoreAllMocks();
  vi.clearAllMocks();
});

describe("GrabRow", () => {
  it("renders one hand button per bag and grabs directly on click", async () => {
    const user = userEvent.setup();
    renderAt("/work/next", <GrabRow env="work" item={item} />);
    await user.click(await screen.findByRole("button", { name: "✋ Offsite" }));
    await waitFor(() => expect(api.grabItem).toHaveBeenCalledWith("work", "b1", "item-1"));
    expect(screen.getByRole("button", { name: "✋ Calls" })).toBeInTheDocument();
    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
  });

  it("marks bags already holding the item as pressed and not clickable", async () => {
    vi.mocked(api.listGrabBags).mockResolvedValue([
      bag("b1", "Offsite", { item_ids: ["item-1"] }),
      bag("b2", "Calls"),
    ]);
    renderAt("/work/next", <GrabRow env="work" item={item} />);
    const held = await screen.findByRole("button", { name: "✋ Offsite" });
    expect(held).toHaveAttribute("aria-pressed", "true");
    expect(held).toBeDisabled();
    expect(screen.getByRole("button", { name: "✋ Calls" })).toBeEnabled();
  });

  it("renders nothing when there are no bags", async () => {
    vi.mocked(api.listGrabBags).mockResolvedValue([]);
    const { container } = renderAt("/work/next", <GrabRow env="work" item={item} />);
    await waitFor(() => expect(api.listGrabBags).toHaveBeenCalled());
    expect(container.querySelector(".grab-row")).toBeNull();
  });
});

describe("GrabBagsNavSection", () => {
  it("+ opens a name field that creates an empty bag", async () => {
    const user = userEvent.setup();
    renderAt("/work/next", <GrabBagsNavSection env="work" />);
    await user.click(screen.getByRole("button", { name: /new grab bag/i }));
    await user.type(screen.getByPlaceholderText(/bag name/i), "New one{Enter}");
    await waitFor(() => expect(api.createGrabBag).toHaveBeenCalledWith("work", "New one"));
    await waitFor(() => expect(screen.queryByPlaceholderText(/bag name/i)).not.toBeInTheDocument());
  });

  it("ignores a blank name and Escape closes the field", async () => {
    const user = userEvent.setup();
    renderAt("/work/next", <GrabBagsNavSection env="work" />);
    await user.click(screen.getByRole("button", { name: /new grab bag/i }));
    await user.type(screen.getByPlaceholderText(/bag name/i), "   {Enter}");
    expect(api.createGrabBag).not.toHaveBeenCalled();
    await user.keyboard("{Escape}");
    expect(screen.queryByPlaceholderText(/bag name/i)).not.toBeInTheDocument();
  });

  it("links to the all-bags view", async () => {
    renderAt("/work/next", <GrabBagsNavSection env="work" />);
    expect(screen.getByRole("link", { name: /grab bags/i })).toHaveAttribute(
      "href",
      "/work/grab-bags",
    );
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

describe("sortBagItems", () => {
  const live = makeItem("live", "Live");
  const done = {
    ...makeItem("done", "Done"),
    status: "archive" as const,
    completed_at: "2026-10-20T10:00:00",
  };
  const ref = { ...makeItem("ref", "Ref"), status: "reference" as const };
  const deferred = { ...makeItem("deferred", "Deferred"), defer_until: "2999-01-01T09:00:00" };
  const overdueDeferred = {
    ...makeItem("od", "Overdue deferred"),
    defer_until: "2999-01-01T09:00:00",
    overdue: true,
  };
  const expiredDefer = { ...makeItem("ed", "Expired defer"), defer_until: "2000-01-01T09:00:00" };

  it("flags completed, reference and future-deferred items as set aside", () => {
    expect(isSetAside(live)).toBe(false);
    expect(isSetAside(done)).toBe(true);
    expect(isSetAside(ref)).toBe(true);
    expect(isSetAside(deferred)).toBe(true);
    expect(isSetAside(overdueDeferred)).toBe(false);
    expect(isSetAside(expiredDefer)).toBe(false);
  });

  it("keeps grab order within each group and moves set-aside items last", () => {
    const sorted = sortBagItems([done, live, ref, expiredDefer, deferred]);
    expect(sorted.map((i) => i.id)).toEqual(["live", "ed", "done", "ref", "deferred"]);
  });
});

describe("GrabBagDetailView ordering", () => {
  it("renders set-aside items after live ones, greyed out", async () => {
    const done = { ...makeItem("done", "Done thing"), completed_at: "2026-10-20T10:00:00" };
    const live = makeItem("live", "Live thing");
    vi.mocked(api.getGrabBag).mockResolvedValue({
      bag: bag("b1", "Offsite", { item_count: 2 }),
      items: [done, live],
    });
    const { container } = renderAt(
      "/work/grab-bags/b1",
      <GrabBagDetailView />,
      "/:env/grab-bags/:bagId",
    );
    await screen.findByText("Live thing");
    const cards = Array.from(container.querySelectorAll(".item"));
    expect(cards.map((c) => c.getAttribute("data-item-id"))).toEqual(["live", "done"]);
    expect(cards[0]).not.toHaveClass("parked");
    expect(cards[1]).toHaveClass("parked");
    expect(screen.getByText("2 items · 1 set aside")).toBeInTheDocument();
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
