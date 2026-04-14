# 2026-04-15: /discover-threads Phase 2~4 완성

## 배경

어제(2026-04-14) 세션에서 `/discover-threads` Phase 1 (코퍼스 멘션 마이닝) 을 스킬로 출시했다. 오늘 세션에서 Phase 2~4 로 확장하는 게 목표였다:
- **Phase 2**: 후보 프로필을 browse 로 fetch 해서 bio + follower + 최근 포스트 3개로 enrich
- **Phase 3.1**: 키워드 검색 API 로 완전 신규 유저 발굴
- **Phase 3.2**: 해시태그 페이지 스크래핑
- **Phase 4**: Explore/For You 피드 스켈레톤

사용자 요청이 단순 "한 기능 추가" 가 아니라 "모든 phase 를 한 번에, 에이전트 팀 병렬로 끝까지" 였으므로 `/core:run-with-agent-team` 스프린트 모드로 진행.

## 원인 분석 / 리서치 결과

4명 scout 병렬 조사로 확보한 핵심 발견:

- **scout-1 (browse/GraphQL 인벤토리)**: `scripts/collect.py` 의 `_resolve_browse_cmd`, `browse_goto`, `browse_eval`, `parse_json_output`, `JS_GET_USERID`, `JS_COLLECT`, `JS_GET_USERID_API` 가 모두 재사용 가능. 현재 유일하게 사용 중인 GraphQL doc_id 는 `26348619898139541` (포스트 페이지네이션). 프로필/search 용 신규 doc_id 는 미구현 상태.

- **scout-2 (프로필 enrichment 방법)**: Threads 프로필 페이지에 Relay SSR JSON blob (`<script type="application/json" data-sjs>`) 이 이미 포함돼 있어 bio / follower_count / is_private / is_verified / full_name 을 별도 GraphQL 호출 없이 추출 가능. doc_id `23996318473300828` fallback 도 있지만 SSR 파싱이 더 안정적. 이 방법이 Phase 2 구현의 핵심.

- **scout-3 (검색/Explore 엔드포인트)**: `/api/v1/users/search/?q={keyword}&count={n}` 비공식 REST 가 **이미 `collect.py:106` 의 `JS_GET_USERID_API` 에서 사용 중**. 신규 인프라 필요 없음. 해시태그는 `threads.net/tag/{name}` URL 의 SSR 파싱으로 가능하지만 실증 필요. Explore/For You 피드는 공개 doc_id 전무 → skeleton 만 가능.

- **scout-4 (아키텍처 설계)**: 단일 파일 유지 (패키지 분할 시 `from label import label_file` 같은 import 경로 깨짐 리스크). 소스 plugin 은 ABC 아닌 **함수 포인터 dict**. `Candidate` 확장 + `DiscoverConfig` 신설. `--enrich` opt-in 으로 Phase 1 기본 동작 유지.

3개 제안서 중 **제안 C (Phase 2+3.1+3.2+4)** 승인.

## 수정 내역

### 코드 (scripts/discover_threads.py)

`builder-1` 이 305 → ~1050 라인으로 확장. 7-commit atomic 분할 후 형태:

| 커밋 | 내용 |
|------|------|
| `554e3f6` chore | browse helper (`_dt_*`) 인라인 복사 + JS 템플릿 5종 (`JS_ENRICH_PROFILE`, `JS_SEARCH_USERS`, `JS_HASHTAG_AUTHORS`, `JS_GET_USERID_DT`, `JS_COLLECT_RECENT`) + `Candidate` 확장 + `DiscoverConfig` 신설 |
| `28e3bb6` feat | Phase 2: `enrich_candidate()` + `_fetch_recent_posts()` + `--enrich` / `--enrich-limit` |
| `228b42b` refactor | 멀티소스 인프라: `discover_corpus` 래퍼, `DISCOVERY_SOURCES` dict, `merge_candidates`, `--sources` / `--weights` CLI |
| `4fe6435` feat | Phase 3.1: `discover_search()` + `--query` |
| `17f9b89` feat | Phase 3.2: `discover_hashtag()` + `--hashtag` |
| `7567d05` feat | Phase 4: `discover_explore()` NotImplementedError stub |
| `1280498` docs | SKILL.md + CLAUDE.md routing |
| `7102fd7` fix | main() 주석 정합성 |

이후 live 검증 중 발견한 버그 2건 수정:

