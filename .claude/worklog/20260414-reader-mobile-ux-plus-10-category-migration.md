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

## 후속 작업 — dev-tools ↔ ai-llm 경계 재분류 (같은 세션 저녁)

오후 분류 결과를 스팟체크한 결과 `dev-tools` (104개) 에 Claude Code / Cursor / openclaw / Google AI Studio 같은 **AI 코딩 어시스턴트 리뷰** 가 상당수 섞여 있음을 발견 — classifier 가 "AI 도구" 를 "dev 도구" 로 일관되게 해석하는 편향.

### 수정

| 커밋 | 내용 |
|------|------|
| `12aa9e5` | **classify.py 치명 버그 수정**: codex 가 결과를 안 주면(rate limit, timeout, parse fail) `cat = None` 이 되어 "skip" 과 똑같이 `unlink()` 해버리는 문제. 오늘 codex 크레딧 소진 재분류 시 104개 파일이 전부 삭제되기 직전에 발견. `cat is None` 과 `cat == "skip"` 분리, None 이면 uncategorized 에 남겨 재시도 가능하게. 배치 시작 시 tmp_output 선제 삭제, 실패 시 codex stderr tail 출력. 같은 커밋에 프롬프트 튜닝 ("AI 도구·LLM 제품 리뷰는 ai-llm, dev-tools 는 비-AI 도구에 한정") 포함. |
| `d461c67` | **Haiku 서브에이전트로 104 → 재분류**: codex 대신 Claude Haiku 에이전트 호출. 매니페스트 JSON (74KB) 생성 → Agent 호출 → `/tmp/dev_tools_out.json` → python 적용 스크립트로 파일 이동 + frontmatter 갱신. |

### 재분류 결과 (dev-tools 104개 → 재분산)

| 대상 | 개수 |
|------|------|
| ai-llm | +53 |
| learning-retro | +22 |
| viral-sns | +11 |
| web-app | +5 |
| productivity | +3 |
| product-strategy | +3 |
| monetization | +1 |
| career-growth | +1 |
| dev-tools (유지) | 5 |

최종 분포는 ai-llm 380 → 433, dev-tools 104 → 5. 남은 5 는 진짜 비-AI 개발 도구 (블로그 자동화, 터미널 워크플로우, supabase CLI, Google Workspace 자동화 등).

### apply 스크립트 버그

`/tmp/apply_dt_reclass.py` 가 `src == target` (dev-tools → dev-tools) 인 경우에 `write_text()` 로 덮어쓴 다음 `unlink()` 해서 방금 쓴 파일을 지움. 5개 survivor 는 `git checkout HEAD --` 로 즉시 복구. 스크립트는 /tmp 에 있는 일회성이라 수정 안 함.

## 후속 작업 — Memory Architecture 부트스트랩

이 프로젝트는 이미 `.claude/memory/` scaffold (scripts/vault symlink) 와 `.claude/settings.json` 의 memory hook 이 canonical 상태였지만, auto-memory 경로 `~/.claude/projects/-Users-WooseongKim-Projects-Temperstone-thread-collector/memory/MEMORY.md` 가 아예 없어서 `/debrief` 가 worklog-only fallback 으로 빠지고 있었음. 추가로 `.gitignore` 에 memory block 도 누락.

### 수정

- `~/.claude/projects/…/memory/MEMORY.md` 실파일 생성 (symlink 아님)
- `.gitignore` 에 `# Memory Architecture` + `.claude/memory/.cache/` + `.claude/memory/vault/` 추가

`vaults/thread-collector` 는 sibling 들과 달리 iCloud symlink 가 아닌 **실제 디렉토리**로 존재. 기존 선택을 존중해 변환하지 않음.

## PR

PR 없음, 로컬 main 에 직접 커밋 (이 리포는 solo 운영).

## 다음 단계

