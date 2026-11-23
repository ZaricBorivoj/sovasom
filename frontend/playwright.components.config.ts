import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests/components',
  workers: 2,
  forbidOnly: !!process.env.CI,
  snapshotPathTemplate: '{testDir}/__screenshots__/{projectName}/{arg}{ext}',
  use: { baseURL: 'http://127.0.0.1:6006', browserName: 'chromium' },
  webServer: {
    command: process.env.STORYBOOK_STATIC
      ? 'node ../scripts/serve-storybook.mjs'
      : 'npm run storybook',
    url: 'http://127.0.0.1:6006',
    reuseExistingServer: !process.env.CI,
    timeout: 120000,
  },
  projects: [
    { name: 'desktop', use: { viewport: { width: 1440, height: 1000 } } },
    { name: 'phone', use: { viewport: { width: 390, height: 844 } } },
  ],
});
