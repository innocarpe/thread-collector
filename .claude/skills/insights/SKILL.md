---
name: insights
version: 3.0.0
description: |
  수집 결과를 codex exec으로 분석해 인사이트를 생성합니다.
  Threads.net 유저(@username)와 NaverCafe(cafe_name) 모두 지원.
allowed-tools:
  - Bash
  - AskUserQuestion
---

# /insights — ThreadCollector Insights Generator

수집된 포스트 전체를 codex exec으로 분석해 `insights/` 폴더 생성.

- **Threads**: `@username` → `Threads/{username}/insights/` (overview, patterns, key-posts)
- **NaverCafe**: `cafe_name` → `NaverCafe/{cafe}/insights/` (operator + community 분리)

이 스킬은 보통 `/collect` → `/classify` 다음에 자동으로 이어서 실행되는 최종 단계다.

---

## Step 1: 인수 파싱 및 대상 판별

args에서 대상 추출.

- `@`로 시작하면 → **Threads 모드**
- `@` 없으면 → **NaverCafe 모드** (예: `vibemoney`)

대상 없으면 AskUserQuestion:
> "인사이트를 생성할 대상을 알려주세요. Threads 유저(@username) 또는 NaverCafe 이름(예: vibemoney)"

---

## Step 2-A: Threads 모드

```bash
cd "$(git rev-parse --show-toplevel)"
python3 scripts/insights.py @{USERNAME}
```

완료 확인:
```
InsightsCollector done — @{USERNAME}
  insights/overview.md
  insights/patterns.md
  insights/key-posts.md
```

---

## Step 2-B: NaverCafe 모드

### 2-B-1. classify 먼저 확인

```bash
ls NaverCafe/{CAFE}/community/uncategorized/*.md 2>/dev/null | wc -l
```

미분류 파일이 있으면 먼저 classify 실행:
```bash
python3 scripts/classify_naver.py {CAFE}
```

### 2-B-2. 인사이트 생성

```bash
cd "$(git rev-parse --show-toplevel)"
python3 scripts/insights_naver.py {CAFE}
```

완료 확인:
```
InsightsCollector 완료 — {CAFE}
  insights/00-overview.md
  insights/operator/full-analysis.md
  insights/operator/income-methods.md
  insights/operator/tools-stack.md
  insights/operator/marketing-tactics.md
  insights/community/income-methods.md
  insights/community/tools-ai.md
  insights/community/case-studies.md
  insights/community/qa-pain-points.md
```

섹션별 단독 실행 옵션:
```bash
python3 scripts/insights_naver.py {CAFE} --only operator
python3 scripts/insights_naver.py {CAFE} --only community
python3 scripts/insights_naver.py {CAFE} --only overview
```

---

## Step 3: 에러 처리

- `No categorized posts` → /collect 후 /classify 먼저 실행 안내
- codex timeout → 재시도 안내
- 파일 미생성 → codex 출력 확인 안내

ARGUMENTS: (대상 extracted from args by the skill)
