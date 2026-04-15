---
source: blog
creator: sebastian-rohl
url: https://sebastianroehl.substack.com/p/building-an-indie-app-business-88
title: Building An Indie App Business #88
published_at: 2026-02-01
collected_at: 2026-04-15
categories: ["ai-llm", "startup-philosophy", "productivity"]
insight_extracted_at: 2026-04-15
---

## 핵심 주장 (≤5)
1. AI는 더 이상 단순 코딩 보조 도구가 아니라, 개발자가 전체 프로젝트를 위임하고 관리하는 생산성 게임 체인저가 되고 있다.
2. 인디 개발자에게 중요한 일상 업무는 직접 코드를 타이핑하는 것보다 문제를 명확히 정의하고 솔루션을 설계하는 쪽으로 이동하고 있다.
3. 작은 UX 개선도 사용자 혼란을 줄이고 제품의 반응성과 신뢰감을 크게 높일 수 있다.
4. AI 결과물을 맹신할 수는 없지만, 개발 이해도를 가진 운영자가 검토와 피드백을 전제로 활용하면 더 빠르게 제품을 전진시킬 수 있다.
5. 앞으로는 순수 코딩 능력만이 아니라 문제 정의, 해결책 설계, AI 에이전트 오케스트레이션 능력이 더 중요해질 가능성이 크다.

## 공개된 숫자·지표
- FocusKit 업데이트 버전: 1.2.1 (기간: 이번 주, 출처: "I made good progress on FocusKit 1.2.1 this week.")
- 시도 시간: 약 1시간 (기간: 이번 주, 출처: "I spent about an hour trying different approaches before I accepted defeat.")
- 생성된 앱 규모: 33 files (기간: 수요일 밤부터 다음 날 아침까지, 출처: "When I woke up on Wednesday morning, there was a working React app waiting for me. 33 files.")
- 생성된 코드 규모: almost 8,000 lines of code (기간: 수요일 밤부터 다음 날 아침까지, 출처: "Almost 8,000 lines of code.")
- 팟캐스트 분량: about an hour (기간: 공개된 에피소드, 출처: "If you want to hear me ramble for about an hour about my indie journey, check out the latest episode")
- 에피소드 번호: 84 (기간: 공개된 에피소드, 출처: "check out the latest episode")

## 언급된 도구·서비스
- OpenClaw: 개인용 AI assistant로 언급되며, 필자의 AI와 일에 대한 관점을 바꾸는 계기가 된 최신 화제 주제
- FocusKit: 필자가 개발 중인 앱으로, 이번 글에서 1.2.1 업데이트의 UX 개선 사례를 설명하는 데 사용됨
- SwiftUI: 툴바의 date picker 길게 누르기 기능을 구현하려 했지만 API 제약 때문에 깔끔한 방식으로 구현하지 못한 프레임워크
- React: 잠자는 동안 AI가 만들어 둔 Second Brain 웹 앱의 구현 기술
- GitHub: Second Brain 앱에서 마크다운 파일 자동 커밋과 버전 히스토리 저장에 사용되며, AI가 결과물을 push한 대상으로도 언급됨
- Telegram: 봇과 대화해 대시보드의 작업을 자동 추가/삭제하는 인터페이스로 언급됨
- Copilot: 2년 전부터 쓰기 시작한 AI 코딩 도우미의 예시로 언급됨

## 언급된 다른 creator·앱
- Obsidian: 필자가 원하는 Second Brain 앱의 기본 방향과 유사한 기준점으로 언급됨
- Charlie Chapman: 팟캐스트 "Launched"에 필자를 초대한 진행자
- HabitKit: 빌드 인 퍼블릭과 느린 성장 속 지속성의 맥락에서 언급된 필자의 앱
- Launched: 필자가 게스트로 출연한 팟캐스트

