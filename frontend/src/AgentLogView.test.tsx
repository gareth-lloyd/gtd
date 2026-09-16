import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { MemoryRouter } from "react-router-dom";
import App from "./App";
import { ROUTER_FUTURE } from "./routerConfig";

vi.mock("./api", () => {
  const item = {
    id: "agent-item",
    title: "Investigate the flaky thing",
    body: "Some background notes.",
    created: "2026-06-24T09:00:00",
    updated: "2026-06-24T14:00:00",
    status: "next",
    contexts: ["calls"],
    energy: "low",
    time_minutes: 30,
    project: "p1",
    project_priority: 2,
    area: "engineering",
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
    output: "## Agent run 2026-06-24\n\nFound the **root cause** in the parser.",
  };
  return {
    api: {
      listEnvs: vi.fn().mockResolvedValue([{ name: "work" }]),
      getConfig: vi.fn().mockResolvedValue({
        name: "work",
        contexts: ["calls"],
        areas: ["engineering"],
        default_energy: "medium",
      }),
      listItems: vi.fn().mockResolvedValue([]),
      getItem: vi.fn().mockResolvedValue(item),
      listProjects: vi.fn().mockResolvedValue([{ id: "p1", title: "GTD", priority: 2 }]),
      snapshotStatus: vi
        .fn()
        .mockResolvedValue({ dirty_count: 0, dirty_files: [], unloadable_files: [] }),
      listSearchCorpus: vi.fn().mockResolvedValue({ items: [], projects: [] }),
      pull: vi.fn().mockResolvedValue({ pulled: false, changed: false, error: null }),
      launchAgent: vi.fn().mockResolvedValue(undefined),
    },
  };
});

function renderAt(entry: string) {
  const qc = new QueryClient({
    defaultOptions: { queries: { retry: false, staleTime: Infinity } },
  });
  return render(
    <QueryClientProvider client={qc}>
      <MemoryRouter initialEntries={[entry]} future={ROUTER_FUTURE}>
        <App />
      </MemoryRouter>
    </QueryClientProvider>,
  );
}

describe("AgentLogView", () => {
  beforeEach(() => {
    localStorage.setItem("gtd:env", "work");
    vi.clearAllMocks();
  });

  it("renders the agent log prominently with the ticket overview and metadata", async () => {
    renderAt("/work/items/agent-item/agent");

    // Agent log content is shown directly (front and centre — not collapsed)
    const panel = await screen.findByTestId("agent-log-panel");
    expect(within(panel).getByText(/root cause/)).toBeInTheDocument();

    // Ticket overview: title + key metadata chips
    expect(screen.getByText("Investigate the flaky thing")).toBeInTheDocument();
    expect(screen.getByText("📁 GTD")).toBeInTheDocument();
    expect(screen.getByText("@calls")).toBeInTheDocument();
    expect(screen.getByText("⚡low")).toBeInTheDocument();
    expect(screen.getByText("30m")).toBeInTheDocument();
  });

  it("hides the right detail panel so the log gets the full content width", async () => {
    const { container } = renderAt("/work/items/agent-item/agent");

    await screen.findByTestId("agent-log-panel");
    expect(container.querySelector(".detail-panel")).toBeNull();
  });

  it("keeps the detail panel on other routes", async () => {
    const { container } = renderAt("/work/next");

    await screen.findByText("inbox");
    expect(container.querySelector(".detail-panel")).not.toBeNull();
  });

  it("shows an empty state when the item has no agent log", async () => {
    const { api } = await import("./api");
    const base = await api.getItem("work", "agent-item");
    vi.mocked(api.getItem).mockResolvedValueOnce({ ...base!, output: "" });
    renderAt("/work/items/agent-item/agent");

    const panel = await screen.findByTestId("agent-log-panel");
    expect(within(panel).getByText(/no agent log yet/i)).toBeInTheDocument();
  });

  describe("Next agent work", () => {
    it("renders the follow-up box above the log, with launch disabled while empty", async () => {
      renderAt("/work/items/agent-item/agent");

      const box = await screen.findByTestId("next-agent-work");
      const panel = screen.getByTestId("agent-log-panel");
      // The box sits at the top of the full view — before the log itself.
      expect(box.compareDocumentPosition(panel) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
      expect(within(box).getByRole("textbox", { name: /next agent work/i })).toHaveValue("");
      expect(within(box).getByRole("button", { name: /🤖 agent/ })).toBeDisabled();
      expect(within(box).getByRole("button", { name: /desktop agent/ })).toBeDisabled();
    });

    it("launches an iTerm session carrying the typed follow-up, then clears the box", async () => {
      const { api } = await import("./api");
      const user = userEvent.setup();
      renderAt("/work/items/agent-item/agent");

      const box = await screen.findByTestId("next-agent-work");
      const input = within(box).getByRole("textbox", { name: /next agent work/i });
      await user.type(input, "Now fix the parser bug you found");
      await user.click(within(box).getByRole("button", { name: /🤖 agent/ }));

      await waitFor(() =>
        expect(api.launchAgent).toHaveBeenCalledWith(
          "work",
          "agent-item",
          "iterm",
          "Now fix the parser bug you found",
        ),
      );
      await waitFor(() => expect(input).toHaveValue(""));
    });

    it("launches a desktop session with the desktop target", async () => {
      const { api } = await import("./api");
      const user = userEvent.setup();
      renderAt("/work/items/agent-item/agent");

      const box = await screen.findByTestId("next-agent-work");
      await user.type(within(box).getByRole("textbox", { name: /next agent work/i }), "Verify");
      await user.click(within(box).getByRole("button", { name: /desktop agent/ }));

      await waitFor(() =>
        expect(api.launchAgent).toHaveBeenCalledWith("work", "agent-item", "desktop", "Verify"),
      );
    });

    it("does not launch on whitespace-only input", async () => {
      const { api } = await import("./api");
      const user = userEvent.setup();
      renderAt("/work/items/agent-item/agent");

      const box = await screen.findByTestId("next-agent-work");
      await user.type(within(box).getByRole("textbox", { name: /next agent work/i }), "   ");
      expect(within(box).getByRole("button", { name: /🤖 agent/ })).toBeDisabled();
      expect(api.launchAgent).not.toHaveBeenCalled();
    });
  });
});
