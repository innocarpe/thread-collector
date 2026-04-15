# TemperStone 앱 포트폴리오 사업 마스터 플레이북
— 7명 creator 종합 분석에서 도출한 실행 가능 전략

생성일: 2026-04-15
근거 코퍼스: 7명 creator / 개별 replication-playbook + overview + patterns

---

## TL;DR (30초)

1인 사업자로 앱 포트폴리오를 쌓는 가장 빠른 경로: **소형 유틸리티 앱을 주 2개 페이스로 출시하고, 하루 $1 기준으로 유지/폐기를 빠르게 판단한다.**
programmingzombie는 50~60개 시점에 하루 $100을 달성했고, 150개에서 회사 월급 이상을 넘겼다.
AI(Cursor, Codex)로 개발 속도를 올리되, 마케팅·운영 비중을 60% 이상으로 유지하는 것이 핵심이다.
ASO + AdMob House ads 교차 홍보로 외부 광고비 없이 포트폴리오 내부 트래픽을 순환시켜야 한다.
"빌드 인 퍼블릭"으로 출시 전부터 수요를 쌓는 구조를 병행한다. 스텔스 제약 기간(~2026-06-30)에는 핸들만 익명으로 운영하면 된다.

---

## 7명 creator 매핑

| creator | 강점 | TemperStone 복제 가치 | 핵심 수치 |
|---------|------|---------------------|----------|
| programmingzombie | Android 대량 포트폴리오 + AdMob 운영 | **가장 직접 복제 가능한 모델** — 350앱 포트폴리오, 월 주 2개 출시 | 50~60개 → 하루 $100 / 150개 → 월급 이상 / 월수익 회사 월급 4~7배 |
| sebastian-rohl | 생산성 SaaS, ASO, 크로스프로모션 | 인접 확장 모델 + AI 파이프라인 | 2025년 1월 매출 $112k, FocusKit 출시 첫날 $111 |
| hussein-el-feky | 무료 앱 + AdMob House ads | ASO + 자사 앱 교차 홍보 구조 | 1M installs(~4년 누적), Typing Master 25개국 이상 Top 100 |
| roman-koch | Cursor 기반 10단계 워크플로, 검증 우선 | 개발 파이프라인 구체 절차 | 2025년 8개 출시, ThinkPool 프로토타입 약 3시간 |
| yuma-ueno | 고성장 인디 사례 분석 | 외부 사례 패턴 학습 | Ernesto Lopez 11 AI앱 월 $70k+, Ben Cera 3개월 ARR $6.2M+ |
| adam-wathan | 오픈소스 → 유료 업셀 | 개발자 대상 프리미엄 패키지 전략 | 3일 런치 매출 $61,392 / Tailwind UI 5개월 만에 $200만 직전 |
| weyoume | 주간 공개 로그, 초협소 유틸리티 | 블로그-앱 동시 운영 루틴 | 다이어트 로그 15~26주차 연속 공개 |

### Threads 광고수익 creator 3명

> 소스 다름 주의: 아래 3명은 Blog 코퍼스(7명)와 다른 소스인 **Threads.net 게시글**에서 수집되었다. 앱 포트폴리오가 아니라 **순수 콘텐츠 광고수익(AdSense·Tistory·WordPress)** 모델 creator다.

| creator | 팔로워(수집 시점) | 수익 모델 | 공개 수치 | TemperStone 복제 가치 |
|---|---|---|---|---|
| @dual__income | 68 | 워드프레스 블로그 + 애드센스 + 외부유입 | 워드프레스 6개월 수익 0원 → 외부유입 전환 후 그 달에 $100 돌파; 블로그로 월 50만 원 공개 | 0→1 초기 구간 직접 복제 가능한 5단계 실행 순서 |
| @ywkim2026 | 7 | 워드프레스 10개 사이트 포트폴리오 + 애드센스 | 하루 $10 박스권(10~15달러); 페이지 RPM 7.78; 워드프레스 개별 사이트 RPM 10~20달러; 티스토리 10개 삭제 후 수익률 상승; 유료 광고 미사용 | 개발자 본업 + 부수입 수익형 블로그 운영 패턴 — 운영자 배경과 최대 일치 |
| @worp_cy | 45 | 워드프레스·티스토리 병행 + 애드센스 | 소수점 수익 → 하루 $1 돌파 기록; 애드센스 총 3개 도메인 승인 체득; 티스토리 수익 급감 후 워드프레스 전환 고민 실시간 공개 | 플랫폼 선택(티스토리 vs 워드프레스) 실전 비교 기록 |

원본: `Threads/dual__income/insights/` · `Threads/ywkim2026/insights/` · `Threads/worp_cy/insights/`

---

## Part 1 — 수렴하는 패턴 (공통 인사이트)

### 1.1 대량 출시 + 소액 수익 포트폴리오 모델

programmingzombie의 핵심 명제: "앱 100개면 하루 $100"이라는 가설로 포트폴리오를 확장했고, 실제로는 **50~60개 시점에 하루 $100**을 달성했다. 153개 앱 시점에 회사 월급 이상 부가수익, 이후 **월수익이 회사 월급의 4~7배**까지 올라갔다.

yuma-ueno가 분석한 사례들도 같은 방향이다. Ernesto Lopez는 11개 AI 앱으로 월 $70k+를 운영했고, Hunter Isaacson은 1년 안에 앱 5개를 출시하며 피벗에 성공했다.

hussein-el-feky도 단일 히트가 아니라 여러 앱의 누적 포트폴리오로 **약 4년에 걸쳐 1M installs**에 도달했다.

**TemperStone 적용 원칙**: 대박 1개가 아니라 앱당 하루 $1 기준으로 포트폴리오를 쌓는다. 첫 앱의 완성도보다 두 번째, 세 번째 앱 출시 속도가 더 중요하다.

**핵심 판단 단위**: 앱당 하루 $1. programmingzombie는 이 소박한 기준이 실행 장벽을 낮추고 포트폴리오 확장을 가능하게 했다고 반복 설명했다.

### 1.2 인접 확장 (한 사용자층 유지)

sebastian-rohl은 HabitKit(habit tracker)에서 FocusKit(pomodoro timer)으로 확장할 때 완전히 새로운 시장이 아니라 **같은 자기계발/생산성 문맥** 안에서 이동했다. 기존 사용자 대상 HabitKit 설정 화면 배너로 크로스프로모션을 했고, FocusKit은 초기 랭킹 없이도 성장했다.

adam-wathan도 유료 책 → Tailwind CSS(오픈소스) → Tailwind UI(프리미엄 상업 제품)로 이어지는 인접 확장을 했다. 매번 기존 오디언스를 재사용했다.

hussein-el-feky는 AdMob House ads를 활용해 유료 광고비 없이 자사 앱 간 트래픽을 순환시켰다.

**TemperStone 적용 원칙**: iOS 유틸리티 앱 포트폴리오를 묶을 때 카테고리를 너무 분산하지 말고, 특정 사용자군(예: 개인 생산성, 기록 관리, 간단 계산)을 먼저 정한 뒤 그 안에서 인접 앱을 계속 출시한다. 앱이 2개 이상이 되는 시점부터 AdMob House ads 교차 홍보를 즉시 세팅한다.

### 1.3 AI 활용 속도 가속

roman-koch의 10단계 워크플로: 문서화 후 Cursor에 전체 문서를 넣고 `Please review all project files and ask questions if anything is unclear.`로 먼저 리뷰시킨 뒤 구현한다. ThinkPool 첫 동작 프로토타입이 **약 3시간** 만에 나왔다.

sebastian-rohl은 AI를 `기획 모델 → 구현 모델 → 인간 리뷰` 파이프라인으로 사용했다. Opus 4.6으로 계획하고 Codex 5.3으로 구현한 뒤 직접 리뷰하는 방식을 명시했다. 한 번은 자는 동안 React 앱 **33 files, almost 8,000 lines of code**가 생성됐다.

programmingzombie는 ChatGPT로 광고 제목·설명·이미지 초안을 빠르게 만들고, AI 자동화로 **1년** 동안 **100개**를 추가 출시해 **월수익 회사 월급의 4~7배**까지 확대했다.

yuma-ueno 사례들에서도 Ernesto Lopez, Ben Cera, Matthew Gallagher 모두 AI를 코드 생성보다 반복 구현, 카피라이팅, 운영 문서화에 먼저 적용했다.

**TemperStone 적용 원칙**: AI를 "코드를 다 써달라"보다 "기획 → 문서화 → 구현 → 리뷰" 단계별 보조 도구로 사용한다. HOW보다 WHAT/WHY를 AI에게 준다(sebastian-rohl 원칙).

### 1.4 공개적으로 만들기 (Build in Public)

adam-wathan은 이메일 리스트, 트위터, 라이브스트리밍으로 작업 과정을 계속 노출했고, 출시 전 이메일 리스트 1,500명만으로 **3일 런치 매출 $61,392**를 만들었다.

sebastian-rohl은 X, LinkedIn, Bluesky, Threads에 동시 크로스포스팅했고, 공개 책임감이 출시 마감을 지키게 만들었다.

yuma-ueno가 분석한 Jack Friks는 X 빌드 인 퍼블릭으로 팔로워 기반 유통을 만들었다.

weyoume는 개인 루틴(다이어트 로그, Xcode 오류 해결)을 주간 단위 공개 기록으로 운영하며 콘텐츠와 제품 아이디어를 동시에 확보했다.

**TemperStone 적용 원칙**: 스텔스 제약(~2026-06-30) 동안에는 익명 핸들로 X 또는 Threads에서 제작 과정을 공개한다. 실명·회사명 없이도 "매주 앱 2개 출시 챌린지" 형태의 빌드 인 퍼블릭은 가능하다. 스텔스 해제 후 핸들을 본계정에 연결하면 된다.

### 1.5 순수익 기준 운영 루틴

programmingzombie는 AdMob 수익과 Google Ads 비용을 **같은 화면**에서 보며 순수익 기준으로 의사결정해야 한다고 반복 강조했다. Google Ads 시작 기준값: **타깃 설치당 비용 200~600원**, **일일예산은 설치당 비용 × 50**.

sebastian-rohl은 RevenueCat 대시보드로 총매출, MRR, 활성 구독자, 최근 28일 매출을 추적했다. FocusKit 초기 ASO: 미국 habit tracker 2위, 오스트리아 1위.

roman-koch는 앱별 다운로드, 매출, 키워드 인기/난이도, 경쟁 앱 리뷰 수, 경쟁 앱 월매출 추정을 기본 측정판으로 유지했다.

hussein-el-feky는 스토어 리스팅(설명문, 키워드, 스크린샷) 변경 전후 설치 수를 기록하고, 성과가 나쁘면 이전 리스팅으로 되돌렸다.

**TemperStone 적용 원칙**: AdMob 수익 + Google Ads 비용을 같은 시트에서 보는 순수익 대시보드를 Day 0에 만든다. 앱당 지표는 최소 `다운로드`, `광고 수익`, `광고비`, `순수익`, `설치당 비용`으로 구성한다.

### 1.6 광고수익 콘텐츠의 초기 0→1 반복

> 소스: Threads 3명 (@dual__income, @ywkim2026, @worp_cy) — Blog 코퍼스와 다른 소스.

3명의 데이터에서 공통으로 드러나는 패턴은 **"소수점 → $1 → 박스권 → 탈출"의 구간별 반복**이다.

@worp_cy는 "몇 주 전만 해도 소수점이어서 지금은 너무 좋아"라고 기록했고, 이후 하루 $1 돌파를 시스템 작동의 첫 증거로 다뤘다. @dual__income은 워드프레스 6개월 동안 수익 0원 → 외부유입 전략 전환 후 그 달에 $100을 돌파했다. @ywkim2026은 하루 $10~$15 박스권에 머물면서 "어떻게 탈출 해야할지"를 커뮤니티에 공개적으로 물었고, 대량 발행 전략(RPM 1~2달러 수준)에서 기존 글 파이프라인 최적화로 전환 후 RPM 7.78까지 올렸다.

세 사람 모두 **물량(발행량)**으로 뚫으려다가 구조(유입 경로·RPM 효율) 문제임을 뒤늦게 발견하는 동일한 학습 궤적을 겪었다.

**TemperStone 적용 원칙**: 광고수익 블로그를 병행할 경우 첫 목표는 하루 $1(시스템 작동 증거), 두 번째 목표는 박스권($10~$15) 진입 후 유입 경로 집중 보강이다. 발행량 대신 RPM과 유입 채널 수를 기준 지표로 설정한다.

---

## Part 2 — 갈라지는 전략 (차별 지점)

### 2.1 수익화 모델 비교

| creator | 모델 | 적용 조건 |
|---------|------|----------|
| programmingzombie | AdMob + Google Ads | 대량 무료 유틸리티, Android 포트폴리오 |
| sebastian-rohl | 구독 SaaS (App Store) | 생산성 카테고리, iOS 네이티브 차별점 존재 시 |
| hussein-el-feky | 무료 + AdMob + House ads 교차 홍보 | 설치 수 극대화, 포트폴리오 내 트래픽 순환 |
| adam-wathan | 일회성 디지털 제품 → 티어드 패키지 업셀 | 개발자 대상, 오픈소스 배포 자산 활용 |
| roman-koch | 유료 앱 + ASO (광고 최소화) | 앱스토어 유기 발견에 의존, 고품질 소수 제품 |
| yuma-ueno 사례 | 혼합 (구독, ARPU 높은 틈새, 바이럴 루프) | 제품 내장형 유통이 가능한 경우 |
| weyoume | 주간 공개 로그 → 앱 유입 | 콘텐츠-앱 동시 운영이 가능한 경우 |

