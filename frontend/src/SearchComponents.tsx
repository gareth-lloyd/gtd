import React, { useEffect, useRef, useState } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import { useSearchIndex, type SearchHit } from "./search";
import { contextChipStyle } from "./context-colors";
import { ProjectBadges } from "./ProjectComponents";
import { useEnvParam } from "./useEnvParam";

const SEARCH_CAP = 200;
const DROPDOWN_LIMIT = 8;

export function hitLink(env: string, hit: SearchHit): string {
  return hit.kind === "item"
    ? `/${env}/items/${hit.item.id}`
    : `/${env}/projects/${hit.project.id}`;
}

export function HitRow({
  hit,
  selected,
  onClick,
}: {
  hit: SearchHit;
  selected?: boolean;
  onClick?: () => void;
}) {
  if (hit.kind === "item") {
    const item = hit.item;
    return (
      <div className={selected ? "search-hit selected" : "search-hit"} onClick={onClick}>
        <span className="hit-kind">item</span>
        <span className="hit-title">{item.title}</span>
        <span className="hit-meta">
          <span className="chip">{item.status}</span>
          {item.contexts.slice(0, 3).map((c) => (
            <span key={c} className="chip context-chip" style={contextChipStyle(c)}>
              @{c}
            </span>
          ))}
        </span>
      </div>
    );
  }
  const project = hit.project;
  return (
    <div className={selected ? "search-hit selected" : "search-hit"} onClick={onClick}>
      <span className="hit-kind">project</span>
      <span className="hit-title">{project.title}</span>
      <span className="hit-meta">
        <ProjectBadges project={project} />
        {project.outcome && <span className="hit-snippet">{project.outcome}</span>}
      </span>
    </div>
  );
}

export function SearchBar({ env, focusTick }: { env: string; focusTick: number }) {
  const navigate = useNavigate();
  const inputRef = useRef<HTMLInputElement>(null);
  const [query, setQuery] = useState("");
  const [focused, setFocused] = useState(false);
  const [selected, setSelected] = useState(0);
  const [everFocused, setEverFocused] = useState(false);
  const { index, isLoading } = useSearchIndex(env, { enabled: everFocused });

  useEffect(() => {
    if (focusTick === 0) return;
    inputRef.current?.focus();
    inputRef.current?.select();
  }, [focusTick]);

  useEffect(() => {
    setSelected(0);
  }, [query]);

  const allHits = useMemoSearch(index, query, SEARCH_CAP);
  const hits = allHits.slice(0, DROPDOWN_LIMIT);
  const total = allHits.length;
  const hasQuery = query.trim().length > 0;
  const showDropdown = focused && hasQuery;

  function activate(hit: SearchHit) {
    setFocused(false);
    setQuery("");
    navigate(hitLink(env, hit));
  }

  function seeAll() {
    setFocused(false);
    navigate(`/${env}/search?q=${encodeURIComponent(query.trim())}`);
  }

  function onKeyDown(e: React.KeyboardEvent<HTMLInputElement>) {
    if (e.key === "Escape") {
      setQuery("");
      inputRef.current?.blur();
      return;
    }
    if (!hasQuery) return;
    if (e.key === "ArrowDown") {
      e.preventDefault();
      setSelected((s) => Math.min(s + 1, hits.length));
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setSelected((s) => Math.max(s - 1, 0));
    } else if (e.key === "Enter") {
      e.preventDefault();
      if (selected < hits.length) activate(hits[selected]);
      else seeAll();
    }
  }

  return (
    <div className="search-bar">
      <input
        ref={inputRef}
        type="search"
        placeholder="Search… (/)"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onFocus={() => {
          setFocused(true);
          setEverFocused(true);
        }}
        onBlur={() => {
          setTimeout(() => setFocused(false), 100);
        }}
        onKeyDown={onKeyDown}
      />
      {showDropdown && (
        <div className="search-dropdown">
          {isLoading && !index && <div className="search-empty">Building index…</div>}
          {index && hits.length === 0 && <div className="search-empty">No matches.</div>}
          {hits.map((hit, i) => (
            <div
              key={`${hit.kind}:${hit.id}`}
              onMouseDown={(e) => e.preventDefault()}
              onClick={() => activate(hit)}
              onMouseEnter={() => setSelected(i)}
            >
              <HitRow hit={hit} selected={i === selected} />
            </div>
          ))}
          {total > hits.length && (
            <div
              className={selected === hits.length ? "search-see-all selected" : "search-see-all"}
              onMouseDown={(e) => e.preventDefault()}
              onClick={seeAll}
              onMouseEnter={() => setSelected(hits.length)}
            >
              See all {total} results →
            </div>
          )}
        </div>
      )}
    </div>
  );
}

function useMemoSearch(
  index: ReturnType<typeof useSearchIndex>["index"],
  query: string,
  limit: number,
): SearchHit[] {
  const trimmed = query.trim();
  return React.useMemo(() => {
    if (!index || !trimmed) return [];
    return index.search(trimmed, limit);
  }, [index, trimmed, limit]);
}

export function SearchView() {
  const env = useEnvParam();
  const [params, setParams] = useSearchParams();
  const q = params.get("q") ?? "";
  const { index, isLoading } = useSearchIndex(env);
  const hits = useMemoSearch(index, q, SEARCH_CAP);

  const items = hits.filter((h) => h.kind === "item");
  const projects = hits.filter((h) => h.kind === "project");

  return (
    <div className="search-view">
      <input
        type="search"
        className="search-view-input"
        placeholder="Search…"
        value={q}
        onChange={(e) => {
          const next = new URLSearchParams(params);
          if (e.target.value) next.set("q", e.target.value);
          else next.delete("q");
          setParams(next, { replace: true });
        }}
        autoFocus
      />
      {!q.trim() && <div className="empty">Type to search.</div>}
      {q.trim() && isLoading && !index && <div className="empty">Building index…</div>}
      {q.trim() && index && hits.length === 0 && <div className="empty">No matches.</div>}
      {projects.length > 0 && (
        <>
          <h3 className="search-group-title">Projects ({projects.length})</h3>
          <ul className="search-results">
            {projects.map((hit) => (
              <li key={hit.id}>
                <Link to={hitLink(env, hit)} className="search-result-link">
                  <HitRow hit={hit} />
                </Link>
              </li>
            ))}
          </ul>
        </>
      )}
      {items.length > 0 && (
        <>
          <h3 className="search-group-title">Items ({items.length})</h3>
          <ul className="search-results">
            {items.map((hit) => (
              <li key={hit.id}>
                <Link to={hitLink(env, hit)} className="search-result-link">
                  <HitRow hit={hit} />
                </Link>
              </li>
            ))}
          </ul>
          {hits.length === SEARCH_CAP && (
            <div className="empty">Showing first {SEARCH_CAP} — refine your search.</div>
          )}
        </>
      )}
    </div>
  );
}
