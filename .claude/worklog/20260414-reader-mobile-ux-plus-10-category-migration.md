# 2026-04-14: 리더 모바일 UX 개선 + 10개 카테고리 재분류

## 배경

1. **모바일 UX 문제**: 사이드바 (Users / Category / Status / 토픽 4섹션 × 총 ~20 항목) 가 모바일 첫 화면을 통째로 차지해서 글 리스트까지 스크롤이 한참 걸렸다. 이전 세션에서 다른 에이전트가 손본 grid 3컬럼 레이아웃은 유저명 잘림 + 모바일 수직 스크롤 먹통 현상까지 유발한 상태였다.
2. **인사이트 페이지**: `/insights/[username]` 상단 '홈으로' 버튼 디자인이 어색하고, 탭 사이 hydration mismatch (`Text content did not match`) 가 `MarkdownBody` 에서 발생.
3. **카테고리 체계**: 1541개 글인데 카테고리가 `tech-dev / product-business / career-philosophy` 3개뿐이라 카테고리 필터가 실질적인 브라우징 도구가 아니었다. 반면 `labels` (토픽) 에는 이미 19종 세분화가 돼 있음.

## 원인 분석

### 사이드바 레이아웃 (ffd0208)
- 이전 에이전트가 `.filter-item-row` 를 `grid-template-columns: minmax(0, 2fr) minmax(80px, 1fr) minmax(70px, auto)` 로 잡아, FilterItem 이 충분한 폭을 못 가져가고 유저명이 잘림.
- 모바일에서 `.sidebar { overflow-y: auto }` 가 터치 스크롤을 가로채어 페이지 전체 스크롤이 안 되는 버그.

### Hydration mismatch (d33b35c)
- `lib/posts.ts` 의 excerpt 생성이 `bodyText.slice(0, 150)` — UTF-16 code unit 기준. 이모지 `😵‍💫` (U+1F635 서러게이트 페어 + ZWJ + U+1F4AB) 의 중간에서 잘리면 lone surrogate 가 남아 서버 HTML 과 클라이언트 렌더 결과가 달라짐.

### 카테고리 과소화 (ea3d14d)
- 3개 카테고리로는 1541개 글을 의미 있게 나눌 수 없고, 각 카테고리당 ~500개가 몰려 브라우징 도구로서 기능을 못함.
- `collect.py` 의 키워드 휴리스틱 기반 초기 분류도 coarse (3개로만 분기).

## 수정 내역

### 코드 변경

| 커밋 | scope | 내용 |
|------|-------|------|
| ffd0208 | blog | `.filter-item-row` grid → flex, `.insights-pill` 28×28 원형, 모바일 `.sidebar { overflow: visible }` |
| d1f63dc | blog | `/insights/[username]` 신규, `.post-back` 스타일 '홈으로', 3단 헤더 (eyebrow/title/subtitle) + 섹션 구분선 |
| d33b35c | blog | `lib/posts.ts`: `Array.from(bodyText).slice(0,150).join("")` 로 code point 단위 슬라이스 |
| 55de162 | blog | `components/reader/filter-sheet.tsx` 신규 (Provider/Trigger/Panel), Context 로 `openId` 싱글톤 관리, 데스크톱은 `display: contents` 로 투명화, 모바일은 `position: fixed` 바텀시트 + 4섹션 독립 패널. `SidebarReaderFilters` 에 `section?: "status"\|"topics"` prop 추가 |
| ea3d14d | classify | `types/post.ts` 10개 카테고리 교체, `scripts/classify.py` `CATEGORY_DESCRIPTIONS` 테이블 + 새 프롬프트 (주제 우선 배정 룰), `scripts/collect.py` 키워드 초기분류 제거 (always None), `CLAUDE.md` / classify SKILL 문서 갱신 |

### 데이터 마이그레이션 (674ca99)

- 파일럿: `@ai_margin_` (97개) → 7개 카테고리에 분산, frontmatter `category` 자동 갱신 확인 후 전체 적용
- 나머지 9명 백그라운드 batch: `appnomad_lab → vibeceo.log → side.money_story → ai.trend.ray → brxce.ai → dalgom.bami → dev_shibaa → kongkey__ → specal1849` 순으로 classify.py 호출
- 1521 file changes, 27188 insertions, 1145 deletions

