# TemperStone 앱 포트폴리오 — 치트시트
*의심이 날 때 이 파일부터 다시 읽어라.*

생성일: 2026-04-15

---

## 핵심 원칙 7가지

1. **iOS 단일 플랫폼으로 한 사이클을 먼저 돌린다** — iOS ARPU가 Android 대비 3~5배. 직장인 1인이 양 플랫폼 동시 운영하면 빌드·QA·광고 소재가 각각 2~3배로 늘어나 둘 다 어중간해진다. (dalgom_bami)
2. **경쟁 앱 분석은 TikTok + Meta Ad Library가 답지다** — Sensor Tower 20~100위에서 소형 팀 앱 찾고, TikTok 검색으로 사용자 획득 패턴, Meta Ad Library로 광고 소재 패턴을 파악한다. 아이디어 선정에 최소 1주일을 쓴다. (dalgom_bami)
3. **구독 모델 + Paid UA는 마케팅을 외주화하는 방법이다** — 인플루언서 역량이 없어도 Meta Ads + Apple Search Ads 월 30~50만원으로 트래픽을 산다. AdMob 대량 포트폴리오는 트래픽이 먼저 필요해 순서가 다르다. (dalgom_bami, sebastian-rohl)
4. **하루 $1 기준으로 빠르게 판단한다** — 대박 1개가 아니라 앱당 하루 $1이 판단 단위다. 50~60개 시점에 하루 $100이 목표다. (programmingzombie)
5. **출시가 학습이다** — 검증 없이 몇 달을 개발하면 zero traction이 나온다. 1시간 미만 출시도 장기 수익 자산이 된다. 작게 내고 계속 수정한다. (roman-koch, programmingzombie)
6. **인접 확장으로 기존 오디언스를 재사용한다** — 두 번째 앱부터는 첫 앱 설정 화면 배너로 크로스프로모션. AdMob House ads로 포트폴리오 내 트래픽 순환. (sebastian-rohl, hussein-el-feky)
7. **공개하며 만들면 수요가 먼저 쌓인다** — 완성 후 홍보가 아니라 제작 중 공개. 익명 핸들로 스텔스 기간(~2026-06-30)에도 가능. (adam-wathan, sebastian-rohl, weyoume)

---

## Day 0 체크리스트 (iOS 구독 트랙 기준)

- [ ] 1. Sensor Tower — 관심 카테고리 1~2개 → 매출 20~100위 소형 팀 앱 5~10개 추리기 (dalgom_bami)
- [ ] 2. TikTok 검색 + Meta Ad Library — 경쟁 앱 광고 소재·획득 패턴 분석 (dalgom_bami)
- [ ] 3. 첫 앱 컨셉 확정: 10배 가치 차별화 + ASO 인기 20 초과, 난이도 70 미만, 월매출 $5,000 초과 (roman-koch 필터 병용)
- [ ] 4. Apple Developer Program 가입 ($99/년, 개인 계정)
- [ ] 5. Apple Small Business Program 즉시 신청 (매출 0원이어도 가능. 소급 없음. 30%→15%)
- [ ] 6. App Store Connect Agreements·Tax·Banking 완료 (출시 전 필수)
- [ ] 7. RevenueCat 계정 준비 + StoreKit 2 구독 설계
- [ ] 8. AdMob 계정 + Google Play Console 준비 (병행 트랙)
- [ ] 9. 순수익 대시보드 생성 (AdMob 수익 + Google Ads 비용 같은 시트)
- [ ] 10. 익명 빌드 인 퍼블릭 채널 1개 세팅 (X 또는 Threads)
- [ ] 11. Cursor 설치 + 10단계 워크플로 문서 템플릿 준비 (roman-koch 모델)

---

## 판단 기준 숫자표

| 단계 | 기준 수치 | 행동 |
|------|----------|------|
| 앱당 기준 단위 | 하루 $1 | 이 기준으로 유지/휴면 분류 |
| 소액 수익 | 하루 $1 미만 | 휴면 자산, 다음 앱으로 이동 |
| 유지 | 하루 $1~$5 | Google Ads 예산 소폭 증액 |
| 집중 투자 | 하루 $5~$10 | 인접 앱 크로스프로모션 연결 |
| 주력 수입원 | 하루 $10+ | 업데이트·광고·확장 집중 |
| 전체 포트폴리오 목표 (3개월) | 하루 $10~$30 | 누적 20~30개 앱 기준 |
| 전체 포트폴리오 목표 (6개월) | 하루 $100 | 50~60개 앱 기준 (programmingzombie 사례) |
| 월급 이상 부가수익 | — | 150개 앱 시점 (programmingzombie 사례) |
| Google Ads 시작값 | 설치당 비용 200~600원 | 일일예산 = 설치당 비용 × 50 (programmingzombie 기준) |
| ASO 진입 기준 | 인기 점수 20 초과, 난이도 70 미만 | roman-koch 기준 |
| 경쟁 시장 판단 | 월매출 추정 $20,000+ | 강한 신호 (roman-koch) |
| 위험 시장 판단 | 월매출 추정 $5,000 미만 | 보통 보류 (roman-koch) |

---

## 자주 참조할 파일

- [`Blog/_master/master-playbook.md`](./master-playbook.md) — 8명 종합 전략 전문, 30/60/90 실행 플랜
- [`Threads/dalgom.bami/insights/`](../../Threads/dalgom.bami/insights/) — iOS 구독 모델 1순위 트랙 원본 (Part 2.3 소스)
- [`Blog/programmingzombie/insights/replication-playbook.md`](../programmingzombie/insights/replication-playbook.md) — 포트폴리오 모델 원형, AdMob 운영 기준값
- [`Blog/roman-koch/insights/replication-playbook.md`](../roman-koch/insights/replication-playbook.md) — Cursor 10단계 워크플로, ASO 필터 기준
- [`Blog/sebastian-rohl/insights/replication-playbook.md`](../sebastian-rohl/insights/replication-playbook.md) — 인접 확장, 크로스프로모션, AI 파이프라인
- [`Blog/hussein-el-feky/insights/replication-playbook.md`](../hussein-el-feky/insights/replication-playbook.md) — 무료 배포 + House ads 교차 홍보

---

*이 파일은 `Blog/_master/master-playbook.md`의 요약본이다. 판단 근거가 필요할 때는 원본 플레이북의 Part 5(함정) 또는 Part 6(원문 수치)를 확인한다.*
