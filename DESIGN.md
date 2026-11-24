---
version: alpha
name: Pokénova 포케노바
description: 포켓몬 팬이 PC · 폰으로 이로치 · 기술 · 도구를 찾아보는 어두운 도감 사이트. 검은 바탕에 몬스터볼 빨강 하나로 강조
colors:
  primary: "#E53935"
  on-primary: "#FFFFFF"
  primary-pressed: "#C62828"
  primary-disabled: "#7D2725"
  primary-container: "#1A0000"
  secondary: "#F5C518"
  on-secondary: "#000000"
  error: "#E53935"
  on-error: "#FFFFFF"
  success: "#4CAF50"
  warning: "#FF9800"
  chart-1: "#3355FF"
  chart-2: "#E0691A"
  chart-3: "#1EA672"
  chart-4: "#A259FF"
  chart-5: "#E5484D"
  chart-6: "#0B8FB0"
  light:
    surface: "#0A0A0A"
    surface-muted: "#141414"
    surface-raised: "#1E1E1E"
    surface-sunken: "#0F0F0F"
    on-surface: "#F0F0F0"
    on-surface-variant: "#BBBBBB"
    on-surface-muted: "#888888"
    outline: "#252525"
    outline-strong: "#333333"
    primary-text: "#FF6B6B"
    error-text: "#FF6B6B"
    success-text: "#4CAF50"
    inverse-surface: "#1E1E1E"
    on-inverse-surface: "#F0F0F0"
    chart-grid: "#252525"
  dark:
    surface: "#0A0A0A"
    surface-muted: "#141414"
    surface-raised: "#1E1E1E"
    surface-sunken: "#0F0F0F"
    on-surface: "#F0F0F0"
    on-surface-variant: "#BBBBBB"
    on-surface-muted: "#888888"
    outline: "#252525"
    outline-strong: "#333333"
    primary-text: "#FF6B6B"
    error-text: "#FF6B6B"
    success-text: "#4CAF50"
    inverse-surface: "#1E1E1E"
    on-inverse-surface: "#F0F0F0"
    chart-grid: "#252525"
typography:
  headline-lg:
    fontFamily: Noto Sans KR, Segoe UI
    fontSize: 26px
    fontWeight: 900
    lineHeight: 1.1
    letterSpacing: -0.5px
  headline-md:
    fontFamily: Noto Sans KR, Segoe UI
    fontSize: 20px
    fontWeight: 900
    lineHeight: 1.3
  title:
    fontFamily: Noto Sans KR, Segoe UI
    fontSize: 18px
    fontWeight: 900
    lineHeight: 1.4
    letterSpacing: -0.5px
  body-lg:
    fontFamily: Noto Sans KR, Segoe UI
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.6
  body-md:
    fontFamily: Noto Sans KR, Segoe UI
    fontSize: 12.8px
    fontWeight: 400
    lineHeight: 1.5
  input:
    fontFamily: Noto Sans KR, Segoe UI
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.4
  label-lg:
    fontFamily: Noto Sans KR, Segoe UI
    fontSize: 14.4px
    fontWeight: 700
    lineHeight: 1.3
  label-md:
    fontFamily: Noto Sans KR, Segoe UI
    fontSize: 14px
    fontWeight: 600
    lineHeight: 1.3
  caption:
    fontFamily: Noto Sans KR, Segoe UI
    fontSize: 11px
    fontWeight: 500
    lineHeight: 1.4
rounded:
  xs: 4px
  sm: 8px
  md: 10px
  lg: 14px
  xl: 24px
  full: 999px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  xxl: 48px
motion:
  state-change:
    duration: 150ms
    timingFunction: cubic-bezier(0.25, 0.1, 0.25, 1)
  selection:
    duration: 200ms
    timingFunction: cubic-bezier(0.25, 0.1, 0.25, 1)
  surface-enter:
    duration: 200ms
    timingFunction: cubic-bezier(0.25, 0.1, 0.25, 1)
  surface-exit:
    duration: 200ms
    timingFunction: cubic-bezier(0.3, 0, 1, 1)
  screen-enter:
    duration: 400ms
    timingFunction: cubic-bezier(0.05, 0.7, 0.1, 1)
  screen-exit:
    duration: 200ms
    timingFunction: cubic-bezier(0.3, 0, 0.8, 0.15)
  reveal:
    duration: 500ms
    timingFunction: cubic-bezier(0.34, 1.56, 0.64, 1)
  toast-enter:
    duration: 350ms
    timingFunction: cubic-bezier(0.34, 1.56, 0.64, 1)
