import { useCallback, useEffect, useMemo, useRef } from 'react';
import { useQueryClient, type QueryClient } from '@tanstack/react-query';
import { api, type Item, type Project } from './api';
import { toasts } from './toast';

type Snapshot = {
  single: Item | undefined;
  lists: [unknown[], Item[] | undefined][];
} | null;

function findItemInSnapshot(snapshot: Snapshot, id: string): Item | undefined {
  if (!snapshot) return undefined;
  if (snapshot.single?.id === id) return snapshot.single;
  for (const [, list] of snapshot.lists) {
    const found = list?.find((i) => i.id === id);
    if (found) return found;
  }
  return undefined;
}

function projectMoveMessage(
  qc: QueryClient,
  env: string,
  oldProjectId: string | null,
  newProjectId: string | null
): string {
  const projects = qc.getQueryData<Project[]>(['projects', env, false]);
  const titleFor = (id: string | null) =>
    id ? projects?.find((p) => p.id === id)?.title ?? id : null;
  const oldTitle = titleFor(oldProjectId);
  const newTitle = titleFor(newProjectId);
  if (newTitle && oldTitle) return `Moved from ${oldTitle} to ${newTitle}`;
  if (newTitle) return `Moved to ${newTitle}`;
  return `Removed from ${oldTitle ?? 'project'}`;
}

export function invalidateItemQueries(
  qc: QueryClient,
  env: string,
  itemId: string,
) {
  qc.invalidateQueries({ queryKey: ['items', env] });
  qc.invalidateQueries({ queryKey: ['item', env, itemId] });
  qc.invalidateQueries({ queryKey: ['search-corpus', env], refetchType: 'none' });
  qc.invalidateQueries({ queryKey: ['snapshot-status'] });
  qc.invalidateQueries({ queryKey: ['projects', env] });
  // Prefix-match all project detail queries for this env — we can't reliably
  // determine the old project ID when the item was loaded via a composite
  // project detail query rather than an items list.
  qc.invalidateQueries({ queryKey: ['project', env] });
}

export function invalidateProjectQueries(
  qc: QueryClient,
  env: string,
  projectId?: string,
) {
  qc.invalidateQueries({ queryKey: ['projects', env] });
  if (projectId) {
    qc.invalidateQueries({ queryKey: ['project', env, projectId] });
  }
  qc.invalidateQueries({ queryKey: ['search-corpus', env], refetchType: 'none' });
  qc.invalidateQueries({ queryKey: ['snapshot-status'] });
}

/**
 * Find an item in the TanStack Query cache without triggering a fetch.
 * Checks both the single-item cache and all items-list caches.
 */
export function findItemInCache(
  qc: QueryClient,
  env: string,
  itemId: string,
): Item | undefined {
  const single = qc.getQueryData<Item>(['item', env, itemId]);
  if (single) return single;
  const lists = qc.getQueriesData<Item[]>({ queryKey: ['items', env] });
  for (const [, data] of lists) {
    const found = data?.find((i) => i.id === itemId);
    if (found) return found;
  }
  // Also check project detail caches (shape: { project, actions: Item[] })
  const projects = qc.getQueriesData<{ actions: Item[] }>({ queryKey: ['project', env] });
  for (const [, data] of projects) {
    const found = data?.actions?.find((i) => i.id === itemId);
    if (found) return found;
  }
  return undefined;
}

/**
 * Coalesces field-level edits into one PATCH per debounce window, with
 * optimistic cache updates (and rollback on error) so rapid edits feel
 * instant and the UI stays consistent across every list that contains
 * this item.
 */
