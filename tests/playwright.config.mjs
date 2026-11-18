import { defineConfig, devices } from '@playwright/test'

// 배정 포트(4100) + 50. 다른 프로젝트 검증과 겹치지 않게 고정
const port = Number(process.env.E2E_PORT ?? 4150)

export default defineConfig({
  testDir: 'e2e',
  fullyParallel: true,
  reporter: 'line',
  outputDir: '../logs/e2e-results',
  use: { baseURL: `http://localhost:${port}` },
  projects: [
    { name: 'pc', use: { ...devices['Desktop Chrome'] } },
    { name: 'phone', use: { ...devices['Desktop Chrome'], viewport: { width: 390, height: 844 } } },
  ],
  webServer: {
    command: `node serve.mjs ${port}`,
    port,
    reuseExistingServer: false,
    timeout: 30_000,
  },
})
