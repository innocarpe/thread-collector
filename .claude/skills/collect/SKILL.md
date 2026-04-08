---
name: collect
version: 2.0.0
description: |
  Threads.net 유저의 게시글을 GraphQL 페이지네이션으로 전량 수집하고,
  인사이트를 카테고리별로 분류해 마크다운 파일로 저장.
  Usage: /collect @username [--types tech,product,career] [--limit N]
allowed-tools:
  - Bash
  - AskUserQuestion
---

# /collect — ThreadCollector

Threads.net 유저의 게시글을 수집해 `Threads/{username}/` 에 카테고리별 마크다운으로 저장.

실제 로직은 `scripts/collect.py` 에 구현되어 있음. 이 스킬은 중계 역할만 함.

---

## Step 0: 인수 파싱

args에서 username 추출. `@` prefix 있어도 OK.
`--types tech,product,career` 형태로 카테고리 제한 가능.
`--limit N` 으로 최대 배치 수 지정 (기본값: 20).

username 없으면 AskUserQuestion으로 질문.

---

## Step 1: 스크립트 실행

```bash
python3 /Users/WooseongKim/Projects/TemperStone/ThreadCollector/scripts/collect.py @{USERNAME} --limit {LIMIT}
```

타입 지정 시:
```bash
python3 /Users/WooseongKim/Projects/TemperStone/ThreadCollector/scripts/collect.py @{USERNAME} --limit {LIMIT} --types {TYPES}
```

스크립트가 진행상황을 출력함. 에러 발생 시 메시지 확인 후 사용자에게 안내.

---

## Step 2: 완료 확인

스크립트 성공 시 출력:
```
✅ 완료: @{USERNAME} — {N}개 포스트 저장
```

에러 시:
- `browse not found` → gstack browse 설치 안내
- `userID 추출 실패` → `--user-id <ID>` 옵션으로 재시도 안내
- 기타 → 에러 메시지 그대로 사용자에게 전달

---

## 직접 실행 (Codex / 터미널)

```bash
python3 scripts/collect.py @username
python3 scripts/collect.py @username --limit 30
python3 scripts/collect.py @username --types tech,product
python3 scripts/collect.py @username --user-id 12345678901
```
