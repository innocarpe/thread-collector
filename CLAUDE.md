# ThreadCollector

Threads.net 유저의 게시글 및 네이버 카페 게시글을 수집해서 인사이트를 카테고리별 마크다운으로 저장하는 도구.

## 프로젝트 구조

```
ThreadCollector/
├── .claude/skills/collect/SKILL.md        # /collect 스킬 (Threads)
├── .claude/skills/classify/SKILL.md       # /classify 스킬
├── .claude/skills/insights/SKILL.md       # /insights 스킬
├── scripts/collect.py                     # Threads 수집 + 키워드 분류
├── scripts/collect_naver.py               # NaverCafe 수집 (비공식 API)
├── scripts/classify.py                    # AI 재분류 (codex exec)
├── scripts/insights.py                    # 인사이트 생성 (codex exec)
├── Threads/                               # Threads 수집 결과
│   └── {username}/
│       ├── tech-dev/
│       ├── product-business/
│       ├── career-philosophy/
│       ├── uncategorized/
│       └── insights/
└── NaverCafe/                             # NaverCafe 수집 결과
    └── {cafe_slug}/                       # 예: vibemoney
        ├── income-methods/                # 수익화 방법
        ├── tools-ai/                      # 도구/AI/자동화
        ├── case-studies/                  # 성공 사례/후기
        ├── marketing/                     # 마케팅/콘텐츠
        ├── uncategorized/                 # 미분류
        └── insights/                      # 인사이트 요약
```

## 알려진 카페 목록 (scripts/collect_naver.py KNOWN_CAFES)

| 카페 슬러그 | clubId | 설명 |
|------------|--------|------|
| vibemoney | 31623270 | 바이브코딩 · 온라인 수익화 카페 |

## Skill routing

When the user's request matches an available skill, ALWAYS invoke it using the Skill
tool as your FIRST action. Do NOT answer directly, do NOT use other tools first.

Key routing rules:
- "/collect", "collect @username", "수집해", "게시글 모아줘", "threads 분석" → invoke `collect` skill
- 특정 유저 인사이트 요청, "@username 글 뽑아줘" → invoke `collect` skill
- "/classify", "분류해", "미분류 정리", "uncategorized 처리" → invoke `classify` skill
- "/insights", "인사이트 뽑아줘", "분석해줘", "overview 만들어" → invoke `insights` skill
- "/run-blog", "블로그 켜줘", "로컬 실행", "dev 서버" → invoke `run-blog` skill
- "/setup-thread-cookies", "쿠키 셋업", "threads 로그인 설정", "새 맥 셋업" → invoke `setup-thread-cookies` skill

## 인사이트 카테고리

기본 분류 체계 (변경 시 SKILL.md도 함께 수정):

| 파일 | 내용 |
|------|------|
| `tech-dev.md` | 기술/개발: 코딩, 아키텍처, 툴, AI, 시스템 설계 |
| `product-business.md` | 프로덕트/비즈니스: PMF, 스타트업, 성장 전략 |
| `career-philosophy.md` | 커리어/철학: 일하는 방식, 마인드셋, 인생관 |

## 워크플로우

### Threads.net

```
# 1. 수집 (키워드 분류, 미분류는 uncategorized/ 보존)
/collect @username
/collect @username --types tech,product     # 특정 카테고리만
/collect @username --limit 30               # 배치 수 제한

# 2. AI 재분류 (uncategorized/ → 올바른 카테고리 or 삭제)
/classify @username

# 3. 인사이트 생성 (overview, patterns, key-posts)
/insights @username
```

### NaverCafe

```
# 수집 (Chrome Profile 7 쿠키 자동 사용)
python3 scripts/collect_naver.py vibemoney              # 전체 수집 (기본 50페이지)
python3 scripts/collect_naver.py vibemoney --limit 10   # 10페이지만 (약 150개)
python3 scripts/collect_naver.py vibemoney --types income,tools  # 특정 카테고리만
python3 scripts/collect_naver.py vibemoney --menu-id 23 # 특정 게시판만

# 새 카페 추가: scripts/collect_naver.py KNOWN_CAFES 딕셔너리에 추가
# 또는 --club-id 직접 지정
python3 scripts/collect_naver.py newcafe --club-id 12345678
```

#### 카테고리 (NaverCafe)

| 폴더 | 설명 |
|------|------|
| `income-methods/` | 수익화 방법, 부업, 매출, 온라인 판매 |
| `tools-ai/` | AI 도구, 자동화, 바이브코딩, 노코드 |
| `case-studies/` | 성공 후기, 실제 사례, 수익 인증 |
| `marketing/` | SNS 마케팅, 콘텐츠, 퍼널, SEO |

## API 설정 (선택사항)

browse 스크래핑 없이 공식 API 사용하려면:

1. [Meta Developer Console](https://developers.facebook.com/apps/) 에서 Threads 앱 생성
2. `.thread-collector-config` 파일 생성:
   ```
   ACCESS_TOKEN=your_token_here
   ```
3. 설정 확인: `python3 scripts/fetch_threads.py --check-config`
