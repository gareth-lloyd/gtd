// Slim API client for the mobile capture app. Talks to the locked cloud
// surface (gtd_api.urls_mobile): list envs, read inbox, read next, capture.
//
// The shared-secret passphrase can't be baked into this public bundle, so the
// user types it once; we stash it in localStorage and send it as X-GTD-Token
// on every request. A 401 clears the stored token so the app re-prompts.

const TOKEN_KEY = "gtd:token";

export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY);
}

export function setToken(token: string): void {
  localStorage.setItem(TOKEN_KEY, token);
}

export function clearToken(): void {
  localStorage.removeItem(TOKEN_KEY);
}

export class UnauthorizedError extends Error {
  constructor() {
    super("unauthorized");
    this.name = "UnauthorizedError";
  }
}

export function errorMessage(err: unknown): string {
  return err instanceof Error ? err.message : "Something went wrong";
}

export interface Item {
  id: string;
  title: string;
  body: string;
  contexts: string[];
  energy: "low" | "medium" | "high" | null;
  time_minutes: number | null;
  project: string | null;
  project_priority: number | null;
  due: string | null;
  overdue: boolean;
  status: string;
}

export interface EnvName {
  name: string;
}

async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
  const token = getToken();
  const headers = new Headers(init.headers);
  if (token) headers.set("X-GTD-Token", token);
  if (init.body) headers.set("Content-Type", "application/json");

  const res = await fetch(`/api${path}`, { ...init, headers });
  if (res.status === 401) {
    clearToken();
    throw new UnauthorizedError();
  }
  if (!res.ok) {
    let detail = `${res.status}`;
    try {
      const body = await res.json();
      if (body?.error) detail = body.error;
    } catch {
      // non-JSON error body — keep the status code
    }
    throw new Error(detail);
  }
  if (res.status === 204) return undefined as T;
  return res.json() as Promise<T>;
}

export function listEnvs(): Promise<EnvName[]> {
  return request<EnvName[]>("/envs/");
}

export function listInbox(env: string): Promise<Item[]> {
  return request<Item[]>(`/envs/${env}/inbox/`);
}

export function listNext(env: string): Promise<Item[]> {
  return request<Item[]>(`/envs/${env}/next/`);
}

// capture echoes the created item plus `synced`: false means the item was
// saved locally on the server but not yet pushed to GitHub (so not durable).
export type CaptureResult = Item & { synced: boolean };

export function capture(env: string, title: string, body = ""): Promise<CaptureResult> {
  return request<CaptureResult>(`/envs/${env}/capture/`, {
    method: "POST",
    body: JSON.stringify({ title, body }),
  });
}