1. ~~**dev-tools vs ai-llm 경계 재분류**~~ — 완료 (`12aa9e5`, `d461c67`)
2. **product-strategy / career-growth / web-app** 는 스팟체크 결과 모두 정상 분포로 판정, 튜닝 불필요
3. **collect.py 의 `categorize()` 를 지웠으므로**, 신규 수집 글은 전부 `uncategorized/` 로 들어감. `/collect → /classify` 파이프라인을 항상 쌍으로 돌리는 게 필수가 됨
4. **모바일 바텀시트 UX**: 트리거 4개가 grid 2열로 배치돼 2+2 로 쌓임. 트리거 개수가 바뀌면 (예: 토픽 조건부 숨김) 레이아웃이 어색해질 수 있음 — flex wrap 고려
5. **apply 스크립트 패턴 개선**: src==target 케이스 방어 (파일 이동 스크립트 작성 시 항상 체크할 것)

## 핵심 교훈

1. **"UI 이슈"로 보이는 것도 데이터 모델 문제일 수 있다.** "카테고리가 너무 적다"는 불만은 결국 택소노미 설계 문제였고, 이미 `labels` 에 필요한 세분화가 존재하고 있었다. 코드를 건드리기 전에 먼저 데이터 분포를 확인 (`grep labels:` 으로 19종 추출) 한 뒤 방향을 잡은 게 옳았음.

2. **React hydration 에러는 100% 결정론적 원인을 찾아야 한다.** `Text content did not match` 는 서버/클라이언트 렌더 결과가 1바이트라도 다르면 난다. emoji + `slice()` = lone surrogate 가 전형적인 원인. 앞으로 사용자 텍스트를 길이로 자르는 모든 곳은 code point 단위여야 한다 (`Array.from().slice().join()`).

3. **탐색적 질문에 바로 구현 들어가지 말기.** 사용자가 "어떻게 풀까" 라고 물으면 2–3 문장 제안 + 트레이드오프로 답하고 승인 받은 뒤 실행. 특히 재분류같은 데이터 마이그레이션은 파일럿 먼저 돌려 품질 확인 → 전체 배치. 파일럿 없이 1500개 돌렸으면 프롬프트 튜닝 기회 없이 다 끝났을 것.

4. **데스크톱/모바일 한 번에 커버하는 패턴: `display: contents`.** 같은 JSX 트리에서 모바일은 `position: fixed` 오버레이, 데스크톱은 inline 레이아웃으로 쓸 때, 컨테이너를 `display: contents` 로 두면 자식이 부모에 직접 flow 된다. 중복 렌더나 React portal 없이 해결됨. 단 `all: unset` 을 먼저 넣어 기존 클래스 스타일을 리셋해야 충돌 안 남.

5. **globals.css 처럼 여러 에이전트가 만지는 파일은 diff stat 으로 항상 확인.** 이번에 다른 에이전트가 marked 라이브러리 도입 커밋 (aac3835) 을 만들면서 내 filter-sheet CSS 블록을 함께 absorb 해버려서, 내 commit 1 에서는 TSX 만 올리면 되는 상황이었음. git status 를 먼저 안 봤으면 "어? CSS 가 안 보이네" 하고 헤맸을 수 있음.

6. **codex exec 같은 외부 CLI 호출 스크립트는 `stdout == ""` 을 "skip" 과 엄격히 구분해야 한다.** classify.py 가 codex의 rate-limit 실패를 조용히 "junk → unlink" 로 변환해서 104개 파일을 지울 뻔했다. 일반화: **외부 도구가 실패했을 때의 기본값은 `destructive action` 이 아니라 `no-op + retry` 여야 한다**. write/delete 를 수행하는 스크립트는 "결과 없음 == 실패" 분기를 먼저 그려라.

7. **codex 크레딧 소진 시 대안: Claude Haiku via Agent 도구.** 104개 분류는 Haiku 에이전트 한 번 호출로 30초 내외에 끝남. codex 가 실패해도 매니페스트만 JSON 으로 빌드하면 교체 가능. 앞으로 codex 의존 스크립트는 이 fallback 경로를 염두에 두는 게 좋음.

8. **파일 이동 스크립트는 `src == target` 방어 필수.** apply_dt_reclass.py 가 write→unlink 순서로 동작해서 동일 경로 이동 시 파일을 지웠다. 항상 `if src.resolve() != target.resolve()` 체크 후 이동.