components:
  # 버튼
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.label-lg}"
    rounded: 12px
    height: 47px
    padding: 28px
  button-primary-pressed:
    backgroundColor: "{colors.primary-pressed}"
    textColor: "{colors.on-primary}"
  button-primary-disabled:
    backgroundColor: "{colors.primary-disabled}"
    textColor: "{colors.on-primary}"
  button-secondary:
    backgroundColor: "{colors.light.surface-raised}"
    textColor: "{colors.light.on-surface-variant}"
    typography: "{typography.label-md}"
    rounded: 9px
    height: 42px
    padding: 14px
  button-ghost:
    backgroundColor: "{colors.light.surface}"
    textColor: "{colors.light.on-surface-muted}"
    typography: "{typography.label-lg}"
    rounded: 12px
    height: 47px
    padding: 20px
  button-danger:
    backgroundColor: "{colors.error}"
    textColor: "{colors.on-error}"
    typography: "{typography.label-md}"
    rounded: "{rounded.md}"
    height: 44px
    padding: 18px
  button-small:
    backgroundColor: "{colors.light.surface}"
    textColor: "{colors.light.on-surface-muted}"
    typography: "{typography.label-md}"
    rounded: "{rounded.full}"
    height: 36px
    padding: 12px
  button-icon:
    backgroundColor: "{colors.light.surface}"
    textColor: "{colors.light.on-surface-variant}"
    rounded: "{rounded.sm}"
    size: 40px
  fab:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.lg}"
    size: 56px
  # 입력
  input:
    backgroundColor: "{colors.light.surface-sunken}"
    textColor: "{colors.light.on-surface}"
    typography: "{typography.input}"
    rounded: "{rounded.md}"
    height: 40px
    padding: 14px
  input-error:
    backgroundColor: "{colors.light.surface}"
    textColor: "{colors.light.error-text}"
    typography: "{typography.caption}"
  textarea:
    backgroundColor: "{colors.light.surface-sunken}"
    textColor: "{colors.light.on-surface}"
    typography: "{typography.input}"
    rounded: "{rounded.md}"
    height: 82px
    padding: 14px
  search-field:
    backgroundColor: "{colors.light.surface-sunken}"
    textColor: "{colors.light.on-surface}"
    typography: "{typography.input}"
    rounded: "{rounded.full}"
    height: 43px
    padding: 18px
  select:
    backgroundColor: "{colors.light.surface}"
    textColor: "{colors.light.on-surface}"
    typography: "{typography.input}"
    rounded: "{rounded.md}"
    height: 40px
    padding: 14px
  checkbox:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    rounded: 4px
    size: 20px
  radio:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.full}"
    size: 20px
  switch-on:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.full}"
    width: 48px
    height: 28px
  switch-off:
    backgroundColor: "{colors.light.outline-strong}"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.full}"
    width: 48px
    height: 28px
  slider:
    backgroundColor: "{colors.primary}"
    rounded: "{rounded.full}"
    height: 4px
  # 표시
  chip:
    backgroundColor: "{colors.light.surface-raised}"
    textColor: "{colors.light.on-surface}"
    typography: "{typography.label-md}"
    rounded: "{rounded.full}"
    height: 36px
    padding: 12px
  chip-selected:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.label-md}"
    rounded: "{rounded.full}"
    height: 36px
    padding: 12px
  badge:
    backgroundColor: "{colors.light.surface-raised}"
    textColor: "{colors.light.on-surface-muted}"
    typography: "{typography.caption}"
    rounded: "{rounded.full}"
    height: 23px
    padding: 10px
  avatar:
    backgroundColor: "{colors.light.surface-muted}"
    textColor: "{colors.light.on-surface}"
    typography: "{typography.label-md}"
    rounded: "{rounded.full}"
    size: 40px
  tooltip:
    backgroundColor: "{colors.light.inverse-surface}"
    textColor: "{colors.light.on-inverse-surface}"
    typography: "{typography.caption}"
    rounded: "{rounded.sm}"
    padding: 8px
  progress-bar:
    backgroundColor: "{colors.primary}"
    rounded: "{rounded.full}"
    height: 3px
  progress-track:
    backgroundColor: "{colors.light.outline}"
    rounded: "{rounded.full}"
    height: 3px
  skeleton:
    backgroundColor: "{colors.light.surface-raised}"
    rounded: 6px
  divider:
    backgroundColor: "{colors.light.outline}"
    height: 1px
  # 묶음
  card:
    backgroundColor: "{colors.light.surface-muted}"
    textColor: "{colors.light.on-surface}"
    rounded: "{rounded.lg}"
    padding: 14px
  card-muted:
    backgroundColor: "{colors.light.surface-raised}"
    textColor: "{colors.light.on-surface}"
    rounded: "{rounded.md}"
    padding: 14px
  list-item:
    backgroundColor: "{colors.light.surface-muted}"
    textColor: "{colors.light.on-surface}"
    typography: "{typography.body-lg}"
    rounded: 12px
    height: 59px
    padding: 18px
  empty-state:
    backgroundColor: "{colors.light.surface}"
    textColor: "{colors.light.on-surface-muted}"
    typography: "{typography.body-lg}"
    padding: 80px
  stat:
    backgroundColor: "{colors.light.surface-muted}"
    textColor: "{colors.light.on-surface}"
    typography: "{typography.headline-lg}"
    rounded: 16px
    padding: 16px
  # 이동
  top-app-bar:
    backgroundColor: "{colors.light.surface-muted}"
    textColor: "{colors.light.on-surface}"
    typography: "{typography.title}"
    height: 60px
    padding: 24px
  bottom-tab-bar:
    backgroundColor: "{colors.light.surface}"
    textColor: "{colors.light.on-surface-muted}"
    typography: "{typography.caption}"
    height: 64px
  bottom-tab-item-active:
    backgroundColor: "{colors.light.surface}"
    textColor: "{colors.light.primary-text}"
    typography: "{typography.caption}"
  tabs:
    backgroundColor: "{colors.light.surface-sunken}"
    textColor: "{colors.light.on-surface-muted}"
    typography: "{typography.label-md}"
    rounded: "{rounded.full}"
    height: 36px
    padding: 18px
  tab-active:
    backgroundColor: "{colors.primary-container}"
    textColor: "{colors.light.on-surface}"
    typography: "{typography.label-md}"
  segmented-control:
    backgroundColor: "{colors.light.surface-muted}"
    textColor: "{colors.light.on-surface}"
    typography: "{typography.label-md}"
    rounded: "{rounded.md}"
    height: 36px
    padding: 4px
  segmented-item-active:
    backgroundColor: "{colors.light.surface}"
    textColor: "{colors.light.on-surface}"
    typography: "{typography.label-md}"
    rounded: "{rounded.sm}"
  pagination:
    backgroundColor: "{colors.light.surface}"
    textColor: "{colors.light.on-surface}"
    typography: "{typography.label-md}"
    rounded: "{rounded.sm}"
    size: 36px
  # 겹쳐 뜨는 것
  menu:
    backgroundColor: "{colors.light.surface-muted}"
    textColor: "{colors.light.on-surface}"
    typography: "{typography.body-md}"
    padding: 16px
  menu-item:
    backgroundColor: "{colors.light.surface-raised}"
    textColor: "{colors.light.on-surface-variant}"
    typography: "{typography.label-md}"
    rounded: "{rounded.md}"
    height: 44px
    padding: 16px
  dialog:
    backgroundColor: "{colors.light.surface-muted}"
    textColor: "{colors.light.on-surface}"
    typography: "{typography.body-md}"
    rounded: "{rounded.xl}"
    padding: 28px
    width: 480px
  bottom-sheet:
    backgroundColor: "{colors.light.surface}"
    textColor: "{colors.light.on-surface}"
    typography: "{typography.body-md}"
    rounded: "{rounded.lg}"
    padding: 16px
  toast:
    backgroundColor: "{colors.light.inverse-surface}"
    textColor: "{colors.light.on-inverse-surface}"
    typography: "{typography.label-md}"
    rounded: "{rounded.full}"
    padding: 22px
  # 그래프 (점 + 선, DESIGN_RULES)
  chart-line:
    backgroundColor: "{colors.chart-1}"
    size: 2px
  chart-point:
    backgroundColor: "{colors.chart-1}"
    size: 6px
  chart-point-today:
    backgroundColor: "{colors.chart-1}"
    size: 10px
  chart-grid:
    backgroundColor: "{colors.light.chart-grid}"
    height: 1px
  chart-axis:
    backgroundColor: "{colors.light.surface}"
    textColor: "{colors.light.on-surface-muted}"
    typography: "{typography.caption}"
