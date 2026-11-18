---
id: 1118-pokenova-security
project: P001
type: 수정
branch: claude/1118-pokenova-security
port: 4103
status: 진행 중
created: 2026-11-18
---

# 실행 계획: pokenova-security

## 목표
하네스 첫 검사에서 나온 보안 · 버그를 고친다("다 고쳐", 2026-11-18). 관리자 비밀번호 노출 · 옛 주소 이동 · 특성 영어 이름 겹침 · 폼 이로치 그림 빠짐 · CLAUDE.md 데이터 원천 설명.

## 완료 기준
- [x] `admin.html` 에 비밀번호 값 · 비밀번호 비교가 없고, 구글 로그인(Firebase Auth)으로 들어간다
- [x] 관리자만 읽고 지우게 하는 Firestore 보안 규칙 파일이 저장소에 있다(배포는 정혁님)
- [x] `vercel.json` 이 루트(`/`)도 새 주소로 보낸다
- [x] `quiz_abilities.json` 영어 이름이 겹치지 않고, 포켓몬 데이터의 특성 이름이 전부 특성 목록에 있다
- [x] 폼 전부 이로치 그림이 있다
- [x] `CLAUDE.md` 데이터 원천 설명이 로컬 `data/*.json` 기준이다
- [x] 위 항목마다 단위 시험이 있고 verify-task 통과

## 접근법
- 관리자: 클라이언트 비밀번호 비교를 지우고 Firebase Auth 구글 로그인으로 바꾼다. 실제 보호는 Firestore 보안 규칙(`firebase/firestore.rules`, 관리자 UID 만 읽기 · 고치기 · 지우기). 규칙 배포 · 구글 로그인 켜기 · UID 넣기는 정혁님 콘솔 일. 버린 방법: 비밀번호를 해시로 숨기기(클라이언트 비교라 여전히 우회됨)
- 옛 주소: 실측하니 `/pokedex` 등은 308 으로 넘어가는데 `/` 만 200. Vercel 의 `/:path*` 가 빈 경로(루트)를 못 잡는 것으로 보고 `/` 전용 규칙을 앞에 더한다
- 혼연일체: 저장소 `scripts/fetch_japanese_names.py` 의 `ABILITY_SLUG_BY_ID`(266 `as-one-glastrier`, 267 `as-one-spectrier`, PokeAPI 확인값)에 맞춰 `en` 을 나눈다. 포켓몬 데이터 참조도 설명으로 짝지어 맞춤
- 이로치: 기존 스크립트 `download_form_shiny_sprites.js` 의 (B) 경로(official-artwork shiny/{id}) 그대로 10261 한 장만 받는다. 전체 스크립트를 돌리면 pokedex.json 을 다시 쓰고 PokeAPI 를 280번 부르므로 버림
- 보안 규칙 · 로그인은 실제 Firebase 없이 시험하기 어려워 파일 내용 검사(단위)로 대신한다

## 단계
1. 재현 시험(실패 확인) 2. 데이터 · vercel.json 고침 3. admin 로그인 · 규칙 파일 4. CLAUDE.md 5. verify-task · PR

## 결정 기록
- 11-18 관리자 판별은 이메일이 아니라 UID 목록(`isAdmin`). 공개 저장소에 정혁님 이메일을 남기지 않으려고. 자리표시 `ADMIN_UID_HERE` 를 그대로 게시하면 아무도 관리자가 아니게(닫힌 쪽) 둠
- 11-18 규칙: 퀴즈 기록 3종은 누구나 `create`(quiz.html 이 남김), `leaderboard` 는 누구나 읽기(퀴즈 순위표), 나머지 읽기 · 고치기 · 지우기는 관리자만, 그 밖 문서는 막음
- 11-18 규칙 원본은 `firebase/firestore.rules`, `.assetsignore` 로 사이트에선 뺌. Firebase CLI(`firebase.json`)는 안 붙임(배포는 콘솔 붙여 넣기)
- 11-18 데이터 조회 함수가 오류를 삼키고 localStorage 로 넘어가던 것을 `permission-denied` 만 다시 던지게 함. 안 그러면 관리자가 아닌 계정이 빈 대시보드를 봄
- 11-18 혼연일체 영어 이름은 저장소의 PokeAPI 대응표(`ABILITY_SLUG_BY_ID`)를 `_` 로 바꾼 `as_one_glastrier` · `as_one_spectrier`. 폼 참조는 설명(블리자포스 · 레이스포스)으로 짝지음
- 11-18 이로치 1장은 스크립트 전체 대신 같은 URL 로 1장만 받음(pokedex.json 서식 · PokeAPI 280회 호출 피함)
- 11-18 옛 주소는 vercel.json 만 고침. Vercel 쪽 재배포 여부는 정혁님 확인

- 11-18 (리뷰 1회차 막음 3건 반영) 공개 create 에 키 · 길이 · 범위 검사. 정답 상한은 리뷰 예시 500 대신 2000: 능력치 문제 1287 · 포켓몬 1025 라 500 이면 정상 기록이 막힘. 오답 상한 100000(쉬움은 목숨 무한)
- 11-18 순위표 목록은 200개 제한. 정답 순 200개를 받으려고 orderBy(correct) 를 넣어 복합 인덱스(mode ↑ · correct ↓)가 필요해짐. quiz.html 은 배포 제외라 지금은 영향 없음, 퀴즈를 되살릴 때 인덱스 만들기(정혁님)
- 11-18 관리자 XSS: 신고 버튼은 data-id + 표 하나의 click 리스너, esc 에 ' 추가, 숫자 칸은 num() 으로 강제 변환
- 11-18 PROGRESS_LOG 의 옛 비밀번호 값 지움. git 기록에는 남는다

## 정혁님 할 일 (합친 뒤)
1. Firebase 콘솔 > Authentication > 로그인 방법: Google 사용 설정, 설정 > 승인된 도메인에 `pokenova.pochams.com` 추가
2. `/admin` 에서 한 번 로그인 → Authentication > 사용자 에서 UID 복사
3. Firestore Database > 규칙: `firebase/firestore.rules` 붙여 넣고 **`ADMIN_UID_HERE` 를 꼭 UID 로 바꾼 뒤** 게시
4. 옛 비밀번호는 공개 저장소 git 기록에 남음 → 같은 값을 다른 곳에 쓰면 바꾸기
5. Vercel 이 아직 GitHub 연결로 배포되는지 확인(옛 주소 루트 이동)
6. 퀴즈를 되살릴 때: Firestore 복합 인덱스 leaderboard (mode ↑, correct ↓)

## 오류 기록
- 첫 커밋에서 pre-commit 이 아직 고치지 않은 `security.test.mjs` 실패로 막음 → 데이터 커밋 동안 파일을 잠시 빼 두고 다음 커밋에 같이 넣음

## 검증 결과
- 단위 28개 통과(새 시험 11개), 관리자 페이지 헤드리스 확인: 로그인 화면 · 구글 로그인 버튼 · 콘솔 오류 0 (`logs/.../admin-login.png`)
- verify-task 1회차: 검사 8가지 통과, 계획 파일 미커밋으로만 실패 → 커밋 뒤 2회차 통과
- 리뷰 반영 뒤 단위 38개 통과(새 9개), 헤드리스로 악성 신고 id 를 넣어도 버튼이 같은 id 로 동작 · 대화창 0 · img 0
