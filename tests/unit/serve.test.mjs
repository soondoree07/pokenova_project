import path from 'node:path'
import { describe, expect, it } from 'vitest'
import { resolveFile } from '../serve.mjs'
import { ROOT } from './helpers.mjs'

// 검증용 서버가 배포처럼 깨끗한 주소를 보여 주는지
describe('검증용 서버 주소 풀이', () => {
  const rel = (url) => { const file = resolveFile(url); return file && path.relative(ROOT, file) }

  it('/ 는 index.html', () => expect(rel('/')).toBe('index.html'))
  it('/pokedex 는 pokedex.html', () => expect(rel('/pokedex')).toBe('pokedex.html'))
  it('물음표 뒤는 무시한다', () => expect(rel('/pokedex?shiny=1')).toBe('pokedex.html'))
  it('데이터 파일은 그대로', () => expect(rel('/data/pokedex.json')).toBe(path.join('data', 'pokedex.json')))
  it('없는 주소는 null', () => expect(rel('/no-such-page')).toBeNull())
  it('폴더 밖으로 나가는 주소는 null', () => expect(rel('/../../etc/passwd')).toBeNull())
})