### 2.2 어떤 모델이 TemperStone에 맞나?

TemperStone 컨텍스트: iOS/SwiftUI 숙련 + Kotlin/Android 수년 + Python 가능, 1인 운영, 0→1 단계, 앱 포트폴리오 사업 직전.

**추천 순위**:

**1순위 — programmingzombie + hussein-el-feky 복합 모델**
- Android와 iOS 양쪽 개발 가능한 TemperStone의 강점을 최대로 활용
- 소형 유틸리티 앱 대량 출시 → AdMob 수익화 → 포트폴리오 내 House ads 교차 홍보
- 첫 앱부터 하루 $1 기준으로 빠르게 판단, 50~60개 시점에 하루 $100 목표
- Google Ads는 효율 확인 후 좁은 타깃으로 소액 집행

**2순위 — sebastian-rohl 모델 (2번째 앱부터 병행)**
- 첫 앱으로 사용자층 확보 후, 인접 생산성 앱으로 확장
- 첫 앱 설정 화면 배너 크로스프로모션 즉시 적용
- iOS 네이티브 기능(Live Activities, Widget)이 차별점이 되는 아이디어 선별

**3순위 — roman-koch 워크플로 (개발 파이프라인 도구로 사용)**
- Cursor 10단계 워크플로를 모든 앱 개발에 기본 절차로 적용
- ASO 검증(인기 점수 20 초과, 난이도 70 미만)을 아이디어 필터로 사용

**당분간 보류 — adam-wathan 모델**
- 개발자 오디언스 대상 프리미엄 디지털 제품은 오디언스 빌딩이 먼저 필요
- 현재 0개 앱 → 포트폴리오 구축 후 재검토

---

## Part 2.5 — 광고수익 콘텐츠 채널 (AdSense·Tistory·WordPress)

> 기존 Part 2의 수익화 모델 비교가 앱(AdMob·구독·디지털 제품) 중심이라, TemperStone이 원한 "순수 콘텐츠 광고수익" 경로를 별도 항목으로 보강한다. 강의 판매 모델은 제외. 소스: Threads 3명 (@dual__income, @ywkim2026, @worp_cy) — Blog 코퍼스와 다른 소스.

### 2.5.1 3명의 광고수익 실체 (원문 수치 인용)

**@dual__income — $0 → $100 돌파 궤적**

- 워드프레스 6개월 동안 수익 0원 → 포기 직전 ("블로그로 돈 버는 놈들은 '외부유입' 한다고 해서 따라함 / 그 달에 바로 100달러 뚫어버리더라")
- 외부유입 3채널: 네이버 지식인 답변 채택 / 네이버 블로그 스마트블록 키워드 틈새 상위노출 (블로그 지수 낮아도 일 방문 2~4만 가능) / 네이버 카페 잠입형 글
- 핵심 수치: "외부유입 10%만 애드센스로 들어와도 월 100달러 무조건 넘어가서"
- 현재 블로그로 월 50만 원 수익 공개 ("블로그로 '월 50만 원'씩 나오니까… 그제야 숨통 트이더라")
- 블로그 주제별 일일수익 기준 매핑 (원문): ~ $0.10 = 일기·감정·넋두리 / $1~$5 = 맛집 후기·영화 리뷰 / $5~$10 = 일상 꿀팁·제품리뷰 / $10~$30 = 정부지원금·대출·자동차
- 5단계 실행 순서 (원문): 승인율 높은 주제 선택 → GPTs로 승인용 글 20개 작성 → 애드센스 승인 신청 → 네이버 외부유입 3군데 뚫기 → [글쓰기 + 외부유입] 세트 돌리기

**@ywkim2026 — 개발자 본업 + 수익형 블로그 다사이트 포트폴리오**

- 워드프레스 10개 사이트 운영 중; 티스토리 10개는 애드센스 삭제
- 현재 애드센스 평균 하루 $10 ("애공 평균..하루10달러 ……언제쯤 20-30달러 될러냐.. / 참고로 유료광고 안함")
- 전략 전환 기록: "한달 전까지 대량 글로만 승부 했지만 RPM이 1-2달러 수준… 트래픽 많지만 비효율…… / 신규 글 발행보다 기존 글 파이프라인으로 RPM 올리는 중"
- 현재 RPM: 페이지 RPM 7.78 / 개별 사이트 RPM 10~20달러 / 목표 "페이지RPM 10달러 넘겨보자"
- 티스토리 전체 삭제 후 수익률 상승 곡선 ("티스토리 사이트 모두 삭제 했더니… 수익률 싱승 곡선… / 오늘 20달러 돌파할지 지켜보자")
- $10~$15 박스권 탈출이 당면 과제; 유료 광고 없이 구조 개선으로 해결 시도 중

**@worp_cy — 직장인 N잡러, 티스토리→워드프레스 전환 실시간 기록**

- 정체성: "직장인이지만 월급 외 수익을 위해 여러가지 시도중인 N잡러 / 결국 애드센스에 대한 이야기지"
- 수익 궤적: 소수점 → 하루 $1 ("몇 주 전만 해도 소수점이어서 지금은 너무 좋아") → 1달러 벽도 무너질 수 있음 기록
- 티스토리 수익 급감 경험 + 플랫폼 리스크 공개 ("티스토리 뭔일 있는지 수익이 급감 / 티스토리와 워드프레스 병행하다가 / 워드프레스 수익 올라가면 갈아타긴 해야할 듯")
- 애드센스 승인 총 3개 도메인 체득 ("이로써 승인은 총 3개 도메인 냈고 / 얼추 승인 방법도 체득이 되었다")
- AI 활용 기준: 초반 가속 도구로 사용하되 후처리 필수 ("완전 ai 복붙은 아니고 내가 후처리 가공을 했지")

### 2.5.2 이 모델의 장점 / 단점 (앱 AdMob 모델과의 비교)

