---
id: 1118-harness-p001
project: P001
type: 설정
branch: claude/1118-harness-p001
port: 4100
status: 진행 중
created: 2026-11-18
---

# 실행 계획: harness-p001

## 목표
"내가 하는 모든 프로젝트에 하네스 다 적용시켜" (정혁님 2026-11-18)
= 포케노바(정적 HTML 도감 사이트)에 하네스 검증 환경을 붙인다. 사이트 동작은 바꾸지 않는다.

## 완료 기준
- [ ] `harness.json` · `ARCHITECTURE.md` · `docs/exec-plans/tech-debt-tracker.md` 가 있고, 기존 `CLAUDE.md` 는 틀에 맞춰 합쳐졌다
- [ ] Vitest 단위 테스트가 `index.html` 사본 일치 · 데이터 파일 정합(번호 · 이름 · 그림 파일)을 확인한다
- [ ] Playwright E2E 가 공개 페이지 7개(`/` · `/pokedex` · `/movedex` · `/itemdex` · `/entry` · `/record` · `/today`)를 PC · 390px 로 열어 콘솔 오류 · 우리 서버 실패 요청 · 가로 스크롤이 없음을 확인한다 (바깥 주소 차단, 포트 4150)
- [ ] 배포(Cloudflare · Vercel)가 새 파일 때문에 빌드 방식을 바꾸지 않는다 (루트에 `package.json` 을 두지 않음)
- [ ] 100줄 기준선 · 비밀값 첫 검사 결과가 tech-debt-tracker 에 있다
- [ ] `verify-task` 8가지가 통과한다

## 접근법
- 테스트 도구는 `tests/` 아래 따로 둔 개발용 `package.json` 에 넣는다. 루트에 `package.json` 이 생기면 Cloudflare Workers Builds 와 Vercel 이 의존성 설치 · 빌드 감지를 시작할 수 있어서다(확인할 수 없는 배포 대시보드 설정에 기대지 않음)
- 개발 서버는 의존성 없는 `tests/serve.mjs`(Node http). 배포와 같게 clean URL(`/pokedex` → `pokedex.html`)을 흉내 낸다
- 정적 HTML 이라 레이어 검사는 건너뜀(`stack: static`), 린트 · 빌드 명령은 없음
- 버린 방법: 루트 `package.json` + `.assetsignore` 로 막기. 대시보드 빌드 설정을 볼 수 없어 위험을 0 으로 만들 수 없다

## 단계
1. 전체 기준 첫 검사 (100줄 · 비밀값 · git 기록)
2. `tests/` 개발용 package.json · Vitest · Playwright · serve.mjs
3. harness.json · CLAUDE.md 합치기 · ARCHITECTURE.md · tech-debt-tracker · .gitignore · .assetsignore
4. 커밋 → verify-task (최대 5번) → PR

## 결정 기록
- 2026-11-18 · 실제 배포는 **Cloudflare Workers**(응답 `server: cloudflare`, RESUME 2026-07-12 이전). `projects.json` 의 `vercel` 은 옛 값. `harness.json` 의 `deploy` 는 `cloudflare` 로 적음
- 2026-11-18 · 테스트 도구를 `tests/package.json` 에 둔다. 루트 `package.json` 이 생기면 Cloudflare Workers Builds 는 의존성 설치를 시작하고(대시보드 빌드 명령은 볼 수 없음), Vercel 도 빌드 감지를 바꿀 수 있어서. 그래서 `vercel.json` 은 손대지 않았고 배포 방식은 그대로
- 2026-11-18 · `.assetsignore` 에 `tests` · `docs` · `logs` · `harness.json` · `ARCHITECTURE.md` 추가. 안 넣으면 개발 파일이 사이트 주소로 공개된다. 사이트 동작은 그대로(새 파일만 막음)
- 2026-11-18 · 개발 서버는 의존성 없는 `tests/serve.mjs`. 배포처럼 `/pokedex` → `pokedex.html`
- 2026-11-18 · `test_quick` 도 전체 실행. 단위 테스트가 import 가 아니라 파일을 읽어서 `--changed` 로는 데이터 · HTML 변경을 못 잡음(전체 0.2초)
- 2026-11-18 · E2E 에서 `admin.html`(운영 Firebase · 비밀번호) · `quiz.html`(배포 제외)은 뺐다. 바깥 주소는 전부 막아 실제 데이터에 닿지 않음
- 2026-11-18 · `@playwright/test` 는 1.63.0 고정(하네스 키트 · 설치된 브라우저와 같은 판)
- 2026-11-18 · `CLAUDE.md` 는 덮어쓰지 않고 틀(한 줄 소개 · 실행 · 규칙 · 빠른 참조)에 맞춰 기존 내용을 그대로 옮김. 낡은 설명(pochams API 경유 · vercel.app 301)은 고치지 않고 tech-debt-tracker 에 적음
- 2026-11-18 · 첫 검사에서 본 관리자 비밀번호 노출은 고치지 않고 보고만(사이트 동작 · 보안 변경이라 따로 작업)
- 2026-11-18 · 합치기 레벨 L3 (배포 중 · `.assetsignore`(배포 설정) · 개발 의존성 추가)

## 오류 기록

## 검증 결과
- 1차 전체 검사(하네스 붙이기 전): 100줄 넘는 파일 17개(전부 개발 스크립트) · 레이어 검사 없음(static) · 빌드 · 린트 없음 · 추적 파일 속 키 모양 3곳(관리자 비밀번호 1 · Firebase 웹 apiKey 2) · git 기록 속 7곳(같은 것들) · `.env` 커밋 기록 0
- 단위 16개 · E2E 22개(11개 × PC · 390px) 로컬 통과