**최종 분포** (1507개, junk 34개 skip):

| 카테고리 | 개수 | 비중 |
|----------|------|------|
| viral-sns | 439 | 29.1% |
| ai-llm | 380 | 25.2% |
| monetization | 189 | 12.5% |
| startup-philosophy | 118 | 7.8% |
| dev-tools | 104 | 6.9% |
| productivity | 95 | 6.3% |
| learning-retro | 78 | 5.2% |
| career-growth | 43 | 2.9% |
| web-app | 35 | 2.3% |
| product-strategy | 26 | 1.7% |

## 배포

- 배포 없음 (로컬 dev 서버 `localhost:3000` 에서만 검증)
- `npx tsc --noEmit` 모두 통과
- 사용자가 PC/모바일 브라우저에서 수동 확인 완료

## PR

PR 없음, 로컬 main 에 직접 커밋 (이 리포는 solo 운영).

## 다음 단계

1. **분류 품질 튜닝**: dev-tools vs ai-llm 경계 케이스 ("구글 AI 스튜디오", "openclaw") 가 섞임. 필요시 프롬프트에 "AI 도구 리뷰는 ai-llm" 룰 추가
2. **product-strategy / career-growth / web-app** 가 1.7~2.9% 로 낮음. 실제로 글이 적은 건지, 아니면 classify 가 해당 카테고리를 덜 선택하는지 분포 모니터링 필요
3. **collect.py 의 `categorize()` 를 지웠으므로**, 신규 수집 글은 전부 `uncategorized/` 로 들어감. `/collect → /classify` 파이프라인을 항상 쌍으로 돌리는 게 필수가 됨 (기존 CLAUDE.md 워크플로우 그대로 OK)
4. **모바일 바텀시트 UX**: 트리거 4개가 grid 2열로 배치돼 2+2 로 쌓임. 트리거 개수가 바뀌면 (예: 토픽 조건부 숨김) 레이아웃이 어색해질 수 있음 — flex wrap 고려

## 핵심 교훈

1. **"UI 이슈"로 보이는 것도 데이터 모델 문제일 수 있다.** "카테고리가 너무 적다"는 불만은 결국 택소노미 설계 문제였고, 이미 `labels` 에 필요한 세분화가 존재하고 있었다. 코드를 건드리기 전에 먼저 데이터 분포를 확인 (`grep labels:` 으로 19종 추출) 한 뒤 방향을 잡은 게 옳았음.

2. **React hydration 에러는 100% 결정론적 원인을 찾아야 한다.** `Text content did not match` 는 서버/클라이언트 렌더 결과가 1바이트라도 다르면 난다. emoji + `slice()` = lone surrogate 가 전형적인 원인. 앞으로 사용자 텍스트를 길이로 자르는 모든 곳은 code point 단위여야 한다 (`Array.from().slice().join()`).

3. **탐색적 질문에 바로 구현 들어가지 말기.** 사용자가 "어떻게 풀까" 라고 물으면 2–3 문장 제안 + 트레이드오프로 답하고 승인 받은 뒤 실행. 특히 재분류같은 데이터 마이그레이션은 파일럿 먼저 돌려 품질 확인 → 전체 배치. 파일럿 없이 1500개 돌렸으면 프롬프트 튜닝 기회 없이 다 끝났을 것.

4. **데스크톱/모바일 한 번에 커버하는 패턴: `display: contents`.** 같은 JSX 트리에서 모바일은 `position: fixed` 오버레이, 데스크톱은 inline 레이아웃으로 쓸 때, 컨테이너를 `display: contents` 로 두면 자식이 부모에 직접 flow 된다. 중복 렌더나 React portal 없이 해결됨. 단 `all: unset` 을 먼저 넣어 기존 클래스 스타일을 리셋해야 충돌 안 남.

5. **globals.css 처럼 여러 에이전트가 만지는 파일은 diff stat 으로 항상 확인.** 이번에 다른 에이전트가 marked 라이브러리 도입 커밋 (aac3835) 을 만들면서 내 filter-sheet CSS 블록을 함께 absorb 해버려서, 내 commit 1 에서는 TSX 만 올리면 되는 상황이었음. git status 를 먼저 안 봤으면 "어? CSS 가 안 보이네" 하고 헤맸을 수 있음.
