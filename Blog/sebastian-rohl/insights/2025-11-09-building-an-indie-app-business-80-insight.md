---
source: blog
creator: sebastian-rohl
url: https://sebastianroehl.substack.com/p/building-an-indie-app-business-80
title: Building An Indie App Business #80
published_at: 2025-11-09
collected_at: 2026-04-15
categories: ["product-strategy", "web-app", "startup-philosophy"]
insight_extracted_at: 2026-04-15
---

## 핵심 주장 (≤5)
1. 포모도로 앱의 인사이트 화면은 전체 세션 기록, 집중/휴식 시간, 기간별 차트, 카테고리 분포, 스트릭과 주간 목표를 통해 사용자가 자신의 작업 습관을 더 잘 이해하게 돕는다.
2. iOS 26 이상을 대상으로 AlarmKit과 라이브 액티비티를 통합하면 앱 경험을 네이티브에 가깝고 더 완성도 높게 만들 수 있다.
3. 데이터 구조를 미래 지향적으로 설계하고 자동 마이그레이션과 기기 간 동기화를 갖추는 것은 멀티디바이스 사용성에 중요하다.
4. 실제 대량 데이터를 미리 주입해 성능을 테스트하고 병목을 최적화해야 통계 중심 화면에서도 반응성이 유지된다.
5. 온보딩은 한 화면으로 단순화하고, 작은 버그 수정과 UX 개선을 계속 누적하는 편이 제품 완성도를 높이는 데 효과적이다.

## 공개된 숫자·지표
- 계획된 출시일: November 30th (기간: 출시 목표 시점, 출처: "I’m really trying hard to get everything ready for my planned launch on November 30th.")
- 지원 OS 버전: iOS 26 and above (기간: 버전 1.0.0 출시 기준, 출처: "Since my app will only be available for iOS 26 and above, I had the chance to use this new feature from Apple, which was really cool.")
- 성능 테스트용 시드 데이터: around 12,000 focus sessions (기간: past two years, 출처: "When I was testing the app, I seeded around 12,000 focus sessions for the past two years to see how it would perform with a lot of data.")
- 인사이트 차트 기간 옵션: week, month, year, all-time (기간: 앱 기능 범위, 출처: "You can switch between week, month, year, or all-time view to see how your productivity changed over time.")
- 온보딩 화면 수: one screen (기간: 온보딩 플로우, 출처: "So I only have one screen that explains the purpose of the app in a simple way.")

## 언급된 도구·서비스
- Pomodoro timer app: 저자가 11월 30일 출시를 목표로 개발 중인 신규 앱으로, 인사이트 화면·온보딩·구매 기능 등 대부분의 작업 맥락이 이 앱을 중심으로 설명됨
- IndieHackers.com: 저자가 인터뷰를 진행한 외부 플랫폼으로, 자신의 모바일 앱 비즈니스 여정을 공유한 장소로 언급됨
- AlarmKit APIs: 세션 종료 시 iOS 기본 알람과 유사한 큰 알람 화면을 구현하기 위해 통합한 Apple의 신규 API
- iOS alarms: AlarmKit 통합 결과가 닮아가도록 참고한 네이티브 알람 경험
- live activity: 잠금 화면과 Dynamic Island에 세션 상태를 표시하는 기능으로 구현됨
- Dynamic Island: 라이브 액티비티가 표시되는 iPhone UI 영역으로 언급됨
- SwiftData: 자동 마이그레이션이 쉬워서 미래 지향적 데이터베이스 구조를 만드는 데 도움이 된 기술로 언급됨
- iPad: 자동 기기 간 동기화가 실제로 동작하는 확인 대상으로 언급됨
- HabitKit: 단순한 온보딩 접근이 이미 잘 작동했다고 비교 기준으로 언급한 저자의 기존 앱
- RevenueCat: 인앱 구매와 구독을 통합한 서비스로, 오퍼링·패키지 설정 및 문서 개선이 쉬웠다고 평가됨
- App Store Connect: RevenueCat와 함께 상품 패키지와 결제 설정을 연결한 Apple 도구
- App Store: 저자가 이번 달 안에 앱을 출시하고자 하는 유통 채널

