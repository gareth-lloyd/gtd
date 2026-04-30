import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { render, screen, fireEvent, act, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MemoryRouter } from 'react-router-dom';
import type { Item, Project } from './api';

vi.mock('./api', () => ({
  api: {
    getConfig: vi.fn().mockResolvedValue({
      name: 'work',
      contexts: ['calls', 'computer', 'thinking'],
      areas: ['engineering', 'admin'],
      default_energy: 'medium',
    }),
    getItem: vi.fn(),
    listProjects: vi.fn(),
    updateItem: vi.fn(),
    moveItem: vi.fn(),
    completeItem: vi.fn(),
    deleteItem: vi.fn(),
    purgeItem: vi.fn(),
  },
}));

import { api } from './api';
import { ItemCard } from './ItemCard';
import { SelectionProvider } from './SelectionContext';

const baseItem: Item = {
  id: 'item-1',
  title: 'Write release notes',
  body: '',
  created: '2026-04-10T09:00:00',
  updated: '2026-04-10T09:00:00',
  status: 'next',
  contexts: ['calls'],
  energy: 'low',
  time_minutes: 15,
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
};

const projectA: Project = {
  id: 'proj-a',
  title: 'ship',
  body: '',
  created: '2026-04-01T09:00:00',
  updated: '2026-04-01T09:00:00',
  status: 'active',
  outcome: null,
  area: null,
  tags: [],
  due: null,
  priority: 1,
  max_next_items: 1,
};

const projectB: Project = {
  id: 'proj-b',
  title: 'ihg',
  body: '',
  created: '2026-04-01T09:00:00',
  updated: '2026-04-01T09:00:00',
  status: 'active',
  outcome: null,
  area: null,
  tags: [],
  due: null,
  priority: 3,
  max_next_items: null,
};

function renderCard(item: Item) {
  const qc = new QueryClient({
    defaultOptions: { queries: { retry: false, staleTime: Infinity } },
  });
  const utils = render(
    <QueryClientProvider client={qc}>
      <MemoryRouter initialEntries={['/work/next']}>
        <SelectionProvider>
          <ItemCard
            env="work"
            item={item}
            projects={[projectA, projectB]}
          />
        </SelectionProvider>
      </MemoryRouter>
    </QueryClientProvider>
  );
  return { ...utils, qc };
}

beforeEach(() => {
  vi.mocked(api.listProjects).mockResolvedValue([projectA, projectB]);
  vi.mocked(api.updateItem).mockResolvedValue({ ...baseItem });
  vi.mocked(api.getItem).mockResolvedValue({ ...baseItem });
});

afterEach(() => {
  vi.clearAllMocks();
});

describe('ItemCard collapsed', () => {
  it('renders the current field values as chips', async () => {
    renderCard(baseItem);
    expect(screen.getByText('Write release notes')).toBeDefined();
    expect(screen.getByText('@calls')).toBeDefined();
    expect(screen.getByText('⚡low')).toBeDefined();
    expect(screen.getByText('15m')).toBeDefined();
  });

  it('renders no due chip when item has no due date', () => {
    const { container } = renderCard(baseItem);
    expect(container.querySelector('.chip-overdue')).toBeNull();
    expect(container.textContent).not.toContain('due ');
  });

  it('renders neutral due chip when not overdue', () => {
    const { container } = renderCard({ ...baseItem, due: '2099-01-01', overdue: false });
    const chip = Array.from(container.querySelectorAll('.chip')).find((el) =>
      el.textContent?.includes('due 2099-01-01'),
    );
    expect(chip).toBeDefined();
    expect(chip!.classList.contains('chip-overdue')).toBe(false);
  });

  it('renders overdue chip with .chip-overdue when overdue', () => {
    const { container } = renderCard({ ...baseItem, due: '2020-01-01', overdue: true });
    const chip = Array.from(container.querySelectorAll('.chip')).find((el) =>
      el.textContent?.includes('due 2020-01-01'),
    );
    expect(chip).toBeDefined();
    expect(chip!.classList.contains('chip-overdue')).toBe(true);
  });

  it('clicking the card selects it and shows title input', async () => {
    const user = userEvent.setup();
    renderCard(baseItem);
    await user.click(screen.getByText('Write release notes'));
    // After selection, the title input should appear
    expect(screen.getByDisplayValue('Write release notes')).toBeDefined();
  });
});

describe('ItemCard selected — debounced title', () => {
  it('editing the title issues exactly one debounced PATCH after 500ms', async () => {
    const user = userEvent.setup();
    renderCard(baseItem);
    // Select the card first
    await user.click(screen.getByText('Write release notes'));

    const input = screen.getByDisplayValue('Write release notes') as HTMLInputElement;
    vi.useFakeTimers();
    try {
      fireEvent.change(input, { target: { value: 'Updated title' } });
      expect(api.updateItem).not.toHaveBeenCalled();
      act(() => {
        vi.advanceTimersByTime(499);
      });
      expect(api.updateItem).not.toHaveBeenCalled();
      act(() => {
        vi.advanceTimersByTime(1);
      });
      expect(api.updateItem).toHaveBeenCalledTimes(1);
      expect(api.updateItem).toHaveBeenCalledWith('work', 'item-1', {
        title: 'Updated title',
      });
    } finally {
      vi.useRealTimers();
    }
  });

  it('multiple rapid edits before the debounce window coalesce into one PATCH', async () => {
    const user = userEvent.setup();
    renderCard(baseItem);
    await user.click(screen.getByText('Write release notes'));

    const input = screen.getByDisplayValue('Write release notes') as HTMLInputElement;
    vi.useFakeTimers();
    try {
      fireEvent.change(input, { target: { value: 'A' } });
      fireEvent.change(input, { target: { value: 'AB' } });
      fireEvent.change(input, { target: { value: 'ABC' } });
      act(() => {
        vi.advanceTimersByTime(500);
      });
      expect(api.updateItem).toHaveBeenCalledTimes(1);
      expect(api.updateItem).toHaveBeenCalledWith('work', 'item-1', {
        title: 'ABC',
      });
    } finally {
      vi.useRealTimers();
    }
  });
});

