---
source: blog
creator: sebastian-rohl
url: https://sebastianroehl.substack.com/p/focuskit-is-live
title: FocusKit is LIVE
published_at: 2025-11-29
collected_at: 2026-04-15
categories: ["product-strategy", "monetization", "web-app"]
insight_extracted_at: 2026-04-15
---

## 핵심 주장 (≤5)
1. FocusKit은 "가장 깔끔하고, 우아하며, 차분한" 포커스 타이머를 목표로 한 iOS 네이티브 포모도로 앱이다.
2. 제품 차별점은 단순한 타이머가 아니라 세션 메모, 카테고리, 통계, Live Activities, AlarmKit 기반 알림 같은 iOS 네이티브 경험의 결합에 있다.
3. 생산성 데이터는 주·월·연·전체 기간 단위의 시각화와 카테고리 필터링을 통해 사용자가 자신의 집중 패턴을 이해하도록 설계됐다.
4. 작성자는 Flutter로 HabitKit을 만든 경험 이후, SwiftUI·SwiftData·iCloud sync 등 iOS 생태계를 적극 활용하는 방향으로 전환했다.
5. 출시 직후 다운로드와 앱스토어 평점·리뷰 요청을 함께 노출해 초기 배포와 사회적 증거를 동시에 확보하려 한다.

## 공개된 숫자·지표
- 없음

## 언급된 도구·서비스
- FocusKit: 새로 출시한 네이티브 iOS 포모도로 타이머 앱
- App Store: 앱 다운로드 링크를 제공하고 평점·리뷰를 요청한 배포 채널
- Pomodoro technique: 집중 세션과 휴식 세션 운영 방식의 핵심 프레임워크
- AlarmKit: 앱이 닫혀 있거나 기기가 Silent/Focus 모드여도 세션 종료 알림을 보내는 데 사용한 시스템 기능
- Live Activities: 잠금 화면과 Dynamic Island에서 세션을 추적하고 제어하는 데 사용한 iOS 기능
- Dynamic Island: 세션 카운트다운과 제어 UI를 노출하는 시스템 표면
- iCloud Sync: 세션과 카테고리를 기기 간 자동 동기화하는 데 사용한 기능
- SwiftUI: 이 앱을 "fully native"하게 구현한 주요 UI 프레임워크
- SwiftData: iOS 네이티브 데이터 관리 스택으로 언급됨
- Flutter: 이전 앱 HabitKit을 수년간 개발할 때 사용했던 프레임워크

## 언급된 다른 creator·앱
- HabitKit: 작성자가 수년간 Flutter로 개발해온 기존 앱

## 복제 가능한 전술 (≤3)
1. 출시 공지에서 제품 철학과 핵심 차별점을 한 번에 압축해 전달한다.
   - 구체적 스텝: 첫 문단에서 출시 사실을 명확히 알린다. 이어서 "깔끔함", "우아함", "차분함"처럼 제품이 지향하는 감각을 한 문장으로 정의한다. 이후 기능 목록은 그 철학을 뒷받침하는 항목만 남겨 소개한다.
   - 예상 리소스: 출시 공지 글 1편, 제품 소개 문구 정리 시간
   - 예상 효과: 사용자가 앱을 기능 모음이 아니라 분명한 사용 경험으로 인식하게 된다.
2. 플랫폼 고유 기능을 전면에 내세워 경쟁 앱과의 차이를 만든다.
   - 구체적 스텝: 잠금 화면, Dynamic Island, Silent/Focus 모드 대응처럼 특정 OS에서만 가능한 경험을 추린다. 각 기능이 실제 사용 흐름에서 어떤 불편을 줄이는지 설명한다. "네이티브라서 가능한 점"을 별도 문단으로 묶어 강조한다.
   - 예상 리소스: 네이티브 기능 구현, 제품 설명 문구 작성 시간, iOS 시스템 기능 이해
   - 예상 효과: 단순 포모도로 앱이 아니라 iOS 생태계에 최적화된 제품이라는 인상을 강화할 수 있다.
3. 출시 직후 다운로드 요청과 리뷰 요청을 함께 배치한다.
   - 구체적 스텝: 공지 상단에 다운로드 링크를 둔다. 바로 다음 문장에서 다운로드와 앱스토어 평점·리뷰를 함께 요청한다. 마지막에는 피드백을 환영한다는 문장으로 후속 의견 수집 채널을 연다.
   - 예상 리소스: App Store 링크, 공지 채널 1개 이상
   - 예상 효과: 초기 설치 수와 사용자 피드백 확보를 동시에 유도할 수 있다.

## 원문 요약 (≤5문장)
작성자는 새 네이티브 iOS 포모도로 앱 FocusKit의 앱스토어 출시를 알렸다. 그는 이 앱을 군더더기 없는 차분한 포커스 타이머로 포지셔닝하며, 커스텀 세션, 통계, 카테고리, 알람, Live Activities, iCloud 동기화를 핵심 기능으로 소개한다. 특히 AlarmKit, Dynamic Island, Live Activities 같은 iOS 시스템 기능을 활용해 네이티브 경험을 강조한다. 또한 HabitKit을 Flutter로 개발해온 이후 이번에는 SwiftUI와 iCloud 중심의 iOS 생태계를 전면적으로 받아들였다고 설명한다. 글 전체는 다운로드, 평점·리뷰, 피드백 요청으로 마무리된다.

## 본문 포인트별 발췌
> I’m super excited to share something with you: **FocusKit**, my brand-new native iOS Pomodoro timer app is officially live on the App Store today.
> FocusKit is my attempt at building the cleanest, most elegant, and most calming focus timer you’ve ever used.
> Your productivity visualized with clean charts that help you understand when and how you work best.
> Unlike traditional notifications, alarms powered by AlarmKit work even when your device is in Silent or Focus mode, ensuring your focus sessions end on time.
> After building HabitKit with Flutter for years, I wanted to embrace everything iOS has to offer: **Live Activities, Dynamic Island, Alarms, native animations, SwiftData, iCloud sync**, the whole ecosystem.
