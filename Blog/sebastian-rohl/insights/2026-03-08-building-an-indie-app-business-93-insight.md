---
source: blog
creator: sebastian-rohl
url: https://sebastianroehl.substack.com/p/building-an-indie-app-business-93
title: Building An Indie App Business #93
published_at: 2026-03-08
collected_at: 2026-04-15
categories: ["case-study", "monetization", "web-app"]
insight_extracted_at: 2026-04-15
---

## 핵심 주장 (≤5)
1. FocusKit은 아직 초기 단계지만 MRR과 최근 28일 매출이 발생하며 성장 방향이 긍정적이다.
2. FocusKit의 Apple Watch 연동은 참여도와 리텐션 개선에 도움이 될 것으로 기대된다.
3. 비밀 macOS 프로젝트는 MVP 기능 완성 단계에 도달했고, 다음 단계는 외부 사용자 피드백 확보다.
4. HabitKit의 성능 문제는 AI를 활용한 약 30분짜리 리팩터링으로 대략 10배 개선됐다.
5. 초기부터 잠재 비용을 과도하게 최적화하기보다, 실제로 발생한 문제가 생겼을 때 대응하는 편이 낫다.

## 공개된 숫자·지표
- FocusKit MRR: $121 (기간: 게시 시점 기준 현재, 출처: "MRR is at $121, and revenue for the last 28 days is at $637.")
- FocusKit 최근 28일 매출: $637 (기간: last 28 days, 출처: "MRR is at $121, and revenue for the last 28 days is at $637.")
- HabitKit 성능 개선폭: roughly 10x (기간: 이번 주 리팩터링 이후, 출처: "It refactored the code in about 30 minutes and the performance of the app improved by roughly 10x.")
- HabitKit 리팩터링 소요 시간: about 30 minutes (기간: 이번 주, 출처: "It refactored the code in about 30 minutes and the performance of the app improved by roughly 10x.")
- HabitKit 성능 문제를 붙잡은 기간: past 2 years (기간: 최근 2년, 출처: "I’ve been trying to improve the performance of HabitKit for the past 2 years.")
- 협업자 수: 2명 (기간: 이번 주 빌드 공유 시점, 출처: "After that, I submitted another improved build to my two collaborators.")
- Firebase 월 청구액: 0.21€ (기간: monthly bill, 출처: "I present to you: the monthly bill. 0.21€.")

## 언급된 도구·서비스
- FocusKit: Watch 출시와 Apple Watch 연동을 진행한 앱
- HabitKit: 유지보수, 성능 업데이트, 의존성 업데이트를 진행한 앱
- Apple Watch: FocusKit 1.3에서 세션과 워크플로우를 손목에서 관리할 수 있게 하는 연동 대상
- Flutter: HabitKit에서 업그레이드한 프레임워크
- AI: HabitKit 성능 문제 해결을 위한 리팩터링에 사용한 접근
- Opus 4.6: 성능 개선 작업의 계획 수립에 사용한 도구
- Codex 5.3: 성능 개선 작업의 구현에 사용한 도구
- Firebase: 월 청구액을 확인한 백엔드 서비스
- X: 비밀 macOS 프로젝트의 타깃 유저와 맞는 오디언스를 보유한 채널
- LinkedIn: 비밀 macOS 프로젝트의 타깃 유저와 맞는 오디언스를 보유한 채널

## 언급된 다른 creator·앱
- FocusKit: 작성자가 운영하며 Watch 릴리스를 진행한 앱
- HabitKit: 작성자가 다시 적극 개발 모드로 전환한 앱
- 비밀 macOS 프로젝트: MVP 기능 완성 후 첫 사용자 피드백을 준비 중인 프로젝트

## 복제 가능한 전술 (≤3)
1. 장기간 해결되지 않는 성능 문제는 병목을 먼저 정의한 뒤 AI에게 다중 파일 리팩터링을 맡겨 돌파한다.
   - 구체적 스텝: 성능 병목 구간을 개발자가 먼저 파악한다. 계획 수립에는 Opus 4.6 같은 도구를 사용한다. 구현은 Codex 5.3 같은 코드 생성 도구로 여러 파일에 걸친 리팩터링을 수행한다. 변경 후 성능 개선과 부작용 여부를 확인한다.
   - 예상 리소스: AI 도구 2종, 코드베이스 접근 권한, 약 30분 이상의 검토 시간
   - 예상 효과: 수년간 막혀 있던 성능 문제를 짧은 시간 안에 해결하고, 앱 성능을 대략 10배 개선할 수 있다.
2. 새 플랫폼 연동 기능을 출시한 직후에는 초기 버그 리포트를 빠르게 수집하고 다음 주 최우선으로 수정한다.
   - 구체적 스텝: 주요 기능 릴리스를 배포한다. 초기 사용자 반응과 버그 리포트를 즉시 수집한다. 다음 주 우선순위를 버그 수정에 둬 이슈가 쌓이기 전에 처리한다.
   - 예상 리소스: 릴리스 가능한 앱, 사용자 피드백 채널, 다음 주 개발 시간
   - 예상 효과: 긍정적 초기 반응을 유지하면서 출시 직후 품질 문제를 빠르게 안정화할 수 있다.
3. 새로운 B2B/B2D 성격의 제품은 MVP 기능 완성 후 기존 오디언스 채널과 맞는 타깃 그룹에게 첫 외부 피드백을 받는다.
   - 구체적 스텝: 내부 테스트에서 나온 UX와 디자인 문제를 먼저 수정한다. 개선 빌드를 협업자에게 다시 공유한다. 이후 X와 LinkedIn 같은 기존 오디언스 채널과 맞는 타깃 그룹에게 첫 사용자 피드백을 요청한다.
   - 예상 리소스: 내부 테스트 환경, 협업자 2명, X와 LinkedIn 오디언스
   - 예상 효과: 정식 공개 전에 타깃 적합성이 높은 사용자 반응을 빠르게 확인할 수 있다.

## 원문 요약 (≤5문장)
이번 주 작성자는 FocusKit Watch 출시, HabitKit 유지보수 및 성능 개선, 비밀 macOS 프로젝트의 MVP 기능 완성까지 여러 제품에서 동시에 진전을 만들었다. FocusKit은 MRR $121, 최근 28일 매출 $637을 기록했고, Apple Watch 연동이 참여도와 리텐션 개선에 기여하길 기대하고 있다. HabitKit은 AI를 활용한 약 30분짜리 리팩터링으로 성능이 대략 10배 개선됐으며, 작성자는 계획에는 Opus 4.6, 구현에는 Codex 5.3을 사용했다고 밝혔다. 인디 개발 운영 측면에서는 독일 세무 마감 대응처럼 지루한 운영 업무도 피할 수 없다고 강조했다. 또한 실제로는 월 Firebase 비용이 0.21€에 불과했다며, 너무 이른 최적화에 시간을 쓰지 말라고 조언했다.

## 본문 포인트별 발췌
> MRR is at $121, and revenue for the last 28 days is at $637.
> The Watch integration should help with engagement and retention, and I’m hoping the next few updates will push the numbers even higher.
> The next step now is getting first user feedback, and I will share more details about this soon.
> It refactored the code in about 30 minutes and the performance of the app improved by roughly 10x.
> I present to you: the monthly bill. 0.21€.
