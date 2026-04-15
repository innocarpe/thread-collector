---
source: blog
creator: adam-wathan
url: https://adamwathan.me/renderless-components-in-vuejs
title: Renderless Components in Vue.js
published_at: 2018-03-22
collected_at: 2026-04-15
categories: ["web-app"]
insight_extracted_at: 2026-04-15
---

## 핵심 주장 (≤5)
1. 렌더리스 컴포넌트는 자체 HTML을 렌더링하지 않고 상태와 동작만 관리하며, 단일 scoped slot으로 부모가 실제 렌더링을 완전히 제어하게 만든다.
2. 표현과 동작을 분리하면 동일한 복잡한 UI 동작을 서로 다른 레이아웃에 재사용할 수 있어 커스터마이징이 쉬워진다.
3. scoped slot prop은 데이터, 액션, 바인딩의 세 범주로 나눠 설계하면 컴포넌트 API를 더 체계적으로 만들 수 있다.
4. `v-model` 같은 동작도 속성 바인딩과 이벤트 바인딩으로 분해해 slot prop으로 전달하면 렌더리스 패턴 안에서 캡슐화할 수 있다.
5. 이 패턴은 라이브러리처럼 외형 커스터마이징이 중요하거나, 비슷한 동작에 다른 레이아웃이 여럿 있을 때 특히 유용하지만 항상 같은 모양의 컴포넌트에는 과할 수 있다.

## 공개된 숫자·지표
- 없음

## 언급된 도구·서비스
- Vue.js: slots, scoped slots, render function, custom form control, `v-model` 등을 설명하고 렌더리스 컴포넌트 구현 예시에 사용됨
- CodePen: 전통적인 태그 입력, 대체 레이아웃, 렌더리스 태그 입력, fetch-data 컴포넌트 데모를 공유하는 용도로 사용됨
- Advanced Vue Component Design: 관련 컴포넌트 설계 패턴을 더 깊게 다루는 비디오 시리즈로 소개됨

## 언급된 다른 creator·앱
- 없음

## 복제 가능한 전술 (≤3)
1. 복잡한 UI 컴포넌트의 상태와 동작을 렌더리스 컴포넌트로 분리하고, 부모가 마크업을 직접 정의하게 설계한다.
   - 구체적 스텝: 기존 UI 컴포넌트의 동작 로직을 추출한다; 렌더리스 컴포넌트에서 `render()`로 단일 scoped slot을 반환한다; 상태는 데이터 prop으로, 조작 함수는 액션 prop으로, 입력/버튼 제어는 attrs/events 바인딩 prop으로 노출한다; 부모 컴포넌트에서 slot-scope로 필요한 prop만 받아 원하는 HTML 레이아웃에 연결한다.
   - 예상 리소스: Vue.js 컴포넌트 코드, render function 이해, 기존 컴포넌트 리팩터링 시간
   - 예상 효과: 동일한 동작을 유지하면서도 레이아웃과 디자인을 자유롭게 바꿀 수 있어 재사용성과 커스터마이징성이 높아진다.
2. slot prop을 데이터·액션·바인딩으로 나눠 제공해 부모가 구현 디테일을 몰라도 필요한 상호작용을 붙일 수 있게 만든다.
   - 구체적 스텝: 표시용 상태는 객체/배열 등 데이터 prop으로 전달한다; 상태 변경 함수는 액션 prop으로 전달한다; 특정 엘리먼트에 붙어야 하는 속성과 이벤트는 `v-bind`/`v-on`용 객체로 묶어 전달한다; 소비자 컴포넌트는 내부 로직을 다시 구현하지 않고 이를 그대로 바인딩한다.
   - 예상 리소스: Vue slot-scope 문법, `v-bind`, `v-on`
   - 예상 효과: 부모 템플릿은 표현에 집중하고, 자식 컴포넌트는 동작 세부사항을 캡슐화해 API 일관성이 좋아진다.
3. 렌더리스 기반 로직 위에 opinionated wrapper component를 얹어, 자주 쓰는 레이아웃은 한 줄 사용성으로 다시 감싼다.
   - 구체적 스텝: 렌더리스 컴포넌트를 공통 엔진으로 둔다; 특정 레이아웃용 wrapper 컴포넌트에서 slot markup을 미리 작성한다; `value`와 `input` 이벤트를 wrapper에서 그대로 중계한다; 반복 사용되는 레이아웃은 wrapper로 쓰고, 예외 레이아웃만 직접 scoped slot을 사용한다.
   - 예상 리소스: 기존 렌더리스 컴포넌트, 얇은 wrapper 컴포넌트 1개 이상
   - 예상 효과: 커스터마이징 유연성은 유지하면서도 반복되는 장황한 HTML 작성 부담을 줄일 수 있다.

## 원문 요약 (≤5문장)
이 글은 커스터마이징이 어려운 전통적 UI 컴포넌트 패키지의 한계를 해결하는 방법으로 Vue.js의 렌더리스 컴포넌트 패턴을 소개한다. 저자는 scoped slot을 데이터, 액션, 바인딩으로 나눠 설계하면 상태와 동작을 컴포넌트 내부에 두면서도 부모가 원하는 HTML을 자유롭게 렌더링할 수 있다고 설명한다. 태그 입력 컴포넌트를 예제로 들어 태그 목록 표시, 삭제, 입력 처리, 엔터 추가를 단계적으로 렌더리스 구조로 옮기는 과정을 보여준다. 이후 같은 로직으로 서로 다른 레이아웃을 구현하고, 자주 쓰는 형태는 opinionated wrapper component로 다시 감싸 사용성을 보완할 수 있다고 제안한다. 마지막으로 이 패턴은 라이브러리 개발이나 유사 동작의 다중 레이아웃이 있을 때 적합하지만, 항상 같은 모양의 컴포넌트에는 과한 선택일 수 있다고 정리한다.

## 본문 포인트별 발췌
> A _renderless component_ is a component that **doesn't render any of its own HTML**.
> Since renderless components only deal with state and behavior, they don't impose any decisions about design or layout.
> That means that if you can figure out a way to move all of the interesting behavior out of a UI component like our tags input control and into a renderless component, **you can reuse the renderless component to implement any tags input control layout**.
> When designing renderless components like this, **it's better to err on the side of "too many slot props" than too few**.
> Splitting a component into a presentational component and a renderless component is an extremely useful pattern to master and can make code reuse a lot easier, but it's not always worth it.
