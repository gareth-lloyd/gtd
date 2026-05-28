import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import App from "./App";

function jsonResponse(body: unknown, status = 200): Response {
  return {
    ok: status >= 200 && status < 300,
    status,
    json: async () => body,
  } as Response;
}

const fetchMock = vi.fn();

beforeEach(() => {
  localStorage.clear();
  fetchMock.mockReset();
  vi.stubGlobal("fetch", fetchMock);
});

afterEach(() => {
  vi.unstubAllGlobals();
});

describe("passphrase gate", () => {
  it("shows the gate when no token is stored", () => {
    render(<App />);
    expect(screen.getByLabelText("Passphrase")).toBeInTheDocument();
    expect(fetchMock).not.toHaveBeenCalled();
  });

  it("stores the token and reveals the tabs on submit", async () => {
    fetchMock.mockResolvedValue(jsonResponse([{ name: "home" }, { name: "work" }]));
    render(<App />);
    await userEvent.type(screen.getByLabelText("Passphrase"), "letmein");
    await userEvent.click(screen.getByRole("button", { name: "Unlock" }));

    expect(localStorage.getItem("gtd:token")).toBe("letmein");
    expect(await screen.findByRole("button", { name: "capture" })).toBeInTheDocument();
  });

  it("clears the token and re-shows the gate on a 401", async () => {
    localStorage.setItem("gtd:token", "stale");
    fetchMock.mockResolvedValue(jsonResponse({ error: "invalid token" }, 401));
    render(<App />);

    expect(await screen.findByRole("alert")).toHaveTextContent(/passphrase/i);
    expect(localStorage.getItem("gtd:token")).toBeNull();
    expect(screen.getByLabelText("Passphrase")).toBeInTheDocument();
  });
});

describe("authenticated requests", () => {
  beforeEach(() => {
    localStorage.setItem("gtd:token", "secret");
  });

  it("sends the X-GTD-Token header", async () => {
    fetchMock.mockResolvedValue(jsonResponse([{ name: "home" }]));
    render(<App />);
    await waitFor(() => expect(fetchMock).toHaveBeenCalled());
    const [, init] = fetchMock.mock.calls[0];
    const headers = new Headers(init.headers);
    expect(headers.get("X-GTD-Token")).toBe("secret");
  });

  it("captures to inbox and clears the textarea", async () => {
    fetchMock
      .mockResolvedValueOnce(jsonResponse([{ name: "home" }]))
      .mockResolvedValueOnce(jsonResponse({ id: "1", title: "buy milk", status: "inbox" }, 201));
    render(<App />);
    await screen.findByRole("button", { name: "capture" });

    const box = screen.getByLabelText("Capture");
    await userEvent.type(box, "buy milk");
    await userEvent.click(screen.getByRole("button", { name: "Capture" }));

    const captureCall = fetchMock.mock.calls.find(([url]) => url === "/api/envs/home/capture/");
    expect(captureCall).toBeTruthy();
    expect(JSON.parse(captureCall![1].body)).toEqual({ title: "buy milk", body: "" });
    expect(await screen.findByRole("status")).toHaveTextContent(/captured/i);
    expect(box).toHaveValue("");
  });

  it("renders inbox items", async () => {
    fetchMock.mockImplementation((url: string) => {
      if (url === "/api/envs/home/inbox/")
        return Promise.resolve(
          jsonResponse([
            { id: "1", title: "task one", contexts: ["calls"], project: null, overdue: false },
          ]),
        );
      return Promise.resolve(jsonResponse([{ name: "home" }]));
    });
    render(<App />);
    await userEvent.click(await screen.findByRole("button", { name: "inbox" }));

    const list = await screen.findByRole("list");
    expect(within(list).getByText("task one")).toBeInTheDocument();
    expect(within(list).getByText("calls")).toBeInTheDocument();
  });

  it("switches env, refetches, and persists the choice", async () => {
    fetchMock.mockImplementation((url: string) => {
      if (url === "/api/envs/")
        return Promise.resolve(jsonResponse([{ name: "home" }, { name: "work" }]));
      return Promise.resolve(jsonResponse([])); // any inbox/next list = empty
    });
    render(<App />);
    await userEvent.click(await screen.findByRole("button", { name: "inbox" }));
    await screen.findByText(/nothing here/i);

    await userEvent.selectOptions(screen.getByLabelText("Environment"), "work");

    expect(localStorage.getItem("gtd:env")).toBe("work");
    await waitFor(() =>
      expect(fetchMock.mock.calls.some(([url]) => url === "/api/envs/work/inbox/")).toBe(true),
    );
  });

  it("warns when a capture is saved but not yet synced", async () => {
    fetchMock
      .mockResolvedValueOnce(jsonResponse([{ name: "home" }]))
      .mockResolvedValueOnce(
        jsonResponse({ id: "1", title: "x", status: "inbox", synced: false }, 201),
      );
    render(<App />);
    await screen.findByRole("button", { name: "capture" });
    await userEvent.type(screen.getByLabelText("Capture"), "x");
    await userEvent.click(screen.getByRole("button", { name: "Capture" }));

    expect(await screen.findByRole("status")).toHaveTextContent(/sync pending/i);
  });

  it("surfaces a non-401 capture error instead of silently failing", async () => {
    fetchMock
      .mockResolvedValueOnce(jsonResponse([{ name: "home" }]))
      .mockResolvedValueOnce(jsonResponse({ error: "unknown context(s): ['bogus']" }, 400));
    render(<App />);
    await screen.findByRole("button", { name: "capture" });
    await userEvent.type(screen.getByLabelText("Capture"), "do thing");
    await userEvent.click(screen.getByRole("button", { name: "Capture" }));

    const alert = await screen.findByRole("alert");
    expect(alert).toHaveTextContent(/unknown context/i);
    // The text is preserved on failure so the user can retry.
    expect(screen.getByLabelText("Capture")).toHaveValue("do thing");
  });

  it("shows an error instead of an infinite Loading state when a read fails", async () => {
    fetchMock.mockImplementation((url: string) => {
      if (url === "/api/envs/") return Promise.resolve(jsonResponse([{ name: "home" }]));
      return Promise.resolve(jsonResponse({ error: "boom" }, 500));
    });
    render(<App />);
    await userEvent.click(await screen.findByRole("button", { name: "inbox" }));

    expect(await screen.findByRole("alert")).toHaveTextContent(/boom/i);
    expect(screen.queryByText(/loading/i)).not.toBeInTheDocument();
  });

  it("falls back to a real env when the persisted env no longer exists", async () => {
    localStorage.setItem("gtd:env", "home"); // not in the server's list
    fetchMock.mockImplementation((url: string) => {
      if (url === "/api/envs/") return Promise.resolve(jsonResponse([{ name: "work" }]));
      return Promise.resolve(jsonResponse([]));
    });
    render(<App />);
    await screen.findByRole("button", { name: "capture" });

    await waitFor(() => expect(localStorage.getItem("gtd:env")).toBe("work"));
  });
});
