import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import type { Item } from "./api";

vi.mock("./api", () => ({
  api: {
    mergeItem: vi.fn(),
    listSearchCorpus: vi.fn(),
    listProjects: vi.fn(),
  },
}));

import { api } from "./api";
import { toasts } from "./toast";
import { MergeButton } from "./MergeButton";

function makeItem(id: string, title: string, overrides: Partial<Item> = {}): Item {
  return {
    id,
    title,
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
    completed_at: null,
    output: "",
    ...overrides,
  };
}

const current = makeItem("item-1", "Call dentist about crown");
const dup = makeItem("item-2", "Ring dentist re crown", { status: "inbox" });
const unrelated = makeItem("item-3", "Write release notes");

function renderButton(item: Item = current) {
  const qc = new QueryClient({
    defaultOptions: {
      queries: { retry: false, staleTime: Infinity },
      mutations: { retry: false },
    },
  });
  const utils = render(
    <QueryClientProvider client={qc}>
      <MergeButton env="work" item={item} />
    </QueryClientProvider>,
  );
  return { ...utils, qc };
}

beforeEach(() => {
  vi.mocked(api.listSearchCorpus).mockResolvedValue({
    items: [current, dup, unrelated],
    projects: [],
  });
  vi.mocked(api.listProjects).mockResolvedValue([]);
  vi.mocked(api.mergeItem).mockResolvedValue(undefined as unknown as void);
  vi.spyOn(window, "confirm").mockReturnValue(true);
});

afterEach(() => {
  vi.restoreAllMocks();
  vi.clearAllMocks();
});

describe("MergeButton", () => {
  it("does not load the search corpus until opened", () => {
    renderButton();
    expect(screen.getByRole("button", { name: /merge other/ })).toBeInTheDocument();
    expect(api.listSearchCorpus).not.toHaveBeenCalled();
    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
  });

  it("opens a picker that filters the corpus and excludes the current item", async () => {
    const user = userEvent.setup();
    renderButton();
    await user.click(screen.getByRole("button", { name: /merge other/ }));

    const dialog = await screen.findByRole("dialog");
    const input = within(dialog).getByRole("searchbox");
    expect(input).toHaveFocus();
    await waitFor(() => expect(api.listSearchCorpus).toHaveBeenCalledWith("work"));

    await user.type(input, "dentist");
    await within(dialog).findByText("Ring dentist re crown");
    expect(within(dialog).queryByText("Call dentist about crown")).not.toBeInTheDocument();
    expect(within(dialog).queryByText("Write release notes")).not.toBeInTheDocument();
    expect(within(dialog).getByText("inbox")).toBeInTheDocument();
  });

  it("selecting a hit confirms, launches the merge agent, toasts, and closes", async () => {
    const user = userEvent.setup();
    const show = vi.spyOn(toasts, "show");
    const { qc } = renderButton();
    const invalidate = vi.spyOn(qc, "invalidateQueries");
    await user.click(screen.getByRole("button", { name: /merge other/ }));
    const dialog = await screen.findByRole("dialog");
    await user.type(within(dialog).getByRole("searchbox"), "dentist");
    await user.click(await within(dialog).findByText("Ring dentist re crown"));

    expect(window.confirm).toHaveBeenCalledWith(expect.stringContaining("Ring dentist re crown"));
    await waitFor(() => expect(api.mergeItem).toHaveBeenCalledWith("work", "item-1", "item-2"));
    await waitFor(() => expect(screen.queryByRole("dialog")).not.toBeInTheDocument());
    expect(show).toHaveBeenCalledWith("success", expect.stringContaining("Agent launched"));
    expect(invalidate).toHaveBeenCalledWith(
      expect.objectContaining({ queryKey: ["item", "work", "item-1"] }),
    );
  });

  it("declining the confirm leaves the picker open and does not merge", async () => {
    const user = userEvent.setup();
    vi.mocked(window.confirm).mockReturnValue(false);
    renderButton();
    await user.click(screen.getByRole("button", { name: /merge other/ }));
    const dialog = await screen.findByRole("dialog");
    await user.type(within(dialog).getByRole("searchbox"), "dentist");
    await user.click(await within(dialog).findByText("Ring dentist re crown"));
    expect(api.mergeItem).not.toHaveBeenCalled();
    expect(screen.getByRole("dialog")).toBeInTheDocument();
  });

  it("Escape closes the picker", async () => {
    const user = userEvent.setup();
    renderButton();
    await user.click(screen.getByRole("button", { name: /merge other/ }));
    await screen.findByRole("dialog");
    await user.keyboard("{Escape}");
    await waitFor(() => expect(screen.queryByRole("dialog")).not.toBeInTheDocument());
  });
});
