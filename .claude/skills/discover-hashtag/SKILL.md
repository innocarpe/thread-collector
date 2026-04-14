---
name: discover-hashtag
description: "해시태그 페이지 스크래핑으로 Threads.net 신규 유저를 발굴하는 전용 스킬. threads.net/tag/ SSR 파싱으로 특정 해시태그 커뮤니티의 유저를 찾는 Phase 3.2 모드."
---

# /discover-hashtag — 해시태그로 신규 Threads 유저 발굴

`threads.net/tag/{tag}` 페이지를 SSR blob 파싱으로 스크래핑해서 특정 해시태그를 사용하는 **신규 유저**를 발굴한다.
관심 키워드의 커뮤니티에서 활동 중인 유저를 찾고 싶을 때 사용한다.

사용자가 결과 리포트를 보고 마음에 드는 유저를 골라 `/collect @handle` 로 수집하는 "역방향 파이프라인" 의 앞단이다.

---

## 사용 시점

- "해시태그로 유저 찾아줘"
- "#ai_llm 유저 발굴"
- "해시태그 ai_llm 으로 찾아"
- "해시태그 검색으로 발굴"
- "/discover-hashtag"
- "hashtag search"
- "#바이브코딩 유저들 찾아줘"

---

## Step 1: 인수 파싱

사용자 메시지에서 다음을 추출:

- **해시태그 이름** — `#` 포함/미포함 모두 OK. `#ai_llm` → `ai_llm` 으로 정규화. 여러 개면 `--hashtag` 반복. **미지정 시 코퍼스 상위 관심사에서 사전 정의된 해시태그를 자동으로 뽑아 사용** — `--hashtag` 생략 가능.
- **결과 수** — "N명", "N개" 언급 시 `--limit N` (기본 15)
- **enrich 수** — 언급 없으면 기본 10 유지

사용자가 해시태그를 명시했으면 그대로 사용, 아니면 자동 도출로 진행. 더 이상 되묻지 말 것.

---

## Step 2: 실행

```bash
cd "$(git rev-parse --show-toplevel)"

# 단일 해시태그
python3 scripts/discover_threads.py \
  --sources hashtag \
  --hashtag ai_llm \
  --enrich \
  --enrich-limit 10 \
  --limit 15

# 복수 해시태그
python3 scripts/discover_threads.py \
  --sources hashtag \
  --hashtag ai_llm \
  --hashtag indiehacking \
  --enrich \
  --enrich-limit 10 \
  --limit 15

# 결과 수 조절
python3 scripts/discover_threads.py \
  --sources hashtag \
  --hashtag 바이브코딩 \
  --enrich \
  --enrich-limit 15 \
  --limit 25
```

스크립트 동작:
1. `--sources hashtag` 로 corpus 멘션 마이닝 없이 해시태그 페이지만 스크래핑
2. `threads.net/tag/{tag}` 페이지를 browse_goto 로 접근, SSR blob 파싱으로 유저 목록 추출
3. 결과 merge 후 `--enrich` 로 상위 10명 프로필(bio, 팔로워 수, 최근 포스트 3개) fetch
4. `.claude/discover-threads/YYYYMMDD-candidates.md` 로 리포트 저장

---

## Step 3: 결과 보고

사용자에게 간결히 보고:

- 사용된 해시태그 목록
- 발굴된 총 후보 수 (성공한 해시태그만)
- **상위 5명** handle, bio 한 줄, 팔로워 수, 발굴 해시태그 배지
- 실패한 해시태그가 있으면 경고와 함께 안내
- 리포트 파일 경로

형식 예시:
```
#️⃣ 해시태그 스크래핑 완료 — #ai_llm, #indiehacking
발굴 후보: 18명 → 상위 15명 리포트 저장

상위 5명:
1. @handle_a  |  팔로워 9.2k  |  "AI 툴로 수익화 실험 중"  |  #ai_llm
2. @handle_b  |  팔로워 5.4k  |  "1인 SaaS 빌더"           |  #indiehacking
...

리포트: .claude/discover-threads/20260415-candidates.md
다음 단계: 마음에 드는 유저를 골라 `/collect @handle` 실행
```

실패 해시태그가 있으면:
```
⚠️  #some_tag: 404 또는 파싱 실패 — 나머지 해시태그는 정상 처리됨
```

---

## 다음 파이프라인

사용자가 리포트를 보고 유저를 선택하면:

1. 리포트의 Threads 프로필 링크 클릭 → 실제 계정 확인
2. 괜찮으면 → `/collect @handle` 로 수집 시작
3. 기존 `collect → classify → insights` 파이프라인 자동 연계

---

## 한계

- **404/파싱 실패**: `threads.net/tag/{name}` URL 패턴은 공식 문서가 없어 404 또는 SSR blob 파싱 실패 가능. 실패 시 graceful degradation (빈 결과 + stderr 경고, 전체 실행 계속).
- **쿠키 선행 필요**: `/setup-thread-cookies` 로 Chrome 쿠키가 셋업돼 있어야 페이지 접근 가능. 초기 설정 없이 실행하면 빈 결과 또는 인증 오류 발생.
- **해시태그 명칭**: 한국어 해시태그는 URL 인코딩 문제로 실패할 수 있음. 영어/언더스코어 형태(`ai_llm`, `vibecoding`) 병행 시도 권장.
- **enrichment 속도**: 프로필 fetch 는 1~2초 랜덤 딜레이. 10명 기준 10~20초 추가 소요. `--enrich-limit` 으로 조절 가능.
