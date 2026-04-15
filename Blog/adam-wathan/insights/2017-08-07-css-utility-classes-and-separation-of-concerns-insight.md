---
source: blog
creator: adam-wathan
url: https://adamwathan.me/css-utility-classes-and-separation-of-concerns
title: "CSS Utility Classes and \"Separation of Concerns\""
published_at: 2017-08-07
collected_at: 2026-04-15
categories: ["web-app", "dev-tools"]
insight_extracted_at: 2026-04-15
---

## 핵심 주장 (≤5)
1. 전통적인 "관심사의 분리" 방식은 HTML과 CSS의 결합을 없애지 못하며, 실제로는 CSS가 HTML 구조에 강하게 의존하게 만든다.
2. HTML과 CSS의 관계는 "관심사의 분리"보다 "의존성 방향"으로 이해해야 하며, restyleable HTML과 reusable CSS 사이의 선택 문제다.
3. 콘텐츠 기반 클래스보다 재사용 가능한 콘텐츠-비종속 컴포넌트와 유틸리티 클래스를 조합하는 편이 중복을 줄이고 새 UI를 더 적은 CSS로 만들게 해준다.
4. 작은 유틸리티 집합을 팀 전체가 공유하면 스타일 선택이 제한되어 디자인 일관성을 강제할 수 있다.
5. 컴포넌트는 처음부터 추상화하지 말고, 유틸리티로 먼저 만들고 반복 패턴이 실제로 생겼을 때만 추출하는 것이 낫다.

## 공개된 숫자·지표
- GitLab CSS 통계: 텍스트 색상 402개, 배경색 239개, 폰트 크기 59개 (기간: 없음, 출처: "GitLab: 402 text colors, 239 background colors, 59 font sizes")
- Buffer CSS 통계: 텍스트 색상 124개, 배경색 86개, 폰트 크기 54개 (기간: 없음, 출처: "Buffer: 124 text colors, 86 background colors, 54 font sizes")
- HelpScout CSS 통계: 텍스트 색상 198개, 배경색 133개, 폰트 크기 67개 (기간: 없음, 출처: "HelpScout: 198 text colors, 133 background colors, 67 font sizes")
- Gumroad CSS 통계: 텍스트 색상 91개, 배경색 28개, 폰트 크기 48개 (기간: 없음, 출처: "Gumroad: 91 text colors, 28 background colors, 48 font sizes")
- Stripe CSS 통계: 텍스트 색상 189개, 배경색 90개, 폰트 크기 35개 (기간: 없음, 출처: "Stripe: 189 text colors, 90 background colors, 35 font sizes")
- GitHub CSS 통계: 텍스트 색상 163개, 배경색 147개, 폰트 크기 56개 (기간: 없음, 출처: "GitHub: 163 text colors, 147 background colors, 56 font sizes")
- ConvertKit CSS 통계: 텍스트 색상 128개, 배경색 124개, 폰트 크기 70개 (기간: 없음, 출처: "ConvertKit: 128 text colors, 124 background colors, 70 font sizes")

## 언급된 도구·서비스
- CSS Zen Garden: 스타일시트만 바꿔 사이트를 완전히 재디자인할 수 있다는 전통적 분리 원칙의 대표 사례로 언급
- BEM: 구조 의존성을 낮추기 위해 더 많은 클래스를 마크업에 추가하는 방법론으로 소개
- CodePen: 각 CSS 접근 방식의 데모를 공유하는 예제로 사용
- Bootstrap: HTML이 CSS에 의존하는 UI 프레임워크의 예로 언급
- Bulma: HTML이 CSS에 의존하는 UI 프레임워크의 예로 언급
- CSS Stats: 실제 서비스들의 텍스트 색상·배경색·폰트 크기 개수를 보여주는 근거 도구로 사용
- Tachyons: 유틸리티 기반 프레임워크 사례이자 템플릿 컴포넌트 접근을 설명하는 예제로 사용
- Vue.js: 유틸리티 조합을 템플릿 컴포넌트로 추상화하는 예제로 사용
- Less: 기존 클래스를 믹스인으로 활용해 유틸리티에서 컴포넌트를 추출하는 전처리기로 언급
- Sass: Less와 달리 유틸리티를 바로 믹스인처럼 쓰기 어렵다는 비교 대상으로 언급
- Stylus: Sass와 함께 같은 한계 사례로 언급
- PostCSS: Tailwind CSS가 구현된 프레임워크 기반으로 언급
- Tailwind CSS: 저자가 공개한 utility-first PostCSS 프레임워크로 소개
- Basscss: 시작점으로 추천한 유틸리티 프레임워크
- Beard: 시작점으로 추천한 유틸리티 프레임워크
- turretcss: 시작점으로 추천한 유틸리티 프레임워크

