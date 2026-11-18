import { describe, expect, it } from 'vitest'
import { readText } from './helpers.mjs'

// index.html 은 pokedex.html 의 자동 생성 사본이다 (scripts/build_index.js).
// pokedex.html 만 고치고 build_index 를 안 돌리면 루트(/)만 옛 버전이 된다
describe('index.html 사본', () => {
  const index = readText('index.html')
  const pokedex = readText('pokedex.html')

  it('pokedex.html 내용과 같다 (앞의 자동 생성 안내 주석만 다름)', () => {
    expect(index.endsWith(pokedex)).toBe(true)
    expect(index.startsWith('<!--')).toBe(true)
  })

  it('루트에서 이로치 모드를 켜는 IS_ROOT 판정이 있다', () => {
    expect(pokedex).toContain('IS_ROOT')
  })
})
