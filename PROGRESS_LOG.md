# Pokénova 작업 로그

마지막 업데이트: 2026-03-27 (닉네임 욕설 필터, 애널라이즈 데이터 수정)

---

## 프로젝트 개요

- **경로**: `/home/soondoree07/pokenova_project/`
- **GitHub**: `https://github.com/soondoree07/pokenova_project`
- **사이트**: `https://soondoree07.github.io/pokenova_project/`
- **서버 실행**: `python3 -m http.server 8080` → 브라우저에서 `localhost:8080/`

## 파일 구성

```
pokenova_project/
├── index.html              # 메인 퀴즈 사이트 (포켓몬/기술/특성/도구 4종 퀴즈)
├── collect-data.js         # PokeAPI → 로컬 JSON 수집 스크립트
├── apply-translations.js   # needs_translation.json → quiz_*.json 반영 스크립트
├── admin.html              # 관리 페이지
└── data/
    ├── quiz_pokemon.json       # 포켓몬 1025마리 (메가/거다이/리전폼 포함)
    ├── quiz_moves.json         # 기술 850개
    ├── quiz_abilities.json     # 특성 307개
    ├── quiz_items.json         # 도구 953개
    └── needs_translation.json  # 번역 필요 항목 모음
```

## 완료된 작업

### 데이터 수집
- [x] `collect-data.js` 작성 → PokeAPI에서 전체 데이터 수집
- [x] 포켓몬: 한국어/영어 이름, 타입, 특성, 폼(메가진화/거다이맥스/리전폼), 스프라이트
- [x] 기술: 타입, 분류(물리/특수/변화), 세대, 위력/명중/PP, 설명
- [x] 특성: 한국어/영어 이름, 설명, 보유 포켓몬 목록
- [x] 도구: 한국어/영어 이름, 설명, 스프라이트, 카테고리
- [x] `needs_translation.json` 자동 추출 (한국어 없는 항목)

### 퀴즈 사이트
- [x] PokeAPI 실시간 연동 → 로컬 JSON 연동으로 전환
- [x] 포켓몬 맞추기: 실루엣 맞추기, 힌트 시스템, 목숨, 점수
- [x] 기술 맞추기: 설명 보고 기술 이름 맞추기, 시작 전 난이도 선택
- [x] 특성 맞추기, 도구 맞추기 기본 구현
- [x] 목숨 시스템 버그 수정 (틀릴때마다 시각적으로 감소)
- [x] 게임오버시 "완료" 버튼 → 초기화
- [x] 힌트 시스템: 쉬움=무제한, 보통=3개+5문제마다+1, 어려움=3개고정
- [x] 다음 문제 로드시 입력창 자동 포커스

---

## ✅ 완료: 2026-03-24 작업 내용

### 도구 맞추기 카테고리 탭
- [x] 도구 퀴즈에 카테고리 탭 3개 추가: **중요한물건** / **도구** / **기타**
  - 중요한물건: 지닌도구, 메가스톤, Z크리스탈, 플레이트, 메모리, 진화 관련
  - 도구: 나무열매, 회복아이템, 몬스터볼, 기술머신, 비타민, 봉투류
  - 기타: 배틀아이템(파워계열 = 플러스파워 등)
- [x] 카테고리별 아이템 필터링 및 탭 전환 시 퀴즈 리셋
- [x] `ITEM_CAT_MAP`으로 PokeAPI category 필드를 3개 그룹에 매핑

### 번역 완료
- [x] 기술 이름 24개 (Gen 8-9 히스이/팔데아): 페이탈클로, 배리어러시 등
- [x] 특성 이름 31개 (Gen 9 팔데아): 가시지않는향기, 쿼크차지 등
- [x] 특성 설명 40개 한국어 번역
- [x] 도구 설명 730개+ 한국어 번역 (패턴 기반 + 수동)
- [x] 배틀 아이템 17개 영어 설명 수정 (구애3종, 맹독구슬, 화염구슬 등)
- [x] 도구 이름 20개 한국어 추가 (Gen IV 메일류, 키아이템)

