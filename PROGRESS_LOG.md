# 포켓몬 퀴즈 사이트 작업 로그

마지막 업데이트: 2026-03-24 (도구 카테고리 탭 추가 + 번역 완료)

---

## 프로젝트 개요

- **경로**: `/home/soondoree07/pokemon_project_1/`
- **GitHub**: `gh repo view` 로 확인
- **서버 실행**: `python3 -m http.server 8080` → 브라우저에서 `localhost:8080/pokemon-quiz.html`

## 파일 구성

```
pokemon_project_1/
├── pokemon-quiz.html       # 메인 퀴즈 사이트 (포켓몬/기술/특성/도구 4종 퀴즈)
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

## 참고 링크
- 나무위키 포켓몬 기술 목록: https://namu.wiki/w/포켓몬스터/기술
- 포켓몬위키: https://pokemonwiki.kr
- 포켓몬 공식(한국): https://pokemon.co.kr
- 포켓몬 DB: https://pokemondb.net/move/all
