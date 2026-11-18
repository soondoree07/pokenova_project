import vm from 'node:vm'
import { describe, expect, it } from 'vitest'
import { readText } from './helpers.mjs'

// 관리자 화면은 퀴즈 이용자가 남긴 기록(신고 · 순위 · 세션)을 innerHTML 로 그린다.
// 그 값은 누구나 Firestore 에 쓸 수 있으니, 어떤 값이 와도 태그 · 스크립트가 되면 안 된다 (2026-11-18 리뷰)
const html = readText('admin.html')
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1]

function loadAdmin() {
  const els = {}
  const el = (id) => (els[id] ??= { id, innerHTML: '', textContent: '', classList: { toggle() {} }, addEventListener() {} })
  const ctx = { document: { getElementById: el, querySelector: () => null }, localStorage: { getItem: () => null }, window: {}, console }
  vm.createContext(ctx)
  vm.runInContext(script + '\n;globalThis.__t = { renderReportTable, renderSessionTable, renderLeaderboardTable, renderQuizStats, esc };', ctx)
  return { t: ctx.__t, els }
}

const EVIL = `x');alert(1);//<img src=x onerror=alert(2)>"'`
const NUM_EVIL = '<img src=x onerror=alert(3)>'
// 글자로 보이는 건 괜찮다. 진짜 태그(<img) 나 이용자 값이 들어간 onclick 이 생기면 실패
const bad = (out) => [/<img/i, /onclick="[^"]*alert/i].filter((re) => re.test(out))

describe('관리자 화면 저장형 XSS', () => {
  it('esc 는 작은따옴표도 바꾼다', () => {
    expect(loadAdmin().t.esc(`a'b`)).toBe('a&#39;b')
  })

  it('신고 표: 이용자가 정한 id · 문구가 스크립트가 되지 않는다', () => {
    const { t, els } = loadAdmin()
    t.renderReportTable([{ id: EVIL, ko: EVIL, memo: EVIL, type: EVIL, modeLabel: EVIL, ts: 1, resolved: false }])
    const out = els['report-tbody'].innerHTML
    expect(bad(out)).toEqual([])
    expect(out).not.toMatch(/onclick=/)
  })

  it('세션 · 순위 · 퀴즈 통계: 숫자 자리에 글자가 와도 태그가 되지 않는다', () => {
    const { t, els } = loadAdmin()
    const row = { mode: 'pokemon', modeLabel: EVIL, nickname: EVIL, difficulty: EVIL, correct: NUM_EVIL, wrong: NUM_EVIL, ts: 1 }
    t.renderSessionTable([row])
    t.renderLeaderboardTable([row])
    t.renderQuizStats([row])
    for (const id of ['session-tbody', 'lb-tbody', 'quiz-stat-grid']) expect(bad(els[id].innerHTML), id).toEqual([])
  })
})

describe('퀴즈 순위표 닉네임', () => {
  it('quiz.html 순위표는 닉네임을 이스케이프해서 그린다', () => {
    expect(readText('quiz.html')).not.toMatch(/\$\{r\.nickname\s*\|\|/)
  })
})
