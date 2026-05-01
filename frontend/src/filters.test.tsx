import { describe, it, expect } from "vitest";
import { renderHook, act } from "@testing-library/react";
import { MemoryRouter, useLocation } from "react-router-dom";
import { useNextFilters } from "./filters";

function wrap(initial: string) {
  return function Wrapper({ children }: { children: React.ReactNode }) {
    return <MemoryRouter initialEntries={[initial]}>{children}</MemoryRouter>;
  };
}

function renderWithLocation(initial: string) {
  let location: ReturnType<typeof useLocation> | null = null;
  const { result } = renderHook(
    () => {
      location = useLocation();
      return useNextFilters();
    },
    { wrapper: wrap(initial) },
  );
  return { result, getLocation: () => location! };
}

describe("useNextFilters — overdue", () => {
  it("reads overdue=true from the URL", () => {
    const { result } = renderWithLocation("/work/next?overdue=true");
    expect(result.current.overdue).toBe(true);
  });

  it("defaults overdue to false when absent", () => {
    const { result } = renderWithLocation("/work/next");
    expect(result.current.overdue).toBe(false);
  });

  it("setOverdue(true) writes overdue=true to the URL", () => {
    const { result, getLocation } = renderWithLocation("/work/next");
    act(() => result.current.setOverdue(true));
    expect(getLocation().search).toContain("overdue=true");
  });

  it("setOverdue(false) drops the param entirely", () => {
    const { result, getLocation } = renderWithLocation("/work/next?overdue=true");
    act(() => result.current.setOverdue(false));
    expect(getLocation().search).not.toContain("overdue");
  });

  it("combines with contexts without clobbering them", () => {
    const { result, getLocation } = renderWithLocation("/work/next?contexts=calls");
    act(() => result.current.setOverdue(true));
    const search = getLocation().search;
    expect(search).toContain("contexts=calls");
    expect(search).toContain("overdue=true");
  });
});
