# 구조

정적 HTML 사이트. 빌드 단계가 없고, 저장소 루트가 그대로 사이트다(올리지 않을 파일은 `.assetsignore`).

## 폴더
- `*.html` — 페이지마다 한 파일(화면 · 스타일 · 스크립트가 한 파일 안). `index.html` = `pokedex.html` 자동 사본
- `data/` — 도감 데이터 JSON(고유명사의 원천). 화면이 `fetch('/data/...')` 로 읽는다
- `sprites/` — 포켓몬 · 도구 그림 (`_headers` 로 1년 캐시)
- `scripts/` · 루트 `*.js` — 데이터 · 그림 받아오기, `index.html` 만들기 (개발용, 배포 제외)
- `archive/` — 옛 파이썬 스크립트 · 문서 보관
- `tests/` — 하네스 검증(개발용 `package.json` · 서버 · 단위 · 흐름)

## 레이어
정적 HTML 이라 검사하지 않는다(`harness.json` 의 `stack: static`). 페이지 사이에 import 가 없다.

## 흐름
```
data/*.json ─ fetch ─> pokedex.html (?shiny=1 · 루트면 이로치) ─ build_index.js ─> index.html
                     ├> movedex.html · itemdex.html
                     └> entry · record · today (네비에서 임시 숨김)
admin.html ─> Firebase (운영) · quiz.html ─> pochams API (배포 제외)
```

- 데이터 원천은 `pochams_project` 와 같이 쓴다. 고치는 순서는 `CLAUDE.md` "데이터 수정 규칙"
- 구글 통계(gtag)는 모든 공개 페이지에 붙어 있다

## 배포
- Cloudflare Workers 정적 자산: main 에 push 하면 자동 배포, 주소 https://pokenova.pochams.com (clean URL: `/pokedex.html` → `/pokedex`)
- `vercel.json` 은 옛 Vercel 배포용(rewrites · 옛 주소 이동)

## 시험
- 단위: `tests/unit/*.test.mjs` (Vitest) — `index.html` 사본 일치 · 데이터 정합 · 검증 서버 주소 풀이
- 흐름: `tests/e2e/*.spec.mjs` (Playwright) — 공개 페이지 7개가 뜨는지 · 도감 3종에 카드가 그려지는지, PC · 390px. 바깥 주소는 막는다
- 서버: `tests/serve.mjs` (의존성 없음). 검증 포트는 E2E 4150 고정
