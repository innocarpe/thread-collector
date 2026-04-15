---
source: blog
creator: sebastian-rohl
url: https://sebastianroehl.substack.com/p/building-an-indie-app-business-96
title: Building An Indie App Business #96
published_at: 2026-03-29
collected_at: 2026-04-15
categories: ["case-study", "aso", "web-app"]
insight_extracted_at: 2026-04-15
---

## 핵심 주장 (≤5)
1. HabitKit 1.15.0 구현이 완료됐고, 가장 많이 요청된 기능 중 하나였던 리스트 뷰 홈 화면 위젯을 모든 플랫폼에 제공하는 업데이트다.
2. HabitKit이 오스트리아에서 "habit tracker" 키워드 1위를 기록했고, 이는 현재 ASO 전략이 효과를 내고 있다는 검증으로 해석된다.
3. AI 코딩 도구 덕분에 익숙하지 않은 프레임워크, 서버 인프라, 플랫폼 API를 포함한 복잡한 기능과 프로젝트도 솔로 개발자가 시도 가능한 범위로 들어왔다.
4. Claude Cowork를 Obsidian vault와 연결해 프로젝트, 작업, 아이디어를 이해하는 AI 운영 보조 체계를 만들고 있으며, 자동화 신뢰성이 높아져 실제 운영에 쓸 수 있다고 본다.
5. AI를 활용해 아침 브리핑, 이메일 초안 작성, 저녁 저널 인사이트 추출까지 일과 운영 루틴을 자동화하려 한다.

## 공개된 숫자·지표
- HabitKit App Store 순위: "habit tracker" 키워드 오스트리아 1위 (기간: 해당 주, 출처: "HabitKit hit #1 for “habit tracker” in Austria.")
- HabitKit 버전: 1.15.0 (기간: 해당 주 개발 완료 시점, 출처: "HabitKit 1.15.0 is done.")
- FocusKit 버전: 1.4.0 (기간: 백로그 상태인 다음 업데이트, 출처: "FocusKit 1.4.0 widgets still on the backlog.")
- MacOS 앱 릴리스 범위: 1.0 기능 완성 상태 (기간: 해당 주, 출처: "The app itself is feature-complete for 1.0, what’s left is mostly the business side: RevenueCat integration, App Store listing, legal documents, and a landing page.")
- Claude Cowork 아침 점검 시간: 오전 6시 (기간: 매일, 출처: "every morning at 6 AM, Claude reviews my Second Brain, checks what’s on my plate, and delivers an actionable briefing for the day.")
- Claude Cowork 저녁 점검 시간: 오후 6시 (기간: 매일, 출처: "In the evening at 6 PM, it goes through my journal notes from the day and extracts noteworthy insights back into the vault.")

## 언급된 도구·서비스
- HabitKit: 습관 추적 앱으로, 1.15.0 업데이트에 리스트형 홈 화면 위젯과 버그 수정이 포함됨
- Flutter: HabitKit 1.15.0 구현 과정에서 툴링 정비에 사용됨
- App Store: HabitKit 검색 순위 성과 측정과 비공개 MacOS 프로젝트 출시 준비에 사용됨
- RevenueCat: 비공개 MacOS 프로젝트 출시 전 필요한 결제/비즈니스 인프라 항목으로 언급됨
- Claude Cowork: Obsidian vault와 연결해 일정 기반 브리핑, 이메일 초안 작성, 저널 인사이트 추출을 수행하는 AI 보조 도구
- Obsidian: Second Brain 저장소로 사용되며 Claude Cowork가 연결되는 지식 베이스
- OpenClaw: 과거에 유사 자동화를 시도했지만 cron job 신뢰성 문제로 중단한 도구
- cron jobs: 과거 자동화 시도에서 안정적으로 돌지 않았던 스케줄 실행 방식
- FocusKit: 다음 위젯 업데이트가 밀린 상태인 앱

