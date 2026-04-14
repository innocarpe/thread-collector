# 2026-04-15 세션에서 추가된 기능 요약

## 새로 쓸 수 있는 Claude Code 스킬

### /discover-threads (확장됨)
기존 Phase 1 멘션 마이닝 + 이번 세션에서 Phase 2/3/4 확장된 범용 discover 스킬.

```bash
# Phase 1 기본 (기존 동작)
/discover-threads

# Phase 2: 프로필 enrichment 추가
/discover-threads  → "프로필까지 같이 보여줘"

# Phase 3.1: 키워드 검색
/discover-threads  → "AI 수익화 키워드로 찾아줘"

# Phase 3.2: 해시태그
/discover-threads  → "해시태그로 유저 찾아줘"

# 직접 실행
python3 scripts/discover_threads.py --sources corpus,search,hashtag --query "바이브코딩" --hashtag ai_llm --enrich
```

---

### /discover-search (신규)
키워드 검색으로 신규 Threads 유저 발굴. Phase 3.1 전용 스킬.

- **트리거**: "키워드로 유저 찾아줘", "'AI 수익화' 로 유저 발굴", "/discover-search"
- **사용 예**: "키워드로 유저 찾아줘: AI 수익화, 바이브코딩"
- **직접 실행**: `python3 scripts/discover_threads.py --sources search --query "AI 수익화" --enrich --enrich-limit 10 --limit 15`
- **주의**: Threads 비공식 REST 엔드포인트, 401/403 가능. `/setup-thread-cookies` 선행 권장.

---

### /discover-hashtag (신규)
해시태그 페이지 스크래핑으로 신규 유저 발굴. Phase 3.2 전용 스킬.

- **트리거**: "해시태그로 유저 찾아줘", "#ai_llm 유저 발굴", "/discover-hashtag"
- **사용 예**: "#ai_llm 해시태그로 유저 찾아"
- **직접 실행**: `python3 scripts/discover_threads.py --sources hashtag --hashtag ai_llm --enrich --enrich-limit 10 --limit 15`
- **주의**: `threads.net/tag/` URL 미공식, 404/파싱 실패 가능. 실패 시 graceful degradation.

---

### /discover-full (신규)
corpus + search + hashtag + enrichment 풀 파이프라인. 가장 넓은 탐색.

- **트리거**: "풀 파이프라인으로 유저 발굴", "모든 소스로 유저 찾아줘", "/discover-full"
- **사용 예**: "풀 파이프라인으로 유저 발굴: 바이브코딩, ai_llm"
- **직접 실행**: `python3 scripts/discover_threads.py --sources corpus,search,hashtag --query "바이브코딩" --hashtag ai_llm --enrich --enrich-limit 15 --limit 25`
- **주의**: 실행 시간 1~2분. 일부 소스 실패해도 나머지 결과 포함.

---

## 기존 스킬도 그대로 쓸 수 있음

| 스킬 | 설명 |
|------|------|
| `/collect @username` | Threads 유저 수집 → classify → insights 자동 연계 |
| `/classify @username` | 미분류 글 10-category AI 재분류 |
| `/insights @username` | 인사이트 생성 |
| `/run-blog` | 블로그 dev 서버 실행 |
| `/setup-thread-cookies` | Chrome 쿠키 셋업 |
| `/collect-naver vibemoney` | NaverCafe 수집 |

---

## 코드 변화 (세션 결과)

- `scripts/discover_threads.py`: 305 → ~1050 라인 (Phase 2/3/4 추가)
- 10-category 재분류 완료 (1507개 글)
- 모바일 사이드바 bottom sheet UX 개선 (blog)
- 인사이트 페이지 UX 개선 (blog)
- hydration 버그 수정 (blog)

---

## 역방향 발견 파이프라인 — 워크플로우 예시

### 키워드로 새 유저 발굴 후 수집
```
1. /discover-search "AI 수익화"   → 검색으로 후보 유저 목록 (리포트 저장)
2. 리포트에서 마음에 드는 유저 확인 (.claude/discover-threads/YYYYMMDD-candidates.md)
3. /collect @handle               → 수집 → classify → insights 자동 실행
4. /run-blog                      → 블로그에서 결과 확인
```

### 해시태그로 커뮤니티 탐색
```
1. /discover-hashtag #ai_llm      → 해시태그 커뮤니티 유저 목록
2. 리포트 확인 후 원하는 유저 선택
3. /collect @handle
```

### 전방위 탐색
```
1. /discover-full 바이브코딩 ai_llm  → corpus + search + hashtag 한 번에
2. discovered_via 배지로 어느 소스에서 발견됐는지 확인
3. /collect @handle
```
