import { expect, test } from '@playwright/test'

// 공개 페이지가 뜨고, 콘솔 오류 · 우리 서버 실패 요청 · 가로 스크롤이 없는지
// admin(비밀번호 · 운영 Firebase) · quiz(배포 제외)는 뺀다
const paths = ['/', '/pokedex', '/pokedex?shiny=1', '/movedex', '/itemdex', '/entry', '/record', '/today']

for (const path of paths) {
  test(`${path} 페이지가 뜬다`, async ({ page }) => {
    const errors = []
    // 구글 통계 · 바깥 API · 글꼴은 막는다 — 우리 사이트 코드만 보고, 실제 데이터에 닿지 않게
    await page.route(/^https?:\/\/(?!localhost)/, (route) => route.abort())
    page.on('pageerror', (error) => errors.push(error.message))
    page.on('console', (message) => {
      // 실패한 요청은 아래 response 에서 주소와 함께 잡는다
      if (message.type() === 'error' && !message.text().startsWith('Failed to load resource')) errors.push(message.text())
    })
    page.on('response', (response) => {
      if (response.status() >= 400) errors.push(`${response.status()} ${response.url()}`)
    })

    const response = await page.goto(path)
    expect(response?.status()).toBe(200)
    await page.waitForLoadState('networkidle')
    await expect(page.locator('body')).toBeVisible()

    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth)
    expect(overflow, '가로 스크롤').toBeLessThanOrEqual(0)
    expect(errors, '콘솔 오류').toEqual([])
  })
}

// 도감 3종은 data/*.json 을 불러와 카드를 그린다 — 데이터가 화면까지 오는지
const dexCards = { '/': '.card-name', '/movedex': '.move-card', '/itemdex': '.item-card' }
for (const [path, selector] of Object.entries(dexCards)) {
  test(`${path} 에 데이터 카드가 그려진다`, async ({ page }) => {
    await page.route(/^https?:\/\/(?!localhost)/, (route) => route.abort())
    await page.goto(path)
    await expect(page.locator(selector).first()).toBeVisible()
  })
}
