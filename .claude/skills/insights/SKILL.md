# /insights — ThreadCollector Insights Generator

수집된 포스트 전체를 codex exec으로 분석해 `insights/` 폴더 생성.
`overview.md`, `patterns.md`, `key-posts.md` 3개 파일 작성.

---

## Step 1: 인수 파싱

args에서 username 추출. `@` prefix 있어도 OK.

username 없으면 AskUserQuestion으로 질문.

---

## Step 2: 스크립트 실행

```bash
python3 /Users/WooseongKim/Projects/Temperstone/thread-collector/scripts/insights.py @{USERNAME}
```

스크립트가 진행 상황을 출력함:
- 카테고리별 포스트 수 확인
- codex exec으로 전체 분석 (60-120초 소요)
- insights/ 파일 3개 생성

---

## Step 3: 완료 확인

성공 시 출력:
```
InsightsCollector done — @{USERNAME}
  insights/overview.md  (N bytes)
  insights/patterns.md  (N bytes)
  insights/key-posts.md  (N bytes)
```

에러 시:
- `No categorized posts` → /collect 후 /classify 먼저 실행 안내
- codex timeout → 재시도 안내
- 파일 미생성 → codex 출력 확인 안내

---

## 직접 실행

```bash
python3 scripts/insights.py @username
python3 scripts/insights.py @username --output-dir /path/to/Threads
```

ARGUMENTS: (username extracted from args by the skill)
