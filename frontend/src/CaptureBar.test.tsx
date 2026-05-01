import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import type { Item } from "./api";

vi.mock("./api", () => ({
  api: {
    captureItem: vi.fn(),
    captureItemAi: vi.fn(),
    listProjects: vi.fn().mockResolvedValue([]),
    updateItem: vi.fn(),
    moveItem: vi.fn(),
  },
}));

import { api } from "./api";
import { CaptureBar, type CaptureMode } from "./CaptureBar";

const baseItem: Item = {
  id: "item-1",
  title: "New thing",
  body: "",
  created: "2026-04-29T12:00:00",
  updated: "2026-04-29T12:00:00",
  status: "inbox",
  contexts: [],
  energy: "low",
  time_minutes: 5,
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

function renderBar(mode: CaptureMode = "regular") {
  const qc = new QueryClient({
    defaultOptions: { queries: { retry: false, staleTime: Infinity } },
  });
  let currentMode = mode;
  const onModeChange = vi.fn((m: CaptureMode) => {
    currentMode = m;
  });
  const utils = render(
    <QueryClientProvider client={qc}>
      <CaptureBar env="work" focusTick={0} mode={currentMode} onModeChange={onModeChange} />
    </QueryClientProvider>,
  );
  return { ...utils, qc, onModeChange };
}

beforeEach(() => {
  vi.mocked(api.captureItem).mockResolvedValue({ ...baseItem });
});

afterEach(() => {
  vi.clearAllMocks();
});

describe("CaptureBar regular mode", () => {
  it("captures with at_top: false by default", async () => {
    const user = userEvent.setup();
    renderBar("regular");
    const input = screen.getByPlaceholderText(/Capture to inbox/i) as HTMLInputElement;
    fireEvent.change(input, { target: { value: "New thing" } });
    await user.click(screen.getByRole("button", { name: /^Capture$/ }));
    await waitFor(() => {
      expect(api.captureItem).toHaveBeenCalledTimes(1);
    });
    expect(api.captureItem).toHaveBeenCalledWith("work", "New thing", "", {
      energy: "low",
      time_minutes: 5,
      at_top: false,
    });
  });
});

describe("CaptureBar regular-top mode", () => {
  it("captures with at_top: true", async () => {
    const user = userEvent.setup();
    renderBar("regular-top");
    const input = screen.getByPlaceholderText(/Capture to inbox/i) as HTMLInputElement;
    fireEvent.change(input, { target: { value: "Urgent" } });
    await user.click(screen.getByRole("button", { name: /^Capture$/ }));
    await waitFor(() => {
      expect(api.captureItem).toHaveBeenCalledTimes(1);
    });
    expect(api.captureItem).toHaveBeenCalledWith("work", "Urgent", "", {
      energy: "low",
      time_minutes: 5,
      at_top: true,
    });
  });

  it('shows "(top)" in the destination hint', () => {
    renderBar("regular-top");
    expect(screen.getByText(/inbox \(top\)/)).toBeDefined();
  });
});