---

<!-- 틀: ~/.claude/harness/templates/DESIGN.md · 규칙: ~/.claude/docs/DESIGN_SYSTEM.md
     값은 위 앞머리 YAML 이 기준이다. 아래 본문은 이유와 쓰는 법만 적고 값을 다시 적지 않는다.
     절 제목(## Colors 등)은 도구가 찾는 이름이라 영어 그대로 둔다. 검사: npx -y @google/design.md@0.4.0 lint DESIGN.md
     2026-11-24 지금 코드(pokedex · movedex · itemdex · today · record · entry 의 인라인 <style>)에서 읽어 만들었다. 코드는 아직 이 값을 변수로 쓰지 않는다 -->

## Overview

포켓몬 팬이 PC · 폰에서 이로치 색 · 기술 · 도구를 찾아보는 도감 사이트. 검은 바탕 위에 포켓몬 그림과 타입 색이 주인공이고, 사이트 색은 몬스터볼 빨강(`primary`) 하나로만 강조한다. 장식보다 그림이 먼저 보이게.

화면은 페이지마다 인라인 `<style>` 로 따로 쓰여 있고 CSS 변수가 없다. 이 파일은 그 값들을 모아 하나로 정한 기준이다. 비슷한 값이 섞여 있던 곳은 하나로 묶었고(아래 Colors), 지금 코드와 다른 값은 맨 아래 "지금 코드와 다른 곳"에 모았다.

`admin.html`(관리자)은 남색 바탕 · 노랑 강조로 따로 만든 화면이라 이 기준 밖이다(배포 화면 아님).

## Colors

- **라이트 모드 없음.** 어두운 화면 하나라 `light` · `dark` 같은 값(P000 디자인 시스템 틀과 정함, 2026-11-24). 드코 어느 모드에서도 사이트 모습 그대로 나온다
- **primary** `#E53935`: 지금 보는 메뉴 · 선택된 칩 · 저장 버튼 · 입력칸 포커스 테두리 · 로고 "nova". 화면마다 주 버튼은 하나
- **primary-pressed**: 저장 버튼 마우스 올림(`.btn-save:hover`). **primary-disabled**: 코드는 비활성 버튼을 `opacity: 0.5` 로 흐리게 한다. 카드 바탕(`#141414`) 위 50% 색을 계산해 넣음
- **primary-container**: 고른 배틀팀 탭 바탕(`.team-tab.active`)
- **secondary** `#F5C518`: 오늘의 포켓몬의 금색(제목 강조 · "보관하기" 버튼, 글자는 검정)
- **warning** `#FF9800`: 오류 신고(버튼 · 고른 신고 유형 · 숨겨진 특성 표시). **success**: 저장 완료 글자 · 놓아주기
- **error**: 사이트에 따로 된 오류 색이 없어 `primary` 와 같은 빨강. 위험 버튼(초기화 · 지우기)은 평소 회색, 마우스를 올리면 빨강
- **surface** 페이지 바탕, **surface-muted** 헤더 · 카드 · 창, **surface-raised** 메뉴 버튼 · 칩 · 개수 배지 · 창 안 항목, **surface-sunken** 입력칸 · 오늘의 포켓몬 안쪽 칸 · 배틀팀 슬롯
  - 코드에는 `#1a1a1a` · `#1c1c1c` · `#1e1e1e` 와 `#0d0d0d` · `#0f0f0f` · `#111` 이 섞여 있다. 각각 `surface-raised` · `surface-sunken` 으로 묶었다
- **on-surface** 본문 글자, **on-surface-variant** 메뉴 버튼 글자(`#bbb`), **on-surface-muted** 라벨 · 개수 · 영어 이름
- **outline** 카드 · 헤더 · 창 둘레, **outline-strong** 메뉴 버튼 · 칩 · 기술 도감 검색칸 테두리
- **primary-text · error-text** `#FF6B6B`: 어두운 바탕 위 빨강 글자. `#E53935` 는 카드 바탕(`#141414`) 위 4.36:1 로 모자라 코드에 있던 밝은 빨강(거다이 전용기 이름)을 씀(카드 위 6.6:1)
- **inverse-surface**: 뒤집힌 색이 아니라 토스트 바탕(오늘의 포켓몬 토스트 `#1e1e1e`). 툴팁도 같은 색으로
- **chart-1~6**: 그래프 없음(틀 값). **chart-grid** 는 능력치 막대 바탕(`#252525`)
- **타입 색 · 지역 배지 색**은 게임 데이터 색이라 토큰에 넣지 않았다. 다만 포켓몬 도감(`#EE8130` 불꽃 등)과 기술 · 오늘의 포켓몬(`#e53935` 불꽃 등)이 서로 다른 18색을 쓴다. 맞출 때는 포켓몬 도감 쪽 하나로
- 글자와 바탕 대비 4.5:1 이상(본문), 3:1 이상(큰 제목 · 아이콘)

## Typography

| 글꼴 | 출처 · 라이선스 | 쓰는 곳 | 파일 |
|---|---|---|---|
| Noto Sans KR | Google Fonts (SIL OFL 1.1, 상업 · 웹 사용 가능) | 한글 · 영어 전체 | 파일 없음. `pokedex` · `index` · `entry` 가 Google Fonts 주소(`family=Noto+Sans+KR:wght@400;500;700;900`)로 부른다 |
| Segoe UI | 윈도우 기본 글꼴(Microsoft, 내려받아 싣지 않음) | 두 번째 글꼴 | 없음. `movedex` · `itemdex` · `today` · `record` 는 Segoe UI 가 먼저이고 Noto Sans KR 을 부르지 않아 맥 · 폰에서는 기기 기본 글꼴로 보인다 |

- 공개 저장소라 Fontshare Closed Source 글꼴(Satoshi 등) 파일은 올리지 않는다. 쓰게 되면 Fontshare 웹 주소로(DESIGN_SYSTEM.md "Fontshare")
- 굵기는 400 · 500 · 600 · 700 · 900. 이름 · 제목은 900, 버튼 · 칩 600~700
- 코드는 `rem` 을 쓴다(`0.82rem` 등). 여기서는 `px` 로 바꿔 적었다(드코가 `em` · `rem` 을 못 읽음)
- 입력칸은 `input` 스타일 16px(아이폰 확대 방지, DESIGN_RULES). PC 검색칸은 지금 15px
- 버튼 글씨는 14px 아래로 내리지 않는다(DESIGN_RULES). 지금 메뉴 버튼 13.12px · 칩 12.48px 은 규칙에 못 미침
- 한글 줄바꿈: `word-break: keep-all` 은 포켓몬 카드 이름에만 있다. 새 화면은 `body` 에 둔다(DESIGN_RULES)

## Layout

- 본문 최대 폭: 포켓몬 도감 그리드 1400px, 헤더 · 기술 · 도구 도감 1200px, 배틀팀 960px, 오늘의 포켓몬 520px, 바닥글 700px
- 포켓몬 카드 그리드는 칸 최소 130px(폰 100px · 480px 아래 88px), 간격 12px(폰 8px). 기술 · 도구 카드는 칸 최소 300px, 폰은 한 줄
- 간격은 `spacing` 값만 쓴다. 헤더 좌우 `lg`(폰 12px), 카드 사이 12px, 절 사이 `xl`
- 끊는 폭: 768px(헤더 검색칸이 두 번째 줄로), 600px(햄버거 메뉴), 480px · 380px(글자 · 칸 줄임)

## Elevation & Depth

층은 바탕 색 차이(`surface` → `surface-muted` → `surface-raised`)와 `outline` 선으로 나눈다. 그림자는 떠 있는 것에만: 창(`0 20px 60px` 검정 80%), 폰 메뉴(`0 8px 24px` 검정 50%), 토스트. 창 뒤는 검정 75% 막과 흐림 4px.

## Shapes

- 단계: xs 4(배틀팀 기술 칸) · sm 8(신고 유형 · 햄버거) · md 10(기술 · 도구 카드 · 특성 줄 · 입력칸) · lg 14(포켓몬 카드) · xl 24(창) · full(칩 · 타입 배지 · 검색칸 · 토스트, 코드는 `20px` · `50px`)
- 버튼은 12px(저장 · 신고하기), 메뉴 버튼은 9px. 이 둘은 단계 밖이라 컴포넌트에 값으로 적었다
- 배틀팀 슬롯 · 기록 카드 16px, 오늘의 포켓몬 카드 18px, 신고 창 20px 도 단계 밖. 새로 만들 땐 단계 값으로

## Motion & Micro-interaction

- 마우스 올림 · 눌림 `state-change`(코드 `.15s`, 곡선 지정 없음 = ease), 탭 · 칸 바뀜 `selection`(`.2s`), 창 열림 `surface-enter`(`modalIn .2s ease`, 작게 + 아래에서 커지며 나타남)
- 창 닫힘 · 화면 전환 움직임 없음(`surface-exit` · `screen-enter` · `screen-exit` 은 틀 값). 페이지가 따로따로라 화면 전환이 없다
- `reveal`: 오늘의 포켓몬 카드가 튀어나오는 움직임(살짝 넘쳤다 돌아오는 곡선). `toast-enter`: 토스트가 아래에서 튀어 오름
- 포켓몬 카드에 마우스를 올리면 4px 위로 뜨고 둘레가 빨강
- 오늘의 포켓몬 그림이 3초마다 위아래로 떠다니는 반복 움직임이 있다. 새로 만들 땐 꾸밈용 반복 움직임을 넣지 않는다
- 웹이라 간단한 전환은 CSS. 스크롤 따라 움직이는 연출이 필요하면 GSAP. 움직임 줄이기 설정(`prefers-reduced-motion`)은 지금 코드에 없다

## Iconography

- **아이콘 팩 없음.** 지금은 두 가지를 아이콘으로 쓴다
  - 이모지(돋보기 · 반짝이 · 경고 · 햄버거 `☰` 등): 기기 글꼴로 그려져 기기마다 모양이 다르다. 라이선스 걱정 없음
  - 몬스터볼 그림(`sprites/items/*.png`, 메뉴 버튼 24px): PokeAPI sprites 저장소에서 받은 게임 그림. 권리는 Nintendo · Game Freak · Creatures(팬 사이트로 바닥글에 표기)
- 로고의 몬스터볼은 그림이 아니라 CSS 로 그린다(`.logo-ball`)
- 새 아이콘이 필요하면 팩 하나만: **Lucide** (ISC, `@iconify-json/lucide`), 선 굵기 2px, 16 · 20 · 24px. 빌드 도구가 없는 정적 사이트라 쓸 SVG 만 저장소에 복사하고 LICENSE 를 같이 둔다. 이모지 아이콘과 섞어 쓰지 않는다

## Voice & Content Strategy

`~/.claude/ux-writing.md` 를 따른다. 말을 거는 문장(토스트 · 확인 창 · 오류)만 해요체, 라벨 · 상태 · 빈 화면은 단어로 끝낸다("검색 결과 없음"). 버튼은 누르면 일어나는 일("저장하기", "신고하기").

포켓몬 · 기술 · 특성 · 도구 이름은 코드에 적지 않고 `data/*.json` 에서 가져온다(CLAUDE.md "게임/도메인 명칭 규칙").

## Components

| 묶음 | 컴포넌트 | 쓰는 곳 |
|---|---|---|
| 버튼 | `button-primary`(+ `-pressed` · `-disabled`) · `button-secondary` · `button-ghost` · `button-danger` · `button-small` · `button-icon` · `fab` | 주 버튼 = 배틀팀 "저장하기". secondary = 헤더 메뉴 버튼(`.site-nav-btn`). ghost = "전체 초기화" · 창 "취소". small = "전체 해제"(`.btn-clear-section`). icon = 햄버거. 채운 위험 버튼 · FAB 없음(틀 값) |
| 입력 | `input` · `input-error` · `textarea` · `search-field` · `select` · `checkbox` · `radio` · `switch-on` · `switch-off` · `slider` | search-field = 포켓몬 도감 헤더 검색칸 · 배틀팀 창 검색칸. textarea = 오류 신고 메모. 선택 상자 · 체크 · 스위치 · 슬라이더 없음(틀 값), 입력칸 오류 문구 없음 |
| 표시 | `chip` · `chip-selected` · `badge` · `avatar` · `tooltip` · `progress-bar` · `progress-track` · `skeleton` · `divider` | chip = 분류 · 세대 · 타입 거르기(`.filter-btn` · `.chip`). 세대 칩은 고르면 파랑(`#2563eb`), 타입 칩은 그 타입 색. badge = 개수(`0 / 6` · 컬렉션 `0마리`). progress = 오늘의 포켓몬 능력치 막대(채움 색은 능력치마다 다름). skeleton = 도구 그림 자리. 아바타 · 툴팁 없음(틀 값) |
| 묶음 | `card` · `card-muted` · `list-item` · `empty-state` · `stat` | card = 포켓몬 카드. card-muted = 창 안 특성 줄 · 폼 카드. list-item = 내 기록 게임 줄. empty-state = "검색 결과 없음" · 기록 없음. stat = 내 기록 최고 점수 카드(점수는 빨강) |
| 이동 | `top-app-bar` · `bottom-tab-bar` · `bottom-tab-item-active` · `tabs` · `tab-active` · `segmented-control` · `segmented-item-active` · `pagination` | top-app-bar = 헤더(로고 · 검색 · 메뉴 버튼, 600px 아래 햄버거). 오늘의 포켓몬 · 내 기록은 52px 고정 헤더(반투명 + 흐림). tabs = 배틀팀1~3 탭(고르면 빨강 둘레). 하단 탭 · 나눔 버튼 · 쪽 번호 없음(틀 값) |
| 겹쳐 뜨는 것 | `menu` · `menu-item` · `dialog` · `bottom-sheet` · `toast` | menu = 폰 햄버거 메뉴(헤더 아래 전체 폭). dialog = 포켓몬 · 특성 · 기술 상세 창, 오류 신고 창, 배틀팀 고르기 창. 아래 시트 없음(틀 값). toast = 오늘의 포켓몬 "보관했어요" |
| 그래프 | `chart-line` · `chart-point` · `chart-point-today` · `chart-grid` · `chart-axis` | 그래프 없음(틀 값). 만들게 되면 점 + 선(DESIGN_RULES) |

새 컴포넌트가 필요하면 같은 이름 규칙(`묶음-변형`, 상태는 `-pressed` · `-disabled` · `-active`)으로 앞머리에 먼저 더한다.

## Do's and Don'ts

- Do: 새 색 · 글자 크기가 필요하면 이 파일 앞머리에 먼저 더한다
- Do: 빨강은 화면마다 지금 위치 · 주 버튼 · 선택에만. 그림과 타입 색이 주인공
- Don't: 아이콘 팩을 섞지 않는다(이모지와 SVG 아이콘도)
- Don't: 브라우저 기본 `<select>` 를 쓰지 않는다(디자인된 팝오버 메뉴, DESIGN_RULES)
- Don't: 회색 글자를 `#555` · `#444` 처럼 바탕 대비 4.5:1 아래로 내리지 않는다

### 지금 코드와 다른 곳 (고칠 거리, 2026-11-24)

이 파일은 아래 값을 규칙 쪽으로 적었다. 코드를 고칠 때 맞춘다.

| 무엇 | 지금 코드 | 이 파일 |
|---|---|---|
| 흰 글자 on 빨강 버튼 대비 | 4.23:1 (`#fff` on `#e53935`, 4.5:1 미달) | 값은 그대로. 고친다면 버튼 바탕을 `primary-pressed` 쪽으로 |
| 흐린 글자 | `#555` · `#444` · `#666`(빈 화면 · 바닥글 · 초기화 버튼 · 탭, 바탕 대비 2.3~3.5:1) | `on-surface-muted` `#888`(5.6:1) |
| 작은 버튼 높이 · 글씨 | "전체 해제" 28px · PC 칩 27~30px, 글씨 12~13px | 36px · 14px(DESIGN_RULES) |
| 폰 창 | 가운데 뜨는 창 | DESIGN_RULES 는 폰에서 아래 시트 |
| 테두리 대비 | `outline-strong` `#333`(바탕 대비 1.6:1, 3:1 미달) | 값은 그대로. 입력칸 테두리를 고칠 때 `#555` 이상 |
| 글꼴 | 4개 페이지가 Noto Sans KR 을 부르지 않음 | 전 페이지 Noto Sans KR |
| 타입 색 | 포켓몬 도감과 기술 · 오늘의 포켓몬이 다른 18색 | 포켓몬 도감 쪽 하나 |