### 특성 폼 이름 한국어 변환
- [x] 특성 보유 포켓몬 목록(`pokemon` 배열)의 영어 폼 이름 → 한국어
  - kyogre-primal → 원시가이오가, groudon-primal → 원시그란돈
  - kyurem-black → 블랙큐레무, kyurem-white → 화이트큐레무
  - mewtwo-mega-x/y → 메가뮤츠X/Y 등 94개 항목 전부 수정 (0개 미완료)

---

## ✅ 완료: 한국어 번역 (2026-03-24)

### 번역 완료 현황

| 카테고리 | 상태 |
|----------|------|
| 기술 이름 (24개) | ✅ 완료 (Bulbapedia 참조) |
| 특성 이름 (31개) | ✅ 완료 (Bulbapedia 참조) |
| 특성 설명 (40개) | ✅ 완료 |
| 도구 설명 (907개) | ✅ 750개 번역, 나머지 unused/plot 아이템은 퀴즈 제외 처리 |

### 이전에 필요했던 항목 (참고용)

#### 기술 (24개) - ID 827~850, 히스이/팔데아 신규 기술
| ID | 영어 | 번역 필요 |
|----|------|-----------|
| 827 | Dire Claw | |
| 828 | Psyshield Bash | |
| 829 | Power Shift | |
| 830 | Stone Axe | |
| 831 | Springtide Storm | |
| 832 | Mystical Power | |
| 833 | Raging Fury | |
| 834 | Wave Crash | |
| 835 | Chloroblast | |
| 836 | Mountain Gale | |
| 837 | Victory Dance | |
| 838 | Headlong Rush | |
| 839 | Barb Barrage | |
| 840 | Esper Wing | |
| 841 | Bitter Malice | |
| 842 | Shelter | |
| 843 | Triple Arrows | |
| 844 | Infernal Parade | |
| 845 | Ceaseless Edge | |
| 846 | Bleakwind Storm | |
| 847 | Wildbolt Storm | |
| 848 | Sandsear Storm | |
| 849 | Lunar Blessing | |
| 850 | Take Heart | |

**참고 출처**: 나무위키, 포켓몬위키(pokemonwiki.kr), 포켓몬 공식(pokemon.co.kr)

#### 특성 (31개) - ID 268~298, Gen 9 팔데아 특성 (이름 영어)
| ID | 영어 | 번역 필요 |
|----|------|-----------|
| 268 | Lingering Aroma | |
| 269 | Seed Sower | |
| 270 | Thermal Exchange | |
| 271 | Anger Shell | |
| 272 | Purifying Salt | |
| 273 | Well-Baked Body | |
| 274 | Wind Rider | |
| 275 | Guard Dog | |
| 276 | Rocky Payload | |
| 277 | Wind Power | |
| 278 | Zero to Hero | |
| 279 | Commander | |
| 280 | Electromorphosis | |
| 281 | Protosynthesis | |
| 282 | Quark Drive | |
| 283 | Good as Gold | |
| 284 | Vessel of Ruin | |
| 285 | Sword of Ruin | |
| 286 | Tablets of Ruin | |
| 287 | Beads of Ruin | |
| 288 | Orichalcum Pulse | |
| 289 | Hadron Engine | |
| 290 | Opportunist | |
| 291 | Cud Chew | |
| 292 | Sharpness | |
| 293 | Supreme Overlord | |
| 294 | Costar | |
| 295 | Toxic Debris | |
| 296 | Armor Tail | |
| 297 | Earth Eater | |
| 298 | Mycelium Might | |

#### 특성 (9개) - ID 299~307, 이름은 한국어이지만 설명이 영어
| ID | 한국어 이름 | 영어 설명 (번역 필요) |
|----|-------------|----------------------|
| 299 | 심안 | The Pokémon ignores changes to opponents' evasiveness... |
| 300 | 감미로운꿀 | Lowers the evasion of opposing Pokémon by 1 stage... |
| 301 | 대접 | When the Pokémon enters a battle, it showers its ally... |
| 302 | 독사슬 | The power of the Pokémon's toxic chain may badly poison... |
| 303 | 초상투영 | The Pokémon's heart fills with memories... |
| 304 | 테라체인지 | When the Pokémon enters a battle, it absorbs the energy... |
| 305 | 테라셸 | The Pokémon's shell contains the powers of each type... |
| 306 | 제로포밍 | When Terapagos changes into its Stellar Form... |
| 307 | 독조종 | Pokémon poisoned by Pecharunt's moves will also become confused. |

