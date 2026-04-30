import { describe, it, expect } from 'vitest';
import type { Item } from './api';
import { computeProjectStats } from './ProjectComponents';

function mkItem(overrides: Partial<Item> = {}): Item {
  return {
    id: overrides.id ?? 'item',
    title: overrides.title ?? 'item',
    body: '',
    created: '2026-04-10T09:00:00',
    updated: '2026-04-10T09:00:00',
    status: 'next',
    contexts: [],
    energy: null,
    time_minutes: null,
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
    ...overrides,
  };
}

describe('computeProjectStats', () => {
  it('returns zeroed structure for an empty project', () => {
    const stats = computeProjectStats([]);
    expect(stats.totalMinutes).toBe(0);
    expect(stats.totalCount).toBe(0);
    expect(stats.byEnergy.low).toEqual({ count: 0, minutes: 0 });
    expect(stats.byEnergy.medium).toEqual({ count: 0, minutes: 0 });
    expect(stats.byEnergy.high).toEqual({ count: 0, minutes: 0 });
    expect(stats.byEnergy.unset).toEqual({ count: 0, minutes: 0 });
  });

  it('sums time and groups by energy, treating null energy as unset', () => {
    const stats = computeProjectStats([
      mkItem({ id: '1', energy: 'low', time_minutes: 15 }),
      mkItem({ id: '2', energy: 'low', time_minutes: 30 }),
      mkItem({ id: '3', energy: 'medium', time_minutes: 60 }),
      mkItem({ id: '4', energy: 'high', time_minutes: 5 }),
      mkItem({ id: '5', energy: null, time_minutes: 10 }),
      mkItem({ id: '6', energy: null, time_minutes: null }),
    ]);
    expect(stats.totalCount).toBe(6);
    expect(stats.totalMinutes).toBe(120);
    expect(stats.byEnergy.low).toEqual({ count: 2, minutes: 45 });
    expect(stats.byEnergy.medium).toEqual({ count: 1, minutes: 60 });
    expect(stats.byEnergy.high).toEqual({ count: 1, minutes: 5 });
    expect(stats.byEnergy.unset).toEqual({ count: 2, minutes: 10 });
  });

  it('treats null time_minutes as zero', () => {
    const stats = computeProjectStats([
      mkItem({ id: '1', energy: 'medium', time_minutes: null }),
    ]);
    expect(stats.totalMinutes).toBe(0);
    expect(stats.byEnergy.medium).toEqual({ count: 1, minutes: 0 });
  });
});