export function useItemPatch(env: string, itemId: string) {
  const qc = useQueryClient();
  const pendingRef = useRef<Partial<Item>>({});
  const timerRef = useRef<number | null>(null);
  const snapshotRef = useRef<Snapshot>(null);

  const doFlush = useCallback(async () => {
    if (timerRef.current != null) {
      window.clearTimeout(timerRef.current);
      timerRef.current = null;
    }
    const patch = pendingRef.current;
    pendingRef.current = {};
    if (Object.keys(patch).length === 0) return;

    const projectChanged = 'project' in patch;
    const oldProject = projectChanged
      ? findItemInSnapshot(snapshotRef.current, itemId)?.project ?? null
      : null;

    try {
      const updated = await api.updateItem(env, itemId, patch);
      snapshotRef.current = null;
      invalidateItemQueries(qc, env, itemId);
      if (projectChanged && oldProject !== updated.project) {
        toasts.show('info', projectMoveMessage(qc, env, oldProject, updated.project));
      }
    } catch (err) {
      const snap = snapshotRef.current;
      if (snap) {
        qc.setQueryData(['item', env, itemId], snap.single);
        for (const [key, list] of snap.lists) {
          qc.setQueryData(key, list);
        }
      }
      snapshotRef.current = null;
      throw err;
    }
  }, [env, itemId, qc]);

  const patch = useCallback(
    (fields: Partial<Item>, opts: { debounce?: number } = {}) => {
      if (!snapshotRef.current) {
        const single = qc.getQueryData<Item>(['item', env, itemId]);
        const lists: [unknown[], Item[] | undefined][] = qc
          .getQueriesData<Item[]>({ queryKey: ['items', env] })
          .map(([key, data]) => [key as unknown[], data]);
        snapshotRef.current = { single, lists };
      }

      pendingRef.current = { ...pendingRef.current, ...fields };

      qc.setQueryData<Item | undefined>(['item', env, itemId], (prev) =>
        prev ? { ...prev, ...fields } : prev
      );
      qc.setQueriesData<Item[]>({ queryKey: ['items', env] }, (prev) =>
        prev?.map((it) => (it.id === itemId ? { ...it, ...fields } : it))
      );

      if (timerRef.current != null) {
        window.clearTimeout(timerRef.current);
      }
      const delay = opts.debounce ?? 0;
      if (delay === 0) {
        void doFlush();
      } else {
        timerRef.current = window.setTimeout(() => {
          timerRef.current = null;
          void doFlush();
        }, delay);
      }
    },
    [env, itemId, qc, doFlush]
  );

  useEffect(() => {
    return () => {
      if (timerRef.current != null) {
        window.clearTimeout(timerRef.current);
        void doFlush();
      }
    };
  }, [doFlush]);

  return { patch, flush: doFlush };
}

export type ChipOption<T extends string> = {
  value: T;
  label?: React.ReactNode;
  style?: React.CSSProperties;
  extra?: React.ReactNode;
};

type ChipToggleGroupProps<T extends string> = {
  options: ChipOption<T>[];
  noneLabel?: string;
  className?: string;
  styleForSelected?: (value: T) => React.CSSProperties | undefined;
  children?: React.ReactNode;
} & (
  | {
      mode: 'single';
      value: T | null;
      onChange: (next: T | null) => void;
    }
  | {
      mode: 'multi';
      value: T[];
      onChange: (next: T[]) => void;
    }
);

export function ChipToggleGroup<T extends string>(props: ChipToggleGroupProps<T>) {
  const { options, noneLabel, className, styleForSelected, children } = props;

  const selectedSet =
    props.mode === 'multi' ? new Set(props.value) : null;
  const isSelected = (v: T) =>
    props.mode === 'multi' ? selectedSet!.has(v) : props.value === v;

  const toggle = (v: T) => {
    if (props.mode === 'multi') {
      const arr = props.value;
      props.onChange(arr.includes(v) ? arr.filter((x) => x !== v) : [...arr, v]);
    } else {
      props.onChange(props.value === v ? null : v);
    }
  };

  return (
    <div className={`chip-toggle-group ${className ?? ''}`}>
      {noneLabel !== undefined && props.mode === 'single' && (
        <button
          type="button"
          className="chip-toggle"
          aria-pressed={props.value === null}
          onClick={() => props.onChange(null)}
        >
          {noneLabel}
        </button>
      )}
      {options.map((opt) => {
        const selected = isSelected(opt.value);
        const style = selected
          ? styleForSelected?.(opt.value) ?? opt.style
          : undefined;
        return (
          <button
            type="button"
            key={opt.value}
            className="chip-toggle"
            aria-pressed={selected}
            style={style}
            onClick={() => toggle(opt.value)}
          >
            {opt.label ?? opt.value}
            {opt.extra}
          </button>
        );
      })}
      {children}
    </div>
  );
}

interface DatePickerRowProps {
  value: string | null;
  onChange: (v: string | null) => void;
}

export function DatePickerRow({ value, onChange }: DatePickerRowProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const quick = useMemo(
    () => [
      { label: 'Today', v: daysFromToday(0) },
      { label: 'Tomorrow', v: daysFromToday(1) },
      { label: 'Next Mon', v: nextMonday() },
    ],
    []
  );
  const matchesQuick = quick.some((q) => q.v === value);
  const customDateSet = value != null && !matchesQuick;

  const openPicker = () => {
    const el = inputRef.current;
    if (!el) return;
    try {
      (el as HTMLInputElement & { showPicker?: () => void }).showPicker?.();
    } catch {
      el.focus();
      el.click();
    }
  };

  return (
    <>
      {quick.map((q) => (
        <button
          type="button"
          key={q.label}
          className="chip-toggle"
          aria-pressed={value === q.v}
          onClick={() => onChange(q.v)}
        >
          {q.label}
        </button>
      ))}
      <button
        type="button"
        className="chip-toggle picker"
        aria-pressed={customDateSet}
        onClick={openPicker}
        title={customDateSet ? `Picked ${value}` : 'Pick a date'}
      >
        <span aria-hidden>📅</span>
        {customDateSet && <span className="picker-date">{value}</span>}
      </button>
      {value && (
        <button
          type="button"
          className="chip-toggle clear"
          onClick={() => onChange(null)}
          title="Clear"
        >
          ×
        </button>
      )}
      <input
        ref={inputRef}
        type="date"
        className="hidden-date-input"
        tabIndex={-1}
        aria-hidden
        value={value ?? ''}
        onChange={(e) => onChange(e.target.value || null)}
      />
    </>
  );
}

