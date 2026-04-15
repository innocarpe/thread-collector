# sources/blog — 블로그 수집 모듈

## 목적

인디 개발자·창업자의 블로그(개인 블로그·Medium·Substack·Tistory 등) 글을 수집해  
**복제 가능한 전략·전술**을 카테고리별 인사이트로 추출한다.  
Threads.net 코퍼스와 상호 보완하여, 짧은 SNS 게시글에서 포착하기 어려운  
장문의 성장 기록·사례 연구·기술 결정 배경을 확보하는 것이 핵심 목표다.

---

## 현재 상태

**Phase 1 스켈레톤** — 구조 정의 및 타겟 리스트만 존재.  
실제 fetch/parse 로직은 **Phase 2A**에서 `sources/blog/adapters/` 하위에 구현한다.

---

## 아키텍처

### BlogAdapter Protocol

`sources/blog/collect.py`에 선언된 `BlogAdapter` Protocol을 모든 adapter가 구현해야 한다.

```
BlogAdapter
  .discover_posts(root_url) → list[PostRef]   # 피드·sitemap·HTML 파싱, 글 목록 반환
  .fetch_post(post_ref)     → Post             # 본문 + 메타데이터 fetch
  .detect_language(post)    → str              # 언어 감지 (ko, en 등)
```

### 자동 감지 순서 (adapter: auto)

```
rss → sitemap → tistory → generic_html
```

1. **rss**: `<root>/feed`, `<root>/rss`, `<root>/atom.xml` 등 RSS/Atom 피드 시도
2. **sitemap**: `<root>/sitemap.xml` → `<loc>` 태그에서 글 URL 추출
3. **tistory**: Tistory 도메인 감지 시 전용 파서 사용 (페이지네이션 처리 포함)
4. **generic_html**: 위 모두 실패 시 HTML 링크 크롤링

### adapter 종류

| adapter | 대상 |
|---------|------|
| `rss` | RSS/Atom 피드를 제공하는 일반 블로그 |
| `sitemap` | sitemap.xml 기반 크롤링 |
| `tistory` | Tistory 전용 파서 |
| `medium` | Medium 프로필 페이지 (공개 글 한정) |
| `substack` | Substack 뉴스레터 (공개 글 한정) |
| `generic_html` | RSS/sitemap 없는 일반 HTML 페이지 |
| `auto` | 위 순서대로 자동 감지 |

---

## 저장 레이아웃

```
Blog/
└── {creator-slug}/
    ├── ai-llm/
    ├── viral-sns/
    ├── monetization/
    ├── dev-tools/
    ├── product-strategy/
    ├── startup-philosophy/
    ├── career-growth/
    ├── learning-retro/
    ├── productivity/
    ├── web-app/
    ├── portfolio-ops/     ← 신규 (Phase 2)
    ├── aso/               ← 신규 (Phase 2)
    ├── case-study/        ← 신규 (Phase 2)
    ├── uncategorized/
    └── insights/
        ├── overview.md
        ├── patterns.md
        └── key-posts.md
```

- 파일명: `{slug}.md` (canonical URL에서 마지막 path segment 기반 생성)
- Threads/ 폴더와 동형 구조 → `lib/posts.ts` 에서 `BLOG_DIR` 상수 추가만으로 동일 루프 재사용 가능
- frontmatter에 `sourceType: "blog"` 필드로 출처 구분

### frontmatter 스키마 (블로그 포스트)

```yaml
---
sourceType: "blog"
source: "https://soulduse.tistory.com/123"
creator: "programmingzombie"
url: "https://soulduse.tistory.com/123"
canonical_url: "https://soulduse.tistory.com/123"
title: "포스트 제목"
published_at: "2025-06-26"          # ISO 8601 날짜
collected_at: "2026-04-15T10:00:00" # 수집 시각 (ISO 8601)
categories: ["dev-tools", "monetization"]
lang: "ko"
---
```

---

## 증분 수집 (dedup)

- `canonical_url` + `published_at` 조합을 기준으로 중복 판별
- 이미 존재하는 파일은 재수집하지 않음 (force 옵션으로 강제 재수집 가능)
- 각 creator 디렉토리에 `.collected_urls` 캐시 파일 관리 (Phase 2A 구현)

---

## Rate Limiting

- 기본값: **2초** (요청 사이 sleep)
- `targets.yaml`의 `rate_limit_sec` 필드로 creator별 override
- Medium·Substack은 1초, Tistory·generic_html은 2초 기본

---

## robots.txt 준수

- 각 adapter는 수집 시작 전 `<root>/robots.txt` 확인
- `Disallow:` 경로가 포함된 URL은 skip
- `User-agent: *` 기준 적용
- robots.txt 파싱 실패 시 수집 진행 (fail-open)

---

## 실패 로깅

```
sources/blog/logs/{creator-slug}-{YYYYMMDD}.log
```

