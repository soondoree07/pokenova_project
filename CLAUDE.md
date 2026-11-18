# P001 포케노바 — 프로젝트 규칙

> 전역 규칙(~/.claude/CLAUDE.md) 위에 이 프로젝트만의 것만 적는다. 길어지면 docs/ 로 뺀다.

## 한 줄 소개
정적 HTML 포켓몬 도감 사이트(루트 = 이로치 도감 · 기술 · 아이템 도감). 서버 없음, 데이터는 `data/*.json`. https://pokenova.pochams.com

## 실행
- 개발 서버: `harness.json` 의 `dev` (`node tests/serve.mjs <포트>`, 의존성 없음 · 배포처럼 깨끗한 주소)
- 검증: `verify-task` (단위 `cd tests && npx vitest run` · 흐름 `cd tests && npx playwright test` = 공개 페이지 · PC · 390px). 처음엔 `cd tests && npm ci`
- 배포: main 에 push 하면 Cloudflare Workers(정적 자산)가 자동 배포. **배포 중이라 코드 변경은 L3**
- 테스트 도구는 `tests/package.json` 에만 둔다. **루트에 `package.json` 을 만들지 않는다**(배포가 의존성 설치 · 빌드 감지를 시작할 수 있음)
- 사이트에 올리지 않을 파일은 `.assetsignore` 에 넣는다(Cloudflare 업로드 제외)

## 이 프로젝트만의 규칙

### 게임/도메인 명칭 규칙
포켓몬 이름, 특성·기술·아이템 등 **게임 내 고유 명칭은 반드시 DB/데이터 파일에서 가져온다.**

- 코드에 한국어/영어 명칭을 직접 하드코딩하지 않는다
- 명칭이 필요하면 → 먼저 관련 데이터 파일(`data/quiz_*.json` 등)을 확인하고 거기서 가져온다
- 데이터에서 가져올 수 없는 구조라면, 명칭을 파라미터로 받아서 사용하는 방식으로 설계한다
- 임의로 추측한 명칭을 코드에 넣지 않는다

자세한 이유는 메모리 `feedback_no_arbitrary_names.md` 참조.

### 구조 주의
- `index.html` 은 `pokedex.html` 의 자동 생성 사본. `pokedex.html` 을 고치면 `node scripts/build_index.js` (단위 테스트가 어긋나면 잡는다)
- `_redirects` 는 쓰지 않는다(Cloudflare clean URL 과 충돌해 루트 404, RESUME 2026-07-13)
- 폼 관련 필드를 데이터에 넣으면 `pokedex.html` 의 엔트리 생성 4곳(리전 · 합체 · 메가 · 거다이)에도 넘긴다
- `admin.html` · `quiz.html` 은 E2E 에서 뺀다(운영 Firebase · 배포 제외)

## 도메인
- **프로덕션 URL**: `https://pokenova.pochams.com`
- **구 URL (리다이렉트)**: `https://pokenova.vercel.app` → `pokenova.pochams.com`으로 301 리다이렉트

## Devlog
이 프로젝트의 `project` 필드명: **`pokenova`**

자동 devlog 업데이트 규칙은 `~/.claude/CLAUDE.md` 전역 규칙을 따른다.

---

## 데이터 수정 규칙

**원천은 이 저장소의 `data/*.json` 이다.** 화면은 서버 없이 이 파일을 `fetch('data/...')` 로 바로 읽는다(2026-07-12 부터, pochams API 의존 제거).
데이터를 고치면 이 저장소에 커밋 · push 하는 것으로 사이트에 반영된다(Cloudflare 자동 배포, 코드 변경과 같이 L3).

### 파일과 화면

