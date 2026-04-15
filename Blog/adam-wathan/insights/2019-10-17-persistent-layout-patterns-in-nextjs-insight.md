---
source: blog
creator: adam-wathan
url: https://adamwathan.me/2019/10/17/persistent-layout-patterns-in-nextjs
title: Persistent Layout Patterns in Next.js
published_at: 2019-10-17
collected_at: 2026-04-15
categories: ["web-app"]
insight_extracted_at: 2026-04-15
---

## 핵심 주장 (≤5)
1. Next.js와 Gatsby 같은 현대 SPA 프레임워크도 기본 동작에서는 링크 클릭 시 전체 UI를 다시 렌더링해, 지속되는 UI 경험이 깨질 수 있다.
2. 페이지 컴포넌트 자체가 항상 최상단 노드가 되면, 첫 번째 레이아웃 컴포넌트가 같아 보여도 React는 하위 트리를 버리고 새로 렌더링한다.
3. `_app.js`에서 단일 공통 레이아웃을 감싸는 방식은 사이트 전체에 하나의 레이아웃만 쓸 때는 유효하지만, 섹션별 레이아웃이 필요해지면 빠르게 한계에 부딪힌다.
4. URL 기준으로 `_app.js`에서 레이아웃 트리를 분기하면 지속 레이아웃을 구현할 수 있지만, 레이아웃 구조가 URL과 강하게 결합되고 조건 분기가 복잡해진다.
5. 페이지별 `getLayout` 함수를 두고 `_app.js`에서 이를 호출하는 방식이 가장 선언적이고 유연하며, 임의 수준의 UI 지속성을 허용한다.

## 공개된 숫자·지표
- 없음

## 언급된 도구·서비스
- Next.js: 지속 레이아웃 패턴을 실험하고 구현하는 대상 프레임워크
- Gatsby: Next.js와 함께 기본 경험이 전체 UI 재렌더링이라고 비교 대상으로 언급됨
- React: 페이지 컴포넌트가 바뀔 때 하위 트리를 버리고 다시 렌더링하는 동작 설명에 사용됨
- Backbone: 초기 SPA 인기 시기의 예시 프레임워크로 언급됨
- Ember: 초기 SPA 인기 시기의 예시 프레임워크로 언급됨
- Angular: 초기 SPA 인기 시기의 예시 프레임워크로 언급됨
- Twitter: 독자가 질문이나 아이디어를 보낼 수 있는 연락 채널로 언급됨

## 언급된 다른 creator·앱
- Twitter: 글 말미에서 작성자가 `@adamwathan` 계정으로 연락 가능하다고 안내함

## 복제 가능한 전술 (≤3)
1. 사이트 전체에 단 하나의 공통 레이아웃만 필요한 경우, 커스텀 `_app.js`에서 공통 `SiteLayout`으로 모든 페이지를 감싼다.
   - 구체적 스텝: `pages/_app.js`를 만들고 `Component`를 `SiteLayout` 바깥이 아니라 안쪽에 렌더링한다; 각 페이지에서는 최상위에 다시 공통 레이아웃을 두지 않는다; 페이지 전환 후 검색 입력값 같은 UI 상태가 유지되는지 확인한다.
   - 예상 리소스: Next.js 프로젝트, 공통 레이아웃 컴포넌트 1개, 짧은 구현 및 수동 확인 시간
   - 예상 효과: 페이지 전환 사이에서 공통 레이아웃 인스턴스가 재사용되어 레이아웃 내부 상태가 유지된다.
2. 섹션별 레이아웃이 필요한 소규모 사이트라면, `_app.js`에서 현재 URL을 기준으로 전체 레이아웃 트리를 직접 분기한다.
   - 구체적 스텝: `_app.js`에서 `router.pathname`으로 현재 섹션을 판별한다; 섹션별로 `SiteLayout > SectionLayout > Component` 같은 전체 트리를 직접 반환한다; 중첩 레이아웃 내부에서 상위 레이아웃을 다시 감싸지 않도록 구성해 동일 DOM 위치의 레이아웃 인스턴스가 유지되게 한다.
   - 예상 리소스: Next.js 라우터 접근, 섹션 레이아웃 컴포넌트, URL 규칙 정리
   - 예상 효과: 계정 설정 탭 같은 섹션 내부 UI도 페이지 전환 시 지속되어 스크롤 위치 손실을 줄일 수 있다.
3. 더 유연한 구조가 필요하면, 각 페이지에 정적 `getLayout` 함수를 두고 `_app.js`가 이를 호출해 페이지별 전체 레이아웃 트리를 구성한다.
   - 구체적 스텝: 각 페이지 파일에 `Page.getLayout = page => (...)` 형태의 함수를 정의한다; `_app.js`에서 `const getLayout = Component.getLayout || (page => page)`를 사용해 현재 페이지를 감싼다; 중복을 줄이려면 레이아웃 컴포넌트 자체에도 `getLayout` 함수를 export하고 페이지는 그것을 재사용한다.
   - 예상 리소스: 페이지별 정적 프로퍼티 패턴, `_app.js` 수정, 레이아웃 컴포넌트 정리
   - 예상 효과: 페이지별로 전체 레이아웃 트리를 선언적으로 제어하면서도 더 높은 수준의 UI 지속성을 확보할 수 있다.

## 원문 요약 (≤5문장)
글은 Next.js에서 기본적으로 페이지 전환 시 전체 UI가 재렌더링되어 SPA 특유의 지속 UI 경험이 깨질 수 있다는 문제를 짚는다. 저자는 이를 해결하기 위해 `_app.js` 단일 공통 레이아웃, URL 기반 분기, 페이지별 정적 `layout` 프로퍼티, 페이지별 `getLayout` 함수라는 네 가지 패턴을 비교한다. 단일 공통 레이아웃은 단순하지만 유연성이 낮고, URL 분기 방식은 작동하지만 URL 구조와 레이아웃이 강하게 결합된다. 정적 `layout` 프로퍼티는 `_app.js` 복잡도를 줄이지만 상위 레이아웃 인스턴스가 바뀌면 상태 지속성이 깨질 수 있다. 최종적으로 페이지별 `getLayout` 함수와 레이아웃 컴포넌트의 `getLayout` 재사용 패턴이 가장 유연한 해법으로 제시된다.

## 본문 포인트별 발췌
> the default experience is re-rendering the entire UI every time you click a link
> React throws out all of its children and re-renders them from scratch
> we can only provide a single layout component
> It also couples your layouts to your URLs
> This puts each page component in charge of its entire layout, and allows an arbitrary degree of UI persistence:
