---
source: blog
creator: adam-wathan
url: https://adamwathan.me/dont-use-em-for-media-queries
title: Don't Use Em for Media Queries
published_at: 2017-11-30
collected_at: 2026-04-15
categories: ["web-app"]
insight_extracted_at: 2026-04-15
---

## 핵심 주장 (≤5)
1. Safari 확대(zoom) 환경에서 문제를 일으키는 것은 `px` 미디어 쿼리가 아니라 `em` 미디어 쿼리다.
2. Safari는 확대 시 `em` 브레이크포인트를 의도보다 훨씬 늦게 발동시켜 반응형 레이아웃을 과도하게 늦게 변경한다.
3. 공통적으로 쓰이는 브라우저 전반에서 일관되게 동작하는 단위는 픽셀이므로, 당시 기준으로 미디어 쿼리에는 `px`를 쓰는 편이 낫다.
4. 사용자가 브라우저 기본 글꼴 크기를 바꾸면 `px` 기반 브레이크포인트가 설계와 다르게 동작할 수 있지만, 작성자 경험상 실사용 문제 제보는 없었다.
5. 루트 폰트 크기를 픽셀로 고정하면 기본 글꼴 크기 커스터마이징을 무시하게 되어 접근성 측면에서 더 나쁠 수 있다.

## 공개된 숫자·지표
- 기본 글꼴 크기: `16px` (기간: 예시 설명, 출처: "In this example you can see that the backgrounds change at the same time, because 25em at the default font size of 16px matches the 400px breakpoint.")
- 픽셀 브레이크포인트 예시: `400px` (기간: 테스트 예시, 출처: "Here I've got two containers set to change their background color at 400px and 25em respectively, with the zoom set to normal (100%):")
- em 브레이크포인트 예시: `25em` (기간: 테스트 예시, 출처: "Here I've got two containers set to change their background color at 400px and 25em respectively, with the zoom set to normal (100%):")
- 기본 확대 비율: `100%` (기간: 테스트 예시, 출처: "Here I've got two containers set to change their background color at 400px and 25em respectively, with the zoom set to normal (100%):")
- Safari 확대 비율: `150%` (기간: 테스트 예시, 출처: "Here it's clear that Safari is triggering the pixel breakpoint much sooner than it triggers the `em` breakpoint.")
- Safari에서 `400px` 브레이크포인트 발동 시점: `600px` (기간: Safari 150% 확대 테스트, 출처: "Interesting! Safari is triggering the 400px breakpoint at 600px when zoomed to 150% (the correct behavior) but it's triggering the `25em` breakpoint at 900px, which makes no sense at all.")
- Safari에서 `25em` 브레이크포인트 발동 시점: `900px` (기간: Safari 150% 확대 테스트, 출처: "Interesting! Safari is triggering the 400px breakpoint at 600px when zoomed to 150% (the correct behavior) but it's triggering the `25em` breakpoint at 900px, which makes no sense at all.")
- 레이아웃 예시 뷰포트 폭: `약 960px` (기간: practical consequences 예시, 출처: "Here's what it might look like at around 960px wide:")
- 축소 비교 대상 뷰포트 폭: `640px` (기간: Safari 150% 확대에서 px 미디어 쿼리 예시, 출처: "The layout drops to two columns, like you'd see at 640px viewport size.")
- 운영 중인 사이트 규모: `매월 수백만 명의 순방문자` (기간: 작성자의 운영 경험, 출처: "I maintain sites with millions of unique visitors each month and haven't once had someone report a layout issue because of this, so even though this certainly sucks, it seems like in practice it's not causing sites to become truly unusable.")

## 언급된 도구·서비스
- Safari: 확대 시 `px`와 `em` 미디어 쿼리의 발동 시점을 비교하는 핵심 테스트 대상 브라우저
- Chrome: Safari, Firefox와 함께 `px`/`em` 단위 비교 스크린샷에 포함된 브라우저
- Firefox: Safari, Chrome과 함께 `px`/`em` 단위 비교 스크린샷에 포함된 브라우저
- JSFiddle: `400px`와 `25em` 브레이크포인트 동작을 재현하는 예제 링크로 사용됨

