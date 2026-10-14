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

/** "✋ grab": add this item to an existing grab bag, or a new one named on the spot. */
export function GrabButton({ env, item }: { env: string; item: Item }) {
  const [open, setOpen] = useState(false);
  return (
    <>
      <Button onClick={() => setOpen(true)} title="Put this item in a grab bag">
        ✋ grab
      </Button>
      {open && <GrabDialog env={env} item={item} onClose={() => setOpen(false)} />}
    </>
  );
}

function GrabDialog({ env, item, onClose }: { env: string; item: Item; onClose: () => void }) {
  const qc = useQueryClient();
  const inputRef = useRef<HTMLInputElement>(null);
  const [name, setName] = useState("");
  const { data: bags, isLoading } = useGrabBags(env);

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const done = (bag: GrabBag) => {
    qc.invalidateQueries({ queryKey: ["grab-bags", env] });
    toasts.show("success", `Grabbed "${item.title}" into ${bag.name}`);
    onClose();
  };
  const grabMut = useMutation<GrabBag, Error, GrabBag>({
    mutationFn: (bag) => api.grabItem(env, bag.id, item.id),
    onSuccess: done,
  });
  const createMut = useMutation<GrabBag, Error, string>({
    mutationFn: (bagName) => api.createGrabBag(env, bagName, item.id),
    onSuccess: done,
  });
  const busy = grabMut.isPending || createMut.isPending;

  const create = () => {
    const trimmed = name.trim();
    if (trimmed && !busy) createMut.mutate(trimmed);
  };

  return (
    <div
      className="capture-overlay"
      onClick={onClose}
      onKeyDown={(e) => {
        if (e.key === "Escape") {
          e.stopPropagation();
          onClose();
        }
      }}
    >
      <div
        className="capture grab-dialog"
        role="dialog"
        aria-label="Grab into a bag"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="grab-dialog-bags">
          {isLoading && <span className="search-empty">Loading…</span>}
          {bags?.map((b) => (
            <Button
              key={b.id}
              onClick={() => grabMut.mutate(b)}
              busy={grabMut.isPending && grabMut.variables?.id === b.id}
              disabled={busy}
              title={`${itemCount(b.item_count)} · ${fmtAge(b.created)} old`}
            >
              {b.name}
            </Button>
          ))}
          {bags?.length === 0 && <span className="search-empty">No grab bags yet.</span>}
        </div>
        <form
          className="grab-dialog-new"
          onSubmit={(e) => {
            e.preventDefault();
            create();
          }}
        >
          <input
            ref={inputRef}
            type="text"
            placeholder="New grab bag name…"
            value={name}
            disabled={busy}
            onChange={(e) => setName(e.target.value)}
          />
          <Button type="submit" busy={createMut.isPending} disabled={busy || !name.trim()}>
            + New bag
          </Button>
        </form>
        <div className="capture-hint">Esc to cancel · grabbing doesn't change the item</div>
      </div>
    </div>
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
    return <div className="empty">No grab bags. Use ✋ grab on any item to start one.</div>;
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
