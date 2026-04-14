---
name: discover-full
description: "corpus 멘션 마이닝 + 키워드 검색 + 해시태그 스크래핑 + enrichment를 한 번에 실행하는 멀티소스 풀 파이프라인 스킬. 가장 넓은 그물로 Threads 신규 유저를 발굴한다."
---

# /discover-full — 멀티소스 풀 파이프라인으로 Threads 유저 발굴

corpus 멘션 마이닝(Phase 1) + 키워드 검색(Phase 3.1) + 해시태그 스크래핑(Phase 3.2) + 프로필 enrichment(Phase 2) 를 한 번에 실행해 **가장 넓은 범위**에서 후보 유저를 발굴한다.

단일 소스보다 다양하고 풍부한 후보 목록을 얻고 싶을 때, 또는 특정 주제에 대한 전방위 탐색을 원할 때 사용한다.

사용자가 결과 리포트를 보고 마음에 드는 유저를 골라 `/collect @handle` 로 수집하는 "역방향 파이프라인" 의 앞단이다.

---

## 사용 시점

- "풀 파이프라인으로 유저 발굴"
- "모든 소스로 유저 찾아줘"
- "완전 탐색 모드"
- "/discover-full"
- "discover all"
- "corpus + 검색 + 해시태그 다 써서 찾아줘"
- "멀티소스로 발굴해줘"

---

## Step 1: 인수 파싱

사용자 메시지에서 다음을 추출:

- **키워드** (`--query`) — "키워드:", "검색어:", 따옴표 안 텍스트, 또는 문맥상 핵심 단어. 여러 개 가능.
- **해시태그** (`--hashtag`) — `#` 포함/미포함 모두 OK. 여러 개 가능.
- **결과 수** — "N명", "N개" 언급 시 `--limit N` (기본 25)
- **enrich 수** — 언급 없으면 기본 15 유지

키워드/해시태그 모두 없는 경우:
- corpus 소스는 키워드 없이 자동 실행 (`.thread-collector-interests.json` 또는 자동 도출)
- search/hashtag 소스는 skip (경고 없이 corpus 결과만)
- 또는 사용자에게 확인:
  > 키워드나 해시태그가 있으면 더 넓게 탐색할 수 있어요. 없으면 코퍼스 멘션 마이닝만 실행합니다. 계속할까요?

---

## Step 2: 실행

```bash
cd "$(git rev-parse --show-toplevel)"

# 풀 파이프라인 (corpus + search + hashtag)
python3 scripts/discover_threads.py \
  --sources corpus,search,hashtag \
  --query "AI 수익화" \
  --hashtag ai_llm \
  --enrich \
  --enrich-limit 15 \
  --limit 25

# 키워드 여러 개 + 해시태그 여러 개
python3 scripts/discover_threads.py \
  --sources corpus,search,hashtag \
  --query "바이브코딩" \
  --query "인디해킹" \
  --hashtag ai_llm \
  --hashtag indiehacking \
  --enrich \
  --enrich-limit 15 \
  --limit 25

# corpus만 있을 때 (키워드/해시태그 없는 경우)
python3 scripts/discover_threads.py \
  --sources corpus \
  --enrich \
  --enrich-limit 15 \
  --limit 25
```

스크립트 동작:
1. **corpus**: 기존 Threads 포스트에서 `@handle` 멘션 추출 + 빈도·카테고리 집계
2. **search**: `/api/v1/users/search/?q={keyword}` 로 완전 신규 유저 발굴 (각 키워드별)
3. **hashtag**: `threads.net/tag/{tag}` SSR blob 파싱 (각 해시태그별)
4. **merge**: 동일 handle이 여러 소스에서 발견되면 `discovered_via` set 에 모두 추가, 점수 = `소스별 weighted sum × (1 + topic_match_ratio) × diversity_boost`
5. **enrichment**: 상위 15명 프로필(bio, 팔로워 수, 최근 포스트 3개) fetch
6. `.claude/discover-threads/YYYYMMDD-candidates.md` 로 리포트 저장

---

## Step 3: 결과 보고

사용자에게 간결히 보고:

- 사용된 소스 목록 + 키워드/해시태그
- 소스별 발굴 수 (corpus N명, search N명, hashtag N명)
- 멀티소스 중복 후보 (corpus + search 모두에서 발견된 유저 등)
- **상위 10명** handle, bio 한 줄, 팔로워 수, discovered_via 배지
- 리포트 파일 경로

형식 예시:
```
모든 소스 탐색 완료
  corpus:  14명
  search:  19명 ("AI 수익화", "바이브코딩")
  hashtag: 11명 (#ai_llm, #indiehacking)
  → 중복 제거 후 31명, 상위 25명 리포트 저장

상위 10명:
1. @handle_a  |  팔로워 22k  |  "AI 수익화 전문"  |  [corpus][search]
2. @handle_b  |  팔로워 9k   |  "1인 SaaS 빌더"   |  [search][hashtag]
...

리포트: .claude/discover-threads/20260415-candidates.md
다음 단계: 마음에 드는 유저를 골라 `/collect @handle` 실행
```

실패 소스가 있으면:
```
⚠️  search: 401 응답 (쿠키 만료 가능) — corpus/hashtag 결과는 정상 포함됨
```

---

## 다음 파이프라인

사용자가 리포트를 보고 유저를 선택하면:

1. 리포트의 Threads 프로필 링크 클릭 → 실제 계정 확인
2. 괜찮으면 → `/collect @handle` 로 수집 시작
3. 기존 `collect → classify → insights` 파이프라인 자동 연계

---

## 한계

- **실행 시간**: search/hashtag live fetch + enrichment 15명 ≈ 1~2분. 단일 소스보다 현저히 오래 걸림. 빠른 탐색이 목적이면 `/discover-search` 또는 `/discover-hashtag` 권장.
- **일부 소스 실패**: 각 소스는 독립적으로 실행되므로 한 소스가 실패해도 나머지 결과는 정상 포함. 최종 리포트에 소스별 상태 표기.
- **401/403 (search)**: Threads 비공식 REST 엔드포인트. 실패 시 search 소스만 빈 결과 처리, 전체 실행 계속.
- **404/파싱 실패 (hashtag)**: `threads.net/tag/{name}` URL 패턴 미공식. 실패 시 해당 해시태그만 빈 결과, 전체 실행 계속.
- **쿠키 선행 필요**: `/setup-thread-cookies` 로 Chrome 쿠키가 셋업돼 있어야 search/hashtag 소스 정상 동작.
- **Phase 4 explore**: `--sources` 에 `explore` 추가 시 `NotImplementedError` 경고 후 해당 소스만 skip.
