import { useCallback, useEffect, useMemo, useRef } from 'react';
import { useQueryClient, type QueryClient } from '@tanstack/react-query';
import { api, type Item } from './api';

export function invalidateItemQueries(
  qc: QueryClient,
  env: string,
  itemId: string,
  projectId?: string | null
) {
  qc.invalidateQueries({ queryKey: ['items', env] });
  qc.invalidateQueries({ queryKey: ['item', env, itemId] });
  qc.invalidateQueries({ queryKey: ['search-corpus', env], refetchType: 'none' });
  qc.invalidateQueries({ queryKey: ['snapshot-status'] });
  qc.invalidateQueries({ queryKey: ['projects', env] });
  if (projectId) {
    qc.invalidateQueries({ queryKey: ['project', env, projectId] });
  }
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
  const snapshotRef = useRef<{
    single: Item | undefined;
    lists: [unknown[], Item[] | undefined][];
  } | null>(null);

  const doFlush = useCallback(async () => {
    if (timerRef.current != null) {
      window.clearTimeout(timerRef.current);
      timerRef.current = null;
    }
    const patch = pendingRef.current;
    pendingRef.current = {};
    if (Object.keys(patch).length === 0) return;

    try {
      const updated = await api.updateItem(env, itemId, patch);
      snapshotRef.current = null;
      invalidateItemQueries(qc, env, itemId, updated.project);
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
  const { options, noneLabel, className, styleForSelected } = props;

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