| 항목 | 앱 AdMob 모델 (Part 2, programmingzombie 기준) | 광고수익 블로그 모델 (Part 2.5) |
|---|---|---|
| 초기 투입 | 중 (앱 1개 개발 + AdMob 연결) | 저 (글 1편 = 최소 단위, 투자금 0원 — @dual__income 원문) |
| 현금흐름 발생 시점 | 앱 출시 후 설치 수 확보까지 수 주~수 개월 | 애드센스 승인 후 외부유입 확보 시 수 주 내 (외부유입 전환 후 그 달에 $100 — @dual__income 원문) |
| 하루 $1 달성 조건 | 설치 수 × eCPM / 광고 노출 구조 | 유입 트래픽 × RPM (소수점→$1: 수 주 — @worp_cy 원문) |
| 장기 자산화 | 앱 수명 동안 계속 수익 (앱 하나가 약 4년간 $0.1~$0.2/일 — programmingzombie 원문) | "3년 뒤 시작한 사람은 지금 쓴 네 글을 따라올 수 없음" — @dual__income 원문 |
| 스케일 상한 | 포트폴리오 × 앱당 수익 (50~60개 → 하루 $100 — programmingzombie 원문) | RPM 개선 × 사이트 수 × 트래픽 (현재 RPM 10~20달러 목표 — @ywkim2026 원문) |
| 개발자 활용도 | 높음 (iOS/Android 직접 개발) | 낮음 (글쓰기 중심; 개발 배경은 기술 블로그 주제로 활용 가능) |
| 플랫폼 리스크 | 앱스토어 정책 / 알고리즘 변화 | 티스토리 의존 시 급감 리스크 — @worp_cy 직접 경험 |

### 2.5.3 TemperStone이 "무엇부터 시작할지"에 대한 직답

운영자의 원래 고민: "수익화 콘텐츠 제작 파이프라인 뭐부터 만들지(가장 빠르고 쉽게)?"

3명 데이터 기반 권장 진입 순서:

1. **워드프레스 블로그 개설 + 애드센스 승인** — 투자금 0원, @dual__income의 5단계 순서 그대로 실행 (승인율 높은 주제 → GPTs로 승인용 글 20개 → 신청). @worp_cy는 동일 방법으로 총 3개 도메인 승인 체득.
2. **외부유입 3채널 세팅** — 승인 직후 바로 착수. @dual__income: "외부유입 10%만 애드센스로 들어와도 월 100달러 무조건 넘어가서." 네이버 지식인 + 스마트블록 키워드 + 네이버 카페 조합.
3. **RPM 효율 최적화 (대량 발행 대신)** — @ywkim2026이 증명한 전환: "신규 글 발행보다 기존 글 파이프라인으로 RPM 올리는 중." 티스토리 비효율 자산 정리 후 수익률 상승.

특히 @ywkim2026이 개발자 본업 + 부수입 수익형 블로그 다사이트 포트폴리오를 운영하는 패턴이 TemperStone 14년차 풀스택 배경과 **가장 직접 이식 가능**. 이 경로를 메인으로 잡고, @dual__income의 0→1 궤적 수치($100 돌파 실기록)를 벤치마크로 쓴다.

---

## Part 3 — TemperStone 30/60/90 실행 플랜

### Day 0 (오늘)

- [ ] **아이디어 10개 후보 선정**: 앱브레인, 구글 트렌드, 네이버 데이터랩, ASO 도구로 키워드 조사. roman-koch 기준 적용 — ASO 인기 점수 20 초과, 난이도 70 미만, 경쟁 앱 월매출 추정 $5,000 초과
- [ ] **첫 앱 주제 확정**: "작고 자주 쓰이는 유틸리티", "광고 노출 구조 가능", "타깃 구매력 낮지 않음" 세 조건 확인
- [ ] **순수익 대시보드 초안 생성**: AdMob 수익 + Google Ads 비용을 같은 시트에서 보는 구조 설계
- [ ] **익명 빌드 인 퍼블릭 채널 1개 세팅**: X 또는 Threads에 익명 핸들 (스텔스 제약 ~2026-06-30 동안 실명·회사명 제외)
- [ ] **AdMob 계정 + Google Play Console + App Store Connect 준비 확인**
- 필요 도구: 앱브레인, 앱애니, 구글 트렌드, 네이버 데이터랩, Sensor Tower, ASO 도구, Google Sheets, AdMob, Cursor

### Week 1 (첫 주)

- [ ] **첫 앱 MVP 출시 (iOS 또는 Android 중 더 빠른 쪽)**: 핵심 기능만, 기획-개발-배포 1시간 미만 목표 (programmingzombie 기준)
- [ ] **Cursor 10단계 워크플로 1회 적용** (roman-koch): 문제 정의 문서 → 화면 명세 → Mermaid 플로우 → Cursor 리뷰 → Build
- [ ] **두 번째 앱 아이디어 준비**: 공통 템플릿 기반으로 "주제만 바꾸면 뽑을 수 있는 구조" 마련
- [ ] **AdMob 연결 + 설치 수 모니터링 시작**
- [ ] **빌드 인 퍼블릭 첫 포스팅**: 앱 출시 과정 공개
- 목표: 앱 1개 출시, 공통 템플릿 1개, AdMob 연결, 첫 공개 포스팅

### Month 1 (1~4주차)

- [ ] **주 2개 앱 출시 챌린지 가동** (programmingzombie 모델): 4주 × 2개 = 최소 8개 앱
- [ ] **앱별 하루 $1 판단 기준 성과표 운영**: `하루 $1 미만` / `하루 $1~$5` / `확장 후보` 분류
- [ ] **Google Ads 소액 첫 실험**: 타깃 설치당 비용 200~600원, 일일예산 = 설치당 비용 × 50, 좁은 국가·언어 타깃 (programmingzombie 기준값)
- [ ] **AdMob House ads 세팅**: 앱 2개 이상부터 포트폴리오 내 교차 홍보 (hussein-el-feky 모델)
- [ ] **ASO 첫 실험**: 설명문, 스크린샷 변경 전후 설치 수 기록 (hussein-el-feky 모델)
- 마일스톤: 앱 8개 출시, AdMob 수익 첫 발생, 앱당 하루 $1 분류표 가동
- 측정 지표: 앱별 순수익, 설치당 비용, AdMob eCPM, ASO 순위

### Month 3 (1~12주차)

- [ ] **누적 앱 20~30개 목표**: 상위 성과 앱에 광고·업데이트 집중, 반응 없는 앱은 휴면 자산으로 관리
- [ ] **하루 $10~$30 구간 진입 확인**: programmingzombie 기준으로 10~15개 주력 수입원, 20~30개 중간 성과 앱 분류
- [ ] **인접 앱 첫 번째 크로스프로모션 실험** (sebastian-rohl 모델): 기존 앱 설정 화면에 신규 앱 배너 삽입
- [ ] **Cursor 워크플로 속도 최적화**: 문서화 시간 단축, 공통 템플릿 고도화
- 판단 기준: 하루 $10 달성 앱이 1개 이상이면 해당 카테고리 인접 확장 검토. 전체 포트폴리오 일 순수익 합산 $10~$30 도달 여부

