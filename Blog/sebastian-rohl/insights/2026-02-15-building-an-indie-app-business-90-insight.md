---
source: blog
creator: sebastian-rohl
url: https://sebastianroehl.substack.com/p/building-an-indie-app-business-90
title: Building An Indie App Business #90
published_at: 2026-02-15
collected_at: 2026-04-15
categories: ["dev-tools", "ai-llm", "productivity"]
insight_extracted_at: 2026-04-15
---

## 핵심 주장 (≤5)
1. 도구와 프롬프팅에 시간을 쓰더라도, 이후 개발 속도를 높일 수 있는 시스템 구축은 의미가 있다.
2. 계절적 매출 하락기에는 대시보드 변동에 집착하기보다 제품 개선에 집중하는 편이 더 낫다.
3. AI의 도움을 받아 장기간 미뤄온 사이드 프로젝트도 베타 단계까지 밀어붙일 수 있다.
4. AI 코딩은 `계획-구현-리뷰`로 역할을 분리할 때 생산성과 통제력을 동시에 확보할 수 있다.
5. AI 시대에는 직접 코드를 짜는 능력만큼, 원하는 결과를 명확하게 설명하는 능력이 중요해진다.

## 공개된 숫자·지표
- 사이드 프로젝트 개발 기간: 2년 이상 (기간: 누적, 출처: "I’ve been dragging this macOS app around for over 2 years now!")
- 유튜브 영상 길이 예시: 30분 (기간: 단일 영상 예시, 출처: "So now instead of watching a 30-minute video, I can just feed it the link and get a clean summary in seconds.")
- 요약 생성 속도: 몇 초 (기간: 단일 작업 예시, 출처: "So now instead of watching a 30-minute video, I can just feed it the link and get a clean summary in seconds.")
- 기능 구현 시도 시간: 약 1시간 (기간: 이번 주 단일 작업, 출처: "I spent about an hour trying different approaches before accepting defeat.")
- 산만함으로 소모한 시간: 45분 (기간: 단일 세션 예시, 출처: "I always tell myself “just one video” or “just a quick scroll” and then 45 minutes have passed and I feel worse than before.")

## 언급된 도구·서비스
- HabitKit: 작성자의 기존 앱으로, 매출 흐름과 버그 수정 맥락에서 언급됨
- FocusKit: 작성자의 기존 앱으로, MRR·업데이트·WatchKit 통합 작업 맥락에서 언급됨
- RevenueCat: 매출 변동을 확인하던 대시보드로 언급됨
- SwiftUI: 툴바 날짜 선택기에 롱프레스 제스처를 붙이려 했지만 API 제약으로 어려움을 겪은 기술 스택
- WatchKit: FocusKit의 Apple Watch 통합 작업에 사용 중인 프레임워크
- OpenClaw: 개인 AI 어시스턴트 환경을 구축하는 데 사용 중인 도구
- YouTube: AI가 링크를 받아 요약하는 콘텐츠 소스로 사용됨
- knowledge base: YouTube 요약을 저장하는 지식 저장소로 사용됨
- MiniMax M2.5: 향후 테스트해보려는 모델로 언급됨
- Opus 4.6: 기능 요구사항, 아키텍처, 엣지 케이스를 포함한 계획 수립에 사용됨
- Codex 5.3: Cursor 안에서 실제 코드 구현에 사용됨
- Cursor: Codex 5.3으로 구현 작업을 수행하는 개발 환경으로 언급됨
- X: AI 관련 정보를 얻지만 동시에 주의를 분산시키는 소셜 플랫폼으로 언급됨
- Reddit: 집중력을 해치는 플랫폼으로 언급됨

## 언급된 다른 creator·앱
- Apple: FocusKit을 Apple이 직접 만든 것처럼 느껴지게 하고 싶다는 제품 비전의 기준점으로 언급됨

## 복제 가능한 전술 (≤3)
1. AI 코딩 워크플로를 `계획 모델-구현 모델-인간 리뷰` 3단계로 분리한다.
   - 구체적 스텝: 구현할 기능의 요구사항·아키텍처·엣지 케이스를 먼저 계획용 모델에 입력해 단계별 설계를 만든 뒤, 그 계획을 구현용 모델에 넘겨 코드 생성에 사용하고, 마지막으로 사람이 결과물을 읽고 테스트하며 명백한 오류를 수정한다.
   - 예상 리소스: 계획용 LLM 1개, 구현용 LLM 1개, 코드 편집기(Cursor), 수동 리뷰 시간
   - 예상 효과: 직접 전부 코딩할 때보다 더 빠르게 움직이면서도 코드베이스 통제력을 유지할 수 있다.
2. 장기 미뤄둔 프로젝트는 AI를 활용해 먼저 내부 테스터에게 보여줄 수 있는 베타 상태까지 끌어올린다.
   - 구체적 스텝: 미뤄진 프로젝트를 완성도보다 작동 가능성 기준으로 재정의하고, AI 보조로 핵심 동작을 구현한 뒤 첫 내부 테스터에게 전달 가능한 수준까지 우선 출하한다.
   - 예상 리소스: AI 코딩 보조 도구, 내부 테스터 1명, 베타 배포 준비 시간
   - 예상 효과: 머릿속에만 있던 프로젝트를 실제 사용자 검증 단계로 옮겨 심리적 정체를 해소할 수 있다.
3. AI 어시스턴트에 반복형 요약 작업과 자체 작업 공간을 부여해 활용도를 높인다.
   - 구체적 스텝: YouTube 링크를 입력하면 자동으로 요약해 지식 베이스에 저장하는 커스텀 스킬을 만들고, 별도로 AI가 자신의 작업·능력·저널을 관리할 전용 워크스페이스를 구성한다.
   - 예상 리소스: OpenClaw 같은 AI 어시스턴트 환경, 지식 베이스, 커스텀 스킬 설정 시간
   - 예상 효과: 긴 영상을 직접 보지 않고도 핵심 내용을 빠르게 흡수하고, AI가 더 많은 자기 맥락을 가질수록 성능이 좋아진다.

## 원문 요약 (≤5문장)
이번 글에서 작성자는 매출보다 시스템 구축과 개발 워크플로 개선에 집중한 한 주를 정리한다. AI의 도움으로 2년 넘게 미뤄온 macOS 사이드 프로젝트를 내부 베타 단계까지 진전시켰고, FocusKit 1.2.1의 UX 개선과 WatchKit 통합 기반 작업도 진행했다. 개인 AI 어시스턴트 OpenClaw에는 유튜브 요약 스킬과 자체 작업 공간을 추가해 활용도를 높였다. 코딩 워크플로는 Opus 4.6으로 계획하고 Codex 5.3으로 구현한 뒤 직접 리뷰하는 방식이 현재 가장 잘 맞는다고 평가한다. 동시에 X, Reddit, YouTube 같은 플랫폼이 집중력을 해친다는 점도 자각하며 다시 절제된 작업 습관으로 돌아갈 필요를 강조한다.

## 본문 포인트별 발췌
> "But sometimes that’s exactly what you need to do to move faster later."
> "But this week, with some heavy AI assistance, I finally got it to a state where I can put it in front of the first internal tester."
> "The more context the AI has about itself and what it can do, the better it performs."
> "This workflow has been incredibly productive for me lately."
> "I’m starting to think less about “how do I code this?” and more about “how do I describe what I want so an AI can build it?”"
