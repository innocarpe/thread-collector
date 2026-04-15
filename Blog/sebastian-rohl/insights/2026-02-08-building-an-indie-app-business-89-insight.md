---
source: blog
creator: sebastian-rohl
url: https://sebastianroehl.substack.com/p/building-an-indie-app-business-89
title: Building An Indie App Business #89
published_at: 2026-02-08
collected_at: 2026-04-15
categories: ["ai-llm", "dev-tools", "productivity"]
insight_extracted_at: 2026-04-15
---

## 핵심 주장 (≤5)
1. 2월에는 1월 유입 구독자의 갱신 매출 급증과 이탈 급증이 동시에 발생해 MRR이 정체되거나 감소할 수 있다.
2. 이 MRR 정체 구간은 매년 반복되는 계절적 사이클이며, 글쓴이는 3월이나 4월에 다시 성장세가 돌아온다고 본다.
3. FocusKit은 아직 작은 규모지만 출시 1년이 되지 않은 앱이 최근 28일간 약 750달러를 벌고 있다는 점 자체를 의미 있는 진전으로 본다.
4. FocusKit의 커스텀 루틴 업데이트는 사용자가 루틴을 직접 구성·관리할 수 있게 해 제품의 유연성과 커스터마이징 수준을 크게 높였다.
5. 자동 다음 세션 진행과 일일 루틴 리셋 같은 사용성 개선은 눈에 띄는 기능은 아니어도 일상 사용 경험과 리텐션에 직접적인 영향을 준다.

## 공개된 숫자·지표
- FocusKit MRR: $113 (기간: 현재 시점, 출처: "Right now, we are at $113 MRR and we made $748 in total revenue for the past 28 days.")
- FocusKit 총매출: $748 (기간: 지난 28일, 출처: "Right now, we are at $113 MRR and we made $748 in total revenue for the past 28 days.")
- 지원 메일 처리 시간: 30분 (기간: 평일 업무 시작 시점 기준, 출처: "the first 30 minutes of my work day are usually eaten up by answering support emails.")
- 자동화 목표 처리 시간: 5분 (기간: 아침 이메일 처리 세션 목표, 출처: "That could turn my 30-minute email session into a 5-minute one.")

## 언급된 도구·서비스
- HabitKit: 1월 초 신규 구독자 유입과 2월 갱신·이탈 사이클을 설명하는 기존 주력 앱
- FocusKit: MRR·최근 28일 매출을 공개하고, 커스텀 루틴 및 UX 개선 업데이트를 진행 중인 포모도로/집중 타이머 앱
- OpenClaw: 개발 속도 향상과 지원 메일 자동화 초안 작성에 활용하려는 에이전트형 AI 도구
- X: OpenClaw 관련 업데이트를 공유하는 채널로 언급
- Gmail: 현재 지원 메일이 연결된 개인 메일 주소로, 향후 별도 지원 메일로 분리할 대상
- Sonnet 5: 향후 OpenClaw 워크플로 확장에 기대를 거는 모델
- App Store: 새 지원 메일 주소로 설명 문구를 업데이트해야 하는 노출 지점

## 언급된 다른 creator·앱
- HabitKit: 1월 시즌성과 2월 MRR 정체를 설명하는 기준점으로 언급된 앱
- FocusKit: 수익화 초기 단계의 성장 사례와 제품 업데이트의 중심이 되는 앱
- OpenClaw: 개인 앱 비즈니스용 AI 비서로 육성 중인 프로젝트
- Eric: OpenClaw 봇의 이름으로, 지원 메일 답변 초안을 작성하게 하려는 대상

## 복제 가능한 전술 (≤3)
1. 계절성 구독 비즈니스에서는 1월 유입 코호트의 2월 갱신률과 이탈률을 함께 보고 MRR 정체를 정상 사이클로 관리한다.
   - 구체적 스텝: 1월 신규 구독자 증가 이후 2월에 갱신 매출과 해지 증가를 동시에 추적한다; 일별 MRR만 보지 말고 월별 사이클로 해석한다; 3월~4월 반등 여부를 과거 패턴과 비교해 판단한다.
   - 예상 리소스: 구독 분석 데이터, 월별 MRR 추적 시간
   - 예상 효과: 단기 정체 구간에서 과잉 반응을 줄이고 반복되는 성장 사이클을 더 침착하게 운영할 수 있다.
2. 사용자마다 선호 흐름이 갈리는 기능은 설정 토글로 열어두고, 반복적으로 제기되는 불만은 기본값까지 재설계한다.
   - 구체적 스텝: 반복 접수되는 사용성 불만을 수집한다; 서로 다른 작업 방식이 존재하면 설정에서 선택 가능하게 만든다; 다수 사용자의 실제 사용 흐름에 맞는 옵션을 기본값으로 지정한다.
   - 예상 리소스: 사용자 피드백, 설정 UI 수정, 테스트 시간
   - 예상 효과: 일상 사용 경험이 개선되고, 글쓴이 표현대로 "happy users stick around longer"에 가까운 리텐션 개선을 기대할 수 있다.
3. 지원 메일 자동화는 `전용 지원 메일 주소 구축 -> AI가 초안만 작성 -> 템플릿·제품 위키 학습`의 3단계로 도입한다.
   - 구체적 스텝: 개인 메일 대신 전용 지원 메일 주소를 만들고 앱 설명·인앱 지원 버튼·웹사이트 푸터 등 연결 지점을 모두 교체한다; AI에게 발송 권한 없이 초안 작성만 맡긴다; 기존 답변 템플릿과 앱 화면·기능·자주 묻는 질문을 문서화해 컨텍스트로 제공한다.
   - 예상 리소스: 메일 계정 설정, 문서 정리 시간, OpenClaw 같은 AI 도구
   - 예상 효과: 글쓴이의 기대 기준으로 아침 지원 메일 처리 시간을 30분에서 5분 수준으로 줄일 가능성이 있다.

## 원문 요약 (≤5문장)
글쓴이는 2월이 HabitKit 비즈니스에서 갱신과 이탈이 동시에 커지는 시기라 MRR이 정체되거나 감소하는 달이라고 설명한다. FocusKit은 현재 $113 MRR, 최근 28일 매출 $748로 아직 작지만 출시 1년도 안 된 앱으로서는 의미 있는 진전으로 평가한다. 이번 주에는 FocusKit에 커스텀 루틴 기능을 출시했고, 다음 업데이트로 자동 다음 세션 진행과 일일 루틴 리셋을 추가할 예정이다. 또한 OpenClaw를 활용해 지원 메일 답변 초안을 자동 생성하는 워크플로를 설계 중이며, 이를 위해 전용 지원 메일 주소와 제품 위키 구축이 필요하다고 본다. 궁극적으로는 반복적인 지원 업무를 줄여 더 생산적인 시간으로 전환하려는 의도가 핵심이다.

## 본문 포인트별 발췌
> The result? Stagnating (or even declining) MRR.
> But honestly, this is totally fine for me. It’s happening every single year and by now I know that growing MRR will be back in March or April.
> Right now, we are at $113 MRR and we made $748 in total revenue for the past 28 days.
> And happy users stick around longer, which is great for retention and ultimately for the business.
> That could turn my 30-minute email session into a 5-minute one.