## 언급된 다른 creator·앱
- HabitKit: 개발 완료, ASO 성과, 위젯 기능 확장 맥락에서 반복 언급됨
- FocusKit: iOS 홈 화면 위젯 업데이트가 백로그에 남아 있는 앱으로 언급됨
- Claude Cowork: 개인 운영 자동화 실험의 핵심 앱으로 언급됨
- OpenClaw: 이전에 시도했던 대안 도구로 언급됨

## 복제 가능한 전술 (≤3)
1. 작은 국가/시장부터 핵심 검색어 ASO 성과를 검증하고, 순위가 잡히는 패턴을 확인한 뒤 다른 국가로 확장한다.
   - 구체적 스텝: 앱의 핵심 검색어를 정해 스토어 리스팅을 지속 개선한다; 작은 시장에서도 해당 키워드 순위를 추적한다; 순위 상승이 확인되면 같은 방향으로 다른 국가 리스팅을 확장한다.
   - 예상 리소스: App Store 리스팅 편집 권한, 순위 모니터링 시간
   - 예상 효과: 작은 시장 기준이라도 핵심 경쟁 키워드 상위 노출을 통해 ASO 전략의 유효성을 검증할 수 있다.
2. AI 비서를 개인 지식 저장소와 연결해 하루 2회 운영 루틴을 자동화한다.
   - 구체적 스텝: 프로젝트·작업·아이디어가 모여 있는 Second Brain을 준비한다; Claude Cowork 같은 도구를 vault에 연결한다; 오전에는 당일 브리핑과 미처리 이메일/지원 메일 초안 생성을 예약한다; 저녁에는 당일 저널 노트에서 인사이트를 추출해 다시 vault에 적재하도록 설정한다.
   - 예상 리소스: Claude Cowork, Obsidian vault, 스케줄 설정 시간
   - 예상 효과: 깊은 작업에 집중하는 동안 운영성 업무 일부를 AI가 선행 처리해 주는 체계를 만들 수 있다.
3. 기능 개발이 끝난 뒤 출시 체크리스트를 비즈니스 작업 단위로 분리해 마무리한다.
   - 구체적 스텝: 제품이 1.0 기능 완성 상태인지 확인한다; 남은 작업을 RevenueCat 연동, App Store 리스팅, 법률 문서, 랜딩 페이지처럼 출시 필수 항목으로 분해한다; 구현보다 출시 준비 항목을 우선순위로 전환한다.
   - 예상 리소스: 결제 도구, 스토어 메타데이터 작업 시간, 법률 문서 준비, 랜딩 페이지 제작
   - 예상 효과: 기능 완료 후 실제 출시를 막는 운영·비즈니스 병목을 빠르게 해소할 수 있다.

## 원문 요약 (≤5문장)
이번 글에서 저자는 HabitKit 1.15.0 개발을 마쳤고, 리스트형 홈 화면 위젯과 각종 버그 수정을 포함한 업데이트를 곧 심사에 제출할 예정이라고 밝혔다. 또한 HabitKit이 오스트리아 App Store에서 "habit tracker" 검색어 1위를 기록해 ASO 전략의 성과를 확인했다고 설명한다. 비공개 MacOS 프로젝트는 1.0 기능 개발이 끝났고, 이제 RevenueCat 연동, 스토어 등록, 법률 문서, 랜딩 페이지 같은 출시 준비만 남아 있다고 정리했다. 인디 인사이트로는 AI 코딩 도구가 솔로 개발자의 실행 범위를 넓혀 주고 있으며, Claude Cowork와 Obsidian을 연결해 일일 브리핑, 이메일 초안, 저널 인사이트 추출을 자동화하는 운영 체계를 실험 중이라고 공유했다.

## 본문 포인트별 발췌
> **HabitKit 1.15.0 is done.**
> **HabitKit hit #1 for “habit tracker” in Austria.**
> Seeing HabitKit rank at the top for such a competitive keyword, even if it’s a smaller market, validates that the ASO strategy is working.
> **AI is giving me more confidence as a developer.**
> Here’s what I’ve set up so far: every morning at 6 AM, Claude reviews my Second Brain, checks what’s on my plate, and delivers an actionable briefing for the day.
