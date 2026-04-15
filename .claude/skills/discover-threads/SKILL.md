---
name: discover-threads
description: "기존 코퍼스 멘션 마이닝(Phase 1) + 프로필 enrichment(Phase 2) + 키워드 검색/해시태그(Phase 3) + Explore 스켈레톤(Phase 4) 로 Threads 후보 유저를 발굴해 마크다운 리포트 출력. 사용자가 직접 /collect 할 유저를 고르는 파이프라인의 앞단."
---

# /discover-threads — ThreadCollector User Discovery

기존에 수집한 Threads 포스트들을 스캔해서 **아직 수집 안 된 유저** 중 멘션 빈도와 관심 카테고리 매칭이 좋은 후보를 랭킹한 뒤 마크다운 리포트로 출력한다.

Phase 2 이상을 활성화하면 각 후보의 Threads 프로필(bio, 팔로워 수, 최근 포스트)을 자동으로 enrichment 하고, 키워드 검색/해시태그 페이지로 완전히 새로운 유저를 발굴할 수도 있다.

사용자가 직접 프로필 링크를 열어보고 마음에 드는 유저만 골라서 `/collect @handle` 로 수집하는 "역방향 파이프라인" 의 앞단이다.

---

## 사용 시점

- "트렌드 유저 찾아줘", "요즘 핫한 유저 추천해줘", "새로 누구 수집할지 골라줘"
- "discover", "/discover-threads"
- "멘션된 유저들 정리해줘"
- "해시태그로 유저 찾아줘", "AI 수익화 키워드로 찾아줘"
- "프로필까지 같이 보여줘", "bio 같이 뽑아줘"
- "검색으로 새 유저 찾아줘", "discover 검색", "discover hashtag"

---

## Step 1: 인수 파싱

args 에서 다음 옵션 추출:

### Phase 1 기존 옵션 (기본값으로 Phase 1 동작 유지)

- `--interest ai-llm,monetization` — 관심 카테고리 직접 지정 (overrides auto/파일)
- `--limit 15` — 리포트에 포함할 최대 후보 수 (default 20)
- `--min-mentions 2` — 최소 멘션 횟수, corpus 소스에만 적용 (default 2)
- `--output <경로>` — 리포트 출력 파일 경로 (default `.claude/discover-threads/YYYYMMDD-candidates.md`)
- `--print` — 리포트를 터미널에도 출력

### Phase 2+ 신규 옵션

- `--enrich` — 상위 후보들의 Threads 프로필을 SSR blob 파싱으로 fetch. bio, follower_count, is_private, is_verified, full_name, 최근 포스트 3개 취득. **opt-in, 미지정 시 Phase 1 동작과 동일**.
- `--enrich-limit N` — enrichment 적용 최대 후보 수 (default 10, 속도 조절용)
- `--sources corpus,search,hashtag` — 콤마 구분 소스 목록 (default `corpus`). 가능한 값: `corpus`, `search`, `hashtag`, `explore`.
- `--query "AI 수익화"` — 검색 키워드 (반복 허용: `--query "AI 수익화" --query "바이브코딩"`). `search` 소스 활성화 시 사용.
- `--hashtag ai_llm` — 해시태그 이름 (반복 허용: `--hashtag ai_llm --hashtag indiehacking`). `hashtag` 소스 활성화 시 사용.
- `--weights corpus:3,search:1,hashtag:1` — 소스별 점수 가중치 (default `corpus:3,search:1,hashtag:1,explore:2`)

없으면 default 로 돌린다. **아무 옵션 없이 실행하면 기존 Phase 1 (corpus 멘션 마이닝) 과 완전히 동일하게 동작한다.**

---

## Step 2: 디스커버리 실행

```bash
cd "$(git rev-parse --show-toplevel)"

# Phase 1 기본 (기존 동작, --sources corpus 자동)
python3 -m sources.threads.discover

# Phase 2: 프로필 enrichment 추가
python3 -m sources.threads.discover --enrich

# Phase 3.1: 키워드 검색으로 새 유저 발굴
python3 -m sources.threads.discover --sources search --query "AI 수익화" --enrich

# Phase 3.2: 해시태그 페이지로 새 유저 발굴
python3 -m sources.threads.discover --sources hashtag --hashtag ai_llm --enrich

# 멀티 소스 조합 (corpus + search + hashtag)
python3 -m sources.threads.discover --sources corpus,search,hashtag --query "바이브코딩" --hashtag indiehacking --enrich

# 관심사 / 결과 수 조절
python3 -m sources.threads.discover --interest ai-llm,monetization --limit 30 --min-mentions 3
```

