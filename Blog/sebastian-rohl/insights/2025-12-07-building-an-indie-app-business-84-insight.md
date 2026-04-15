---
source: blog
creator: sebastian-rohl
url: https://sebastianroehl.substack.com/p/building-an-indie-app-business-84
title: Building An Indie App Business #84
published_at: 2025-12-07
collected_at: 2026-04-15
categories: ["startup-philosophy", "case-study", "monetization"]
insight_extracted_at: 2026-04-15
---

## 핵심 주장 (≤5)
1. 출시 전부터 첫 업데이트를 준비해두면 런치 직후 버그와 피드백에 더 빠르게 대응할 수 있다.
2. 초기 단계에서는 사용자가 개발자가 적극적으로 앱을 개선하고 피드백을 반영하고 있다는 신호를 주는 것이 중요하다.
3. 베타 테스트에서 반복적으로 나온 요청을 반영한 기본 카테고리 기능은 사용자가 매 세션마다 같은 입력을 반복하지 않게 해준다.
4. 빌드 인 퍼블릭 방식으로 검증된 매출 지표를 공개하면 제품 운영의 투명성을 높일 수 있다.
5. 초기 유료 광고는 당장 수익성보다 제품에 대한 초기 노출과 전환 데이터 확보를 목표로 운영할 수 있다.

## 공개된 숫자·지표
- FocusKit 1.0.1 출시 시점: 런치 2일 후 월요일 (기간: 출시 직후, 출처: "I released FocusKit 1.0.1 on Monday, just two days after launch.")
- 총매출: $446 (기간: 출시 첫 주 기준, 출처: "Total Revenue: $446")
- MRR: $18 (기간: 출시 첫 주 기준, 출처: "MRR: $18")
- 다운로드: 794 (기간: 출시 첫 주 기준, 출처: "Downloads: 794")
- 평점/리뷰: 26개, 4.8점 (기간: 출시 첫 주 기준, 출처: "Ratings/Reviews: 26 - 4.8 stars")
- Reddit 광고비: 50€ (기간: 현재까지, 출처: "So far I’ve spent 50€, got around 16k impressions and 92 clicks.")
- Reddit 광고 노출수: 약 16k (기간: 현재까지, 출처: "So far I’ve spent 50€, got around 16k impressions and 92 clicks.")
- Reddit 광고 클릭수: 92 (기간: 현재까지, 출처: "So far I’ve spent 50€, got around 16k impressions and 92 clicks.")
- Reddit 광고 일일 예산: 10€ (기간: 캠페인 운영 기준, 출처: "I set a daily budget of 10€, so it’s not going to break the bank either way.")
- Apple Search Ads 광고비: 75€ (기간: 현재까지, 출처: "I’ve spent 75€ so far and it generated 550 impressions, 60 taps and 35 installs.")
- Apple Search Ads 노출수: 550 (기간: 현재까지, 출처: "I’ve spent 75€ so far and it generated 550 impressions, 60 taps and 35 installs.")
- Apple Search Ads 탭수: 60 (기간: 현재까지, 출처: "I’ve spent 75€ so far and it generated 550 impressions, 60 taps and 35 installs.")
- Apple Search Ads 설치수: 35 (기간: 현재까지, 출처: "I’ve spent 75€ so far and it generated 550 impressions, 60 taps and 35 installs.")
- Apple Search Ads 설치당 비용: 약 2.14€ (기간: 현재까지, 출처: "That’s a cost per install of around 2.14€, which I think is pretty reasonable for a first experiment.")
- 탭 대비 설치 전환율: 거의 60% (기간: 현재까지, 출처: "The conversion from tap to install is also really good at almost 60%")

