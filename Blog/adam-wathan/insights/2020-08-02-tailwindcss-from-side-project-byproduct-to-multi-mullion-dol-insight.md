---
source: blog
creator: adam-wathan
url: https://adamwathan.me/tailwindcss-from-side-project-byproduct-to-multi-mullion-dollar-business
title: Tailwind CSS: From Side-Project Byproduct to Multi-Million Dollar Business
published_at: 2020-08-02
collected_at: 2026-04-15
categories: ["case-study", "monetization", "startup-philosophy"]
insight_extracted_at: 2026-04-15
---

## 핵심 주장 (≤5)
1. 여러 프로젝트에 반복 이식해 본 결과, 재사용 가능한 것은 컴포넌트보다 유틸리티였고 이것이 "utility-first"를 철학으로 인식하게 만든 계기였다.
2. 작업 과정을 공개한 라이브스트리밍이 사용자 관심과 피드백을 만들었고, 그 노출이 Tailwind Labs 비즈니스의 직접적 출발점이 되었다.
3. 서로 다른 실제 프로젝트에 동시에 맞춰보는 과정이 프레임워크를 더 "project-agnostic"하게 만드는 강한 제약으로 작동했다.
4. Less로 한계를 밀어붙이던 구현을 PostCSS와 JavaScript로 옮긴 것이 유지보수 자신감과 기능 확장성을 크게 높였다.
5. 오픈소스로 커뮤니티를 만든 뒤 상업 제품인 Tailwind UI로 확장해 큰 매출을 만든 것이 핵심 사업화 경로였다.

## 공개된 숫자·지표
- Tailwind CSS 누적 설치 수: 1,000만 회 돌파 (기간: 2020-08 직전 누적, 출처: "So about a month or so ago, Tailwind cracked 10 million total installs, which given its humble beginnings, completely blows my mind.")
- Tailwind UI 매출: 200만 달러 돌파 임박 (기간: 출시 후 약 5개월 시점, 출처: "We're also about to cross $2 million in revenue from Tailwind UI, our first commercial Tailwind CSS product which was released about 5 months ago")
- 첫 Tailwind CSS 출시 후 Tailwind UI 매출 200만 달러 근접까지 걸린 시간: 2년이 채 안 됨 (기간: 첫 Tailwind CSS 출시부터 2020-08 시점, 출처: "a bit under two years after the very first Tailwind CSS release")
- Tailwind Labs 매출: 400만 달러 초과 (기간: 2년 미만, 출처: "which has now done over $4m in revenue in under 2 years")
- Digest 스타일시트를 재사용한 프로젝트 수: 최소 4~5개 (기간: Digest 중단 이후, 출처: "I must have brought them across to at least 4 or 5 other projects after we abandoned Digest.")
- Tailwind 공개 준비 기간: 2~3개월 (기간: 2017년 6~7월 이후, 출처: "for the next 2-3 months, Jonathan and I worked feverishly on making something that was good enough to open-source.")
- Tailwind UI 초기 액세스 출시 직전 연속 작업 시간: 36시간 (기간: 2020년 2월 출시 직전, 출처: "after working literally 36 hours straight before our self-imposed deadline")

## 언급된 도구·서비스
- Bootstrap: 초기 사이드 프로젝트 Digest에서 원래 쓰려 했던 CSS 프레임워크
- Sass: Bootstrap 4 alpha가 Less 대신 채택해 저자가 사용을 포기한 전처리기
- Less: Digest와 초기 프레임워크를 작성한 CSS 전처리기
- Tailwind CSS: 반복 재사용된 유틸리티 스타일에서 출발해 오픈소스 프레임워크가 된 결과물
- KiteTail: 개발자 대상 웹훅 기반 체크아웃 플랫폼으로, Tailwind 전신 스타일 시스템을 다듬던 프로젝트
- YouTube: "Building KiteTail" 시리즈를 통해 작업 과정을 공개한 채널
- Twitter: 초기 공개, 반응 수집, 제품 티저, 출시 공지에 사용한 채널
- onelook.com: Tailwind라는 이름을 찾을 때 사용한 단어 검색 도구
- PostCSS: Tailwind를 JavaScript로 재구현하는 기반으로 사용한 도구
- autoprefixer: PostCSS의 활용 예를 설명하며 언급한 도구
- Full Stack Radio: PostCSS로 CSS 프레임워크를 만드는 과정을 이야기한 팟캐스트
- PurgeCSS: Tailwind의 unused CSS 제거 문제를 해결하는 중요한 계기를 준 도구
- Refactoring UI: 저자들이 Tailwind에 풀타임으로 집중할 수 있는 자금 기반을 제공한 상업 제품
- Tailwind UI: Tailwind CSS 기반의 첫 상업 제품

