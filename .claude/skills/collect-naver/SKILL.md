---
name: collect-naver
version: 1.0.0
description: |
  네이버 카페 게시글 수집 → AI 분류 → 인사이트 생성 전체 파이프라인.
  Usage: /collect-naver vibemoney [--limit N] [--only-menus 7,22]
allowed-tools:
  - Bash
  - AskUserQuestion
---

# /collect-naver — NaverCafe Collector

네이버 카페 게시글을 수집해 `NaverCafe/{cafe}/` 에 operator/community 분리 저장.
수집 후 uncategorized AI 재분류 → 인사이트 자동 생성까지 한 번에 처리.

---

## Step 1: 인수 파싱

args에서 cafe_name 추출. (예: `vibemoney`, `newcafe`)

cafe_name 없으면 AskUserQuestion:
> "수집할 네이버 카페 슬러그를 알려주세요. (예: vibemoney)"

추가 옵션 파싱:
- `--limit N` → 게시판당 최대 페이지 수 (기본 200)
- `--only-menus 7,22` → 특정 게시판만
- `--collect-only` → 수집만 (classify/insights 생략)
- `--club-id XXXXXXXX` → KNOWN_CAFES에 없는 새 카페

---

## Step 2: 수집

```bash
cd "$(git rev-parse --show-toplevel)"
python3 -m sources.naver_cafe.collect {CAFE} [옵션들]
```

새 카페인 경우 (`--club-id` 필요):
```bash
python3 -m sources.naver_cafe.collect {CAFE} --club-id {CLUB_ID}
```

완료 확인: `NaverCafe Collector 완료 — {CAFE}` 출력 확인.

---

## Step 3: AI 재분류 (uncategorized 있을 때만)

```bash
ls NaverCafe/{CAFE}/community/uncategorized/*.md 2>/dev/null | wc -l
```

1개 이상이면:
```bash
python3 -m sources.naver_cafe.classify {CAFE}
```

완료 확인: `NaverCafe Classifier 완료` 출력 확인.

`--collect-only` 지정 시 Step 3~4 생략.

---

## Step 4: 인사이트 생성

```bash
python3 -m sources.naver_cafe.insights {CAFE}
```

완료 확인: `InsightsCollector 완료` 출력, 파일 9개 생성 확인.

섹션별 단독 실행이 필요하면:
```bash
python3 -m sources.naver_cafe.insights {CAFE} --only operator
python3 -m sources.naver_cafe.insights {CAFE} --only community
python3 -m sources.naver_cafe.insights {CAFE} --only overview
```

---

## Step 5: 결과 요약

수집 완료 후 아래 형식으로 리포트:

```
NaverCafe 수집 완료 — {CAFE}
  수집: N개 (운영자 N / 커뮤니티 N)
  분류: uncategorized N개 → 재분류 N개, 삭제 N개
  인사이트: NaverCafe/{CAFE}/insights/ 9개 파일
```

---

## 알려진 카페

| 슬러그 | clubId | 설명 |
|--------|--------|------|
| vibemoney | 31623270 | 바이브코딩 · 온라인 수익화 |
| shortsyoutuber | 31606881 | 쇼츠 유튜브 운영 · 알고리즘 · 채널 운영 |

새 카페 추가 시 `sources/naver_cafe/collect.py` 의 `KNOWN_CAFES` 딕셔너리에 등록.

### 쇼츠유튜버 기본값
- cafe slug: `shortsyoutuber`
- clubId: `31606881`
- 운영자 닉네임: `쇼츠유튜버`
- 게시판: `1`(자유게시판), `2`(쇼츠 정보게시판), `3`(수강생 숙제 게시판)
- 수집 예시: `python3 -m sources.naver_cafe.collect shortsyoutuber --only-menus 1,2,3`

---

## 에러 처리

- 쿠키 없음 → "Chrome Profile 7에서 네이버 로그인 확인 후 재시도"
- 401 에러 → 네이버 로그아웃 상태. Chrome에서 로그인 후 재시도
- club-id 불명 → `--club-id` 옵션으로 직접 지정 안내
- codex 없음 → `npm install -g @openai/codex` 안내

ARGUMENTS: (cafe_name and options extracted from args by the skill)
