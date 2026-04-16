import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { render, screen, fireEvent, act } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import type { Item, Project } from './api';

vi.mock('./api', () => ({
  api: {
    getConfig: vi.fn().mockResolvedValue({
      name: 'work',
      contexts: ['calls', 'computer', 'thinking'],
      areas: ['engineering', 'admin'],
      default_energy: 'medium',
    }),
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
  defer_until: null,
  waiting_on: null,
  waiting_since: null,
  order: null,
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
  sequential: true,
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
  sequential: false,
};

function renderCard(item: Item, expanded: boolean) {
  const qc = new QueryClient({
    defaultOptions: { queries: { retry: false, staleTime: Infinity } },
  });
  const onExpand = vi.fn();
  const onCollapse = vi.fn();
  const utils = render(
    <QueryClientProvider client={qc}>
      <ItemCard
        env="work"
        item={item}
        projects={[projectA, projectB]}
        expanded={expanded}
        onExpand={onExpand}
        onCollapse={onCollapse}
      />
    </QueryClientProvider>
  );
  return { ...utils, qc, onExpand, onCollapse };
}

beforeEach(() => {
  vi.mocked(api.listProjects).mockResolvedValue([projectA, projectB]);
  vi.mocked(api.updateItem).mockResolvedValue({ ...baseItem });
});

afterEach(() => {
  vi.clearAllMocks();
});

describe('ItemCard collapsed', () => {
  it('renders the current field values as chips', async () => {
    renderCard(baseItem, false);
    expect(screen.getByText('Write release notes')).toBeDefined();
    expect(screen.getByText('@calls')).toBeDefined();
    expect(screen.getByText('⚡low')).toBeDefined();
    expect(screen.getByText('15m')).toBeDefined();
  });

  it('clicking the card triggers onExpand', async () => {
    const user = userEvent.setup();
    const { onExpand } = renderCard(baseItem, false);
    await user.click(screen.getByText('Write release notes'));
    expect(onExpand).toHaveBeenCalled();
  });
});

describe('ItemCard expanded — discrete edits', () => {
  it('toggling a context chip issues a single PATCH with the new contexts', async () => {
    const user = userEvent.setup();
    renderCard(baseItem, true);
    // Wait for config query to resolve so context chips render.
    const computer = await screen.findByRole('button', { name: '@computer' });
    await user.click(computer);
    expect(api.updateItem).toHaveBeenCalledTimes(1);
    expect(api.updateItem).toHaveBeenCalledWith('work', 'item-1', {
      contexts: ['calls', 'computer'],
    });
  });

  it('clicking a project chip PATCHes the project id', async () => {
    const user = userEvent.setup();
    renderCard(baseItem, true);
    const chip = await screen.findByRole('button', { name: /📁 ihg/ });
    await user.click(chip);
    expect(api.updateItem).toHaveBeenCalledWith('work', 'item-1', {
      project: 'proj-b',
    });
  });

  it('order row is visible only when the assigned project is sequential', async () => {
    const seqItem: Item = { ...baseItem, project: 'proj-a', order: 2 };
    const { unmount } = renderCard(seqItem, true);
    await screen.findByRole('button', { name: /📁 ihg/ });
    expect(screen.getByText('order')).toBeDefined();
    unmount();

    const nonSeqItem: Item = { ...baseItem, project: 'proj-b' };
    renderCard(nonSeqItem, true);
    await screen.findByRole('button', { name: /📁 ihg/ });
    expect(screen.queryByText('order')).toBeNull();
  });

  it('switching projects sends only the project field, not order', async () => {
    const user = userEvent.setup();
    const seqItem: Item = { ...baseItem, project: 'proj-a', order: 2 };
    renderCard(seqItem, true);
    const ihgChip = await screen.findByRole('button', { name: /📁 ihg/ });
    await user.click(ihgChip);
    expect(api.updateItem).toHaveBeenCalledWith('work', 'item-1', {
      project: 'proj-b',
    });
  });
});

describe('ItemCard expanded — debounced title', () => {
  it('editing the title issues exactly one debounced PATCH after 500ms', async () => {
    renderCard(baseItem, true);
    const input = screen.getByDisplayValue(
      'Write release notes'
    ) as HTMLInputElement;
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
    renderCard(baseItem, true);
    const input = screen.getByDisplayValue(
      'Write release notes'
    ) as HTMLInputElement;
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

describe('ItemCard collapse triggers', () => {
  it('pressing Escape fires onCollapse', async () => {
    const { onCollapse } = renderCard(baseItem, true);
    screen.getByDisplayValue('Write release notes');
    fireEvent.keyDown(document, { key: 'Escape' });
    expect(onCollapse).toHaveBeenCalled();
  });

  it('click outside the card fires onCollapse', async () => {
    const { onCollapse } = renderCard(baseItem, true);
    screen.getByDisplayValue('Write release notes');
    fireEvent.mouseDown(document.body);
    expect(onCollapse).toHaveBeenCalled();
  });

  it('Cmd+Enter in the title flushes pending edits and collapses', async () => {
    const { onCollapse } = renderCard(baseItem, true);
    const input = screen.getByDisplayValue(
      'Write release notes'
    ) as HTMLInputElement;
    fireEvent.change(input, { target: { value: 'Pending title' } });
    fireEvent.keyDown(input, { key: 'Enter', metaKey: true });
    expect(onCollapse).toHaveBeenCalled();
    expect(api.updateItem).toHaveBeenCalledWith('work', 'item-1', {
      title: 'Pending title',
    });
  });

  it('Ctrl+Enter in the notes textarea flushes and collapses', async () => {
    const { onCollapse } = renderCard(baseItem, true);
    const textarea = screen.getByPlaceholderText(
      /Notes/i
    ) as HTMLTextAreaElement;
    fireEvent.change(textarea, { target: { value: 'Draft notes' } });
    fireEvent.keyDown(textarea, { key: 'Enter', ctrlKey: true });
    expect(onCollapse).toHaveBeenCalled();
    expect(api.updateItem).toHaveBeenCalledWith('work', 'item-1', {
      body: 'Draft notes',
    });
  });
});
