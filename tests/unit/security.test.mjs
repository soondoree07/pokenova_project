import { describe, expect, it } from 'vitest'
import { exists, readJson, readText } from './helpers.mjs'

// 관리자 페이지는 공개 주소라 화면 코드에 비밀 값이 있으면 누구나 본다.
// 확인은 구글 로그인 + Firestore 보안 규칙이 맡는다 (2026-11-18 첫 검사)
describe('관리자 페이지', () => {
  const admin = readText('admin.html')

  it('비밀번호 입력 · 비교 코드가 없다', () => {
    expect(admin).not.toMatch(/ADMIN_PASSWORD/)
    expect(admin).not.toMatch(/type="password"/)
  })

  it('Firebase 구글 로그인으로 들어간다', () => {
    expect(admin).toMatch(/firebase-auth\.js/)
    expect(admin).toMatch(/GoogleAuthProvider/)
    expect(admin).toMatch(/onAuthStateChanged/)
  })

  it('권한이 없다는 Firestore 오류를 빈 목록으로 삼키지 않는다', () => {
    expect(admin).toMatch(/permission-denied/)
  })
})

describe('Firestore 보안 규칙 파일', () => {
  const path = 'firebase/firestore.rules'

  it('저장소에 있고 사이트에는 올리지 않는다', () => {
    expect(exists(path)).toBe(true)
    expect(readText('.assetsignore')).toMatch(/^firebase$/m)
  })

  it('퀴즈 기록 3종은 관리자만 읽고 지울 수 있다', () => {
    const rules = readText(path)
    for (const col of ['sessions', 'reports', 'leaderboard']) {
      const block = rules.match(new RegExp(`match /${col}/\\{[^}]+\\} \\{([^}]*)\\}`))
      expect(block, col).not.toBeNull()
      expect(block[1]).toMatch(/allow (read, )?update, delete: if isAdmin\(\)/)
    }
    expect(rules).toMatch(/request\.auth\.uid/)
  })
})

describe('옛 주소 이동 (vercel.json)', () => {
  const { redirects } = readJson('vercel.json')
  const toNew = redirects.filter((r) => r.has?.[0]?.value === 'pokenova.vercel.app')

  it('루트(/)도 새 주소로 보낸다', () => {
    expect(toNew.some((r) => r.source === '/' && r.destination === 'https://pokenova.pochams.com/')).toBe(true)
  })

  it('나머지 경로도 새 주소로 보낸다', () => {
    expect(toNew.some((r) => r.source === '/:path*')).toBe(true)
  })
})