function daysFromToday(offset: number): string {
  const d = new Date();
  d.setDate(d.getDate() + offset);
  return d.toISOString().slice(0, 10);
}

function nextMonday(): string {
  const d = new Date();
  const delta = (8 - d.getDay()) % 7 || 7;
  d.setDate(d.getDate() + delta);
  return d.toISOString().slice(0, 10);
}

/** True when defer_until is a future moment (scheduled, not yet active). */
export function isScheduled(item: { defer_until: string | null }): boolean {
  if (!item.defer_until) return false;
  const d = new Date(item.defer_until);
  if (Number.isNaN(d.getTime())) return false;
  return d > new Date();
}

interface DateTimePickerRowProps {
  value: string | null;
  onChange: (v: string | null) => void;
}

/**
 * Defer-until editor: quick presets (minutes/hours and canonical dates) plus
 * a datetime-local fallback. Values are stored as ISO strings; midnight for
 * day-level presets, precise hour:minute for sub-day presets.
 */
export function DateTimePickerRow({ value, onChange }: DateTimePickerRowProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const presets = useMemo(
    () => [
      { label: '+1h', make: () => hoursFromNow(1) },
      { label: '+3h', make: () => hoursFromNow(3) },
      { label: 'Tomorrow 9am', make: () => tomorrowAt(9, 0) },
      { label: 'Next Mon 9am', make: () => nextMondayAt(9, 0) },
    ],
    []
  );

  const inputValue = value ? toDatetimeLocalValue(value) : '';

  const openPicker = () => {
    const el = inputRef.current;
    if (!el) return;
    try {
      (el as HTMLInputElement & { showPicker?: () => void }).showPicker?.();
    } catch {
      el.focus();
      el.click();
    }
  };

  return (
    <>
      {presets.map((p) => (
        <button
          type="button"
          key={p.label}
          className="chip-toggle"
          onClick={() => onChange(p.make())}
        >
          {p.label}
        </button>
      ))}
      <button
        type="button"
        className="chip-toggle picker"
        aria-pressed={value != null}
        onClick={openPicker}
        title={value ? `Deferred until ${formatDateTime(value)}` : 'Pick a date/time'}
      >
        <span aria-hidden>📅</span>
        {value && <span className="picker-date">{formatDateTime(value)}</span>}
      </button>
      {value && (
        <button
          type="button"
          className="chip-toggle clear"
          onClick={() => onChange(null)}
          title="Clear"
        >
          ×
        </button>
      )}
      <input
        ref={inputRef}
        type="datetime-local"
        className="hidden-date-input"
        tabIndex={-1}
        aria-hidden
        value={inputValue}
        onChange={(e) => onChange(e.target.value ? fromDatetimeLocalValue(e.target.value) : null)}
      />
    </>
  );
}

function hoursFromNow(hours: number): string {
  const d = new Date();
  d.setHours(d.getHours() + hours);
  return toIsoLocal(d);
}

function tomorrowAt(hour: number, minute: number): string {
  const d = new Date();
  d.setDate(d.getDate() + 1);
  d.setHours(hour, minute, 0, 0);
  return toIsoLocal(d);
}

function nextMondayAt(hour: number, minute: number): string {
  const d = new Date();
  const delta = (8 - d.getDay()) % 7 || 7;
  d.setDate(d.getDate() + delta);
  d.setHours(hour, minute, 0, 0);
  return toIsoLocal(d);
}

/** Produce an ISO-like local timestamp without the "Z" suffix. */
function toIsoLocal(d: Date): string {
  const pad = (n: number) => String(n).padStart(2, '0');
  return (
    `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}` +
    `T${pad(d.getHours())}:${pad(d.getMinutes())}:00`
  );
}

function toDatetimeLocalValue(iso: string): string {
  // datetime-local inputs want "YYYY-MM-DDTHH:MM" (no seconds).
  const m = iso.match(/^(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2})/);
  if (m) return `${m[1]}T${m[2]}`;
  // Fall back: pure date → midnight
  if (/^\d{4}-\d{2}-\d{2}$/.test(iso)) return `${iso}T00:00`;
  return iso.slice(0, 16);
}

function fromDatetimeLocalValue(v: string): string {
  return v.length === 16 ? `${v}:00` : v;
}

function formatDateTime(iso: string): string {
  const m = iso.match(/^(\d{4}-\d{2}-\d{2})T(\d{2}):(\d{2})/);
  if (!m) return iso;
  const [, date, hh, mm] = m;
  if (hh === '00' && mm === '00') return date;
  return `${date} ${hh}:${mm}`;
}