### Month 6 (1~26주차)

- [ ] **누적 앱 50~60개 목표**: programmingzombie 사례 기준 이 시점에 하루 $100 달성 가능성 검증
- [ ] **iOS + Android 동시 배포 파이프라인 구축**: SwiftUI + Kotlin Compose 공통 템플릿으로 플랫폼 간 이식 속도 향상
- [ ] **구독 SaaS 1개 가능성 검토** (sebastian-rohl 모델): AdMob 포트폴리오 수익이 안정화되면 MRR 기반 앱 1개 병행
- [ ] **빌드 인 퍼블릭 팔로워 첫 측정**: 스텔스 해제(2026-06-30) 직후 실명 연결 준비
- 목표: 포트폴리오 하루 순수익 $30~$100, 앱 50~60개, 운영 자동화 루틴 안정화

---

## Part 3.5 — 옵션 B: 광고수익 블로그 브리지 (병행)

> 소스: Threads 3명 (@dual__income, @ywkim2026, @worp_cy) — Blog 코퍼스와 다른 소스.

앱 포트폴리오(옵션 A)가 50~60개에서 하루 $100을 만들려면 수개월 걸린다. 그동안 현금흐름 없이 버티는 대신, 광고수익 블로그를 병행해 브리지를 만든다. 두 채널은 서로 경쟁하지 않고, 오히려 앱 개발 중 발생하는 문제 해결 과정 자체가 블로그 글감이 된다(@ywkim2026 모델: 개발자 본업 + 부수입 수익형 블로그 다사이트 포트폴리오). @dual__income: "블로그 투자금은 0원. 지금은 돈보다 '돈버는 구조' 구축이 중요."

### Day 0 (블로그 쪽)
- [ ] **워드프레스 블로그 1개 개설** — 티스토리가 아닌 워드프레스로 시작 (@ywkim2026: 티스토리 전체 삭제 후 수익률 상승; @worp_cy: 워드프레스 수익 올라가면 갈아타긴 해야할 듯)
- [ ] **승인율 높은 주제 1개 선정** — @dual__income 원칙: "한 가지 주제 + 일관성 이게 핵심", YMYL(건강/금융) 제외, 상업성 키워드 25% 미만 유지
- [ ] **GPTs로 승인용 글 20개 작성 후 애드센스 승인 신청** — @dual__income 5단계 그대로; @worp_cy: 3개 도메인 승인 체득

### Week 1 (블로그 쪽)
- [ ] **네이버 외부유입 3채널 세팅 시작** — @dual__income: 지식인 답변 + 스마트블록 키워드 + 카페 잠입형 글. "외부유입 10%만 들어와도 월 100달러 무조건 넘어가서"
- [ ] **하루 1편 글쓰기 + 외부유입 작업 루틴** — @dual__income: "애드센스 블로그 글 1개를 쓰고 그날 외부유입 작업을 하는거징. 즉각적인 조회수 반응이 온다니까"
- [ ] **RPM 기준 지표 세팅** — 발행량이 아니라 페이지 RPM을 성과 지표로 사용 (@ywkim2026 원칙)

### Month 1 (블로그 쪽)
- [ ] **하루 $1 달성 여부 확인** — @worp_cy: 소수점 → $1이 시스템 작동 첫 증거. "$1 박스권도 무너질 수 있다 / 그만두지만 않으면 된다"
- [ ] **개발 경험을 블로그 글감으로 전환** — 앱 개발 중 겪은 Xcode 오류, SwiftUI 이슈, AdMob 연결 팁 → 기술 블로그 포스팅. @dual__income 주제별 수익 기준: $5~$10/일 = 일상 꿀팁·제품리뷰 구간
- [ ] **비효율 자산 점검** — RPM이 안 나오는 글은 키워드·구조 개선 or 정리 (@ywkim2026: "신규 글 발행보다 기존 글 파이프라인으로 RPM 올리는 중")
- 마일스톤: 블로그 1개 운영, 하루 $1 진입, 외부유입 3채널 중 1개 이상 작동

---

## Part 4 — 도구 스택 추천 (7명이 실제로 쓴 도구만)

| 카테고리 | 추천 도구 | 근거 creator | 비용 |
|----------|-----------|------------|------|
| AI 코딩 | Cursor | roman-koch 10단계 워크플로, 프로토타입 약 3시간 | $20/mo |
| AI 기획·리뷰 | Claude (Opus 계열) | sebastian-rohl: 기획 모델로 Opus 사용 | 사용량 과금 |
| AI 구현 | Codex (GPT 계열) | sebastian-rohl: 구현 모델로 Codex 사용 | 사용량 과금 |
| AI 광고 소재 | ChatGPT | programmingzombie: 광고 제목·설명·이미지 초안 | $20/mo |
| 수익화 (구독) | RevenueCat | sebastian-rohl: MRR, 활성 구독자, 28일 매출 추적 | 무료 시작 |
| 수익화 (광고) | AdMob | programmingzombie, hussein-el-feky: 핵심 수익 채널 | 무료 |
| UA 광고 | Google Ads | programmingzombie: 설치당 비용 200~600원, 일일예산 ×50 | 집행액 과금 |
| 검색 광고 | Apple Search Ads | sebastian-rohl: 설치당 비용 약 2.14€, 탭→설치 전환 약 60% | 집행액 과금 |
| ASO 리서치 | Sensor Tower | roman-koch: 경쟁 앱 월매출 추정 | 유료 |
| ASO 리서치 | AppBrain, AppAnnie | programmingzombie: 키워드·연관 검색어 조사 | 무료/유료 |
| 트렌드 | Google Trends, 네이버 데이터랩 | programmingzombie: 시장 수요 확인 | 무료 |
| 수요 검증 | Reddit | roman-koch: 반복 질문, 불만, 실패 해결책 찾기 | 무료 |
| 플로우차트 | Mermaid | roman-koch: 개발 전 흐름도 문서화 | 무료 |
| 스토어 운영 | Google Play Console, App Store Connect | 전체 creator | 무료 |
| 운영 자동화 | Claude Code (오전/오후 루틴) | sebastian-rohl: 오전 6AM 브리핑, 오후 6PM 저널 | 사용량 과금 |

### 블로그 광고수익 추가 도구 (Threads 3명 기반)

> 소스: Threads 3명 (@dual__income, @ywkim2026, @worp_cy) — Blog 코퍼스와 다른 소스.