## 언급된 다른 creator·앱
- Zell Liew: `PX, EM, or REM Media Queries?` 글에서 `em` 단위를 추천했고, 이 글은 그 결론을 재검증하는 맥락에서 작성됨
- JSFiddle: 미디어 쿼리 동작을 직접 확인할 수 있는 예제 호스팅 도구로 언급됨

## 복제 가능한 전술 (≤3)
1. Safari 확대 환경에서 `px`와 `em` 미디어 쿼리의 발동 시점을 동일 조건으로 비교 테스트한다.
   - 구체적 스텝: 동일한 레이아웃 블록 2개를 만들고 각각 `400px`, `25em` 브레이크포인트를 설정한 뒤 Safari에서 `100%`와 `150%` 확대 상태로 배경색이나 컬럼 수 변화를 비교한다.
   - 예상 리소스: Safari, 간단한 테스트 페이지 또는 JSFiddle, 짧은 수동 검증 시간
   - 예상 효과: 확대 시 어떤 단위가 더 늦거나 빠르게 발동하는지 브라우저별 차이를 직접 확인할 수 있다.
2. 반응형 컬럼 레이아웃 검증 시 텍스트 크기와 브레이크포인트 발동 시점을 함께 본다.
   - 구체적 스텝: 타일형 다단 레이아웃을 준비하고 동일한 텍스트 렌더링 크기 조건에서 `px` 기반과 `em` 기반 미디어 쿼리가 각각 몇 컬럼으로 바뀌는지 비교한다.
   - 예상 리소스: 반응형 샘플 레이아웃, Safari/Chrome/Firefox
   - 예상 효과: 단순 브레이크포인트 값 비교가 아니라 실제 사용자가 보는 컬럼 붕괴 시점 차이를 확인할 수 있다.
3. 접근성 타협안을 선택할 때 루트 폰트 고정 대신 실제 사용자 불편 신고 여부를 우선 확인한다.
   - 구체적 스텝: 기본 글꼴 크기 변경으로 인한 경미한 레이아웃 깨짐 가능성을 문서화하고, 루트 폰트 크기를 강제로 픽셀 고정하기 전에 사용자 제보나 지원 채널 이슈가 실제로 있는지 검토한다.
   - 예상 리소스: 운영 중인 사이트의 사용자 피드백 채널, 현재 CSS 설정 검토
   - 예상 효과: 접근성 저하를 감수하는 강제 설정 없이도 실제 문제 빈도를 기준으로 의사결정할 수 있다.

## 원문 요약 (≤5문장)
이 글은 Safari 확대 환경에서 `px`와 `em` 미디어 쿼리 중 무엇이 더 올바르게 동작하는지 재검증한 글이다. 작성자는 테스트 결과 Safari의 문제는 `px`가 아니라 `em` 미디어 쿼리가 확대 시 지나치게 늦게 발동하는 데 있다고 주장한다. 그 결과 다단 레이아웃이 텍스트 크기와 맞지 않게 너무 늦게 단일 컬럼으로 무너질 수 있다고 설명한다. 따라서 당시 기준으로는 공통 브라우저에서 더 일관적인 `px`를 미디어 쿼리에 쓰는 편이 낫다고 결론낸다. 다만 사용자의 기본 글꼴 크기를 존중하는 접근성 관점에서는 루트 폰트 크기 강제 고정보다 약간의 레이아웃 문제를 감수하는 편이 낫다고 본다.

## 본문 포인트별 발췌
> Interesting! Safari is triggering the 400px breakpoint at 600px when zoomed to 150% _(the correct behavior)_ but it's triggering the `25em` breakpoint at _900px_, which makes no sense at all.
> **When zoomed in, Safari triggers `em` breakpoints much later than it should.**
> Again, this is because Safari is triggering the breakpoint **far too late** when using em units.
> Pixels are the only unit that behave consistently across all commonly used browsers.
> I maintain sites with millions of unique visitors each month and haven't once had someone report a layout issue because of this, so even though this certainly sucks, it seems like in practice it's not causing sites to become truly unusable.