#### 도구 (46개) - 이름도 영어
대부분 Mail 류 아이템(편지 봉투류)과 키 아이템
- grass mail, flame mail, bubble mail, bloom mail, tunnel mail, steel mail, heart mail, snow mail, space mail, air mail, mosaic mail, brick mail
- orange mail, harbor mail, glitter mail, mech mail, wood mail, wave mail, bead mail, shadow mail, tropic mail, dream mail, fab mail, retro mail
- devon goods, pokéblock case, rm. 1/2/4/6 key, oak's parcel, bike voucher, fame checker, berry pouch, teachy tv, tri-pass, rainbow pass, mysticticket, auroraticket, powder jar, ruby, sapphire, magma emblem, old sea map, god stone, hm08

#### 도구 설명 (907개) - 이름은 한국어, 설명만 영어
→ `data/needs_translation.json` 파일에 저장됨

---

## 번역 작업 방법

1. `data/needs_translation.json` 파일의 `ko` 필드(이름)와 `desc` 필드(설명)를 한국어로 수정
2. `node apply-translations.js` 실행 → quiz_*.json 파일에 반영
3. 번역 완료 항목은 `needs_translation.json`에서 자동 제거됨

```bash
# Node 실행 방법 (nvm 사용)
export NVM_DIR="$HOME/.nvm" && . "$NVM_DIR/nvm.sh"
node apply-translations.js
```

---

---

## ✅ 완료: 2026-03-24 (2차) 작업 내용

### 포켓몬 도감 페이지 (pokedex.html) 신규 기능

- [x] 고스트/유령 타입명 통일 → **고스트**로 일원화 (데이터: 고스트, 필터: 고스트)
- [x] 특성 설명 표시: 한국어 설명이 있는 특성은 영어 이름 대신 한국어 설명 표시 (`quiz_abilities.json` 로드)
- [x] 리전폼(알로라/가라르/히스이/팔데아) 별도 카드로 분리
  - 알로라 → 7세대 끝 (displayId 809.xxx)
  - 가라르 → 8세대 끝 (displayId 905.001~)
  - 히스이 → 8세대 끝, 가라르 이후 (displayId 905.201~)
  - 팔데아 → 9세대 끝 (displayId 1025.xxx)
  - 배지 색상: 알로라(초록), 가라르(파랑), 히스이(갈색), 팔데아(보라)
  - 필터 버튼 **리전폼** 추가 (전체/일반/리전폼/메가진화/거다이맥스)
  - 토템폼·피카츄알로라캡 제외, 같은 이름 중복 제외
- [x] 거다이맥스 전용기술에 한국어 효과 설명 추가 (32종 전부)
- [x] 거다이맥스 전용기술 설명 CSS (`.gmax-move-desc`)

### 레전드 Z-A 신규 메가진화 26종 추가

- [x] `quiz_pokemon.json`: 26종 forms에 추가 (abilities: `['?']`)
- [x] `pokedex.html` CANONICAL_MEGA에 26종 추가
- 목록: 메가픽시, 메가우츠보트, 메가아쿠스타, 메가망나뇽, 메가메가니움, 메가장크로다일,
  메가무장조, 메가눈여아, 메가염무왕, 메가두드리고, 메가펜드라, 메가스크래피,
  메가전룡, 메가샹델라, 메가브리가론, 메가마폭시, 메가개굴닌자, 메가화염레오,
  메가플로렛, 메가칼라마네로, 메가고사리가지, 메가독차룡, 메가루차불,
  메가지가르데, 메가할비롱, 메가파란도

### 도구 데이터 정리

- [x] 비전투/스토리 아이템 420개 제거 (quiz_items.json: 953개 → 533개)
  - 제거 카테고리: unused, plot-advancement, gameplay, all-mail, data-cards,
    miracle-shooter, loot, baking-only, event-items, collectibles, apricorn-box, mulch, dex-completion
