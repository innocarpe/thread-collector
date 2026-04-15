---
source: blog
creator: sebastian-rohl
url: https://sebastianroehl.substack.com/p/building-an-indie-app-business-91
title: Building An Indie App Business #91
published_at: 2026-02-22
collected_at: 2026-04-15
categories: ["dev-tools", "web-app", "productivity"]
insight_extracted_at: 2026-04-15
---

## 핵심 주장 (≤5)
1. FocusKit의 Apple Watch 통합은 베타 직전 수준까지 진척됐고, 시계에서 세션 제어와 루틴 진행 상황 확인 같은 핵심 사용 흐름을 제공하려 한다.
2. watchOS 개발은 필요한 API가 부족해 단순해 보이는 작업도 창의적인 우회가 필요할 만큼 구현 난도가 높다.
3. 빠른 기능 개발 이후에는 워크플로와 애니메이션 성능 저하가 생기기 쉬워 별도의 최적화 단계가 필요하다.
4. AI는 아이디어를 프로토타입으로 바꾸는 속도를 높여주지만, 그 속도 때문에 오히려 더 많이 일하게 되는 역설을 만든다.
5. Cursor의 Skills와 Rules를 제대로 설정하면 코드베이스에 대한 AI 출력 품질이 눈에 띄게 좋아진다.

## 공개된 숫자·지표
- macOS 사이드 프로젝트 개발 기간: 2년 이상 (기간: 누적, 출처: "If you remember from last week, I finally got it to beta after dragging it around for over 2 years.")
- HabitKit 랜딩 페이지 작업 단위: 30분 (기간: 1회 작업 세션, 출처: "It’s one of those projects you can pick up for 30 minutes when you need a break from your main task.")
- AI로 인한 체감 생산성 증가: 10% (기간: 새 모델이 나올 때의 체감, 출처: "I’m trying to be more intentional about this, but it’s hard when every new model makes you 10% faster.")

## 언급된 도구·서비스
- FocusKit: Apple Watch로 확장 중인 앱으로, 시계에서 세션 시작·정지·리셋·스킵과 루틴 진행 상황 조회를 제공하려고 사용됨
- Apple Watch: FocusKit의 베타 직전 통합 대상 플랫폼으로 언급됨
- watchOS: API 제약과 우회 구현의 어려움을 겪는 개발 대상 운영체제로 언급됨
- AI assistance: 여러 실패한 접근을 시도하는 과정에서도 함께 사용됐지만 어려운 문제는 여전히 남아 있었다는 맥락에서 언급됨
- Xcode: Watch face Complications를 만들 때 개발자 경험이 좋았다고 평가된 도구
- HabitKit: 메인 작업 사이사이에 새 랜딩 페이지를 만드는 대상 앱이자 다음 주 유지보수 대상
- iOS 26 Liquid Glass: Apple의 최근 디자인 방향성 사례로 높게 평가됨
- Apple Music: 최신 iOS 베타에서 디자인 완성도가 특히 좋다고 본 앱
- Cursor: Skills와 Rules, 그리고 새 marketplace를 통해 프로젝트별 AI 작업 환경을 개선하는 도구
- Craft: 생산성 및 저널링 앱으로 시험 사용 중이며, 사용 경험이 아름답고 만족스럽다고 평가됨
- Obsidian: 한동안 사용하려 했지만 거칠고 tasks plugin 경험이 매끄럽지 않다고 평가된 도구
- Flutter: HabitKit을 다시 적극 개발 가능한 상태로 만들기 위해 업그레이드 예정인 프레임워크

## 언급된 다른 creator·앱
- FocusKit: Apple Watch 통합과 성능 디버깅 진척을 설명하는 핵심 앱
- HabitKit: 랜딩 페이지 작업과 다음 주 유지보수 계획의 중심 앱
- Craft: 새 생산성/저널링 앱으로 실사용을 시험 중인 앱
- Obsidian: Craft와 비교 대상으로 언급된 생산성 앱
- Apple Music: 최신 iOS 베타 디자인 사례로 긍정적으로 언급된 앱

## 복제 가능한 전술 (≤3)
1. 메인 제품 개발 사이에 짧은 보조 프로젝트를 병행해 집중력과 생산성을 같이 유지한다.
   - 구체적 스텝: 핵심 개발 과제를 정한 뒤, 피로가 오면 별도 컨텍스트의 소규모 작업(예: 랜딩 페이지)을 꺼내 30분 정도 진행하고 다시 메인 프로젝트로 복귀한다.
   - 예상 리소스: 짧은 작업 슬롯, 별도 프로젝트 1개, 전환 가능한 개발 환경
   - 예상 효과: "Different context, different tech stack, but still productive."라는 방식처럼 신선함을 유지하면서도 중요한 작업의 모멘텀을 잃지 않을 수 있다.
2. Cursor 프로젝트별 Skills와 Rules를 정비하고 marketplace의 검증된 설정을 적극 도입한다.
   - 구체적 스텝: 현재 프로젝트의 Cursor 설정을 점검하고, marketplace에서 battle-tested skills를 찾아 import한 뒤 코드베이스에 맞는 Rules와 Skills를 구성해 AI 출력 결과를 비교한다.
   - 예상 리소스: Cursor, marketplace 탐색 시간, 프로젝트별 규칙 정리 시간
   - 예상 효과: 저자 표현대로 "Having good rules and skills set up for your codebase makes the AI output so much better." 수준의 품질 개선을 기대할 수 있다.
3. 빠르게 기능을 붙인 뒤에는 성능 점검을 별도 작업으로 분리해 워크플로와 애니메이션을 다시 다듬는다.
   - 구체적 스텝: 통합 작업이나 기능 추가가 끝난 시점에 실제 기기 테스트를 하고, 지연되는 워크플로와 어색한 애니메이션을 식별한 뒤 최적화와 베스트 프랙티스 점검에 집중하는 디버깅 세션을 잡는다.
   - 예상 리소스: 실제 테스트 환경, 디버깅 시간, 성능 점검 도구
   - 예상 효과: 빠른 반복 개발 이후 생긴 "lag"와 "janky"한 사용감을 줄여 릴리스 준비도를 높일 수 있다.

## 원문 요약 (≤5문장)
이번 글에서 저자는 FocusKit의 Apple Watch 통합을 베타 직전까지 밀어붙였고, watchOS 개발의 높은 난도와 성능 최적화 필요성을 함께 언급했다. 별도의 macOS 사이드 프로젝트는 릴리스 준비 단계에 가까워졌고, HabitKit은 메인 작업 사이의 짧은 시간에 랜딩 페이지를 만드는 방식으로 병행하고 있다. 인사이트 파트에서는 AI가 개발 속도를 높여주지만 오히려 더 많은 일을 하게 만드는 역설을 짚었다. 또 Cursor의 Skills와 Rules, marketplace를 활용하면 AI 출력 품질이 개선된다고 평가했다. 마지막으로 다음 주에는 HabitKit의 Flutter 업그레이드와 유지보수에 집중할 계획이라고 밝혔다.

## 본문 포인트별 발췌
> "FocusKit Watch Integration is almost ready for beta."
> "That said, building for watchOS is not easy."
> "It’s one of those projects you can pick up for 30 minutes when you need a break from your main task."
> "The tool that should free up your time actually makes you want to spend more time building because the results come so fast."
> "Having good rules and skills set up for your codebase makes the AI output so much better."
