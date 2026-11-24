---
id: 1124-design-system
project: P001
type: 문서
branch: claude/1124-design-system
port: 4102
status: 진행 중
created: 2026-11-24
---

# 실행 계획: design-system

## 목표
정혁님(2026-11-24): "우리가 앞으로 앱이나 웹 만들때 디자인 관련해서 디자인 시스템이 각 프로젝트마다 있어야돼" — 포케노바 몫(일감 1124-122636-P001-6801, P000 디자인 시스템 틀이 넘김). 드코 파일은 P024 가 만든다.

## 완료 기준
- [x] 저장소 맨 위 `DESIGN.md`: 틀(harness/templates/DESIGN.md) 구조 · 컴포넌트 이름 그대로, 값은 지금 코드에서 읽은 값(없는 것만 틀 값, 본문에 표시)
- [x] `npx -y @google/design.md@0.4.0 lint DESIGN.md` 오류 0 (경고는 허용 목록 또는 본문에 이유)
- [x] `design/SCREENS.md`: 띄우는 명령 한 줄 + 표(화면 · 주소 · 폭 · 로그인 · 메모), 모든 화면(모달 · 빈 화면 · 오류 화면 포함)
- [x] 코드 파일 변경 없음(L0), 글꼴 · 아이콘 라이선스를 Typography · Iconography 에 적음

## 접근법
페이지마다 인라인 `<style>` 이라 CSS 변수가 없다. pokedex · movedex · itemdex · today · record · entry 의 색을 세어 많이 쓰는 값을 토큰으로, 크기는 Playwright 로 실제 요소를 재서 적는다. 버린 방법: 틀 값을 기본으로 두고 바꾼 것만 적기(사이트 모습과 달라져 드코에서 쓸모없음).

## 단계
1. 문서 읽기(DESIGN_SYSTEM · 틀 · DESIGN_RULES)
2. CSS 값 모으기 · 요소 크기 재기 · 대비 계산
3. DESIGN.md 쓰기 → lint
4. design/SCREENS.md 쓰기(화면 실제로 띄워 확인)
5. verify-task → 리뷰 → PR → L0 합치기 → 보고

## 결정 기록
- 2026-11-24 라이트 모드가 없다(어두운 화면 하나). P000 디자인 시스템 틀에 물어 "가"로: light · dark 둘 다 지금 사이트 값(같은 값). 이유: 드코 어느 모드에서도 사이트 모습 그대로
- 2026-11-24 primary = #e53935(P000 지정), primary-text = #ff6b6b(코드에 있는 값, 카드 바탕 #141414 위 6.6:1. #e53935 는 4.36:1 로 모자람)
- 2026-11-24 흰 글자 on #e53935 는 4.23:1(lint 경고). 코드 값 그대로 두고 본문에 고칠 거리로 적음(코드는 이 작업 범위 밖)
- 2026-11-24 `.assetsignore` 에 DESIGN.md · design/ 를 넣지 않음: 넣으면 배포 설정 변경이라 L3. 이번은 L0 로 두고 따로 보고
- 2026-11-24 띄우는 명령은 `node tests/serve.mjs 4102`(루트 package.json 을 만들지 않는 프로젝트라 `npm run dev` 가 없음)

- 2026-11-24 리뷰 1회차 막음 3건(배틀팀 API 실패 설명 · 오류 화면 누락 · admin 배포 여부 · 타입 색 세 벌) · 권함 8건을 모두 반영. 막음이 나와 레벨을 L0 → L1 로 올림(규칙)

- 2026-11-24 리뷰 2회차 막음 1건(배틀팀 실패 화면 문구가 실제로는 안 보임) 반영, 3회차 막음 없음
- 2026-11-24 `merge-level` L1 검사는 배포 중 프로젝트면 코드 0개여도 막는다. 그래서 `complete-task --level L1` 을 못 쓰고 프로젝트 세션에 합치기를 맡김

## 오류 기록
- 2026-11-24 `pkill -f "serve.mjs 4102"; verify-task` 가 exit 144: pkill 이 그 명령 줄 자체를 잡아 셸을 끔. 포트로 PID 를 찾아 끄는 방식으로 바꿈(`lsof -ti tcp:4102`)
<!-- 명령 · 메시지 핵심 · 원인 · 해결 · 로그 경로 -->

## 검증 결과
- verify-task 3회차 통과(f7b3a8d): 테스트 · 100줄 · 의존성 · 화면 · e2e · 문서 · 비밀값 통과, 린트 · 빌드는 명령 없음
- `npx -y @google/design.md@0.4.0 lint DESIGN.md` 오류 0 · 경고 31(고아 토큰 23 · motion 무시 1 · `#fff` on `#E53935` 4.23:1 7)
- 리뷰(새 에이전트) 1회차 막음 3 · 권함 8 → 반영, 2회차 막음 1 → 반영, 3회차 막음 없음