| 카테고리 | 추천 | 근거 | 비용 |
|---|---|---|---|
| 블로그 플랫폼 | 워드프레스 (WordPress) | @ywkim2026: 워드프레스 10개 운영, 티스토리 10개 삭제 후 수익률 상승; @worp_cy: "워드프레스 수익 올라가면 갈아타긴 해야할 듯" | 호스팅 비용 ($5~$15/mo) |
| 블로그 플랫폼 (단기 시작) | 티스토리 | @worp_cy: 초기 승인 실험 다수; @dual__income: 초보 진입 채널. 단, 알고리즘 의존 리스크 있음 | 무료 |
| 광고 네트워크 | Google AdSense | @dual__income, @ywkim2026, @worp_cy 공통 핵심 수익 채널 | 무료 (수익 쉐어) |
| 콘텐츠 보조 | GPTs (ChatGPT) | @dual__income: "GPTs로 승인용 글 20개 작성"; @worp_cy: 후처리 가공 전제로 AI 포스팅 실험 | $20/mo |
| 외부유입 | 네이버 지식인 + 네이버 카페 | @dual__income: 외부유입 전환 후 그 달에 $100 돌파의 핵심 채널 | 무료 |
| SEO 키워드 | 스마트블록 키워드 조사 (네이버 블로그 기반) | @dual__income: "블로그 지수 낮아도 이 방법으로 일 방문 2~4만 가능" | 무료 |
| 수익 추적 | 애드센스 대시보드 (RPM 기준) | @ywkim2026: 페이지 RPM을 핵심 지표로 관리; 하루 단위 + 시간 단위 체크 | 무료 |

---

## Part 5 — 함정과 안티패턴

### 5.1 긴 개발 → 출시 후 zero traction

> "6개월 공들인 앱보다 하루 만에 만든 앱이 10배 이상 수익을 낸다."
> — programmingzombie (2023-02-07-106-insight.md)

> "몇 달간 개발한 뒤 출시했는데도 zero traction이 나오는 함정이 가장 크다."
> — roman-koch (2025-02-19-insight.md)

> "Hunter Isaacson은 2년 넘게 실패 앱에 매달린 뒤 피벗했다."
> — yuma-ueno (2026-03-23-insight.md)

**대응**: 핵심 기능만 넣고 출시. roman-koch의 `80/20 Rule` — 사용자의 80%는 기능의 20%만 쓴다.

### 5.2 다운로드 수 착각

> "다운로드가 많아도 어린 층 타깃, 낮은 광고 단가, 광고 노출이 어려운 구조 때문에 수익화에 실패했다."
> — programmingzombie (2023-12-31-129-insight.md)

**대응**: 타깃 구매력, 광고 단가, 앱 구조에서의 광고 노출 가능성을 아이디어 선정 단계에서 먼저 확인.

### 5.3 AdMob 수익만 보고 광고 끄기

> "AdMob 수익과 Google Ads 비용을 따로 보면 순수익 판단이 안 된다."
> — programmingzombie (2025-07-02-173-insight.md)

**대응**: 반드시 같은 대시보드에서 순수익 기준으로 의사결정.

### 5.4 큰 리빌드 충동

> "큰 리빌드보다 작은 업데이트가 실제로 더 자주 일어난다."
> — sebastian-rohl (2026-01-11-insight.md)

**대응**: 성능 병목이나 사용자 불만은 설정 토글, 기본값 변경으로 먼저 처리. 전체 재설계는 최후 수단.

### 5.5 검증 없는 개발

> "아이디어 검증 없이 몇 달을 개발해도 출시 후 zero downloads가 나올 수 있다."
> — roman-koch (2025-04-18-insight.md)

**대응**: 코딩 전에 ASO 키워드, 경쟁 앱 리뷰 수, Reddit 반응, 사전 등록으로 수요 먼저 확인.

### 5.6 광고를 ROAS 관점으로만 보기

> "초기 광고는 채널 감을 배우는 단계다. 수익성보다 채널 학습이 우선."
> — sebastian-rohl (2025-12-07-insight.md)

**대응**: 첫 Google Ads / Apple Search Ads는 소액(programmingzombie: 일일예산 설치당 비용 × 50)으로 채널 데이터 수집용으로 운영.

### 5.7 처음부터 너무 많은 공개 채널 운영

> "커뮤니티 운영 채널을 처음부터 너무 많이 벌리지 말고, 질문이 쌓일 때 공식 아카이브 채널을 연다."
> — adam-wathan 플레이북 TemperStone 주의점

**대응**: 빌드 인 퍼블릭 채널은 X 또는 Threads 중 1개만 먼저 시작.

### 5.8 AI 검토 생략

> "구현은 위임했지만 최종 검토와 수정은 직접 했다."
> — sebastian-rohl (2026-02-15-insight.md)

**대응**: AI가 생성한 코드는 반드시 직접 리뷰. 특히 결제, AdMob 연결, 개인정보 처리 부분.

### 5.9 티스토리 단일 플랫폼 의존 (광고수익 블로그 전용)

> "티스토리 뭔일 있는지 수익이 급감 / 사실 수익도 작았지만 수익나는 콘텐츠도 몇개 안됬어 / 그 포스팅이 노출 순위가 확 밀렸나봐"
> — @worp_cy (2025-01-06, Threads/worp_cy/monetization/2025-01-06-나는-수익-줄었다.md)

> "티스토리 사이트 모두 삭제 했더니… 수익률 싱승 곡선…"
> — @ywkim2026 (2026-03-23, Threads/ywkim2026/monetization/2026-03-23-티스토리-사이트-모두-삭제-했더니-수익률-싱승-곡선.md)

**대응**: 블로그 광고수익 채널은 티스토리보다 워드프레스 중심으로 가져간다. 티스토리는 초기 승인 실험 채널로만 활용하고, 수익 자산은 워드프레스로 이전한다.

### 5.10 초기 $0.1/일 구간에서 포기 (광고수익 블로그 전용)

> "워드프레스 6개월 했는데 수익 0원이라 포기 직전까지 감 / 블로그로 돈 버는 놈들은 '외부유입' 한다고 해서 따라함 / 그 달에 바로 100달러 뚫어버리더라"
> — @dual__income (2025-11-08, Threads/dual__income/monetization/2025-11-08-30대인-내가-달러-버는-방법.md)

> "몇 주 전만 해도 소수점이어서 지금은 너무 좋아"
> — @worp_cy (2024-12-24, Threads/worp_cy/monetization/2024-12-24-어제도-1달러-이상-벌었다.md)

**대응**: 발행량만 쌓는 단계에서 수익이 안 나는 것은 정상이다. 수익 구조 전환의 핵심 변수는 외부유입 채널 개통이다. @dual__income 5단계 순서(승인 → 외부유입 3채널 세팅)를 그대로 실행하기 전까지 수익 수치로 포기 판단하지 말 것.

