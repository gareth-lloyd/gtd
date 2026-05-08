import { useEffect, useMemo, useRef } from "react";
import { useQuery, keepPreviousData } from "@tanstack/react-query";
import { useSearchParams } from "react-router-dom";
import { useAutoAnimate } from "@formkit/auto-animate/react";
import { api, type Bucket, type Item } from "./api";
import { useNextFilters } from "./filters";
import { ItemCard } from "./ItemCard";
import { Button } from "./Button";
import { useEnvParam } from "./useEnvParam";
import { useSpotlight } from "./spotlight";
import { useSelection } from "./SelectionContext";
import { isEditableTarget } from "./CaptureBar";

const DEFAULT_DOC_TITLE = "gtd";

const DONE_PAGE_SIZE = 50;

export function NextActionsView() {
  const env = useEnvParam();
  const { contexts, energy, maxMinutes, minMinutes, noProject, overdue } = useNextFilters();
  const params: Record<string, string> = { status: "next" };
  if (contexts.length) params.contexts = contexts.join(",");
  if (energy) params.energy = energy;
  if (maxMinutes) params.max_minutes = maxMinutes;
  if (minMinutes) params.min_minutes = minMinutes;
  if (noProject) params.no_project = "true";
  if (overdue) params.overdue = "true";

  const { data: items, isLoading } = useQuery({
    queryKey: ["items", env, "next", contexts, energy, maxMinutes, minMinutes, noProject, overdue],
    queryFn: () => api.listItems(env, params),
  });

  if (isLoading) return <div className="empty">Loading…</div>;
  return <ItemList env={env} items={items ?? []} />;
}

export function BucketView({ env, bucket }: { env: string; bucket: Bucket }) {
  const [params, setParams] = useSearchParams();
  const includeDeferred = bucket === "inbox" && params.get("include_deferred") === "true";

  const listParams: Record<string, string> = { status: bucket };
  if (includeDeferred) listParams.include_deferred = "true";

  const { data: items, isLoading } = useQuery({
    queryKey: ["items", env, bucket, includeDeferred],
    queryFn: () => api.listItems(env, listParams),
  });

  return (
    <>
      {bucket === "inbox" && (
        <div className="bucket-toolbar">
          <label className="toggle">
            <input
              type="checkbox"
              checked={includeDeferred}
              onChange={(e) => {
                const next = new URLSearchParams(params);
                if (e.target.checked) next.set("include_deferred", "true");
                else next.delete("include_deferred");
                setParams(next, { replace: true });
              }}
            />
            Show deferred
          </label>
        </div>
      )}
      {isLoading ? (
        <div className="empty">Loading…</div>
      ) : (
        <ItemList env={env} items={items ?? []} />
      )}
    </>
  );
}

export function BucketRoute({ bucket }: { bucket: Bucket }) {
  const env = useEnvParam();
  return <BucketView env={env} bucket={bucket} />;
}

export function DoneView() {
  const env = useEnvParam();
  const [params, setParams] = useSearchParams();
  const page = Math.max(1, parseInt(params.get("page") ?? "1", 10) || 1);

  const { data, isLoading, isFetching } = useQuery({
    queryKey: ["items-done", env, page, DONE_PAGE_SIZE],
    queryFn: () => api.listDoneItems(env, page, DONE_PAGE_SIZE),
    placeholderData: keepPreviousData,
  });

  if (isLoading) return <div className="empty">Loading…</div>;

  const total = data?.total ?? 0;
  const items = data?.items ?? [];
  const hasNext = data?.has_next ?? false;
  const hasPrev = page > 1;
  const totalPages = Math.max(1, Math.ceil(total / DONE_PAGE_SIZE));

  const goto = (next: number) => {
    const sp = new URLSearchParams(params);
    if (next <= 1) sp.delete("page");
    else sp.set("page", String(next));
    setParams(sp, { replace: true });
  };

  return (
    <>
      <div className="bucket-toolbar">
        <span className="status">
          {total === 0 ? "No completed items." : `${total} done · page ${page}/${totalPages}`}
        </span>
        <div className="spacer" />
        <Button onClick={() => goto(page - 1)} disabled={!hasPrev || isFetching}>
          ← Prev
        </Button>
        <Button onClick={() => goto(page + 1)} disabled={!hasNext || isFetching}>
          Next →
        </Button>
      </div>
      {items.length === 0 ? (
        <div className="empty">Nothing here.</div>
      ) : (
        <ItemList env={env} items={items} />
      )}
    </>
  );
}

export function ItemList({ env, items }: { env: string; items: Item[] }) {
  const { data: projects } = useQuery({
    queryKey: ["projects", env, false],
    queryFn: () => api.listProjects(env, false),
  });
  const [listRef] = useAutoAnimate<HTMLUListElement>();
  const { spotlightId, setSpotlight } = useSpotlight();
  const { select, selectedId, setNavigableIds } = useSelection();

  const spotlitItem = spotlightId ? items.find((i) => i.id === spotlightId) : undefined;
  const visibleItems = useMemo(() => (spotlitItem ? [spotlitItem] : items), [spotlitItem, items]);

  useEffect(() => {
    setNavigableIds(visibleItems.map((i) => i.id));
    return () => setNavigableIds([]);
  }, [visibleItems, setNavigableIds]);

  // Auto-select on spotlight transition only. Depending on the id (not the
  // object) keeps this stable across TanStack refetches and lets the user
  // collapse via Escape without us re-expanding.
  useEffect(() => {
    if (!spotlitItem) return;
    select(spotlitItem.id);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [spotlitItem?.id]);

  useEffect(() => {
    if (spotlightId && !spotlitItem && items.length > 0) setSpotlight(null);
  }, [spotlightId, spotlitItem, items.length, setSpotlight]);

  useEffect(() => {
    const title = spotlitItem?.title;
    if (!title) return;
    const previous = document.title;
    document.title = title;
    return () => {
      document.title = previous || DEFAULT_DOC_TITLE;
    };
  }, [spotlitItem?.title]);

  // Read selectedId via ref so the listener doesn't churn on every selection.
  const selectedIdRef = useRef(selectedId);
  selectedIdRef.current = selectedId;
  useEffect(() => {
    if (!spotlitItem) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key !== "Escape") return;
      if (isEditableTarget(e.target)) return;
      const active = document.activeElement as HTMLElement | null;
      if (active?.closest(".capture") || active?.closest(".search-bar")) return;
      if (selectedIdRef.current) return;
      setSpotlight(null);
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [spotlitItem, setSpotlight]);

  if (items.length === 0) return <div className="empty">Nothing here.</div>;
  return (
    <>
      {spotlitItem && (
        <button
          type="button"
          className="spotlight-exit"
          aria-label="Exit spotlight"
          title="Exit spotlight (Esc)"
          onClick={() => setSpotlight(null)}
        >
          ✕
        </button>
      )}
      <ul ref={listRef} className={`item-list${spotlitItem ? " spotlight-mode" : ""}`}>
        {visibleItems.map((item) => (
          <li key={item.id}>
            <ItemCard env={env} item={item} projects={projects} />
          </li>
        ))}
      </ul>
    </>
  );
}
