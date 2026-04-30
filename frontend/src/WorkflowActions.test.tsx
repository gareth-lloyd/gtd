import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MemoryRouter } from 'react-router-dom';
import type { Item } from './api';

vi.mock('./api', () => ({
  api: {
    moveItem: vi.fn(),
    completeItem: vi.fn(),
    deleteItem: vi.fn(),
    purgeItem: vi.fn(),
  },
}));

import { api } from './api';
import { SelectionProvider } from './SelectionContext';
import { WorkflowActions } from './WorkflowActions';

const nextItem: Item = {
  id: 'item-1',
  title: 'Write release notes',
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
};

function renderActions(item: Item) {
  const qc = new QueryClient({
    defaultOptions: {
      queries: { retry: false, staleTime: Infinity },
      mutations: { retry: false },
    },
  });
  const utils = render(
    <QueryClientProvider client={qc}>
      <MemoryRouter initialEntries={['/work/next']}>
        <SelectionProvider>
          <WorkflowActions env="work" item={item} />
        </SelectionProvider>
      </MemoryRouter>
    </QueryClientProvider>
  );
  return { ...utils, qc };
}

beforeEach(() => {
  vi.mocked(api.moveItem).mockResolvedValue({ ...nextItem });
  vi.mocked(api.completeItem).mockResolvedValue({ ...nextItem, status: 'archive' });
  vi.mocked(api.deleteItem).mockResolvedValue({ ...nextItem, status: 'trash' });
  vi.mocked(api.purgeItem).mockResolvedValue(undefined as unknown as void);
});

afterEach(() => {
  vi.clearAllMocks();
});

describe('WorkflowActions — next bucket', () => {
  it('renders move buttons for waiting and someday (but not current bucket)', () => {
    renderActions(nextItem);
    expect(screen.getByRole('button', { name: /→ waiting/ })).toBeDefined();
    expect(screen.getByRole('button', { name: /→ someday/ })).toBeDefined();
    // Current bucket is next — no "→ next" button should appear
    expect(screen.queryByRole('button', { name: /→ next$/ })).toBeNull();
  });

  it('clicking "→ waiting" calls moveItem with waiting', async () => {
    const user = userEvent.setup();
    renderActions(nextItem);
    await user.click(screen.getByRole('button', { name: /→ waiting/ }));
    await waitFor(() => {
      expect(api.moveItem).toHaveBeenCalledWith('work', 'item-1', 'waiting');
    });
  });

  it('clicking "→ someday" calls moveItem with someday', async () => {
    const user = userEvent.setup();
    renderActions(nextItem);
    await user.click(screen.getByRole('button', { name: /→ someday/ }));
    await waitFor(() => {
      expect(api.moveItem).toHaveBeenCalledWith('work', 'item-1', 'someday');
    });
  });

  it('clicking "✓ done" calls completeItem', async () => {
    const user = userEvent.setup();
    renderActions(nextItem);
    await user.click(screen.getByRole('button', { name: /✓ done/ }));
    await waitFor(() => {
      expect(api.completeItem).toHaveBeenCalledWith('work', 'item-1');
    });
  });

  it('clicking "Delete" soft-deletes (deleteItem)', async () => {
    const user = userEvent.setup();
    renderActions(nextItem);
    await user.click(screen.getByRole('button', { name: /^Delete$/ }));
    await waitFor(() => {
      expect(api.deleteItem).toHaveBeenCalledWith('work', 'item-1');
    });
    // Soft-delete should NOT call purge.
    expect(api.purgeItem).not.toHaveBeenCalled();
  });
});

describe('WorkflowActions — inbox bucket', () => {
  it('offers next/waiting/someday as move options', () => {
    renderActions({ ...nextItem, status: 'inbox' });
    expect(screen.getByRole('button', { name: /→ next/ })).toBeDefined();
    expect(screen.getByRole('button', { name: /→ waiting/ })).toBeDefined();
    expect(screen.getByRole('button', { name: /→ someday/ })).toBeDefined();
  });
});

describe('WorkflowActions — archive bucket', () => {
  it('hides move buttons and the complete button (item is already done)', () => {
    renderActions({ ...nextItem, status: 'archive' });
    expect(screen.queryByRole('button', { name: /→/ })).toBeNull();
    expect(screen.queryByRole('button', { name: /✓ done/ })).toBeNull();
    // Still offers soft delete.
    expect(screen.getByRole('button', { name: /^Delete$/ })).toBeDefined();
  });
});

describe('WorkflowActions — trash bucket', () => {
  it('shows restore and purge (not the normal actions)', () => {
    renderActions({ ...nextItem, status: 'trash' });
    expect(screen.getByRole('button', { name: /↺ restore/ })).toBeDefined();
    expect(screen.getByRole('button', { name: /Purge/ })).toBeDefined();
    expect(screen.queryByRole('button', { name: /→ waiting/ })).toBeNull();
    expect(screen.queryByRole('button', { name: /✓ done/ })).toBeNull();
  });

  it('restore calls moveItem with inbox', async () => {
    const user = userEvent.setup();
    renderActions({ ...nextItem, status: 'trash' });
    await user.click(screen.getByRole('button', { name: /↺ restore/ }));
    await waitFor(() => {
      expect(api.moveItem).toHaveBeenCalledWith('work', 'item-1', 'inbox');
    });
  });

  it('purge calls purgeItem after confirm', async () => {
    const user = userEvent.setup();
    const confirmSpy = vi.spyOn(window, 'confirm').mockReturnValue(true);
    renderActions({ ...nextItem, status: 'trash' });
    await user.click(screen.getByRole('button', { name: /Purge/ }));
    await waitFor(() => {
      expect(api.purgeItem).toHaveBeenCalledWith('work', 'item-1');
    });
    confirmSpy.mockRestore();
  });

  it('purge does nothing when the user cancels the confirm prompt', async () => {
    const user = userEvent.setup();
    const confirmSpy = vi.spyOn(window, 'confirm').mockReturnValue(false);
    renderActions({ ...nextItem, status: 'trash' });
    await user.click(screen.getByRole('button', { name: /Purge/ }));
    // Give any pending promise queues a tick to drain before asserting.
    await new Promise((resolve) => setTimeout(resolve, 0));
    expect(api.purgeItem).not.toHaveBeenCalled();
    confirmSpy.mockRestore();
  });
});

describe('WorkflowActions — busy state disables siblings', () => {
  it('disables all buttons while a mutation is pending', async () => {
    const user = userEvent.setup();
    // Never-resolving promise keeps the mutation in the pending state.
    let resolveMove: ((v: Item) => void) | undefined;
    vi.mocked(api.moveItem).mockReturnValue(
      new Promise<Item>((resolve) => {
        resolveMove = resolve;
      })
    );
    renderActions(nextItem);
    await user.click(screen.getByRole('button', { name: /→ waiting/ }));

    // All buttons should be disabled while pending.
    await waitFor(() => {
      const deleteBtn = screen.getByRole('button', { name: /^Delete$/ });
      expect(deleteBtn).toHaveProperty('disabled', true);
    });
    const somedayBtn = screen.getByRole('button', { name: /→ someday/ });
    expect(somedayBtn).toHaveProperty('disabled', true);
    const doneBtn = screen.getByRole('button', { name: /✓ done/ });
    expect(doneBtn).toHaveProperty('disabled', true);

    // Resolve the pending promise so we don't leak.
    resolveMove?.({ ...nextItem });
  });
});
