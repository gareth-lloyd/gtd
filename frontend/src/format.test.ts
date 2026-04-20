import { afterEach, describe, expect, it, vi } from 'vitest';
import type { Project } from './api';
import { fmtDate, generateProjectId, slugify, sortProjects } from './format';

function mkProject(overrides: Partial<Project> = {}): Project {
  return {
    id: overrides.id ?? 'p',
    title: overrides.title ?? 'Project',
    body: '',
    created: '2026-03-01T09:00:00',
    updated: '2026-03-01T09:00:00',
    status: 'active',
    outcome: null,
    area: null,
    tags: [],
    due: null,
    priority: null,
    max_next_items: null,
    ...overrides,
  };
}

describe('slugify', () => {
  it('lowercases and collapses non-alphanumerics to hyphens', () => {
    expect(slugify('Hello, world!')).toBe('hello-world');
    expect(slugify('Email Sarah — re: Q2 plans')).toBe('email-sarah-re-q2-plans');
  });

  it('trims leading and trailing hyphens', () => {
    expect(slugify('  --Hello--  ')).toBe('hello');
  });

  it('returns "untitled" for empty or punctuation-only input', () => {
    expect(slugify('')).toBe('untitled');
    expect(slugify('---')).toBe('untitled');
    expect(slugify('!!!???')).toBe('untitled');
  });

  it('truncates to 50 characters', () => {
    const long = 'a'.repeat(100);
    const result = slugify(long);
    expect(result.length).toBe(50);
    expect(result).toBe('a'.repeat(50));
  });

  it('produces stable slugs for identical inputs', () => {
    expect(slugify('Ship frontend')).toBe(slugify('SHIP FRONTEND'));
  });
});

describe('generateProjectId', () => {
  afterEach(() => {
    vi.useRealTimers();
  });

  it('prefixes with today\'s ISO date and appends a slug', () => {
    vi.useFakeTimers();
    vi.setSystemTime(new Date('2026-04-20T09:15:00Z'));
    const id = generateProjectId('Ship frontend');
    expect(id).toMatch(/^\d{4}-\d{2}-\d{2}-[a-z0-9-]+$/);
    expect(id.endsWith('-ship-frontend')).toBe(true);
  });

  it('falls back to "untitled" slug for empty titles', () => {
    vi.useFakeTimers();
    vi.setSystemTime(new Date('2026-04-20T09:15:00Z'));
    expect(generateProjectId('')).toMatch(/^\d{4}-\d{2}-\d{2}-untitled$/);
  });
});

describe('fmtDate', () => {
  it('returns the first 10 chars for an ISO datetime', () => {
    expect(fmtDate('2026-04-20T14:30:00')).toBe('2026-04-20');
  });

  it('returns plain ISO date unchanged', () => {
    expect(fmtDate('2026-04-20')).toBe('2026-04-20');
  });

  it('returns empty string for empty input', () => {
    expect(fmtDate('')).toBe('');
  });
});

describe('sortProjects', () => {
  it('sorts by priority ascending (1 before 3)', () => {
    const input = [
      mkProject({ id: 'a', priority: 3 }),
      mkProject({ id: 'b', priority: 1 }),
    ];
    const result = sortProjects(input);
    expect(result.map((p) => p.id)).toEqual(['b', 'a']);
  });

  it('null priority sorts after rated projects', () => {
    const input = [
      mkProject({ id: 'unrated', priority: null, title: 'A' }),
      mkProject({ id: 'rated', priority: 5, title: 'Z' }),
    ];
    const result = sortProjects(input);
    expect(result.map((p) => p.id)).toEqual(['rated', 'unrated']);
  });

  it('ties on priority break by due date (ISO ascending)', () => {
    const input = [
      mkProject({ id: 'later', priority: 2, due: '2026-06-01', title: 'Z' }),
      mkProject({ id: 'sooner', priority: 2, due: '2026-05-01', title: 'A' }),
    ];
    const result = sortProjects(input);
    expect(result.map((p) => p.id)).toEqual(['sooner', 'later']);
  });

  it('dated items sort before undated within same priority', () => {
    const input = [
      mkProject({ id: 'undated', priority: 2, due: null, title: 'A' }),
      mkProject({ id: 'dated', priority: 2, due: '2026-07-01', title: 'Z' }),
    ];
    const result = sortProjects(input);
    expect(result.map((p) => p.id)).toEqual(['dated', 'undated']);
  });

  it('falls back to alphabetical title when priority and due are equal', () => {
    const input = [
      mkProject({ id: 'b', priority: 2, title: 'Beta' }),
      mkProject({ id: 'a', priority: 2, title: 'Alpha' }),
    ];
    const result = sortProjects(input);
    expect(result.map((p) => p.id)).toEqual(['a', 'b']);
  });

  it('does not mutate the input array', () => {
    const input = [
      mkProject({ id: 'b', priority: 3 }),
      mkProject({ id: 'a', priority: 1 }),
    ];
    const snapshot = input.map((p) => p.id);
    sortProjects(input);
    expect(input.map((p) => p.id)).toEqual(snapshot);
  });
});