describe('ItemCard URL link chips', () => {
  it('keeps URL link chips visible below the editor when the card is selected', async () => {
    const user = userEvent.setup();
    const withUrl: Item = {
      ...baseItem,
      body: 'see https://example.com/foo for context',
    };
    const { container } = renderCard(withUrl);

    // Visible while collapsed (the chip — the markdown body also renders an
    // anchor for the URL, so query by the chip class explicitly)
    expect(container.querySelector('.link-chip')).not.toBeNull();

    await user.click(screen.getByText('Write release notes'));

    expect(screen.getByDisplayValue('Write release notes')).toBeDefined();
    const chip = container.querySelector('.link-chip') as HTMLAnchorElement | null;
    expect(chip).not.toBeNull();
    expect(chip!.getAttribute('href')).toBe('https://example.com/foo');
  });

  it('reflects newly-typed URLs in the body textarea immediately', async () => {
    const user = userEvent.setup();
    const { container } = renderCard(baseItem);
    await user.click(screen.getByText('Write release notes'));

    const textarea = screen.getByPlaceholderText(/Notes/i) as HTMLTextAreaElement;
    fireEvent.change(textarea, {
      target: { value: 'check https://newsite.test/x' },
    });
    const chip = container.querySelector('.link-chip') as HTMLAnchorElement | null;
    expect(chip).not.toBeNull();
    expect(chip!.getAttribute('href')).toBe('https://newsite.test/x');
  });
});

describe('ItemCard scheduled readonly mode', () => {
  function localIso(offsetMs: number): string {
    // Produce a local-time ISO-like string matching what our backend emits.
    const d = new Date(Date.now() + offsetMs);
    const pad = (n: number) => String(n).padStart(2, '0');
    return (
      `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}` +
      `T${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`
    );
  }

  it('selecting a scheduled item renders a readonly view with an Edit button', async () => {
    const user = userEvent.setup();
    const scheduled: Item = { ...baseItem, defer_until: localIso(60 * 60 * 1000) };
    renderCard(scheduled);
    await user.click(screen.getByText('Write release notes'));

    // No editable inputs for title/body
    expect(screen.queryByDisplayValue('Write release notes')).toBeNull();
    expect(screen.queryByPlaceholderText(/Notes/i)).toBeNull();
    // Edit button is present
    const editButton = screen.getByRole('button', { name: /Edit scheduled item/i });
    expect(editButton).toBeDefined();

    // Clicking Edit reveals the inputs
    await user.click(editButton);
    expect(screen.getByDisplayValue('Write release notes')).toBeDefined();
  });

  it('a non-scheduled item (past defer_until) stays editable on selection', async () => {
    const user = userEvent.setup();
    const notScheduled: Item = { ...baseItem, defer_until: localIso(-60 * 60 * 1000) };
    renderCard(notScheduled);
    await user.click(screen.getByText('Write release notes'));

    expect(screen.getByDisplayValue('Write release notes')).toBeDefined();
    expect(
      screen.queryByRole('button', { name: /Edit scheduled item/i })
    ).toBeNull();
  });
});

describe('ItemCard deselect triggers', () => {
  it('Cmd+Enter in the title flushes pending edits and deselects', async () => {
    const user = userEvent.setup();
    renderCard(baseItem);
    await user.click(screen.getByText('Write release notes'));

    const input = screen.getByDisplayValue('Write release notes') as HTMLInputElement;
    fireEvent.change(input, { target: { value: 'Pending title' } });
    fireEvent.keyDown(input, { key: 'Enter', metaKey: true });
    expect(api.updateItem).toHaveBeenCalledWith('work', 'item-1', {
      title: 'Pending title',
    });
    // After Cmd+Enter, the card should deselect — title input gone, collapsed view shows
    await waitFor(() => {
      expect(screen.queryByDisplayValue('Pending title')).toBeNull();
    });
  });

  it('Ctrl+Enter in the notes textarea flushes and deselects', async () => {
    const user = userEvent.setup();
    renderCard(baseItem);
    await user.click(screen.getByText('Write release notes'));

    const textarea = screen.getByPlaceholderText(/Notes/i) as HTMLTextAreaElement;
    fireEvent.change(textarea, { target: { value: 'Draft notes' } });
    fireEvent.keyDown(textarea, { key: 'Enter', ctrlKey: true });
    expect(api.updateItem).toHaveBeenCalledWith('work', 'item-1', {
      body: 'Draft notes',
    });
  });
});