### 5.11 발행량으로만 RPM 박스권 탈출 시도 (광고수익 블로그 전용)

> "한달 전까지 대량 글로만 승부 했지만 RPM이 1-2달러 수준… 트래픽 많지만 비효율…… / 신규 글 발행보다 기존 글 파이프라인으로 RPM 올리는 중"
> — @ywkim2026 (2026-03-27, Threads/ywkim2026/monetization/2026-03-27-현시간-기준-페이지rpm-7.md)

> "1일 5포스팅 해도 '사람 심리' 모르면 부질없다"
> — @dual__income (Threads/dual__income/viral-sns/)

**대응**: $10~$15 박스권에서 발행량 증가는 RPM을 낮춘다(트래픽 ↑, 단가 ↓). 대신 기존 글의 키워드·구조·광고 노출 개선으로 RPM 자체를 높이는 작업을 우선한다.

---

## Part 6 — 수치 베이스라인 (원문 인용)

### programmingzombie
- 50~60개 앱 시점: 하루 $100 (출처: 2025-07-28-174-insight.md)
- 150개 앱 시점: 회사 월급 이상 부가수익 (출처: 2025-07-28-174-insight.md)
- 월수익 회사 월급 4~7배: 최종 복제 목표 (출처: 2024-11-15-153-insight.md)
- 월수익 회사 월급 6~12배 이상: 수익 확장 후 (출처: 2025-07-28-174-insight.md)
- AI 자동화로 1년 동안 100개 추가 출시 (출처: 2025-09-25-178-insight.md)
- 1시간 미만 출시 앱, 20분 미만 개발 앱도 약 4년간 하루 $0.1~0.2 장기 수익 자산 (출처: 2025-04-02-167-insight.md)
- Google Ads 시작값: 설치당 비용 200~600원, 일일예산 = 설치당 비용 × 50 (출처: 2024-02-17-135-insight.md)

### sebastian-rohl
- 2025년 1월 한 달 매출: $112k (출처: 2026-01-18-insight.md)
- FocusKit 첫날 매출: $111, MRR $6 (출처: 2025-11-30-insight.md)
- FocusKit 첫 주: 다운로드 약 언급 없음 / 매출 $446, MRR $18 (출처: 2025-12-07-insight.md)
- FocusKit 출시 약 1개월: 1,600 downloads, $874 total revenue, $52 MRR (출처: 2025-12-07-insight.md)
- FocusKit 두 달 시점: Over $100 MRR (출처: 2026-01-25-insight.md)
- Apple Search Ads 실험: 75€ 집행, 550 impressions, 60 taps, 35 installs, 설치당 비용 약 2.14€, 탭→설치 전환 약 60% (출처: 2025-12-07-insight.md)
- Reddit Ads 실험: 50€ 집행, 16k impressions, 92 clicks (출처: 2025-12-07-insight.md)
- HabitKit: 미국 App Store habit tracker 2위, 오스트리아 1위 (출처: 2026-03-29-insight.md)

### hussein-el-feky
- 1M installs: 약 4년 누적 (출처: 2019-07-13-insight.md)
- Typing Master: nearly 500 thousand installs, 25개국 이상 Word Games Top 100, 인도 #15 (출처: 2019-07-13-insight.md)
- 다운로드의 90% 이상이 무료 앱 (원문 creator 관찰치, 출처: 2019-07-13-insight.md)

### roman-koch
- 2025년 출시 앱: 8개 (출처: 2026-01-04-insight.md)
- ThinkPool 첫 동작 프로토타입: 약 3시간 (출처: 2026-01-05-insight.md)
- ThinkPool 마지막 버그 수정: 약 15분 (출처: 2026-01-05-insight.md)
- SmokeFree App 2025년 성과: 다운로드 약 1,480, 매출 약 $700 (출처: 2026-01-04-insight.md)
- CookieTime 2025년 성과: 다운로드 약 78, 매출 $0 (출처: 2026-01-04-insight.md)
- Split & Tip 2025년 성과: 다운로드 약 50, 매출 $0 (출처: 2026-01-04-insight.md)
- ASO 기준: 인기 점수 20 초과, 난이도 70 미만 (출처: 2026-01-30-insight.md)
- 경쟁 앱 월매출 추정 $20,000 초과: 강한 신호 (출처: 2026-01-30-insight.md)
- 경쟁 앱 월매출 추정 $5,000 미만: 보통 너무 위험한 시장 (출처: 2026-01-30-insight.md)

### yuma-ueno 사례
- Ernesto Lopez: 11개 AI 앱, 월 $70k+ (출처: 2026-03-11-insight.md)
- Ben Cera (Polsia): 출시 3개월 만에 ARR $6.2M+ (출처: 2026-04-06-insight.md)
- Cal AI: 출시 6개월 만에 월 매출 $1M (출처: 2026-03-17-insight.md)
- NGL(Hunter Isaacson): 1년 안에 앱 5개 출시 (출처: 2026-03-23-insight.md)

### adam-wathan
- 이메일 리스트: 런치 전 1,500명 (출처: 2017-04-21-insight.md)
- 3일 런치 매출: $61,392 (출처: 2017-04-21-insight.md)
- 평균 판매가: $67.84 (출처: 2017-04-21-insight.md)
- 11개월 누적 매출: $138,835 (출처: 2017-04-21-insight.md)
- 출시 후 월 지속 매출: $1,000~$2,000 (출처: 2017-04-21-insight.md)
- Tailwind UI: 출시 약 5개월 만에 $200만 달러 직전 (출처: 2020-08-02-insight.md)

### @dual__income (Threads — Blog 코퍼스와 다른 소스)
- 워드프레스 6개월 수익 $0 → 외부유입 전환 후 그 달에 $100 돌파 (출처: Threads/dual__income/monetization/2025-11-08-30대인-내가-달러-버는-방법.md)
- 블로그 월 수익 "월 50만 원"씩 공개 (출처: Threads/dual__income/monetization/2026-01-17-빚-갚겠다고-알바-찾는-순간.md)
- 블로그 주제별 일일수익 기준: ~ $0.10 = 일기·감정 / $1~$5 = 맛집·영화 / $5~$10 = 일상 꿀팁·제품리뷰 / $10~$30 = 정부지원금·대출·자동차 (출처: Threads/dual__income/monetization/2025-10-29-글쓰기-근육량에-따른-블로그-주제.md)
- 외부유입 전략: 외부유입 10%만 애드센스 유입 시 월 $100 초과 (출처: Threads/dual__income/monetization/2025-11-08-30대인-내가-달러-버는-방법.md)
- 네이버 스마트블록 키워드 전략: 블로그 지수 낮아도 일 방문 2~4만 가능 (출처: 동일)
- 애드센스 승인 기준: 카테고리 1개, 글 20개, 상업성 키워드 25% 미만 (출처: Threads/dual__income/monetization/2026-01-04-애드센스-승인.md)

