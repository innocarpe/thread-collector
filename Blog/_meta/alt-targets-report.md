# 대체 타겟 발굴 리포트
생성일: 2026-04-15

## 실패 3명 진단

| slug | 실패 원인 | 대체 가능성 |
|------|---------|----------|
| max-artemov | indiehackers.com robots.txt 전체 차단 | 낮음 — 개인 블로그 없음, IH 의존 |
| adam-lyttle | starterstory.com + indiehackers.com 둘 다 robots.txt 차단 | 낮음 — 독립 블로그 미확인 |
| josh-manders | joshmanders.com 사이트 존재, but RSS/Atom 피드 경로 전체 404 | 낮음 — Ghost/Substack 없음 |

---

## 후보 검증 결과 (전수)

| 후보 | 도메인 | 피드 발견 | robots 통과 | 최근 포스트 | 선정 |
|------|--------|----------|------------|------------|------|
| Jake Lee | jakelee.co.uk | `/feed` 200 ✓ | ✓ (open) | 2026-02-06 ✓ | ✗ 주제 불일치 (게임리뷰·여행) |
| Tony Dinh | tonydinh.com | 모든 경로 000 | N/A | N/A | ✗ 사이트 응답 없음 |
| Pieter Levels | levels.io | `/feed/` 301→200 ✓ | ✓ | 2022-09-18 ✗ | ✗ 마지막 포스트 2022년 |
| Marc Lou | marclou.com | `/feed` → indiepa.ge 리다이렉트 | N/A | N/A | ✗ 블로그 피드 없음 |
| Jon Yongfook | yongfook.com | 모든 경로 404 | N/A | N/A | ✗ 피드 없음 |
| Danny Postma | dannypostma.com | 모든 경로 308 루프 | N/A | N/A | ✗ 피드 없음 |
| Joe Masilotti | masilotti.com | `/feed.xml` 200 ✓ | ✗ ClaudeBot Disallow | 2026-02-12 | ✗ robots.txt 차단 |
| Simon Eskildsen | sirupsen.com | `/atom.xml` 200 ✓ | ✓ | 2026-03-12 ✓ | ✗ 주제 불일치 (수학·분산시스템) |
| Keith Harrison | useyourloaf.com | `/blog/rss.xml` 200 ✓ | ✓ | 2025-11-24 ✓ | ✗ 순수 iOS Swift 튜토리얼 (비즈니스 없음) |
| Paul Hudson | hackingwithswift.com | `/feed.xml` 200 ✓ | ✗ ClaudeBot Disallow | 2026-04 ✓ | ✗ robots.txt 차단 |
| Damon Chen | damonchen.xyz | 000 | N/A | N/A | ✗ 사이트 없음 |
| Arvid Kahl | arvidkahl.com | 405 응답 | N/A | N/A | ✗ 사이트 오류 |
| Daniel Vassallo | dvassallo.com | 모든 경로 404 | ✓ | N/A | ✗ 피드 없음 |
| Majid Jabrayilov | swiftwithmajid.com | `/feed` 200 ✓ | ✓ (empty=open) | 2026-04-06 ✓ | ✗ 순수 SwiftUI 튜토리얼 (비즈니스 없음) |
| Dave Verwer | daveverwer.com | `/feed.xml` 200 ✓ | ✓ | 2021-01-01 ✗ | ✗ 마지막 포스트 2021년 |
| Marco Arment | marco.org | `/rss.xml` 200 ✓ | ✓ (empty=open) | 2026-04-01 ✓ | ✗ 포스트 빈도 매우 낮음 (연 1~2개) |
| Pete Codes | petecodes.io | `/feed/` 200 ✓ | ✓ (no Disallow) | 2026-04-13 ✓ | **✓ 선정** |
| Craig Hockenberry | furbo.org | `/feed/` 200 ✓ | ✓ (GPTBot only) | 2026-03-19 ✓ | **✓ 선정** |
| Brent Simmons | inessential.com | `/xml/rss.xml` 200 ✓ | ✓ (empty=open) | 2026-03-03 ✓ | **✓ 선정** |
| appsfromhome.com | appsfromhome.com | `/feed` → 리다이렉트 | ✓ | N/A | ✗ 피드가 HTML 랜딩 페이지로 리다이렉트 |
| appcheap.io | appcheap.io | `/feed/` 200 ✓ | ✗ ClaudeBot Disallow | 2025-12 ✓ | ✗ robots.txt 차단 |
| indiegamedev.net | indiegamedev.net | `/feed/` 200 ✓ | ✓ | 2022-03-28 ✗ | ✗ 마지막 포스트 2022년 |
| Riley Testut | rileytestut.com | `/feed` 200 ✓ | ✓ (empty=open) | 2025-10-07 ✓ | ✗ 포스트 빈도 너무 낮음 (연 1~2개) |