## 언급된 다른 creator·앱
- Steve Schoger: Digest를 함께 시작했고 이후 Tailwind UI와 Tailwind Labs를 함께 만든 비즈니스 파트너
- Stefan Bauer: 반응형 유틸리티 접두사 아이디어를 제안한 협업자
- Jonathan Reinink: 자신의 SaaS 리디자인에 프레임워크를 적용하며 Tailwind를 더 범용적으로 만드는 데 기여한 협업자
- David Hemphill: Less 대신 PostCSS를 시도해 보라고 제안한 인물
- Andrew Del Prete: PurgeCSS 관련 중요한 블로그 글을 써 Tailwind 생태계에 영향을 준 인물
- Andrey Sitnik: PostCSS 제작자로 언급됨
- Brad Cornes: Tailwind 팀 확장 과정에서 합류한 팀원
- Simon Vrachliotis: Tailwind 팀 확장 과정에서 합류한 팀원

## 복제 가능한 전술 (≤3)
1. 내부적으로 반복 재사용되는 부수 산출물을 독립 제품 후보로 검증한다.
   - 구체적 스텝: 한 프로젝트에서 만든 스타일/스크립트/워크플로를 다음 프로젝트들에 그대로 이식해 본다. 이식할 때마다 그대로 재사용되는 부분과 매번 버려지는 부분을 분리한다. 여러 프로젝트에서 살아남는 공통층만 별도 패키지나 프레임워크 후보로 정리한다.
   - 예상 리소스: 여러 실프로젝트, 재사용 관찰 시간, 공통 코드 정리 작업
   - 예상 효과: 원문처럼 재사용 가능한 핵심이 컴포넌트보다 유틸리티인지 식별할 수 있고, 제품화 가능한 "portable" 자산을 발견할 수 있다.
2. 작업 과정을 공개해 수요 신호와 제품 아이디어를 끌어낸다.
   - 구체적 스텝: 실제 제품을 만드는 과정을 라이브스트림이나 공개 콘텐츠로 보여준다. 반복적으로 받는 질문과 관심 포인트를 기록한다. 특정 내부 도구나 구현 방식에 질문이 몰리면 그것을 별도 공개 또는 제품화 후보로 전환한다.
   - 예상 리소스: 스트리밍 또는 공개 채널, 작업 기록 시간, 피드백 정리
   - 예상 효과: 원문처럼 원래 제품으로 만들 생각이 없던 자산도 외부 반응을 통해 오픈소스/사업 아이템으로 발전할 수 있다.
3. 상이한 실제 사용 사례를 동시에 만족시키도록 설계해 범용성을 높인다.
   - 구체적 스텝: 서로 디자인이나 요구가 다른 두 개 이상의 실제 프로젝트에 같은 기반 시스템을 적용한다. 한쪽에서만 통하는 규칙이나 컴포넌트는 제거하고, 둘 다에서 필요한 설정성과 추상화만 남긴다. 이 과정에서 구현 한계가 보이면 더 적합한 기술 스택으로 이전한다.
   - 예상 리소스: 서로 다른 실사용 프로젝트, 공동 사용자 또는 협업자, 리팩터링 시간
   - 예상 효과: 원문처럼 "project-agnostic"한 구조를 만드는 강한 검증 루프가 생기고, 오픈소스화와 상업화에 유리한 범용성이 올라간다.

## 원문 요약 (≤5문장)
Tailwind CSS는 별도 제품을 목표로 시작한 것이 아니라, 실패한 사이드 프로젝트 Digest의 스타일시트를 여러 프로젝트에 재사용하는 과정에서 태어났다. Adam Wathan은 라이브스트리밍으로 KiteTail을 만들며 CSS에 대한 반복 질문을 받았고, 이것이 Tailwind를 오픈소스로 공개하는 직접적 계기가 되었다. Jonathan Reinink 등의 실제 사용 사례와 David Hemphill의 PostCSS 제안은 Tailwind를 더 범용적이고 유지보수 가능한 프레임워크로 발전시키는 데 중요했다. 이후 커뮤니티와 제품 적합성을 키운 뒤 Tailwind UI를 출시했고, 출시 약 5개월 만에 200만 달러 매출 돌파를 앞두게 되었다. 글의 핵심은 실패한 프로젝트의 부산물, 공개 작업, 오픈소스, 상업 제품이 연결되며 큰 사업으로 전환될 수 있다는 점이다.

## 본문 포인트별 발췌
> So about a month or so ago, Tailwind cracked 10 million total installs, which given its humble beginnings, completely blows my mind.
> We're also about to cross $2 million in revenue from Tailwind UI, our first commercial Tailwind CSS product which was released about 5 months ago — a bit under two years after the very first Tailwind CSS release.
> The utilities were the only things that were truly “portable”, while the component styles were always too opinionated to reuse on another design.
> This is the benefit of working in public — Steve and I would have never built this Tailwind Labs business (which has now done over $4m in revenue in under 2 years) if I hadn’t been live-streaming my work on yet-another-abandoned-side-project.
> This turned out to be key for making the framework actually good, because our projects had completely different designs, and what-would-become-Tailwind needed to support both of those projects.