| 커밋 | 버그 | 원인 | 수정 |
|------|------|------|------|
| `c708205` | 리포트 렌더링 시 한글 깨짐 + `UnicodeEncodeError: surrogates not allowed` | SSR blob 정규식으로 추출한 `bio`/`full_name` 에 `\uXXXX` 리터럴이 남아 `json.loads` 후에도 escape 문자열 그대로. `chr()` 개별 변환 시 서러게이트 페어 (U+D800~DFFF) 를 lone surrogate 로 만들어 encode 실패 | `_decode_unicode_escapes()` 헬퍼 추가. 서러게이트 페어를 먼저 U+10000+ 으로 합산한 뒤 나머지 처리 |
| `87a1cb3` | Phase 3.1 search 가 NetworkError 로 실패 | `_dt_browse_goto("https://www.threads.net")` 요청이 `threads.com` 으로 리다이렉트 → `.com` 컨텍스트에서 `.net/api/v1/users/search/` fetch 가 **cross-origin 차단**. Desktop UA 로 `requests` 호출하면 `400 "useragent mismatch"` 반환 | browse eval 경로 포기, `_build_search_session()` (pycookiecheat + LSD 정규식 추출) + `_search_users_python()` (Instagram mobile UA `Instagram 303.0.0.11.111 Android ...`) 로 Python requests 직접 호출 |

### 신규 특화 스킬 3개 (f8a1ee3)

사용자가 CLI 옵션을 외울 필요 없이 자연어로 호출 가능하도록 모드별 스킬 분리:

| 파일 | 트리거 예시 | 실행 명령 |
|------|------------|----------|
| `.claude/skills/discover-search/SKILL.md` | "키워드로 유저 찾아줘: AI 수익화" | `--sources search --query ... --enrich` |
| `.claude/skills/discover-hashtag/SKILL.md` | "#ai_llm 해시태그로 유저 발굴" | `--sources hashtag --hashtag ... --enrich` |
| `.claude/skills/discover-full/SKILL.md` | "풀 파이프라인으로 유저 발굴" | `--sources corpus,search,hashtag --enrich` |

기존 `/discover-threads` 는 범용 fallback 으로 유지. CLAUDE.md routing 표에 3개 신규 규칙이 범용 라인 **앞에** 추가되어 구체 매칭 우선.

### 세션 기능 요약 문서

`.claude/session-features-20260415.md` — 이 세션에서 추가된 기능 / CLI 옵션 / 워크플로우 예시를 한 페이지로 정리. "이번에 뭐 만들었지?" 를 방지.

## 배포

배포 없음, 로컬 `main` 직접 커밋 (solo 레포). `npx tsc --noEmit` 해당 없음 (Python 스크립트). Python syntax 검증 `ast.parse` 통과 + Phase 1 회귀 테스트 (`python3 scripts/discover_threads.py --min-mentions 2`) 매 레이어마다 통과.

Live 검증 (실제 browse + 쿠키 사용):
- Phase 1 corpus: 16 candidates, top-5 handle 동일 ✅
- Phase 2 enrich: `@tofukyung` 등 상위 3명 bio/팔로워/recent_posts 채워짐 ✅
- Phase 3.1 search: "AI LLM" 단일 query 55명, "바이브코딩" 40명 ✅
- Phase 3.2 hashtag: `indiehacking` 태그 20명. `ai_llm` 태그 0명 (SSR 구조상 username 필드 없음, graceful) ✅
- Phase 4 explore: NotImplementedError → main() try/except catch → 경고 출력 후 다른 소스 계속 ✅
- 멀티소스 merge: corpus + search 조합에서 handle 중복 병합 + discovered_via set 합집합 + 가중치 적용 ✅

## PR

없음 (solo 레포, 직접 main).

## 다음 단계

