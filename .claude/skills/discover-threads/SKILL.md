---
name: discover-threads
description: "기존 코퍼스에서 아직 수집 안 된 Threads 후보 유저를 발굴해 마크다운 리포트로 출력. 사용자가 직접 /collect 할 유저를 고르는 파이프라인의 앞단."
---

# /discover-threads — ThreadCollector User Discovery

기존에 수집한 Threads 포스트들을 스캔해서 **아직 수집 안 된 유저** 중 멘션 빈도와 관심 카테고리 매칭이 좋은 후보를 랭킹한 뒤 마크다운 리포트로 출력한다.

사용자가 직접 프로필 링크를 열어보고 마음에 드는 유저만 골라서 `/collect @handle` 로 수집하는 "역방향 파이프라인" 의 앞단이다.

---

## 사용 시점

- "트렌드 유저 찾아줘", "요즘 핫한 유저 추천해줘", "새로 누구 수집할지 골라줘"
- "discover", "/discover-threads"
- "멘션된 유저들 정리해줘"

---

## Step 1: 인수 파싱

args 에서 다음 옵션 추출:

- `--interest ai-llm,monetization` — 관심 카테고리 직접 지정 (overrides auto/파일)
- `--limit 15` — 리포트에 포함할 최대 후보 수 (default 20)
- `--min-mentions 2` — 최소 멘션 횟수 (default 2)
- `--print` — 리포트를 터미널에도 출력

없으면 default 로 돌린다.

---

## Step 2: 디스커버리 실행

```bash
cd "$(git rev-parse --show-toplevel)"
python3 scripts/discover_threads.py [옵션...]
```

이 스크립트는:

1. `Threads/*/` 아래 모든 포스트 스캔 (insights/uncategorized 제외)
2. `@handle` 멘션을 정규식으로 추출, 기존 유저와 노이즈 handle 제거
3. 각 후보의 멘션 빈도, 어느 카테고리 글에서 언급됐는지, 어느 유저가 언급했는지 집계
4. 관심사 해석 우선순위: `--interest` > `.thread-collector-interests.json` > 코퍼스 상위 3개 카테고리 자동 도출
5. 점수 = `mentions × (1 + topic_match_ratio) × diversity_boost`
6. `.claude/discover-threads/YYYYMMDD-candidates.md` 로 랭킹 리포트 작성

---

## Step 3: 결과 보고

사용자에게 간결히 보고:

- 스캔한 포스트/유저 수
- 사용된 관심사 + 그 출처(auto / file / CLI)
- 상위 5명 간략 요약 (handle, 멘션 수, 주요 카테고리)
- 리포트 파일 경로

리포트에는 각 후보의 Threads 프로필 링크, 멘션 컨텍스트 샘플 3개, 그리고 "다음 단계: `/collect @handle`" 가이드가 포함된다.

---

## 다음 파이프라인

사용자가 리포트를 읽고 마음에 드는 유저를 고르면:

1. 리포트의 프로필 링크 클릭 → Threads 에서 실제 확인
2. 괜찮으면 → `/collect @handle` 로 수집 시작
3. 기존 collect → classify → insights 파이프라인이 자동 연계

---

## 한계

- **Phase 1**: 현재는 기존 코퍼스 멘션 마이닝만 지원. 코퍼스가 작거나 폐쇄적이면 후보가 빨리 고갈됨.
- **Phase 2 (예정)**: 각 후보의 Threads 프로필을 browse 로 fetch 해 bio + 최근 포스트로 enrichment
- **Phase 3 (예정)**: Threads 검색 API 직접 호출로 완전히 새 유저 발견
- **해시태그 기반 발견**은 코퍼스 내 해시태그가 마크다운 앵커 fragment 수준의 노이즈밖에 없어 Phase 에서 제외함.
