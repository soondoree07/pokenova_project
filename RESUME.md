# 진행 상황 (2026-07-12 KST 기준)

> 트리거(`포케노바`/`pokenova`) 시 이 파일을 **가장 먼저** 읽고 이어간다.

## 이 프로젝트가 뭐냐 (한 줄)

포케노바 = **정적 HTML 도감 사이트** (pokedex/movedex/itemdex/index/entry/record/today `.html`, 데이터 `data/*.json`, 스프라이트 `sprites/pokemon/`). 서버 없음. **Cloudflare Workers**(정적 자산) 호스팅.

## 2026-07-12 세션 — 이로치 도감 · 로컬 데이터화 · Cloudflare 이전

포켓몬 정보 쇼츠 채널의 첫 콘텐츠(이로치 색상)를 위해 이로치 도감 신설 + pochams API 의존 제거.

1. **이로치 도감 신설** — `pokedex.html`에 `?shiny=1` 파라미터 방식. 네비 "포켓몬 도감" **오른쪽**에 `✨ 이로치 도감`(`pokedex.html?shiny=1`) 추가.
   - `const SHINY = new URLSearchParams(location.search).get('shiny')==='1'` + `spriteOf(p)` 헬퍼로 카드·모달·폼 스프라이트 3곳 분기.
   - `download_shiny_sprites.js`로 PokéAPI official-artwork/shiny **1025마리 전부** 다운로드 → `pokedex.json` 각 항목에 `shinySprite` 필드 추가(백업 `.bak`). **1025/1025 official, 누락 0.**
2. **movedex·itemdex·특성 로컬 데이터화** — pochams API(402로 다운)에 의존하던 fetch를 로컬 파일로 교체. Promise.all fail-fast로 도감 전체가 안 뜨던 문제 해결.
   - pokedex 특성: `data/quiz_abilities.json` / movedex: `data/quiz_moves.json`(L374) / itemdex: `data/quiz_items.json`(L306). 모두 `.catch(()=>[])` 폴백.
   - **포케노바가 이제 데이터 자급자족** — pochams API 없어도 도감 전부 동작.
3. **네비 임시 숨김** — 7개 HTML 전부에서 퀴즈(index)·기록(record)·오늘의포켓몬(today) 네비 링크 주석 처리(`임시숨김`, 복구 쉬움). 현재 노출 네비: 포켓몬 도감·이로치 도감·기술 도감·아이템 도감·배틀팀.
4. **Cloudflare Workers 이전** — Vercel → Cloudflare. 커스텀 도메인 `pokenova.pochams.com` 연결(라이브 200 확인).
   - `_headers`(신규): `/sprites/*` 1년 immutable 캐시.
   - `.assetsignore`(신규): .git·node_modules·*.bak·스크립트·*.py 등 제외 → 25MiB 파일 한도 빌드에러 해결.
   - `_redirects`는 생성했다가 **삭제**(Cloudflare 기본 clean-URL과 충돌해 리다이렉트 루프).

## 2026-07-12 추가 — 이로치 도감 폼 shiny 275/284

- 기본 1025 외에 **폼 284개**도 shiny 채움. `download_form_shiny_sprites.js`(za_ 폼명→PokeAPI 이름 변환 다운로드). 공식243·홈4·base26·necrozma리맵2 = **275/284**.
- **남은 9개**(공식 shiny 아트워크 부재 → 정규 폴백): deerling·sawsbuck 계절 6, frillish·jellicent 암컷 2, **메가냐오닉스**(ZA 신규 메가) 1. 필요하면 나무위키/포켓몬위키에서 수동 확보.
- `build_pokedex.js` 재생성 시 base·폼 `shinySprite` 보존하도록 수정(재실행해도 shiny 안 날아감).

## 현재 막힌 지점 / 결정 대기

- 없음. 모든 변경 커밋·푸시 완료(main). Cloudflare가 GitHub main push 시 자동 재배포.

## 다음 액션 (이어할 작업 후보)

1. **쇼츠 콘텐츠 제작 재개** — 원래 목표였던 이로치 색상 쇼츠(첫 에피소드). TTS는 **Typecast** 방향. (pokemon_shorts 쪽 작업)
2. **이로치 도감 UI/UX 다듬기**(요청 시) — 배지/정렬/검색 등.
3. **숨긴 네비 복구**(원할 때) — 7개 HTML의 `임시숨김` 주석 해제.

## 이미 완료된 셋업 / 데이터 파이프라인 (재시도 불필요)

- **데이터 마스터 = `pokenova_project/data/`**. 여기 `pokedex.json`의 `inChampions` true/false가 포챔스 등장 포켓몬을 결정.
- **한 번 업데이트로 둘 다 반영**: `cd pochams_project && npm run sync -- --push` → pokedex.json → 포챔스 브릿지·DB seed(Neon, 즉시 반영) + 포케노바 data 커밋·push(Cloudflare 자동 재배포). 상세는 `pochams_project/scripts/sync-data.sh`.
- 라이브: `https://pokenova.pochams.com/pokedex?shiny=1` (이로치 도감, ✨ 네비).
- 이번 세션 push 커밋: 9ec9716 / e73431c / 8d09e25 / 9de01ad / f74e208 (main).
