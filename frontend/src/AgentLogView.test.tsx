import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, within } from "@testing-library/react";
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

  it("shows an empty state when the item has no agent log", async () => {
    const { api } = await import("./api");
    const base = await api.getItem("work", "agent-item");
    vi.mocked(api.getItem).mockResolvedValueOnce({ ...base!, output: "" });
    renderAt("/work/items/agent-item/agent");

    const panel = await screen.findByTestId("agent-log-panel");
    expect(within(panel).getByText(/no agent log yet/i)).toBeInTheDocument();
  });
});