## 언급된 도구·서비스
- Product Hunt: FocusKit를 당일 피처드로 올려 업보트를 요청하는 런치 채널로 사용
- RevenueCat: 검증된 매출 통계를 `tryfocuskit.com/open`에 임베드해 공개하는 데 사용
- Reddit Ads: 생산성 관련 서브레딧을 타깃으로 초기 유입 실험에 사용
- App Store Connect: 특정 광고 캠페인별 설치 어트리뷰션 추적이 어렵다고 언급
- Apple Search Ads: "Pomodoro Timer" 키워드 중심으로 더 타깃된 유료 광고 실험에 사용

## 언급된 다른 creator·앱
- FocusKit: 글의 중심 앱이자 출시 후 첫 주 운영, 업데이트, 광고 실험의 대상
- HabitKit: 이전 런치 경험에서 "버그에 항상 대비해야 한다"는 교훈을 얻은 비교 사례

## 복제 가능한 전술 (≤3)
1. 런치 직전부터 첫 패치 버전을 준비해 초기 피드백 대응 속도를 높인다.
   - 구체적 스텝: 출시 며칠 전부터 첫 업데이트 브랜치를 만들고, 런치 직후 들어온 버그·UX 피드백을 바로 반영해 1차 패치를 빠르게 배포한다.
   - 예상 리소스: 출시 직전 개발 시간, 앱 업데이트 배포 권한, 사용자 피드백 수집 채널
   - 예상 효과: 초기 사용자에게 앱을 적극적으로 개선하고 있다는 신호를 주고, 버그 대응 과정에서 혼선을 줄일 수 있다.
2. 베타 테스트에서 반복적으로 나온 요청을 우선순위 높은 기능으로 반영한다.
   - 구체적 스텝: 베타 피드백 중 반복 언급된 불편을 추려 가장 자주 등장한 항목부터 기능화하고, 사용 흐름 중 가장 자주 반복되는 행동을 줄이는 방식으로 구현한다.
   - 예상 리소스: 베타 사용자 피드백 기록, 우선순위 정리 시간, 제품 개발 시간
   - 예상 효과: 사용자가 매번 같은 조작을 반복하지 않게 되어 사용 편의성이 개선되고, 초기 만족도를 높일 수 있다.
3. 초기 유료 광고는 수익성보다 채널별 전환 감각을 얻는 실험으로 운영한다.
   - 구체적 스텝: 타깃 커뮤니티 기반 광고와 키워드 기반 광고를 각각 소규모 예산으로 집행하고, 노출수·클릭/탭·설치·설치당 비용을 비교하면서 일정 기간 추이를 본다.
   - 예상 리소스: Reddit Ads 또는 Apple Search Ads 계정, 소규모 광고 예산, 스토어 성과 확인 도구
   - 예상 효과: 어떤 채널이 더 타깃팅이 잘 되고 스토어 페이지가 전환을 받쳐주는지 빠르게 파악할 수 있다.

## 원문 요약 (≤5문장)
저자는 FocusKit 출시 1주차에 빠른 업데이트와 버그 수정, 기능 추가를 병행하며 초기 사용자 피드백에 대응했다. 첫 주 성과로 총매출, MRR, 다운로드, 평점/리뷰 수를 공개하며 전반적으로 만족스럽다고 평가했다. 특히 RevenueCat 통계를 공개 페이지에 임베드해 빌드 인 퍼블릭 방식의 투명성을 강조했다. 유료 광고는 Reddit Ads와 Apple Search Ads 두 채널에서 테스트했으며, Reddit은 노출 확보용, Apple Search Ads는 더 정밀한 전환 실험으로 다뤘다. 다음 주 우선순위는 FocusKit 1.1.0 심사 통과와 외부 리뷰어 아웃리치다.

## 본문 포인트별 발췌
> "Here’s something I learned from launching HabitKit: you should always be prepared for bugs."
> "I released FocusKit 1.0.1 on Monday, just two days after launch."
> "I wanted to show early users that I’m actively working on the app and listening to their feedback."
> "I’m a big fan of building in public, so everything is transparent there."
> "I’m not expecting the Reddit campaign to be profitable."