| 데이터 | 파일 | 읽는 화면 |
|---|---|---|
| 도감(포켓몬 + 폼 + 이로치 + `inChampions`) | `data/pokedex.json` | `pokedex` · `index` · `today` · `movedex` |
| 종족값 | `data/pokemon_stats.json` | `pokedex` · `today` |
| 포켓몬 원본 | `data/quiz_pokemon.json` | 화면은 안 읽음. `pokedex.json` 생성 원본(`node scripts/build_pokedex.js`) · 포챔스가 읽음 |
| 기술 | `data/quiz_moves.json` · `data/quiz_zmoves.json` | `movedex` |
| 도구 | `data/quiz_items.json` | `itemdex` |
| 특성 | `data/quiz_abilities.json` | `pokedex` 특성 설명 |
| 배우는 기술 | `data/learnsets.json` | `movedex` |

- `pokedex.json` 은 `quiz_pokemon.json` 에서 만든다. 둘 다 고칠 때는 같이 맞춘다(단위 시험이 특성 참조를 잡는다)
- 아직 pochams API 를 부르는 곳: `quiz.html`(배포 제외) · `entry.html`(네비에서 숨김)

### 포챔스(pochams_project)로 넘기기

포챔스는 이 `data/` 를 읽어 자기 DB(Neon)를 만든다. 포케노바에서 데이터를 고쳤고 포챔스에도 반영해야 하면 포챔스 쪽에서 돌린다(운영 DB 쓰기라 정혁님 확인 뒤):

```bash
cd /home/soondoree07/pochams_project
npm run sync          # pokedex.json → 포챔스 소스 재생성 → seed (scripts/sync-data.sh)
npm run upsert ability <en>   # 한두 개만이면 upsert
```

자세한 순서는 `pochams_project/CLAUDE.md`.

### 외부에서 데이터를 받아올 때 — 우리 id 로 묻지 않는다

PokeAPI 는 **이름(슬러그)으로 묻는다.** 번호는 우리 것과 다르다.

2026-09-10 에 도구 일본어 이름 124개가 통째로 밀려 있던 것을 찾았다. 옛
스크립트가 `/api/v2/item/{우리 id}` 로 물어서, 583번 도구(요정의깃털)를
물으면 PokeAPI 583번(루가루암 Z)이 돌아왔다. 349번 이후가 전부 어긋나
화석·가면·메가스톤이 엉뚱한 Z크리스탈 이름을 달고 있었다.

- 번호로 물어도 되는 곳은 **포켓몬뿐**이다. 우리 id 가 곧 전국도감 번호이고
  PokeAPI species 번호와 같다(전수 확인함).
- 도구·특성은 이름이 다른 것이 있다. 대응표는
  `scripts/fetch_japanese_names.py` 의 `ITEM_SLUG`·`ABILITY_SLUG`·`MOVE_SLUG` 에
  적어 둔다. 추측해서 넣지 말고 확인한 것만 적는다.
- 폼도 마찬가지다. `squawkabilly` 가 아니라 `squawkabilly-green-plumage` 다.
  `learnsets.json` 26종이 빈 채로 있던 이유가 이것이고,
  `scripts/fill_missing_learnsets.py` 에 그 대응표가 있다.

```bash
python3 scripts/fetch_japanese_names.py --check     # 저장 없이 무엇이 바뀔지 본다
python3 scripts/fetch_japanese_names.py items       # 일부만 반영
python3 scripts/fill_missing_learnsets.py --check   # 빈 기술폭 점검
```

출처는 **PokeAPI 우선, 없으면 포켓몬위키**다. 둘이 어긋나면 PokeAPI 를 쓰고
화면에 남긴다(실측 3건이 전부 위키 오류였다). 어느 쪽에도 없으면 **건드리지
않고 보고한다.** 이름을 지어내지 않는다.

## 빠른 참조
| 목적 | 문서 |
|---|---|
| 구조 · 데이터 흐름 · 시험 위치 | `ARCHITECTURE.md` |
| 이어하기 · 지난 기록 | `RESUME.md` · `PROGRESS_LOG.md` |
| 진행 중 · 끝난 작업 | `docs/exec-plans/` |
| 미뤄 둔 문제 · 100줄 기준선 | `docs/exec-plans/tech-debt-tracker.md` |
