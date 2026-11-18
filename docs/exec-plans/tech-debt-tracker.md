# 미뤄 둔 문제

## 100줄 기준선 (2026-11-18, 하네스 붙일 때)

100줄 넘는 코드 파일 17개. 모두 개발용 스크립트(사이트에 안 올라감). 더 커지면 `check-file-size` 가 막는다. 줄이면 여기서 지운다.
HTML 안의 스크립트는 검사 대상이 아니다(`index.html` · `pokedex.html` 6만 자대, `quiz.html` 14만 자). 쪼개려면 js 파일로 빼는 작업부터.

| 줄 | 파일 |
|---|---|
| 466 | `collect-data.js` |
| 274 | `archive/build_sv_learnsets.py` |
| 240 | `scripts/fetch_japanese_names.py` |
| 215 | `archive/build_learnsets.py` |
| 208 | `download_sprites.js` |
| 207 | `scripts/download_hires_items.js` |
| 183 | `scripts/fill_missing_learnsets.py` |
| 173 | `download_form_shiny_sprites.js` |
| 149 | `archive/verify_all_moves.py` |
| 138 | `archive/generate_item_list.py` |
| 132 | `archive/add_items.py` |
| 128 | `scripts/make_item_artifact.js` |
| 126 | `archive/fix_gen9_moves.py` |
| 122 | `scripts/build_pokedex.js` |
| 121 | `download_shiny_sprites.js` |
| 109 | `apply-translations.js` |
| 106 | `archive/make_item_doc.py` |

## 첫 검사에서 본 것 (고치기는 따로)

막음
- 해결 11-18 (코드 쪽, 콘솔 적용은 정혁님) **관리자 비밀번호가 화면 코드에 그대로 있다** `admin.html` (`ADMIN_PASSWORD`). `/admin` 은 공개 주소라 페이지 소스를 열면 누구나 본다. git 기록에도 남아 있다. 비밀번호를 바꾸고, 확인을 Firebase 로그인 · 보안 규칙으로 옮기는 작업 필요(값은 여기 적지 않음)

고치면 좋음
- `RESUME.md` 가 사이트에 올라가 있다(https://pokenova.pochams.com/RESUME.md 200). `.assetsignore` 에 없어서. `CLAUDE.md` · `PROGRESS_LOG.md` 는 빠져 있음
- 해결 11-18 (`/` 전용 규칙, Vercel 재배포 뒤 확인) 옛 주소 `pokenova.vercel.app` 이 새 주소로 넘어가지 않고 200 으로 옛 Vercel 배포를 보여 준다(`vercel.json` 이동 규칙이 안 먹음 · 확인 2026-11-18)
- `docs/projects.json` 의 P001 `deploy` 가 `vercel` 인데 실제 배포는 Cloudflare. 하네스 쪽에서 고칠 것
- 해결 11-18 `CLAUDE.md` "데이터 수정 규칙"은 pochams API 경유라고 하지만, 2026-07-12 부터 도감은 로컬 `data/*.json` 을 읽는다(RESUME). 데이터 원천 설명을 다시 맞출 것
- 해결 11-18 폼 285개 중 1개(`squawkabilly` 폼 하나)에 이로치 그림이 없다. RESUME 의 "폼 284/284" 뒤에 폼이 늘어난 듯
- 해결 11-18 `quiz_abilities.json` 에 영어 이름(`en`) 겹침 1건(혼연일체 `as_one`, RESUME 의 퀴즈 정복 판정 버그 원인)
- `tests/` 개발 의존성 `npm audit` high 5개: vitest 가 쓰는 `picomatch`(개발 도구에서만, 배포 안 됨)

참고
- 비밀값 검사: Firebase 웹 `apiKey` 2곳(`admin.html` · `quiz.html`)은 원래 공개되는 값이라 문제 아님. 보호는 Firestore 보안 규칙이 맡는다
