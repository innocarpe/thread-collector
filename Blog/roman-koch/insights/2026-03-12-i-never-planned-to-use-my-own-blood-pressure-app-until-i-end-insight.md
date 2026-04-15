---
source: blog
creator: roman-koch
url: https://medium.com/@romankoch/i-never-planned-to-use-my-own-blood-pressure-app-until-i-ended-up-in-the-emergency-room-81556fd5d739?source=rss-4f0be52319a3
title: 2026-03-12-i-never-planned-to-use-my-own-blood-pressure-app-until-i-end
published_at: 2026-03-12
collected_at: 2026-04-15
categories: ["case-study", "product-strategy"]
insight_extracted_at: 2026-04-15
---

## 핵심 주장 (≤5)
1. 앱은 혈압을 측정하는 도구가 아니라, 실제 측정값을 빠르게 기록하고 이력과 변화를 확인하며 필요 시 의사에게 공유할 수 있게 해주는 수기 기록 도구여야 한다.
2. 실제 긴급 상황에서 사용해 보니, 단순한 UI와 빠른 입력 흐름 같은 기본 설계가 제품의 실질적 가치로 이어졌다.
3. 스트레스 상황의 사용성은 평상시 테스트와 다르게 드러나며, 탭 수, 가독성, 핵심 정보 접근성 같은 작은 디테일이 훨씬 중요해진다.
4. 창업자 자신이 실제 사용자가 되는 순간, 제품의 유용성뿐 아니라 개선 포인트도 더 선명하게 보인다.

## 공개된 숫자·지표
- 단어 수: 812 (기간: 원문 기준, 출처: `extras.word_count: 812`)

## 언급된 도구·서비스
- Beat It: 혈압 측정 후 수동으로 수축기·이완기 값을 입력하고, 히스토리·차트·추세 확인 및 의사용 데이터 내보내기에 쓰인 앱
- App Store: Beat It 앱이 출시된 배포 채널
- iOS Blood Pressure - Beat It: 글 말미에 연결된 앱 링크
- mybptracker.app: 앱 소개 웹사이트
- romankoch.online: 작성자의 개인 페이지

## 언급된 다른 creator·앱
- 없음

## 복제 가능한 전술 (≤3)
1. 의료 기록 앱은 측정 기능을 억지로 넣기보다 측정 후 기록과 공유에 집중한 단순 수기 입력 경험으로 설계한다.
   - 구체적 스텝: 혈압계 같은 별도 측정 기기로 값을 잰 뒤 바로 입력할 수 있게 수축기·이완기 입력 화면을 최소 단계로 설계하고, 저장 후 히스토리·추세·내보내기 화면으로 연결한다.
   - 예상 리소스: 앱 UI 설계 및 기록/히스토리/내보내기 기능 구현, 스마트폰 앱
   - 예상 효과: 사용자가 값을 빠르게 저장하고 시간에 따른 변화를 확인하며 필요 시 의사에게 기록을 보여주기 쉬워진다.
2. 제품 테스트는 평상시 UX 점검에 그치지 말고, 스트레스 상황에서도 빠르게 쓸 수 있는지 기준으로 다시 검토한다.
   - 구체적 스텝: 핵심 입력 플로우에서 탭 수, 기록 속도, 히스토리 가독성, 중요한 정보의 즉시 노출 여부를 점검하고 불필요한 단계나 요소를 제거한다.
   - 예상 리소스: 실제 사용 시나리오 기반 UX 리뷰 시간, 앱 프로토타입 또는 운영 중 제품
   - 예상 효과: 사용자가 아프거나 불안한 상황에서도 기록을 남기고 필요한 정보를 바로 찾기 쉬워진다.
3. 의사 상담용 맥락을 만들 수 있도록 단일 수치가 아니라 시간대별 기록 흐름을 남기게 한다.
   - 구체적 스텝: 측정할 때마다 값을 연속 기록하도록 유도하고, 히스토리 화면과 공유 가능한 내보내기 기능으로 하루 동안의 변화 흐름을 보여준다.
   - 예상 리소스: 타임라인/히스토리 UI, 데이터 저장, 내보내기 기능
   - 예상 효과: 사용자가 기억에 의존하지 않고 하루 동안의 progression을 의료진에게 명확히 전달할 수 있다.

## 원문 요약 (≤5문장)
작성자는 원래 어머니의 혈압 기록 문제를 해결하기 위해 Beat It을 만들었고, 자신이 직접 쓸 제품이라고는 생각하지 않았다. 앱은 혈압을 측정하는 것이 아니라 측정 후 값을 빠르게 기록하고, 히스토리와 추세를 보고, 필요 시 의사에게 공유할 수 있게 설계됐다. 하지만 작성자가 몸이 좋지 않아 하루 동안 혈압을 반복 측정하고 기록한 뒤 응급실에 가게 되면서, 이 앱은 개인적으로도 실제로 유용한 도구가 됐다. 그 경험을 통해 단순한 입력 흐름, 적은 탭 수, 빠른 정보 접근성 같은 요소가 스트레스 상황에서 특히 중요하다는 점을 확인했다. 그는 이 사건을 계기로 자신이 만든 앱을 개발자 관점이 아니라 실제 사용자 관점에서 다시 보게 됐다고 말한다.

## 본문 포인트별 발췌
> "Why shouldn’t it be the easiest place to track blood pressure?"
> "It became useful to me personally."
> "I had a timeline. I had the progression. I had something clear. That helped a lot."
> "Those things always matter in product design. But they matter even more when the user is not calm, not focused, and just wants to record something important as fast as possible."
> "It does not try to replace the monitor. It just makes tracking easier, more organized, and easier to share."
