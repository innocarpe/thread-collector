# sebastian-rohl 반복 패턴 분석

## 반복 사용 전술
- 작은 업데이트의 고빈도 배포: 대규모 리빌드보다 빠른 패치와 점진 개선을 선호한다 — 최소 9번 이상 등장, 출시 직후 `1.0.1`, `1.1.1`, `1.3`, `1.15.0`처럼 잘게 쪼개 배포하며 버그와 UX 마찰을 바로 줄인다.
- 사용자 피드백의 즉시 반영: 베타와 지원 메일, 리뷰를 로드맵보다 우선한다 — 최소 8번 등장, 약 30명의 베타 테스터 피드백을 받아 원래 `v1.1` 예정 기능도 `v1`에 앞당겨 넣고, 반복 요청 기능은 위젯·루틴·기본 카테고리처럼 곧바로 제품에 편입한다.
- 앱스토어 중심 최적화: 제품 개발과 동시에 ASO, 리뷰, 스크린샷, 아이콘을 같이 다듬는다 — 최소 8번 등장, 키워드 리서치, 전문 디자이너 아이콘, 리뷰 요청, 스크린샷 A/B 테스트, Search Ads를 한 묶음으로 운영한다.
- 기존 자산을 신작 성장 엔진으로 활용: 새 앱을 완전히 새로 띄우기보다 기존 앱과 오디언스로 부스팅한다 — 최소 5번 등장, HabitKit 설정 화면 배너, 소셜 크로스포스팅, 지인 네트워크, 뉴스레터 독자를 FocusKit 초기 유입으로 연결한다.

## 일관되게 사용하는 도구
- RevenueCat: 매출 추적과 결제 인프라 — 여러 글에서 대시보드 수치를 기준으로 의사결정하고, 공개 페이지에 통계를 임베드해 빌드 인 퍼블릭 신뢰를 만든다.
- App Store Connect / App Store: 배포, 심사 대응, 리뷰, ASO 실험의 중심 도구 — 출시 일정 관리부터 심사 리젝 대응, 가격 테스트, 리뷰 축적까지 반복적으로 사용한다.
- SwiftUI / Apple 생태계: 신규 제품의 핵심 구현 스택 — FocusKit, 위젯, Apple Watch, AlarmKit, Live Activities처럼 네이티브 경험을 차별화 포인트로 삼는다.
- Cursor + Claude/Codex/Opus: AI 개발 워크플로 — 계획은 큰 모델, 구현은 코딩 모델, 최종 판단은 본인이 맡는 방식으로 성능 개선과 신규 기능 개발 속도를 끌어올린다.

## 반복되는 수익화 패턴
- 시즌성 구독 매출: HabitKit은 연말·연초 자기계발 수요를 강하게 탄다 — `2025-12-30` 기준 총매출 `$602,000`, MRR `$28,000`, `2026-01-18`에는 지난 28일 매출이 `$100K+`를 넘겼다.
- 랭킹 기반 매출 증폭: 핵심 키워드 상위권이 장기 매출 안정화로 이어진다 — 미국 앱스토어 `habit tracker` 5위권, 이후 2위, 오스트리아 1위를 언급하며 월매출이 `above $40k`로 안정화됐다고 회고한다.
- 신작은 저가 진입 후 검증: FocusKit은 출시 첫날 `$111` 매출, 첫 주 `$446`, 약 4개월 내 MRR `$120` 수준까지 올라오며 교차 프로모션과 광고로 초기 수익성을 검증한다.

## 핵심 믿음·철학
- 그는 통제 가능한 것에 집착한다. “Instead of stressing about the decline, I focus on what I can control: making my apps better and preparing for the next peak.”
- 그는 작은 실행의 누적을 더 신뢰한다. “Small and consistent updates are so much better than huge rebuilds that never happen because you lose motivation in the middle of the project.”
- 그는 운영 현실을 낭만화하지 않는다. “But the boring work is often the most important work.”
- 그는 플랫폼 의존 리스크를 명확히 인식한다. “The moral of the story? Platform risk is real. Never forget that you’re building on someone else’s land.”

## 성장 궤적
2025년 11월의 sebastian-rohl은 FocusKit 출시 준비에 몰입한 제품 제작자였다. 이 시기 핵심은 마감 설정, 베타 테스트, 앱스토어 심사 통과, 첫날 매출 확인 같은 런치 오퍼레이션이었다. 12월에는 SwiftUI 전환을 공개적으로 정당화하며 “왜 iOS 네이티브인가”를 사업 전략과 연결했고, 연말 회고에서는 HabitKit의 대형 성공과 플랫폼 리스크를 함께 해석했다. 2026년 1월부터는 FocusKit을 별도 수익원으로 키우는 단계로 넘어가며 루틴, 템플릿, 위젯, Watch 통합 같은 리텐션 기능에 집중했다. 2월과 3월에는 단순 앱 개발자에서 AI를 오케스트레이션하는 운영자로 역할이 진화했다. AI로 리팩터링, 프로토타이핑, 이메일 초안, 데일리 브리핑까지 자동화 범위를 넓혔지만, 동시에 저널링, 집중 시간, 소셜 미디어 차단 같은 인간적 운영 습관을 더 중요한 기반으로 본다는 점이 일관되게 남아 있다.
