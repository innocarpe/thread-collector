---
name: discover-search
description: "키워드 검색으로 Threads.net 신규 유저를 발굴하는 전용 스킬. Threads 비공식 REST search 엔드포인트를 사용해 코퍼스에 없는 완전 신규 유저를 찾는 Phase 3.1 모드."
---

# /discover-search — 키워드 검색으로 신규 Threads 유저 발굴

Threads 비공식 REST 검색 엔드포인트(`/api/v1/users/search/`)를 통해 지정한 키워드에 매칭되는 **완전 신규 유저**를 발굴한다.
기존 코퍼스에 없는 유저를 찾고 싶을 때, 특정 주제 전문가를 직접 검색하고 싶을 때 사용한다.

사용자가 결과 리포트를 보고 마음에 드는 유저를 골라 `/collect @handle` 로 수집하는 "역방향 파이프라인" 의 앞단이다.

---

## 사용 시점

- "키워드로 유저 찾아줘"
- "'AI 수익화' 로 유저 발굴"
- "'바이브코딩' 검색해서 유저 찾아"
- "검색으로 새 Threads 유저 찾아줘"
- "/discover-search"
- "search threads users"
- "키워드 검색으로 발굴"

---

## Step 1: 인수 파싱

사용자 메시지에서 다음을 추출:

- **키워드** — 따옴표 안 문자열, `키워드:`, `쿼리:` 뒤 텍스트, 또는 문맥상 핵심 검색어. 여러 개면 `--query` 반복. **미지정 시 코퍼스 상위 관심사(예: `ai-llm`, `viral-sns`, `monetization`)에서 사전 정의된 키워드를 자동으로 뽑아 사용** — `--query` 생략 가능.
- **결과 수** — "N명", "N개" 언급 시 `--limit N` (기본 15)
- **enrich 수** — 언급 없으면 기본 10 유지

사용자가 키워드를 명시했으면 그대로 사용, 아니면 자동 도출로 진행. 더 이상 되묻지 말 것.

---

## Step 2: 실행

```bash
cd "$(git rev-parse --show-toplevel)"

# 단일 키워드
python3 -m sources.threads.discover \
  --sources search \
  --query "키워드" \
  --enrich \
  --enrich-limit 10 \
  --limit 15

# 복수 키워드
python3 -m sources.threads.discover \
  --sources search \
  --query "AI 수익화" \
  --query "바이브코딩" \
  --enrich \
  --enrich-limit 10 \
  --limit 15

# 결과 수 조절
python3 -m sources.threads.discover \
  --sources search \
  --query "인디해킹" \
  --enrich \
  --enrich-limit 15 \
  --limit 25
```

스크립트 동작:
1. `--sources search` 로 corpus 멘션 마이닝 없이 검색만 실행
2. Threads 비공식 REST `/api/v1/users/search/?q={keyword}&count=20` 호출
3. `collect.py` 의 LSD/csrfToken/X-IG-App-ID 헤더 체계 재사용
4. 결과 merge 후 `--enrich` 로 상위 10명 프로필(bio, 팔로워 수, 최근 포스트 3개) fetch
5. `.claude/discover-threads/YYYYMMDD-candidates.md` 로 리포트 저장

---

## Step 3: 결과 보고

사용자에게 간결히 보고:

- 사용된 키워드 목록
- 발굴된 총 후보 수
- **상위 5명** handle, bio 한 줄, 팔로워 수, 발굴 키워드 표기
- 리포트 파일 경로

형식 예시:
```
🔍 검색 완료 — "AI 수익화", "바이브코딩"
발굴 후보: 23명 → 상위 15명 리포트 저장

상위 5명:
1. @handle_a  |  팔로워 12.3k  |  "AI로 수익화하는 법 공유합니다"
2. @handle_b  |  팔로워 8.1k   |  "바이브코딩으로 SaaS 만들기"
...

리포트: .claude/discover-threads/20260415-candidates.md
다음 단계: 마음에 드는 유저를 골라 `/collect @handle` 실행
```

---

## 다음 파이프라인

사용자가 리포트를 보고 유저를 선택하면:

1. 리포트의 Threads 프로필 링크 클릭 → 실제 계정 확인
2. 괜찮으면 → `/collect @handle` 로 수집 시작
3. 기존 `collect → classify → insights` 파이프라인 자동 연계

---

## 한계

- **401/403 오류**: Threads 비공식 REST 엔드포인트는 인증 실패 가능. 실패 시 graceful degradation (빈 결과 + stderr 경고, 전체 실행 계속). `/setup-thread-cookies` 로 쿠키를 셋업한 뒤 재시도 권장.
- **쿠키 선행 필요**: Chrome Profile 쿠키가 없으면 검색 자체가 실패할 수 있음. 처음 사용 시 `/setup-thread-cookies` 먼저 실행.
- **검색 품질**: 비공식 엔드포인트라 결과 정확도가 공식 검색과 다를 수 있음. 키워드를 한국어/영어 병행 사용 권장.
- **enrichment 속도**: 프로필 fetch 는 1~2초 랜덤 딜레이. 10명 기준 10~20초 추가 소요. `--enrich-limit` 으로 조절 가능.
