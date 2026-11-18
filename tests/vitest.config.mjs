import { defineConfig } from 'vitest/config'

// 단위 테스트는 tests/unit 아래 *.test.mjs 만. 화면 흐름은 tests/e2e (Playwright)
export default defineConfig({
  test: { include: ['unit/**/*.test.mjs'], environment: 'node' },
})
