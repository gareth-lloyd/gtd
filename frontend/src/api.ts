export type Bucket =
  | 'inbox'
  | 'next'
  | 'waiting'
  | 'someday'
  | 'reference'
  | 'archive'
  | 'trash';
export type Energy = 'low' | 'medium' | 'high';
export type ProjectStatus = 'active' | 'on_hold' | 'complete' | 'dropped';

export interface Item {
  id: string;
  title: string;
  body: string;
  created: string;
  updated: string;
  status: Bucket;
  contexts: string[];
  energy: Energy | null;
  time_minutes: number | null;
  project: string | null;
  area: string | null;
  tags: string[];
  due: string | null;
  defer_until: string | null;
  waiting_on: string | null;
  waiting_since: string | null;
}

export interface Project {
  id: string;
  title: string;
  body: string;
  created: string;
  updated: string;
  status: ProjectStatus;
  outcome: string | null;
  area: string | null;
  tags: string[];
}

export interface EnvConfig {
  name: string;
  contexts: string[];
  areas: string[];
  default_energy: Energy;
}

export interface EnvSummary {
  name: string;
}

export interface SnapshotStatus {
  dirty_count: number;
  dirty_files: string[];
}

export interface SnapshotResult {
  committed: boolean;
  sha: string | null;
  files_changed: number;
  message: string;
  pushed: boolean;
}

const API_BASE = '/api';

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...init,
  });
  if (!res.ok) {
    let message = `${res.status} ${res.statusText}`;
    try {
      const body = await res.json();
      if (body.error) message = body.error;
    } catch {
      // body not JSON, keep status line
    }
    throw new Error(message);
  }
  if (res.status === 204) return null as T;
  return res.json();
}

export const api = {
  listEnvs: () => request<EnvSummary[]>('/envs/'),
  getConfig: (env: string) => request<EnvConfig>(`/envs/${env}/config/`),

  listItems: (env: string, params: Record<string, string> = {}) => {
    const qs = new URLSearchParams(params).toString();
    return request<Item[]>(`/envs/${env}/items/${qs ? '?' + qs : ''}`);
  },
  getItem: (env: string, id: string) =>
    request<Item>(`/envs/${env}/items/${id}/`),
  captureItem: (env: string, title: string, body = '') =>
    request<Item>(`/envs/${env}/items/`, {
      method: 'POST',
      body: JSON.stringify({ title, body }),
    }),
  updateItem: (env: string, id: string, patch: Record<string, unknown>) =>
    request<Item>(`/envs/${env}/items/${id}/`, {
      method: 'PATCH',
      body: JSON.stringify(patch),
    }),
  moveItem: (env: string, id: string, to: Bucket) =>
    request<Item>(`/envs/${env}/items/${id}/move/`, {
      method: 'POST',
      body: JSON.stringify({ to }),
    }),
  completeItem: (env: string, id: string) =>
    request<Item>(`/envs/${env}/items/${id}/complete/`, { method: 'POST' }),
  deleteItem: (env: string, id: string) =>
    request<Item>(`/envs/${env}/items/${id}/`, { method: 'DELETE' }),
  purgeItem: (env: string, id: string) =>
    request<void>(`/envs/${env}/items/${id}/purge/`, { method: 'POST' }),

  listProjects: (env: string) =>
    request<Project[]>(`/envs/${env}/projects/`),
  getProject: (env: string, id: string) =>
    request<{ project: Project; actions: Item[] }>(
      `/envs/${env}/projects/${id}/`
    ),
  createProject: (
    env: string,
    data: { id: string; title: string; body?: string; outcome?: string; area?: string }
  ) =>
    request<Project>(`/envs/${env}/projects/`, {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  snapshotStatus: () => request<SnapshotStatus>('/snapshot/status/'),
  snapshot: (message?: string, push = false) =>
    request<SnapshotResult>('/snapshot/', {
      method: 'POST',
      body: JSON.stringify({ message, push }),
    }),
};