1. **`ai_margin_` 같이 대규모 corpus 유저에서 `/discover-full` 재실행** 해서 실제 신규 후보 풀을 확인해보기. 지금 16명 corpus + 55명 search 결과가 있으니 enrichment 돌려서 진짜 수집할 유저 픽업.
2. **hashtag SSR 파서 개선**: 현재 `ai_llm` 같은 일부 태그 페이지에서 0명 반환. threads.net/tag/{name} 구조가 키워드별로 다른 게 원인일 수 있음. 다른 태그 5~10개 샘플링 후 파싱 패턴 보완.
3. **Python requests 경로를 Phase 3.2 hashtag 에도 적용 고려**: Phase 3.1 search 는 browse eval 을 완전히 포기하고 requests 로 이관했지만, hashtag 는 여전히 browse 기반. 만약 hashtag 도 cross-origin 같은 이슈가 있으면 동일 패턴으로 이관 가능.
4. **score 절댓값 3배 문제**: corpus_weight=3.0 도입으로 Phase 1 대비 score 수치가 3배. 상대 순위는 동일해서 기능 문제는 없지만 SKILL.md 에 안내 한 줄 추가하면 혼란 방지.
5. **collect_naver.py None/skip 버그**: 어제 worklog 에서 "시한폭탄" 으로 지목했는데 이번 세션에선 못 건드렸음. 다음 세션 우선순위.

## 핵심 교훈

1. **외부 진단의 "아키텍처 변경 필요" 주장은 재검증할 것.** Task B 검증 팀원은 Phase 3.1 NetworkError 를 "headless context 의 cross-page XHR 차단 → 아키텍처 변경 없이 해결 불가" 로 판정했지만 실제 원인은 전혀 달랐다 (`.net` → `.com` 리다이렉트로 인한 cross-origin 차단 + User-Agent 불일치). 반증 증거 (`collect.py` 에서 같은 엔드포인트를 정상 사용 중) 가 있으면 진단을 의심하고 다시 파보는 게 맞다. 포기 선언 전 반드시 "다른 곳에선 왜 되는가" 를 물을 것.

2. **브라우저 eval 과 직접 HTTP 호출은 완전히 다른 path.** Threads 같은 강한 anti-bot 사이트에서 브라우저 컨텍스트는 쿠키/세션/LSD 토큰/Referer 가 자동 세팅되는 이점이 있지만, cross-origin 제약이 있다. 반대로 Python requests 경로는 UA/헤더/쿠키/토큰을 모두 수동 조립해야 하지만 origin 제약이 없다. **"브라우저 기반 fallback → Python 직접 호출"** 은 내 도구 상자의 표준 패턴으로 기억할 것.

3. **Unicode escape 는 두 번 디코드될 수 있다.** SSR blob 에 `biography: "\uBC30\uB2C8..."` 같은 JS escape 가 있고 이를 Python 정규식으로 뽑으면 **리터럴 문자열** `\uBC30\uB2C8...` 가 된다. `json.loads` 는 필드 값 안의 escape 를 또 해석하지 않는다. `chr(int(...))` 로 개별 변환은 BMP 밖 이모지/수식 문자의 서러게이트 페어를 lone surrogate 로 만들어 encode 실패로 이어진다. 해결: 서러게이트 페어를 먼저 U+10000+ 으로 합산해야 한다. 이 패턴은 JSON 데이터를 정규식으로 뽑는 곳 어디서나 재발 가능.

4. **팀 스프린트 모드의 7-commit 되감기는 정밀 작업.** 단일 파일 ~750 라인 증가분을 7개 레이어로 나누려면 각 레이어마다 컴파일 + Phase 1 회귀 테스트 + 커밋 루프가 필요. 기계적이지만 한 번 잘못하면 정합성 깨짐. commit splitter 에이전트를 별도로 spawn 해 전담시키는 게 리더가 직접 하는 것보다 안전하고 병렬화 가능. 작업을 끝낸 뒤 마지막에 `diff {backup} {현재}` 로 정합성 검증은 필수.

5. **신규 기능 문서는 "사용자가 자연어로 호출 가능한가" 를 기준으로 설계.** 기존 `/discover-threads` 가 Phase 1~4 를 전부 지원하지만 옵션 (`--enrich`, `--sources`, `--query`, `--hashtag`, `--weights`) 이 복잡해 사용자가 기억하기 어렵다. 해결: 모드별 특화 스킬 (`/discover-search`, `/discover-hashtag`, `/discover-full`) 을 별도로 만들어 한국어 트리거로 호출 가능하게. CLAUDE.md routing 순서도 구체적인 것이 먼저 매칭되도록 배치.

6. **디버깅 세션에 별도 agent 스폰이 빠르다.** Task B 검증 agent 는 "아키텍처 변경 필요" 로 결론냈지만, fixer agent 를 새로 만들어 "진짜 원인 찾아라" 명령하니 20분 만에 해결했다. 기존 agent 의 컨텍스트 (포기 선언) 를 물려받지 않는 게 디버깅에 유리. 클린 시작이 답을 더 잘 찾는다.
