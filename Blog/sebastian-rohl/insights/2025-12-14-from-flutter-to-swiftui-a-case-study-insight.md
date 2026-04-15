---
source: blog
creator: sebastian-rohl
url: https://sebastianroehl.substack.com/p/from-flutter-to-swiftui-a-case-study
title: From Flutter to SwiftUI - A Case Study
published_at: 2025-12-14
collected_at: 2026-04-15
categories: ["case-study", "web-app", "dev-tools"]
insight_extracted_at: 2026-04-15
---

## 핵심 주장 (≤5)
1. Flutter는 초기 인디 앱 개발 단계에서 단일 코드베이스로 iOS와 Android를 동시에 출시하며 빠르게 기능을 출시하기에 유리했다.
2. 앱이 성장하고 네이티브 기능 요구가 늘어나면 Flutter의 "하나의 코드베이스" 장점이 약해지고, 실제로는 추가 네이티브 코드베이스를 유지해야 한다.
3. Apple 생태계에 집중할 경우 SwiftUI는 위젯, Shortcuts, Live Activities 같은 네이티브 시스템 통합에서 Flutter보다 훨씬 단순하다.
4. 개발 도구 경험은 Flutter가 우세하지만, Apple 전용 앱 전략과 네이티브 기능 활용이 중요하면 SwiftUI가 더 적합하다.
5. 작성자는 기존 Flutter 앱은 유지하되, 향후 신규 프로젝트는 SwiftUI 중심으로 가는 쪽이 더 높은 심리적 안정성과 운영 효율을 준다고 판단했다.

## 공개된 숫자·지표
- 초기 플랫폼별 매출 비중: 50-50 (기간: "At one point", 출처: "At one point, the revenue share across platforms for my app business was 50-50.")
- HabitKit 외부 패키지 수: 50개 이상 (기간: 명시 없음, 출처: "My app HabitKit uses over 50 different external packages, which shows how rich the ecosystem is.")
- 현재 플랫폼별 매출 비중: 75-25 (기간: "Nowadays", 출처: "Nowadays the revenue split between iOS and Android is 75-25 (and the gap is growing and growing).")
- 인디 앱 여정 초기 안정기: 첫 12개월 (기간: 초기 단계, 출처: "The first 12 months of my indie app journey were a breeze, at least from a technical point of view.")

## 언급된 도구·서비스
- Flutter: 작성자가 3개의 앱을 만든 크로스플랫폼 프레임워크이자, 초기 개발 속도와 동시 출시의 핵심 도구로 언급됨
- SwiftUI: 새 앱 FocusKit을 전부 구축한 Apple 네이티브 UI 프레임워크로, 네이티브 기능 통합 장점이 강조됨
- ASP.NET: 작성자의 첫 실무 소프트웨어 엔지니어링 직장에서 사용한 웹 기술 스택으로 언급됨
- Angular: 작성자가 웹 SPA 개발 경험을 쌓았고, Flutter의 선언형 UI가 익숙하게 느껴진 배경으로 언급됨
- Azure: 첫 실무에서 다뤘던 웹 기술로 언급됨
- Udemy: 모바일 개발 학습에 활용한 강의 플랫폼으로 언급됨
- The Complete Flutter Development Bootcamp with Dart: Angela Yu의 Flutter 학습 강의로, 작성자의 Flutter 진입 계기로 언급됨
- Firebase: Flutter 생태계에서 라이브러리 추가가 쉬운 예시이자, 동기화 백엔드 대안 서비스로 언급됨
- PowerSync: Flutter에서 동기화를 위해 고려할 수 있는 서드파티 서비스 예시로 언급됨
- Google Play: 뉴스레터 링크 문제로 리뷰팀 분쟁이 있었다고 언급된 Android 배포 채널
- VSCode: Flutter의 공식 개발 환경으로 쓸 수 있다는 점이 큰 장점으로 언급됨
- Xcode: SwiftUI 개발에 사실상 묶이는 IDE로, 느리고 불편하다고 평가됨
- Cursor: 작성자가 코드는 여기서 작성하고 앱 실행은 Xcode에서 하는 우회 조합으로 언급함
- Inject: Swift에서 hot reload 대안처럼 쓰이지만 공식 Flutter 경험에 못 미치는 해킹성 솔루션으로 언급됨
- WWDC videos: Apple 생태계 학습 자료 중 가장 가치 있는 리소스로 언급됨
- React Native: Liquid Glass 같은 iOS 스타일을 크로스플랫폼으로 구현하려면 더 나을 수 있는 대안으로 언급됨
- Cupertino widget library: Flutter의 iOS 스타일 위젯 라이브러리로, Liquid Glass 구현에 부족하다고 언급됨
- Impeller: Flutter의 새 렌더링 엔진으로, shader jank 문제를 완전히 해결하지 못했다고 언급됨
- iCloud sync: SwiftUI와 Apple 생태계 집중 시 데이터베이스 동기화를 단순화하는 방법으로 언급됨

