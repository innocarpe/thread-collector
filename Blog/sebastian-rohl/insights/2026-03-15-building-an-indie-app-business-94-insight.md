---
source: blog
creator: sebastian-rohl
url: https://sebastianroehl.substack.com/p/building-an-indie-app-business-94
title: Building An Indie App Business #94
published_at: 2026-03-15
collected_at: 2026-04-15
categories: ["productivity", "startup-philosophy"]
insight_extracted_at: 2026-04-15
---

## 핵심 주장 (≤5)
1. 솔로 인디 개발자는 아프면 업무를 대신할 사람이 없어 사실상 사업 전체가 멈춘다.
2. HabitKit 1.14.6 업데이트는 AI가 도운 대규모 성능 개선을 실제 출시까지 연결한 중요한 릴리스다.
3. HabitKit과 FocusKit 모두에서 홈 스크린 위젯은 가장 많이 요청된 기능 중 하나라 우선순위가 높다.
4. 위젯 개발은 iOS부터 시작하고, Android는 Jetpack Glance의 제약 때문에 뒤로 미루는 것이 합리적이라고 본다.
5. FocusKit 가격 인상 여부는 오래 고민하기보다 실제로 시도해 보고 판단하는 접근이 더 낫다고 본다.

## 공개된 숫자·지표
- 성능 문제 해결 기간: 2년 (기간: 1.14.6 업데이트 전 누적 기간, 출처: "Two years of struggling with performance issues, massive improvements in one update!")
- FocusKit 검토 중 가격: $2 / month (기간: 향후 가격 조정 검토 시점, 출처: "The idea would be to add a light theme, stabilize the app a bit more, and then bump it to $2 / month.")

## 언급된 도구·서비스
- AI: HabitKit의 대규모 성능 개선을 달성하는 데 도움을 준 수단으로 언급됨
- App Store: HabitKit 1.14.6 배포 채널로 언급됨
- Google Play: HabitKit 1.14.6 배포 채널로 언급됨
- Jetpack Glance framework: Android 홈 스크린 위젯 개발에 사용되는 프레임워크로, 제약이 많고 다루기 어렵다고 평가됨

## 언급된 다른 creator·앱
- HabitKit: 성능 개선 업데이트 1.14.6 출시와 다음 기능인 홈 스크린 위젯 계획이 언급됨
- FocusKit: 홈 스크린 위젯 개발 시작, 라이트 테마 및 앱스토어 스크린샷 A/B 테스트, 가격 인상 검토가 언급됨

## 복제 가능한 전술 (≤3)
1. 멀티플랫폼 기능은 구현 난도가 낮은 플랫폼부터 먼저 출시한다.
   - 구체적 스텝: 사용자 요청이 많은 기능을 선정하고, 플랫폼별 API 제약을 비교한 뒤 구현이 더 깔끔한 플랫폼 버전을 먼저 개발·출시하고, 제약이 큰 플랫폼은 후속 작업으로 분리한다.
   - 예상 리소스: 플랫폼 API 문서, 기존 앱 코드베이스, 위젯 개발 시간
   - 예상 효과: 더 빠르게 요청 기능을 출시하고, 복잡한 플랫폼 제약으로 인한 초기 개발 지연을 줄일 수 있다.
2. 자주 요청되는 기능은 미리 정리한 실행 계획을 바탕으로 바로 개발에 착수한다.
   - 구체적 스텝: 사용자 요청이 반복적으로 들어온 기능을 고르고, 업데이트 범위와 구현 순서를 먼저 문서화한 뒤, 개발 주간에는 계획에 따라 바로 구현을 시작한다.
   - 예상 리소스: 기능 요청 정리, 간단한 구현 계획 문서, 개발 시간
   - 예상 효과: 우선순위 판단 시간을 줄이고, 컨디션이나 외부 변수로 생산성이 낮은 주에도 실행을 이어가기 쉽다.
3. 가격 변경은 장기 고민만 하지 말고 제품 보강 후 실제로 테스트한다.
   - 구체적 스텝: 가격 인상 후보 기능(예: 라이트 테마, 안정화 작업)을 먼저 반영하고, 이후 가격을 조정한 뒤 사용자 유입과 반응을 관찰한다.
   - 예상 리소스: 제품 개선 작업, 앱 가격 설정 권한, 반응 관찰 시간
   - 예상 효과: 추측 대신 실제 시장 반응으로 가격 전략을 판단할 수 있다.

## 원문 요약 (≤5문장)
이번 주 글은 건강 문제와 개인 사정으로 생산성이 떨어진 가운데서도 핵심 업데이트를 배포하고 다음 기능 우선순위를 정리한 기록이다. HabitKit 1.14.6은 AI의 도움으로 달성한 대규모 성능 개선을 담아 출시되었다. 다음 주요 작업으로 HabitKit과 FocusKit 모두에서 수요가 높은 홈 스크린 위젯 개발이 진행되며, 우선 iOS부터 시작할 계획이다. 작성자는 솔로 개발자가 아플 때 사업이 멈추는 구조적 취약성을 직접 언급한다. 또한 FocusKit의 가격 인상은 계속 고민만 하기보다 실제로 시도해 보는 쪽이 나을 수 있다고 본다.

## 본문 포인트별 발췌
> Being a solo indie dev without any employees means there’s simply no one to pick up the work when you’re not at 100%.
> Two years of struggling with performance issues, massive improvements in one update!
> This is actually one of the most requested features HabitKit has ever received.
> I’m going to start with iOS first because the widget APIs are much cleaner and easier to work with there.
> Maybe I’ll just try it and see what happens. That’s usually the best strategy anyway when you’re overthinking things.