- 각 수집 세션별 로그 파일 생성
- 로그 항목: 수집 URL, HTTP 상태 코드, skip 사유, 에러 메시지
- 오래된 로그(30일 이상)는 자동 정리 (Phase 2A 구현)

---

## extract_insights 스키마 (글 1개 단위)

각 블로그 포스트에서 추출하는 인사이트 구조:

| 필드 | 설명 | 제약 |
|------|------|------|
| `source` | 원문 URL | — |
| `creator` | creator slug | — |
| `url` | 수집 URL | — |
| `title` | 포스트 제목 | — |
| `published_at` | 발행일 (ISO 8601) | — |
| `collected_at` | 수집 시각 (ISO 8601) | — |
| `categories` | 분류 카테고리 슬러그 목록 | 1~3개 |
| `key_claims` | 핵심 주장·논점 | 최대 5개 |
| `metrics` | 공개된 숫자·지표 (MAU, 매출, 전환율 등) | — |
| `tools_mentioned` | 언급 도구·서비스 | — |
| `creators_mentioned` | 언급된 다른 creator·앱 | — |
| `tactics` | 복제 가능한 전술 | 최대 3개 |
| `summary` | 원문 요약 | 최대 5문장 |
| `full_content` | 원문 전체 (마크다운) | — |

---

## 법적·윤리 원칙

- **개인 사용 전용** — 수집 결과의 재판매·재배포 금지
- **저작권 표시 보존** — 원문 frontmatter에 source URL 필수 기재
- **로그인 필요 블로그 제외** — 인증 우회 없이 공개 글만 수집
- **운영자 실명·회사명 유출 금지** — TemperStone 스텔스 운영 기간 준수 (2026-06-30까지)
- **robots.txt 준수** — Disallow 경로 skip (위 항목 참조)
- **Rate limiting** — 서버 부하 최소화 (최소 1초 간격)

---

## 10명 Creator 리스트

Phase 2C 타겟(최우선): **programmingzombie** (soulduse.tistory.com)

| 우선순위 | slug | 이름 | URL | adapter |
|----------|------|------|-----|---------|
| 1 | `programmingzombie` | 프로그래밍좀비 (soulduse) | soulduse.tistory.com | auto |
| 2 | `sebastian-rohl` | Sebastian Röhl (HabitKit) | sebastianroehl.substack.com | substack |
| 3 | `max-artemov` | Max Artemov | indiehackers.com/product/max-artemov | generic_html |
| 3 | `adam-lyttle` | Adam Lyttle | starterstory.com / indiehackers.com | generic_html |
| 3 | `hussein-el-feky` | Hussein El Feky | hfeky.medium.com | medium |
| 4 | `roman-koch` | Roman Koch | medium.com/@romankoch | medium |
| 4 | `yuma-ueno` | Yuma Ueno | medium.com/@yumaueno | medium |
| 4 | `adam-wathan` | Adam Wathan | adamwathan.me | rss |
| 4 | `josh-manders` | Josh Manders | joshmanders.com | rss |
| 4 | `weyoume` | WeYouMe | mydevspace.blogspot.com | generic_html |

전체 설정: `sources/blog/targets.yaml` 참조

---

## Phase 로드맵

### Phase 2A: adapters 실구현
- `sources/blog/adapters/rss.py` — RSS/Atom 파서
- `sources/blog/adapters/sitemap.py` — sitemap.xml 파서
- `sources/blog/adapters/tistory.py` — Tistory 전용 크롤러
- `sources/blog/adapters/generic_html.py` — 범용 HTML 크롤러
- `sources/blog/adapters/medium.py` — Medium 공개 글 파서
- `sources/blog/adapters/substack.py` — Substack 공개 글 파서
- `sources/blog/collect.py` main() 구현 — targets.yaml 로드 → adapter 자동 선택 → 수집 루프

### Phase 2B: extract_insights.py
- `sources/blog/extract_insights.py` — codex exec 기반 구조화 인사이트 추출
- 위 extract_insights 스키마에 따라 글별 YAML 인사이트 생성
- `/insights` 스킬에 blog 소스 통합

### Phase 2C: programmingzombie 전량 수집 + 인사이트 (최우선)
- soulduse.tistory.com 전량 수집 (tistory adapter 사용)
- 카테고리 분류 (`classify.py` 또는 adapter 내 자동 분류)
- `Blog/programmingzombie/insights/` 생성 (overview, patterns, key-posts)
- Threads 코퍼스와 교차 분석

### Phase 3: 나머지 9명 수집
- priority 2~4 creator 순서대로 수집
- 언어별(ko/en) 분리 처리

### Phase 4: HQ 문서로 propagate
- `Blog/*/insights/` → HQ 문서 `02-제품/apps/전략/크리에이터-인사이트/` 로 요약 전파
- Threads 인사이트와 통합 리포트 생성