## 언급된 다른 creator·앱
- Angela Yu: 작성자가 수강한 Flutter 강의의 강사
- HabitKit: 작성자가 Flutter로 만든 앱이자 성공 사례, 성능 문제와 네이티브 기능 확장의 한계를 설명하는 핵심 사례
- FocusKit: 작성자가 SwiftUI로 전환해 만든 새 앱

## 복제 가능한 전술 (≤3)
1. 신규 앱의 플랫폼 전략을 사용자 비중과 네이티브 기능 요구를 기준으로 먼저 결정한다.
   - 구체적 스텝: 앱 아이디어 단계에서 목표 플랫폼을 정리하고, 위젯·Shortcuts·Live Activities·Lock Screen/Home Screen Widgets 같은 네이티브 기능이 핵심인지 확인한 뒤, 양 플랫폼 동시 출시가 핵심이면 Flutter를, Apple 전용과 깊은 네이티브 통합이 핵심이면 SwiftUI를 선택한다.
   - 예상 리소스: 기획 시간, 목표 사용자 분석, Flutter 또는 SwiftUI 중 하나의 주 개발 스택
   - 예상 효과: 초기에는 빠른 출시와 멀티플랫폼 도달을 얻거나, 반대로 Apple 생태계 통합과 운영 단순성을 더 크게 확보할 수 있다.
2. 크로스플랫폼 앱이라도 네이티브 기능 요구가 생기면 추가 코드베이스 유지 비용을 조기에 반영한다.
   - 구체적 스텝: 기능 로드맵에 Home Screen widgets, Lock Screen widgets, Shortcuts 등 네이티브 기능 요구를 따로 표시하고, 해당 기능이 들어가는 시점부터 Swift/Kotlin 네이티브 모듈 유지 계획과 학습 부담을 일정에 포함한다.
   - 예상 리소스: Flutter 코드베이스 외에 Swift, Kotlin, 각 플랫폼 API 학습 및 유지보수 시간
   - 예상 효과: "하나의 코드베이스로 끝난다"는 착시를 줄이고, 실제 유지보수 복잡도를 더 정확히 예측할 수 있다.
3. 로컬 전용 앱이 성장하기 전에 동기화 전략을 선행 설계한다.
   - 구체적 스텝: 초기에 로컬 DB만 둘지 결정할 때부터 다중 기기 사용 요구를 점검하고, 크로스플랫폼이면 Firebase·PowerSync 같은 백엔드/서드파티 동기화 옵션을 검토하며, Apple 전용이면 iCloud sync 적용 가능성을 먼저 평가한다.
   - 예상 리소스: 데이터 모델 점검, 백엔드 또는 서드파티 서비스 검토, Apple 전용일 경우 iCloud sync 설정
   - 예상 효과: 앱이 인기를 얻은 뒤 뒤늦게 동기화를 붙이는 큰 장벽을 줄이고, 플랫폼 전략에 맞는 더 단순한 동기화 경로를 확보할 수 있다.

## 원문 요약 (≤5문장)
작성자는 웹 개발 배경에서 Flutter를 선택해 여러 앱을 빠르게 출시했고, 특히 HabitKit으로 성과를 냈다. 그러나 앱이 성장하면서 성능 이슈, 네이티브 기능 확장 비용, 동기화 백엔드 부담, Android 대비 낮아진 수익성이 겹치며 Flutter의 장점이 약해졌다고 설명한다. 반대로 SwiftUI는 Xcode와 개발 도구 경험은 불편하지만 Apple 생태계 기능 통합, 디자인 반영, 장기 안정성 면에서 더 낫다고 본다. 그래서 기존 Flutter 앱은 유지하되 신규 앱 FocusKit은 SwiftUI로 만들었고, 앞으로도 Apple 중심 프로젝트에는 SwiftUI를 우선 고려하겠다고 정리한다. 결론적으로 프레임워크 선택은 기술 취향보다 플랫폼 전략과 사업 목표에 맞춰야 한다는 메시지다.

## 본문 포인트별 발췌
> "At one point, the revenue share across platforms for my app business was 50-50."
> "My app HabitKit uses over 50 different external packages, which shows how rich the ecosystem is."
> "Nowadays the revenue split between iOS and Android is 75-25 (and the gap is growing and growing)."
> "If you want to support many native-only features in your apps, do yourself a favor and pick SwiftUI instead of Flutter."
> "For me personally, the switch was worth it."
