import { useEffect, useRef, useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Link, NavLink, useNavigate, useParams } from "react-router-dom";
import { api, type GrabBag, type Item } from "./api";
import { Button } from "./Button";
import { fmtAge } from "./format";
import { ItemList } from "./ItemList";
import { toasts } from "./toast";
import { useEnvParam } from "./useEnvParam";

// Grab bags are throwaway, named collections of items to look at in one place.
// Membership lives on the bag only: grabbing or emptying never touches an item.
// The server prunes a bag once every item in it is archived/trashed.

const NAV_LIMIT = 3;

function useGrabBags(env: string) {
  return useQuery({
    queryKey: ["grab-bags", env],
    queryFn: () => api.listGrabBags(env),
  });
}

function itemCount(n: number): string {
  return n === 1 ? "1 item" : `${n} items`;
}

/**
 * A row of "✋ <bag>" buttons under an item's workflow actions — one click
 * grabs the item into that bag. Bags already holding the item show pressed.
 * Bags are only created from the side nav's "+".
 */
export function GrabRow({ env, item }: { env: string; item: Item }) {
  const qc = useQueryClient();
  const { data: bags } = useGrabBags(env);
  const grabMut = useMutation<GrabBag, Error, GrabBag>({
    mutationFn: (bag) => api.grabItem(env, bag.id, item.id),
    onSuccess: (_, bag) => {
      qc.invalidateQueries({ queryKey: ["grab-bags", env] });
      toasts.show("success", `Grabbed "${item.title}" into ${bag.name}`);
    },
  });
  if (!bags || bags.length === 0) return null;
  return (
    <div className="item-actions grab-row" onClick={(e) => e.stopPropagation()}>
      {bags.map((b) => {
        const held = b.item_ids.includes(item.id);
        return (
          <Button
            key={b.id}
            aria-pressed={held || undefined}
            onClick={() => grabMut.mutate(b)}
            busy={grabMut.isPending && grabMut.variables?.id === b.id}
            disabled={held || grabMut.isPending}
            title={held ? `Already in ${b.name}` : `Grab into ${b.name}`}
          >
            ✋ {b.name}
          </Button>
        );
      })}
    </div>
  );
}

/** Side-nav "grab bags" entry with a "+" to name a new bag, then the recent bags. */
export function GrabBagsNavSection({ env }: { env: string }) {
  const qc = useQueryClient();
  const [adding, setAdding] = useState(false);
  const [name, setName] = useState("");
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (adding) inputRef.current?.focus();
  }, [adding]);

  const close = () => {
    setAdding(false);
    setName("");
  };
  const createMut = useMutation<GrabBag, Error, string>({
    mutationFn: (bagName) => api.createGrabBag(env, bagName),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["grab-bags", env] });
      close();
    },
  });

  return (
    <>
      <div className="side-nav-row">
        <NavLink to="grab-bags" end className={({ isActive }) => (isActive ? "active" : "")}>
          grab bags
        </NavLink>
        <button
          type="button"
          className="side-nav-add"
          aria-label="New grab bag"
          title="New grab bag"
          onClick={() => (adding ? close() : setAdding(true))}
        >
          +
        </button>
      </div>
      {adding && (
        <form
          className="side-nav-new"
          onSubmit={(e) => {
            e.preventDefault();
            const trimmed = name.trim();
            if (trimmed && !createMut.isPending) createMut.mutate(trimmed);
          }}
        >
          <input
            ref={inputRef}
            type="text"
            placeholder="Bag name…"
            value={name}
            disabled={createMut.isPending}
            onChange={(e) => setName(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Escape") {
                e.stopPropagation();
                close();
              }
            }}
          />
        </form>
      )}
      <GrabBagNavLinks env={env} />
    </>
  );
}

/** Side-nav sub-links: the most recently touched bags. */
export function GrabBagNavLinks({ env }: { env: string }) {
  const { data: bags } = useGrabBags(env);
  if (!bags || bags.length === 0) return null;
  return (
    <div className="side-nav-sub">
      {bags.slice(0, NAV_LIMIT).map((b) => (
        <NavLink
          key={b.id}
          to={`/${env}/grab-bags/${b.id}`}
          className={({ isActive }) => (isActive ? "sub-link active" : "sub-link")}
          title={b.name}
        >
          <span className="sub-link-title">{b.name}</span>
        </NavLink>
      ))}
    </div>
  );
}

export function GrabBagsView() {
  const env = useEnvParam();
  const { data: bags, isLoading } = useGrabBags(env);
  if (isLoading) return <div className="empty">Loading…</div>;
  if (!bags || bags.length === 0) {
    return (
      <div className="empty">No grab bags. Use + next to grab bags in the menu to start one.</div>
    );
  }
  return (
    <ul className="project-index">
      {bags.map((b) => (
        <li key={b.id}>
          <Link to={`/${env}/grab-bags/${b.id}`} className="project-index-row">
            <span className="project-index-title">{b.name}</span>
            <span className="chip">{itemCount(b.item_count)}</span>
            <span className="chip" title={`created ${b.created}`}>
              {fmtAge(b.created)} old
            </span>
          </Link>
        </li>
      ))}
    </ul>
  );
}

export function GrabBagDetailView() {
  const env = useEnvParam();
  const { bagId = "" } = useParams<{ bagId: string }>();
  const navigate = useNavigate();
  const qc = useQueryClient();
  const { data, isLoading } = useQuery({
    queryKey: ["grab-bags", env, bagId],
    queryFn: () => api.getGrabBag(env, bagId),
  });

  const emptyMut = useMutation({
    mutationFn: () => api.emptyGrabBag(env, bagId),
    onSuccess: () => {
      qc.removeQueries({ queryKey: ["grab-bags", env, bagId] });
      qc.invalidateQueries({ queryKey: ["grab-bags", env] });
      navigate(`/${env}/grab-bags`);
    },
  });

  if (isLoading) return <div className="empty">Loading…</div>;
  if (!data) {
    return (
      <div className="empty">
        This grab bag is gone — emptied, or everything in it is done.{" "}
        <Link to={`/${env}/grab-bags`}>All grab bags</Link>
      </div>
    );
  }

  const { bag, items } = data;
  return (
    <div className="project-detail">
      <header className="project-header">
        <h2>{bag.name}</h2>
        <div className="project-meta">
          <span className="chip" title={bag.created}>
            {fmtAge(bag.created) === "just now"
              ? "created just now"
              : `created ${fmtAge(bag.created)} ago`}
          </span>
          <span className="chip">{itemCount(items.length)}</span>
        </div>
      </header>
      <div className="project-actions">
        <Button
          onClick={() => {
            if (
              confirm(
                `Empty "${bag.name}"? The bag is deleted; its items are not changed or completed.`,
              )
            ) {
              emptyMut.mutate();
            }
          }}
          busy={emptyMut.isPending}
          title="Delete this bag. Items keep their project, bucket and every other field."
        >
          Empty
        </Button>
      </div>
      <ItemList env={env} items={items} />
    </div>
  );
}