## 복제 가능한 전술 (≤3)
1. 사용자 혼란이 발생하는 비어 있는 상태를 현재 진행 상태가 보이도록 바꿔 UX 신뢰감을 높인다.
   - 구체적 스텝: 지원 메일이나 사용자 문의에서 반복되는 혼란 지점을 찾는다 -> 해당 화면의 empty state 원인을 확인한다 -> 진행 중인 세션이나 작업을 임시 상태로라도 UI에 노출한다 -> 애니메이션이나 상태 표시를 더해 "앱이 정상 작동 중"이라는 신호를 준다 -> 배포 후 동일 문의가 줄어드는지 확인한다
   - 예상 리소스: 제품 로그 또는 지원 메일, UI 수정 시간, 프론트엔드 구현 도구
   - 예상 효과: 사용자가 앱이 세션을 추적하지 않는다고 오해하는 문제를 줄이고, 앱이 더 살아 있고 반응성 있게 느껴지게 한다
2. AI 에이전트에는 구현 방법보다 필요한 기능과 그 이유를 명확히 설명하고, 작업은 비동기로 맡긴 뒤 결과물을 검토한다.
   - 구체적 스텝: 필요한 기능 목록과 각 기능의 사용 이유를 문서화한다 -> AI assistant에게 WHAT과 WHY 중심으로 지시한다 -> 결과물 생성 동안 직접 붙어서 코딩하지 않는다 -> 완료 후 코드, 동작, 문서를 검토한다 -> 승인하거나 다음 반복을 위한 피드백을 준다
   - 예상 리소스: AI assistant, 요구사항 정리 시간, 코드 리뷰 및 테스트 시간, GitHub 같은 버전 관리 도구
   - 예상 효과: 잠자는 동안에도 작동하는 수준의 결과물을 받아 개발 속도를 높이고, 운영자는 문제 정의와 검토에 집중할 수 있다
3. 개인 워크플로우에 맞는 생산성 도구는 마크다운과 버전 관리 중심으로 단순한 기반부터 만든다.
   - 구체적 스텝: 노트를 markdown 기반으로 두고 PARA 구조를 정한다 -> 파일 브라우저, 방해 없는 에디터, 클릭 가능한 task checkbox, auto-save, GitHub auto-commit 같은 핵심만 먼저 정의한다 -> 이후 time tracking, todo management 같은 커스텀 기능은 확장으로 붙인다
   - 예상 리소스: markdown 파일 저장소, GitHub, 웹 앱 프론트엔드, 개인 워크플로우 설계 시간
   - 예상 효과: 오프라인 의존도를 낮추면서 개인 요구에 정확히 맞는 Second Brain 기반을 만들 수 있다

## 원문 요약 (≤5문장)
필자는 이번 주 FocusKit 1.2.1에서 현재 진행 중인 세션을 History 탭에 표시하는 작은 UX 개선을 추가했고, 이런 디테일이 사용자 혼란을 줄인다고 설명한다. 동시에 OpenClaw를 계기로 AI를 단순 코딩 보조가 아니라 전체 프로젝트를 맡길 수 있는 생산성 시스템으로 보기 시작했다고 말한다. 그는 수요일 밤 AI assistant에게 Second Brain 웹 앱 요구사항을 설명한 뒤, 다음 날 아침 33개 파일과 거의 8,000줄 코드로 동작하는 React 앱을 받았다고 전한다. 이 경험을 바탕으로 인디 개발자의 역할은 직접 구현보다 문제 정의, 솔루션 설계, AI 에이전트 관리 쪽으로 이동하고 있다고 주장한다. 마지막으로 Charlie Chapman의 팟캐스트 Launched에 출연해 HabitKit, 빌드 인 퍼블릭, 사용자 중심 개발에 대해 이야기했다고 덧붙인다.

## 본문 포인트별 발췌
> I’m not just using AI as a coding helper anymore. I’m starting to see it as a complete productivity game changer.
> When I woke up on Wednesday morning, there was a working React app waiting for me. 33 files. Almost 8,000 lines of code.
> It’s not about coding WITH AI anymore. It’s more like managing AI developers.
> It’s less about typing code and more about thinking clearly about problems and solutions.
> We can spend more time on the things that actually matter: figuring out what users really need, making the product better, talking to customers, and growing the business.
