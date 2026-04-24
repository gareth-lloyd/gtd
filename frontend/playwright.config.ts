import { defineConfig } from '@playwright/test';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { STUB_AI_RESPONSE } from './e2e/global-setup';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = path.resolve(HERE, '..');
const TMP_DATA_ROOT = path.join(HERE, 'e2e', '.tmp', 'data');

// Dedicated e2e port to avoid colliding with the dev server on 8765.
const PORT = 8766;

export default defineConfig({
  testDir: './e2e',
  testMatch: /.*\.spec\.ts$/,
  fullyParallel: false,
  workers: 1,
  retries: 0,
  reporter: [['list']],
  globalSetup: './e2e/global-setup.ts',
  use: {
    baseURL: `http://localhost:${PORT}`,
    trace: 'retain-on-failure',
    launchOptions: {
      slowMo: process.env.PW_SLOWMO ? Number(process.env.PW_SLOWMO) : 0,
    },
  },
  webServer: {
    command: `uv run manage.py runserver ${PORT} --noreload`,
    cwd: PROJECT_ROOT,
    url: `http://localhost:${PORT}/api/envs/`,
    reuseExistingServer: !process.env.CI,
    timeout: 30_000,
    env: {
      GTD_DATA_ROOT: TMP_DATA_ROOT,
      GTD_AI_STUB_RESPONSE: JSON.stringify(STUB_AI_RESPONSE),
    },
  },
});
