import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MemoryRouter } from 'react-router-dom';
import App from './App';

// Mock the API module so we don't need a running backend
vi.mock('./api', () => ({
  api: {
    listEnvs: vi.fn().mockResolvedValue([{ name: 'work' }]),
    getConfig: vi.fn().mockResolvedValue({
      name: 'work',
      contexts: ['calls', 'computer', 'errands'],
      areas: ['engineering'],
      default_energy: 'medium',
    }),
    listItems: vi.fn().mockResolvedValue([
      {
        id: 'test-1',
        title: 'Test item',
        body: '',
        created: '2026-04-10T09:00:00',
        updated: '2026-04-10T09:00:00',
        status: 'next',
        contexts: ['calls', 'computer'],
        energy: 'low',
        time_minutes: 5,
        project: null,
        area: null,
        tags: [],
        due: null,
        defer_until: null,
        waiting_on: null,
        waiting_since: null,
      },
    ]),
    snapshotStatus: vi.fn().mockResolvedValue({ dirty_count: 0, dirty_files: [] }),
    listProjects: vi.fn().mockResolvedValue([]),
    listSearchCorpus: vi.fn().mockResolvedValue({ items: [], projects: [] }),
  },
}));

function renderApp(initialEntry = '/work/next') {
  const qc = new QueryClient({
    defaultOptions: {
      queries: { retry: false, staleTime: Infinity },
    },
  });
  return render(
    <QueryClientProvider client={qc}>
      <MemoryRouter initialEntries={[initialEntry]}>
        <App />
      </MemoryRouter>
    </QueryClientProvider>
  );
}

describe('Context colors in the UI', () => {
  beforeEach(() => {
    localStorage.setItem('gtd:env', 'work');
  });

  it('renders context chips with colored backgrounds on items', async () => {
    renderApp();
    // Wait for the item to appear
    const item = await screen.findByText('Test item');
    const card = item.closest('.item')! as HTMLElement;

    const chips = within(card).getAllByText(/@(calls|computer)/);
    expect(chips.length).toBe(2);

    for (const chip of chips) {
      const bg = chip.style.backgroundColor;
      // JSDOM normalizes hsl() to rgb(); check it has a color at all
      expect(bg).toMatch(/rgb/);
    }
  });

  it('context chips for different contexts have different colors', async () => {
    renderApp();
    const item = await screen.findByText('Test item');
    const card = item.closest('.item')! as HTMLElement;

    const callsChip = within(card).getByText('@calls');
    const computerChip = within(card).getByText('@computer');
    expect(callsChip.style.backgroundColor).not.toBe(
      computerChip.style.backgroundColor
    );
  });

  it('app background tints when a context filter is checked', async () => {
    const user = userEvent.setup();
    renderApp();

    // Wait for filter panel to load (contexts come from config query)
    const checkbox = await screen.findByRole('checkbox', { name: /@calls/ });
    const appEl = document.querySelector('.app')! as HTMLElement;

    // Before: no inline background
    expect(appEl.getAttribute('style')).toBeNull();

    // Check the calls context filter
    await user.click(checkbox);

    // After: app should have an inline background-color
    const style = appEl.getAttribute('style') || '';
    expect(style).toContain('background-color');
  });

  it('app background resets when all context filters are cleared', async () => {
    const user = userEvent.setup();
    renderApp();

    const checkbox = await screen.findByRole('checkbox', { name: /@calls/ });
    await user.click(checkbox); // select
    await user.click(checkbox); // deselect

    const appEl = document.querySelector('.app')! as HTMLElement;
    // Style should be empty or not contain background-color
    const style = appEl.getAttribute('style') || '';
    expect(style).not.toContain('background-color');
  });

  it('filter panel checkboxes have colored left borders', async () => {
    renderApp();

    const checkbox = await screen.findByRole('checkbox', { name: /@calls/ });
    const row = checkbox.closest('.check-row') as HTMLElement;
    expect(row).not.toBeNull();
    // Should have a colored left border via inline style
    expect(row.style.borderLeft).toMatch(/rgb/);
  });
});

describe('Project priority on next view', () => {
  beforeEach(() => {
    localStorage.setItem('gtd:env', 'work');
  });

  it('renders a P1 badge on an item whose project is P1', async () => {
    const { api } = await import('./api');
    (api.listItems as ReturnType<typeof vi.fn>).mockResolvedValueOnce([
      {
        id: 'p1-task',
        title: 'Urgent task',
        body: '',
        created: '2026-04-10T09:00:00',
        updated: '2026-04-10T09:00:00',
        status: 'next',
        contexts: [],
        energy: null,
        time_minutes: null,
        project: 'p1proj',
        project_priority: 1,
        area: null,
        tags: [],
        due: null,
        defer_until: null,
        waiting_on: null,
        waiting_since: null,
        order: null,
      },
    ]);

    renderApp();
    const title = await screen.findByText('Urgent task');
    const card = title.closest('.item')! as HTMLElement;
    const badge = within(card).getByText('P1');
    expect(badge.className).toContain('priority-badge');
    expect(badge.className).toContain('p1');
  });

  it('omits the badge when the item has no project_priority', async () => {
    const { api } = await import('./api');
    (api.listItems as ReturnType<typeof vi.fn>).mockResolvedValueOnce([
      {
        id: 'floating',
        title: 'Floating task',
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
        defer_until: null,
        waiting_on: null,
        waiting_since: null,
        order: null,
      },
    ]);

    renderApp();
    const title = await screen.findByText('Floating task');
    const card = title.closest('.item')! as HTMLElement;
    expect(within(card).queryByText(/^P[1-5]$/)).toBeNull();
  });
});

describe('Search', () => {
  beforeEach(() => {
    localStorage.setItem('gtd:env', 'work');
  });

  it('renders the header search input', async () => {
    renderApp();
    const input = await screen.findByPlaceholderText(/search/i);
    expect(input).toBeDefined();
  });

  it('renders the search page at /work/search?q=foo', async () => {
    renderApp('/work/search?q=foo');
    const inputs = await screen.findAllByPlaceholderText(/search/i);
    // header search + page search input
    expect(inputs.length).toBeGreaterThanOrEqual(1);
  });
});
