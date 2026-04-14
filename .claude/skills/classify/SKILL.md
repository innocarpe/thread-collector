# /classify — ThreadCollector AI Classifier

`uncategorized/` 폴더의 글들을 codex exec으로 AI 분류.
키워드 매칭에 실패한 글들을 올바른 카테고리로 이동하거나 junk를 삭제.

이 스킬은 보통 `/collect` 직후 자동으로 이어서 실행되며, 분류가 끝나면 이어서 `/insights`까지 생성하는 흐름의 중간 단계다. 사용자가 classify-only를 명시적으로 원하지 않는 한, 단독으로 멈추는 대신 전체 파이프라인의 일부로 취급한다.

---

## Step 1: 인수 파싱

args에서 username 추출. `@` prefix 있어도 OK.

username 없으면 AskUserQuestion으로 질문.

---

## Step 2: 스크립트 실행

```bash
python3 scripts/classify.py @{USERNAME}
```

스크립트가 진행 상황을 출력함:
- `uncategorized/` 에서 파일 읽기
- codex exec으로 배치 분류
- 올바른 카테고리 폴더로 이동
- junk는 삭제

---

## Step 3: 완료 확인

성공 시 출력:
```
ClassifyCollector done — @{USERNAME}
  → tech-dev/  +N
  → product-business/  +N
  → career-philosophy/  +N
  Skipped (junk/irrelevant): N
```

에러 시:
- `No uncategorized/ folder` → /collect 먼저 실행 안내
- codex 인증 오류 → `codex login` 안내
- timeout → 재시도 안내

---

## 직접 실행

```bash
cd "$(git rev-parse --show-toplevel)"
python3 scripts/classify.py @username
python3 scripts/classify.py @username --output-dir /path/to/Threads
```

ARGUMENTS: (username extracted from args by the skill)