## 언급된 다른 creator·앱
- Nicolas Gallagher: reusable CSS 중심 사고로 전환하게 만든 글의 저자로 언급
- Dave Shea: CSS Zen Garden 맥락에서 간접적으로 연결되는 인물은 있으나 본문 실명 언급은 없음
- GitLab: CSS 값 중복 사례를 보여주는 서비스로 언급
- Buffer: CSS 값 중복 사례를 보여주는 서비스로 언급
- HelpScout: CSS 값 중복 사례를 보여주는 서비스로 언급
- Gumroad: CSS 값 중복 사례를 보여주는 서비스로 언급
- Stripe: CSS 값 중복 사례를 보여주는 서비스로 언급
- GitHub: CSS 값 중복 사례를 보여주는 서비스로 언급
- ConvertKit: CSS 값 중복 사례를 보여주는 서비스로 언급

## 복제 가능한 전술 (≤3)
1. 새 UI를 만들 때 콘텐츠 이름 기반 컴포넌트 대신 재사용 가능한 시각 패턴 단위로 먼저 분해한다.
   - 구체적 스텝: 새 마크업을 작성한 뒤 `.author-bio` 같은 콘텐츠 전용 클래스 대신 `.card`, `.btn--primary`, `.align-right`처럼 다른 화면에서도 쓸 수 있는 패턴 단위가 있는지 확인하고, 기존 클래스를 조합해 먼저 구현한다.
   - 예상 리소스: 기존 CSS 클래스 인벤토리 점검 시간, HTML 수정, CSS 유틸리티/컴포넌트 사전
   - 예상 효과: 같은 스타일이 필요한 새 콘텐츠 타입을 추가할 때 스타일시트를 다시 열지 않고 HTML만으로 조합 가능한 구조를 만들 수 있다.
2. 하위 컴포넌트 전용 추상화보다 정렬·간격 같은 단일 목적 유틸리티로 치환한다.
   - 구체적 스텝: `.actions-list--left`, `.header-bar__actions` 같은 맥락 전용 클래스가 보이면 그것이 실제로 담당하는 속성을 분해해 `.align-left`, `.align-right`, `.mar-r-sm` 같은 재사용 유틸리티로 바꾸고, 마크업에서 직접 조합한다.
   - 예상 리소스: 소규모 CSS 리팩터링, 클래스명 정리, 관련 템플릿 수정
   - 예상 효과: 불필요한 추상화를 삭제해 CSS를 더 작게 만들고, 동일한 정렬·간격 규칙을 여러 문맥에서 재사용할 수 있다.
3. 컴포넌트를 선제적으로 만들지 말고 유틸리티로 구현한 뒤 반복 패턴만 나중에 추출한다.
   - 구체적 스텝: 네비게이션, 카드, 버튼 같은 UI를 처음에는 유틸리티 조합으로 만들고, 동일한 클래스 묶음이 여러 번 반복되는 시점에만 `.btn-purple` 같은 컴포넌트 클래스로 승격한다.
   - 예상 리소스: 유틸리티 클래스 세트, 반복 패턴 검토 시간, 필요 시 Less/Sass/PostCSS 환경
   - 예상 효과: 재사용되지 않을 컴포넌트 추상화를 줄여 스타일시트의 팽창과 복잡도 증가를 완화할 수 있다.

## 원문 요약 (≤5문장)
글은 CSS 설계가 "관심사의 분리"라는 도덕적 기준이 아니라 HTML과 CSS 중 무엇이 무엇에 의존하는지의 문제라고 주장한다. 저자는 semantic CSS, BEM, 콘텐츠-비종속 컴포넌트, 그리고 utility-first CSS로 발전한 자신의 사고 과정을 단계별로 설명한다. 핵심은 콘텐츠 전용 클래스보다 재사용 가능한 시각 패턴과 단일 목적 유틸리티를 조합하는 편이 중복을 줄이고 새 UI를 더 빠르게 만들 수 있다는 점이다. 또한 실제 서비스들의 CSS 통계를 근거로, 새 CSS를 계속 쓰는 방식은 값의 다양성을 폭증시켜 일관성을 해친다고 지적한다. 결론적으로 저자는 유틸리티로 먼저 만들고 반복될 때만 컴포넌트를 추출하는 접근을 추천한다.

## 본문 포인트별 발췌
> My markup wasn't concerned with styling decisions, but my CSS was very concerned with my markup structure.
> Instead, **think about _dependency direction._**
> In this model, your HTML is restyleable, but your CSS is not reusable.
> In this model, your CSS is reusable, but your HTML is not restyleable.
> every line of new CSS is still an opportunity for new complexity
