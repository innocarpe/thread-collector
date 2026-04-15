---
source: blog
creator: sebastian-rohl
url: https://sebastianroehl.substack.com/p/building-an-indie-app-business-87
title: Building An Indie App Business #87
published_at: 2026-01-25
collected_at: 2026-04-15
categories: ["monetization", "ai-llm", "startup-philosophy"]
insight_extracted_at: 2026-04-15
---

## 핵심 주장 (≤5)
1. 앱 비즈니스의 매출과 다운로드는 성수기와 비수기를 반복하는 사이클을 가지므로, 하락 국면에서 패닉하지 말고 성수기에 기반을 다져야 한다.
2. 저자는 하락하는 숫자 자체보다 통제 가능한 영역인 제품 개선과 다음 피크 준비에 집중하는 태도가 중요하다고 본다.
3. FocusKit은 아직 관련 App Store 키워드 랭킹 없이도 HabitKit 내 교차 프로모션과 광고만으로 초기 매출 성장을 만들고 있다.
4. 새 사용자의 설정 부담을 줄이려면 커스텀 기능과 함께 바로 쓸 수 있는 템플릿 라이브러리를 제공하는 것이 효과적이다.
5. AI는 인디 개발자를 대체하지는 않지만, 올바른 지시와 검토를 전제로 하면 반복 구현을 크게 줄여 창의적 결정과 UX에 더 집중하게 해주는 강력한 도구다.

## 공개된 숫자·지표
- FocusKit MRR: Over $100 (기간: 이번 주 시점, 출처: "We reached a new milestone this week that I’m really proud of: Over $100 in Monthly Recurring Revenue (MRR) and over $1,000 in total revenue over the past 28 days!")
- FocusKit 총매출: over $1,000 (기간: past 28 days, 출처: "We reached a new milestone this week that I’m really proud of: Over $100 in Monthly Recurring Revenue (MRR) and over $1,000 in total revenue over the past 28 days!")
- FocusKit 출시 시점: just two months ago (기간: 글 작성 시점 기준, 출처: "For a new app that I launched just two months ago, this feels like real progress.")
- HabitKit 사이클 경험 기간: past 3 years (기간: past 3 years, 출처: "This is the normal behavior for HabitKit, and I’ve been experiencing this cycle for the past 3 years now.")
- 긴 휴식 규칙 예시: every second focus sessions / 5-minute (기간: 루틴 설정 예시, 출처: "For example, you could say “after every second focus sessions, give me a long break instead of the usual 5-minute one”.")

## 언급된 도구·서비스
- HabitKit: 설정 화면 배너를 통해 FocusKit을 교차 프로모션하는 기존 앱으로 사용됨
- FocusKit: 저자가 출시 두 달 된 신규 앱으로, 매출 성장과 1.2 업데이트 작업의 중심으로 언급됨
- App Store: FocusKit이 아직 관련 키워드 랭킹을 얻지 못한 유통 채널로 언급됨
- Reddit: FocusKit 성장을 만드는 paid ads 채널로 사용됨
- App Store Search ads: FocusKit 성장을 만드는 유료 광고 채널로 사용됨
- Cursor: 저자가 원하는 기능을 설명하고 코드를 작성하도록 지시하는 AI 개발 도구로 사용됨
- Claude: Cursor와 함께 코드 작성을 맡기고 결과를 검토·수정하는 AI 도구로 사용됨

## 언급된 다른 creator·앱
- HabitKit: FocusKit 성장의 교차 프로모션 소스로 반복 언급됨
- FocusKit: 이번 글의 매출 이정표와 제품 업데이트 사례의 중심 앱으로 반복 언급됨

## 복제 가능한 전술 (≤3)
1. 기존 앱의 설정 화면에 신규 앱 배너를 넣어 교차 프로모션 트래픽을 만든다.
   - 구체적 스텝: 이미 사용자 기반이 있는 앱의 설정 화면처럼 자주 스크롤되는 지점을 고른다. 신규 앱을 소개하는 작은 배너를 배치한다. 클릭 이후 신규 앱 상세 페이지나 설치 흐름으로 연결한다. 유입과 매출 기여를 보고 효과를 확인한다.
   - 예상 리소스: 기존 앱 1개, 배너 UI 작업, 신규 앱 링크 추적 수단
   - 예상 효과: App Store 유기 랭킹이 없어도 초기 성장의 대부분을 기존 제품 사용자 기반에서 만들 수 있다.
2. 고급 커스터마이징 기능에는 사전 정의 템플릿 라이브러리를 함께 제공한다.
   - 구체적 스텝: 사용자가 직접 세션 수, 집중 시간, 휴식 시간을 전부 설계해야 하는 기능을 찾는다. 대표 사용 시나리오별 기본 루틴 템플릿을 만든다. 새 사용자가 템플릿을 바로 선택해 시작하게 하고, 이후 세부값만 수정하게 한다.
   - 예상 리소스: 제품 기획 시간, 템플릿 설계, 설정 UI
   - 예상 효과: 새 사용자가 처음부터 모든 설정을 고민하지 않아도 되어 더 빨리 핵심 가치를 경험할 수 있다.
3. 홈 화면 퀵 액션처럼 가장 짧은 경로에 피드백 제출 진입점을 만든다.
   - 구체적 스텝: 앱 삭제 직전이나 불편을 느낄 때 바로 보일 수 있는 OS 수준 단축 진입점을 추가한다. 사용자가 길게 누르기만 해도 의견 제출 또는 이슈 제보로 이동하게 만든다. 유입된 피드백을 제품 개선 루프에 바로 반영한다.
   - 예상 리소스: 플랫폼 퀵 액션 구현, 피드백 수집 채널
   - 예상 효과: 피드백 제출 장벽이 낮아져 더 많은 의견을 받고, 앱을 삭제하려는 사용자의 이탈 전에 문제를 포착할 수 있다.

## 원문 요약 (≤5문장)
저자는 HabitKit의 매출이 1월 첫 주 피크 이후 다시 내려가고 있지만, 지난 3년간 반복된 정상적인 계절성 사이클로 받아들이고 있다고 설명한다. 대신 하락 자체보다 앱을 더 좋게 만들고 다음 피크를 준비하는 데 집중한다고 말한다. 새 앱 FocusKit은 출시 두 달 만에 MRR 100달러 이상, 최근 28일 총매출 1,000달러 이상을 달성했고, 이 성장은 주로 HabitKit 설정 화면의 교차 프로모션과 Reddit 및 App Store Search ads에서 왔다. 제품 측면에서는 커스텀 루틴, 템플릿 라이브러리, 홈 화면 피드백 퀵 액션, Timeline 탭 개편을 진행했다. 마지막으로 AI에 대해서는 Cursor와 Claude에 구현을 맡기고 자신은 지시·검토·수정에 집중하는 방식이 인디 개발자의 작업 방식을 크게 바꾸고 있다고 평가한다.

## 본문 포인트별 발췌
> The key is to build a solid foundation during the good times so you’re prepared for the slower periods.
> Instead of stressing about the decline, I focus on what I can control: making my apps better and preparing for the next peak.
> We reached a new milestone this week that I’m really proud of: Over $100 in Monthly Recurring Revenue (MRR) and over $1,000 in total revenue over the past 28 days!
> Most of it is fueled by cross-promotion through the settings screen of HabitKit.
> Instead, I’m mostly directing Cursor and Claude to write the code for me.