- [x] Z크리스탈 퀴즈에서 숨김 처리 (데이터 유지, ITEM_CAT_MAP에서 제외)

### 번역 현황 업데이트

| 항목 | 상태 |
|------|------|
| 특성 이름 31개 (ID 268~298) | ✅ 완료 |
| 특성 설명 40개 (ID 268~307) | ✅ 완료 |
| 기술 설명 42개 (Z기술 18 + Gen8-9 24) | ⏳ 미번역 |
| 도구 이름/설명 영어 | ✅ 퀴즈 포함 아이템 전부 완료 (needs_translation 잔여 203개는 모두 퀴즈 제외 항목) |
| 레전드ZA 메가 특성 26종 | ⏳ 5종 완료 (드래곤스킨/메가솔라/틀깨기/멀티스케일/눈퍼뜨리기), 나머지 미확인 |

---

---

## ✅ 완료: 2026-03-26 작업 내용

### 사이트 리브랜딩
- [x] 사이트 이름 전체 **Pokénova** 로 변경 (`<title>`, 헤더, 관리자 페이지)

### Firebase Firestore 연결 (프로젝트: pokenova-f17e7, 서울 리전)
- [x] Firebase 모듈 SDK(`<script type="module">`) 방식으로 초기화
- [x] 기존 compat SDK / Google 로그인 / 랭킹 카드 코드 전부 제거
- [x] 오류 신고 → Firestore `reports` 컬렉션 저장 (localStorage 백업 유지)
- [x] 게임 세션 → Firestore `sessions` 컬렉션 저장
- [x] Firestore 보안 규칙: 전체 허용 (개발 단계)

### 리더보드 기능
- [x] 게임오버 시 닉네임 입력 폼 표시 (한글/영어/숫자, 최대 10글자)
- [x] 닉네임 + 점수 → Firestore `leaderboard` 컬렉션 저장
- [x] 건너뛰기 가능
- [x] 각 퀴즈 탭에 **🏆 리더보드 보기** 버튼 + 정답 내림차순 TOP 100 패널
- [x] Firestore 미연결 시 localStorage 백업으로 표시

### 오류 신고 기능
- [x] 모든 퀴즈 탭에 **⚠️ 오류 신고** 버튼 추가
- [x] 신고 유형(문제오류/정답오류/기타) + 메모 입력 모달
- [x] Firestore `reports` 컬렉션에 저장

### 관리자 페이지 재설계 (`admin.html`)
- [x] 비밀번호 로그인 유지 (qkrwjdgur07)
- [x] Firebase 연결 시 Firestore에서 실시간 데이터 읽기
- [x] 섹션: 개요 통계 / 퀴즈별 통계 / 오류 신고 로그 / 게임 세션 테이블
- [x] 오류 신고 처리완료/삭제 기능 (Firestore + localStorage 동기화)
- [x] 접속: `localhost:8080/admin.html`

### 퀴즈 기능 개선
- [x] 도구 맞추기: 힌트 3회 제한 추가
- [x] 도구 맞추기: Z크리스탈 29개 퀴즈에서 제외 (`z-crystals` 카테고리)
- [x] 특성/도구 맞추기: **게임 시작** 버튼 추가 (탭 진입 시 바로 시작 안 함)
- [x] 특성/도구 맞추기: **↩ 처음으로** 버튼 추가 (게임 중 → 시작 화면 복귀)
- [x] 처음으로 버튼 스타일 4개 모드 전부 통일

### 버그 수정
- [x] `fbUpdateAndShowRank` 삭제 후 잔여 호출 제거 (데이터 로드 불가 버그)
- [x] `hideRankCard` null 참조 에러 수정

### 커밋 목록 (오늘)
| 커밋 | 내용 |
|------|------|
| 62b45a3 | 사이트 이름 Pokénova로 변경 |
| 1a0b80a | 리더보드 기능 추가 |
| ebfe03a | 특성/도구 처음으로 버튼 스타일 통일 |
| abaceb2 | 특성/도구 맞추기: 게임 시작 버튼 + 처음으로 버튼 추가 |
| 74d3f73 | 도구 맞추기: 힌트 3회 제한 + Z크리스탈 제외 |
| f8c2331 | hideRankCard null 참조 에러 수정 |
| 929a902 | fbUpdateAndShowRank 잔여 호출 제거 |
| de40e65 | Firebase Firestore 연결 |
| 173b478 | 오류 제보 기능 + 관리자 페이지 재설계 |

