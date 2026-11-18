import { describe, expect, it } from 'vitest'
import { exists, readJson } from './helpers.mjs'

// 화면이 읽는 데이터 파일이 서로 맞는지. 고유명사는 이 파일들이 원천이다
const pokedex = readJson('data/pokedex.json')
const forms = pokedex.flatMap((p) => p.forms ?? [])

describe('포켓몬 도감 데이터', () => {
  it('번호가 1부터 빠짐 · 겹침 없이 이어진다', () => {
    expect(pokedex.map((p) => p.id)).toEqual(pokedex.map((_, i) => i + 1))
  })

  it('모든 포켓몬에 한국어 · 영어 이름이 있다', () => {
    expect(pokedex.filter((p) => !p.ko || !p.en)).toEqual([])
  })

  it('그림 경로가 전부 실제 파일을 가리킨다 (기본 · 폼 · 이로치)', () => {
    const paths = [...pokedex, ...forms].flatMap((p) => [p.sprite, p.shinySprite]).filter(Boolean)
    expect(paths.filter((p) => !exists(p))).toEqual([])
  })

  it('기본 포켓몬은 전부 이로치 그림이 있다', () => {
    expect(pokedex.filter((p) => !p.shinySprite).map((p) => p.en)).toEqual([])
  })
})

describe('퀴즈 · 도감 이름 데이터', () => {
  for (const name of ['quiz_pokemon', 'quiz_moves', 'quiz_items', 'quiz_abilities']) {
    it(`${name}.json 의 모든 항목에 한국어 · 영어 이름이 있다`, () => {
      const list = readJson(`data/${name}.json`)
      expect(list.length).toBeGreaterThan(0)
      expect(list.filter((entry) => !entry.ko || !entry.en)).toEqual([])
    })
  }
})
