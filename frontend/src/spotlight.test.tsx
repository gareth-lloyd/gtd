import { describe, it, expect } from "vitest";
import { renderHook, act } from "@testing-library/react";
import { MemoryRouter, useLocation } from "react-router-dom";
import { useSpotlight } from "./spotlight";
import { ROUTER_FUTURE } from "./routerConfig";

function wrap(initial: string) {
  return function Wrapper({ children }: { children: React.ReactNode }) {
    return (
      <MemoryRouter initialEntries={[initial]} future={ROUTER_FUTURE}>
        {children}
      </MemoryRouter>
    );
  };
}

function renderWithLocation(initial: string) {
  let location: ReturnType<typeof useLocation> | null = null;
  const { result } = renderHook(
    () => {
      location = useLocation();
      return useSpotlight();
    },
    { wrapper: wrap(initial) },
  );
  return { result, getLocation: () => location! };
}

describe("useSpotlight", () => {
  it("reads spotlight=<id> from the URL", () => {
    const { result } = renderWithLocation("/work/next?spotlight=abc");
    expect(result.current.spotlightId).toBe("abc");
  });

  it("defaults spotlightId to null when absent", () => {
    const { result } = renderWithLocation("/work/next");
    expect(result.current.spotlightId).toBeNull();
  });

  it("setSpotlight(id) writes the id to the URL", () => {
    const { result, getLocation } = renderWithLocation("/work/next");
    act(() => result.current.setSpotlight("xyz"));
    expect(getLocation().search).toContain("spotlight=xyz");
  });

  it("setSpotlight(null) drops the param entirely", () => {
    const { result, getLocation } = renderWithLocation("/work/next?spotlight=abc");
    act(() => result.current.setSpotlight(null));
    expect(getLocation().search).not.toContain("spotlight");
  });

  it("preserves other query params when setting", () => {
    const { result, getLocation } = renderWithLocation("/work/next?contexts=calls");
    act(() => result.current.setSpotlight("xyz"));
    const search = getLocation().search;
    expect(search).toContain("contexts=calls");
    expect(search).toContain("spotlight=xyz");
  });
});