---

---

## ✅ 완료: 2026-03-26 (2차) 작업 내용

### 점수 UI 개선
- [x] 누적 정답/오답 표시 제거, **연속 정답(스트릭)만** 유지 (4개 모드 전체)
- [x] updateScore 함수에서 DOM null 에러 수정 (리더보드 탭 클릭 불가 버그 해결)

### 리더보드 난이도 분리
- [x] 포켓몬/기술 맞추기: 보통/어려움 난이도별 리더보드 분리
- [x] 쉬움 난이도는 리더보드 없음 (게임오버 시 바로 다시시작 표시)
- [x] Firestore 복합 쿼리: `mode + difficulty + correct` (인덱스 필요)

### 한 문제당 최대 1목숨 차감
- [x] 4개 모드 전체: 같은 문제에서 틀려도 목숨은 1개만 차감 (`xWrongThisRound` 플래그)

### 모바일 최적화
- [x] iOS 줌 방지: 모든 input/textarea 폰트 크기 16px 이상 강제
- [x] 터치 타겟: button, nav-tab, diff-btn, lb-diff-tab 등 최소 높이 44px
- [x] body padding-top: 데스크탑 76px / 모바일 64px
- [x] 380px 이하 소형 화면: 난이도 설명 텍스트 숨김

### 사이트 로고 링크
- [x] Pokénova 로고 클릭 시 메인 페이지(index.html)로 이동 (메인에서 누르면 새로고침)

### 제작자 푸터 추가
- [x] 페이지 하단 footer 추가: 닉네임(잉짱), 이메일(soondoree07@gmail.com)
- [x] 닌텐도/게임프리크 저작권 면책 문구 (영문)
- [x] © 2026 Pokénova 표기

### 프로젝트 이름 변경
- [x] GitHub 저장소: `pokemon_project_1` → `pokenova_project`
- [x] 로컬 폴더: `pokemon_project_1` → `pokenova_project`
- [x] 메인 파일: `pokemon-quiz.html` → `index.html`
- [x] 내부 링크 전체 업데이트 (index.html, pokedex.html, admin.html)
- [x] 사이트 URL: `https://soondoree07.github.io/pokenova_project/`

### 커밋 목록
| 커밋 | 내용 |
|------|------|
| 03f621b | 모바일 최적화 |
| 48c40d2 | Pokénova 로고 링크 + 제작자 푸터 추가 |
| d629cfa | 프로젝트 이름 변경 및 파일명 index.html로 변경 |

---

---

## ✅ 완료: 2026-03-27 작업 내용

### 닉네임 욕설 필터링
- [x] `NICK_BLACKLIST` 배열: 한국어/영어 욕설 목록
- [x] `containsBadWord()`: 소문자 변환 + 공백 제거 후 포함 여부 검사
- [x] `validateNick()`에 욕설 감지 시 "사용할 수 없는 닉네임이에요" 에러 반환

### 데이터 수정
- [x] 애널라이즈(Analytic) 특성 포켓몬 목록 추가 (기존: 빈 배열)
  - 추가: 코일, 레어코일, 별가사리, 아쿠스타, 폴리곤, 폴리곤2, 자포코일, 폴리곤Z, 보르쥐, 보르그, 리그레, 벰크 (전부 숨겨진특성)

### 커밋 목록
| 커밋 | 내용 |
|------|------|
| 545d15d | 닉네임 욕설 필터링 추가 |
| fbacf42 | 애널라이즈 특성 포켓몬 목록 추가 |

---

## 참고 링크
- 나무위키 포켓몬 기술 목록: https://namu.wiki/w/포켓몬스터/기술
- 포켓몬위키: https://pokemonwiki.kr
- 포켓몬 공식(한국): https://pokemon.co.kr
- 포켓몬 DB: https://pokemondb.net/move/all
