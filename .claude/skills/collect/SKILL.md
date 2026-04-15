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

실제 로직은 `sources/threads/collect.py` 에 구현되어 있음. 이 스킬은 중계 역할만 함.

기본 동작은 **수집 → classify → insights** 를 한 번에 이어서 실행하는 전체 파이프라인이다. `collect` 요청은 멈추는 지점이 아니라 시작 지점이며, 사용자가 collection-only / classify-only / insights-only를 명시하지 않는 한 끝까지 자동으로 처리한다. 중간에 사용자 확인을 기다리지 말고, 결과적으로 남는 uncategorized가 있으면 classify를 수행하고, 그 뒤 insights를 생성한다.

## 기본 실행 체크리스트

1. `python3 -m sources.threads.collect @{USERNAME}` 실행
2. 수집 결과 확인
3. `uncategorized/`가 있으면 즉시 `python3 -m sources.threads.classify @{USERNAME}` 실행
4. 분류 후 `python3 -m sources.threads.insights @{USERNAME}` 실행
5. `insights/overview.md`, `patterns.md`, `key-posts.md` 생성 여부 확인

---

## Step 0: 사전 조건 확인

처음 실행하는 맥이거나 `pycookiecheat` 설치 여부가 불확실하면:

```bash
python3 -c "import pycookiecheat" 2>&1
```

실패 시 사용자에게 안내:
> `/setup-thread-cookies` 를 먼저 실행해 주세요. (pycookiecheat + Chrome 쿠키 셋업)

그 외에는 바로 진행.

---

## Step 1: 인수 파싱

args에서 username 추출. `@` prefix 있어도 OK.
`--types tech,product,career` 형태로 카테고리 제한 가능.
`--limit N` 으로 최대 배치 수 지정 (기본값: 20).

username 없으면 AskUserQuestion으로 질문.

---

## Step 1: 스크립트 실행

```bash
python3 -m sources.threads.collect @{USERNAME} --limit {LIMIT}
```

타입 지정 시:
```bash
python3 -m sources.threads.collect @{USERNAME} --limit {LIMIT} --types {TYPES}
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
cd "$(git rev-parse --show-toplevel)"
python3 -m sources.threads.collect @username
python3 -m sources.threads.collect @username --limit 30
python3 -m sources.threads.collect @username --types tech,product
python3 -m sources.threads.collect @username --user-id 12345678901
```