## 언급된 다른 creator·앱
- HabitKit: 저자의 기존 앱으로, 불필요하게 긴 온보딩 없이도 잘 작동한 사례로 언급됨

## 복제 가능한 전술 (≤3)
1. 통계형 생산성 앱이라면 인사이트 화면을 "전체 기록 + 기간별 추세 + 카테고리 분포 + 스트릭/목표" 구조로 먼저 완성한다.
   - 구체적 스텝: 세션 전체 기록을 스크롤 가능한 히스토리로 제공하고, 총 세션 수와 Focus/Break 시간 합계를 노출한다. 이어서 주·월·년·전체 기간 전환이 가능한 바 차트를 붙이고, 카테고리별 시간 또는 세션 수를 퍼센트와 절대값으로 함께 보여준다. 마지막으로 연속 사용 일수와 주간 목표 진행률을 한 카드에 묶어 동기 부여 요소를 만든다.
   - 예상 리소스: 통계 집계 로직, 차트 컴포넌트, 세션/카테고리 데이터 모델
   - 예상 효과: 사용자가 자신의 습관과 생산성 변화를 더 쉽게 이해하고, 앱에 반복적으로 돌아올 이유가 생긴다.
2. 출시 전에 실제 사용량을 가정한 시드 데이터를 넣고 병목 구간을 직접 최적화한다.
   - 구체적 스텝: 지난 사용 이력을 가정한 대량 세션 데이터를 데이터베이스에 시드한 뒤, 버튼 입력과 통계 화면 반응 속도를 직접 테스트한다. 특히 통계 계산이 몰리는 화면에서 지연이 발생하는지 확인하고, 병목 코드를 찾아 계산과 렌더링 흐름을 최적화한다.
   - 예상 리소스: 시드 데이터 생성 스크립트, 성능 테스트 시간, 프로파일링 도구
   - 예상 효과: 수천 개 세션이 있어도 앱이 더 빠르고 반응적으로 느껴지도록 만들 수 있다.
3. 온보딩은 한 화면으로 최소화하고, 결제와 구독은 검증된 외부 서비스를 붙여 출시 준비 속도를 높인다.
   - 구체적 스텝: 앱 목적만 짧게 설명하는 단일 온보딩 화면을 만들고, 사용자가 Continue를 누르면 즉시 핵심 화면으로 진입시키며 나머지는 UI 자체가 설명하도록 설계한다. 동시에 RevenueCat 같은 서비스를 이용해 오퍼링과 상품 패키지를 구성하고 App Store Connect와 연결해 결제 흐름을 조기에 마무리한다.
   - 예상 리소스: 간단한 온보딩 UI, RevenueCat 계정, App Store Connect 설정 시간
   - 예상 효과: 불필요한 초기 이탈을 줄이고, 출시 직전까지 결제 인프라를 빠르게 안정화할 수 있다.

## 원문 요약 (≤5문장)
저자는 휴가 이후 복귀한 주간에 11월 30일 출시를 목표로 새 포모도로 앱의 주요 기능을 빠르게 마무리했다고 설명한다. 이번 주 핵심 진척은 인사이트 화면 완성, AlarmKit 및 라이브 액티비티 통합, 자동 마이그레이션과 기기 간 동기화가 가능한 데이터 구조 정리였다. 또한 지난 2년치 약 12,000개의 포커스 세션을 시드해 성능 병목을 찾고 통계 화면 반응성을 개선했다. 온보딩은 HabitKit에서 검증된 방식처럼 한 화면으로 단순화했고, RevenueCat과 App Store Connect로 구매 및 구독 설정도 끝냈다. 남은 백로그는 많지만, 작은 버그 수정과 UX 개선을 계속 더하며 이번 달 앱스토어 출시를 밀어붙이겠다는 의지를 밝힌다.

## 본문 포인트별 발췌
> I’m really trying hard to get everything ready for my planned launch on November 30th.
> You can switch between week, month, year, or all-time view to see how your productivity changed over time.
> Since my app will only be available for iOS 26 and above, I had the chance to use this new feature from Apple, which was really cool.
> When I was testing the app, I seeded around 12,000 focus sessions for the past two years to see how it would perform with a lot of data.
> So I only have one screen that explains the purpose of the app in a simple way.
