import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const HERE = path.dirname(fileURLToPath(import.meta.url));

export const E2E_ENV = "e2e";

const BUCKETS = [
  "inbox",
  "next",
  "waiting",
  "someday",
  "reference",
  "projects",
  "archive",
  "trash",
  "templates",
];

const CONFIG_YAML = `name: ${E2E_ENV}
contexts: [calls, computer, errands, office]
areas: [engineering, admin]
default_energy: medium
`;

export const STUB_AI_RESPONSE = {
  title: "Email Jane about Q2 roadmap",
  summary: "Filed to inbox — ready to triage",
  body: null,
  energy: "medium",
  time_minutes: 10,
  contexts: ["computer"],
  area: null,
  project_query: null,
  due: null,
  defer_until: null,
} as const;

export function tmpDataRoot(): string {
  return path.resolve(HERE, ".tmp", "data");
}

export function envRoot(): string {
  return path.join(tmpDataRoot(), E2E_ENV);
}

export function resetEnvFiles(): void {
  const root = envRoot();
  for (const bucket of BUCKETS) {
    const dir = path.join(root, bucket);
    fs.rmSync(dir, { recursive: true, force: true });
    fs.mkdirSync(dir, { recursive: true });
  }
}

export default async function globalSetup() {
  const root = envRoot();
  fs.mkdirSync(root, { recursive: true });
  for (const bucket of BUCKETS) {
    fs.mkdirSync(path.join(root, bucket), { recursive: true });
  }
  fs.writeFileSync(path.join(root, "config.yml"), CONFIG_YAML);
}
