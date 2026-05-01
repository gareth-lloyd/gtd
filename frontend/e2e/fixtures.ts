import { test as base, expect } from "@playwright/test";
import type { Energy } from "../src/api";
import { E2E_ENV, envRoot, resetEnvFiles } from "./global-setup";

export const ENV = E2E_ENV;
export const BASE_URL = "http://localhost:8766";

async function api<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE_URL}/api${path}`, {
    headers: { "Content-Type": "application/json", ...(init?.headers || {}) },
    ...init,
  });
  if (!res.ok) {
    throw new Error(`API ${path} failed: ${res.status} ${await res.text()}`);
  }
  return res.json() as Promise<T>;
}

export async function seedProject(input: {
  id: string;
  title: string;
  outcome?: string | null;
  area?: string | null;
  priority?: number | null;
  max_next_items?: number | null;
}): Promise<void> {
  await api(`/envs/${ENV}/projects/`, {
    method: "POST",
    body: JSON.stringify({
      id: input.id,
      title: input.title,
      body: "",
      outcome: input.outcome ?? null,
      area: input.area ?? null,
      tags: [],
      due: null,
      priority: input.priority ?? null,
      max_next_items: input.max_next_items ?? null,
    }),
  });
}

export async function seedItemInNext(input: {
  title: string;
  project?: string | null;
  contexts?: string[];
  energy?: Energy;
}): Promise<{ id: string }> {
  const item = await api<{ id: string }>(`/envs/${ENV}/items/`, {
    method: "POST",
    body: JSON.stringify({
      title: input.title,
      body: "",
      energy: input.energy ?? "medium",
      time_minutes: null,
      contexts: input.contexts ?? [],
    }),
  });
  if (input.project) {
    await api(`/envs/${ENV}/items/${item.id}/`, {
      method: "PATCH",
      body: JSON.stringify({ project: input.project }),
    });
  }
  await api(`/envs/${ENV}/items/${item.id}/move/`, {
    method: "POST",
    body: JSON.stringify({ to: "next" }),
  });
  return item;
}

export async function listNextItems(): Promise<Array<{ id: string; title: string }>> {
  return api(`/envs/${ENV}/items/?status=next&show_all=true`);
}

export const test = base.extend<{ autoReset: void }>({
  autoReset: [
    // eslint-disable-next-line no-empty-pattern -- Playwright fixture introspection requires destructuring even when no fixtures are used.
    async ({}, use) => {
      resetEnvFiles();
      await use();
    },
    { auto: true },
  ],
});

export { envRoot };

export { expect };
