---
source: blog
creator: adam-wathan
url: https://adamwathan.me/composing-the-uncomposable-with-css-variables
title: Composing the Uncomposable with CSS Variables
published_at: 2020-09-18
collected_at: 2026-04-15
categories: ["web-app"]
insight_extracted_at: 2026-04-15
---

## 핵심 주장 (≤5)
1. CSS 속성이 개별 하위 속성으로 분해되면 유틸리티 클래스 시스템에서 임의 조합이 가능하지만, 그렇지 않으면 클래스 조합 수가 폭발해 순수 CSS의 표현력을 그대로 옮기기 어렵다.
2. CSS 변수는 빌드 타임이 아니라 런타임에 계산되므로, 상위 컨텍스트에서 값을 재정의해 같은 스타일 규칙을 다른 결과로 바꿀 수 있다.
3. CSS 변수는 완성된 값뿐 아니라 값의 일부 조각도 담을 수 있어서, `rgba()`의 알파값처럼 하나의 CSS 속성 안에서도 독립적으로 조합 가능한 "슬롯"을 만들 수 있다.
4. `transform`처럼 원래는 비조합적인 속성도 기본 클래스에서 no-op 값을 가진 변수 슬롯을 선언하고, 후속 유틸리티가 각 변수만 덮어쓰게 하면 조합 가능하게 만들 수 있다.
5. `font-variant-numeric`처럼 선택적 조각을 이어 붙이는 경우 빈 값 대신 공백을 CSS 변수 기본값으로 사용해 규칙 무효화를 피할 수 있지만, 프로덕션에서는 CSS minifier 때문에 별도 우회가 필요할 수 있다.

## 공개된 숫자·지표
- 없음

## 언급된 도구·서비스
- Tailwind CSS: 비조합적인 CSS 속성을 유틸리티 클래스로 조합 가능하게 만드는 실제 사례로 사용됨
- CSS custom properties (CSS variables): 런타임 계산과 부분 값 조합을 통해 비조합적 속성을 조합 가능하게 만드는 핵심 메커니즘으로 사용됨
- Sass: CSS 변수와 달리 빌드 타임에 계산되는 도구의 예시로 언급됨
- Less: CSS 변수와 달리 빌드 타임에 계산되는 도구의 예시로 언급됨
- Stylus: CSS 변수와 달리 빌드 타임에 계산되는 도구의 예시로 언급됨
- PostCSS: 공백 기반 CSS 변수 기본값을 minifier가 제거하는 문제가 PostCSS 8에서 개선될 수 있다고 언급됨
- GitHub: PostCSS 관련 수정 이슈 링크 대상으로 언급됨

## 언급된 다른 creator·앱
- 없음

## 복제 가능한 전술 (≤3)
1. 비조합적인 단일 CSS 속성을 "기본 클래스 + 변수 슬롯 유틸리티" 구조로 다시 설계한다.
   - 구체적 스텝: 조합하고 싶은 속성(예: `transform`)을 고른다; 해당 속성의 기능 단위(예: `translateX`, `translateY`, `rotate`, `scale`)별 CSS 변수를 만든다; 기본 클래스에서 각 변수에 no-op 기본값을 넣고 최종 속성값을 `var(...)` 조합으로 선언한다; 개별 유틸리티 클래스는 속성 자체를 건드리지 않고 관련 변수만 덮어쓴다; HTML에서는 기본 클래스와 필요한 유틸리티를 함께 적용한다.
   - 예상 리소스: CSS 편집 시간, 유틸리티 클래스 체계, 브라우저에서 조합 동작 확인
   - 예상 효과: 원래는 하나의 선언으로만 다뤄야 하던 속성을 여러 클래스 조합으로 제어할 수 있다.
2. 하나의 속성 안에 부분 값이 섞인 경우, CSS 변수로 "부분 값"만 분리해 독립 제어한다.
   - 구체적 스텝: 색상·투명도처럼 한 속성에서 독립 제어하고 싶은 축을 찾는다; 완성된 값을 변수로 두지 말고 RGB 채널이나 알파값처럼 일부 조각만 변수로 저장한다; 최종 속성은 `rgba(var(--rgb-brand), var(--text-opacity))` 같은 형태로 조립한다; 기본 유틸리티는 기본값을 넣고, 후속 유틸리티는 해당 변수만 변경한다.
   - 예상 리소스: CSS 변수 지원 환경, 색상 또는 함수형 CSS 값 설계, 클래스 우선순위 확인
   - 예상 효과: 한 CSS 속성 안에서 색상과 불투명도처럼 원래 함께 묶인 값을 클래스 단위로 독립 제어할 수 있다.
3. 선택적 토큰 리스트 속성은 공백 기본값을 둔 변수 슬롯으로 연결하고, 프로덕션 빌드까지 검증한다.
   - 구체적 스텝: `font-variant-numeric`처럼 여러 선택적 토큰이 이어지는 속성을 고른다; 각 토큰 자리에 대응하는 CSS 변수를 만든다; 기본 클래스에서 각 변수에 빈 문자열이 아니라 공백 값을 넣고 최종 속성에서 순서대로 `var(...)`를 이어 붙인다; 개별 유틸리티는 해당 변수에 실제 토큰 값만 넣는다; minifier가 공백 변수를 제거하는지 프로덕션 빌드 결과를 확인하고, 필요하면 글에서 제시한 `var(--not-a-real-variable,/*!*/ /*!*/)` 같은 우회 기본값을 사용한다.
   - 예상 리소스: CSS minifier가 포함된 빌드 환경, 프로덕션 빌드 점검 시간, PostCSS 등 후처리 도구
   - 예상 효과: 원래는 조합하기 어려운 선택적 키워드 리스트 속성도 유틸리티 클래스로 조합 가능해진다.

## 원문 요약 (≤5문장)
글은 유틸리티 클래스 시스템이 CSS의 조합성을 유지하려면 속성이 하위 단위로 분해 가능해야 한다는 문제의식에서 출발한다. 저자는 CSS 변수가 런타임에 계산되고 부분 값도 담을 수 있다는 점을 이용해, `transform` 같은 비조합적 속성에 변수 슬롯을 만들어 조합 가능하게 하는 방법을 설명한다. 이어 Tailwind CSS의 텍스트 opacity 구현처럼 하나의 속성 안에서 색상과 투명도를 분리 제어하는 패턴을 소개한다. 더 나아가 `font-variant-numeric`처럼 선택적 토큰을 이어 붙이는 속성에는 공백을 변수 기본값으로 사용해 규칙 무효화를 피하는 기법을 제안한다. 다만 이 방식은 CSS minifier가 공백 값을 제거할 수 있어 프로덕션 빌드에서는 우회 문법이 필요할 수 있다고 경고한다.

## 본문 포인트별 발췌
> Without this composability, it would be essentially impossible to do all of the things you can do in pure CSS because of the combinatoric explosion of classes that would have to exist to support every combination of values.
> The cool things about CSS variables is that unlike in Sass/Less/Stylus/potato, they are computed at run-time rather than at build-time, so they can change.
> This is cool on its own, but what's even cooler is that CSS variables don't have to represent a complete value — they can be used for partial values, too.
> This takes a traditionally non-composable property, and makes it perfectly composable using multiple classes in your HTML.
> The problem is that doing things this way, our variables like `--variant-ordinal` have no default value, which means when `var(--variant-ordinal)` tries to resolve, it will be what the spec calls the invalid value, which actually invalidates the whole rule, so the CSS isn't applied at all.
