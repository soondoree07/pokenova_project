# Pokenova Project

## 도메인
- **프로덕션 URL**: `https://pokenova.pochams.com`
- **구 URL (리다이렉트)**: `https://pokenova.vercel.app` → `pokenova.pochams.com`으로 301 리다이렉트

## Devlog
이 프로젝트의 `project` 필드명: **`pokenova`**

자동 devlog 업데이트 규칙은 `~/.claude/CLAUDE.md` 전역 규칙을 따른다.

---

## 데이터 수정 규칙

pokenova는 포켓몬·기술·도구·특성·배우는기술 데이터를 **Neon PostgreSQL DB**에서 가져온다 (pochams API 경유).
데이터를 수정할 때는 소스 JSON 파일을 수정한 뒤 pochams seed를 재실행한다.

### 소스 파일 위치

| 데이터 | 소스 파일 | DB 테이블 |
|---|---|---|
| 포켓몬 | `data/quiz_pokemon.json` + `data/pokemon_stats.json` | `pokemon_data` |
| 기술 | `data/quiz_moves.json` | `move_data` |
| 도구 | `data/quiz_items.json` | `item_data` |
| 특성 | `data/quiz_abilities.json` | `ability_data` |
| 배우는 기술 | `data/learnsets.json` | `pokemon_learnset` |

### 수정 절차

**원칙: JSON 수정 후 반드시 DB에 반영한다. 반영 없이 JSON만 수정하고 끝내지 않는다.**

#### 1개~몇 개만 수정할 때 → upsert (1~2초)

```bash
cd /home/soondoree07/pochams_project
npm run upsert move <en>        # 기술 1개
npm run upsert item <en>        # 도구 1개
npm run upsert ability <en>     # 특성 1개
npm run upsert pokemon <en>     # 포켓몬 1개 (기본형+메가+알트폼 전부)
npm run upsert learnset <en>    # 포켓몬 배우는기술
```

#### 대량 추가·구조 변경할 때 → 전체 seed (20~40초)

```bash
cd /home/soondoree07/pochams_project
npm run seed
```

> pokenova 자체에는 배포가 필요 없다. upsert 또는 seed 재실행만으로 DB가 업데이트되고 pochams API가 즉시 반영된다.

### champions_learnsets.json 갱신

포켓몬(quiz_pokemon.json), 기술(quiz_moves.json), 배우는기술(learnsets.json) 수정 시 seed 후 champions_learnsets.json도 재생성한다.
재생성 명령은 pochams_project/CLAUDE.md의 "champions_learnsets.json 자동 갱신" 섹션 참고.