### @ywkim2026 (Threads — Blog 코퍼스와 다른 소스)
- 현재 애드센스 하루 평균 $10 / 유료 광고 미사용 (출처: Threads/ywkim2026/monetization/2026-04-10-애공-평균.md)
- $10~$15 박스권 탈출 과제 (출처: Threads/ywkim2026/monetization/2026-02-23-열심히-달려보자.md)
- 대량 발행 시 RPM 1~2달러 수준; 기존 글 파이프라인 전환 후 RPM 7.78 (출처: Threads/ywkim2026/monetization/2026-03-27-현시간-기준-페이지rpm-7.md)
- 워드프레스 10개 운영, 개별 사이트 RPM 10~20달러 (출처: 동일)
- 티스토리 10개 전체 삭제 후 수익률 상승 곡선 / 20달러 돌파 시도 (출처: Threads/ywkim2026/monetization/2026-03-23-티스토리-사이트-모두-삭제-했더니-수익률-싱승-곡선.md)

### @worp_cy (Threads — Blog 코퍼스와 다른 소스)
- 수익 궤적: 소수점 → 하루 $1 돌파 ("몇 주 전만 해도 소수점") (출처: Threads/worp_cy/monetization/2024-12-24-어제도-1달러-이상-벌었다.md)
- 티스토리 수익 급감 경험: 노출 순위 하락 → 포스팅 지속 (출처: Threads/worp_cy/monetization/2025-01-06-나는-수익-줄었다.md)
- 애드센스 총 3개 도메인 승인 체득 (출처: Threads/worp_cy/monetization/2025-01-31-오예-드디어-애드센스-승인-났다.md)
- AI 포스팅 실험: 후처리 가공 전제, 수백 개 포스팅 이상 쌓아야 유효 판단 (출처: Threads/worp_cy/monetization/2025-01-12-ai를-활용해서-포스팅을-한-4개-올려봤는데-과연-노출이-잘-될지.md)

---

## Part 7 — TemperStone 맞춤 의사결정 트리

첫 앱 선정 시 다음 흐름으로 결정한다.

```
[아이디어 후보]
    │
    ▼
[ASO 필터] — 인기 점수 20 초과? + 난이도 70 미만?
    │ NO → 폐기 또는 보류
    │ YES
    ▼
[시장 규모 필터] — 경쟁 앱 월매출 추정 $5,000 초과?
    │ NO → 폐기
    │ YES
    ▼
[광고 구조 필터] — AdMob 광고 노출이 앱 구조상 가능한가?
    │ NO → 유료 앱/구독 구조로 재설계 또는 폐기
    │ YES
    ▼
[타깃 구매력 필터] — 타깃이 어린 층이거나 광고 단가 낮은 카테고리?
    │ YES → 폐기 또는 구독 전환
    │ NO
    ▼
[속도 필터] — 1주 안에 MVP 출시 가능한가?
    │ NO → 범위 축소 또는 보류
    │ YES
    ▼
[출시] — AdMob 연결 + Google Ads 소액 실험 + 빌드 인 퍼블릭 포스팅 동시 진행
    │
    ▼
[하루 $1 판정] (출시 후 2주)
    │ 하루 $1 미만 → 휴면 자산으로 분류 + 다음 앱으로 이동
    │ 하루 $1~$5 → 유지 + Google Ads 예산 소폭 증액
    │ 하루 $5+ → 집중 투자 + 인접 앱 크로스프로모션 연결
```

**인접 앱 확장 판단 트리**:
```
[앱 N개 운영 중]
    │
    ▼
[앱 2개 이상?]
    │ YES → AdMob House ads 교차 홍보 즉시 세팅
    │
    ▼
[특정 카테고리에서 하루 $5+ 앱 존재?]
    │ YES → 같은 사용자층 인접 앱 기획 (sebastian-rohl 모델)
    │ NO → 계속 대량 출시 (programmingzombie 모델)
```

---

## 출처 색인

| 섹션 | creator | 파일 경로 |
|------|---------|----------|
| 1.1 | programmingzombie | `Blog/programmingzombie/insights/replication-playbook.md` |
| 1.1 | yuma-ueno | `Blog/yuma-ueno/insights/replication-playbook.md` |
| 1.1 | hussein-el-feky | `Blog/hussein-el-feky/insights/replication-playbook.md` |
| 1.2 | sebastian-rohl | `Blog/sebastian-rohl/insights/replication-playbook.md` |
| 1.2 | adam-wathan | `Blog/adam-wathan/insights/replication-playbook.md` |
| 1.2 | hussein-el-feky | `Blog/hussein-el-feky/insights/replication-playbook.md` |
| 1.3 | roman-koch | `Blog/roman-koch/insights/replication-playbook.md` |
| 1.3 | sebastian-rohl | `Blog/sebastian-rohl/insights/replication-playbook.md` |
| 1.3 | programmingzombie | `Blog/programmingzombie/insights/replication-playbook.md` |
| 1.4 | adam-wathan | `Blog/adam-wathan/insights/replication-playbook.md` |
| 1.4 | sebastian-rohl | `Blog/sebastian-rohl/insights/replication-playbook.md` |
| 1.4 | weyoume | `Blog/weyoume/insights/replication-playbook.md` |
| 1.5 | programmingzombie | `Blog/programmingzombie/insights/replication-playbook.md` |
| 1.5 | sebastian-rohl | `Blog/sebastian-rohl/insights/replication-playbook.md` |
| 1.5 | roman-koch | `Blog/roman-koch/insights/replication-playbook.md` |
| Part 5 | 모든 creator | 각 `replication-playbook.md` 주의사항 섹션 |
| Part 6 | 모든 creator | 각 `replication-playbook.md` 참고 글 출처 |
| Threads 매핑 표 | @dual__income | `Threads/dual__income/insights/` |
| Threads 매핑 표 | @ywkim2026 | `Threads/ywkim2026/insights/` |
| Threads 매핑 표 | @worp_cy | `Threads/worp_cy/insights/` |
| 1.6, 2.5, 3.5, 5.9~5.11, Part 6 | @dual__income | `Threads/dual__income/monetization/` (9개 파일) |
| 1.6, 2.5, 3.5, 5.10~5.11, Part 6 | @ywkim2026 | `Threads/ywkim2026/monetization/` (10개 파일) |
| 1.6, 2.5, 3.5, 5.9~5.10, Part 6 | @worp_cy | `Threads/worp_cy/monetization/` (13개 파일) |