이 스크립트는 소스별로 다음을 수행한다:

### corpus (Phase 1)
1. `Threads/*/` 아래 모든 포스트 스캔 (insights/uncategorized 제외)
2. `@handle` 멘션을 정규식으로 추출, 기존 유저와 노이즈 handle 제거
3. 각 후보의 멘션 빈도, 어느 카테고리 글에서 언급됐는지, 어느 유저가 언급했는지 집계
4. 관심사 해석 우선순위: `--interest` > `.thread-collector-interests.json` > 코퍼스 상위 3개 카테고리 자동 도출

### search (Phase 3.1)
- Threads 비공식 REST `/api/v1/users/search/?q={keyword}&count=20` 호출
- `collect.py` 의 `JS_GET_USERID_API` 패턴(LSD/csrfToken/X-IG-App-ID 헤더 체계) 재사용
- 401/403 응답 시 graceful degradation: 빈 결과 + stderr 경고, 전체 실행 계속

### hashtag (Phase 3.2)
- `threads.net/tag/{tag}` 페이지를 browse_goto 로 접근, SSR blob 파싱으로 유저 목록 추출
- 404/파싱 실패 시 graceful degradation: 빈 결과 + stderr 경고, 전체 실행 계속

### explore (Phase 4 — skeleton)
- `NotImplementedError` stub. 공개 doc_id/엔드포인트 미확인 상태.
- 호출 시 경고 출력 후 해당 소스만 스킵, 전체 실행은 계속.

### enrichment (Phase 2, --enrich 시)
- 각 소스 실행 + merge 완료 후 상위 N명에 대해 프로필 fetch
- `threads.net/@{handle}` 페이지 SSR JSON blob (`<script type="application/json" data-sjs>`) 에서 bio, follower_count, is_private, is_verified, full_name 추출
- 최근 포스트 3개: 기존 `JS_COLLECT(first:3)` 재사용
- fetch 실패 시 `enrich_status` 필드로 표기, 후보 제거 없음

### merge
- 동일 handle 이 여러 소스에서 발견되면 `discovered_via` set 에 모두 추가
- 점수 = `소스별 weighted sum × (1 + topic_match_ratio) × diversity_boost`
- enrichment 후 follower_count 기반 부스트 재계산

---

## Step 3: 결과 보고

사용자에게 간결히 보고:

- 스캔한 포스트/유저 수 (corpus 소스 활성 시)
- 사용된 소스 목록 (`corpus`, `search`, `hashtag` 등)
- 사용된 관심사 + 그 출처(auto / file / CLI)
- 상위 5명 간략 요약 (handle, 점수, 멘션 수, 소스 배지, enrich_status)
- 리포트 파일 경로

리포트에는 각 후보의:
- Threads 프로필 링크
- 소스 배지 (`corpus`, `search`, `hashtag` 등 discovered_via 표기)
- corpus 멘션 컨텍스트 샘플 3개 (corpus 소스 발견 시)
- search 키워드 / hashtag 태그 표기 (해당 소스 발견 시)
- enrichment 정보 (bio, 팔로워 수, 최근 포스트 3개 제목) — `--enrich` 시
- "다음 단계: `/collect @handle`" 가이드

---

## 다음 파이프라인

사용자가 리포트를 읽고 마음에 드는 유저를 고르면:

1. 리포트의 프로필 링크 클릭 → Threads 에서 실제 확인
2. 괜찮으면 → `/collect @handle` 로 수집 시작
3. 기존 collect → classify → insights 파이프라인이 자동 연계

---

## 한계

- **Phase 1 corpus**: 코퍼스가 작거나 폐쇄적이면 후보가 빨리 고갈됨. search/hashtag 소스와 조합 권장.
- **Phase 3.1 search**: Threads 비공식 REST 엔드포인트. 401/403 응답 시 graceful degradation (빈 결과 + 경고). `collect.py` 가 이미 사용 중인 인프라 재사용.
- **Phase 3.2 hashtag**: `threads.net/tag/{name}` URL 패턴은 공식 문서가 없어 404/파싱 실패 가능. 실패 시 graceful degradation (빈 결과 + 경고, 전체 실행 계속).
- **Phase 4 explore**: Explore/For You 피드는 공개 doc_id/엔드포인트 미확인. 현재 `NotImplementedError` skeleton 만 선언. `--sources explore` 지정 시 경고 출력 후 해당 소스만 스킵.
- **enrichment 속도**: 프로필 fetch 는 1.0~2.0초 랜덤 딜레이. 10명 기준 10~20초 추가 소요. `--enrich-limit` 으로 조절 가능.