---

## 선정된 신규 3명

### 1. pete-codes
- URL: https://petecodes.io/
- Feed URL: https://petecodes.io/feed/
- 주제: 인디 개발자로서 사이트 매각·SEO·side-project 수익화 경험 공유, vibe coding
- 최근 포스트 샘플:
  - 2026-04-13: "This is Nantes a drill" (여행 + 개발 병행)
  - 2026-01-23: "Coding with Claude Opus"
  - 2025-11-05: "I'm selling my No CS Degree website" (사이트 매각 의사결정)
- targets.yaml 설정: `adapter: rss`, `category_hint: [startup-philosophy, monetization, product-strategy, career-growth]`, `priority: 3`
- TemperStone 관점 가치: 개인 사이트/앱 매각·수익화 실험 경험, 인디 개발자의 현실적 side-project 운영 인사이트. 포트폴리오 전략보단 인디해킹/모노타이징 관점에서 유용.

### 2. craig-hockenberry
- URL: https://furbo.org/
- Feed URL: https://furbo.org/feed/
- 주제: 베테랑 인디 iOS/Mac 개발자 (Twitterrific 공동창업자), 앱스토어 정책·앱 운영·Apple 플랫폼 인사이트
- 최근 포스트 샘플:
  - 2026-03-19: "Pico Names"
  - 2026-03-14: "Your Mac and a Canon Printer"
  - 2026-01-01: "The Year That Kicked My Ass"
- targets.yaml 설정: `adapter: rss`, `category_hint: [portfolio-ops, product-strategy, dev-tools, aso]`, `priority: 3`
- TemperStone 관점 가치: 20년 이상 인디 앱 운영 경험, App Store 정책 변화 대응, 소규모 팀(사실상 솔로) 제품 유지 철학. 앱 포트폴리오 장기 운영 관점에서 참고가치 높음.

### 3. brent-simmons
- URL: https://inessential.com/
- Feed URL: https://inessential.com/xml/rss.xml
- 주제: NetNewsWire 인디 개발자, 오픈소스 앱 지속 운영·커뮤니티·앱 비즈니스 철학
- 최근 포스트 샘플:
  - 2026-03-03: "I Tried to Explain What I Do"
  - 2026-02-27: "Why Objective-C"
  - 2026-02-18: "Why Not Objective-C"
- targets.yaml 설정: `adapter: rss`, `category_hint: [portfolio-ops, product-strategy, startup-philosophy, dev-tools]`, `priority: 3`
- TemperStone 관점 가치: 오픈소스 앱 무료 배포 → 후원 모델로 지속 운영하는 인디 전략, 개발자 커뮤니티 운영·앱 장수 비결. monetization은 적지만 startup-philosophy와 portfolio-ops 측면에서 독보적.

---

## 타겟 선정 한계 및 다음 세션 권장 사항

### 한계
- 3명 모두 "앱 포트폴리오 + AdMob 수익화 + 대량 출시" 테마에 완벽히 일치하지는 않음.
- 해당 주제(AdMob/대량출시/인디Android)로 RSS 피드가 확인된 독립 블로그가 매우 드뭄.
- 잘 알려진 후보 대부분이 robots.txt 차단(ClaudeBot Disallow), 사이트 응답 없음, 피드 없음 중 하나에 해당.

### 다음 세션 탐색 권장
- **Substack에서 직접 검색**: `app portfolio`, `admob revenue`, `indie android` 키워드로 Substack 내 검색 → 아직 유명하지 않지만 활성화된 뉴스레터 발굴
- **Twitter/X bio 검색**: "indie developer" + "multiple apps" + "admob" 프로필 → 개인 블로그 URL 확인
- **IndieHackers 우회**: individual creator가 개인 블로그를 따로 운영하는 경우 해당 개인 블로그 URL 수집 (IH 프로필 말고)
- **Ghost.io 검색**: Ghost Discovery에서 "app store", "indie iOS", "app revenue" 키워드
- 후보 고려: Thomas Ricouard(dimillian) — Medium이지만 iOS+Agentic 내용 풍부, Medium 어댑터로 수집 가능성 검토
